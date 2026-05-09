# =============================================================================
# APC64Manager.py — Gestión y configuración del APC64
# =============================================================================

from functools import partial
from .Boton import Boton
from .APC64Controls import APC64Controls as C


class APC64Manager:
    """
    Gestiona toda la configuración del APC64: controles, listeners, botones y modos.
    Recibe una referencia al parent (ExampleActions) para acceder a sus métodos.
    """

    def __init__(self, parent):
        self.parent = parent
        self.cs     = None
        self._init_estado()

    # ------------------------------------------------------------------
    # ESTADO INTERNO
    # ------------------------------------------------------------------

    def _init_estado(self):
        self.botonMute       = None
        self.botonSolo       = None
        self.botonArm        = None
        self.botonLoopPos    = None
        self.botonLoopLen    = None
        self.botonLoopOffset = None
        self.botonLoopOnOff  = None
        self.botonMacro1     = None
        self.botonMacro2     = None
        self.botonMacro3     = None
        self.botonMacro4     = None

        self._device_button_listeners        = []
        self._channel_strip_button_listeners = []
        self._shift_button_listeners         = []
        self._record_arm_orig_listeners         = []

        self._banco_device       = 0
        self._long_press_pending = {}
        self._track_state_2_modo = 0
        self.record_arm_state = 0
    # ------------------------------------------------------------------
    # SETUP PRINCIPAL
    # ------------------------------------------------------------------

    def setup(self, control_surface):
        """Configura el APC64 completo. Llamar tras obtener el control surface."""
        self.cs = control_surface

        self._config_encoder()
        self._config_track_select_buttons()
        self._config_touch_elements()
        self._config_track_state_buttons()
        self._config_pads()
        self._config_matrix()
        self._config_modos()

        record_arm = self.cs.get_control_by_name(C.RECORD_ARM)
        self._record_arm_orig_listeners = self.get_listeners(record_arm)
        boton = Boton(C.RECORD_ARM, 22, 3, self)
        boton.accion_on  = lambda: self._on_record_arm(0)
        boton.accion_continua = False
        boton.crear_control(self.cs)


        self.log("APC64Manager: configurado correctamente")

    # ------------------------------------------------------------------
    # CONFIGURACIÓN DE CONTROLES
    # ------------------------------------------------------------------

    def _config_encoder(self):
        control = self.cs.get_control_by_name(C.ENCODER)
        self.limpiar_listeners(control)
        control.add_value_listener(self.parent.encoder_value)

        control = self.cs.get_control_by_name(C.ENCODER_BUTTON)
        if not control.value_has_listener(self.parent.encoder_buton):
            control.add_value_listener(self.parent.encoder_buton)

    def _config_track_select_buttons(self):
        for i in range(8):
            self.addControl(
                C.track_select_buttons()[i],
                color=None,
                accion=partial(self.parent.cambia_pista, i + 1)
            )

    def _config_touch_elements(self):
        for i in range(8):
            self.addControl(
                C.touch_elements()[i],
                color=None,
                accion=partial(self.parent.select_param, C.touch_elements()[i], i)
            )

    def _config_track_state_buttons(self):
        for nombre in C.track_state_buttons():
            self.limpiar_listeners(self.cs.get_control_by_name(nombre))

        boton = Boton(C.TRACK_STATE_0, 22, 9, self)
        boton.accion_on = lambda: self.parent.action("(PSEQ) $BTN_1_APC$")
        boton.crear_control(self.cs)

        for nombre in (C.TRACK_STATE_1, C.TRACK_STATE_3, C.TRACK_STATE_5):
            boton = Boton(nombre, 0, 0, self)
            boton.crear_control(self.cs)

        boton = Boton(C.TRACK_STATE_2, 22, 4, self, False, True)
        boton.accion_on  = lambda: self.modo_directo(True)
        boton.accion_off = lambda: self.modo_directo(False)
        boton.crear_control(self.cs)

        boton = Boton(C.TRACK_STATE_4, 22, 22, self)
        boton.accion_on = lambda: self.parent.action("DEV VAR 1; DEV VARRECALL")
        boton.crear_control(self.cs)

        boton = Boton(C.TRACK_STATE_6, 22, 12, self, accion_continua=True)
        self.limpiar_listeners(self.cs.get_control_by_name(C.TRACK_STATE_6))
        boton.accion_on = partial(self.parent.cambia_valor, -1)
        boton.crear_control(self.cs)

        boton = Boton(C.TRACK_STATE_7, 22, 12, self, accion_continua=True)
        self.limpiar_listeners(self.cs.get_control_by_name(C.TRACK_STATE_7))
        boton.accion_on = partial(self.parent.cambia_valor, 1)
        boton.crear_control(self.cs)

        device_control        = self.cs.get_control_by_name(C.DEVICE)
        channel_strip_control = self.cs.get_control_by_name(C.CHANNEL_STRIP)
        shift_control         = self.cs.get_control_by_name(C.SHIFT)

        self._device_button_listeners        = self.get_listeners(device_control)
        self._channel_strip_button_listeners = self.get_listeners(channel_strip_control)
        self._shift_button_listeners         = self.get_listeners(shift_control)

        control2 = self.cs.get_control_by_name(C.TRACK_STATE_1)
        self.limpiar_listeners(control2)
        device_control.add_value_listener(self.toggle_banco_device)

        scene7 = self.cs.get_control_by_name(C.SCENE_LAUNCH_7)
        self.limpiar_listeners(scene7)
        self.asignar_listeners(scene7, self._shift_button_listeners)




    def _config_pads(self):
        for nombre in C.pads_fila(7):
            self.limpiar_listeners(self.cs.get_control_by_name(nombre))

        self.botonMute = self._crear_boton(C.PAD_5_7, 22, 9)
        self.botonSolo = self._crear_boton(C.PAD_6_7, 22, 41)
        self.botonArm  = self._crear_boton(C.PAD_7_7, 22, 5)

        macros = [
            (C.PAD_0_7, "$PARAM_MD_1$ $PARAM_MD_1_INCREMENTO$ ", "$PARAM_MD_1_RESET$"),
            (C.PAD_1_7, "$PARAM_MD_2$ $PARAM_MD_2_INCREMENTO$ ", "$PARAM_MD_2_RESET$"),
            (C.PAD_2_7, "$PARAM_MD_3$ $PARAM_MD_3_INCREMENTO$ ", "$PARAM_MD_3_RESET$"),
            (C.PAD_3_7, "$PARAM_MD_4$ $PARAM_MD_4_INCREMENTO$ ", "$PARAM_MD_4_RESET$"),
        ]
        macro_refs = []
        for nombre, accion_on_str, accion_off_str in macros:
            boton = Boton(nombre, 22, 3, self)
            boton.accion_on       = lambda s=accion_on_str:  self.parent.action(s)
            boton.accion_off      = lambda s=accion_off_str: self.parent.action(s)
            boton.accion_continua = True
            boton.crear_control(self.cs)
            boton.activar_control(False)
            macro_refs.append(boton)

        self.botonMacro1, self.botonMacro2, self.botonMacro3, self.botonMacro4 = macro_refs

    def _crear_boton(self, nombre, color_on, color_off):
        boton = Boton(nombre, color_on, color_off, self)
        boton.crear_control(self.cs)
        return boton

    def _config_matrix(self):
        matrix = self.cs.get_control_by_name(C.PADS)
        for button in matrix:
            if not button.value_has_listener(self._on_pad_press):
                button.add_value_listener(self._on_pad_press)

        scenes = self.cs.get_control_by_name(C.SCENE_LAUNCH_BUTTONS)
        for button in scenes:
            if not button.value_has_listener(self._on_pad_press):
                button.add_value_listener(self._on_pad_press)

    def _config_modos(self):
        self.modo_edicion_clip(False)
        self.modo_directo(False)

    # ------------------------------------------------------------------
    # LISTENERS INTERNOS
    # ------------------------------------------------------------------

    def _on_record_arm(self, value):
        self.toast("Hola %s" % self.record_arm_state)
        record_arm = self.cs.get_control_by_name(C.RECORD_ARM)

        if self.record_arm_state == 0:
            self.record_arm_state = 1
            self.asignar_listeners(record_arm, self._record_arm_orig_listeners)
        else:
            self.record_arm_state = 0
            self._config_track_state_buttons()
            self.limpiar_listeners(record_arm)     # limpia listeners originales que quedaron
            boton = Boton(C.RECORD_ARM, 22, 3, self)
            boton.accion_on = lambda: self._on_record_arm(0)
            boton.accion_continua = False
            boton.crear_control(self.cs)

    def _on_pad_press(self, value):
        if value > 0:
            self._config_pads()

    # ------------------------------------------------------------------
    # BANCO DE DISPOSITIVO
    # ------------------------------------------------------------------

    def toggle_banco_device(self, value):
        if value > 0:
            self._long_press_pending['banco'] = True
            self.cs.schedule_message(15, self._check_long_press_banco)
        else:
            self._long_press_pending['banco'] = False

    def _check_long_press_banco(self):
        if self._long_press_pending.get('banco'):
            self._long_press_pending['banco'] = False
            if self._banco_device == 0:
                self.cambia_banco(1)
                self._banco_device = 1
            else:
                self.cambia_banco(-1)
                self._banco_device = 0

    def cambia_banco(self, incremento):
        up         = self.cs.get_control_by_name(C.UP)
        down       = self.cs.get_control_by_name(C.DOWN)
        device_btn = self.cs.get_control_by_name(C.DEVICE)

        device_btn.receive_value(127)

        if incremento > 0:
            self.cs.schedule_message(2, lambda: down.receive_value(127))
            self.cs.schedule_message(4, lambda: down.receive_value(0))
        else:
            self.cs.schedule_message(2, lambda: up.receive_value(127))
            self.cs.schedule_message(4, lambda: up.receive_value(0))

        self.cs.schedule_message(6, lambda: device_btn.receive_value(0))

    # ------------------------------------------------------------------
    # MODOS
    # ------------------------------------------------------------------

    def modo_edicion_clip(self, activo):
        for boton in (self.botonLoopLen, self.botonLoopPos,
                      self.botonLoopOffset, self.botonLoopOnOff):
            if boton:
                boton.activar_control(activo)
        if activo:
            self.modo_directo(False)

    def modo_directo(self, activo):
        for boton in (self.botonMacro1, self.botonMacro2,
                      self.botonMacro3, self.botonMacro4):
            if boton:
                boton.activar_control(activo)
        if activo:
            self.modo_edicion_clip(False)

    # ------------------------------------------------------------------
    # GESTIÓN DE LISTENERS
    # ------------------------------------------------------------------

    def limpiar_listeners(self, control):
        for slot in list(control._value_signal._slots):
            control.remove_value_listener(slot.callback)

    def get_listeners(self, control):
        return [slot.callback for slot in control._value_signal._slots]

    def asignar_listeners(self, control, listeners):
        for listener in listeners:
            if not control.value_has_listener(listener):
                control.add_value_listener(listener)

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------

    def addControl(self, nombre, color, accion):
        control = self.cs.get_control_by_name(nombre)
        if control is None:
            self.log("addControl ERROR: control no encontrado -> %s" % nombre)
            return
        if color is not None:
            control.send_value(color)
        if accion is not None and not control.value_has_listener(accion):
            control.add_value_listener(accion)

    def log(self, message):
        self.parent.log(message)

    def toast(self, message):
        self.parent.toast(message)

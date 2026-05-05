# =============================================================================
# ExampleActions.py  —  ClyphX Pro User Actions para APC64
# =============================================================================

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from functools import partial
from .APC64Manager import APC64Manager
import Live


class ExampleActions(UserActionsBase):
    """Acciones personalizadas para controlar el APC64 desde ClyphX Pro."""

    # ------------------------------------------------------------------
    # INICIALIZACIÓN
    # ------------------------------------------------------------------

    def create_actions(self):
        self.add_global_action("config_apc",        self.config_apc)
        self.add_global_action("push_user_mode",    self.push_user_mode)
        self.add_global_action("ex_global",         self.global_action_example)

        self.add_track_action("focus_track",   self.focus_track)
        self.add_track_action("cambia_anillo", self.cambia_anillo)
        self.add_track_action("select_chain",  self.select_chain)
        self.add_track_action("ex_track",      self.track_action_example)

        self.add_device_action("ex_device", self.device_action_example)
        self.add_clip_action("ex_clip",     self.clip_action_example)

        self._init_estado()

    def _init_estado(self):
        self.apc        = APC64Manager(self)
        self.track_sel  = 1
        self.device_sel = 0
        self.anillo     = 1
        self.enc        = 0
        self.step_size  = 1

    # ------------------------------------------------------------------
    # CONFIGURACIÓN DEL APC64
    # ------------------------------------------------------------------

    def config_apc(self, action_def, args):
        """Localiza el APC64 y delega la configuración al APC64Manager."""
        id_surface = 1
        control_surfaces = list(Live.Application.get_application().control_surfaces)
        if not (0 <= id_surface < len(control_surfaces)):
            self.log("config_apc ERROR: no se encontró la superficie %s" % id_surface)
            return

        self.apc.setup(control_surfaces[id_surface])

    # ------------------------------------------------------------------
    # ENCODER
    # ------------------------------------------------------------------

    def encoder_value(self, value):
        self.cambia_valor(-1 if value == 127 else 1)

    def encoder_buton(self, value):
        if value > 0:
            self.toast("Paso: %s" % self.step_size)

    # ------------------------------------------------------------------
    # NAVEGACIÓN DE PISTAS
    # ------------------------------------------------------------------

    def cambia_pista(self, pista, value):
        """Selecciona, mutea, solea, arma o hace fold de una pista según el modo activo."""
        if value != 0:
            return

        comp = self.apc.cs.get_component_by_name("Session_Ring")
        track_offset   = comp.track_offset
        visible_tracks = [t for t in self.song().tracks
                          if not t.is_grouped or t.is_visible]

        idx = track_offset + pista - 1
        if idx >= len(visible_tracks):
            return

        real_track = visible_tracks[idx]
        real_idx   = list(self.song().tracks).index(real_track) + 1

        if real_track.is_foldable:
            self.action("%s/FOLD" % real_idx)
        elif self.apc.botonMute and self.apc.botonMute.botonValue > 0:
            self.action("%s/mute" % real_idx)
        elif self.apc.botonSolo and self.apc.botonSolo.botonValue > 0:
            self.action("%s/solo" % real_idx)
        elif self.apc.botonArm and self.apc.botonArm.botonValue > 0:
            self.action("%s/arm" % real_idx)
        else:
            self.action("%s/focus_track" % real_idx)

    def cambia_valor(self, inc):
        """Incrementa o decrementa el parámetro actualmente asignado al encoder."""
        parameter = self.enc
        if not parameter:
            return
        rango = parameter.max - parameter.min
        diff  = (0.01 if rango <= 2.0 else 1) * inc * self.step_size
        parameter.value = max(parameter.min, min(parameter.max, parameter.value + diff))

    def cambiaAnillo(self, value):
        if value == 0:
            comp   = self.apc.cs.get_component_by_name("Session_Ring")
            escena = comp.scene_offset + 1
            self.action("CS 2 RING S%s" % escena)

    def cambia_anillo(self, action_def, args):
        if self.anillo == 1:
            self.anillo = 9
            self.action("CS 1 RING T8")
        else:
            self.anillo = 1
            self.action("CS 1 RING T1")

    def focus_track(self, action_def, args):
        track_index = list(self.song().tracks).index(action_def['track']) + self.anillo

        if track_index == self.track_sel:
            device_count = len(list(action_def['track'].devices)) - 1
            self.device_sel = (self.device_sel + 1) if self.device_sel < device_count else 0
        else:
            self.device_sel = 0

        self.action("%s/ SEL" % track_index)
        self.action("%s/DEV(%s) SEL" % (track_index, self.device_sel))

        device_name = self.song().tracks[track_index - 1].devices[self.device_sel].name
        if "(MULT)" in device_name:
            self.action("DEV(1) SEL; DEVRIGHT")
        else:
            self.action("%s/DEV(%s) SEL" % (track_index, self.device_sel + 1))

        self.track_sel = track_index

    # ------------------------------------------------------------------
    # PARÁMETROS Y DISPOSITIVOS
    # ------------------------------------------------------------------

    def select_param(self, ident, index, value):
        from .APC64Controls import APC64Controls as C
        control  = self.apc.cs.get_control_by_name(C.touch_strips()[index])
        self.enc = control.mapped_object

    def select_chain(self, action_def, args):
        if not args:
            return
        device_chain   = args
        selected_track = self.song().view.selected_track
        track_index    = list(self.song().tracks).index(action_def['track']) + 1

        self.action("{}/DEV(1.ALL.1) OFF".format(track_index))
        self.action("{}/DEV(1.{}.1) ON".format(track_index, device_chain))
        self.action("{}/DEV(1.{}.1) SEL".format(track_index, device_chain))
        self.action("{}/DEV(1) P1 {}".format(track_index, device_chain))

        self.song().view.selected_track = selected_track

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------

    def action(self, actions):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)

    def toast(self, message):
        self.canonical_parent.show_message(message)

    def log(self, message):
        self.canonical_parent.log_message(message)

    # ------------------------------------------------------------------
    # ACCIONES PUSH
    # ------------------------------------------------------------------

    def push_user_mode(self, action_def, args):
        if not args or "on" in args:
            self.action("PUSH MODE USER; WAIT 2;")
            self.action("WAIT 5;"
                        "MIDI 176 53 20; MIDI 176 44 20; MIDI 176 45 20;"
                        "MIDI 176 46 20; MIDI 176 47 20; MIDI 176 111 20;")
        if args and "off" in args:
            self.action("PUSH MODE LIVE;")
        self.toast("Push User Mode %s" % args)

    # ------------------------------------------------------------------
    # ACCIONES DE EJEMPLO
    # ------------------------------------------------------------------

    def global_action_example(self, action_def, args):
        self.log("X-Trigger is X-Clip=%s" % action_def["xtrigger_is_xclip"])
        self.toast("%s: Hello World" % (args[0] if args else ""))

    def track_action_example(self, action_def, args):
        track  = action_def["track"]
        master = self.song().master_track
        if not args or "vol" in args:
            track.mixer_device.volume.value  = master.mixer_device.volume.value
        if not args or "pan" in args:
            track.mixer_device.panning.value = master.mixer_device.panning.value

    def device_action_example(self, action_def, args):
        device = action_def["device"]
        if device:
            for p in device.parameters:
                if p.is_enabled and not p.is_quantized:
                    p.value = p.default_value
            self.log("Reset device: %s" % device.name)

    def clip_action_example(self, action_def, args):
        clip = action_def["clip"]
        if clip:
            if action_def["xtrigger"] != clip:
                clip.name = args
            else:
                self.log("Error: no se puede renombrar el X-Clip origen")

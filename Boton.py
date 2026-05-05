# =============================================================================
# Boton.py — Clase Boton para controles del APC64
# =============================================================================


class Boton:
    """
    Encapsula un control del APC64 con comportamiento de pulsador o conmutador,
    colores de estado y acciones on/off opcionales con repetición automática.
    """

    def __init__(self, nombre, color_on, color_off, parent,
                 accion_continua=False, boton_conmutador=False):
        self.nombre            = nombre
        self.color_on          = color_on
        self.color_off         = color_off
        self.accion_continua   = accion_continua
        self.accion_on         = None
        self.accion_off        = None
        self.parent            = parent
        self.control           = None
        self.control_surface   = None
        self._boton_pressed    = False
        self.botonValue        = 0
        self._boton_conmutador = boton_conmutador
        self.activado          = False

    def crear_control(self, control_surface):
        """Obtiene el control por nombre, establece el color y registra el listener."""
        self.control_surface = control_surface
        self.control = control_surface.get_control_by_name(self.nombre)
        if self.control:
            if not self.control.value_has_listener(self._boton_presionar):
                self.control.add_value_listener(self._boton_presionar)
            if self.color_off is not None:
                self.control.send_value(self.color_off)
            self.activado = True
        else:
            self.parent.log("Boton ERROR: control no encontrado -> {}".format(self.nombre))

    def activar_control(self, activo):
        """Activa o desactiva visualmente el botón."""
        if self.control:
            self.activado = activo
            self.control.send_value(self.color_off if activo else 0)
        else:
            self.parent.log("Boton ERROR: control no encontrado -> {}".format(self.nombre))

    def _boton_presionar(self, value):
        """Maneja la entrada MIDI del botón."""
        if not self.activado:
            return

        if self._boton_conmutador:
            if value > 0:
                self.botonValue = 0 if self.botonValue > 0 else 127
        else:
            self.botonValue = value

        if self.botonValue > 0:
            if self.color_on is not None:
                self.control.send_value(self.color_on)
            if not self._boton_pressed:
                self._boton_pressed = True
                self._ejecutar_accion_on()
        else:
            if self.color_off is not None:
                self.control.send_value(self.color_off)
            self._boton_pressed = False
            self._ejecutar_accion_off()

    def _ejecutar_accion_on(self):
        """Ejecuta accion_on y, si es continua, la repite mientras esté pulsado."""
        if not self._boton_pressed:
            return
        if self.accion_on is not None:
            self.accion_on()
        if self.accion_continua and self.control_surface:
            self.control_surface.schedule_message(5, self._ejecutar_accion_on)

    def _ejecutar_accion_off(self):
        """Ejecuta accion_off al soltar el botón."""
        if not self._boton_pressed and self.accion_off is not None:
            self.accion_off()

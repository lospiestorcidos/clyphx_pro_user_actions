"""
ClyphX_Pro allows you to add your own actions that work just like built in actions.
This file demonstrates how that's done.
_________________________________________________________________________________________

NOTES ABOUT FILES/MODULES:
You can create as many of these files as you like, but you must follow these rules:
(1) - All files you create must be placed in this user_actions folder.  *See note below.
(2) - The names of your files cannot begin with an underscore.
(3) - Your file should contain a class that extends UserActionsBase and that class should
      have the same name as the file (aka module) that contains it.  For example, this
      file's name is ExampleActions and the name of the class below is also
      ExampleActions.

Note that ClyphX_Pro uses sandboxing for importing from user-defined modules. So, if your
module contains errors, it will likely not be imported.

Also note that re-installing/updating Live and/or ClyphX Pro could cause files in this
user_actions folder to be removed.  For that reason, it is strongly recommended that you
back up your files in another location after creating or modifying them.  *See note below.


****** NEW IN V1.1.1 ******:
It is now possible to place your files in an alternate folder.  In this way, your files
will never be removed when re-installing/updating ClyphX Pro.  However, they can still
be removed when re-installing/updating Live, so the recommendation about backing up
files still holds.

To use the alternate folder:
(1) - Close Live.
(2) - In Live's Remote Scripts directory, create a folder named _user_actions
(3) - Copy the file named __init__.pyc from this user_actions folder and place it in the
      _user_actions folder you created.
(4) - Re-launch Live.
(5) - Create your files as described above, but place them in the _user_actions folder
      you created.

PLEASE NOTE: In order for the alternate folder to be used, the import statement in this
file (and all user action files) was changed.  So, if you'll be placing files you created
previously in the alternate folder, you'll need to change their import statements.

Instead of this:
from ..UserActionsBase import UserActionsBase

You should use this:
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
_________________________________________________________________________________________

NOTES ABOUT CLASSES:
As mentioned above, files you create should contain a class that extends UserActionsBase.
The class must implement a create_actions method, which is where you'll tell ClyphX_Pro
about the actions your class provides.  You can see this in the example class below.

There are several other useful methods that you can optionally override if you like:
(1) - on_track_list_changed(self) - This will be called any time the track list changes
      in Live.
(2) - on_scene_list_changed(self) - This will be called any time the scene list changes
      in Live.
(3) - on_selected_track_changed(self) - This will be called any time a track is selected
      or the track list changes in Live.
(4) - on_selected_scene_changed(self) - This will be called any time a scene is selected
      in Live.
(5) - on_control_surface_scripts_changed(self, scripts) - This will be called any time
      the list of control surface scripts changes in Live.  The scripts argument is a
      dict mapping the lower case names of scripts to the script objects themselves.

Additionally, there are a couple of other methods and attributes of UserActionsBase that
you should be aware of and that are demonstrated below:
(1) - self.song() - returns the current Live set object.
(2) - self.canonical_parent - returns the ControlSurface (parent) object that has loaded
      the ClyphX_Pro library.  Through this object, you can access two useful methods:
      (a) - log_message(msg) - Writes a message to Live's Log.txt file.
      (b) - show_message(msg) - Shows a message in Live's status bar.

Lastly, through the canonical_parent, you can access the core ClyphX Pro component, which
would allow you to trigger built in ClyphX Pro actions like so:
self.canonical_parent.clyphx_pro_component.trigger_action_list('metro ; 1/mute')

trigger_action_list accepts a single string that specifies the action list to trigger.
_________________________________________________________________________________________

NOTES ABOUT ACTIONS:
Your classes can create 4 types of actions each of which is slightly different, but all
have some common properties.

First of all, you define your actions in your class's create_actions method.  There is an
add method corresponding to each of the 4 types of actions you can create.  For example,
add_global_action(action_name, method) creates a global action.  All 4 add methods take
the same two arguments:
(1) - action_name - The single word, lowercase name to use when accessing the action from
      an X-Trigger. This name should not be the same as the name of any built in action.
(2) - method - The method in your class to call when the action has been triggered.

The methods for each type of action need to accept two arguments:
(1) - action_def - This is a dict that contains contents relevant to the type of action.
      The contents of this dict differs depending on the type of action, but always
      contains the following:
      (a) - xtrigger_is_xclip - A boolean indicating whether the action was triggered via
            an X-Clip.
      (b) - xtrigger - The X-Trigger that triggered the action.
(2) - args - Any arguments that follow the action name.  For example, in the case of
      'VOL RAMP 4 100', RAMP, 4 and 100 are all arguments following the action name (VOL).
      These arguments will be presented to you as a single string and will be converted to
      lower case unless one (or more) of the arguments is in quotes. Arguments in quotes
      are not converted in any way.

Note that ClyphX_Pro uses sandboxing for dispatching actions. So, if your method contains
errors, it will effectively be ignored.
_________________________________________________________________________________________

GLOBAL ACTIONS:
These actions don't apply to any particular object in Live.

Add method: add_global_action(action_name, method)

Additional action_def contents: No additional content.
_________________________________________________________________________________________

TRACK ACTIONS:
These actions apply to a track in Live and function just like Track Actions, so they'll be
called for each track that is specified.

Add method: add_track_action(action_name, method)

Additional action_def contents:
(1) - track - the track object to operate upon.
_________________________________________________________________________________________

DEVICE ACTIONS:
These actions apply to a device in Live and function just like Device Actions, so they'll
be called for each device that is specified.

Add method: add_device_action(action_name, method)

Additional action_def contents:
(1) - track - the track object containing the device.
(2) - device - the device object to operate upon.

Other notes, the action names for these actions are all preceded by 'user_dev'.  So, for
example, if you create a device action named 'my_action', its full name will be
'user_dev my_action'.  This allows your actions to apply to ranges of devices just like is
possible with Device Actions.  For example: 'user_dev(all) my_action'
_________________________________________________________________________________________

CLIP ACTIONS:
These actions apply to a clip in Live and function just like Clip Actions, so they'll
be called for each clip that is specified.

Add method: add_clip_action(action_name, method)

Additional action_def contents:
(1) - track - the track object containing the clip.
(2) - clip - the clip object to operate upon.

Other notes, the action names for these actions are all preceded by 'user_clip'.  So, for
example, if you create a clip action named 'my_action', its full name will be
'user_clip my_action'.  This allows your actions to apply to ranges of clips just like is
possible with Clip Actions.  For example: 'user_clip(all) my_action'
_________________________________________________________________________________________

"""

# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
import Live
from ableton.v2.control_surface import  BankingInfo, DeviceBankRegistry
from functools import partial
import time
from _Framework.Task import Task
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ControlSurface import ControlSurface

# Clase Boton
# Clase Boton
class Boton:
    def __init__(self, nombre, color_on, color_off, accion, parent):
        self.nombre = nombre
        self.color_on = color_on
        self.color_off = color_off
        self.accion = accion  # Esta es la acción a ejecutar
        self.parent = parent  # Referencia al objeto ExampleActions (o similar)
        self.control = None
        self.control_surface = None  # Necesitas guardar la superficie de control
        self._boton_pressed = False  # Variable para rastrear el estado del botón

    def crear_control(self, control_surface):
        """Obtiene el control por nombre, establece el color y añade el listener."""
        self.control_surface = control_surface
        self.control = self.control_surface.get_control_by_name(self.nombre)
        if self.control:
            if self.color_on is not None:
                self.control.send_value(self.color_on)
            # Pasamos 'self' como argumento para que botonPress tenga acceso al objeto Boton
            self.control.add_value_listener(self.botonPress)
        else:
            self.parent.log("Error: No se encontró el control con nombre {}".format(self.nombre))

    def botonPress(self, value):
        """Maneja la presión del botón."""
        if value > 0:  # Botón presionado
            if not self._boton_pressed:  # Si no estaba presionado antes
                self._boton_pressed = True
                self.start_accion_pressed_value()
        else:  # Botón liberado
            self._boton_pressed = False

    def start_accion_pressed_value(self):
        """Ejecuta la acción mientras el botón está presionado."""
        if self._boton_pressed:
            # Asegúrate de que la acción sea un callable y llámala con los argumentos correctos
            if callable(self.accion):
                self.accion()  # Llama a la acción sin argumentos, si es lo que quieres
            else:
                self.parent.log("Error: La acción para el botón {} no es un callable.".format(self.nombre))
            #Programa la siguiente llamada a la acción
            if self.control_surface:
               self.control_surface.schedule_message(5, self.start_accion_pressed_value)

# Your class must extend UserActionsBase.
class ExampleActions(UserActionsBase):
    """ ExampleActions provides some example actions for demonstration purposes. """
    track_sel= 1
    device_sel= 0
    anillo = 1
    enc = 0
    step_size = 1
    cs = None
    solo = False
    arm = False
    mute = False

    botones = []
    # Your class must implement this method.
    def create_actions(self):
        """
        Here, we create 4 actions, each a different type:
        (1) - ex_global can be triggered via the name 'ex_global', which will call the
              method named global_action_example.
        (2) - ex_track can be triggered via the name 'ex_track', which will call the
              method named track_action_example.
        (3) - ex_device can be triggered via the name 'user_dev ex_device', which will
              call the method named device_action_example.
        (4) - ex_clip can be triggered via the name 'user_clip ex_clip', which will
              call the method named clip_action_example.
        """
        self._button1_pressed = False  # Variable para rastrear el estado del botón
        self._button2_pressed = False  # Variable para rastrear el estado del botón
        self._decrement_task = None  # Tarea para decrementar el volumen
        self.add_global_action("ex_global", self.global_action_example)
        self.add_global_action("config_apc", self.config_apc)
        self.add_global_action("push_user_mode", self.push_user_mode)
        self.add_track_action("focus_track", self.focus_track)
        self.add_track_action("cambia_anillo", self.cambia_anillo)
        self.add_track_action("select_chain", self.select_chain)
        self.add_track_action("ex_track", self.track_action_example)
        self.add_device_action("ex_device", self.device_action_example)
        self.add_device_action("bind_mpd", self.bind_mpd)
        self.add_global_action("bind_mpd_this", self.bind_mpd_this)
        self.add_clip_action("ex_clip", self.clip_action_example)
        self.add_device_action("pruebaParam", self.pruebaParam)


    def global_action_example(self, action_def, args):
        """ Logs whether the action was triggered via an X-Clip and shows 'Hello World'
        preceded by any args in Live's status bar. """
        self.canonical_parent.log_message(
            "X-Trigger is X-Clip=%s" % action_def["xtrigger_is_xclip"]
        )
        self.canonical_parent.show_message("%s: Hello World" % args[0])

    def config_apc(self, action_def, args):
        """ Logs whether the action was triggered via an X-Clip and shows 'Hello World'
        preceded by any args in Live's status bar. """
        self.canonical_parent.log_message(
            "Entra en config_apc is X-Clip=%s" % action_def["xtrigger_is_xclip"]
        )
        if args:
            id_surface = args[0]

        id_surface = 1

        control_surfaces = list(Live.Application.get_application().control_surfaces)
        if 0 <= id_surface < len(control_surfaces):
            self.cs = control_surfaces[id_surface]

            control = self.cs.get_control_by_name("Encoder" )
            control.add_value_listener(self.encoder_value)

            control = self.cs.get_control_by_name("Encoder_Button" )
            control.add_value_listener(self.encoder_buton)

            #for i in range(0, 8):
                #self.addControl("Track_Select_Button_%s" % i, None, partial(self.cambia_pista,i+1))
            for i in range(0, 8):
                boton = Boton("Track_Select_Button_%s" % i, None, None, partial(self.cambia_pista, i + 1), self)
                self.botones.append(boton)

            boton = Boton("Track_State_Button_1", 20, None, partial(self.botonElektron2), self)
            self.botones.append(boton)

            # Crear los controles de los botones
            for boton in self.botones:
                boton.crear_control(self.cs)

            #accion = lambda n, value: self.canonical_parent.show_message('Funciona si ')
            #for i in range(0, 6):
                    #self.addControl("Track_State_Button_%s" % i, 1, partial(accion, 14))


            #self.addControl("Track_State_Button_1",  20, partial(self.botonElektron2))

            self.addControl("Track_State_Button_0",  12, partial(self.botonElektron))
            self.addControl("Track_State_Button_3",  9, partial(self.botonControlSecuenciador))
            self.addControl("Track_State_Button_6", 12, partial(self.boton1Value))
            self.addControl("Track_State_Button_7" , 12, partial(self.boton2Value))

            for i in range(0, 8):
                self.addControl("Mi_Pad_{}".format(i) , 1, partial(self.botonMiPad, i ))


            self.addControl("Mi_Pad_0" , 9, partial(self.botonShiftP))
            self.addControl("Mi_Pad_5" , 9, partial(self.botonMute))
            self.addControl("Mi_Pad_6" , 41, partial(self.botonSolo))
            self.addControl("Mi_Pad_7" , 5, partial(self.botonArm))

            #self.addControl("Up_Button",  20, partial(self.cambiaAnillo))
            #self.addControl("Down_Button",  20, partial(self.cambiaAnillo

            for i in range(0, 9):
                self.addControl("Touch_Element_%s" % i, None, partial(self.select_param,"Touch_Element_%s" % i,i ))



    def botonElektron2(self,value):
         if value == 127:
             self.enc = 1
             self.action("(PSEQ)DEV(1) sel ;DEV(1.1.1) SEL" )

    def botonMiPad(self,value, i):
         if value == 0:
            self.canonical_parent.show_message('pad ')

    def addControl(self,nombre, color, accion):
        control = self.cs.get_control_by_name(nombre)
        if color is not None:
            control.send_value(color)
        if accion is not None:
            control.add_value_listener(accion)

    def botonMute(self,value):
        control = self.cs.get_control_by_name("Mi_Pad_5")
        if value > 0:
            control.send_value(3)7
            self.mute = True
        else:
            control.send_value(9)
            self.mute = False

    def botonShiftP(self,value):

        #control = self.cs.get_control_by_name("Mi_Pad_2")
        #self.cs.component_map["Device"].set_next_bank_button(control)
        control = self.cs.get_control_by_name("Touch_Strip_1")

        param = self.song().view.selected_track.mixer_device.volume
        if value > 0:
            control.release_parameter()
        else:
            control.connect_to(param)

    def botonSolo(self,value):

        control = self.cs.get_control_by_name("Mi_Pad_6")
        if value > 0:
            control.send_value(3)
            self.solo = True
        else:
            control.send_value(41)
            self.solo = False


    def botonArm(self,value):
        control = self.cs.get_control_by_name("Mi_Pad_7")
        if value > 0:
            control.send_value(3)
            self.arm = True
        else:
            control.send_value(5)
            self.arm = False

    def botonControlSecuenciador(self,value):
        control = self.cs.get_control_by_name("Track_State_Button_3")
        pads = self.cs.get_control_by_name("Pads")
        if value > 0:
            #pads.grab_control()
            control.send_value(3)

        else:
            #pads.release_control()
            control.send_value(5)

    def boton1Value(self,value):
        if value > 0:
                # Si el botón se presiona, activamos la acción de bajar volumen.
                if not self._button1_pressed:
                    self._button1_pressed = True
                    self.start_lowering_value()
        else:
                # Al soltar el botón, se detiene la bajada de volumen.
                self._button1_pressed = False

    def boton2Value(self,value):
        if value > 0:
                # Si el botón se presiona, activamos la acción de bajar volumen.
                if not self._button2_pressed:
                    self._button2_pressed = True
                    self.start_uppering_value()
        else:
                # Al soltar el botón, se detiene la bajada de volumen.
                self._button2_pressed = False

    def start_lowering_value(self):
            if self._button1_pressed:
                ## Definir un decremento. Por ejemplo, bajamos 1 dB cada ciclo.
                #decremento = 1.0
                ## Calcular el nuevo volumen; asegurarse de no bajar de un mínimo permitido (por ejemplo, -60 dB).
                #nuevo_volumen = max(-60.0, current_volume - decremento)
                parameter = self.enc
                rango = parameter.max - parameter.min
                if rango == 1.0:
                    diff = -0.01 * self.step_size
                elif rango == 2.0:
                    diff = -0.01 * self.step_size
                else:
                    diff = -1 *  self.step_size

                self.canonical_parent.show_message('paso  %s'  % diff)

                parameter.value = max(parameter.min, parameter.value + diff)
                self.cs.schedule_message(5, self.start_lowering_value)  # 100 ms de retardo

    def start_uppering_value(self):
            if self._button2_pressed:
                ## Definir un decremento. Por ejemplo, bajamos 1 dB cada ciclo.
                parameter = self.enc
                rango = parameter.max - parameter.min
                if rango == 1.0:
                    diff = 0.01 * self.step_size
                else:
                    if rango == 2.0:
                        diff = 0.01 * self.step_size
                    else:
                        diff = 1 *  self.step_size

                self.canonical_parent.show_message('paso  %s'  % diff)

                parameter.value = min(parameter.max, parameter.value + diff)
                self.cs.schedule_message(5, self.start_uppering_value)  # 100 ms de retardo


    def botonElektron(self,value):
         if value == 127:
            self.action("(PSEQ) $BTN_1_APC$" )



    def cambiaValue(self,value):
        #self.canonical_parent.show_message('prueba %s' %  value)
        parameter = self.enc

        step_size =  (parameter.max - parameter.min)/self.step_size

        if value == 127:
            diff = -1 * step_size
        else:
            diff= 1 * step_size

        parameter.value = parameter.value + diff

    def encoder_value(self,value):

        if value == 127:
            if self.step_size > 1:
                self.step_size = self.step_size - 1
        else:
            if self.step_size < 10:
                self.step_size = self.step_size + 1


    def encoder_buton (self,value):
        self.canonical_parent.show_message('paso  %s'  % self.step_size)



    def soloPressed(self, press):
        if press==1:
            self.action("VOL <;")
            #time.sleep(1)
            #self.soloPressed(1)
        else:
            return 0

    def cambia_pista(self,pista,value):
        if value == 0:
            comp =  self.cs.get_component_by_name("Session_Ring")
            pista = pista + comp.track_offset
            if self.mute == True:
                self.action("%s/mute;"  % pista)
            elif self.solo == True:
                self.action("%s/solo;"  % pista)
            elif self.arm == True:
                self.action("%s/arm;"  % pista)
            else:
                self.action("%s/focus_track;"  % pista)


    def cambiaAnillo(self,value):
        if value == 0:
            comp =  self.cs.get_component_by_name("Session_Ring")
            escena =  comp.scene_offset+1
            self.canonical_parent.show_message('escena %s' %  escena)
            self.action("CS 2 RING S%s"  % escena)

    def botonera_estado(self,pista,value):
        self.canonical_parent.show_message('botonera_estado %s' %pista)


    def select_param(self,ident,index, value):
        control = self.cs.get_control_by_name("Touch_Strip_%s" %index)

        self.canonical_parent.show_message('prueba')
        #self.action("%%bind_var%%=%s"  % ident)

        self.enc = control.mapped_object

    def bind_param(self,ident,value):
               #self.canonical_parent.show_message('bind %s' %value)
               if ident == 1:
                   self.action("DEV P%s <;" %self.enc )
               else:
                   self.action("DEV P%s >;" %self.enc )



    def action(self, actions):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
    def toast(self, comments):
        self.canonical_parent.show_message(comments)
    def log(self, message):
        self.canonical_parent.log_message(message)

    def select_chain(self, action_def, args):
        if args:
            device_chain=args

        selected_track = self.song().view.selected_track

        track_index = list(self.song().tracks).index(action_def['track']) + 1
        self.action("{}/DEV(1.ALL.1)  OFF;".format(track_index))
        self.action("{}/DEV(1.{}.1) ON;".format(track_index,device_chain))
        self.action("{}/DEV(1.{}.1) SEL;".format(track_index,device_chain))
        self.action("{}/DEV(1) P1 {}".format(track_index, device_chain))

        self.song().view.selected_track = selected_track

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
            if self.device_sel < device_count:
                self.device_sel =  self.device_sel + 1
            else:
                self.device_sel = 0
        else:
            self.device_sel = 0
        self.action("%s/ SEL" % (track_index))
        self.action("%s/DEV(%s) SEL" % (track_index, self.device_sel))
        device_name = self.song().tracks[track_index-1].devices[self.device_sel].name
        if "(MULT)" in device_name:
            self.action("DEV(1) SEL; DEVRIGHT")
        else:
            self.action("%s/DEV(%s) SEL" % (track_index, self.device_sel + 1))

        self.track_sel=track_index



    def push_user_mode(self, action_def, args):

        if not args or "on" in args:
            self.action("PUSH MODE USER;WAIT 2;")
            # MIDI CC
            self.action("WAIT 5;MIDI 176 53 20;"
                        "MIDI 176 44 20;MIDI 176 45 20; "
                        "MIDI 176 46 20;MIDI 176 47 20;MIDI 176 111 20;")

            # MIDI NOTES

            if "off" in args:
                self.action("PUSH MODE LIVE;")

        self.toast("Push User Mode %s" %args)

    def track_action_example(self, action_def, args):
        """ Sets the volume and/or panning of the track to be the same as the master
        track.  This obviously does nothing if the track is the master track. """
        track = action_def["track"]
        master = self.song().master_track
        if not args or "vol" in args:
            track.mixer_device.volume.value = master.mixer_device.volume.value
        if not args or "pan" in args:
            track.mixer_device.panning.value = master.mixer_device.panning.value

    def device_action_example(self, action_def, args):
        """ Resets all of the device's parameters and logs the name of the device.
        This method doesn't require any args so we use _ to indicate that. """
        device = action_def["device"]

        if device:
            for p in device.parameters:
                if p.is_enabled and not p.is_quantized:
                    p.value = p.default_value
            self.canonical_parent.log_message("Reset device: %s" % device.name)

    def pruebaParam(self, action_def, args):
        device = action_def["device"]
        if device:
            parameter = device.parameters[1]
            parameter.value = 0

    def bind_mpd_this(self, action_def, args):
        self.canonical_parent.log_message(
            "X-Trigger is X-Clip=%s" % action_def["xtrigger_is_xclip"]
        )
        self.canonical_parent.show_message("%s: Hello World" % args)

        track_name = self.song().view.selected_track.name
        device_name = self.song().view.selected_track.view.selected_device.name

        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_1 "%s"/DEV("%s") P1' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_2 "%s"/DEV("%s") P2' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_3 "%s"/DEV("%s") P3' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_4 "%s"/DEV("%s") P4' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_5 "%s"/DEV("%s") P5' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_6 "%s"/DEV("%s") P6' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_7 "%s"/DEV("%s") P7' % (track_name, device_name))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(
            'BIND ENC_8 "%s"/DEV("%s") P8' % (track_name, device_name))

        self.canonical_parent.show_message("BIND MPD %s,%s" % (track_index, device.name))

    def bind_mpd(self, action_def, args):

        device = action_def["device"]
        if device:
            for p in device.parameters:
                if p.is_enabled and not p.is_quantized:
                    p.value = p.default_value

            track_index = list(self.song().tracks).index(action_def['track']) + 1
            device_index = list(action_def['track'].devices).index(action_def['device']) +  1
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_1 %s/DEV(%s) P1" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_2 %s/DEV(%s) P2" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_3 %s/DEV(%s) P3" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_4 %s/DEV(%s) P4" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_5 %s/DEV(%s) P5" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_6 %s/DEV(%s) P6" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_7 %s/DEV(%s) P7" % (track_index, device_index))
            self.canonical_parent.clyphx_pro_component.trigger_action_list("BIND ENC_8 %s/DEV(%s) P8" % (track_index, device_index))

            #self.canonical_parent.show_message("BIND DIGITONE_T1_1 %s/DEV(%s) P1" % (track_index, device.name) )


    def clip_action_example(self, action_def, args):
        """ Sets the name of the clip to the name specified in args.  We consider renaming
        the X-Clip that triggered this action an error and so we log that if it
        occurs. """
        clip = action_def["clip"]
        if clip:
            if action_def["xtrigger"] != clip:
                clip.name = args
            else:
                self.canonical_parent.log_message("Error: Tried to rename X-Clip!")

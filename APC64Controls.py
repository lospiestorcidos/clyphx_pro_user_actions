# =============================================================================
# APC64Controls.py — Constantes de nombres de controles del APC64
# Extraídas de elements.py del script oficial de Ableton
# Uso: from APC64Controls import APC64Controls as C
#      control = self.cs.get_control_by_name(C.PLAY)
# =============================================================================


class APC64Controls:

    # -------------------------------------------------------------------------
    # BOTONES DE TRANSPORTE
    # -------------------------------------------------------------------------
    PLAY            = "Play_Button"
    RECORD          = "Record_Button"
    STOP            = "Stop_Button"
    UNDO            = "Undo_Button"
    TEMPO           = "Tempo_Button"

    # -------------------------------------------------------------------------
    # BOTONES MODIFICADORES
    # -------------------------------------------------------------------------
    SHIFT           = "Shift_Button"
    DEVICE          = "Device_Button"
    CLEAR           = "Clear_Button"
    DUPLICATE       = "Duplicate_Button"
    QUANTIZE        = "Quantize_Button"
    FIXED_LENGTH    = "Fixed_Length_Button"

    # -------------------------------------------------------------------------
    # BOTONES DE MODO DE PISTA
    # -------------------------------------------------------------------------
    RECORD_ARM      = "Record_Arm_Button"
    MUTE            = "Mute_Button"
    SOLO            = "Solo_Button"
    CLIP_STOP       = "Clip_Stop_Button"

    # -------------------------------------------------------------------------
    # BOTONES DE MODO DE TOUCH STRIP
    # -------------------------------------------------------------------------
    VOLUME          = "Volume_Button"
    PAN             = "Pan_Button"
    SEND            = "Send_Button"
    CHANNEL_STRIP   = "Channel_Strip_Button"
    OFF             = "Off_Button"

    # -------------------------------------------------------------------------
    # ENCODER
    # -------------------------------------------------------------------------
    ENCODER         = "Encoder"
    ENCODER_BUTTON  = "Encoder_Button"
    ENCODER_WITH_SHIFT = "Encoder_With_Shift"

    # -------------------------------------------------------------------------
    # BOTONES DE NAVEGACIÓN
    # -------------------------------------------------------------------------
    UP              = "Up_Button"
    DOWN            = "Down_Button"
    LEFT            = "Left_Button"
    RIGHT           = "Right_Button"

    # Navegación con Shift
    UP_SHIFT        = "Up_Button_With_Shift"
    DOWN_SHIFT      = "Down_Button_With_Shift"
    LEFT_SHIFT      = "Left_Button_With_Shift"
    RIGHT_SHIFT     = "Right_Button_With_Shift"

    # Navegación con Device
    UP_DEVICE       = "Up_Button_With_Device"
    DOWN_DEVICE     = "Down_Button_With_Device"
    LEFT_DEVICE     = "Left_Button_With_Device"
    RIGHT_DEVICE    = "Right_Button_With_Device"

    # Modificadores combinados
    TEMPO_SHIFT     = "Tempo_Button_With_Shift"
    DEVICE_SHIFT    = "Device_Button_With_Shift"

    # -------------------------------------------------------------------------
    # MATRICES — Acceso por nombre completo
    # -------------------------------------------------------------------------
    PADS                = "Pads"            # Matriz 8x8 completa
    TRACK_STATE_BUTTONS = "Track_State_Buttons"
    TRACK_SELECT_BUTTONS = "Track_Select_Buttons"
    SCENE_LAUNCH_BUTTONS = "Scene_Launch_Buttons"
    TOUCH_STRIPS        = "Touch_Strips"
    TOUCH_STRIPS_2_7    = "Touch_Strips_2_thru_7"
    TOUCH_ELEMENTS      = "Touch_Elements"

    # -------------------------------------------------------------------------
    # TRACK STATE BUTTONS individuales (fila horizontal, notas 64-71)
    # -------------------------------------------------------------------------
    TRACK_STATE_0   = "Track_State_Button_0"
    TRACK_STATE_1   = "Track_State_Button_1"
    TRACK_STATE_2   = "Track_State_Button_2"
    TRACK_STATE_3   = "Track_State_Button_3"
    TRACK_STATE_4   = "Track_State_Button_4"
    TRACK_STATE_5   = "Track_State_Button_5"
    TRACK_STATE_6   = "Track_State_Button_6"
    TRACK_STATE_7   = "Track_State_Button_7"

    # -------------------------------------------------------------------------
    # TRACK SELECT BUTTONS individuales (fila horizontal, notas 100-107)
    # -------------------------------------------------------------------------
    TRACK_SELECT_0  = "Track_Select_Button_0"
    TRACK_SELECT_1  = "Track_Select_Button_1"
    TRACK_SELECT_2  = "Track_Select_Button_2"
    TRACK_SELECT_3  = "Track_Select_Button_3"
    TRACK_SELECT_4  = "Track_Select_Button_4"
    TRACK_SELECT_5  = "Track_Select_Button_5"
    TRACK_SELECT_6  = "Track_Select_Button_6"
    TRACK_SELECT_7  = "Track_Select_Button_7"

    # -------------------------------------------------------------------------
    # SCENE LAUNCH BUTTONS individuales (columna derecha, notas 112-119)
    # -------------------------------------------------------------------------
    SCENE_LAUNCH_0  = "Scene_Launch_Button_0"
    SCENE_LAUNCH_1  = "Scene_Launch_Button_1"
    SCENE_LAUNCH_2  = "Scene_Launch_Button_2"
    SCENE_LAUNCH_3  = "Scene_Launch_Button_3"
    SCENE_LAUNCH_4  = "Scene_Launch_Button_4"
    SCENE_LAUNCH_5  = "Scene_Launch_Button_5"
    SCENE_LAUNCH_6  = "Scene_Launch_Button_6"
    SCENE_LAUNCH_7  = "Scene_Launch_Button_7"

    # -------------------------------------------------------------------------
    # TOUCH STRIPS individuales (canales 0-7, pitch bend)
    # -------------------------------------------------------------------------
    TOUCH_STRIP_0   = "Touch_Strip_0"
    TOUCH_STRIP_1   = "Touch_Strip_1"
    TOUCH_STRIP_2   = "Touch_Strip_2"
    TOUCH_STRIP_3   = "Touch_Strip_3"
    TOUCH_STRIP_4   = "Touch_Strip_4"
    TOUCH_STRIP_5   = "Touch_Strip_5"
    TOUCH_STRIP_6   = "Touch_Strip_6"
    TOUCH_STRIP_7   = "Touch_Strip_7"

    # -------------------------------------------------------------------------
    # TOUCH ELEMENTS individuales (notas 82-89, táctiles)
    # -------------------------------------------------------------------------
    TOUCH_ELEMENT_0 = "Touch_Element_0"
    TOUCH_ELEMENT_1 = "Touch_Element_1"
    TOUCH_ELEMENT_2 = "Touch_Element_2"
    TOUCH_ELEMENT_3 = "Touch_Element_3"
    TOUCH_ELEMENT_4 = "Touch_Element_4"
    TOUCH_ELEMENT_5 = "Touch_Element_5"
    TOUCH_ELEMENT_6 = "Touch_Element_6"
    TOUCH_ELEMENT_7 = "Touch_Element_7"

    # -------------------------------------------------------------------------
    # PADS individuales — formato: "{col}_Pad_{row}"
    # col: 0-7 (izquierda a derecha)
    # row: 0-7 (arriba a abajo, row 7 = fila inferior)
    # Notas MIDI: fila 0 = notas 56-63, fila 7 = notas 0-7
    # -------------------------------------------------------------------------

    # Fila 0 (superior)
    PAD_0_0 = "0_Pad_0";  PAD_1_0 = "1_Pad_0";  PAD_2_0 = "2_Pad_0";  PAD_3_0 = "3_Pad_0"
    PAD_4_0 = "4_Pad_0";  PAD_5_0 = "5_Pad_0";  PAD_6_0 = "6_Pad_0";  PAD_7_0 = "7_Pad_0"

    # Fila 1
    PAD_0_1 = "0_Pad_1";  PAD_1_1 = "1_Pad_1";  PAD_2_1 = "2_Pad_1";  PAD_3_1 = "3_Pad_1"
    PAD_4_1 = "4_Pad_1";  PAD_5_1 = "5_Pad_1";  PAD_6_1 = "6_Pad_1";  PAD_7_1 = "7_Pad_1"

    # Fila 2
    PAD_0_2 = "0_Pad_2";  PAD_1_2 = "1_Pad_2";  PAD_2_2 = "2_Pad_2";  PAD_3_2 = "3_Pad_2"
    PAD_4_2 = "4_Pad_2";  PAD_5_2 = "5_Pad_2";  PAD_6_2 = "6_Pad_2";  PAD_7_2 = "7_Pad_2"

    # Fila 3
    PAD_0_3 = "0_Pad_3";  PAD_1_3 = "1_Pad_3";  PAD_2_3 = "2_Pad_3";  PAD_3_3 = "3_Pad_3"
    PAD_4_3 = "4_Pad_3";  PAD_5_3 = "5_Pad_3";  PAD_6_3 = "6_Pad_3";  PAD_7_3 = "7_Pad_3"

    # Fila 4
    PAD_0_4 = "0_Pad_4";  PAD_1_4 = "1_Pad_4";  PAD_2_4 = "2_Pad_4";  PAD_3_4 = "3_Pad_4"
    PAD_4_4 = "4_Pad_4";  PAD_5_4 = "5_Pad_4";  PAD_6_4 = "6_Pad_4";  PAD_7_4 = "7_Pad_4"

    # Fila 5
    PAD_0_5 = "0_Pad_5";  PAD_1_5 = "1_Pad_5";  PAD_2_5 = "2_Pad_5";  PAD_3_5 = "3_Pad_5"
    PAD_4_5 = "4_Pad_5";  PAD_5_5 = "5_Pad_5";  PAD_6_5 = "6_Pad_5";  PAD_7_5 = "7_Pad_5"

    # Fila 6
    PAD_0_6 = "0_Pad_6";  PAD_1_6 = "1_Pad_6";  PAD_2_6 = "2_Pad_6";  PAD_3_6 = "3_Pad_6"
    PAD_4_6 = "4_Pad_6";  PAD_5_6 = "5_Pad_6";  PAD_6_6 = "6_Pad_6";  PAD_7_6 = "7_Pad_6"

    # Fila 7 (inferior) — la que usas para tus botones personalizados
    PAD_0_7 = "0_Pad_7";  PAD_1_7 = "1_Pad_7";  PAD_2_7 = "2_Pad_7";  PAD_3_7 = "3_Pad_7"
    PAD_4_7 = "4_Pad_7";  PAD_5_7 = "5_Pad_7";  PAD_6_7 = "6_Pad_7";  PAD_7_7 = "7_Pad_7"

    # -------------------------------------------------------------------------
    # ELEMENTOS INTERNOS (uso avanzado)
    # -------------------------------------------------------------------------
    TRACK_COLOR_ELEMENT         = "Track_Color_Element"
    FIRMWARE_MODE_ELEMENT       = "Firmware_Mode_Element"
    TRACK_TYPE_ELEMENT          = "Track_Type_Element"
    RENDER_TO_CLIP_START        = "Render_To_Clip_Start_Element"
    RENDER_TO_CLIP_DATA         = "Render_To_Clip_Data_Element"
    RENDER_TO_CLIP_END          = "Render_To_Clip_End_Element"
    DISPLAY_OWNERSHIP_COMMAND   = "Display_Ownership_Command"
    DISPLAY_LINE_1              = "Display_Line_1"
    DISPLAY_LINE_2              = "Display_Line_2"
    DISPLAY_LINE_3              = "Display_Line_3"

    # -------------------------------------------------------------------------
    # HELPERS — listas útiles para iterar
    # -------------------------------------------------------------------------

    @staticmethod
    def track_state_buttons():
        return ["Track_State_Button_%s" % i for i in range(8)]

    @staticmethod
    def track_select_buttons():
        return ["Track_Select_Button_%s" % i for i in range(8)]

    @staticmethod
    def scene_launch_buttons():
        return ["Scene_Launch_Button_%s" % i for i in range(8)]

    @staticmethod
    def touch_strips():
        return ["Touch_Strip_%s" % i for i in range(8)]

    @staticmethod
    def touch_elements():
        return ["Touch_Element_%s" % i for i in range(8)]

    @staticmethod
    def pads_fila(row):
        """Devuelve los 8 nombres de pad de una fila (0=superior, 7=inferior)."""
        return ["%s_Pad_%s" % (col, row) for col in range(8)]

    @staticmethod
    def pad(col, row):
        """Devuelve el nombre de un pad concreto."""
        return "%s_Pad_%s" % (col, row)

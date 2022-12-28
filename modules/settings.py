from modules import letter_widths

class Settings:
    # Letter width: how much to move current_position after a letter, relative to fontsize
    letter_widths_by_fontfamily: dict[str, dict[str, float]] = {
        "Arial": letter_widths.ARIAL
    }

    def __init__(
        self,
        text_input_file: str,
        inquisit_output_file: str,
        stimuli_output_file: str,
        trial_name: str,
        fontfamily: str,
        start_x: float,
        start_y: float,
        row_end_in_pixel: float,
        fontsize_pct: float,
        inbetween_color_state_1: str = "#f8f8f8",
        inbetween_color_state_2: str = "#000000",
        inbetween_clickable_color: str = "#ffffff00",
        text_color_state_1: str = "#000000",
        text_color_state_2: str = "#000000",
        number_length: int = 4,
        selection_strikethrough=True,
        selection_underline=False,
        reload_letters_after_response=False,
    ) -> None:
        self.text_input_file: str = text_input_file
        self.inquisit_ouput_file: str = inquisit_output_file
        self.stimuli_output_file: str = stimuli_output_file
        self.trial_name: str = trial_name
        self.fontfamily: str = fontfamily
        self.fontsice_pct: float = fontsize_pct
        self.start_x: float = start_x
        self.start_y: float = start_y
        self.row_end_in_pixel: float = row_end_in_pixel
        self.letter_space_px: float = 11*fontsize_pct
        self.line_spacing_px: float = 15*fontsize_pct
        self.inbetween_visible_size_x_px: float = 0.5*fontsize_pct
        self.inbetween_overlap_percent: float = 0.17
        self.inbetween_size_y_px: float = 12*fontsize_pct
        self.inbetween_color_state_1: str = inbetween_color_state_1
        self.inbetween_color_state_2: str = inbetween_color_state_2
        self.inbetween_clickable_color: str = inbetween_clickable_color
        self.number_length: int = number_length
        self.selection_strikethrough: bool = selection_strikethrough
        self.selection_underline: bool = selection_underline
        self.text_color_state_1: str = text_color_state_1
        self.text_color_state_2: str = text_color_state_2
        self.reload_letters_after_response: bool = reload_letters_after_response

        try:
            self.letter_widths: dict[str, float]  = self.letter_widths_by_fontfamily[fontfamily]
        except KeyError:
            available_fontfamilies: str = ", ".join(self.letter_widths_by_fontfamily.keys())
            raise KeyError(f"Fontfamily {fontfamily} not found. Available Fontfamilies are: {available_fontfamilies}.") 

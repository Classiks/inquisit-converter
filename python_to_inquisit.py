from modules.settings import Settings
from modules.inquisit_programmer import InquisitProgrammer

settings: Settings = Settings(
    text_input_file="text_input.txt",
    inquisit_output_file="inquisit_output.iqx",
    stimuli_output_file="stimulus_numbers_output.txt",
    trial_name="text_trial",
    fontfamily="Arial",
    fontsize_pct=4.3,
    start_x=100,
    start_y=250,
    row_end_in_pixel=1600,
    selection_strikethrough=True,
    selection_underline=True,
    inbetween_color_state_1="#AAAAAA33",
    inbetween_color_state_2="#FF0000",
    inbetween_clickable_color="#FFFFFF",
    text_color_state_1="#000000",
    text_color_state_2="#ff0000",
    reload_letters_after_response=False,
)

if __name__ == "__main__":
    programmer: InquisitProgrammer = InquisitProgrammer(settings)
    programmer.read_input_file()
    programmer.create_and_join_inquisit_blocks()
    programmer.write_inquisit_file()
    programmer.write_stimuli_list_file()

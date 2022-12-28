from modules.helper_functions import standardize_num_length, get_letter_or_return_None
from modules.settings import Settings
import modules.inquisit_elements as inquisit_elements

class InquisitProgrammer:

    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings
        self.current_x: float = settings.start_x
        self.current_y: float = settings.start_y

        self.text: str
        self.out_string: str
        self.text_stimuli_list: list[str]
        self.inbetween_stimuli_list: list[str]

    def read_input_file(self) -> None:
        with open(self.settings.text_input_file, mode="r", encoding="utf-8") as infile:
            self.text = infile.read()
    
    def write_inquisit_file(self) -> None:
        with open(self.settings.inquisit_ouput_file, mode="w", encoding="utf-8") as outfile:
            outfile.write(self.out_string)

    def write_stimuli_list_file(self) -> None:
        with open(self.settings.stimuli_output_file, mode="w", encoding="utf-8") as outfile:
            stimuli = [
                standardize_num_length(i, self.settings.number_length)
                for i in range(1, len(self.text)+1)
            ]
            for i, letter in zip(stimuli, self.text):
                if letter == "\n":
                    letter = "[linebreak]"
                if letter == " ":
                    letter = "[space]"
                outfile.write(f'{i} - {letter}\n')
    
    def create_defaults_block(self) -> str:
        return inquisit_elements.build_defaults_tag(
            fontfamily=self.settings.fontfamily,
            fontsize=self.settings.fontsice_pct
        )
    
    def create_values_block(self) -> str:
        values_block: str = "<values>\n"
        values_block += '\n'.join([
            inquisit_elements.build_value_for_text_stimulus(
                element=el,
                start_color=self.settings.text_color_state_1
            )
            for el in self.text_stimuli_list
        ])
        values_block += '\n\n'
        values_block += '\n'.join([
            inquisit_elements.build_value_for_inbetween_stimuli(
                element=el,
                start_color=self.settings.inbetween_color_state_1
            )
            for el in self.inbetween_stimuli_list
        ])
        values_block += "\n</values>"

        return values_block        

    def create_expressions_block(self) -> str:
        expressions_block: str = "<expressions>"
        expressions_block += ''.join([
            inquisit_elements.build_expression_for_text_stimulus(
                element=el,
                trial_name=self.settings.trial_name,
                settings=self.settings
            )
            for el in self.text_stimuli_list
        ])
        expressions_block += '\n'
        expressions_block += ''.join([
            inquisit_elements.build_expression_for_inbetween_stimulus(
                element=el,
                trial_name=self.settings.trial_name,
                settings=self.settings
            )
            for el in self.inbetween_stimuli_list
        ])
        expressions_block += "</expressions>"

        return expressions_block

    def create_inbetween_visible(self, name: str) -> str:
        return inquisit_elements.build_inbetween_visible_stimulus(
            name=name,
            x_position=self.current_x,
            y_position=self.current_y,
            width=self.settings.inbetween_visible_size_x_px,
            height=self.settings.inbetween_size_y_px,
        )

    def get_letter_overlap(self, i: int) -> float:
        letter: str|None = get_letter_or_return_None(self.text, i)
        if letter is None: return 0
        letter_width_in_px: float = self.settings.letter_widths[letter]*self.settings.letter_space_px
        return letter_width_in_px*self.settings.inbetween_overlap_percent

    def create_inbetween_clickable(self, name: str, i: int) -> str:
        left_letter_overlap: float = self.get_letter_overlap(i-1)
        right_letter_overlap: float = self.get_letter_overlap(i+1)

        # move x x% of left letter to the left
        overlapping_x: float = self.current_x - left_letter_overlap

        # create clickable element the size of x% of left letter + inbetweensize + x% of right letter to the left
        inbetween_clickable_x_size: float = self.settings.inbetween_visible_size_x_px + left_letter_overlap + right_letter_overlap

        return inquisit_elements.build_inbetween_clickable_stimulus(
            name=name,
            x_position=overlapping_x,
            y_position=self.current_y,
            width=inbetween_clickable_x_size,
            height=self.settings.inbetween_size_y_px,
            color=self.settings.inbetween_clickable_color
        )

    def create_inbetweens_also_return_name_move_current_x(self, i: int) -> tuple[str, str]:
        inbetween_element_name: str = f'{self.settings.trial_name}_inbetween_after_{standardize_num_length(i, self.settings.number_length)}_before_{standardize_num_length(i+1, self.settings.number_length)}'
        inbetween_visible: str = self.create_inbetween_visible(inbetween_element_name)
        inbetween_clickable: str = self.create_inbetween_clickable(inbetween_element_name, i)

        inbetween_elements: str = inbetween_visible + inbetween_clickable
        self.current_x += self.settings.inbetween_visible_size_x_px

        return (inbetween_elements, inbetween_element_name)

    def create_text_element_also_return_name_move_current_x(self, i: int) -> tuple[str, str]:
        letter: str = self.text[i]

        letter_index: str = standardize_num_length(i+1, self.settings.number_length)  # To start with letter_0001
        text_element_name: str = f'{self.settings.trial_name}_letter_{letter_index}'

        text_stimulus: str = inquisit_elements.build_text_stimulus(
            name=text_element_name,
            letter=letter,
            x_position=self.current_x,
            y_position=self.current_y,
            settings=self.settings
        )

        relative_spacing: float = self.settings.letter_widths[letter]*self.settings.letter_space_px
        self.current_x += relative_spacing

        return (text_stimulus, text_element_name)

    def check_for_linebreak_chracter_and_move_position(self, i: int) -> bool:
        letter = self.text[i]
        if letter == "\n":
            self.current_y += self.settings.line_spacing_px
            self.current_x = self.settings.start_x
            return True
        return False


    def check_for_linebreak_due_to_length_and_move_position(self, i: int) -> None:
        letter = self.text[i]
        if (len(self.text) > i):
            if (letter == " "):
                if self.current_x > self.settings.row_end_in_pixel:
                    self.current_y += self.settings.line_spacing_px
                    self.current_x = self.settings.start_x


    def create_text_and_inbetween_block(self):
        text_and_inbetween_elements_block: str = ""
        text_stimuli: list[str] = []
        inbetween_stimuli: list[str] = []

        inbetween_elements: str
        inbetween_name: str
        text_element: str
        text_name: str

        for i in range(len(self.text)):
            if self.check_for_linebreak_chracter_and_move_position(i):
                continue
            
            inbetween_elements, inbetween_name = self.create_inbetweens_also_return_name_move_current_x(i)
            inbetween_stimuli.append(inbetween_name)

            text_element, text_name = self.create_text_element_also_return_name_move_current_x(i)
            text_stimuli.append(text_name)

            text_and_inbetween_elements_block += (inbetween_elements + text_element)

            self.check_for_linebreak_due_to_length_and_move_position(i)
        # Have an 'inbetween' at the end
        inbetween_elements, inbetween_name = self.create_inbetweens_also_return_name_move_current_x(len(self.text))
        inbetween_stimuli.append(inbetween_name)
        text_and_inbetween_elements_block += inbetween_elements

        self.text_stimuli_list = text_stimuli
        self.inbetween_stimuli_list = inbetween_stimuli
        return text_and_inbetween_elements_block


    def create_trial_expressions(self) -> str:
        trial_expressions: str = ""
        trial_expressions += '\n'.join([f'\texpressions.{el}_expression;' for el in self.text_stimuli_list])
        trial_expressions += '\n\n'
        trial_expressions += '\n'.join([f'\texpressions.{el}_expression;' for el in self.inbetween_stimuli_list])
        
        return trial_expressions


    def create_trial_block_segment(self) -> str:
        return inquisit_elements.build_trial_block_segment(
            trial_name=self.settings.trial_name,
            text_stimuli = ', '.join(self.text_stimuli_list),
            inbetween_stimuli_clickable=', '.join([f'{e}_clickable' for e in self.inbetween_stimuli_list]),
            inbetween_stimuli_visible = ', '.join([f'{e}_visible' for e in self.inbetween_stimuli_list]),
            expressions=self.create_trial_expressions()
        )


    def create_and_join_inquisit_blocks(self) -> None:
        text_inbetween_block: str = self.create_text_and_inbetween_block()
        self.out_string = "\n\n".join([
            self.create_defaults_block(),
            self.create_values_block(),
            self.create_expressions_block(),
            text_inbetween_block,
            self.create_trial_block_segment(),
        ])


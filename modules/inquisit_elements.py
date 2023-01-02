from modules.settings import Settings

def build_defaults_tag(fontfamily: str, fontsize: float) -> str:
    return f"""
<defaults>
/ inputdevice = mouse
/ fontstyle = ("{fontfamily}", {fontsize}%)
</defaults>
"""

def build_value(element: str, start_color) -> str:
    return f"""/ {element}_state = 1
/ {element}_color = "{start_color}"
"""

def build_expression_for_text_stimulus(trial_name: str, element: str, settings: Settings) -> str:
    return f"""
/ {element}_expression = {{
    if (trial.{trial_name}.response == "{element}") {{
        if (values.{element}_state == 1) {{
            values.{element}_state += 1;
            values.{element}_color = "{settings.text_color_state_2}";
        }}
        else {{
            values.{element}_state -= 1;
            values.{element}_color = "{settings.text_color_state_1}";
        }}
    }}
}}
"""

def build_expression_for_inbetween_stimulus(trial_name: str, element: str, settings: Settings) -> str:
    return f"""/ {element}_expression = {{
    if (trial.{trial_name}.response == "{element}_clickable") {{
        if (values.{element}_state == 1) {{
            values.{element}_state += 1;
            values.{element}_color = "{settings.inbetween_color_state_2}";
        }}
        else {{
            values.{element}_state -= 1;
            values.{element}_color = "{settings.inbetween_color_state_1}";
        }}
    }}
}}
"""


def build_text_stimulus(name: str, letter: str, x_position: float, y_position: float, settings: Settings) -> str:
    first_state_letter: str = letter if letter != " " else "  "
    second_state_letter: str = letter if letter != " " else "/ "  # Make visible if the space is clicked
    if settings.selection_strikethrough:
        second_state_letter = f"<s>{second_state_letter}</s>"
    if settings.selection_underline:
        second_state_letter = f"<u>{second_state_letter}</u>"
    
    erase_after_response: str = "/ erase = false" if not settings.reload_letters_after_response else ""

    return f"""
<text {name}>
/ items = ("{first_state_letter}", "{second_state_letter}")
/ position = ({x_position}px, {y_position}px)
/ select = values.{name}_state
/ txcolor = values.{name}_color
/ valign = bottom
/ halign = left
{erase_after_response}
</text>
"""

def build_clickable_shape(name: str, width: float, height: float, x_position: float, y_position: float, color: str) -> str:
    return f"""
<shape {name}_clickable>
/ shape = rectangle
/ size = ({width}px, {height}px)
/ position = ({x_position}px, {y_position}px)
/ color = {color}
/ valign = bottom
/ halign = left
/ erase = false
</shape>
"""

def build_visible_shape(name: str, width: float, height: float, x_position: float, y_position: float) -> str:
    return f"""
<shape {name}_visible>
/ shape = rectangle
/ size = ({width}px, {height}px)
/ position = ({x_position}px, {y_position}px)
/ color = values.{name}_color
/ valign = bottom
/ halign = left
/ erase = false
</shape>
"""

def build_trial_block_segment(trial_name: str, inbetween_stimuli_clickable: str, text_stimuli: str, inbetween_stimuli_visible: str, expressions: str) -> str:
    return f"""
<trial {trial_name}>
/ stimulusframes = [
    1 = {inbetween_stimuli_clickable};
    2 = {text_stimuli};
    3 = {inbetween_stimuli_visible}
]
/ validresponse = (
    {inbetween_stimuli_clickable},
    {text_stimuli}
)
/ ontrialend = [
{expressions}
]
/ branch = [
    trial.{trial_name};
]
</trial>

<block main>
/ trials = [1 = {trial_name}]
</block>
"""
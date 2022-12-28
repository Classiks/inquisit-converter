def standardize_num_length(number: int, n: int) -> str:
    full_num = f'000000{number}'
    return full_num[-n:]


def get_letter_or_return_None(text: str, index: int) -> str|None:
    if index >= len(text):
        return None
    if text[index] == "\n":
        return None
    return text[index]
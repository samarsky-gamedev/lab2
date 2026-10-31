"""Лабораторная работа 2. Вариант 5: почтовые индексы России."""

import re


def is_index(value: str) -> bool:
    """Проверяет формат: ровно шесть цифр от 0 до 9."""
    return re.fullmatch(r"[0-9]{6}", value) is not None


def main() -> None:
    value = input("Введите индекс: ")
    if is_index(value):
        print("Верный формат индекса.")
    else:
        print("Нужно ровно шесть цифр от 0 до 9.")


if __name__ == "__main__":
    main()

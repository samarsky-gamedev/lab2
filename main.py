"""Лабораторная работа 2. Вариант 5: почтовые индексы России."""

import re
from pathlib import Path

PATTERN = re.compile(r"\b[0-9]{6}\b")


def is_index(value: str) -> bool:
    """Проверяет формат: ровно шесть цифр от 0 до 9."""
    return PATTERN.fullmatch(value) is not None


def find_indices(text: str) -> list[str]:
    """Ищет отдельные шестизначные записи, сохраняя порядок и повторы."""
    return PATTERN.findall(text)


def find_in_file(path: str) -> list[str]:
    return find_indices(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    print("Проверяется формат индекса, а не существование почтового отделения.")
    while True:
        try:
            print("\n1 Проверить; 2 Найти в тексте; 3 Найти в файле; 0 Выход")
            choice = input("Действие: ").strip()
            if choice == "0":
                break
            if choice == "1":
                value = input("Индекс: ")
                print("Верный формат." if is_index(value) else "Неверный формат.")
                continue
            if choice == "2":
                matches = find_indices(input("Текст: "))
            elif choice == "3":
                matches = find_in_file(input("Путь к файлу UTF-8: ").strip())
            else:
                print("Неизвестное действие.")
                continue
            print(", ".join(matches) or "Индексы не найдены.")
        except (OSError, UnicodeError) as error:
            print(f"Ошибка чтения файла: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nРабота завершена.")
            break


if __name__ == "__main__":
    main()

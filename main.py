"""Лабораторная работа 2. Вариант 5: почтовые индексы России."""

import re
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

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


class TestPostalIndex(unittest.TestCase):
    def test_valid_indices(self) -> None:
        for value in ("101000", "190000", "000001", "000000", "999999"):
            with self.subTest(value=value):
                self.assertTrue(is_index(value))

    def test_wrong_length(self) -> None:
        for value in ("", "1", "12345", "1234567"):
            with self.subTest(value=value):
                self.assertFalse(is_index(value))

    def test_wrong_characters(self) -> None:
        for value in ("12345A", "12-345", "12 345", "+12345"):
            with self.subTest(value=value):
                self.assertFalse(is_index(value))

    def test_spaces_are_not_part_of_index(self) -> None:
        for value in (" 101000", "101000 ", "101000\n"):
            with self.subTest(value=value):
                self.assertFalse(is_index(value))

    def test_only_ascii_digits(self) -> None:
        for value in ("１２３４５６", "١٢٣٤٥٦", "12345٦"):
            with self.subTest(value=value):
                self.assertFalse(is_index(value))
                self.assertEqual(find_indices(value), [])

    def test_search_preserves_order_and_duplicates(self) -> None:
        self.assertEqual(find_indices("101000, 190000; снова 101000."),
                         ["101000", "190000", "101000"])

    def test_no_parts_of_long_numbers(self) -> None:
        self.assertEqual(find_indices("1234567 0123456 123456789012"), [])

    def test_no_parts_of_words(self) -> None:
        self.assertEqual(find_indices("A101000 101000Б _101000 101000_"), [])

    def test_punctuation_and_line_breaks(self) -> None:
        self.assertEqual(find_indices("(101000)\nИндекс:190000!"),
                         ["101000", "190000"])

    def test_no_matches(self) -> None:
        self.assertEqual(find_indices(""), [])
        self.assertEqual(find_indices("Адрес без индекса, дом 12345"), [])

    def test_file_search(self) -> None:
        with TemporaryDirectory() as folder:
            path = Path(folder) / "адреса.txt"
            path.write_text("Москва: 101000\nСПб: 190000", encoding="utf-8")
            self.assertEqual(find_in_file(str(path)), ["101000", "190000"])

    def test_missing_file(self) -> None:
        with TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                find_in_file(str(Path(folder) / "missing.txt"))


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()

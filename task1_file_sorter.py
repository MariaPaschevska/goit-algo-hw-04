"""
Завдання 1: Рекурсивне копіювання та сортування файлів за розширенням.
 
Використання:
    python task1_file_sorter.py <шлях_до_джерела> [шлях_до_призначення]
 
Якщо шлях до призначення не вказано — використовується директорія "dist".
"""
 
import argparse
import shutil
from pathlib import Path
 
 
def parse_args() -> tuple[Path, Path]:
    """Парсинг аргументів командного рядка."""
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з джерела до директорії призначення, "
                    "розсортовуючи їх у піддиректорії за розширенням."
    )
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії")
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: dist)",
    )
    args = parser.parse_args()
    return args.source, args.destination
 
 
def copy_files_recursively(source_dir: Path, destination_dir: Path) -> None:
    """
    Рекурсивно обходить директорію source_dir.
    Файли копіює до піддиректорії destination_dir/<розширення>/.
    Директорії обходить рекурсивно.
    """
    try:
        items = list(source_dir.iterdir())
    except PermissionError:
        print(f"[!] Немає доступу до директорії: {source_dir}")
        return
    except OSError as exc:
        print(f"[!] Помилка читання {source_dir}: {exc}")
        return
 
    for item in items:
        if item.is_dir():
            # Рекурсивний виклик для піддиректорії
            copy_files_recursively(item, destination_dir)
        elif item.is_file():
            _copy_file(item, destination_dir)
 
 
def _copy_file(file_path: Path, destination_dir: Path) -> None:
    """
    Копіює один файл до піддиректорії destination_dir/<розширення>/.
    Якщо розширення відсутнє — використовується піддиректорія "no_extension".
    """
    extension = file_path.suffix.lstrip(".").lower() or "no_extension"
    target_dir = destination_dir / extension
 
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"[!] Не вдалося створити директорію {target_dir}: {exc}")
        return
 
    target_path = target_dir / file_path.name
 
    # Якщо файл із такою назвою вже існує — додаємо числовий суфікс
    counter = 1
    while target_path.exists():
        target_path = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1
 
    try:
        shutil.copy2(file_path, target_path)
        print(f"[✓] {file_path}  →  {target_path}")
    except PermissionError:
        print(f"[!] Немає доступу до файлу: {file_path}")
    except OSError as exc:
        print(f"[!] Помилка копіювання {file_path}: {exc}")
 
 
def main() -> None:
    source, destination = parse_args()
 
    if not source.exists():
        print(f"[!] Вихідна директорія не існує: {source}")
        return
 
    if not source.is_dir():
        print(f"[!] Вказаний шлях не є директорією: {source}")
        return
 
    print(f"Джерело     : {source.resolve()}")
    print(f"Призначення : {destination.resolve()}")
 
    copy_files_recursively(source, destination)

    print("Готово!")
 
if __name__ == "__main__":
    main()
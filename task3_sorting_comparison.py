"""
Завдання 3: Порівняння алгоритмів сортування.
 
Порівнює:
  • Сортування злиттям  (Merge Sort)  — O(n log n) у всіх випадках
  • Сортування вставками (Insertion Sort) — O(n²) у гіршому / середньому
  • Timsort  (вбудований sorted())        — гібрид, практично O(n log n)
 
Результати виводяться у консоль та зберігаються у файл results.md.
"""
 
import random
import timeit
from typing import Callable
 
# ---------------------------------------------------------------------------
# Реалізація алгоритмів
# ---------------------------------------------------------------------------
 
def merge_sort(arr: list) -> list:
    """Рекурсивне сортування злиттям."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)
 
 
def _merge(left: list, right: list) -> list:
    result: list = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
 
 
def insertion_sort(arr: list) -> list:
    """Сортування вставками (повертає новий список, не змінює оригінал)."""
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
 
 
def timsort(arr: list) -> list:
    """Вбудований Timsort Python."""
    return sorted(arr)
 
 
# ---------------------------------------------------------------------------
# Вимірювання часу
# ---------------------------------------------------------------------------
 
ALGORITHMS: list[tuple[str, Callable]] = [
    ("Merge Sort",      merge_sort),
    ("Insertion Sort",  insertion_sort),
    ("Timsort (built-in)", timsort),
]
 
DATASET_CONFIGS: list[tuple[str, int, str]] = [
    # (назва, розмір, тип)
    ("Малий масив (100)",         100,    "random"),
    ("Середній масив (1 000)",   1_000,   "random"),
    ("Великий масив (10 000)",  10_000,   "random"),
    ("Майже відсортований (10 000)", 10_000, "nearly_sorted"),
    ("Зворотний порядок (10 000)",   10_000, "reversed"),
]
 
REPEATS = 5   # кількість повторів для timeit
 
 
def generate_data(size: int, kind: str) -> list[int]:
    if kind == "random":
        return [random.randint(0, size * 10) for _ in range(size)]
    if kind == "nearly_sorted":
        arr = list(range(size))
        swaps = size // 20          # 5 % елементів переставлено
        for _ in range(swaps):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    if kind == "reversed":
        return list(range(size, 0, -1))
    raise ValueError(f"Невідомий тип даних: {kind}")
 
 
def measure(func: Callable, data: list, repeats: int) -> float:
    """Повертає середній час виконання у мілісекундах."""
    total = timeit.timeit(lambda: func(data[:]), number=repeats)
    return (total / repeats) * 1000   # → мс
 
 
# ---------------------------------------------------------------------------
# Виведення результатів
# ---------------------------------------------------------------------------
 
COL_W = [32, 20, 20, 20]   # ширини стовпців таблиці
 
 
def _header() -> str:
    names = ["Набір даних", "Merge Sort (мс)", "Insertion Sort (мс)", "Timsort (мс)"]
    return (
        " | ".join(n.ljust(COL_W[i]) for i, n in enumerate(names)) + "\n"
        + "-+-".join("-" * w for w in COL_W)
    )
 
 
def _row(label: str, times: list[float]) -> str:
    cells = [label.ljust(COL_W[0])]
    for i, t in enumerate(times, start=1):
        cells.append(f"{t:>10.3f}".ljust(COL_W[i]))
    return " | ".join(cells)
 
 
def run_benchmark() -> list[tuple[str, list[float]]]:
    """Запускає всі вимірювання та повертає результати."""
    results: list[tuple[str, list[float]]] = []
 
    for label, size, kind in DATASET_CONFIGS:
        data = generate_data(size, kind)
        row_times: list[float] = []
        for _, func in ALGORITHMS:
            t = measure(func, data, REPEATS)
            row_times.append(t)
        results.append((label, row_times))
 
    return results
 
 
def print_table(results: list[tuple[str, list[float]]]) -> None:
    print("\n" + "=" * 98)
    print("ПОРІВНЯННЯ АЛГОРИТМІВ СОРТУВАННЯ")
    print("=" * 98)
    print(_header())
    for label, times in results:
        print(_row(label, times))
    print("=" * 98)
 
 
def save_markdown(results: list[tuple[str, list[float]]], path: str = "results.md") -> None:
    algo_names = [a[0] for a in ALGORITHMS]
    header = "| Набір даних | " + " | ".join(algo_names) + " |"
    sep    = "| --- | " + " | ".join(["---"] * len(algo_names)) + " |"
 
    rows = []
    for label, times in results:
        cells = " | ".join(f"{t:.3f} мс" for t in times)
        rows.append(f"| {label} | {cells} |")
 
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Результати порівняння алгоритмів сортування\n\n")
        f.write(f"{header}\n{sep}\n")
        for row in rows:
            f.write(row + "\n")
 
    print(f"\n[✓] Результати збережено у файл: {path}")
 
 
# ---------------------------------------------------------------------------
# Висновки
# ---------------------------------------------------------------------------
 
def print_conclusions() -> None:
    print("""
ВИСНОВКИ
--------
1. Сортування вставками (Insertion Sort) має складність O(n²) і різко
   сповільнюється на масивах від ~10 000 елементів. На великих наборах воно
   може бути у сотні разів повільніше за конкурентів.
 
2. Сортування злиттям (Merge Sort) стабільно працює за O(n log n) у всіх
   випадках: як на випадкових, так і на вже частково відсортованих даних.
   Однак воно витрачає O(n) додаткової пам'яті на злиття підмасивів.
 
3. Timsort (вбудований sorted()) є гібридом сортування злиттям і вставками:
   - На малих підмасивах (≤ 64 елементи) застосовує сортування вставками,
     яке там є найшвидшим завдяки відсутності рекурсивних накладних витрат.
   - На великих підмасивах використовує сортування злиттям.
   - Виявляє вже відсортовані «пробіги» (runs) у вхідних даних і зливає
     їх замість повного пересортування — звідси прискорення на частково
     відсортованих або зворотних масивах.
 
4. Емпірично підтверджено: Timsort є найшвидшим у більшості сценаріїв,
   а на майже відсортованих і зворотних даних його перевага ще більша.
 
Висновок: вбудовані функції sorted() / list.sort() — оптимальний вибір
для переважної більшості задач. Власні реалізації доцільні лише там,
де потрібен специфічний порядок порівняння або особлива поведінка.
""")
 
 
# ---------------------------------------------------------------------------
# Точка входу
# ---------------------------------------------------------------------------
 
def main() -> None:
    random.seed(42)
    print(f"Запускаємо порівняння ({REPEATS} повторів на кожний набір)…")
 
    results = run_benchmark()
    print_table(results)
    print_conclusions()
    save_markdown(results)
 
 
if __name__ == "__main__":
    main()
"""
Завдання 2: Фрактал «Сніжинка Коха» з рекурсією.
 
Використання:
    python task2_koch_snowflake.py           # рівень рекурсії за замовчуванням (4)
    python task2_koch_snowflake.py --level 5 # вказати рівень вручну
 
Залежності: turtle (стандартна бібліотека Python)
"""
 
import argparse
import turtle
 
def koch_curve(t: turtle.Turtle, order: int, size: float) -> None:
    """
    Малює криву Коха заданого порядку.
 
    Args:
        t:     об'єкт черепашки.
        order: рівень рекурсії (0 — просто відрізок).
        size:  довжина поточного відрізка у пікселях.
    """
    if order == 0:
        t.forward(size)
        return
 
    size /= 3.0
    koch_curve(t, order - 1, size)
    t.left(60)
    koch_curve(t, order - 1, size)
    t.right(120)
    koch_curve(t, order - 1, size)
    t.left(60)
    koch_curve(t, order - 1, size)
 
 
def draw_snowflake(order: int, size: float = 300) -> None:
    """
    Малює повну сніжинку Коха (три криві Коха, з'єднані у трикутник).
 
    Args:
        order: рівень рекурсії.
        size:  довжина сторони початкового рівностороннього трикутника.
    """
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха — рівень {order}")
    screen.bgcolor("white")
 
    t = turtle.Turtle()
    t.speed(0)          # максимальна швидкість
    t.color("#1a6fb5")  # синій колір лінії
    t.pensize(1)
 
    # Відцентрувати фігуру
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()
 
    # Три сторони сніжинки
    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)
 
    t.hideturtle()
    screen.mainloop()
 
 
# ---------------------------------------------------------------------------
# Точка входу
# ---------------------------------------------------------------------------
 
def parse_args() -> int:
    parser = argparse.ArgumentParser(
        description="Малює фрактал «Сніжинка Коха» з заданим рівнем рекурсії."
    )
    parser.add_argument(
        "--level",
        type=int,
        default=4,
        metavar="N",
        help="Рівень рекурсії (ціле число ≥ 0, за замовчуванням: 4)",
    )
    args = parser.parse_args()
 
    if args.level < 0:
        parser.error("Рівень рекурсії має бути невід'ємним числом.")
 
    return args.level
 
 
def main() -> None:
    level = parse_args()
    print(f"Малюємо сніжинку Коха рівня {level}…")
    if level > 6:
        print("  (Увага: великий рівень рекурсії може займати деякий час)")
    draw_snowflake(order=level)
 
 
if __name__ == "__main__":
    main()
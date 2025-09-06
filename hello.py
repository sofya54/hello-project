import random


# Создаем пустое поле 10x10
def create_board():
    board = []
    for y in range(10):
        row = []
        for x in range(10):
            row.append(' ')
        board.append(row)
    return board


# Отображаем поле
def print_board(board, hide_ships=False):
    print("   A B C D E F G H I J")
    for i in range(10):
        row = []
        for j in range(10):
            cell = board[i][j]
            if hide_ships and cell == 'V':
                row.append(' ')
            else:
                row.append(cell)
        print(f"{i + 1:2} " + " ".join(row))


# Проверяем, можно ли разместить корабль
def can_place_ship(board, row, col, size, direction):
    if direction == 0:  # Горизонтально
        if col + size > 10:
            return False
        for j in range(col - 1, col + size + 1):
            for i in range(row - 1, row + 2):
                if 0 <= i < 10 and 0 <= j < 10:
                    if board[i][j] == 'V':
                        return False
    else:  # Вертикально
        if row + size > 10:
            return False
        for i in range(row - 1, row + size + 1):
            for j in range(col - 1, col + 2):
                if 0 <= i < 10 and 0 <= j < 10:
                    if board[i][j] == 'V':
                        return False
    return True


# Размещаем корабль на поле
def place_ship(board, size):
    while True:
        direction = random.randint(0, 1)  # 0 - горизонтально, 1 - вертикально
        if direction == 0:
            row = random.randint(0, 9)  # в коде мы говорим in range(10), значит 9 - последняя цифра
            col = random.randint(0, 10 - size)
        else:
            row = random.randint(0, 10 - size)
            col = random.randint(0, 9)

        if can_place_ship(board, row, col, size, direction):
            if direction == 0:
                for j in range(col, col + size):
                    board[row][j] = 'V'
            else:
                for i in range(row, row + size):
                    board[i][col] = 'V'
            break


# Инициализируем поле с кораблями
def make_board():
    board = create_board()
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Список кораблей
    for size in ships:
        place_ship(board, size)
    return board


# Проверяем попадание
def is_hit(board, row, col):
    return board[row][col] == 'V'


# Проверяем, убит ли корабль
def is_removed(board, row, col):
    # Проверяем все клетки вокруг, чтобы определить размер корабля
    # Это упрощенная версия, можно доработать
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 10 and 0 <= c < 10 and board[r][c] == 'V':
            return False
    return True


# Основная функция игры
def play_game():
    print("Добро пожаловать в Морской бой!")
    print("Ваше поле:")
    player_board = make_board()
    computer_board = make_board()
    player_hits = create_board()  # Поле для выстрелов игрока
    computer_hits = create_board()  # Поле для выстрелов компьютера

    player_ships = sum(row.count('V') for row in player_board)
    computer_ships = sum(row.count('V') for row in computer_board)

    while player_ships > 0 and computer_ships > 0:
        # Ход игрока
        print("\nВаше поле:")
        print_board(player_board)
        print("\nВаши выстрелы:")
        print_board(player_hits)

        while True:
            move = input("\nВаш ход (например, A1): ").upper()
            if len(move) < 2 or len(move) > 3:
                print("Некорректный ввод. Введите букву и цифру (например, A1).")
                continue
            if not move[0].isalpha() or move[0] not in "ABCDEFGHIJ":
                print("Первым символом должна быть буква от A до J.")
                continue
            if not move[1:].isdigit():
                print("После буквы должны быть цифры (1-10).")
                continue
            col = ord(move[0]) - ord('A')
            row = int(move[1:]) - 1
            if not (0 <= row < 10 and 0 <= col < 10):
                print("Координаты вне диапазона. Используйте A1-J10.")
                continue
            if player_hits[row][col] != ' ':
                print("Вы уже стреляли сюда!")
                continue
            break
        if is_hit(computer_board, row, col):
            print("Попадание!")
            player_hits[row][col] = 'X'
            computer_board[row][col] = 'X'
            computer_ships -= 1
            if is_removed(computer_board, row, col):
                print("Корабль противника потоплен!")
        else:
            print("Мимо!")
            player_hits[row][col] = '0'
            computer_board[row][col] = '0'

        if computer_ships == 0:
            break

        # Ход компьютера
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if computer_hits[row][col] == ' ':
                break

        if is_hit(player_board, row, col):
            print(f"Компьютер попал в {chr(col + ord('A'))}{row + 1}!")
            computer_hits[row][col] = 'X'
            player_board[row][col] = 'X'
            player_ships -= 1
            if is_removed(player_board, row, col):
                print("Ваш корабль потоплен!")
        else:
            print(f"Компьютер промахнулся в {chr(col + ord('A'))}{row + 1}.")
            computer_hits[row][col] = '0'
            player_board[row][col] = '0'

        print("\nРезультат хода компьютера:")
        print_board(player_board)

    if player_ships == 0:
        print("\nКомпьютер победил!")
    else:
        print("\nВы победили!")
    print("\nИгра окончена.")


# Запускаем игру
play_game()

import random

players = []
table = []
cells = []


class Player:
    def __init__(self, name, coin):
        self.name = name
        self.coin = coin
        self.bets = {}
        self.reset_table()

    def set_bet_coin(self, bet_coin, bet_cell):
        self.coin -= bet_coin
        self.bets[bet_cell] = bet_coin
        print(self.name + ' bet ' + str(bet_coin) +
              ' coin(s) to ' + bet_cell + '.')

    def reset_table(self):
        for cell in table:
            self.bets.update({cell.name: 0})


class Human(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)
        self.double_up = False

    def bet(self):
        if self.coin >= 99:
            max_bet_coin = 99
        else:
            max_bet_coin = self.coin

        if self.double_up:
            bet_coin = self.bets[self.last_bet_cell] * 2
            print(f'{self.name}, you chose to double up. Your bet is automatically set to {bet_coin} on {self.last_bet_cell}.')
        else:
            bet_message = 'How many coins do you bet?:(1-' + \
                str(max_bet_coin) + ')'
            bet_coin = input(bet_message)
            while not self.enable_bet_coin(bet_coin, max_bet_coin):
                bet_coin = input(bet_message)

            bet_message = 'On what do you bet?: (R, B, 1-8)'
            bet_cell = input(bet_message)
            while not self.enable_bet_cell(bet_cell):
                bet_cell = input(bet_message)

            self.last_bet_cell = bet_cell
            self.double_up = False

        super().set_bet_coin(int(bet_coin), self.last_bet_cell)

    def enable_bet_coin(self, string, max_bet_coin):
        if string.isdigit():
            number = int(string)
            if number >= 1 and number <= max_bet_coin:
                return True
            else:
                return False
        else:
            return False

    def enable_bet_cell(self, string):
        if string.isdigit():
            number = int(string)
            if number >= 1 and number <= 8:
                return True
            else:
                return False
        else:
            if string == 'R' or string == 'B':
                return True
            else:
                return False


class Computer(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)
        self.last_bet_cell = None

    def bet(self):
        if self.coin >= 99:
            max_bet_coin = 99
        else:
            max_bet_coin = self.coin

        # 50% chance of doubling up
        if random.random() < 0.5 and self.last_bet_cell:
            bet_coin = self.bets[self.last_bet_cell] * 2
            print(f'{self.name} chose to double up. Their bet is automatically set to {bet_coin} on {self.last_bet_cell}.')
        else:
            bet_coin = random.randint(1, max_bet_coin)

            bet_cell_number = random.randint(0, len(cells) - 1)
            bet_cell = cells[bet_cell_number]
            self.last_bet_cell = bet_cell

        super().set_bet_coin(bet_coin, self.last_bet_cell)



class Cell:
    def __init__(self, name, rate, color):
        self.name = name
        self.rate = rate
        self.color = color


class ColorBase:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    END = '\033[0m'


def set_cells():
    global cells
    cells = []
    for cell in table:
        cells.append(cell.__dict__['name'])


def create_players():
    global players
    human = Human('MY', 500)
    computer1 = Computer('C1', 500)
    computer2 = Computer('C2', 500)
    computer3 = Computer('C3', 500)
    players = [human, computer1, computer2, computer3]


def bet_players():
    for player in players:
        player.bet()


def check_hit():
    hit_cell_number = random.randint(0, len(cells) - 1)
    hit_cell = cells[hit_cell_number]
    hit_color = table[hit_cell_number].color
    print('Winning number is ' + hit_cell + ' (' + hit_color + ').')

    for player in players:
        if player.bets[hit_cell] >= 1:
            win_player(player, hit_cell_number, hit_color)


def win_player(player, hit_cell_number, hit_color):
    hit_cell = cells[hit_cell_number]
    win_rate = table[hit_cell_number].rate

    if hit_cell in ['R', 'B'] and hit_cell == hit_color:
        win_coin = player.bets[hit_cell] * win_rate
    elif hit_cell.isdigit() and 1 <= int(hit_cell) <= 8:
        win_coin = player.bets[hit_cell] * win_rate
    else:
        win_coin = player.bets[hit_cell] * 2  # Default payout for R and B

    player.coin += win_coin

    # Double up logic
    if isinstance(player, Human):
        double_up_choice = input(f'{player.name}, you won! Do you want to double up your bet? (yes/no): ')
        if double_up_choice.lower() == 'yes':
            player.double_up = True

    print(player.name + ' won. Gained ' + str(win_coin) + ' coins.')


def show_coin():
    message = '[Players\' coin] '
    for player in players:
        message += player.name + ': ' + str(player.coin) + ' / '
    print(message)


def create_table():
    global table
    table.append(Cell('R', 2, 'red'))
    table.append(Cell('B', 2, 'black'))
    table.append(Cell('1', 8, 'red'))
    table.append(Cell('2', 8, 'black'))
    table.append(Cell('3', 8, 'red'))
    table.append(Cell('4', 8, 'black'))
    table.append(Cell('5', 8, 'red'))
    table.append(Cell('6', 8, 'black'))
    table.append(Cell('7', 8, 'red'))
    table.append(Cell('8', 8, 'black'))


def show_table():
    row = green_bar() + '_____' + green_bar()
    for player in players:
        row += player.name + green_bar()
    print(row)

    for cell in table:
        row = green_bar() + color(cell.color, cell.name +
                                  '(x' + str(cell.rate) + ')') + green_bar()
        for player in players:
            row += str(player.bets[cell.name]).zfill(2) + green_bar()
        print(row)


def reset_table():
    for player in players:
        player.reset_table()


def color(color_name, string):
    if color_name == 'red':
        return ColorBase.RED + string + ColorBase.END
    elif color_name == 'green':
        return ColorBase.GREEN + string + ColorBase.END
    else:
        return string


def green_bar():
    return color('green', '｜')


def initialize():
    create_table()
    create_players()
    set_cells()


def play_once():
    reset_table()
    bet_players()
    show_table()
    check_hit()
    show_coin()


def is_game_end():
    for player in players:
        if player.coin <= 0:
            return True
    return False


def game_end():
    for player in players:
        if player.coin <= 0:
            print('Game ends as ' + player.name + ' has no coin.')


def play():
    initialize()
    show_coin()
    while not is_game_end():
        play_once()
    else:
        game_end()


play()

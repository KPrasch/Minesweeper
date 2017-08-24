"""
Gameplay Initialization for minesweeper.
"""


from minefield import Minefield


def game():

    m = Minefield.new_game()
    m.welcome()

    actions = {('r', 'reveal'): m.select,
               ('u', 'unflag'): m.unflag,
               ('f', 'flag'): m.flag}
               
    exit_options = ('quit', 'exit', 'q')

    command = None
    while command not in exit_options and not m.game_over:
        print(m)

        location = input("Enter X, Y Coord. >? ")
        x, y = tuple(map(int, location.split(',')))
        coord = y, x

        action = input("Enter action (f)lag (u)nflag or (r)eveal").lower()
        for opts, func in actions.items():
            if action in opts:
                func(coord)
                break
        else:
            print("No such command.")
            continue

        if m.check_win():
            print("You win!")

if __name__ == "__main__":
    game()

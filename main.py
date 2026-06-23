from game.GameEngine import GameEngine

def run_game(game):

    while True:

        game.clear_screen()
        game.print_board()

        selection = game.get_selection()
        game.apply_selection(selection)

        if game.is_won():
            print("POBEDA")
            break

        if game.is_lost():
            print("PORAZ")
            break


def main():

    while True:

        print("\n=== CONNECTIONS ===")
        print("1. Nova igra")
        print("2. Izlaz")

        choice = input("> ").strip()

        if choice == "1":
            
            game = GameEngine()
            run_game(game)

        elif choice == "2":

            print("BYE!")
            break

        else:
            
            print("Nevalid unos")

if __name__ == "__main__":

    main()
from game.logic import check_selection
from game.data import PUZZLE
from game.data import GROUP_COLORS
import os
import random

class GameEngine:

    def __init__(self):

        self.solution = PUZZLE
        self.words = []
        for group in self.solution.values():
            self.words.extend(group)

        self.solved_groups = []
        self.locked_groups = []
        self.locked_words = set()
        self.active_words = self.words.copy()
        self.all_worlds = self.words.copy()
        self.attempts = 4
        self.current_selection = []
        self.used_attempts = set()
        self.last_message = ""
        random.shuffle(self.words)

        self.group_colors = {
            "Boje": "#f9d923",        # žuta
            "Zivotinje": "#6bcB77",   # zelena
            "Drzave": "#4d96ff",      # plava
            "Sportovi": "#b983ff"     # ljubičasta
        }

    def print_board(self):

        print("\n=== CONNECTIONS GAME ===\n")


        if self.locked_groups:

            print("SOLVED GROUPS:\n")

            for symbol, category, words in self.locked_groups:

                print(f"{symbol} {category}: {', '.join(words)}")

            print()

        print("ACTIVE GRID:\n")

        if self.last_message:

                print(self.last_message)
                print()

        for i,word in enumerate(self.active_words, 1):

            if word in self.current_selection:

                display = f"[{word}]"

            else:

                display = word

            print(f"{i}.{display:12}", end = "")


            if i % 4 == 0:

                print()

        print("\n")
        print(f"Attempts left: {self.attempts}\n")



    def get_selection(self):

        while True:

            try:

                print("\nIzaberi 4 broja:")
                indexes = input("> ").split()

                if len(indexes) == 1 and indexes[0].lower() == 'hint':
                    self.give_hint()
                    return self.get_selection()

                if len(set(indexes)) != 4:
                    print("Moras uneti tacno 4 broja")
                    continue

                selection = []
                
                for idx in indexes:

                    num = int(idx)

                    if num < 1 or num > len(self.active_words):
                        raise ValueError
                    
                    selection.append(self.active_words[num -1])

                self.current_selection = selection

                print("Izabrano:")
                for w in selection:
                    print("-", w)

                return selection
            
            except ValueError:
                
                print("Nevalid unos. Probaj ponovo")


    def apply_selection(self, selection):

        key = tuple(sorted(selection))
        if key in self.used_attempts:
            print("Vec si probao ovu kombinaciju")
            return False

        if len(set(selection)) != 4:
            return False
        
        self.used_attempts.add(key)

        if check_selection(selection):

            self.last_message = "✅ Pogodjena grupa!"
            self.lock_group(selection)
            return True
        
        else:

            if self.is_almost_group(selection):

                self.last_message = "🔥 Blizu! 3 od 4 reci pripadaju istoj grupi."

            else:

                self.last_message = "WRONG"

            self.attempts -= 1
            self.current_selection = []
            return False
        
    def remove_group(self, selection):

        for word in selection:

            self.active_words.remove(word)


    def lock_group(self, selection):

        category = None

        for word in selection:
            for cat,words in self.solution.items():
                if word in words:
                    category = cat
                    break

        symbol = GROUP_COLORS.get(category, "⬜")

        print(f"\n{symbol} GRUPA RESENA: {category}")

        self.locked_groups.append((symbol, category, selection))

        self.locked_words.update(selection)
        
    def is_won(self):

        return  len(self.locked_words) == len(self.all_worlds)
    
    def is_lost(self):

        return self.attempts <= 0
    
    def clear_screen(self):

        os.system("cls" if os.name == 'nt' else "clear")

    def give_hint(self):

        print("HINT:")

        hints = []

        for cat, words in self.solution.items():

            remaining = [word for word in words if word in self.active_words]

            if remaining:

                hint = f"{cat}: {remaining[0]}"
                print(f"- {cat}: {remaining[0]}")
                hints.append(hint)

        return hints

    def is_almost_group(self, selection):

        for words in self.solution.values():

            matches = 0

            for word in selection:

                if word in words:
                    
                    matches += 1

                if matches == 3:
                    return True
                
        return False
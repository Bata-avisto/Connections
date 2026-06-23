import tkinter as tk
from game.GameEngine import GameEngine

class ConnectionsGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Connections")

        self.game = GameEngine()

        self.buttons = []
        self.selected = []

        self.create_ui()
        self.render_board()

    def create_ui(self):

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx = 10, pady = 10)

        self.submit_btn = tk.Button(
            self.root,
            text = "Submit",
            command = self.submit
        ).pack(pady = 10)


        self.status_label = tk.Label(
            
            self.root,
            text = "Select 4 words",
            font = ("Arial", 12)
        )

        self.status_label.pack(pady = 5)

        self.hint_btn = tk.Button(
            
            self.root,
            text = "Hint",
            command = self.show_hint

        ).pack(pady = 5)

    def render_board(self):

        #reset UI

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.buttons = []

        category = None

        for i, word in enumerate(self.game.all_worlds):


            category = None

            for c, words in self.game.solution.items():

                if word in words:
                 
                 category = c
                 break
        
            btn = tk.Button(
                self.frame,
                text = word,
                width=12,
                height=2,
                command = lambda w=word: self.toggle_select(w)
            )

            btn.grid(row = i // 4, column =i % 4, padx = 5, pady = 5)

            self.buttons.append((btn, word))

            if word in self.game.locked_words:

                color = self.game.group_colors.get(category, "gray")

                btn.config(
                    bg=color,
                    disabledforeground="black",
                    state="disabled"
                    )
                

    def toggle_select(self, word):

        if word in self.game.locked_words:

            return

        if word in self.selected:

            self.selected.remove(word)

        else:

            if len(self.selected) < 4:

                self.selected.append(word)

        self.update_ui()


    def update_ui(self):

        for btn, word in self.buttons:

            if word in self.game.locked_words:

                category = None

                for c, words in self.game.solution.items():

                    if word in words:   

                        category = c
                        break

                btn.config(

                    bg = self.game.group_colors[category],
                    state = "disabled",
                    disabledforeground = "black"

                )

            elif word in self.selected:

                btn.config(bg = "yellow")

            else:

                btn.config(bg = "SystemButtonFace")
            

    def submit(self):

        if len(self.selected) != 4:

            self.status_label.config(text = "Moras izabrati 4 reci")
            return
        
        result = self.game.apply_selection(self.selected)

        one_away = self.game.is_almost_group(self.selected)


        self.selected = []

        self.render_board()

        if result:

            self.status_label.config(text = "Tacno! Pogodjena Grupa!")

        elif one_away:

            self.status_label.config(text = "One away!")

        else:

            self.status_label.config(text = "Pogresno!")

        if self.game.is_won():

            self.show_end("WIN")

        if self.game.is_lost():

            self.show_end("LOSS")

    def show_end(self, result):

        popup = tk.Toplevel(self.root)
        popup.title("Game Over")

        if result == "WIN":
            
            msg = "POBEDA"

        else:

            msg = "PORAZ"   

        tk.Label(
            popup,
            text = msg,
            font =("Arial", 20)
        ).pack(padx = 20, pady = 20)


    def show_hint(self):

        hints = self.game.give_hint()

        popup = tk.Toplevel(self.root)
        popup.title("Hint")

        tk.Label(

            popup,
            text= "\n".join(hints),
            font = ("Arial", 12)


        ).pack(padx = 20, pady = 20)


if __name__ == "__main__":

    root = tk.Tk()
    app = ConnectionsGUI(root)
    root.mainloop()
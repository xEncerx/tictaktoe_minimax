from tkinter.messagebox import showinfo
import tkinter as tk

class Theme:
    button_bg = "#ebf1f1"
    button_fg = "#34495e"
    main_bg = "#14212a"


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()

        self.current_player = "X"
        self.buttons = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]
        self.theme = Theme()

        self._initialize()

    def _initialize(self) -> None:
        self._restart_img = tk.PhotoImage(file="./images/restart.png")
        self.window.iconbitmap(r"./images/icon.ico")
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("318x400")
        self.window.configure(bg=self.theme.main_bg)
        self.window.resizable(False, False)

        for x in range(3):
            for y in range(3):
                self.buttons[x][y] = tk.Button(text=self.board[x][y], relief=tk.RAISED, width=3, height=1, bg=self.theme.button_bg, fg=self.theme.button_fg,
                                               bd=2, font=("Arial", 40, "bold"), command=lambda row=x, col=y: self._game_button_click(row, col))
                self.buttons[x][y].grid(row=x, column=y)

        self._restart_button = tk.Button(font=("Arial", 14, "bold"), bg=self.theme.button_bg, fg=self.theme.button_fg,
                                         image=self._restart_img, command=self._restart_game)
        self._restart_button.grid(row=3, column=1, pady=10)

    def _check_game_status(self) -> None:
        if self._check_winner():
            showinfo("Game Over", f"Player {self.current_player} wins!")

        elif self._check_draw():
            showinfo("Game Over", "It's a draw!")

        else:
            self.current_player = "O" if self.current_player == "X" else "X"

    def _game_button_click(self, x: int, y: int) -> None:
        if self.board[x][y] == "":
            self.buttons[x][y].config(text=self.current_player, state=tk.DISABLED, disabledforeground=self.theme.button_fg)
            self.board[x][y] = self.current_player

            self._check_game_status()

            if self.current_player == "O":
                self._ai_move()

    def _check_winner(self) -> bool:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def _check_draw(self) -> bool:
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "":
                    return False
        return True

    def _restart_game(self) -> None:
        for x in range(3):
            for y in range(3):
                self.board[x][y] = ""
                self.buttons[x][y].config(text="", state=tk.NORMAL)
        self.current_player = "X"

    def _minimax(self, is_maximizing: bool) -> int:
        if self._check_winner():
            return -1 if is_maximizing else 1
        if self._check_draw():
            return 0

        best_score = float("-inf" if is_maximizing else "inf")
        player = "O" if is_maximizing else "X"

        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "":
                    self.board[x][y] = player
                    score = self._minimax(not is_maximizing)
                    self.board[x][y] = ""
                    best_score = max(score, best_score) if is_maximizing else min(score, best_score)

        return best_score

    def _ai_move(self) -> None:
        best_score = float("-inf")
        best_move_x = best_move_y = None
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "":
                    self.board[x][y] = "O"
                    score = self._minimax(False)
                    self.board[x][y] = ""
                    if score > best_score:
                        best_score = score
                        best_move_x, best_move_y = x, y

        self.board[best_move_x][best_move_y] = "O"
        self.buttons[best_move_x][best_move_y].config(text="O", state=tk.DISABLED, disabledforeground=self.theme.button_fg)

        self._check_game_status()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
from board import Board

NAMES = {"a": "left", "d": "right", "w": "up", "s": "down"}


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.previous = None  # one-level undo: state before the last move

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves:
            return False
        before = self.board.snapshot()
        changed = moves[key]()
        if not changed:
            return False  # unchanged move: no new tile, nothing to undo
        self.previous = before
        self.board.add_random_tile()
        self.best_score = max(self.best_score, self.board.score)
        return True

    def undo(self):
        if self.previous is None:
            return False
        self.board.restore(self.previous)  # restores grid AND score, adds no tile
        self.previous = None               # only one level of undo
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            if self.board.has_won():
                print("You reached 2048! You win!")
                return
            if not self.board.can_move():
                print("No legal moves remain. Game over.")
                return

            key = input("> ").strip().lower()
            if key == "q":
                print("Thanks for playing!")
                return
            if key == "u":
                print("Undid last move." if self.undo() else "Nothing to undo.")
                continue
            if key not in NAMES:
                print("Use W/A/S/D to move, U to undo, Q to quit.")
                continue

            if self.move(key):
                if self.board.last_merges:
                    print(f"Moved {NAMES[key]}: {self.board.last_merges} merge(s), "
                          f"+{self.board.last_gain} points.")
                else:
                    print(f"Moved {NAMES[key]}.")
            else:
                print("Nothing moved — try another direction.")

import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.last_gain = 0    # points gained by the most recent move
        self.last_merges = 0  # merges made by the most recent move
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def _slide(line):
        """Slide one line to the left. Each ORIGINAL tile merges at most once.
        Returns (new_line, points_gained, merge_count)."""
        values = [x for x in line if x]
        result = []
        gained = 0
        merges = 0
        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged = values[i] * 2
                result.append(merged)
                gained += merged
                merges += 1
                i += 2  # skip BOTH tiles that just merged
            else:
                result.append(values[i])
                i += 1
        return result + [0] * (SIZE - len(result)), gained, merges

    @staticmethod
    def slide_line(line):
        return Board._slide(line)[0]

    def _move(self, vertical, reverse):
        changed = False
        gained = 0
        merges = 0
        for i in range(SIZE):
            old = [self.grid[r][i] for r in range(SIZE)] if vertical else self.grid[i][:]
            line = old[::-1] if reverse else old
            new, g, m = self._slide(line)
            if reverse:
                new = new[::-1]
            if vertical:
                for r in range(SIZE):
                    self.grid[r][i] = new[r]
            else:
                self.grid[i] = new
            changed |= old != new
            gained += g
            merges += m
        self.score += gained
        self.last_gain = gained
        self.last_merges = merges
        return changed

    def move_left(self):
        return self._move(vertical=False, reverse=False)

    def move_right(self):
        return self._move(vertical=False, reverse=True)

    def move_up(self):
        return self._move(vertical=True, reverse=False)

    def move_down(self):
        return self._move(vertical=True, reverse=True)

    def has_won(self):
        return any(2048 in row for row in self.grid)

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def snapshot(self):
        """Copy of board + score, used for undo."""
        return [row[:] for row in self.grid], self.score

    def restore(self, snap):
        self.grid = [row[:] for row in snap[0]]
        self.score = snap[1]

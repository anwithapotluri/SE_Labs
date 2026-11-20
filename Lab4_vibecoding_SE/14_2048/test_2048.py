from board import Board
from game import Game


def empty():
    return [[0] * 4 for _ in range(4)]


def test_no_chain_merge():
    assert Board.slide_line([2, 2, 4, 0]) == [4, 4, 0, 0]
    assert Board.slide_line([4, 4, 8, 0]) == [8, 8, 0, 0]

def test_four_equal():
    assert Board.slide_line([2, 2, 2, 2]) == [4, 4, 0, 0]

def test_three_equal():
    assert Board.slide_line([2, 2, 2, 0]) == [4, 2, 0, 0]

def test_ordinary_slide():
    assert Board.slide_line([0, 0, 0, 2]) == [2, 0, 0, 0]
    assert Board.slide_line([2, 4, 8, 16]) == [2, 4, 8, 16]

def test_separated_equal_pair():
    assert Board.slide_line([2, 0, 0, 2]) == [4, 0, 0, 0]
    assert Board.slide_line([2, 4, 2, 0]) == [2, 4, 2, 0]

def test_unchanged_move_adds_no_tile():
    g = Game()
    g.board.grid = empty()
    g.board.grid[0] = [2, 4, 8, 16]
    assert g.move("a") is False
    assert sum(1 for r in g.board.grid for x in r if x) == 4

def test_score_and_best():
    g = Game()
    g.board.grid = empty()
    g.board.grid[0] = [2, 2, 0, 0]
    g.board.score = 0
    assert g.move("a") is True
    assert g.board.score == 4 and g.best_score == 4

def test_undo_restores_board_and_score():
    g = Game()
    g.board.grid = empty()
    g.board.grid[0] = [2, 2, 0, 0]
    g.board.score = 0
    before = [r[:] for r in g.board.grid]
    g.move("a")
    assert g.undo() is True
    assert g.board.grid == before and g.board.score == 0
    assert g.best_score == 4
    assert g.undo() is False

def test_win_detection():
    b = Board()
    b.grid = empty()
    b.grid[1][1] = 2048
    assert b.has_won()

def test_no_move_board():
    b = Board()
    b.grid = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
    assert not b.can_move()

def test_all_directions():
    b = Board(); b.grid = empty(); b.grid[0] = [2, 2, 4, 0]
    b.move_right(); assert b.grid[0] == [0, 0, 4, 4]
    b = Board(); b.grid = empty(); b.grid[0][0] = 2; b.grid[1][0] = 2; b.grid[2][0] = 4
    b.move_up(); assert [b.grid[r][0] for r in range(4)] == [4, 4, 0, 0]
    b = Board(); b.grid = empty(); b.grid[0][0] = 2; b.grid[1][0] = 2; b.grid[2][0] = 4
    b.move_down(); assert [b.grid[r][0] for r in range(4)] == [0, 0, 4, 4]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("All tests passed")

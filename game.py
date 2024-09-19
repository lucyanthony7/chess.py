from chess import Board, Piece

board = Board()

board.start_game()
board.move("p6w",[3,5])
board.move("p5b",[4,4])
board.move("p6w",[4,4])
board.move("k2b",[5,5])
board.move("k2w",[2,6])
board.move("p3w",[2,2])
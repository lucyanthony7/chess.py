from typing import List
import pdb


class Board:
    def __init__(self):
        self.pieces: List[Piece] = []
        self.pieces_taken: List[Piece] = []
        self.current_colour = None
        self.white_king_can_castle_left = True
        self.white_king_can_castle_right = True
        self.black_king_can_castle_left = True
        self.black_king_can_castle_right = True
        
    
    def add_piece(self, piece):
        self.pieces.append(piece)
        
    
    def show_board(self, player):  
            rows = []    
            for i in range(8):
                rows.append([])
                for j in range(8):
                    rows[i].append("   ")
            for piece in self.pieces:
                rows[piece.position[0]][piece.position[1]] = piece.name
                
            if player == "white":
                rows.reverse()  
                i = 0
                for row in rows:
                    print(str(7 - i) + str(row))
                    i += 1
                print("    0      1      2      3      4      5      6      7")
                print(" ")
        
            elif player == "black":
                i = 0
                for row in rows:
                    row.reverse()
                    print(str(i) + str(row))
                    i += 1
                print("    7      6      5      4      3      2      1      0")
                print(" ")
            
            
    def move_valid(self, piece, new_position):
        if piece.type != "pawn":
            if new_position in piece.possible_moves():
                if new_position != piece.position:
                    piece_in_new_position = self.find_piece_on_board(new_position)
                    if piece_in_new_position == None:
                        boolean = True
                        for i in self.pieces:
                            if i.position in piece.piece_in_the_way(new_position):
                                boolean = False
                        return boolean
                    elif piece_in_new_position.colour == piece.colour:
                        return False
                    elif piece_in_new_position.colour != piece.colour:
                        return "TAKE"
            else:
                return False
        if piece.type == "pawn":
            if new_position != piece.position:
                piece_in_new_position = self.find_piece_on_board(new_position)
                if piece_in_new_position == None:
                    if new_position in self.pawn_possible_moves(piece):
                        if (piece.position[0] == 6) and (piece.colour == "white"):
                            return "PAWN BACK ROW"
                        if (piece.position[0] == 1) and (piece.colour == "black"):
                            return "PAWN BACK ROW"
                        else:
                            return True
                    else:
                        return False
                else:
                    if new_position in self.pawn_possible_moves(piece):
                        if (piece.position[0] == 6) and (piece.colour == "white"):
                            return "PAWN BACK ROW TAKE"
                        if (piece.position[0] == 1) and (piece.colour == "black"):
                            return "PAWN BACK ROW TAKE"
                        else: 
                            return "TAKE"
                    else:
                        return False
            else:
                return False
            
    
    def move_piece_on_board(self, piece, new_position):
        if piece.colour != self.current_colour:
            print("Invalid move. " + str(self.current_colour) + " to move")
        valid = self.move_valid(piece, new_position)
        if piece.colour == self.current_colour:
            
            if self.move_is_valid_castle(piece,new_position) == True:
                piece.move1(new_position)
                self.show_board(self.return_opposite_colour(self.current_colour))
                self.current_colour = self.return_opposite_colour(self.current_colour)
                if piece.colour == "black":
                    self.black_king_can_castle_left = False
                    self.black_king_can_castle_right = False
                if piece.colour == "white":
                    self.white_king_can_castle_left = False
                    self.white_king_can_castle_right = False
                
            
            if valid == True:
                if self.move_still_in_check(piece, new_position) == False:
                    piece.move1(new_position)
                    self.show_board(self.return_opposite_colour(self.current_colour))
                    self.current_colour = self.return_opposite_colour(self.current_colour)
                    if piece.type == "king":
                        if piece.colour == "black":
                            self.black_king_can_castle_left = False
                            self.black_king_can_castle_right = False
                        if piece.colour == "white":
                            self.white_king_can_castle_left = False
                            self.white_king_can_castle_right = False
                    if piece.name == "r1w":
                        self.white_king_can_castle_left = False
                    if piece.name == "r2w":
                        self.white_king_can_castle_right = False
                    if piece.name == "r2b":
                        self.black_king_can_castle_left = False
                    if piece.name == "r1b":
                        self.black_king_can_castle_right = False
                        
                else:
                    print("Invalid move. King is in check")
            if valid == False:
                if self.move_still_in_check(piece, new_position) == False:
                    print(f"Invalid move. {piece.name} cannot move to [{new_position[0]}, {new_position[1]}]")
                else:
                    print("Invalid move. King is in check")
            if valid == "TAKE":
                if self.move_still_in_check(piece, new_position) == False:
                    x = self.find_piece_on_board(new_position)
                    x.move1(None)
                    self.pieces.remove(x)
                    self.pieces_taken.append(x)
                    piece.move1(new_position)
                    print(f"{x.name} taken by {piece.name}")
                    print(" ")
                    self.show_board(self.return_opposite_colour(self.current_colour))
                    self.current_colour = self.return_opposite_colour(self.current_colour)
                    if piece.type == "king":
                        if piece.colour == "black":
                            self.black_king_can_castle_left = False
                            self.black_king_can_castle_right = False
                        if piece.colour == "white":
                            self.white_king_can_colour_left = False
                            self.white_king_can_castle_right = False
                    if piece.name == "r1w":
                        self.white_king_can_castle_left = False
                    if piece.name == "r2w":
                        self.white_king_can_castle_right = False
                    if piece.name == "r2b":
                        self.black_king_can_castle_left = False
                    if piece.name == "r1b":
                        self.black_king_can_castle_right = False
                else:
                    print("Invalid move. King is in check")
            if valid == "PAWN BACK ROW":
                if self.move_still_in_check(piece, new_position) == False:
                    piece.move1(None)
                    self.pieces.remove(piece)
                    self.pieces.append(Piece(new_position, piece.colour, "queen", "qw2"))
                    self.show_board(self.return_opposite_colour(self.current_colour))
                    self.current_colour = self.return_opposite_colour(self.current_colour)
                else:
                    print("Invalid move. King is in check")
            elif valid == "PAWN BACK ROW TAKE":
                if self.move_still_in_check(piece, new_position) == False:
                    x = self.find_piece_on_board(new_position)
                    x.move1(None)
                    self.pieces.remove(x)
                    self.pieces_taken.append(x)
                    piece.move1(None)
                    self.pieces.remove(piece)
                    self.pieces.append(Piece(new_position, piece.colour, "queen", "qw2"))
                    self.show_board(self.return_opposite_colour(self.current_colour))
                    self.current_colour = self.return_opposite_colour(self.current_colour)
                else:
                    print("Invalid move. King is in check")
                    
        if self.checkmate(piece) == False:
            print(str(self.current_colour) + " to move")
            print("what is your move?")
            print(" ")
            
        if self.checkmate(piece) == True:
            print("checkmate. " + str(piece.colour) + " wins.")
            
        
    def move_piece(self, name, new_position):
        self.move_piece_on_board(self.find_piece_by_name(name), new_position)
                
            
    def find_piece_on_board(self, location):
        if (0 <= location[0] <= 7) and (0 <= location[1] <= 7):
            for piece in self.pieces:
                if piece.position[0] == location[0] and piece.position[1] == location[1]:
                    return piece
        return None
    
    
    def initialise_board(self):
        
        self.current_colour = "white"
        
        kw = Piece([0,4], "white", "king", "Kw ")
        qw = Piece([0,3], "white", "queen", "qw ")
        b1w = Piece([0,2], "white", "bishop", "b1w")
        k1w = Piece([0,1], "white", "knight", "k1w")
        r1w = Piece([0,0], "white", "rook", "r1w")
        b2w = Piece([0,5], "white", "bishop", "b2w")
        k2w = Piece([0,6], "white", "knight", "k2w")
        r2w = Piece([0,7], "white", "rook", "r2w")
        p1w = Piece([1,0], "white", "pawn", "p1w")
        p2w = Piece([1,1], "white", "pawn", "p2w")
        p3w = Piece([1,2], "white", "pawn", "p3w")
        p4w = Piece([1,3], "white", "pawn", "p4w")
        p5w = Piece([1,4], "white", "pawn", "p5w")
        p6w = Piece([1,5], "white", "pawn", "p6w")
        p7w = Piece([1,6], "white", "pawn", "p7w")
        p8w = Piece([1,7], "white", "pawn", "p8w")
        
        self.add_piece(kw)
        self.add_piece(qw)
        self.add_piece(b1w)
        self.add_piece(k1w)
        self.add_piece(r1w)
        self.add_piece(b2w)
        self.add_piece(k2w)
        self.add_piece(r2w)
        self.add_piece(p1w)
        self.add_piece(p2w)
        self.add_piece(p3w)
        self.add_piece(p4w)
        self.add_piece(p5w)
        self.add_piece(p6w)
        self.add_piece(p7w)
        self.add_piece(p8w)
        
        kb = Piece([7,4], "black", "king", "Kb ")
        qb = Piece([7,3], "black", "queen", "qb ")
        b1b = Piece([7,2], "black", "bishop", "b1b")
        k1b = Piece([7,1], "black", "knight", "k1b")
        r1b = Piece([7,0], "black", "rook", "r1b")
        b2b = Piece([7,5], "black", "bishop", "b2b")
        k2b = Piece([7,6], "black", "knight", "k2b")
        r2b = Piece([7,7], "black", "rook", "r2b")
        p1b = Piece([6,0], "black", "pawn", "p1b")
        p2b = Piece([6,1], "black", "pawn", "p2b")
        p3b = Piece([6,2], "black", "pawn", "p3b")
        p4b = Piece([6,3], "black", "pawn", "p4b")
        p5b = Piece([6,4], "black", "pawn", "p5b")
        p6b = Piece([6,5], "black", "pawn", "p6b")
        p7b = Piece([6,6], "black", "pawn", "p7b")
        p8b = Piece([6,7], "black", "pawn", "p8b")
        
        self.add_piece(kb)
        self.add_piece(qb)
        self.add_piece(b1b)
        self.add_piece(k1b)
        self.add_piece(r1b)
        self.add_piece(b2b)
        self.add_piece(k2b)
        self.add_piece(r2b)
        self.add_piece(p1b)
        self.add_piece(p2b)
        self.add_piece(p3b)
        self.add_piece(p4b)
        self.add_piece(p5b)
        self.add_piece(p6b)
        self.add_piece(p7b)
        self.add_piece(p8b)
        
        self.show_board("white")
        print("white to start")
        return(self.pieces)
    
    
    def find_piece_by_name(self, name):
        for i in self.pieces:
            if i.name == name:
                return i
            
            
    def pawn_possible_moves(self, piece):
        l = []
        p = piece.position
        if piece.colour == "white":
            if self.find_piece_on_board([p[0] + 1, p[1]]) == None:
                l.append([p[0] + 1, p[1]])
            if p[0] == 1 and self.find_piece_on_board([p[0] + 1, p[1]]) == None and self.find_piece_on_board([p[0] + 2, p[1]]) == None:
                l.append([p[0] + 2, p[1]])
            if self.find_piece_on_board([p[0] + 1, p[1] - 1]) != None and self.find_piece_on_board([p[0] + 1, p[1] - 1]).colour == "black":
                l.append([p[0] + 1, p[1] - 1])
            if self.find_piece_on_board([p[0] + 1, p[1] + 1]) != None and self.find_piece_on_board([p[0] + 1, p[1] + 1]).colour == "black":
                l.append([p[0] + 1, p[1] + 1])
        if piece.colour == "black":
            if self.find_piece_on_board([p[0] - 1, p[1]]) == None:
                l.append([p[0] - 1, p[1]])
            if p[0] == 6 and self.find_piece_on_board([p[0] - 1, p[1]]) == None and self.find_piece_on_board([p[0] - 2, p[1]]) == None:
                l.append([p[0] - 2, p[1]])
            if self.find_piece_on_board([p[0] - 1, p[1] - 1]) != None and self.find_piece_on_board([p[0] - 1, p[1] - 1]).colour == "white":
                l.append([p[0] - 1, p[1] - 1])
            if self.find_piece_on_board([p[0] - 1, p[1] + 1]) != None and self.find_piece_on_board([p[0] - 1, p[1] + 1]).colour == "white":
                l.append([p[0] - 1, p[1] + 1])
        return l
    
    
    def start_game(self):
        self.initialise_board()
        print("what is your move?")
        print(" ")
        
    
    def move(self, name, position):
        self.move_piece(name, position)
        
            
    def in_check(self):
        for piece in self.pieces:
            if piece.colour == "white":
                if self.move_valid(piece, self.find_piece_by_name("Kb ").position) != False:
                    return True
            if piece.colour == "black":
                if self.move_valid(piece, self.find_piece_by_name("Kw ").position) != False:
                    return True
        return False
            
            
    def move_still_in_check(self, piece, new_position):
        if self.in_check() == True:
            old_position = piece.position
            piece.move1(new_position)
            if self.in_check() == True:
                piece.move1(old_position)
                return True
            else:
                piece.move1(old_position)
                return False
        else:
            return False
        
        
    def return_pieces_by_colour(self, colour):
        list = []
        for piece in self.pieces:
            if piece.colour == colour:
                list.append(piece)
        return list
    
    def return_piece_by_colour_and_type(self, colour, type):
        for piece in self.pieces:
            if piece.colour == colour:
                if piece.type == type:
                    return piece
    
        
    def checkmate(self, piece):
        if self.in_check() == True:
            for p in self.return_pieces_by_colour(self.return_opposite_colour(piece.colour)):
                for move in p.possible_moves():
                    if (self.move_valid(p, move) != False) and (self.move_still_in_check(p, move)) == False:
                        return False
            else:
                return True
        else:
            return False
        
    def return_opposite_colour(self, colour):
        if colour == "white":
            return "black"
        else:
            return "white"
        
    def move_is_valid_castle(self,piece,new_position):
        if piece.type == "king":
            if piece.colour == "white":
                if self.white_king_can_castle_left == True:
                    if new_position == [0,2]:
                        for piece in self.pieces:
                            p = piece.position
                            if p == [0,1] or p == [0,2] or p == [0,3]:
                                return False
                        else:
                            if self.in_check() == False:
                                return True
                    else:
                        return False
                if self.white_king_can_castle_right == True:
                    if new_position == [0,6]:
                        for piece in self.pieces:
                            p = piece.position
                            if p == [0,5] or p == [0,6]:
                                return False
                        else:
                            if self.in_check() == False:
                                return True
                    else:
                        return False
                    
            if piece.colour == "black":
                if self.black_king_can_castle_left == True:
                    if new_position == [7,6]:
                        for piece in self.pieces:
                            p = piece.position
                            if p == [7,6] or p == [7,5]:
                                return False
                        else:
                            if self.in_check() == False:
                                return True
                    else:
                        return False
                if self.black_king_can_castle_right == True:
                    if new_position == [7,2]:
                        for piece in self.pieces:
                            p = piece.position
                            if p == [7,3] or p == [7,2] or p == [7,1]:
                                return False
                        else:
                            if self.in_check() == False:
                                return True
                    else:
                        return False
        else:
            return False
                        
            
            
        
            
    
            
class Piece:
    
    def __init__(self, position, colour, type, name):
        self.position = position
        self.colour = colour
        self.type = type
        self.name = name
        
    
    def move1(self, new_position):
        self.position = new_position
        
            
    def possible_moves(self):
        dict_moves = {}
        dict_moves["pawn"] = [[1,0],[-1,0]]
        dict_moves["rook"] = [[i,0] for i in range(8)] + [[0,i] for i in range(8)]
        dict_moves["knight"] = [[1,2], [-1,2], [2,1], [-2,1], [1,-2], [-1,-2], [2,-1], [-2,-1]]
        dict_moves["bishop"] = [[i,i] for i in range(-8, 8)] + [[-i,i] for i in range(-8 ,8)]
        dict_moves["queen"] = [[i,0] for i in range(-8, 8)] + [[0,i] for i in range(-8, 8)] + [[i,i] for i in range(-8, 8)] + [[-i,i] for i in range(-8, 8)]
        dict_moves["king"] = [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]
        
        list_of_legit_moves = []
        for i in dict_moves[self.type]:
            x = i[1]
            y = i[0]
            if 0 <= self.position[0] + y <= 7:
                if 0 <= self.position[1] + x <= 7:
                    list_of_legit_moves.append([self.position[0] + y, self.position[1] + x])
        return list_of_legit_moves
    
    
    def piece_in_the_way(self, new_position):
        spaces_in_between = []
        x = self.type
        y = self.position
        if x != "knight" and x != "king" and x != "pawn":
            if new_position[0] - y[0] > 1 or new_position[1] - y[1] > 1:
                if abs(new_position[0] - y[0]) == abs(new_position[1] - y[1]) > 1:
                    for i in range(y[0] + 1, new_position[0] - y[0]):
                        spaces_in_between.append([y[0] + i, y[1] + i])
                if new_position[0] - y[0] == 0:
                    for i in range(y[1] + 1, new_position[1] - y[1]):
                        spaces_in_between.append([y[0], y[1] + i])
                if new_position[1] - y[1] == 0:
                    for i in range(y[0] + 1, new_position[0] - y[0]):
                        spaces_in_between.append([y[0] + i, y[1]])
        return spaces_in_between
        
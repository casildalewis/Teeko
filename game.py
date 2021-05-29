import random
import time
import copy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    drop_phase_check = 0

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        self.drop_phase_check += 2
        if self.my_piece == 'b' and self.drop_phase_check == 2:
            self.drop_phase_check -= 1

        successors = self.succ(state, self.my_piece)
        best_move, best_successor = successors[0]

        for move, successor in successors:
            if self.min_value(successor, 2, -1000, 1000) > self.min_value(best_successor, 2, -1000, 1000):
                best_move = move
                best_successor = successor

        return best_move

    def succ(self, state, turn_piece):
        """Takes in a board state and returns a list of the legal successors. 
        
        During the drop phase, this simply means adding a new piece of the current player's type to 
        the board; during continued gameplay, this means moving any one of the current player's 
        pieces to an unoccupied location on the board, adjacent to that piece.

        Note: wrapping around the edge is NOT allowed when determining "adjacent" positions.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object.
            turn_piece ('r' or 'b'): whose turn it is

        return: 
            successors (list of lists): each list contains a move list (as described in make_move) and a successor state
        """
        successors = []

        if self.drop_phase_check < 9:
            
            for row in range (5):
                for col in range (5):

                    if state[row][col] == ' ':
                        new_state = copy.deepcopy(state)
                        new_state[row][col] = turn_piece
                        successors.append([[(row, col)], new_state])

            return successors

        else:
            for row in range (5):
                for col in range (5):

                    if state[row][col] == turn_piece:

                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if (i != 0 or j != 0) and (row+i in range(5)) and (col+j in range(5)) and state[row+i][col+j] == ' ':
                                    new_state = copy.deepcopy(state)
                                    new_state[row+i][col+j] = turn_piece
                                    new_state[row][col] = ' '
                                    successors.append([[(row+i, col+j), (row, col)], new_state])

            return successors

    def max_value(self, state, depth, alpha, beta):
        """Your first call will be  max_value(self, curr_state, 0) and every subsequent recursive 
        call will increase the value of depth.

        When the depth counter reaches your tested depth limit OR you find a terminal state, 
        terminate the recursion.

        Args:
            state (list of lists): current state in game, ai about to play
            depth: an upper bound on search depth
            alpha: best score (highest) for Max along path to state
            beta: best score (lowest) for Min along path to state
        
        return: min(beta, best-score (for Max) available from state)
        """
        terminal_val = self.game_value(state)
        if(terminal_val != 0):
            return terminal_val

        elif depth == 0:
            return self.heuristic_game_value(state)

        else:
            successors = self.succ(state, self.my_piece)
            for move, successor in successors:
                alpha = max(alpha, self.min_value(successor, depth-1, alpha, beta))
                if alpha>=beta:
                    return beta
        
        return alpha

    def min_value(self, state, depth, alpha, beta):
        """
        Args:
            state (list of lists): current state in game, opponent about to play
            depth: an upper bound on search depth
            alpha: best score (highest) for Max along path to state
            beta: best score (lowest) for Min along path to state

        return: max(α , best-score (for Min) available from state)
        """
        terminal_val = self.game_value(state)
        if(terminal_val != 0):
            return terminal_val
        
        elif depth == 0:
            return self.heuristic_game_value(state)

        else:
            successors = self.succ(state, self.opp)
            for move, successor in successors:
                beta = min(beta, self.max_value(state, depth-1, alpha, beta))
                if alpha>=beta:
                    return alpha

        return beta

    def heuristic_game_value(self, state):
        """Evaluates non-terminal states. 

        (You should call the game_value method from this function to determine whether the state is a terminal 
        state before you start evaluating it heuristically.) 

        This function should return some floating-point value between 1 and -1.

        TODO: this a very stupid strategy to test all other functions <3

        Let weights be :
        c, c, c, c, c
        c, b, b, b, c
        c, b, a, b, c
        c, b, b, b, c
        c, c, c, c, c

        where, depending on whose piece is in the spot,
        c = 0.05 or -0.05
        b = 0.1 or -0.1
        a = 0.2 or -0.2

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object.
        """
        heuristic_val = 0

        if self.drop_phase_check<3:
            a = 0.05
            b = 0.1
            c = 0.2
            weight = [[c, c, c, c, c],
            [c, b, b, b, c],
            [c, b, a, b, c],
            [c, b, b, b, c],
            [c, c, c, c, c]
            ]

            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        heuristic_val += weight[row][col]
                    elif state[row][col] == self.opp:
                        heuristic_val -= weight[row][col]

        return heuristic_val

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range (2):
            for col in range (2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
        
        # check / diagonal wins
        for row in range (2):
            for col in range (2):
                if state[row][4-col] != ' ' and state[row][4-col] == state[row+1][3-col] == state[row+2][2-col] == state[row+3][1-col]:
                    return 1 if state[row][4-col]==self.my_piece else -1

        # check 3x3 square corners wins
        for row in range (3):
            for col in range (3):
                if state[row][col] != ' ' and state[row+1][col+1] == ' ' and state[row][col] == state[row][col+2] == state[row+2][col] == state[row+2][col+2]:
                    return 1 if state[row][col]==self.my_piece else -1


        return 0 # no winner yet


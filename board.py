from extraClasses import LimitedList

class Board:
    """
    A class that stores the information and functions for the game board. 

    Parameters
    ----------

    piecesPerHole: int, optional 
        Number of starting pieces in each of the positions on the board, default 4

    rowLength: int, optional 
        Number of positions in each row, default 6

    """

    def __init__(self, piecesPerHole=4, rowLength=6):
        self.piecesPerHole = piecesPerHole #number of starting pieces in each position on board 
        self.rowLength = rowLength #number of holes/positions per row 

        #calculate positions of goals (indicies)
        self.player1Goal = 0 
        self.player2Goal = self.rowLength + 1 

        self.numberOfPositions = self.rowLength * 2 + 2 #the total number of positions on the board is going to be the number of positions per row times 2 and then two goals 

        #generate lists of all indices of positions on player 1 and player 2 sides of the board
        self.player1Pos = [i for i in range(self.player1Goal+1, self.player2Goal)]
        self.player2Pos = [i for i in range(self.player2Goal+1, self.numberOfPositions)]

        #code to generate board list 
        self.board = LimitedList(self.numberOfPositions) #create list to represent the board 
        
        self.board[self.player1Goal, self.player2Goal] = 0 #set both goals to empty 
        for index in self.player1Pos: #look through all indices in board between the first and second goal, set all of them to the correct number of initial pieces
            self.board[index] = self.piecesPerHole
        for index in self.player2Pos: #do the same, however between second goal and end of board 
            self.board[index] = self.piecesPerHole 
    
    def __repr__(self):
        return repr(self.board) #when handling printing this class, simply handle same as printing list that represents board

    def player1Side(self):
        """
        Returns only player 1's side of the board. 

        Returns 
        -------

        player1Board: list 
            List containing all the piece values for all the slots on player 1's side of the board and player 1's goal 

        """

        return (self.board[:self.player2Goal])
    
    def player2Side(self):
        """
        Returns only player 2's side of the board. 

        Returns
        -------

        player2Board: list 
            List containing all the piece values for all the slots of player 2's side of the board and player 2's goal

        """

        return(self.board[self.player2Goal:])

        

gameBoard = Board()
print(gameBoard)
print(gameBoard.player2Side())

from extraClasses import LimitedList

class Board:
    def __init__(self, piecesPerHole=4, rowLength=6):
        self.piecesPerHole = piecesPerHole #number of starting pieces in each position on board 
        self.rowLength = rowLength #number of holes/positions per row 

        #calculate positions of goals (indicies)
        self.player1Goal = 0 
        self.player2Goal = self.rowLength + 1 

        #code to generate board list 
        numberOfPositions = self.rowLength * 2 + 2 #the total number of positions on the board is going to be the number of positions per row times 2 and then two goals 
        self.board = LimitedList(numberOfPositions) #create list to represent the board 
        
        self.board[self.player1Goal, self.player2Goal] = 0 #set both goals to empty 
        for index in [i for i in range(self.player1Goal+1,self.player2Goal)]: #look through all indices in board between the first and second goal, set all of them to the correct number of initial pieces
            self.board[index] = self.piecesPerHole
        for index in [i for i in range(self.player2Goal+1,numberOfPositions)]: #do the same, however between second goal and end of board 
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

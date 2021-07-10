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
        self.player1Positions = [i for i in range(self.player1Goal+1, self.player2Goal)]
        self.player2Positions = [i for i in range(self.player2Goal+1, self.numberOfPositions)]

        #code to generate board list 
        self.board = LimitedList(self.numberOfPositions) #create list to represent the board 
        
        self.board[self.player1Goal, self.player2Goal] = 0 #set both goals to empty 
        for index in self.player1Positions: #look through all indices in board between the first and second goal, set all of them to the correct number of initial pieces
            self.board[index] = self.piecesPerHole
        for index in self.player2Positions: #do the same, however between second goal and end of board 
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

    def move(self, position, playerMoving, followUpMove=False):
        """
        Function that moves from a specific position on the board. This will deposit 1 "stone" from position moving from 
        into each following position (each position after will decline the number of stones by 1, the number of stones is 
        the current value of the position). This will loop through the entire "move" (as if you land in another position with 
        more stones, you will continue uses those stones). Upon landing in a goal, meaning the player could select a new 
        position to move from, the function will return True signaling this is the case. Otherwise it returns False. This 
        will error if player is unable to play from selected position. 

        Parameters 
        ----------

        position: int 
            Position move starts from. Must be a valid move. 
        
        playerMoving: int, 1 or 2 
            Signals which player is moving. 1 signifies player 1, 2 signifies player 2.

        followUpMove: bool, optional 
            True if being used recursively, ie player already moved on this move and this is the movement for the position they landed on. False otherwise. If True, this disables player correct position checks.

        Returns 
        -------

        continueMove: bool 
            True if player can pick new location to move from.
            False is move is finished

        """

        if position >= 0 and position <= self.numberOfPositions-1: #check to make sure selected position is at least in range of board
            if not followUpMove: #disable these checks if not first position in move
                #check if move is valid for specified player that is moving, if not raise exception
                if playerMoving == 1 and position not in self.player1Positions: 
                    raise self.InvalidMove(position, "move not valid for player 1") 
                if playerMoving == 2 and position not in self.player2Positions:
                    raise self.InvalidMove(position, "move not valid for player 2")
            else: #even if recursive use, still check to make sure program isn't trying to move from goal
                if position not in self.player1Positions and position not in self.player2Positions:
                    raise self.InvalidMove(position, "move either off board or one of the goals")

            numberFromPosition = self.board[position] #find the number of stones in position moving from
            self.board[position] = 0 #empty position moving from 

            self.board.seek_position(position) #start step by step iteration at moving position
            for x in range(numberFromPosition): #go backwards to each position behind adding 1 stone to each 
                currentNextPosValue = self.board.next()

                #ignore goal of opponent if looping over goal
                if playerMoving == 1 and self.board.iterationLocation() != self.player2Goal:
                    self.board.current(setValue=currentNextPosValue+1)
                elif playerMoving == 2 and self.board.iterationLocation() != self.player1Goal:
                    self.board.current(setValue=currentNextPosValue+1)
                else: #if landing on opponent goal, skip it and add to the following position (this breaks if row length is 0, however you don't have a game then anyway...)
                    currentNextPosValue = self.board.next()
                    self.board.current(setValue=currentNextPosValue+1)
            
            if self.board.iterationLocation() != self.player1Goal and self.board.iterationLocation() != self.player2Goal and self.board.current() >= 2: #if the position landed in isn't a goal and previously had at least 1 stone in it, then run a move from there
                self.move(self.board.iterationLocation(), playerMoving, followUpMove=True)
            elif self.board.iterationLocation() == self.player1Goal or self.board.iterationLocation() == self.player2Goal: #if player ended in goal (assuming correct player goal due to other safeties), return True
                return True 
            else: #if not in goal, return false
                return False


        else:
            raise self.InvalidMove(position, "position is not on board")

    #Defining Exceptions 
    class InvalidMove(Exception):
        """
        Exception raised if specified move is invalid. This can either be that it is out of range of the board, not on the moving player's side, or one of the two goals. 

        """

        def __init__(self, movePosition, reason, message="Moving from {} is invalid because: {}."):
            self.movePosition = movePosition
            self.reason = reason 
            self.message = message.format(self.movePosition, self.reason)
            super().__init__(self.message)


gameBoard = Board()
print(gameBoard)
print(gameBoard.player2Side())
gameBoard.move(3,1)

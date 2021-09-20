import random

class TicTacToe():
  '''
  Tic Tac Toe game
  '''

  def __init__(self):
    self.choices = ['x','o']
    self.players = []

  def setup(self):
    '''
    setup up the board, player and turn
    '''
    self.initBoard()
    self.initPlayers()
    self.setTurn() 
    self.play = True 

  def setTurn(self):
    '''
    decide which player would start first
    '''
    self.playerFirst = random.randint(0, 1) == 0

    if self.playerFirst:
      print('Player first')
    else:
      print('Computer First')

  def initPlayers(self):
    '''
    let the user chooses a symbol (x/o)
    '''
    symbol = None

    while symbol not in self.choices:
      symbol = input('Please choose x or o:  ')
  
    self.players.append(Human(symbol))

    computerSymbol = [i for i in self.choices if i != symbol][0] #assign the unchosen symbol to computer

    self.players.append(Computer(computerSymbol)) #add computer to players list

  def initBoard(self):
    '''
    create a n x n size board
    '''
    n = None
    while n is None:
      try:
        n = int(input('please enter an integer for board size:  '))
      except:
        print('please enter an integer')

    self.board = Board(n)
    self.moveCount = 0 


  def restart(self):
    '''
    setup the game again if user choose y else stop the while loop
    '''
    inp = input('Do you want to play again [y/n] ')

    if inp == 'y':
      self.setup()

    else:
      self.play = False
      print('thank for playing')


  def main(self):
    '''
    start a terminal app that take user's input to 
    play tic tac toe against computer
    '''
    self.setup()

    if self.playerFirst:
      playerIdx = 0
    else:
      playerIdx = 1

    player = self.players[playerIdx] #set the player who will start first

    

    while self.play:
      self.board.showBoard()  #show the board
      pos = player.makeMove(self.board)  #player makes a move
      self.board.placeMove(pos,player.symbol) #update the move
      self.moveCount +=1                      #update move count

      if self.board.checkWin(pos,player.symbol): #check wining condition
        print(player.name +' wins!')
        self.board.showBoard()
        self.restart() 

      elif self.moveCount == self.board.totalmove: #check if draw 
        print('draw!!')
        self.board.showBoard()
        self.restart() 

      #switch player 
      else:
        playerIdx = (playerIdx+1) % len(self.players) 
        player = self.players[playerIdx]



class Board():
  '''
  game board for Tic Tae Toe
  '''

  def __init__(self, boardSize:int):
    self.board = {}
    self.boardSize = boardSize
    self.totalmove = self.boardSize *  self.boardSize
    self.createBoard()
  
  def createBoard(self):
      '''
      create an empty board
      '''
      self.board = [['-' for i in range(self.boardSize) ] for row in range(self.boardSize)]


  def showBoard(self):
    '''
    print the board with coordinate with respect to each position
    '''
    print('    '+'   '.join([str(i) for i in range(self.boardSize)] )+'  ')
    for row in range(self.boardSize):
      elem = [self.board[row][col] for col in range(self.boardSize)]
      print(str(row) + ' | ' + ' | '.join(elem) + ' |')

  def isValidMove(self, pos: list) ->bool:
    '''
    check if the move is valid
    '''
    row = pos[0]
    col = pos[1]
    return  row < self.boardSize and col < self.boardSize and  self.board[row][col] == '-' 


  def placeMove(self, pos: list, symbol: str):
    '''
    update the board after player makes a move
    '''
    row = pos[0]
    col = pos[1]
  
    self.board[row][col] = symbol

  def checkWin(self, pos: list, symbol: str) ->bool:
    '''
    check winning condition

    Winning move only happens at x or o's most recent move, 
    so we check row, col and optional diagonal after someone places the move.
    Thus, reduce the number of computations needed
    '''
    #check column
    rowIdx = pos[0]

    for col in range(self.boardSize):
      if self.board[rowIdx][col] != symbol:
        break 
      if col == self.boardSize - 1:
        return True 

    #check row 
    colIdx = pos[1]

    for row in range(self.boardSize):
      if self.board[row][colIdx] != symbol:
        break 
      if row == self.boardSize - 1:
        return True 

    #check diagonal
    if rowIdx == colIdx:
      for i in range(self.boardSize):
        if self.board[i][i] != symbol:
          break 
        if i == self.boardSize - 1:
          return True 

    #check off-diagonal
    if rowIdx + colIdx == self.boardSize - 1 :
      for i in range(self.boardSize):
        if self.board[i][(self.boardSize-1)-i] != symbol:
          break 
        if i == self.boardSize - 1:
          return True 

    return False  


class Player():
  '''
  abstract class for tic tac toe player
  '''
  def __init__(self, symbol: str, name=None):
    self.symbol = symbol
    self.name = name

  def makeMove(self, board):
    pass

class Human(Player):
  '''
  human player that makes move by input row and column number
  '''
  def __init__(self,symbol:str):
    super().__init__(symbol,'player')

  def makeMove(self, board) ->list :
    valid = False
    while not valid:
      try:
        row = int(input('Please enter a row number:  '))
        col = int(input('Please enter a column number: '))
        valid  = board.isValidMove([row,col])
      except:
        print('The input must be integer')
    

    return [row,col]

class Computer(Player):
  '''
  bot that makes a move randomly
  '''
  def __init__(self,symbol:str):
    super().__init__(symbol,'Computer')

  def makeMove(self, board) ->list :
    valid = False
    while not valid:
      row = random.choice([i for i in range(board.boardSize)])
      col = random.choice([i for i in range(board.boardSize)])
      valid  = board.isValidMove([row,col])

    print('Computer make a move')

    return [row,col]







if __name__ == "__main__":
    game = TicTacToe()
    game.main( )
#PT Prigoda and Charlie Williams
#Final Project Dots and Boxes
#Due Date 12/22/15
#This program is the game dots and boxes displayed in a GUI. This is a two
#player game. The program will prompt to user to enter two colors they would
#like to play as. Once the user clicks submit, then a game board will appear,
#showing the score with a quit button. The users then could play dots and
#boxes, and once the board is filled up the program will announce the winner
#at the bottom of the screen.

from grid import *

def main():
    #sets up graphics window
    win = GraphWin("Dots and Boxes", 600, 600)
    #sets the coords so that grid can fit on screen
    win.setCoords(-3, 9, 9, -3)

    #welcome text
    welcome = Text(Point(3,-2),"Welcome to PT and Charlie's\nDots and Boxes Game!")
    welcome.setSize(30)
    welcome.draw(win)

    #directions
    directions = Text(Point(3,0),"This program is the game dots and boxes displayed in a GUI.\n"
                                  " This is a two player game in which both players create lines on a grid.\n"
                                  " By creating a box, you score one point, and whoever\n"
                                  " has the most boxes created by the end, wins!")
    directions.draw(win)
    
    #player 1 enter color text
    enterColor1 = Text(Point(3,1.5),"Player 1 enter a color")
    enterColor1.draw(win)

    #player 2 enter color text
    enterColor2 = Text(Point(3,3.5),"Player 2 enter a color")
    enterColor2.draw(win)

    #player 1 input box
    player1input = Entry(Point(3,2),20)
    player1input.draw(win)

    #player 2 input box
    player2input = Entry(Point(3,4),20)
    player2input.draw(win)

    #submit colors button
    submit = ActualButton(win,Point(3,6),2,1,"Submit")

    #waits for user click
    pt = win.getMouse()

    #gets the text of both player
    one = player1input.getText()
    two = player2input.getText()

    #while loop while the submit button is not clicked
    while not submit.isClicked(pt):
        #get the text from the text box
        one = player1input.getText()
        two = player2input.getText()
        #waits for user click
        pt = win.getMouse()

    #opens up color dictionary, reads and puts it in lower case
    colorDict = open("colorDic.txt","r").read().lower()
    #splits the file by quotations and comas
    colorDict = colorDict.split("',  '")
    #default colors if user color is not in dictioary
    if one not in colorDict:
        one = "blue"
    if two not in colorDict:
        two = "red"

    #undraws all buttons and inputs on screen and draws game
    submit.undraw()
    enterColor1.undraw()
    enterColor2.undraw()
    player1input.undraw()
    player2input.undraw()
    directions.undraw()

    #player 1 score text
    player1 = Text(Point(-2,7), "Player 1: ")
    player1.setSize(18)
    player1.draw(win)

    #player 1s total text
    total1 = Text(Point(-1,7),"0")
    total1.setSize(18)
    total1.draw(win)

    #player 2 score text
    total2 = Text(Point(-1,8),"0")
    total2.setSize(18)
    total2.draw(win)

    #player 2 total text
    player2 = Text(Point(-2,8), "Player 2: ")
    player2.setSize(18)
    player2.draw(win)

    #list of players scores
    players = [total1,total2]

    #quit button to quit game anytime
    quitButton = ActualButton(win,Point(8,8),2,1,"Quit")

    #sets up game grid
    grid = Grid(win,0,0,7,7,1,1)

    #list of the two user colors
    colors = [one,two]
    #accumulator variable
    color = 0

    #not a button text if clicked outside grid
    wrong = Text(Point(3,7),"")
    wrong.setSize(18)
    wrong.draw(win)

    #winner text once grid is filled up
    winner = Text(Point(3,8),"")
    winner.setSize(20)
    winner.setFill("green4")
    winner.draw(win)

    #line that underlines player 1 turn in the user color
    underline = Line(Point(-1,7.25),Point(-3,7.25))
    underline.setFill(one)
    underline.draw(win)

    #line that underlines player 2 turn in the user color
    underline1 = Line(Point(-1,8.25),Point(-3,8.25))
    underline1.setFill("white")
    underline1.draw(win)

    #list of both underlines to keep track of turn
    underlines = [underline, underline1]

    #accumulator variables for each players points
    p1total = 0
    p2total = 0
    #list of both scores starting at 0
    scores = [0,0]

    #wait for user click
    pt = win.getMouse()

    #while loop while the quit button is not clicked
    while not quitButton.isClicked(pt):
        #display not button text if button is not clicked
        wrong.setText("")
        #if first click is inside grid
        if -.5 <= pt.getX() <= 6.5 and -.5 <= pt.getY() <= 6.5:
            #get the position of click
            row,column = grid.getClickPos(pt)
            #set the square color to black when clicked
            grid.setSquareColor(column,row,"black")
            #wait for second click
            pt2 = win.getMouse()
            #if the secon click is inside the grid
            if -.5 <= pt2.getX() <= 6.5 and -.5 <= pt2.getY() <= 6.5:
                #draw a line between the two clicks
                drawn = grid.drawLine(pt,pt2,colors[color])
                #if the two buttons are not next to each other
                if drawn != False:
                    #draws the color of the box inbetween the lines connecting
                    numBoxs = grid.drawBox(drawn,colors[color])
                    #accumulating the scores
                    scores[color] += numBoxs
                    #changes the score once box is completed
                    players[color].setText(str(scores[color]))
                    #if it is player 1s turn
                    if numBoxs == 0:
                        #player 2s undline is white
                        underlines[color].setFill("white")
                        #when the turn switches, make player 1s underline white
                        color = (color + 1)%2
                        #make the underline the user color
                        underlines[color].setFill(colors[color])
            #if the highest amount of boxes are made
            if scores[0] + scores[1] == 36:
                #if player 1s score is higher
                if scores[0] > scores[1]:
                    #display player 1 wins
                    winner.setText("Player 1 Wins!")
                #or if player 2s score is higher
                elif scores[0] < scores[1]:
                    #display player 2 wins
                    winner.setText("Player 2 Wins!")
                #otherwise, display its a tie
                elif scores[0] == scores[1]:
                    winner.setText("It's a Tie!")
        #otherwise, not a button
        else:
            wrong.setText("Not a Button")
        #wait for user click
        pt = win.getMouse() 
    #closes window if quit button is clicked
    win.close()
    
if __name__ == "__main__":
    main()

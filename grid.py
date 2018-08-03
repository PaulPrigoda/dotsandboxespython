# grid.py
from graphics import *
from math import *

class Button:

    """Creates a button but just shows the center so it
       looks like a dot to click. This class is just for
       the dots on the grid."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """ 

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('black')
        self.rect.setOutline('white')
        self.rect.draw(win)
        self.active = True
        self.center = center
        center.setFill('black')
        center.draw(win)

    def isClicked(self, p):
        "Returns true if button active and p is inside"
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.center.setFill('black')
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.center.setFill('darkgrey')
        self.active = False

    def setColor(self,color):
        self.center.setFill(color)

class ActualButton:
    
    """A button is a labeled rectangle in a window.
    It is enabled or disabled with the activate()
    and deactivate() methods. The clicked(pt) method
    returns true if the button is enabled and pt is inside it.
    This button class is for actual buttons."""
    
    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """
        #w and h are the width and the height 
        w,h = width/2.0, height/2.0
        #x and y are the coordinates
        x,y = center.getX(), center.getY()
        #creates top left point of rect
        self.xmax, self.xmin = x+w, x-w
        #creates top right point of rect
        self.ymax, self.ymin = y+h, y-h
        #stores first point
        p1 = Point(self.xmin, self.ymin)
        #stores second point
        p2 = Point(self.xmax, self.ymax)
        #creates rect
        self.rect = Rectangle(p1,p2)
        #color of rect
        self.rect.setFill('lightgray')
        #draws rect
        self.rect.draw(win)
        #puts text in button center
        self.label = Text(center, label)
        #draws text
        self.label.draw(win)
        #this line was not there in class today
        self.activate() 

    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()

    def activate(self):
        """Sets this button to 'active'."""
        #color the text "black"
        self.label.setFill('black')
        #set the outline to look bolder
        self.rect.setWidth(2)
        #set the boolean variable that tracks "active"-ness to True
        self.active = True

    def deactivate(self):
        """Sets this button to 'inactive'."""
        ##color the text "darkgray"
        self.label.setFill("darkgray")
        ##set the outline to look finer/thinner
        self.rect.setWidth(1)
        ##set the boolean variable that tracks "active"-ness to False
        self.active = False

    def isClicked(self, p):
        "Returns true if button active and p is inside"
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def undraw(self):
        "Undraws an object in the GUI."
        self.rect.undraw()
        self.label.undraw()
        
  
class Grid:
    """A grid of squares/buttons"""
    def __init__(self, win, startX, startY, numCols, numRows, squareWidth, squareHeight):
        """initializes a 2D list of blank button objects"""
        self.lines = []
        self.win = win
        #empty list of point
        self.buttonMatrix = []
        #number of columns
        self.numCols = numCols
        #number of rows
        self.numRows = numRows
        self.startX = startX
        self.startY = startY
        #looping through the rows and adding them to button row
        for y in range(startY,numRows):
            buttonRow = []
            #looping through columns and adding them to button
            for x in range(startX,numCols): 
                button = Button(win,Point(x,y),.25,.25,"")
                buttonRow.append(button)
            self.buttonMatrix.append(buttonRow)


    def getClickPos(self, clickPt):
        """returns the column and row number of the button that was clicked
           assumes the point clickPt is in/on the grid"""
        #gets the x value where user clicks
        x = round(clickPt.getX())
        #gets y value where user clicks
        y = round(clickPt.getY())
        #returns x and y
        return y,x

    def setSquareColor(self,x,y,color):
        """Set the color of a button at the given x,y"""
        #sets the color of a button on the grid at a user x and y point
        self.buttonMatrix[y][x].setColor(color)

    def setRowColor(self,rowNum,color):
        #loops through buttons in row and colors them a user color
        for i in range(20):
            self.buttonMatrix[rowNum][i].setColor(color)

    def setColColor(self,colNum,color):
        #loops through buttons in column and colors them a user color
        for i in range(20):
            self.buttonMatrix[i][colNum].setColor(color)

    def setNeighbors(self,midR,midC,color):
        #loops through the buttons surrounding the user clicked button and colors them
        for x in range(-1,2):
            for y in range(-1,2):
                if (-.5 <= midC+x <= 19.5) and (-.5 <= midR+y <= 19.5):
                    self.buttonMatrix[midR+y][midC+x].setColor(color)

    def nextTo(self,pt1,pt2):
        """Returns whether buttons that are clicked are
           next to each other or not"""
        #stores position of click of point 1
        y1,x1 = self.getClickPos(pt1)
        #stores position of click of point 2
        y2,x2 = self.getClickPos(pt2)
        #determains whether the addition of the values is 1 or 0, if one they are next to each other
        if abs(x1-x2) + abs(y1-y2) == 1:
            return True
        #else they are not next to each other
        else:
            return False

    def drawLine(self,pt1,pt2,color):
        """Draws line if two points are clicked inside
           the grid. Otherwise returns false"""
        #if user clicks anywhere on a button, it centers the click by roudning it
        point1 = Point(round(pt1.getX()),round(pt1.getY()))
        point2 = Point(round(pt2.getX()),round(pt2.getY()))
        #if two buttons are next to each other
        if self.nextTo(pt1,pt2) == True:
            #creates a line
            line = Line(point1, point2)
            if (line.getP1().getX(),line.getP1().getY(),line.getP2().getX(),line.getP2().getY()) not in self.lines:                  
                #colors the line the color of the player
                line.setFill(color)
                #draws the line
                line.draw(self.win)
                #appends the points to a list for the creation of a box, even if clicked oppisite ways they get counted the same
                self.lines.append((line.getP1().getX(),line.getP1().getY(),line.getP2().getX(),line.getP2().getY()))
                self.lines.append((line.getP2().getX(),line.getP2().getY(),line.getP1().getX(),line.getP1().getY()))
                return line
        #otherwise return false
        return False

    def vertical(self,line):
        """Checks the three lines to the right and left of
           a vertically drawn line to see if they have been
           drawn or not."""
        #gets the coordniates of point 1 and point 2
        p1 = line.getP1()
        p2 = line.getP2()
        #checks if lines surrounding newly formed vertical line are draw or not
        newLine = (p1.getX(),p1.getY(),p1.getX()+1,p1.getY())
        newLine2 = (p2.getX(),p2.getY(),p2.getX()+1,p2.getY())
        newLine3 = (p1.getX()+1,p1.getY(),p2.getX()+1,p2.getY())
        newLine4 = (p1.getX(),p1.getY(),p1.getX()-1,p1.getY())
        newLine5 = (p2.getX(),p2.getY(),p2.getX()-1,p2.getY())
        newLine6 = (p1.getX()-1,p1.getY(),p2.getX()-1,p2.getY())
        #if the new line isnt in the list and the surrounding lines to the right are not drawn
        if newLine not in self.lines or newLine2 not in self.lines or newLine3 not in self.lines:
            #then dont draw a box to the right of the vertical line
            rightBox = False
        #otherwise create a box within those four lines
        else:
            rightBox = Rectangle(p1, Point(p2.getX()+1,p2.getY()))
        #if the new line isnt in the list and the surrounding lines to the left are not drawn
        if newLine4 not in self.lines or newLine5 not in self.lines or newLine6 not in self.lines:
            #then dont draw a box to the left of the vertical line
            leftBox = False
        #otherwise draw a box to the left of the vertical line
        else:
            leftBox = Rectangle(p1, Point(p2.getX()-1,p2.getY()))
        #return where the boxes were drawn
        return rightBox,leftBox

    def horizontal(self,line):
        """Checks the three lines to the right and left of
           a horizontally drawn line to see if they have been
           drawn or not."""
        #gets the coordniates of point 1 and point 2
        p1 = line.getP1()
        p2 = line.getP2()
        #checks if lines surrounding newly formed horizontal line are draw or not
        newLine7 = (p1.getX(),p1.getY(),p1.getX(),p1.getY()+1)
        newLine8 = (p2.getX(),p2.getY(),p2.getX(),p2.getY()+1)
        newLine9 = (p1.getX(),p1.getY()+1,p2.getX(),p2.getY()+1)
        newLine10 = (p1.getX(),p1.getY(),p1.getX(),p1.getY()-1)
        newLine11 = (p2.getX(),p2.getY(),p2.getX(),p2.getY()-1)
        newLine12 = (p1.getX(),p1.getY()-1,p2.getX(),p2.getY()-1)
        #if the new line isnt in the list and the surrounding lines to the right are not drawn
        if newLine7 not in self.lines or newLine8 not in self.lines or newLine9 not in self.lines:
            #then dont draw a box to the right of the horizontal line
            rightBox = False
        #otherwise create a box within those four lines
        else:
            rightBox = Rectangle(p1, Point(p2.getX(),p2.getY()+1))
            #if the new line isnt in the list and the surrounding lines to the left are not drawn
        if newLine10 not in self.lines or newLine11 not in self.lines or newLine12 not in self.lines:
            #then dont draw a box to the left of the horizontal line
            leftBox = False
        #otherwise create a box within those four lines
        else:
            leftBox = Rectangle(p1, Point(p2.getX(),p2.getY()-1))
        #reutrns where boxes were drawn
        return rightBox,leftBox
            

    def drawBox(self,line,color):
        """Checks if the corrisponding lines are in the self.lines
           list to create a box, and if so then it draws a box between
           the lines."""
        #gets the coordinates of points 1 and 2
        p1 = line.getP1()
        p2 = line.getP2()
        #accumulator variable
        numBoxs = 0
        #if the coordinates of point1 == the coordinates of point2
        if p1.getX() == p2.getX():
            #create a line bewteen the points
            right,left = self.vertical(line)
            #if the right line is false
            if right != False:
                #make a line to the right with user color
                right.setFill(color)
                #draw the line
                right.draw(self.win)
                #accumulator variable
                numBoxs += 1
            #if theleft line it false
            if left != False:
                #create a line to the left with user color
                left.setFill(color)
                #draw the line
                left.draw(self.win)
                #accumulator variable
                numBoxs += 1
        #otherwise create a horizonatal line
        else:
            #left and right of horizontal line
            right,left = self.horizontal(line)
            #if the right line is false
            if right != False:
                #make a line to the right with user color
                right.setFill(color)
                #draw the line
                right.draw(self.win)
                #accumulator variable
                numBoxs += 1
            #if the left line is false
            if left != False:
                #make a line to the left with user color
                left.setFill(color)
                #draw the line
                left.draw(self.win)
                #accumulator variable
                numBoxs += 1
        #returns the variable numBoxs
        return numBoxs
     
        
            
            

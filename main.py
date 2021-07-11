import pygame, sys
from pygame.locals import *

class Game:
    """
    Class to handle game logic and game loop for pygame. This will contain 
    functions to deal with player input and displaying the game graphically. 

    """

    #define window dimensions 
    windowHeight = 1080 
    windowWidth = 1920

    def __init__(self):
        self._running = True 
        self._display = None

    def on_init(self):
        """
        Secondary init function specifically to initialize pygame and to create display. 
        This is run when calling self.on_execute() (which should be done on creation of 
        the class). 

        """

        pygame.init()
        self._display = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption("Mancala")
    
    def on_event(self, event):
        """
        Function for event handling, ie user inputs. Takes pygame "event" as parameter.  

        Parameters 
        ----------

        event: pygame event 
            From pygame.event.get(). 

        """

        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        """
        Function to run logic on game loop.

        """

        pass

    def on_render(self):
        """
        Function to handle rendering for each loop. 

        Citations
        ---------

            Found information on shape rendering in pygame from: http://www.pygame.org/docs/ref/draw.html

        """

        renderFont = pygame.font.SysFont('Times New Roman', 20)
        self._display.fill((255,255,255))
        self._display.blit(renderFont.render("POGCHAMP", True, (0,0,0)), (20, 20))

        
        pygame.draw.rect(self._display, (255, 0, 0), pygame.Rect(30, 30, 60, 60))


    def on_quit(self):
        """
        Function to run logic upon quitting game. Also quits pygame. 

        """

        pygame.quit()

    def on_execute(self):
        """
        Should be run on creation of class (Game().on_execute()). Creates game loop
        and runs all necessary functions in said loop. 

        """

        if self.on_init() == False:
            self._running = False
        pygame.display.flip()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.update()
        self.on_quit()


Game().on_execute()
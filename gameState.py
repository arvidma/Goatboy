'''
Created on 12 jul 2011

@author: arvid
'''
import statusPanel, pygame, gameObjects, levelEditor, mapLogic, guiTools, os
 

class GameState(object):
    '''
    This class holds the state of the game. I find it easier to work with than normal, 
    global, Python variables.
    '''
    allsprites = None
    background = None
    back_surface = None
    clock = None
    defaultLevel = None
    frameCounter = 0
    leveleditor = None
    map = None
    mapname = None
    panel = None 
    screen = None
    scrollx = 0
    scrolly = 0
    scoore = 0
    scoreFromPreviousLevel = 0
    scooresurface = None
    startingTime = 0
    thor = None
    window = None
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Goatboy: the horned avenger') #Fonstertitel

        #### Initialize rendering system ####

        resolution = pygame.display.list_modes()[0] # Plockar den hogsta tillgangliga upplosningen
        bitdepth = 32
        flags = pygame.locals.FULLSCREEN | pygame.locals.DOUBLEBUF
        self.window = pygame.display.set_mode(resolution, flags, bitdepth) 

        self.screen = pygame.display.get_surface() # Skarmyta
   
        #### Initialize background images ####

        self.back_file_name = os.path.join("data", "background.bmp") # bakgrundsfilnamnsokvag
        self.back_surface = guiTools.scaleToScreenSize(pygame.image.load(self.back_file_name), self.screen)
        self.background = pygame.Surface(self.screen.get_size())
        self.scooresurface = pygame.Surface((50, 25))
        self.background.blit(self.back_surface, (0, 0))
        
        #### Miscellania ####

        self.clock = pygame.time.Clock()

        self.map = mapLogic.Map()     # skapa ett map-objekt
        self.map.loadmap("map1.map") # ladda banan fran fil
    
        self.panel = statusPanel.statusPanel(self)      # skapa panelen
        self.thor = gameObjects.Goatboy(self)           # skapa ett goatboy-objekt =)
        self.leveleditor = levelEditor.LevelEditor()    # skapa level-editor object
        
#        gameLogic.loadvisible(self)
#        pygame.display.flip()

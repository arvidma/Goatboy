'''
Created on 15 jul 2011

@author: arvid and mikael
'''

import pygame,os


class statusPanel(pygame.sprite.Sprite):    
    gs = None #gameState    
    panelSurface = None
    panelXcoord = 0

    def __init__(self, gameState):
        pygame.sprite.Sprite.__init__(self)
        
        self.gs = gameState
        
        self.panelSurface = pygame.image.load( os.path.join("data", "panel.bmp") )
        self.panelXcoord = (self.gs.screen.get_width() / 2) - 199 # placera panelen mitt pa skarmen
        
    
    def update(self):
        self.gs.background.blit(self.panelSurface, (self.panelXcoord, 0))
    
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.gs.scoore), 1, (120, 120, 120))
        textpos = text.get_rect()
        textpos.centerx = self.gs.background.get_rect().centerx
        self.gs.background.blit(self.gs.scooresurface, textpos)
        self.gs.background.blit(text, textpos)

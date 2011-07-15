#!/usr/bin/python
'''
Created on 12 jul 2011

@author: Arvid
'''

import gameLogic, eventLoop, gameState, pygame, time

def initializeGame():
    
    try:
        import psyco
        psyco.full()
    except:
        print "Couldn't load Psyco. Game might execute somewhat slower, but should still be OK."
        
    gs = gameState.GameState()
    gs.frameCounter = 0                    # Set up FPS counter
    gs.startingTime = time.time()          #
    return gs

def endGame(gameState):
    playingTime = time.time() - gameState.startingTime  
    print "You played the game for %i seconds, during which %i frames were rendered. That gives an average FPS of %i \n" % (playingTime, gameState.frameCounter, gameState.frameCounter/playingTime)
    gameLogic.highscore(gameState.scoore)
    
    pygame.quit()

def main():
    gs = initializeGame()
    
    while eventLoop.proceed(gs):              # The condition of this while-loop is where
        gs.frameCounter = gs.frameCounter + 1 # the games is actually taking place
    
    endGame(gs)


###### Module body #############

if __name__ == '__main__': main()

###### End of module body ###########


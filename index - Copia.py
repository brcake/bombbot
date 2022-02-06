# -*- coding: utf-8 -*-    
from cv2 import cv2
from os import listdir
from src.logger import logger, loggerMapClicked
from random import randint
from random import random
from datetime import datetime
import pygetwindow
import numpy as np
import mss
import pyautogui
import time
import sys
import yaml
import os
import discord
from datetime import datetime
import os
import easyocr
import pandas as pd
from matplotlib import pyplot as plt
import telegram_send
from pynput.keyboard import Key, Controller

# Load config file.
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
ch = c['home']
pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

cat = """

                               (
                             ) )
                            ( (  ))                
                             ) )(
                              ))       ))),,        
                              (       /  ///       
                                     _ _  /
                             _U___  <     )  ()
                            / /      \_- |. //
                            \_|       |,-"|//
                             __     ,-"   //
                            /  \ ,-"     //
               _  .  --. ,--\," "---    //
           /\_/ \| ""  -"    "-.       //
           \  \  |                    //|
          ,_\________________________//||
          '--------------------------, ||           relaxa e f1 enquanto eu farmo pra você
             //                      \\||
            //      BRCAKE710         \\|
=========================================================================
========== 💰 Have I helped you in any way? All I ask is a tip! 🧾 ======
========== ✨ Faça sua boa ação de hoje, manda aquela gorjeta! 😊 =======
=========================================================================
======================== vvv BCOIN BUSD BNB vvv =========================
============== 0x15e52DC513C358a34675e72b2d7beEF28DD98DF9 ===============
=========================================================================
================ twitch.tv/bomberonebr ==================================
=========================================================================

>>---> Press ctrl + c to kill the bot.

>>---> Some configs can be found in the config.yaml file."""







def addRandomness(n, randomn_factor_size=None):
    """Returns n with randomness
    Parameters:
        n (int): A decimal integer
        randomn_factor_size (int): The maximum value+- of randomness that will be
            added to n

    Returns:
        int: n with randomness
    """

    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    """Returns the input_string without the suffix"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images(dir_path='./targets/'):
    """ Programatically loads all images of dir_path as a key:value where the
        key is the file name without the .png suffix

    Returns:
        dict: dictionary containing the loaded images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


def loadHeroesToSendHome():
    """Loads the images in the path and saves them as a list"""
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes

#def sendStashToDiscord():

    if clickBtn(images['stash']):
        time.sleep(2)

        q = datetime.datetime.now()
        d = q.strftime("%d%m%Y%H%M")
        image_file = os.path.join('screenshots', d +'.png')
        pic = pyautogui.screenshot(image_file)

        time.sleep(1)
        webhook = discord.Webhook.from_url("https://discord.com/api/webhooks/937721880155136070/6KX87oqBzAjZIAlKUnEy-KJQNp_a7WBInQZxyMkva5_3QsGnod2N_MHI26pKlkbHWqLm", adapter=discord.RequestsWebhookAdapter())
        webhook.send(file=discord.File(image_file))

        clickBtn(images['x'])
#

def show(rectangles, img = None):
    """ Show an popup with rectangles showing the rectangles[(x, y, w, h),...]
        over img or a printSreen if no img provided. Useful for debugging"""

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)



def FindImageAndBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    start = time.time()
    matches = positions(img, threshold=threshold)
    if(len(matches)==0):
        hast_timed_out = time.time()-start > timeout
        if(hast_timed_out):
            if not name is None:
                pass
            return False
        return False
    else:
        return True

def FindBtnWork(img,name=None, timeout=3, threshold = ct['default']):
    matches = positions(img, threshold=threshold)
    if(len(matches)==0):
        return 0
    else:
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        return pos_click_x 

def clickBtn(img, timeout=3, threshold = ct['default']):
    """Search for img in the scree, if found moves the cursor over it and clicks.
    Parameters:
        img: The image that will be used as an template to find where to click.
        timeout (int): Time in seconds that it will keep looking for the img before returning with fail
        threshold(float): How confident the bot needs to be to click the buttons (values from 0 to 1)
    """

    logger(None, progress_indicator=True)
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold)

        if(len(matches)==0):
            has_timed_out = time.time()-start > timeout
            return False
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True
        print("THIS SHOULD NOT PRINT")
    return False

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():
    commoms = positions(images['commom-text'], threshold=ct['commom'])
    if (len(commoms) == 0):
        commoms = positions(images['rare-text'], threshold=ct['rare'])
        if (len(commoms) == 0):
            commoms = positions(images['super_rare-text'], threshold=ct['super_rare'])
            if (len(commoms) == 0):
                commoms = positions(images['epic-text'], threshold=ct['epic'])
                if (len(commoms) == 0):
                    commoms = positions(images['legend-text'], threshold=ct['legend'])
                    if (len(commoms) == 0):  
                       # commoms = positions(images['super_legend-text'], threshold=ct['super_legend']) 
                        if (len(commoms) == 0):  
                           return
    x,y,w,h = commoms[len(commoms)-1]

    moveToWithRandomness(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0, -c['click_and_drag_amount'], duration=1, button='left')


def clickButtons(max_herois = 0):
    ClickGreenAndShowLog = max_herois > 0
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    if ClickGreenAndShowLog == True:
        hero_clicks_cnt = 0
        for (x, y, w, h) in buttons:
            moveToWithRandomness(x+(w/2),y+(h/2),1)
            pyautogui.click()
            global hero_clicks
            hero_clicks = hero_clicks + 1
            hero_clicks_cnt = hero_clicks_cnt + 1
            if hero_clicks_cnt == max_herois:
               return hero_clicks_cnt 
            #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
            if hero_clicks > 20:
                logger('too many hero clicks, try to increase the go_to_work_btn threshold')
                return
        return hero_clicks_cnt
    else:  
        return len(buttons)

def isHome(hero, buttons):
    y = hero[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def descobreRaridade(bar):
    commoms = positions(images['commom-text'], threshold=ct['commom'])
    rares = positions(images['rare-text'], threshold=ct['rare'])
    super_rares = positions(images['super_rare-text'], threshold=ct['super_rare'])
    epics = positions(images['epic-text'], threshold=ct['epic'])
    legends = positions(images['legend-text'], threshold=ct['legend'])
   # super_legends = positions(images['super_legend-text'], threshold=ct['super_legend'])

    y = bar[1]

    for (_, button_y, _, button_h) in commoms:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return 'commom'

    for (_, button_y, _, button_h) in rares:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return 'rare'

    for (_, button_y, _, button_h) in super_rares:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return 'super_rare'

    for (_, button_y, _, button_h) in epics:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return 'epic'

    for (_, button_y, _, button_h) in legends:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return 'legend'

   # for (_, button_y, _, button_h) in super_legends:
       # isBelow = y < (button_y + button_h)
       # isAbove = y > (button_y - button_h)
       # if isBelow and isAbove:
           # return 'super_legend'

    return 'null'

def clickGreenBarButtons(baus=0, max_herois = 0):
    # ele clicka nos q tao trabaiano mas axo q n importa
    ClickGreenAndShowLog = max_herois > 0
    offset = 140

    green_bars = positions(images['green-bar'], threshold=ct['green_bar'])
    
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    go_work_x = FindBtnWork(images['go-work'])
    if go_work_x == 0:
       go_work_x = FindBtnWork(images['go-work'])
   # if ClickGreenAndShowLog == True:
       # logger('%d green bars detected' % len(green_bars))
       # logger('%d buttons detected' % len(buttons))
    
    global deveTrabalhar
    global raridade
    not_working_green_bars = []
    for bar in green_bars:       
        deveTrabalhar = 1
        if c['escolher_baus_heroes'] == True:
            raridade = descobreRaridade(bar) 
            if raridade != 'commom' and (baus >= 60 or baus == 0):
                deveTrabalhar = 0

        if (not isWorking(bar, buttons)) and deveTrabalhar == 1:
            not_working_green_bars.append(bar)
   # if len(not_working_green_bars) > 0 and ClickGreenAndShowLog == True:
       # logger('%d buttons with green bar detected' % len(not_working_green_bars))
       # logger('Clicking in %d heroes' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    hero_clicks_cnt = 0
    if ClickGreenAndShowLog == True:
        for (x, y, w, h) in not_working_green_bars:
            # isWorking(y, buttons)
            moveToWithRandomness(go_work_x,y+(h/2),1)
           # moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
            pyautogui.click()
            global hero_clicks
            hero_clicks = hero_clicks + 1
            hero_clicks_cnt = hero_clicks_cnt + 1
            if hero_clicks_cnt == max_herois:
               return hero_clicks_cnt 
            if hero_clicks_cnt > 20:
                logger('Too many hero clicks, try to increase the go_to_work_btn threshold')
                return
            #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        return hero_clicks_cnt
    else:
        return len(not_working_green_bars) 

def clickFullBarButtons(max_herois = 0):
    ClickGreenAndShowLog = max_herois > 0
    offset = 100
    full_bars = positions(images['full-stamina'], threshold=ct['default'])
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0 and ClickGreenAndShowLog == True:
        logger('Clicking in %d heroes' % len(not_working_full_bars))
    hero_clicks_cnt = 0
    if ClickGreenAndShowLog == True: 
        for (x, y, w, h) in not_working_full_bars:
            moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
            pyautogui.click()
            global hero_clicks
            hero_clicks = hero_clicks + 1
            hero_clicks_cnt = hero_clicks_cnt + 1
            if hero_clicks_cnt == max_herois:
               return hero_clicks_cnt 
        return hero_clicks_cnt 
    else:
        return len(not_working_full_bars)

def goToHeroes():
    if clickBtn(images['go-back-arrow']):
        global login_attempts
        login_attempts = 0

    #TODO tirar o sleep quando colocar o pulling
    time.sleep(1)
    clickBtn(images['hero-icon'])
    time.sleep(1)

def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])

#    sendStashToDiscord()

def refreshHeroesPositions():

    if clickBtn(images['go-back-arrow']):
        logger('Refreshing Heroes Positions')
        clickBtn(images['treasure-hunt-icon'])

        return True
    else:
        return False

def login():
    global login_attempts
    

    if login_attempts > 3:
        logger('Too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        return

    if clickBtn(images['connect-wallet'], timeout = 10):
        logger('Connect wallet button detected, logging in!')
        login_attempts = login_attempts + 1
        #TODO mto ele da erro e poco o botao n abre
        time.sleep(7)
    
    if not FindImageAndBtn(images['select-wallet-2']):
        time.sleep(5)

    if clickBtn(images['select-wallet-2'], timeout=8):
        logger('Checking if game has disconnected')
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        time.sleep(10)
        if not FindImageAndBtn(images['treasure-hunt-icon']):
            time.sleep(5)
        if clickBtn(images['treasure-hunt-icon'], timeout = 15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
            time.sleep(2)
            refreshHeroes()
        return
        # click ok button

    if not clickBtn(images['select-wallet-1-no-hover'], ):
        if clickBtn(images['select-wallet-1-hover'], threshold = ct['select_wallet_buttons'] ):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(images['select-wallet-2'], timeout = 20):
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        time.sleep(10)
        if clickBtn(images['treasure-hunt-icon'], timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
            time.sleep(2)
            refreshHeroes()
        # time.sleep(15)

    if FindImageAndBtn(images['ok']):
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        time.sleep(15)



def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len (hero_positions) == 0:
            #TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0]+go_home_buttons[0][2]/2,position[1]+position[3]/2,1)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')



def checkBaus():
    logger('Search for Chests to map')

    bausWood = positions(images['bau-wood'], threshold=ct['bau_wood'])
    bausWoodMeio = positions(images['bau-wood-50'], threshold=ct['bau_wood_50'])
    bausWoodFechado = positions(images['bau-wood-100'], threshold=ct['bau_wood_100'])

    bausRoxo = positions(images['bau-roxo'], threshold=ct['bau_roxo'])
    bausRoxoMeio = positions(images['bau-roxo-50'], threshold=ct['bau_roxo_50'])
    bausRoxoFechado = positions(images['bau-roxo-100'], threshold=ct['bau_roxo_100'])

    bausGold = positions(images['bau-gold'], threshold=ct['bau_gold'])
    bausGoldMeio = positions(images['bau-gold-50'], threshold=ct['bau_gold_50'])
    bausGoldFechado = positions(images['bau-gold-100'], threshold=ct['bau_gold_100'])

    bausBlue = positions(images['bau-blue'], threshold=ct['bau_blue'])
    bausBlueMeio = positions(images['bau-blue-50'], threshold=ct['bau_blue_50'])
    bausBlueFechado = positions(images['bau-blue-100'], threshold=ct['bau_blue_100'])
    
    global response
    if (len(bausRoxoMeio) > 0 or len(bausGoldMeio) > 0 or len(bausBlueMeio) > 0) and (len(bausRoxo) + len(bausGold) + len(bausBlue)+len(bausRoxoFechado) + len(bausGoldFechado) + len(bausBlueFechado)) > 0:
        response = (
                           (len(bausRoxoMeio) + len(bausGoldMeio) + len(bausBlueMeio))
                           * 100
                   ) / (len(bausRoxo) + len(bausGold) + len(bausBlue)+len(bausRoxoFechado) + len(bausGoldFechado) + len(bausBlueFechado))
    else:
        response = 0

    global numerobau
    numerobau= (len(bausWoodMeio) + len(bausRoxoMeio) + len(bausGoldMeio) + len(bausBlueMeio)+ len(bausWood)+ len(bausRoxo) + len(bausGold) + len(bausBlue)+ len(bausWoodFechado)+ len(bausRoxoFechado) + len(bausGoldFechado) + len(bausBlueFechado))
    if (len(bausBlue) + len(bausBlueFechado)) > 0 and numerobau > 10:
       response = 1
    
    logger('|Only send Rarities if result is less than 60        | ')
    logger('|or if blue chests longer than half-life are detected| ')
    logger('Return for calculation : %d' % (response))
    return response

def NumeroBaus():

    bausWood = positions(images['bau-wood'], threshold=ct['bau_wood'])
    bausWoodMeio = positions(images['bau-wood-50'], threshold=ct['bau_wood_50'])
    bausWoodFechado = positions(images['bau-wood-100'], threshold=ct['bau_wood_100'])

    bausRoxo = positions(images['bau-roxo'], threshold=ct['bau_roxo'])
    bausRoxoMeio = positions(images['bau-roxo-50'], threshold=ct['bau_roxo_50'])
    bausRoxoFechado = positions(images['bau-roxo-100'], threshold=ct['bau_roxo_100'])

    bausGold = positions(images['bau-gold'], threshold=ct['bau_gold'])
    bausGoldMeio = positions(images['bau-gold-50'], threshold=ct['bau_gold_50'])
    bausGoldFechado = positions(images['bau-gold-100'], threshold=ct['bau_gold_100'])

    bausBlue = positions(images['bau-blue'], threshold=ct['bau_blue'])
    bausBlueMeio = positions(images['bau-blue-50'], threshold=ct['bau_blue_50'])
    bausBlueFechado = positions(images['bau-blue-100'], threshold=ct['bau_blue_100'])

    logger('Chests Wood   =>   '+'   %d +-50 hp ' % len(bausWoodMeio) + '   --   %d +-80 hp ' %len(bausWood) + '   --   %d 100 hp ' % len(bausWoodFechado))
    logger('Chests Purple =>   '+'   %d +-50 hp ' % len(bausRoxoMeio) + '   --   %d +-80 hp ' %len(bausRoxo) + '   --   %d 100 hp ' % len(bausRoxoFechado))
    logger('Chests Gold   =>   '+'   %d +-50 hp ' % len(bausGoldMeio) + '   --   %d +-80 hp ' %len(bausGold) + '   --   %d 100 hp' % len(bausGoldFechado))
    logger('Chests Blue   =>   '+'   %d +-50 hp ' % len(bausBlueMeio) + '   --   %d +-80 hp ' %len(bausBlue) + '   --   %d 100 hp ' % len(bausBlueFechado))
    
    global numerobau
    numerobau= (len(bausWoodMeio) + len(bausRoxoMeio) + len(bausGoldMeio) + len(bausBlueMeio)+ len(bausWood)+ len(bausRoxo) + len(bausGold) + len(bausBlue)+ len(bausWoodFechado)+ len(bausRoxoFechado) + len(bausGoldFechado) + len(bausBlueFechado))
    logger('Total Number: %d detected chests' % numerobau)
    return numerobau

def clickFullRest():
    while (True):
        buttons = positions(images['rest'], threshold=ct['rest'])
        if len(buttons) > 0:
            clickBtn(images['alldesc'])
           # clickBtn(images['rest'])
        else:
            return

def refreshHeroes():
    logger('Search for heroes to work')

    global baus
    global numero_herois
    global max_herois
    global numero_baus
    numero_herois = 0
    max_herois = 99
    if c['mandar_todos_trabalhar'] == False and c['escolher_baus_heroes'] == True:
        goToHeroes()
        clickFullRest()
        goToGame()
        baus = checkBaus()
        numero_baus = NumeroBaus() 
        if numero_baus < 1:
           numero_baus = numero_baus + 1 
        if numero_baus > 7:
           logger('---------------------------------💪 Requesting at most {} Heroes '.format(15))
        else: 
           logger('---------------------------------💪 Requesting at most {} Heroes '.format(numero_baus * 3))   
    goToHeroes()
    if FindImageAndBtn(images['select-character-heroes']):
        if True:
            if c['mandar_todos_trabalhar'] == True:
                if FindImageAndBtn(images['all']):
                    clickBtn(images['all'])
                    logger('heroes sent all to work')
                goToGame()
            else:
                if c['escolher_baus_heroes'] == True: 
                    logger('Sending heroes with green stamina bar to work', 'green')
                    empty_scrolls_attempts = c['scroll_attemps']
                    while(empty_scrolls_attempts >=0):
                        if FindImageAndBtn(images['full-stamina']):
                            clickBtn(images['all'])
                            logger('+Sending all heroes to work') 
                            goToGame()
                            return
                        max_herois = (numero_baus * 3) - numero_herois
                        numero_herois = numero_herois + clickGreenBarButtons(baus, max_herois)
                        sendHeroesHome()
                        if numero_herois == (numero_baus * 3):  
                            logger('---------------------------------💪+ {} Heroes went to work 💪'.format(numero_herois))                     
                            goToGame()
                            return
                        empty_scrolls_attempts = empty_scrolls_attempts - 1
                        scroll()
                    logger('---------------------------------💪 {} Heroes went to work 💪'.format(numero_herois))  
                else:       
                    if c['select_heroes_mode'] == "full":
                        logger('Sending heroes with full stamina bar to work', 'green')
                    elif c['select_heroes_mode'] == "green":
                       logger('Sending heroes with green stamina bar to work', 'green')
                    else:
                        logger('Sending all heroes to work', 'green')
                    buttonsClicked = 1
                    empty_scrolls_attempts = c['scroll_attemps']
                    while(empty_scrolls_attempts >0):
                        if c['select_heroes_mode'] == 'full':                       
                            numero_herois = clickFullBarButtons()
                            buttonsClicked = clickFullBarButtons(max_herois) 
                        elif c['select_heroes_mode'] == 'green':                        
                            numero_herois = clickGreenBarButtons(baus)
                            buttonsClicked = clickGreenBarButtons(baus, max_herois)
                        else:          
                            numero_herois = clickButtons()
                            buttonsClicked = clickButtons(max_herois)
                        sendHeroesHome()
                        if buttonsClicked == 0:
                            empty_scrolls_attempts = empty_scrolls_attempts - 1
                        scroll()
                        time.sleep(2)
                goToGame()    
        
def mapIsActive():
    go_back_arrow = positions(images['go-back-arrow'])
    if(len(go_back_arrow)>0):
        return True
    else:
        return False

def refreshGame():
    keyboard = Controller()
    keyboard.press(Key.f5)
    keyboard.release(Key.f5)
    time.sleep(1)
    login()

def checkChests(newMap=False):
    if(mapIsActive()):
        logger('🔎 Checking chests quantity')
        #TODO: Diminuir treshold para 0.5 e testar
        wood_chest_closed = positions(images['wood_chest_closed'])
        wood_chest_hit = positions(images['wood_chest_hited_top'])
        steel_chest_closed = positions(images['steel_chest_closed'])
        steel_chest_hit = positions(images['steel_chest_hited_top'])
        gold_chest_closed = positions(images['gold_chest_closed'])
        gold_chest_hit = positions(images['gold_chest_hited'])
        diamond_chest_closed = positions(images['diamond_chest_closed'])
        diamond_chest_hit = positions(images['diamond_chest_hited'])
        jail_closed = positions(images['jail_closed'])
        jail_hit = positions(images['jail_hited'])
        #TODO: colocar sprites do baú da chave

        wood_qtd = len(wood_chest_hit)+len(wood_chest_closed)
        steel_qtd = len(steel_chest_hit)+len(steel_chest_closed)
        gold_qtd = len(gold_chest_hit)+len(gold_chest_closed)
        diamond_qtd = len(diamond_chest_hit)+len(diamond_chest_closed)
        jail_qtd = len(jail_hit)+len(jail_closed)
        all_chests = wood_qtd+steel_qtd+gold_qtd+diamond_qtd+jail_qtd

        result = "🟫 Baús de madeira: {}\n🟪 Baús de ferro: {}\n🟨 Baús de ouro: {}\n🟦 Baús de diamante: {}\n🏛️ Jaulas: {}".format(wood_qtd, steel_qtd, gold_qtd, diamond_qtd, jail_qtd) 
        print(result)

        if(newMap):
            telegram_send.send(messages=[result])

        if(all_chests==0):
            refreshGame()

def checkBcoins():
    logger('🪙 Checking bcoins value on chest')

    clickBtn(images['chest-icon'])

    bcoins_value_rect = positions(images['bcoins-value'])

    if (len(bcoins_value_rect) != 0): 
        time.sleep(1)
        logger('📸 Taking a screenshot of the chest')    
        myScreenshot = pyautogui.screenshot(region=tuple(bcoins_value_rect[0]))
        myScreenshot.save(r'bcoins_value.png')

        logger('🔎 Reading the value of BCOINS in the chest')
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext('bcoins_value.png', paragraph="False") 




        if(len(result)>1):
            if(len(result[1])>1):
                bcoins_value = result[1][1]
                bcoin_record = {'date': str(datetime.now()), 'value': bcoins_value}
                bcoin_database = pd.read_csv('database/bcoin.csv')
                bcoin_database = bcoin_database.append(bcoin_record, ignore_index=True)
                bcoin_database.to_csv('database/bcoin.csv', index=False)
                logger('✉️ Sending the BCOINS quantity to telegram: ')
                telegram_send.send(messages=["🪙 Total de BCOINS no baú: " + bcoins_value])
        os.remove('bcoins_value.png')  

    clickBtn(images['x'])
    sendMapImageToTelegram()

def sendMapImageToTelegram():
    logger('📸 Taking a screenshot of the map')  
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'map_image.png')
    map_image = open('map_image.png', 'rb')

    logger('🗺️ Sending map image to telegram: ')
    telegram_send.send(images=[map_image])
    #telegram_send.send(messages=['🗺️ Um novo mapa apareceu!'])

    #os.remove('map_image.png')



def main():
    """Main execution setup and loop"""
    # ==Setup==
    global hero_clicks
    global login_attempts
    global last_log_is_progress
    hero_clicks = 0
    login_attempts = 0
    last_log_is_progress = False

    global images
    images = load_images()

    if ch['enable']:
        global home_heroes
        home_heroes = loadHeroesToSendHome()
    else:
        print('>>---> Home feature not enabled')
    print('\n')

    print(cat)
    time.sleep(7)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "check_bcoins": 0,
    "check_chests": 0,
    "heroes" : 0,
    "new_map" : 0,
    "check_for_captcha" : 0,
    "refresh_heroes" : 0
    }
    # =========


    windows = []
    for w in pygetwindow.getWindowsWithTitle('bombcrypto'):
        windows.append({
            "window": w,
            "login" : 0,
            "heroes" : 0,
            "new_map" : 0,
            "n9_heroes" : False,
            "check_for_captcha" : 0,
            "refresh_heroes" : 0
            })
    logger('---> %d windows detected' % len(windows))

    while True:
        now = time.time()
        if now - last["check_chests"] > addRandomness(t["check_chests"] * 60):
            last["check_chests"] = now
            checkChests()

        if now - last["check_bcoins"] > addRandomness(t["check_bcoins"] * 60):
            last["check_bcoins"] = now
            checkBcoins()

        for last in windows:
            logger('changing to another window...')
            last["window"].activate()
            if last["window"].isMaximized == False and c['windows_maximize'] == True:
                last["window"].maximize()
               

            logger('---> window:                    %s' % last["window"].title)

            time.sleep(1)
              
            now = time.time()
            if FindImageAndBtn(images['ok']):
                login_attempts = 0
                pyautogui.hotkey('ctrl','f5')
                time.sleep(15)
                sys.stdout.flush()
                last["login"] = now
                login()

            bonecozzzc = 0 
            if c['escolher_baus_heroes'] == True:
                bonecozzzc = positions(images['zzz'], threshold=ct['zzz'])
                if len(bonecozzzc) < 9:
                    time.sleep(2)
                    bonecozzzc = positions(images['zzz'], threshold=ct['zzz']) 
                logger('Detected %d sleeping Heroes ' % len(bonecozzzc)) 
                if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60): 
                    if len(bonecozzzc) > 9: 
                        last["heroes"] = now  
                        last["n9_heroes"] = False         
                        refreshHeroes()
                        last["refresh_heroes"] = now 
                else:
                    if len(bonecozzzc) > 9 and last["n9_heroes"] == False:
                        logger('%d sleeping heroes. Refresh Heroes' % len(bonecozzzc))   
                        last["heroes"] = now  
                        last["n9_heroes"] = True
                        refreshHeroes()
                        last["refresh_heroes"] = now 
            else:         
                if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
                    last["heroes"] = now
                    refreshHeroes()
                    last["refresh_heroes"] = now 
    
            if FindImageAndBtn(images['select-wallet-2']):
                sys.stdout.flush()
                last["login"] = now
                login()

 
            if now - last["login"] > addRandomness(t['check_for_login'] * 60):
                sys.stdout.flush()
                last["login"] = now
                login()


  
            if now - last["new_map"] > t['check_for_new_map_button']:
                last["new_map"] = now

                if clickBtn(images['new-map']):
                    loggerMapClicked()
                    checkChests(newMap=True)
                    sendMapImageToTelegram()



                    time.sleep(2)
                    if len(bonecozzzc) > 9 or c['escolher_baus_heroes'] == False:
                        last["heroes"] = now   
                        refreshHeroes()
                        last["refresh_heroes"] = now  
         

            if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
                last["refresh_heroes"] = now
                refreshHeroesPositions()

           
            if FindImageAndBtn(images['treasure-hunt-icon']):
                if clickBtn(images['treasure-hunt-icon'], timeout=25):
                    # print('sucessfully login, treasure hunt btn clicked')
                    login_attempts = 0
                    time.sleep(2)
                    last["heroes"] = now 
                    refreshHeroes()
                    last["refresh_heroes"] = now 
            
            logger(None, progress_indicator=True)

            sys.stdout.flush()

            time.sleep(1)

if __name__ == '__main__':



    main()


#cv2.imshow('img',sct_img)
#cv2.waitKey()

# colocar o botao em pt
# soh resetar posiçoes se n tiver clickado em newmap em x segundos



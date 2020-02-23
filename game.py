import pygame, mysql.connector

pygame.init()
screen = pygame.display.set_mode([1024,768]) # Set the width and height of the screen [width,height]
pygame.display.set_caption("Dragon Hunter")       # Name your window
done = False                                # Loop until the user clicks the close button.
pygame.font.init()
#print(pygame.font.get_fonts())
font = pygame.font.Font(None,24)
clock = pygame.time.Clock() 
main = True
stringArray = []
bgImg = None
class player():
    def __init__(self):
        self.name = ""
        self.playerClass = ""
        self.money = 100
        self.inventory = []
        self.quests = []
    def addQuest(self,title, description):
        addTextNicely("Quest Added: "+title)
        addTextNicely("Quest Description: "+description)
        self.quests.append(quest(title,description))
    
class quest():
    def __init__(self,qTitle,qDesc):
        self.title = qTitle
        self.description = qDesc
        self.complete = False
    def completeQuest(self):
        addTextNicely("Quest: "+self.title)
        addTextNicely("Complete!")
        self.complete= True
def chooseInventoryItem(question, playerInstance):
    if playerInstance.inventory == []:
        return None
    else:
        text = ""
        for i in playerInstance.inventory:
            text += i+", "
        text = text[:-2]
        return(askQuestion(question+": "+text,playerInstance.inventory,playerInstance))
def shop(playerInstance, itemsToBuy, costs):
    done = False
    while not done:
        addTextNicely("You have "+str(playerInstance.money)+"G")
        addTextNicely("Items for sale:")
        text = ""
        for count in range(len(itemsToBuy)):
            text += itemsToBuy[count]+" ("+str(costs[count])+"G), "
        addTextNicely(text)
        option = askQuestion("Buy item? Item name/leave",["leave"]+itemsToBuy,playerInstance)
        if option == 0:
            done = True
        else:
            if playerInstance.money >= costs[option-1]:
                if (askQuestion("Buy "+itemsToBuy[option-1]+"? Y/N",["y","n"],playerInstance) == 0):
                    playerInstance.inventory.append(itemsToBuy[option-1])
                    playerInstance.money -= costs[option-1]
            else:
                addTextNicely("Not enough funds")
def checkHeight(extra = 1):
    for e in range(extra):
        if font.get_height()*(len(stringArray)+extra-1) > 268:
            stringArray.pop(0)
def displayGraphics():
    if bgImg != None:
        screen.blit(bgImg,(0,0))
    pygame.draw.rect(screen,(0,0,0),(0,500,1024,268))
def addTextNicely(text):
    stringArray.append("")
    checkHeight()
    count = 0 
    display = 0
    while count < len(text):
        if display == 2:
            stringArray[len(stringArray)-1] = stringArray[len(stringArray)-1] + text[count]
            count += 1
        if display > 2:
            display = 0
        display += 1
        screen.fill((0,0,0))
        displayText()
        pygame.display.flip()
def askQuestion(question, answers = [], playerInstance= None):#answers list
    answered = False
    while not answered:
        addTextNicely(question)
        answer = getData()
        stringArray.append(answer)
        checkHeight()
        if answer == "help":
            addTextNicely("Commands: viewQuests, viewInventory")
        elif answer == "viewQuests" and playerInstance != None:
            addTextNicely("Quests: Description: Complete")
            for q in playerInstance.quests:
                addTextNicely(q.title+": "+q.description+": "+str(q.complete))
        elif answer == "viewInventory" and playerInstance!= None:
            addTextNicely("Inventory: Money: "+str(playerInstance.money))
            text = ""
            if playerInstance.inventory == []:
                addTextNicely("Empty")
            else:
                for i in playerInstance.inventory:
                    text+= i+", "
                addTextNicely(text)
    

        elif answers == []:
            return(answer)
        else:
            count = 0
            for option in answers:
                if answer.lower() == option.lower():
                    return(count)
                count += 1
            addTextNicely("Not an option")
            

def displayText():
    fontSize = font.get_height()
    count = 0
    for text in stringArray:
        screen.blit(font.render(text,1,(255,255,255)),(10,510+fontSize*count))
        count += 1
def getData():
    checkHeight(2)
    displayGraphics()
    displayText()
    text = ""
    fontSize = font.get_height()
    yPosition =510+len(stringArray)*fontSize
    done = False
    shift = False
    capslock = False
    keyHeld = False
    keyPressed = 0
    heldCount = 0
    multiKeyMultiplier = 1 #speeds up how often a repeated key is added to text
    underline = font.render("_",1,(255,255,255))
    underlineFlash = 0
    while not done:
        if heldCount >= 20 - 2*multiKeyMultiplier:
            if keyPressed == 8:
                text = text[:-1]
            elif keyPressed != 301 and keyPressed != 304 and keyPressed != 60 and keyPressed != 46 and keyPressed !=47: 
                if shift or capslock:
                    text += (chr(keyPressed)).upper()
                else:
                    text += chr(keyPressed)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keyHeld = True
                keyPressed = event.key
                if keyPressed == 301:
                    capslock = True
                elif keyPressed == 304:
                    shift= True
                elif keyPressed >= 32 and keyPressed<=126:
                    if keyPressed != 60 and keyPressed != 92 and keyPressed != 46 and keyPressed != 47:
                        if shift == True or capslock== True:
                            text += (chr(keyPressed)).upper()
                        else:
                            text+=chr(keyPressed)
                elif keyPressed == 8:
                    text = text[:-1]
                elif keyPressed == 13 and len(text) >0: 
                    done = True
                    return(text)
            if event.type == pygame.KEYUP:
                keyHeld = False
                multiKeyMultiplier =1
                heldCount = 0
                if event.key == 304:
                    shift= False
                if event.key == 301:
                    capslock = False
        if keyHeld:
            heldCount += 1
        if heldCount > 20 - 2*multiKeyMultiplier:
            heldCount = 0
            if multiKeyMultiplier < 10:
                multiKeyMultiplier += 1
        pygame.draw.rect(screen,(0,0,0),(0,yPosition,1024,fontSize))
        screen.blit(font.render(text,1,(255,255,255)),(10,yPosition))
        if underlineFlash < 30:
            screen.blit(underline,(10+ font.size(text)[0],yPosition))
        underlineFlash+= 1
        if underlineFlash > 60:
            underlineFlash = 0
        pygame.display.flip()
        clock.tick(60)
#mydb = mysql.connector.connect(host="192.168.0.84",user="root",passwd="eatshit69", database="players")
#mycursor = mydb.cursor()
#mycursor.execute("SHOW DATABASES")
#open("ssh","w+")

#addTextNicely("You are a mercenary looking for work, who has just arrived in the town of Baggardy")
#addTextNicely("In the town the best places to look for work would be the shop, tavern, or blacksmith")
#askQuestion("Where would you like to go?",["shop","tavern","blacksmith"])
#while main:
#    for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                main = False
#    screen.fill((0,0,0))
#    displayText()
#    pygame.display.flip()
#    clock.tick(60)
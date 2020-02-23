import game, pygame
pygame.init()
screen = pygame.display.set_mode([1024,768]) # Set the width and height of the screen [width,height]
pygame.display.set_caption("Dragon Hunter")       # Name your window                            # Loop until the user clicks the close button.

def play():
    die = False
    win= False
    player = game.player()
    baggardy1 = True
    talkedToShopKeep = False
    workFound = False
    seenScorpians = False
    def shopKeeperTalk():
        leave = False
        game.addTextNicely('"Hello, welcome to my store," The shopkeeper says with a smile')
        while not leave:
            option = game.askQuestion("What would you like to say? ask to: shop/where can find work/leave",["shop","work","where can find work","leave"], player)
            if option == 0:
                oldMon = player.money
                game.shop(player, ["Rope","Apples","Ring","Teeth"],[10,4,50,10])
                if oldMon > player.money:
                    game.addTextNicely('"Thank you for your purchase,"')
            elif option == 1 or option == 2:
                game.addTextNicely('"Well the barman at the tavern recieves bounties from the king, so probably best to ask there,"')
                talkedToShopKeep = True
            else:
                leave = True
            
    def shop():
        if not die:
            game.addTextNicely("You enter the shop.")
            game.addTextNicely("You see a shop filled with a myriad of items any traveller would want.")
            game.addTextNicely("The shopkeeper and his dog sit patiently behind the well stocked counter.")
            option = game.askQuestion("What would you like to do? talk/leave",["talk","leave"], player)
            if option == 0:
                shopKeeperTalk()
    def talkBarman():
        if not die:
            game.addTextNicely("The barman looks at you.")
            if game.askQuestion("What will you do? talk/leave",["talk","leave"], player) == 0:
                option = game.askQuestion("The barman still looks at you. Ask: drink/work/leave",["drink","work","leave"], player)
                if option == 0:
                    oldMon = player.money
                    game.shop(player, ["Water","Beer","Apple Juice","Whisky"],[5,10,10,20])
                    if oldMon > player.money:
                        game.addTextNicely("The barman gives you a small smile.")
                if option == 1:
                    game.addTextNicely("The barman crouches below the bar and hands you a piece of paper")
                    workFound = True
                    game.addTextNicely("You read the paper:")
                    game.addTextNicely("By the orders of King Heron, Searching for someone to slay the dragon that resides in Bristle Cave")
                    game.addTextNicely("REWARD: 10,000G")
                    player.quests[0].completeQuest()
                    player.addQuest("Slay the Dragon","Kill the dragon in Bristle Cave")
                    game.addTextNicely("You may now leave Baggardy")
    def threatenScorpianMan():
        game.addTextNicely("You tell the man to **********.                                               ")
        game.addTextNicely("He stabs you in the gut.")

    def talkGroup():
        game.addTextNicely("As you begin to approach the group you can see hunting knives strapped to their legs, and scorpian tattoos on their arms.")
        seenScorpians = True
        if not game.askQuestion("What would you like to do? Talk/Leave",["talk","leave"], player):
            game.addTextNicely("As you draw near the men the one closest to you stands up and draws his knife on you.")
            if game.askQuestion("What will you do? apologise/threaten",["Apologise","Threaten"], player):
                threatenScorpianMan()
                return(True)
            else:
                game.addTextNicely("You raise up your hands and tell him your sorry")
                game.addTextNicely('"Back off," He says')
                option =game.askQuestion("What will you do? back off/threaten",["leave", "back off","threaten"], player)
                if option == 2:
                    threatenScorpianMan()
                    return(True)
        return(False)

    def tavern():
        game.addTextNicely("The tavern is quiet, apart from a group of four men talking amoungst themselves in the corner.")
        game.addTextNicely("The tavern owner is drying glasses behind the bar.")
        dead = False
        leave = False
        while not leave:
            option = game.askQuestion("What do you want to do?" "Talk to: barman/group of men/leave", ["barman", "men","group of men", "leave"], player)
            if option == 0:
                talkBarman()
            elif option == 1 or option == 2:
                dead = talkGroup()
                if dead:
                    leave = True
            else:
                leave = True
        return(dead)
    def blacksmith():
        game.addTextNicely("You see a blacksmith hard at work")
        if not game.askQuestion("What will you do? talk/leave",["talk","leave"], player):
            game.addTextNicely('"Do you need some weapons lad?" She says')
            leave = False
            while not leave:
                option = game.askQuestion("What will you say? shop/work/leave",["shop","work","leave"],player)
                if option == 0:
                    game.shop(player,["Sword","Lance"],[50,50])
                if option == 1:
                    game.addTextNicely("Don't know anything bout that sorry")
                else:
                    leave = True


    def road():
        dead = False
        game.addTextNicely("You begin your journey towards Bristle Cave")
        game.addTextNicely("It will take two days on foot")
        game.addTextNicely("After several hours along your way you spot a carraige that has crashed")
        if not (game.askQuestion("Investigate? Y/N",["Y","N"],player)):
            game.addTextNicely("As you get closer to the carriage you see a lone hatchet lodged into the carriages side")
            game.addTextNicely("There is an image of a scorpian carved onto the hatchets head")
            option = game.askQuestion("What will you do? ???/leave", ["axe","hatchet","take hatchet","take axe","leave"], player)
            if option >= 0 and option <=4:
                game.addTextNicely("Acquired Hatchet")
                player.inventory.append("hatchet")
        game.addTextNicely("After leaving the carriage behind you realise that night will soon fall.")
        if game.askQuestion("What will you do? continue/camp",["continue","camp"],player):
            if game.askQuestion("Will you set a fire? Y/N",["y","n"],player):
                game.addTextNicely("You wake up the next morning feeling cold, but otherwise fine.")
            else:
                game.addTextNicely("Bandits spot your fire, and they murder and rob you in your sleep.")
                dead = True
        else:
            game.addTextNicely("You continue on your way towards Bristle Cave.")
            game.addTextNicely("Sometime late into the night you are ambushed by bandits!")
            if game.askQuestion("What will you do? run/fight", ["run","fight"]):
                if player.inventory == []:
                    game.addTextNicely("You have nothing to fight with!")
                    game.addTextNicely("The bandits slaughter you")
                    dead = True
                else:
                    text = ""
                    for i in player.inventory:
                        text+= i+", "
                    option = game.askQuestion("What will you fight with? "+text, player.inventory, player)
                    if player.inventory[option] == "hatchet":
                        game.addTextNicely("You draw the hatchet, and hold it steady in your hands")
                        game.addTextNicely("The bandits pause and glance at each other before taking off!")
                    elif player.invenory[option] == "sword" or player.inventory[option] == "lance":
                        game.addTextNicely("You draw your "+player.inventory[option]+" and manage to fight off the bandits!")
                    else:
                        game.addTextNicely("Your weapon was not enough to fight off the bandits!")
                        dead = True
            else:
                game.addTextNicely("The bandits catch you and kill you.")
                dead = True
            return(dead)
    def attackDragon():
        
        option = game.chooseInventoryItem("Choose a weapon",player)
        if option == None:
            game.addTextNicely("You cannot defeat the dragon with no weapon.")
            return(False)
        if player.inventory[option] == "hatchet" or player.inventory[option] == "lance" or player.inventory[option] == "sword":
            game.addTextNicely("You sneak upon the dragon and stab the " +player.inventory[option]+ " into it's heart!")
            game.addTextNicely("You Win!")
            return(True)
    def cave():
        win = False
        game.addTextNicely("You reach Bristle Cave early afternoon.")
        game.addTextNicely("You enter the cave, it is dark and quiet.")
        game.addTextNicely("After walking for a bit you come across a sleeping dragon")
        option =game.askQuestion("What do you do? yell/attack",["yell","attack"],player)
        if option == 1:
            win =attackDragon()
        else:
            game.addTextNicely("You yell and the dragon wakes up and kills you ")
            win = False
        return(win)
        
    player.name = game.askQuestion("What is your name?")
    player.playerClass = game.askQuestion("What is your profession? Knight/Mercenary/Wizard",["Knight","Mercenary","Wizard"], player)
    game.addTextNicely("You are low on funds and are looking for work, you have just arrived in the town of Baggardy.")
    player.addQuest("Find Work","Find some work in the town of Baggardy")
    bagOptions = ["shop","tavern","blacksmith"]
    bagText = "Where would you like to go? shop/tavern/blacksmith (You can also type help to see other commands)"
    while baggardy1 and not die:
        game.addTextNicely("In the town the best places to look for work would be the shop, tavern, or blacksmith.")

        option = game.askQuestion(bagText,bagOptions, player)

        if option == 0:
            shop()
        elif option ==1:
            die = tavern()
            if player.quests[0].complete == True:
                bagOptions.append("leave")
                bagOptions.append("leave Baggardy")
                bagText = "Where would you like to go? shop/tavern/blacksmith/leave Baggardy (You can also type help to see other commands)"
        elif option == 2:
            blacksmith()
        else:
            baggardy1 = False
    if not die:
        die = road()
    if not die:
        win = cave()
    return(win)
    

playGame = True
winGame = play()
while playGame:
    if not winGame:
        game.addTextNicely("You Lose :(")
    option = game.askQuestion("Play Again? Yes/Quit", ["Yes","y","n","quit","no"])
    if option ==  0 or option  == 1:
        die = False
        play()
    else:
        playGame = False
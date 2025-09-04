##
## Name: Sean Hyatt
## Course: IT 261
## Program: Fantasy Hockey Simulator V2
##
## Description: Draft players, and compete against the computer in a virtual fantasy hockey simulation
##
## Change Log
## Date             Description
## 2023-03-05       First Draft of Program
## 2023-03-07       WelcomeMsg and CoinToss working - fix draftClass
## 2023-03-17       Finished the chooseClass function
## 2023-03-19       Finished DisplayClass function - need to figure out how the drafting process is going to go
## 2023-03-29       Working on humanDraft and compDraft
## 2023-03-29       humanDraft working - find a better way to display remaining players
## 2023-03-29              - mainDraft not working
## 2023-03-29              - compDraft almost done - make sure they can't draft two goalies?
## 2023-03-31       Working on displayAvailPlayers()
## 2023-03-31             -mainDraft still not working
## 2023-04-12       Drafting process working - fix the comp draft to draft goalie first. Then F, Then D OR: Skater (fix in file)
## 2023-04-12       Videos go in file in values - maindraft does not stop
## 2023-04-16       See list for problems - calculateHumanFP() - working EXCEPT FOR GOALIES
## 2023-04-17       Drafting Process working - including goalies - need videos and fix calcStats for goalies
## 2023-04-26       Working project - finish final testing and videos
#Imports:
import random
import cv2

#Initilizing Variable:
classDict = {}
humanRoster = {}
compRoster = {}
goalieDict = {}
skaterDict = {}
whichClass = ''


#Display Welcome Message and explain Rules:
def welcomeMsg():
    print('\nWelcome to the Fantasy Hockey Simulator V2!')
    print('\nWe\'ll start with a coin toss, to decide who drafts first!')
    print('\nYou will draft back and forth with the computer based on the given draft class!')
    print('\nAfter drafting, the results will be displayed based on your players stats throughout the week.')
    print('\nGoal = 4 Fantasy Points, Assist = 3 FP, SOG = 1 FP, PIM = - 1 FP')
    print('\nFor Goalies, Saves = 0.5 FP, Goals Against: -1 FP, Wins = 3 FP, Losses = -2 FP\n')

#Flip a coin at random to determine who goes first:
def coinToss():
    #Initialize Variables
    winner = ''
    playerChoice = ''
    coinTossTxtH = ''
    coinTossTxtT = ''

    isValidChoice = False

    #While Loop to validate coin flip choice:
    while isValidChoice == False:
        coinChoice = input('\nHeads or Tails? (H for heads, T for tails): ')
        coinChoice = coinChoice.upper()
        if coinChoice == 'H':
            playerChoice = 'Heads'
            isValidChoice = True
        elif coinChoice == 'T':
            playerChoice = 'Tails'
            isValidChoice = True
        else:
            print('\nPlease Enter a valid choice!')

    #Random Coin Flip Result (1 = heads 2 = tails):
    coinResult = random.randint(1,2)
    if coinResult == 1:
        coinTossTxtH = 'Heads'
    else:
        coinTossTxtT = 'Tails'

    #Determine the Winner and display results to user:
    if playerChoice == coinTossTxtH:
        print('\nCongrats, You won the coin toss, You draft first!')
        print('_____________________________________________________')
        winner = 'Human'
    elif playerChoice == coinTossTxtT:
        print('\nCongrats, You won the coin toss, You draft first!')
        print('_____________________________________________________')
        winner = 'Human'
    else:
        print('\nSorry, you lost the coin toss, the computer will draft first!')
        print('______________________________________________________________')
        winner = 'Computer'

    return winner

def chooseClass():
    #Allow the user to choose which draft class to play with:

    #Display Choices of Draft Classes:
    print('\nDraft Class Options:')
    print('\n\tCurrent Stars Draft Class (1)')
    print('\n\tHockey Hall of Fame Draft Class (2)')

    #Validation Loop to choose and determine which file to open :
    isValidChoice = False
    while isValidChoice == False:
        userClassChoice = input('\nPlease choose the number for the draft class you\'d like to use: (1 or 2)')
        if userClassChoice == '1':
            classChoice = 'Current'
            print('\nYou have chosen the Current Stars Draft Class!')
            print('______________________________________________________________')
            isValidChoice = True
        elif userClassChoice == '2':
            classChoice = 'HHOF'
            print('\nYou have chosen the Hockey Hall of Fame Draft Class!')
            print('______________________________________________________________')
            isValidChoice = True
        else:
            print('INVALID Choice! (1 or 2)')

    return classChoice

def createDict(classChoice):
    # Function takes whichClass as input, and outputs the roster for chosen class:
    global classDict, goalieDict, skaterDict

    #Check which Class
    if classChoice == 'Current':
        classDataFile = open('Current Stars Class.txt', 'r')
    else:
        classDataFile = open('HHOF Class.txt', 'r')

    drafClassRecord = classDataFile.readline()
    print('\n')
    #Put class into Dictionary and display:
    while drafClassRecord != '':
        classReformatted =  drafClassRecord.rstrip('\n')
        classList = classReformatted.split(',')
        classDictKey = classList[0]
        classDictValue = classList[1:]
        classDict[classDictKey] = classDictValue
        if classDictValue[1] == 'G':
            goalieDict[classDictKey] = classDictValue
        else:
            skaterDict[classDictKey] = classDictValue

        drafClassRecord = classDataFile.readline()

def humanDraft():
    #Draft process for human player:

    global classDict, humanRoster, compRoster

    #Logic to draft goalie first
    if len(humanRoster) == 0:
        displayAvailPlayers('G')
    else:
        displayAvailPlayers('S')

    #Data Validation for drafting
    isValid = False

    while isValid == False:
        #Select Player
        playerChoice = input('\nPlease Draft the player by typing their number: ')

        #Check to see if they drafted a key
        if playerChoice in classDict.keys():

            #Display player and call video function:
            print('\nThe player you drafted was:',classDict[playerChoice][0] )
            video = cv2.VideoCapture(classDict[playerChoice][-1])
            playVideo(video)

            #Add Player to human roster
            humanRoster[playerChoice] = classDict[playerChoice]
            isValid = True
        else:
            print('INVLALID CHOICE: Please Draft based on the player number')
            isValid = False

def playVideo(video):
#Function displays a highlight video for a player drafted by the human
    clicked = False

    def onMouse(event, x, y, flags, param):
        global clicked
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True

    cv2.namedWindow('Player Video')
    cv2.setMouseCallback('Player Video', onMouse)

    print('Showing player video. Click window or press any key to stop.')
    success, frame = video.read()
    while cv2.waitKey(25) == -1 and not clicked:
        if frame is not None:
            cv2.imshow('Player Video', frame)
        success, frame = video.read()

    cv2.destroyWindow('Player Video')

def compDraft():
    #Draft Process for computer Player:
    global compRoster, classDict, humanRoster, goalieDict, skaterDict, rndPlayerNbr

    #Logic to draft goalie first
    if len(compRoster) == 0:
        availGoalies = []
        #Find available goalies and put into list to choose from
        for k,v in goalieDict.items():
            if k not in humanRoster.keys() and k not in compRoster.keys():
                availGoalies.append(k)
                #Choose random number for goalie
                rndPlayerNbr = random.choice(availGoalies)
    #After 1st round select random:
    else:
        availableSkaters = []
        for k,v in skaterDict.items():
            if k not in humanRoster.keys() and k not in compRoster.keys():
                availableSkaters.append(k)
                rndPlayerNbr = random.choice(availableSkaters)


    print('\nThe player the computer drafted was:', classDict[rndPlayerNbr][0])
    #Add player to comp roster
    compRoster[rndPlayerNbr] = classDict[rndPlayerNbr]
    print('______________________________________________________________')

def mainDraft():
    #Driving function of the draft
    global classDict, humanRoster, compRoster

    #Make list of Available players to run loop:
    availablePlayers = []
    for k, v in classDict.items():
        if k not in humanRoster.keys() and k not in compRoster.keys():
            availablePlayers.append(k)

    #Loop until no more players to draft - determine drafting order:
    while len(availablePlayers) > 0:
        if firstDrafter == 'Human':
            humanDraft()
            compDraft()
        else:
            compDraft()
            humanDraft()

        availablePlayers = []
        for k, v in classDict.items():
            if k not in humanRoster.keys() and k not in compRoster.keys():
                availablePlayers.append(k)

def displayAvailPlayers(position):
    #Display all available players to draft from based on postition (G or S):

    global classDict, humanRoster, compRoster, goalieDict
    #print('______________________________________________________________')
    #Logic to determine what to display:
    if position == 'G':
        for key, value in goalieDict.items():
            if key not in humanRoster.keys() and key not in compRoster.keys():
                print(key, value[0])
    elif position == 'S':
        for key, value in skaterDict.items():
            if key not in humanRoster.keys() and key not in compRoster.keys():
                print(key, value[0])
    else:
        # never get here
        print('ERROR: Incorrect Position')


def displayHumanRoster():
    #Displays the drafted human roster and their positions
    print('\nHere is the roster you drafted!: ')
    for key, value in humanRoster.items():
        print('\t',key, value[0], '('+ value[1] + ')')

def displayCompRoster():
    #Displays the drafted comp roster and their postitions
    print('\nHere is the roster the computer drafted!: ')
    for key, value in compRoster.items():
        print('\t', key, value[0], '(' + value[1] + ')')

def calculateHumanFP():
    #Calculates number of fantasy points based on stats:

    totalHFP = 0
    print('\n\n Human Roster Individual Fantasy Points:')
    #Assign variables based on roster:
    for key, value in humanRoster.items():
        #Goalie Stats logic:
        if value[1] == 'G':
            pName = value[0]
            saves = int(value[2])
            goalsAgainst = int(value[3])
            wins = int(value[4])
            loss = int(value[5])

            # Formula to calculate individual fantasy points:
            indP = (saves * 0.5) + (goalsAgainst * -1) + (wins * 3) + (loss * -2)

            # Display results:
            print('\n\t', pName)
            print('\tIndividual Points: ', indP)

            # Update total:
            totalHFP += indP
        else:
            #Player logic
            pName = value[0]
            goals = int(value[2])
            assists = int(value[3])
            sog = int(value[4])
            pim = int(value[5])

            #Formula to calculate individual fantasy points:
            indP = (goals * 4) + (assists * 3) + (sog * 1) + (pim * -1)

            #Display results:
            print('\n\t', pName)
            print('\tIndividual Points: ', indP)

            #Update total:
            totalHFP += indP

    #Display total fantasy points:
    print('\nYour roster\'s total fantasy points: ', totalHFP)

    return totalHFP

def calculateCompFP():
    # Goalie Stats logic:

    totalCFP = 0
    print('\n\n Computer Roster Individual Fantasy Points:')
    # Assign variables based on roster:
    for key, value in compRoster.items():
        # Goalie Stats logic:
        if value[1] == 'G':
            pName = value[0]
            saves = int(value[2])
            goalsAgainst = int(value[3])
            wins = int(value[4])
            loss = int(value[5])

            # Formula to calculate individual fantasy points:
            indP = (saves * 0.5) + (goalsAgainst * -1) + (wins * 3) + (loss * -2)

            # Display results:
            print('\n\t', pName)
            print('\tIndividual Points: ', indP)

            # Update total:
            totalCFP += indP
        else:
            pName = value[0]
            goals = int(value[2])
            assists = int(value[3])
            sog = int(value[4])
            pim = int(value[5])

            # Formula to calculate individual fantasy points:
            indP = (goals * 4) + (assists * 3) + (sog * 1) + (pim * -1)

            # Display results:
            print('\n\t', pName)
            print('\tIndividual Points: ', indP)

            # Update total:
            totalCFP += indP

    # Display total fantasy points:
    print('\nComputer roster\'s total fantasy points: ', totalCFP)

    return totalCFP

def displayWinner(humanScore, compScore):
    # Determine winner based on scores and display to user
    print('\n\nBelow are the Final Team Results:')
    print('\n\tHuman Roster Fantasy Points:', humanScore)
    print('\tComputer Roster Fantasy Points:', compScore)

    if humanScore == compScore:
        print('\nClose one! It\'s a Tie!')
    elif humanScore > compScore:
        print('\nCongratulations! You Beat the Computer! Nice Drafting!')
    else:
        print('\nDarn! The Computer Beat You!')

def main():
    #Driving fuction of the program:

    global whichClass, firstDrafter
    welcomeMsg()
    firstDrafter = coinToss()
    whichClass = chooseClass()
    createDict(whichClass)
    mainDraft()
    displayHumanRoster()
    displayCompRoster()
    humanScore = calculateHumanFP()
    compScore = calculateCompFP()
    displayWinner(humanScore,compScore)



main()
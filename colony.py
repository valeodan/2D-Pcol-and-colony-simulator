import random

class Colony:
    def __init__(self, environment, agents, jokerSymbols):
        self.envMatrix = environment['matrix']
        self.rowsEnv = len(self.envMatrix)
        self.colsEnv = len(self.envMatrix[0])
        self.envRules = environment['rules']
        self.numAgents = len(agents)
        self.toConcat2env = []
        self.jokerSymbols = jokerSymbols
        self.agent = [self.Agent(self, agents[i]['id'], agents[i]['contents'], agents[i]['programs'], agents[i]['coordinates'], jokerSymbols) for i in range(self.numAgents)]
        self.log = []

    def initComputationalStep(self):
        self.toConcat2env = []

    def getApplicableRules(self, i, j):
        contents = self.envMatrix[i][j][:]
        applicableRules = []
        for rule in self.envRules:
            allSymbols = 1
            for symbol in rule['left']:
                if symbol in contents:
                    #contents.remove(symbol) #Fixed - Env symbol cant be removed here
                    allSymbols = 1
                else:
                    allSymbols = 0
                    break
            if allSymbols:
                applicableRules.append(rule)
        return applicableRules

    def evolveEnvironmet(self):
        for i in range(1, self.rowsEnv):
            for j in range(1, self.colsEnv):
                applicableRules = self.getApplicableRules(i, j)
                if applicableRules:
                    cell = self.envMatrix[i][j]
                    applyRule = applicableRules[random.randrange(len(applicableRules))]
                    for symbol in applyRule['left']:
                        cell.remove(symbol)
                    cell = cell + applyRule['right']
                    self.envMatrix[i][j] = cell

    def add2environment(self):
        for element in self.toConcat2env:
            SymToAdd=element['symbol']
            if not self.envMatrix[element['position']['i']][element['position']['j']]: #FIXED - symbol must be in array 
                self.envMatrix[element['position']['i']][element['position']['j']] = [SymToAdd]
            else:
                self.envMatrix[element['position']['i']][element['position']['j']].append(SymToAdd)

    def agentsAct(self):
        # generate a set of applicable programs for each agent
        for i in range(self.numAgents):
            self.agent[i].getApplicablePrograms()
        # random order of agents
        # set a list of indexes of the agents
        agentIndexList = [i for i in range(self.numAgents)]
        while agentIndexList:
            #choose a random index of the agent
            agentIndex = agentIndexList.pop(random.randrange(len(agentIndexList)))
            self.agent[agentIndex].applyRandomProgram()

    def colonyStep(self):
        self.initComputationalStep()
        self.agentsAct()
        self.evolveEnvironmet()
        self.add2environment()

    class Agent:
        def __init__(self, col, agentId, contents, programs, coordinates, jokerSymbols):
            self.agentId = agentId
            self.contents = contents
            self.programs = programs
            self.coordinates = coordinates
            self.vicinityLength = 9
            self.colony = col
            self.jokerSymbols = jokerSymbols
            self.applicablePrograms = []

        def getVicinity(self):
            vicinity = []
            for i in range(self.coordinates['i'] - 1, self.coordinates['i'] + 2):
                for j in range(self.coordinates['j'] - 1, self.coordinates['j'] + 2):
                    try:
                        if (self.colony.envMatrix[i][j]): #FIXED - value must be 2D even if it is empty (otherwise the application crashes)
                            vicinity.append(self.colony.envMatrix[i][j])
                        else:
                            vicinity.append(["",""])
                    except:
                        vicinity.append(["",""])
            return vicinity

        def getEnvironmentContent(self):
            return self.colony.envMatrix[self.coordinates['i']][self.coordinates['j']]

        def isProgramApplicable(self, program):
            allRulesAplicable = 1
            innerObjects = self.contents[:]
            envContent = self.getEnvironmentContent()[:]
            envSymbol = "e"
            if not envContent: #Agent out of environment
                envContent=[""] #Fix of app crashing
                envSymbol = ""
            for rule in program:
                # get a type of the rule
                # motion
                print ("innerObjects:", innerObjects, "\nenvContent:", envContent)
                if rule['operator'] in ['u', 'd', 'r', 'l']:
                    vicinity = self.getVicinity()
                    for i in range(self.vicinityLength):
                        if rule['left'][i] in self.jokerSymbols.keys():
                            # joker symbol - at least one of the symbol must be in the environment
                            jokerNotInEnv = True
                            for jokerItem in self.jokerSymbols[rule['left'][i]]: ##Is 'in' OK here? 
                                print("jokerItem",jokerItem, type(jokerItem), ">>vicinity::", vicinity)
                                if jokerItem in (vicinity[i] + [envSymbol]):
                                    jokerNotInEnv = False
                            if jokerNotInEnv:
                                allRulesAplicable=0
                                break
                        else:
                            print ("rule['left'][i]:::", rule['left'][i], "vicinity[i]:::", vicinity[i]+[envSymbol])
                            if not (rule['left'][i] in (vicinity[i] + [envSymbol])):
                                allRulesAplicable = 0
                                break
                # evolving
                elif (rule['operator'] == '>'):
                    if (rule['left'] in innerObjects):
                        innerObjects.remove(rule['left'])
                        # innerObjects += rule['right'] #can I develop and exchange the developped object in one program?
                    else:
                        allRulesAplicable = 0
                # exchange
                elif (rule['operator'] == '<>'):
                    if (rule['left'] in innerObjects) and (rule['right'] in envContent + ['e']):
                        innerObjects.remove(rule['left'])
                        if rule['right'] != 'e':
                            envContent.remove(rule['right'])
                        # innerObjects += rule['right'] # can I exchange and develop exchanged object in one program?
                    else:
                        allRulesAplicable = 0
            return allRulesAplicable

        def getApplicablePrograms(self):
            self.applicablePrograms = []
            for program in self.programs:
                if self.isProgramApplicable(program):
                    self.applicablePrograms.append(program)
            print(self.agentId, ' ', self.applicablePrograms)

        def applyRandomProgram(self):
            if self.applicablePrograms:
                program = self.applicablePrograms[random.randrange(len(self.applicablePrograms))]
                if self.isProgramApplicable(program):
                    for rule in program:
                        # get a type of the rule
                        # motion
                        if rule['operator'] == 'u':
                            self.coordinates['i'] -= 1
                        elif rule['operator'] == 'd':
                            self.coordinates['i'] += 1
                        elif rule['operator'] == 'l':
                            self.coordinates['j'] -= 1
                        elif rule['operator'] == 'r':
                            self.coordinates['j'] += 1
                        # evolving
                        elif rule['operator'] == '>':
                            self.contents.remove(rule['left'])
                            self.contents += rule['right']
                        # exchange
                        elif rule['operator'] == '<>':
                            self.contents.remove(rule['left'])
                            self.contents += rule['right']
                            if rule['right'] != 'e':
                                self.colony.envMatrix[self.coordinates['i']][self.coordinates['j']].remove(rule['right'])
                            SymToEnv=rule['left']
                            insert2env = {
                                'position':self.coordinates,
                                'symbol':SymToEnv
                            }
                            self.colony.toConcat2env.append(insert2env)


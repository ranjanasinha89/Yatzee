#!/usr/bin/env python
# gameofchance.py - implementation of the game Yatzee to find the next best roll
# Ranjana, Sun, October 14, 2018

import sys

def multProbExpectedOutcome(a,b,c, x):
    #x denotes how many powers 6 needs to be raised to. 
    if (a == b and b == c):
        return(float(25/6**x))
    else:
        return(float((a+b+c)/6**x))

def getValuesAndParameters(option):
    # extracts the keys and values from the dictionaries and returns as list
    usedParameters = []
    values = []

    for k, v in option.items():
        usedParameters.append(k)
        values.append(v)

    return usedParameters, values

def calculateExpectation(option):
    state = {'a', 'b', 'c'} # All the dices'
    if len(option) == 3:
        # This is the case when we have all the dices'. So we will calculate the expectation if none of them are rolled.
        expectation = 0
        
        usedParameters, values = getValuesAndParameters(option)

        a = values[0]
        b = values[1]
        c = values[2]

        expectation = a+b+c
        return expectation, "none"
    elif len(option) == 2:
        # This is the case when we have any two of the dices'. So we will calculate the expectation if the third one was rolled.
        expectation = 0
        retString = ''

        usedParameters, values = getValuesAndParameters(option)

        a = values[0]
        b = values[1]

        for c in range(1, 7):
            expectation = expectation + multProbExpectedOutcome(a, b, c, (3-len(option)))

        for v in usedParameters:
            state.remove(v)  # keep the one that was rolled
        retString = ','.join(state)
            
        return expectation, retString
    elif len(option) == 1:
        # This is the case when we have either one dice or no dice.
        if option == {0}:
            # This is the case when have no dices'. So we should calculate expectation if all the three are rolled. 
            expectation = 0
            for a in range(1,7):
                for b in range(1,7):
                    for c in range(1,7):
                        expectation = expectation + multProbExpectedOutcome(a, b, c, (3))
            return expectation, "all" 
        else:
            # This is the case when we have one dice. We we should calculate the expectation if the other two are rolled.
            expectation = 0
            retString = ''

            usedParameters, values = getValuesAndParameters(option)

            a = values[0]

            for b in range(1, 7):
                for c in range(1, 7):
                    expectation = expectation + multProbExpectedOutcome(a, b, c, (3-len(option)))

            for v in usedParameters:
                state.remove(v)   # keep the ones that were rolled
            retString = ','.join(state)

            return expectation, retString                

def gameOfChance(a,b,c):
    if(a == b == c):
        print("Optimal Solution - No need to change")
    else:
        #Divided the dice into eight dictionary so that we can calulate the expectation for all.
        #The first dictionary has all the three digits, that means that will help calculate the expectation
        #of the case, where we do not roll any of the dice. The last one has {0}, which will help calculate the probability 
        #if all the dices' are rolled.

        #Options can be thought of as the fringe.
        options = [{"a": a, "b": b,"c": c},{"a":a,"b":b},{"b":b,"c":c},{"a":a,"c":c},{"a":a},{"b":b},{"c":c},{0}]

        #The expectationDict holds the expectation for all the eight cases. The key is the rolled dices' and the value is the expectation.
        expectationDict = {} 

        while(len(options) > 0):
            expectation, state = calculateExpectation(options.pop())
            expectationDict[state] = expectation
            
        # find out the maximum value from the dictionary and print its key.
        key = max(expectationDict, key=expectationDict.get)
        output = "try to roll " + key
        print(output)  

num_arg = len(sys.argv)

if num_arg < 4:
    print("Please input three numbers ranging from 1 to 6.")

else:
    if num_arg > 4:
        print("We shall consider the first 3 digits.")

    for i in range(1, 4):
        if int(sys.argv[i]) > 6 or int(sys.argv[i]) < 0:
            print("Please input digits from 1 to 6")

    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

gameOfChance(a,b,c)




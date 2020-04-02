import sys
import csv
import itertools 
import re
import math

#Ava Chong
#Datascience Assignment #3

#variables 
input_data = []
itemsets = [] 
frequent_itemset = []
frequent_itemset_unformated = []
association_rules = []
rule_pairs = []

def readFromFile(input_filename):
    with open(input_filename) as f:
        input = csv.reader(f)
        #read line by line
        for row in input:
            r = row
            for col in range(0, len(r)):
                r[col] = str(r[col]).strip()

            r.pop(0)
            r.sort()
            input_data.append(r)
            #find all combinations for each row recursively 
            for value in range(0, len(r)):
                list = [ ]
                comboFinder(r, list, 0)

    itemsets.sort()
    itemsets.sort(key=len)
    #for groups in itemsets:
        #print(groups)

def writeToCSV(output_filename):
    #write to file
    with open(output_filename, "a", newline='') as file:
        writer = csv.writer(file)
        for sub in frequent_itemset:
            writer.writerow(sub)
        for role in association_rules:
            writer.writerow(role)

def comboFinder(row, base, start):
    if (start < len(row)):
        for iterate in range(start, len(row)):
            newCombination = base.copy()
            newCombination.append(row[iterate])
            #check if combination has already been seen
            if (checkMatch(newCombination) == False):
                itemsets.append(newCombination)
            #call again = recursive
            comboFinder(row, newCombination, iterate+1)

def frequencyFinder(min_support_percentage):
    count = len(input_data)
    for subset in itemsets:
        frequencyCount = 0
        for row in input_data:
            if (len(row) >= len(subset)):
                #count how many times combo is found using .issubset
                if (set(subset).issubset(set(row))):
                    frequencyCount = frequencyCount + 1
        #calculate support percentage 
        support_percentage = frequencyCount/count
        if(support_percentage >= min_support_percentage):
            formated = ["S", "{:.4f}".format(support_percentage)]
            for iterate in range(0, len(subset)):
                formated.append(str(subset[iterate]))
            frequent_itemset.append(formated)
            frequent_itemset_unformated.append([subset, support_percentage])

def calculateConfidence(min_confidence):
    for item in frequent_itemset_unformated:
        if (len(item[0]) > 1):
            associationRules(item[1], [], item[0], min_confidence)

def associationRules(full_prob, left, right, min_confidence):
    if(len(right) > 1):
        for element in range(0, len(right)):
            #create new lists to modify and sort
            leftRule = left.copy()
            rightRule = right.copy()
            leftRule.append(right[element])
            rightRule.pop(element)
            leftRule.sort()
            rightRule.sort()
            #check if we have rule with these pairs
            if(checkRule(leftRule, rightRule) == False):
                #if a new rule, fine probabilities
                left_prob = getProbability(leftRule)
                confidence = full_prob/left_prob
                #before adding, make sure rule exceeds min confidence
                if(min_confidence <= confidence):
                    rule = ["R", "{:.4f}".format(full_prob), "{:.4f}".format(confidence)]
                    for left_elem in leftRule:
                        rule.append(str(left_elem))
                    rule.append("'=>'")
                    for right_elem in rightRule:
                        rule.append(str(right_elem))
                    association_rules.append(rule)
                    rule_pairs.append([leftRule, rightRule])
                associationRules(full_prob, leftRule, rightRule, min_confidence)

def checkRule(left, right):
    #checks to see if rule has been made with the pairs
    for rule in rule_pairs:
        if(rule[0] == left):
            if(rule[1] == right):
                return True
    return False

def checkMatch(combo):
    for item in itemsets:
        if (item == combo):
            return True
    return False

def getProbability(find_this):
    for item in frequent_itemset_unformated:
        if (item[0] == find_this):
            return item[1]
    return 0

if __name__ == "__main__":
    #commande line arguments
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    min_support_percentage = float(sys.argv[3])
    min_confidence = float(sys.argv[4])

    #call functions
    readFromFile(input_filename)
    frequencyFinder(min_support_percentage)
    calculateConfidence(min_confidence)
    writeToCSV(output_filename)
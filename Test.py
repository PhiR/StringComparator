import difflib

def stringmatch(string1, string2):
    #Check if string1 and string2 are included in each other, return 1 if they are
    # words = string1.split()
    # for word in words:
    #     if word in string2 and len(word)>1:
    #         return 1
    if len(string1)==0 or len(string2)==0:
        return 0
    if string1 in string2:
        return 1
    if string2 in string1:
        return 1
    #otherwise return the difference between them
    return difflib.SequenceMatcher(None, string1, string2).ratio()

#-------------------------------------------
print(stringmatch('Aix', 'Aix en Provence'))
print(stringmatch('Le plesis', ''))
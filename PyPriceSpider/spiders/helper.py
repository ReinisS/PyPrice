import scrapy

def parseString(string):
    
    string = string.extract_first()

    if string:

        string = string.strip()

        if string[0] == '$':
            string = string[1:]

    return string
from difflib import *
import requests
from bs4 import BeautifulSoup
from google import search
import time


# Open file and return string
def gettext(filename):
    with open(filename) as file:
        return file.read()


# Splits our query into multiple arrays
def split(toSplit, num):
    return [toSplit[start:start + num] for start in range(0, len(toSplit), num)]

fileCompared = "toread.txt"

queryNum = 0
bestMatch = 0
bestLink = ""
linkScores = {}

textData = gettext(fileCompared)
toRead = textData
toRead = ' '.join(toRead.split())

# Remove extra whitepsace and newlines
textData = textData.replace('\\n', '')
textData = ' '.join(textData.split())
# Split data, as google only accepts querys of 32 words or less
textData = split(textData, 250)


# Loop through each query
for line in textData:
    queryNum += 1
    print("")

    deltaTime = time.time()
    print("Searching for query number " + str(queryNum))
    urls = []
    # This is where we search google for the urls
    for url in search('"' + line + '"', stop=3, num=3):
        urls.append(url)
        time.sleep(1)  # Avoid google detecting our bot
    if len(urls) == 0:
        print("No results found")
        continue
    print("Search completed in " + str(round(time.time() - deltaTime, 2)) + " seconds, beginning comparison")

    deltaTime = time.time()
    # Now we process each url
    for url in urls:
        # Optimze popular websites for text
        elementsToSearch = {}
        if "stackoverflow" in url:
            elementsToSearch = {"code"}
        elif "gist.github.com" in url:
            elementsToSearch = {"tbody", "tr"}
        else:
            elementsToSearch = {"p", "code", "li", "b", "u", "i"}
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        toCompare = ""
        # Search the DOM for certain elements, and extract that text
        for element in elementsToSearch:
            for node in soup.findAll(element):
                toCompare += ''.join(node.findAll(text=True))
        toCompare = ' '.join(toCompare.split())
        # Compare ratios
        s = SequenceMatcher(None, toRead, toCompare)
        sim = s.ratio() * 100
        if sim > bestMatch:
            bestMatch = sim
            bestLink = url
        if url not in linkScores:
            linkScores[url] = 1
        else:
            linkScores[url] += 1
        print(str(round(sim, 2)) + "% match at: " + url)
    print("Comparison completed in " + str(round(time.time() - deltaTime, 2)) + " seconds.")
    print("")


bestMatch *= 2
if bestMatch > 100:
    print("OBVIOUS plagiarism detected with a near 100% confidence.")
elif bestMatch > 60:
    print("LIKELY plagiarism detected with a " + str(round(bestMatch, 2)) + "% confidence.")
elif bestMatch > 30:
    print("POSSIBLE plagiarism detected with a " + str(round(bestMatch, 2)) + "% confidence.")
else:
    print("No plagiarism detected. Only a " + str(round(bestMatch, 2)) + "% confidence.")
print("Most similar: " + bestLink)
linkScores = sorted(linkScores, key=linkScores.get, reverse=True)
print("___Top sites___")
try:
    print("#1 " + linkScores[0])
    print("#2 " + linkScores[1])
    print("#3 " + linkScores[2])
except IndexError:
    pass

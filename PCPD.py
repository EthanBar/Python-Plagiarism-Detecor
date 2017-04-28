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

queryNum = 0
bestMatch = 0
bestLink = ""
linkScores = {}
textData = ""
fileCompared = "toread.txt"

with open(fileCompared) as f:
    for line in f:
        textData += line
textData = textData.replace('\\n', '')
textData = ' '.join(textData.split())

textData = split(textData, 150)
print(textData)
print(len(textData))

text = gettext(fileCompared)
text = ' '.join(text.split())

for line in textData:
    queryNum += 1
    print("")
    deltaTime = time.time()
    print("Searching for query number " + str(queryNum))
    urls = []
    for url in search('"' + line + '"', stop=3, num=3):
        urls.append(url)
        time.sleep(1)
    print("Search completed in " + str(round(time.time() - deltaTime, 2)) + " seconds, beginning comparison")
    deltaTime = time.time()
    if len(urls) == 0:
        print("No results found")
        continue

    for url in urls:
        elementsToSearch = {}
        if "stackoverflow" in url:
            elementsToSearch = {"code"}
        else:
            elementsToSearch = {"p", "code", "li"}
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        # toCompare = soup.get_text()
        toCompare = ""
        for element in elementsToSearch:
            for node in soup.findAll(element):
                toCompare += ''.join(node.findAll(text=True))
        toCompare = ' '.join(toCompare.split())
        s = SequenceMatcher(None, text, toCompare)
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
print("#1 " + linkScores[0])
print("#2 " + linkScores[1])
print("#3 " + linkScores[2])
# text3 = urllib.request.urlopen("https://en.wikipedia.org/wiki/Coding").read()
# text = """
# example slightly different stuff here
# """
#
# text2 = """
# example slightly different text stuff here
# """
# d = difflib.Differ()
# diff = d.compare(text, text2)

# text3 = soup.get_text()
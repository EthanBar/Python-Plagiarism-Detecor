from difflib import *
import requests
from bs4 import BeautifulSoup
import scrapy
from google import search
import time

def getText(filename):
    with open(filename) as file:
        return file.read()

urlData = {}
deltaTime = time.time()
print("Searching for query...")
urls = []
for url in search('How does the map() function in Processing work?', stop=10):
    urls.append(url)
print("Search completed in " + str(round(time.time() - deltaTime, 2)) + " seconds, beginning comparison")

deltaTime = time.time()
text = getText("toread.txt")
text = ' '.join(text.split())
bestMatch = 0
bestLink = ""
soElments = {"code"}

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
    print(str(round(sim, 2)) + "% match at: " + url)
print("Comparison completed in " + str(round(time.time() - deltaTime, 2)) + " seconds.")
print("")

bestMatch *= 2
if bestMatch > 100:
    print("OBVIOUS plagiarism detected with a near 100% confidence.")
    print(bestLink)
elif bestMatch > 60:
    print("LIKELY plagiarism detected with a " + str(round(bestMatch, 2)) + "% confidence.")
    print(bestLink)
elif bestMatch > 30:
    print("POSSIBLE plagiarism detected with a " + str(round(bestMatch, 2)) + "% confidence.")
    print(bestLink)
else:
    print("No plagiarism detected. Only a " + str(round(bestMatch, 2)) + "% confidence.")
    print(bestLink)

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
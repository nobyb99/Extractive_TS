from heapq import nlargest
import spacy
import math
# import stop words
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en_core_web_sm')

# stop words
sw = list(STOP_WORDS)


punct = {',', '.', '!'}


def compressor(txt, num):
    story = txt.split(' ')

    doc = nlp(txt)

    # dictionary to hold non-stop words and their frequency

    word_nsw = {}

    for token in doc:
        if token.text not in sw and token.text not in punct:
            if token.text.lower() not in word_nsw.keys():
                word_nsw[token.text.lower()] = 1
            else:
                word_nsw[token.text.lower()] += 1

    # assigning weights to every word by finding most occuring one and assign weights with reference to that

    # find highest frequency non stop word

    highest = max(word_nsw.values())

    # modify weights by division

    for word in word_nsw.keys():
        word_nsw[word] = word_nsw[word] / highest

    # sentence scores

    # create a list of all sentences
    sent_list = [sentence for sentence in doc.sents]

    # create a dictionary to hold sentence and weight pair

    sent_score = {}

    for sent in sent_list:
        for word in sent:
            if word.text.lower() in word_nsw.keys():
                if len(sent.text.split(' ')) < 35:
                    if (sent not in sent_score.keys()):
                        sent_score[sent] = word_nsw[word.text.lower()]
                    else:
                        sent_score[sent] += word_nsw[word.text.lower()]

    # heapq creates a heap and adds element........specialty of a heap is a[0] is always the smallest...so heapq automatically sorts it
    # nlargest has a reverse as true.......meaning a[0] will be the highest

    # nlargest takes (size,iterable[list],key value,optional ,reverse-optional)

    summary = nlargest(num, sent_score, key=sent_score.get)

    # convert contents of list from token span to string

    final = [words.text for words in summary]

    # join the sentences

    output = ' '.join(final)
    return output, len(story), len(output.split(' '))

import string
import nltk
from nltk.stem import *
import os


# TODO: DONE
def stripper(sentence):
    func_pos = ['CD', 'DT', 'EX', 'IN', 'LS', 'POS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'RP', 'TO', 'WDT',
                'WP', 'WRB', 'WP$', '.', ',', '(', ')', ':', ';', '"', "'", '$', '#']
    sentence = nltk.word_tokenize(sentence)
    pos_sent = nltk.pos_tag(sentence)

    stripped_sentence = ''
    for current in pos_sent:
        if(current[1] not in func_pos):
            ps = PorterStemmer()
            word = ps.stem(current[0])
            stripped_sentence += word + " "

    return stripped_sentence


# TODO: DONE
def sentLexicon():
    lexicon = {}

    file = open('../Data_Sets/SentiWordNet_Lexicon/SentiWordNet_3.0.0.txt', 'r')
    data = file.read().split('\n')

    for line in data:
        current = line.split('\t')
        words = current[4].split(' ')
        for word in words:
            word = word.strip(string.digits)
            word = word.strip('#')
            if(word not in lexicon):
                lexicon[word] = {"POS": float(current[2]), "NEG": float(current[3])}
            else:
                currPOS = float(current[2])
                currNEG = float(current[3])
                prevPOS = lexicon[word]["POS"]
                prevNEG = lexicon[word]["NEG"]
                avgPOS = (currPOS + prevPOS)/2
                avgNEG = (currNEG + prevNEG)/2
                lexicon[word] = {"POS": avgPOS, "NEG": avgNEG}

    file.close()

    return lexicon


# TODO: DONE
def testCorpus(corpus, sentiment):
    path = '../Data_Sets/IMDB_Corpuses/' + corpus + '/' + sentiment
    sentences = []

    for filename in os.listdir(path):
        file = open('../Data_Sets/IMDB_Corpuses/' + corpus + '/' + sentiment + '/' + filename, 'r')
        data = file.read()
        sentences.append(data)
        file.close()
    return sentences

# TODO: WIP
def OOV(word):
    return 0, 0


# TODO: DONE
def articleScore(sentence, lexicon):
    sentence_POS = 0
    sentence_NEG = 0

    neg_words = ["n't", 'no', 'not', 'none', 'no one', 'nobody', 'nothing', 'neither', 'nowhere', 'never', '', '', '', '', '', '', '', '']

    words = sentence.split(' ')
    for i in range(len(words)):

        # previous word
        if(i != 0):
            prev_word = words[i - 1].lower()
        else:
            prev_word = None

        # negation words
        if(prev_word == None):
            negation = False
        else:
            if(prev_word in neg_words):
                negation = True
            else:
                negation = False

        # check intensity
        if(prev_word != None):
            if(('ly' == prev_word[-2:]) or (prev_word == 'very')):
                intensity = True
            else:
                intensity = False
        else:
            intensity = False

        # pos/neg sores
        word = words[i].lower()
        if(word in lexicon):
            if(negation == True):
                word_POS = lexicon[word]['NEG']
                word_NEG = lexicon[word]['POS']
            else:
                word_POS = lexicon[word]['POS']
                word_NEG = lexicon[word]['NEG']

            if(intensity == True):
                word_POS = word_POS * 1.5
                word_NEG = word_NEG * 1.5

        else:
            score_POS, score_NEG = OOV(word)
            if(negation == True):
                word_POS = score_NEG
                word_NEG = score_POS
            else:
                word_POS = score_POS
                word_NEG = score_NEG

            if(intensity == True):
                word_POS = word_POS * 1.5
                word_NEG = word_NEG * 1.5

        sentence_POS += word_POS
        sentence_NEG += word_NEG

    sentence_POS = sentence_POS/len(words)
    sentence_NEG = sentence_NEG/len(words)

    return sentence_POS, sentence_NEG


# TODO: DONE
def allScores(articles, lexicon):
    article_score = {}
    counter = 0

    for article in articles:
        sentence_POS, sentence_NEG = articleScore(article, lexicon)
        article_score[counter] = {"article": article, "POS": sentence_POS, "NEG": sentence_NEG}
        counter += 1

    return article_score

# TODO: DONE
def categorizeScores(article_scores):
    neg_scores = {}
    pos_scores = {}
    neut_scores = {}

    for article in article_scores.keys():
        if(article_scores[article]['POS'] == article_scores[article]['NEG']):
            neut_scores[article] = 0
        elif(article_scores[article]['POS'] > article_scores[article]['NEG']):
            pos_scores[article] = 1
        else:
            neg_scores[article] = -1

    return pos_scores, neg_scores, neut_scores



# TODO: WIP
def run():
    # corpus = "train" or "test"
    corpus = "train"
    # sentiment = "pos" or "neg"
    sentiment = "neg"

    # generates scores
    lexicon = sentLexicon()
    articles = testCorpus(corpus, sentiment)
    article_scores = allScores(articles, lexicon)
    pos_scores, neg_scores, neut_scores = categorizeScores(article_scores)

    total = len(articles)
    numPOS = len(pos_scores)
    numNEG = len(neg_scores)
    numNEUT = len(neut_scores)


    # display results
    print("Corpus:", corpus, " - Sentiment:", sentiment)
    print("Number of Articles:", str(total))
    print("Positive  Articles:", str(numPOS), str(numPOS/total))
    print("Negative  Articles:", str(numNEG), str(numNEG/total))
    print("Neutral   Articles:", str(numNEUT), str(numNEUT/total))


run()

import string

# TODO: DONE
def sentLexicon():
    # import lexicon annotated files and save words with scores
    lexicon = {}

    file = open('./Data_Sets/SentiWordNet_Lexicon/SentiWordNet_3.0.0.txt', 'r')
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
def OOV(word):
    # handle oov words with neutral score
    return 0, 0


# TODO: DONE
def articleScore(sentence, lexicon):
    # score articles based on average word scores
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
    # get score of all articles
    article_score = {}
    counter = 0

    for article in articles:
        sentence_POS, sentence_NEG = articleScore(article, lexicon)
        article_score[counter] = {"article": article, "POS": sentence_POS, "NEG": sentence_NEG}
        counter += 1
    return article_score


# TODO: DONE
def categorizeScores(article_dict):
    numPOS = 0
    numNEG = 0
    numNEUT = 0

    for article in article_dict.keys():
        # determine sentiment scores
        if (article_dict[article]['POS'] == article_dict[article]['NEG']):
            numNEUT += 1
        elif (article_dict[article]['POS'] > article_dict[article]['NEG']):
            numPOS += 1
        elif (article_dict[article]['NEG'] > article_dict[article]['POS']):
            numNEG += 1


    return numPOS, numNEG, numNEUT


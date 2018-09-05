import os
import nltk
import pickle

# TODO: Add training/testing data now for training
def train():
    # paths for positive and negative IMDB training sets
    pathPOS = './Data_Sets/IMDB_Corpuses/train/pos'
    pathNEG = './Data_Sets/IMDB_Corpuses/train/neg'
    articlesPOS = {}
    articlesNEG = {}

    # load positive training data
    for filename in os.listdir(pathPOS):
        file = open('./Data_Sets/IMDB_Corpuses/train/pos/' + filename, 'r')
        dataPOS = file.read()
        articlesPOS[filename] = dataPOS
        file.close()

    # load negative training data
    for filename in os.listdir(pathNEG):
        file = open('./Data_Sets/IMDB_Corpuses/train/neg/' + filename, 'r')
        dataNEG = file.read()
        articlesNEG[filename] = dataNEG
        file.close()

    # parts of speech to remove
    func_pos = ['CD', 'DT', 'EX', 'IN', 'LS', 'POS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'RP', 'TO',
                'WDT', 'WP', 'WRB', 'WP$', '.', ',', '(', ')', ':', ';', '"', "'", '$', '#']

    frequencyPOS = {}
    frequencyNEG = {}
    count = 0
    # remove function words and count frequency for positive words
    for articleName in articlesPOS.keys():
        article = nltk.word_tokenize(articlesPOS[articleName])
        posArticle = nltk.pos_tag(article)
        stripped_sentence = ''
        for current in posArticle:
            if (current[1] not in func_pos):
                stripped_sentence += current[0] + " "

        stripped_sentence = stripped_sentence.split()
        print(stripped_sentence)
        print(count)
        count += 1
        for word in stripped_sentence:
            if(word in frequencyPOS):
                frequencyPOS[word] = frequencyPOS[word] + 1
            else:
                frequencyPOS[word] = 1

    count = 0
    # remove function words and count frequency for negative words
    for articleName in articlesNEG.keys():
        article = nltk.word_tokenize(articlesNEG[articleName])
        negArticle = nltk.pos_tag(article)
        stripped_sentence = ''
        for current in negArticle:
            if (current[1] not in func_pos):
                stripped_sentence += current[0] + " "

        stripped_sentence = stripped_sentence.split()
        print(stripped_sentence)
        print(count)
        count += 1
        for word in stripped_sentence:
            if(word in frequencyNEG):
                frequencyNEG[word] = frequencyNEG[word] + 1
            else:
                frequencyNEG[word] = 1

    # output frequency files through pickle
    outFile = open('NaiveBayesFreq.pkl', 'wb')
    pickle.dump(frequencyPOS, outFile)
    pickle.dump(frequencyNEG, outFile)
    outFile.close()

    print('Finished')


# TODO: DONE
def frequency():
    # load pickled files of pre-trained frequencies
    file = open('../NaiveBayesFreq.pkl', 'rb')

    freqPOS = pickle.load(file)
    freqNEG = pickle.load(file)

    file.close()

    return freqPOS, freqNEG


# TODO: DONE
def count(freqPOS, freqNEG):
    countPOS = 0
    countNEG = 0

    # generate count for all positive words
    for key in freqPOS.keys():
        countPOS += freqPOS[key]

    # generate count for all negative words
    for key in freqNEG.keys():
        countNEG += freqNEG[key]

    # generate total count for all negative and positive words
    countPOSNEG = countPOS + countNEG

    return countPOS, countNEG, countPOSNEG


# TODO: DONE
def probability(article, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG):
    articlePOS = 0
    articleNEG = 0
    articleLength = len(article)

    # generate scores for Naive Bayes algorithm for each word
    for word in article:
        if(word in freqPOS):
            wordPOSFreq = freqPOS[word]
        else:
            wordPOSFreq = 1

        if(word in freqNEG):
            wordNEGFreq = freqNEG[word]
        else:
            wordNEGFreq = 1

        wordPOSScore = ((wordPOSFreq / countPOS) * (countPOS / countPOSNEG)) / ((wordPOSFreq + wordNEGFreq) / countPOSNEG)
        wordNEGScore = ((wordNEGFreq / countNEG) * (countNEG / countPOSNEG)) / ((wordPOSFreq + wordNEGFreq) / countPOSNEG)

        # sum all words for each article
        articlePOS += wordPOSScore
        articleNEG += wordNEGScore

    # average the article scores
    articlePOS = articlePOS / articleLength
    articleNEG = articleNEG / articleLength

    return articlePOS, articleNEG


# TODO: DONE
def run(corpus, sentiment, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG):
    # will generate results for score
    numPOS = 0
    numNEG = 0
    numNEUT = 0

    pathPOS = '../Data_Sets/IMDB_Corpuses/' + corpus + '/' + sentiment

    # read filenames from directory, open, and parse into probability
    for filename in os.listdir(pathPOS):
        file = open('../Data_Sets/IMDB_Corpuses/' + corpus + '/' + sentiment + '/' + filename, 'r')
        article = file.read().split(" ")
        articlePOS, articleNEG = probability(article, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG)
        file.close()

        # determine sentiment scores
        if(articlePOS == articleNEG):
            numNEUT += 1
        elif(articlePOS > articleNEG):
            numPOS += 1
        elif(articleNEG > articlePOS):
            numNEG += 1

    total = numPOS + numNEG + numNEUT

    # display results
    print("Corpus:", corpus, " - Sentiment:", sentiment)
    print("Number of Articles:", str(total))
    print("Positive  Articles:", str(numPOS), str(numPOS/total))
    print("Negative  Articles:", str(numNEG), str(numNEG/total))
    print("Neutral   Articles:", str(numNEUT), str(numNEUT/total))


# TODO: DONE
def main():
    #######################################
    # Training
    #######################################
    # run train to count frequencies
    # train()

    #######################################
    # Running
    #######################################
    # gather frequency and count data
    freqPOS, freqNEG = frequency()
    countPOS, countNEG, countPOSNEG = count(freqPOS, freqNEG)

    # run and generate scores for given corpus/sentiment
    # corpus = "train" or "test"
    corpus = "test"
    # sentiment = "pos" or "neg"
    sentiment = "neg"

    run(corpus, sentiment, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG)


main()
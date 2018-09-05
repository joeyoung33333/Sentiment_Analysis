import requests
import nltk
from nltk.stem import *
import Lexicon
import Naive_Bayes
import matplotlib.pyplot as plt

# TODO: Remove Lexicon Method
# TODO: Add Testing IMDB to NB training
# TODO: Add WSJ Annotated Sentiment Articles
# TODO: Implement K-Means 3D Matrix and 2D Matrix
# TODO: DONE2
def stripper(sentence):
    # strips sentence of unnecessary POS and Chars
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
def report(company, today, month, year, data, artData):
    outputData = ""
    outputData += company.title() + '\n'
    outputData += "Dates: " + month + "/1/" + year + " to " + month + "/" + today + "/" + year + "\n"
    outputData += data

    file = open("./Report/" + company + "_report.txt", "w")
    file.write(outputData)
    file.close()

    file = open("./Report/" + company + "_articles.txt", "w")
    file.write(artData)
    file.close()


# TODO: DONE
def suggestion(lexPOS, lexNEG, nbPOS, nbNEG):
    POS = (lexPOS + nbPOS) / 2
    NEG = (lexNEG + nbNEG) / 2
    TOTAL = (nbPOS + nbNEG + lexNEG + lexPOS) / 2
    difference = POS - NEG

    if(POS == 0):
        POS = 1
    if(NEG == 0):
        NEG = 1


    if(TOTAL > 80):
        if (difference == 0):
            result = "Neutral Sentiment. Stocks will not change very much."
        elif (difference > 0):
            percent = POS / NEG
            if(percent > 1.2):
                result = "Positive Sentiment. Stock prices will increase."
            else:
                result = "Insufficient Information (Positive not 20% Greater). Can not make suggestion."
        else:
            percent = NEG / POS
            if(percent > 1.2):
                result = "Negative Sentiment. Stock prices will decrease."
            else:
                result = "Insufficient Information (Negative not 20% Greater). Can not make suggestion."
    else:
        result = "Insufficient Information (Not Enough Articles). Can not make suggestion."

    return result


# TODO: DONE
def graph(days, month, year, company, lexPOS, lexNEG, nbPOS, nbNEG):
    plt.plot(days, lexPOS, color='g')
    plt.plot(days, lexNEG, color='r')
    plt.ylim(0, 100)
    plt.xlabel('Days of Month: ' + str(month) + ' and Year: ' + str(year))
    plt.ylabel('Number of Sentiment Articles')
    plt.title("Lexicon Sentiment Score for " + company.title())
    plt.show()

    plt.plot(days, nbPOS, color='g')
    plt.plot(days, nbNEG, color='r')
    plt.ylim(0, 100)
    plt.xlabel('Days of Month: ' + str(month) + ' and Year: ' + str(year))
    plt.ylabel('Number of Sentiment Articles')
    plt.title("Naive Bayes Sentiment Score for " + company.title())
    plt.show()

# TODO: DONE
def newsArticles(company, year, month, day):
    # collects all news articles of a given company from the first of the month to given date
    # api_key = "77e78b0d43684afca35a38bd91559742"

    url = ('https://newsapi.org/v2/'
           'everything?'
           'sources=the-wall-street-journal, bbc-news, bloomberg, business-insider, abc-news, cbs-news, fortune, '
           'cnn, nbc-news, the-economist, the-new-york-times, the-washington-post, '
           'techradar, mashable, engadget, techcrunch, wired, recode, the-verge'
           '&q=' + company +
           '&language=en'
           '&from=' + year + '-' + month + '-' + day +
           '&to=' + year + '-' + month + '-' + day +
           '&pageSize=100'
           '&apiKey=77e78b0d43684afca35a38bd91559742')

    response = requests.get(url)
    all_articles = response.json()["articles"]
    article_db = []

    for article in all_articles:
        # article data: title, source, description, url, publishedAt
        description = stripper(article['description'])
        article_db.append(description)

    return article_db


# TODO: DONE
def runLexicon(articles, sentLex):
    # generate dictionary containing articles and their scores
    articleScores = Lexicon.allScores(articles, sentLex)

    # get the count of POS/NEG/NEUt articles
    POS, NEG, NEUT = Lexicon.categorizeScores(articleScores)

    return POS, NEG, NEUT


# TODO: DONE
def runNaiveBayes(articles, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG):
    POS, NEG, NEUT = Naive_Bayes.categorizeScores(articles, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG)
    return POS, NEG, NEUT


# TODO: DONE
def engine():
    ###########################################
    # EDIT HERE: Input company and dates to search
    ###########################################
    company = 'facebook'
    year = '2018'
    month = '05'
    today = 11

    # gather lexicon/naive bayes trained data
    sentLex = Lexicon.sentLexicon()
    freqPOS, freqNEG = Naive_Bayes.frequency()
    countPOS, countNEG, countPOSNEG = Naive_Bayes.count(freqPOS, freqNEG)

    # reporting data
    data = ""
    artData = ""

    # graphing data
    days = []
    lexPOSGraph = []
    lexNEGGraph = []
    nbPOSGraph = []
    nbNEGGraph = []


    # gather articles and analyze sentiment for entire month up to date
    for day in range(1, today + 1):
        day = str(day)
        articles = newsArticles(company, year, month, day)

        # article data for report
        artData += 'Company: {}, Month: {}, Day: {}, Year: {}\n\n'.format(company, month, day, year)
        for article in articles:
            artData += article + "\n\n"

        lexPOS, lexNEG, lexNEUT = runLexicon(articles, sentLex)
        nbPOS, nbNEG, nbNEUT = runNaiveBayes(articles, freqPOS, freqNEG, countPOS, countNEG, countPOSNEG)
        result = suggestion(lexPOS, lexNEG, nbPOS, nbNEG)

        # graphing data
        days.append(day)
        lexPOSGraph.append(lexPOS)
        lexNEGGraph.append(lexNEG)
        nbPOSGraph.append(nbPOS)
        nbNEGGraph.append(nbNEG)

        # display data
        print('Company: {}, Month: {}, Day: {}, Year: {}'.format(company, month, day, year))
        print("Lexicon     - POS: {}, NEG: {}, NEUT: {}".format(lexPOS, lexNEG, lexNEUT))
        print("Naive Bayes - POS: {}, NEG: {}, NEUT: {}".format(nbPOS, nbNEG, nbNEUT))
        print("Results: " + result)
        print("______________________________________________________")

        # sentiment data for report
        data += '\nMonth: {}, Day: {}, Year: {}\n'.format(month, day, year)
        data += "Results: " + result + "\n"
        data += "Lexicon     - POS: {},\tNEG: {},\tNEUT: {}\n".format(lexPOS, lexNEG, lexNEUT)
        data += "Naive Bayes - POS: {},\tNEG: {},\tNEUT: {}\n\n".format(nbPOS, nbNEG, nbNEUT)
        data += "______________________________________________________\n"

    graph(days, month, year, company, lexPOSGraph, lexNEGGraph, nbPOSGraph, nbNEGGraph)
    print("Graphs generated...")

    report(company, str(today), month, year, data, artData)
    print("Report generated...")


engine()

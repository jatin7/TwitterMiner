import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde

#from scipy.interpolate import UnivariateSpline
#import matplotlib.ticker as tick
#import pandas as pd

class getTweetStats:
    """ Summary statistics for Tweets"""
    
    def __init__(self, input):
        self.input = input

    def mean(self):
        calc = round(sum(self.input)/len(self.input),2)
        return calc
    
    def stdev(self):
        calc1 = self.mean()
        calc2 = [(self.input[i]-calc1)**2 for i in range(len(self.input))]
        calc3 = round((sum(calc2)/len(calc2))**0.5, 2)
        return calc3
    
    def median(self):
        array = sorted(self.input)
        if len(array) % 2 == 0:
            i = int((len(array) / 2) - 1)
            j = i + 1
            calc = (array[i] + array[j]) / 2
            return calc
        else:
            k = int((len(array) + 1) / 2) - 1
            return array[k]
    
    def iqr(self):
    #IQR interpolation algorithm set as 'linear', where i + (j - i) * fraction of index
        array = sorted(self.input)
        indexq1 = (len(array) + 1) / 4
        indexq3 = 3 * (len(array) + 1) / 4
        getposq1 = array[int(indexq1 - 1)]
        getposq3 = array[int(indexq3 - 1)]
        calcq1 = getposq1 + (indexq1 - (int(indexq1))) * (array[int(indexq1)] - array[int(indexq1) - 1])
        calcq3 = getposq3 + (indexq3 - (int(indexq3))) * (array[int(indexq3)] - array[int(indexq3) - 1])
        return (calcq3 - calcq1)
    
    def summary(self):
        result = {'Min': min(self.input), 'Max': max(self.input), \
            'Mean': self.mean(), 'Median': self.median(), \
            'St Dev': self.stdev(), 'IQR': self.iqr()}
        return result

class getTweetPlots:
    """Plotting data distribution based on the Twitter dataset"""

    def __init__(self,input):
        self.input = input

    def getmeasures(self):
        wordcount = [len(self.input[i]) for i in range(len(self.input))]
        charcount = [len(self.input[i].split()) for i in range(len(self.input))]
        return wordcount, charcount     
        
    def create_boxplt(self):
        # CREATE BOXPLOTS
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
        
        boxplt1 = axes[0].boxplot(self.getmeasures()[0],
                                  whis='range',
                                  showfliers=False,
                                  vert=True,
                                  patch_artist=True,
                                  widths=0.25
                                  )
        axes[0].set_title('Character distribution per tweet')
        #plt.xticks([])
        
        boxplt2 = axes[1].boxplot(self.getmeasures()[1],
                                  whis='range',
                                  showfliers=False,
                                  vert=True,
                                  patch_artist=True,
                                  widths=0.25
                                  )
        axes[1].set_title('Word distribution per tweet')
        #plt.xticks([])
        
        colors = ['lightblue']
        for x in (boxplt1, boxplt2):
            for patch, color in zip(x['boxes'], colors):
                patch.set_facecolor(color)
        
        for x in axes: 
            x.yaxis.grid(True, color='#dddddd')
            x.set_xlabel('')
            x.set_ylabel('')
            x.set_xticks([])
            x.spines['top'].set_color('#dddddd')
            x.spines['left'].set_color('#dddddd')
            x.spines['bottom'].set_color('#dddddd')
            x.spines['right'].set_color('#dddddd')
        plt.show()
        
        [item.get_ydata() for item in boxplt1['whiskers']]
        [item.get_ydata() for item in boxplt2['whiskers']]
        
    def create_densplt(self):
        # CREATE DENSITY PLOTS
        # probability is calculated by using a gaussian function (kernel density estimation)
        kde_chars = gaussian_kde(self.getmeasures()[0])
        kde_words = gaussian_kde(self.getmeasures()[1])
        dist_chars = np.linspace(min(self.getmeasures()[0]), max(self.getmeasures()[0]), 100)
        dist_words = np.linspace(min(self.getmeasures()[1]), max(self.getmeasures()[1]), 100)
        
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
        densplt1 = axes[0].plot(dist_chars, kde_chars(dist_chars),
                                color='lightblue'
                                )
        axes[0].set_title('Probability Density Plot - Characters')
        
        densplt2 = axes[1].plot(dist_words, kde_words(dist_words),
                                color='lightblue'
                                )
        axes[1].set_title('Probablity Density Plot - Words')
        
        for x in axes:
            x.yaxis.grid(True, color='#dddddd')
            x.set_xlabel('')
            x.set_ylabel('')
            x.spines['top'].set_color('#dddddd')
            x.spines['left'].set_color('#dddddd')
            x.spines['bottom'].set_color('#dddddd')
            x.spines['right'].set_color('#dddddd')
        plt.show()
        
#x = [0,1,2,5,8,8]
#y = [40,50,50,60,40,80]
#
#jesus = x, y
#jesus[1]
#
#test = getTweetStats(x).summary()
#
#numpyiqr = (np.subtract(*np.percentile(wordplot, [75, 25], interpolation='linear')))
#print(numpyiqr)
#iqr(wordplot)
#
#jesus = getTweetPlots(test).create_boxplt()
#jesus2 = getTweetPlots(test).create_densplt()
        
        
## STEP X: Plotting: Histogram
#taglabel = list(zip(*hashtags_freq[0:13]))[0]
#tagcount = list(zip(*hashtags_freq[0:13]))[1]
#x_pos = np.arange(len(taglabel)) 
#
## creating trendline with two points (x,y) 
## fits a polynomial function into a linear function that minimises the squared error
#slope, intercept = np.polyfit(x_pos, tagcount, 1)
#trendline = intercept + (slope * x_pos)
#
#plt.figure(num=None, figsize=(12,8), dpi=80, facecolor='w', edgecolor='k')
#plt.plot(x_pos, trendline, color='red', linestyle='--')    
#plt.bar(x_pos, tagcount, align='center')
#plt.xticks(x_pos, taglabel) 
#plt.ylabel('Number of occurences')
#plt.xticks(rotation=45)
#plt.gca().set_axisbelow(True) #plt.gca() gets current axis attributes
#plt.gca().yaxis.grid(True)
#plt.show()

# STEP X: Plotting: Social Network Analysis


# to export plots fig.savefig() or plt.savefig()
# to browse plot styles plt.style.available() and plt.style.use()
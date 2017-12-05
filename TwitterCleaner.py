import re
#import html
#import itertools

class TweetCleaner:
    """ Preprocessing tweets for modeling stage:
            STEP 1: Standardizing: capitalization
            STEP 2: Removing noise: HTTP links
            STEP 3: Removing noise: Escaping HTML characters
            STEP 4: Standardizing: punctuation
            STEP 5/8: Removing noise: Removing blank characters """
    
    def __init__(self, input):
        self.input = input
    
    def cleanup(self):
        step1 = [self.input[i].lower() for i in range(len(self.input))]
        step2 = [re.sub(r'http\S+', '', step1[i]) for i in range(len(step1))]
        step3 = [re.sub(r'&\S+', '', step2[i]) for i in range(len(step2))]
        step4 = [re.sub(r'[^\w\s\'&@#]', '', step3[i]) for i in range(len(step3))]
        step5 = [re.sub(r'[\n\xa0]', '', step4[i]) for i in range(len(step4))]
        step6 = [re.sub(r'\s{2,}', ' ', step5[i]) for i in range(len(step5))]
        step7 = [re.sub(r'^\s+', '', step6[i]) for i in range(len(step6))]
        step8 = [re.sub(r'\s+$', '', step7[i]) for i in range(len(step7))]
        return step8
    
    # STEP 5: Feature selection: tokenization as "bag of words"
    def getbow(self):
        tokens = [self.input[i].split() for i in range(len(self.input))]
        tokens2 = [i for j in tokens for i in j]  
        wordfreq = [(x,tokens2.count(x)) for x in set(tokens2)]
        return sorted(wordfreq, key = lambda x: -x[1])
    
    # STEP 6: Feature selection: hashtags and user tags
    def gethashtags(self):
        hashtags = re.findall(r'#\w+', str(self.input))
        tagfreq = [(x, hashtags.count(x)) for x in set(hashtags)]
        return sorted(tagfreq, key = lambda x: -x[1])
    
#usertags = re.findall(r'@\w+', str(self.input))


#test = cleanTweet(sample).cleanup()
#sample = [' jesus  likes potato , i dont, period']

'''
# STEP X: Standardizing words (NOT WORKING)
step3 = [".join(".join(s)[:2] for _, s in itertools.groupby(step2[i])) for i in range(len(step2))]


# STEP X: Decoding data (Error: 'str' object has no attribute 'decode')
step2 = [step1[i].decode("utf8").encode('ascii','ignore') \
    for i in range(len(step1))]
print (step2[0])


# STEP X: Splitting attached words (working, but it ruins acronyms)
step4 = [" ".join(re.findall('[A-Z][^A-Z]*', step3[i])) for i in range(len(step3))]
print(step4[0])

'''
import twitter # has to be installed with 'pip install python-twitter'
import pickle
import sys # so as to know the error


class TweetFetcher:
    """ Create a request with the Twitter API. Types of request:
            'userposts': Get posts created by an user, username as the keyword
            'followers': Get followers of an user, username as the keyword
            'friends': Get all friends of an user, username as the keyword
            'userlikes: Get all posts liked by an user, username as the keyword
            'search: Get all posts matching the keyword """
    
    def __init__(self, keyword, request='search'):
        args = ['userposts','followers','friends','userlikes','search']
        if request in args:
            self.keyword = keyword
            self.request = request
        else:
            raise ValueError('Invalid request. Check \'help()\' for instructions.')
                
    def create_request(self):
        with open('creds.pkl', 'rb') as handle:
            creds = pickle.load(handle)
        
    # CONNECT TO THE TWITTER API WITH YOUR TWITTER APP CREDENTIALS
        api = twitter.Api(consumer_key = creds['consumer_key'],\
                          consumer_secret = creds['consumer_secret'],\
                          access_token_key = creds['access_token_key'],\
                          access_token_secret = creds['access_token_secret'])
          
        batchsize = 200
        maxi = []
        f = 0
        
    # LOOP WHILE MOST RECENT TWEET IS NOT RETRIEVED
        while True: 
            try:
            # GET USERLIKES AND EXPORT WITH PICKLE
                if self.request == 'userlikes':
                    query = api.GetFavorites(screen_name = self.keyword, count = batchsize, max_id = maxi)
                    to_save = [query[i].AsDict() for i in range(len(query))]
                    with open('%s_%d.pkl' % (self.request, f), 'wb') as handle:
                        pickle.dump(to_save, handle)
                
                # INCREMENT MAX_ID AND ITERATE. RETURN ALL DATA IF MAX_ID IS REACHED
                    f += 1
                    if maxi == to_save[-1]['id']:
                        output = []
                        for i in range(f):
                            with open('%s_%d.pkl' % (self.request, i), 'rb') as handle:
                                output.extend([t['text'] for t in pickle.load(handle)])
                        return output
                        break
                    else:
                        maxi = to_save[-1]['id']
            
            # GET USER FOLLOWERS AND EXPORT WITH PICKLE   
                elif self.request == 'userposts':
                    query = api.GetUserTimeline(screen_name = self.keyword, count = batchsize, max_id = maxi)
                    to_save = [query[i].AsDict() for i in range(len(query))]
                    with open('%s_%d.pkl' % (self.request, f), 'wb') as handle:
                        pickle.dump(to_save, handle)
                
                # INCREMENT MAX_ID AND ITERATE. RETURN ALL DATA IF MAX_ID IS REACHED
                    f += 1
                    if maxi == to_save[-1]['id']:
                        output = []
                        for i in range(f):
                            with open('%s_%d.pkl' % (self.request, i), 'rb') as handle:
                                output.extend([t['text'] for t in pickle.load(handle)])
                        return output
                        break
                    else:
                        maxi = to_save[-1]['id']
            
            # GET ALL MATCHES ON GLOBAL SEARCH AND EXPORT WITH PICKLE  
                elif self.request == 'search':
                    query = api.GetSearch(term = self.keyword, count = batchsize, max_id = maxi)
                    to_save = [query[i].AsDict() for i in range(len(query))]
                    with open('%s_%d.pkl' % (self.request, f), 'wb') as handle:
                        pickle.dump(to_save, handle)
                
                # INCREMENT MAX_ID AND ITERATE. RETURN ALL DATA IF MAX_ID IS REACHED
                    f += 1
                    if maxi == to_save[-1]['id']:
                        output = []
                        for i in range(f):
                            with open('%s_%d.pkl' % (self.request, i), 'rb') as handle:
                                output.extend([t['text'] for t in pickle.load(handle)])
                        return output
                        break
                    else:
                        maxi = to_save[-1]['id']
            except:
                print(sys.exc_info()[0])
                break
            

# OTHER ARGUMENTS TO IMPLEMENT: HOW TO CREATE BATCHES WITHOUT MAX_ID AS CRITERIA?
#                elif self.request == 'followers'
#                    query = api.GetFollowers(screen_name = keyword, count = batchsize)
#                elif self.request == 'friends':
#                    query = api.GetFriends(screen_name = self.keyword, count = batchsize, max_id = maxi)
          
#test = getTweet('burnie093','userlikes').create_request()
#print(len(test))

"""

# ADDITIONAL FORMATS, IF NECESSARY
    #id/tweet tuples
    indices = []
    for i in range(f): # i belongs to [0, 5[
        with open('favs_%d.pkl' % i, 'rb') as handle:
            indices.extend([(t['id'],t['text']) for t in pickle.load(handle)])
    print(indices[0])
    
    #id/user tuples
    users = []
    for i in range(f): # i belongs to [0, 5[
        with open('favs_%d.pkl' % i, 'rb') as handle:
            users.extend([(t['id'],(t['user'])['screen_name']) for t in pickle.load(handle)])
            
    print(users[0:3])
"""
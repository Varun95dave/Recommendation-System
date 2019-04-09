# -*- coding: utf-8 -*-
"""

"""

# you must NOT import or use any other packages or modules besides these
import math
from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is expected in the form of a nested dictionary:
    # at the top level, it has User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    
    def __init__(self, usersItemRatings, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            

    #################################################
    # calcualte the pearson correlation between two item ratings dictionaries userXItemRatings and userYItemRatings
    #
    # userXItemRatings and userYItemRatings data is expected in the form of dictionaries of item ratings
    
    # Example:
    #      userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    #      userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    #
    # NOTE: the number, names, or format of the input parameters to this method must NOT be changed.
    
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        
        self.userXItemRatings = userXItemRatings
        self.userYItemRatings = userYItemRatings
        
        x   = []
        y   = []
        xy  = []
        xsq = []
        ysq = []
        num = []
    
        for i in self.userXItemRatings.keys():
            if i in self.userYItemRatings.keys():
                x_i = self.userXItemRatings[i]
                y_i = self.userYItemRatings[i]
                xs = pow(x_i,2)
                ys = pow(y_i,2)
                x_y = x_i * y_i
                x.append(x_i)
                y.append(y_i)
                xsq.append(xs)
                ysq.append(ys)
                xy.append(x_y)
                num.append(i)
    
        # Entering input parameters into the computationally efficient formula
        n     = len(num)
        if (n == 0) :
            pc = -2
        else:
            nr    = sum(xy) - (sum(x)*sum(y)/n)
            dr_x  = pow(sum(xsq)-(pow(sum(x),2)/n),0.5)
            dr_y  = pow(sum(ysq)-(pow(sum(y),2)/n),0.5)
            dr    = dr_x * dr_y
            if (dr == 0):
                pc    = -2
            else:
                pc    = nr/dr
        return pc

          
        # Things to keep in mind as you code this section:
        # (a) this method must calcualte and return the pearson correlation between the two given dictionaries of items ratings.
        # (b) the number, names, or format of the input parameters to this method must NOT be changed.
        # (c) the method must use the computationally efficient form of pearson correlation to calucalte the pearson correlation
        # (d) the method must use only a total of 1 for loop to calcualte the pearson correlation
        # (e) the method must compute the value of n as the number of common keys in the dictionaries 
        # (f) the method must perform the following error checks:
        #     if n=0, return value of -2
        #     if the denominator of the pearson correlation=0, return value of -2
        # (g) if neither of the error conditions in (f) occured, return the pearson correlation
        
        # once you are done coding this method, delete the pass statement below
    

    #################################################
    # make recommendations for userX from the k most similar nearest neigibors (NNs)
    # NOTE: the number, names, or format of the input parameters to this method must NOT be changed.
    def recommendKNN(self, userX):
        
        
        self.userX  = userX 
        nameX       = self.userX
        userY       = self.usersItemRatings
        
        for ux_name, ux_songrating in userY.items():
            if(ux_name == nameX):
                song_meta        = []
                rec              = []
                name_pc          = {}
                filtered_name_pc = {}

                for uy_name, uy_songrating in userY.items():
                    if (uy_name != ux_name):
                            #Use of pearsonFn
                            pc   = self.pearsonFn(ux_songrating,uy_songrating)
                            pc   = ((pc + 1)/2)
                    else:
                            pc    = -10
    
                    rec.append(pc)
                    name_pc.update(zip(userY,rec))
    
                    # Making a list of all songs
                    for song,rating in uy_songrating.items():
                        song_meta.append(song)
    
                songs = list(set(song_meta))
    
                #Sorting in descending order
                name_pc_alt_sort  = sorted(name_pc.items(), key=itemgetter(1), reverse = True) 
                
                #Eliminating undefn and ownself users
                filtered_pc    = [pc for name,pc in name_pc_alt_sort if pc > -0.1]
                filtered_name  = [name for name,pc in name_pc_alt_sort if pc > -0.1]
    
                #Taking closets K neighbors
                first_k_name = filtered_name[:self.k]
                first_k_pc   = filtered_pc[:self.k]
    
                #Calculating weights wrt k NNs
                total      = sum(first_k_pc)
                first_k_pc = [i/total for i in first_k_pc]
                filtered_name_pc.update(zip(first_k_name,first_k_pc))  
    
                #Creating a list of user-rated songs
                user_songs = [song for song, rating in ux_songrating.items()]
    
                #Identifying unrated songs
                songs      = tuple(songs)
                user_songs = tuple(user_songs)
                unr_song   = set(songs).difference(user_songs) 
    
                #Extracting ratings from kNNs for unrated songs by User X & Calculating weighted rating
                song_wr  = {}
    
                for uy_name, uy_songrating in userY.items():
                        for song, rating in uy_songrating.items():
                            for name, weight in filtered_name_pc.items():
                                if (uy_name == name):
                                    if(song in unr_song):
                                        weightedrating = rating * weight
                                        song_wr.setdefault(song, []).append(weightedrating)
    
    
                results = {key: round(sum(values),2) for key, values in song_wr.items()}
    
                #Recommendation
                reco    = sorted(results.items(), key=itemgetter(1), reverse = True)

        return reco

        # Considerations:
        # (a) this method must calcualte and return the recommendations for userX from the k most similar nearest neighbors
        # (b) the number, names, or format of the input parameters to this method must NOT be changed
        # (c) the method must use self.usersItemRatings (set during class object instantiation) to get the other users and their item ratings
        # (d) the method must use self.k (set during class object instantiation) to get the value of k
        # (e) the method must use the PearsonFn method defined in this class to calcualte similarity
               
        # Steps you might want to follow as you code this section:
        # (a) first, for given userX, get the sorted list of users - by most similar to least similar:
        #     - remember to exclude simialrity of user from himself 
        #     - remember to exclude any users with similarity of -2 (since that means error condition) 
        # (b) then, calcualte the weighted average item recommendations for userX from userX's k NNs
        # (c) then, return sorted list of recommendations (sorted highest to lowest ratings)
        #     example: [('Broken Bells', 2.64), ('Vampire Weekend', 2.2), ('Deadmau5', 1.71)]
        

        



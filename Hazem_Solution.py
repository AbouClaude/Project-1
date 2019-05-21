import pandas as pd
import numpy as np

# Loads Bundesliga results dataset. 
df = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/vcd/Bundesliga.csv')

def Exercise1(df):
    #Group the dataframe by hometeam and assert the values as "the sum of homegoals" and
    #sort them according to the summed values.
    TeamsHomeGoals=df.groupby(['HomeTeam'])['HomeGoals'].sum().sort_values(ascending=False)
    print("The team who scored the most homegoals is:",TeamsHomeGoals.first_valid_index(),"which scored:",TeamsHomeGoals[0],"goals")
    
    

'''
	From the Bundesliga results dataset, defined above  calcualte which team has scored the most Homegoals.
	
    
     another way
    #make pivot tables "Awayteams as rows" , "Hometeams as column" , "Homegoals as Value" the aggrigation function is sum
    t= pd.DataFrame(pd.pivot_table(df,values=['HomeGoals'],index=['AwayTeam'],columns=['HomeTeam'],aggfunc={'HomeGoals':np.sum}))
    #make dictionary comprahansion where include teams as keys, the sum of homegoals for a team 'sum the column' then get the max
    maxgoals={x:t[x].sum() for x in t.columns}
    ans=max(zip(maxgoals.values(), maxgoals.keys()))
    print("the most team who scored homegoals is: ",ans[1][1], "which scored: ", int(ans[0]))
'''

def Exercise2(df):
    #clean sheet for Awayteams: select the records and convert them to  dataframe
    #then Select the required columns 'AwayTeam', 'Round' and 'Date'
    CleanSheetAway=pd.DataFrame(df[(df.HomeGoals ==0)])
    CleanSheetAway=CleanSheetAway[['AwayTeam','Round','Date']]
    #________________________________________________________________
    
    #clean sheet for Hometeams: select the records and convert them to dataframe
    #then Select the required columns 'AwayTeam', 'Round' and 'Date'
    CleanSheetHome=pd.DataFrame(df[(df.AwayGoals ==0)])
    CleanSheetHome=CleanSheetHome[['HomeTeam','Round','Date']]
    #________________________________________________________________
    
    #Concatenate the two mentioned DataFrames then order them according to their indecies
    CleanSheets=pd.concat([CleanSheetHome,CleanSheetAway],sort='quicksort')
    CleanSheets=CleanSheets.sort_index(kind='quicksort')
    #________________________________________________________________
    
    #After concatenating many Nan Values will created so we replaced them by empty space ''
    CleanSheets['AwayTeam'] = CleanSheets['AwayTeam'].replace(np.nan, '', regex=True)
    CleanSheets['HomeTeam'] = CleanSheets['HomeTeam'].replace(np.nan, '', regex=True)
    #________________________________________________________________
    
    #After Cleaning the data we add the AwayTeam and HomeTeam together and put them in one column
    #Then drop the original columns AwayTeam and HomeTeam
    CleanSheets['Team']=CleanSheets['AwayTeam']+CleanSheets['HomeTeam']
    CleanSheets=CleanSheets.drop(['HomeTeam','AwayTeam'],axis=1)
    #________________________________________________________________
    
    #We make pivot table from CleanSheet where the date as index, Table as columns and Rounds as Values
    #Then Clean the data again after the new formation
    CleanSheets=CleanSheets.pivot(index='Date',columns='Team',values='Round')
    CleanSheets=CleanSheets[CleanSheets.columns].replace(np.nan,'',regex=True)
    #________________________________________________________________
    
    #Finally, I made the dataframe where the index as Date and the whole teams
    #who played during the Bundesliga
    #________________________________________________________________
    
    #Create Empty Dictionary to fill the max cleansheet
    #where teams as keys and the values are the max of cleansheet for eachteam
    MaxCleanSheet={}
    cleanmax=0
    #________________________________________________________________
    
    
    #Iterate over all columns of the CleanSheets DataFrame
    #and Compute the maximum clean sheet and store it in the dictionary
    for Team in CleanSheets.columns:
       MaxCleanSheet[Team]=0
       for item in CleanSheets[Team]:
           if(item!=''):
              cleanmax+=1          
           if (item=='' and cleanmax!=0):
              if (cleanmax>MaxCleanSheet[Team]):
                  MaxCleanSheet[Team]=cleanmax
              cleanmax=0
    #_________________________________________________________________
    
    
    #I used max function to get the highest cleansheet but the result only one team
    #So I made list comprahansion to see if there another team are equal to the max team
    high=max(zip(MaxCleanSheet.values(), MaxCleanSheet.keys()))
    print([k for k, v in MaxCleanSheet.items() if v == high[0]], 'have the highest clean sheet streak (5 Matches)')

''' From the Bundesliga results dataset calculate which team has had the 
    most consecutive games without conceding any goals and how many games that
    streak lasted 
    returns ()
'''

	#return (teamWithLongestStreak,lengthOfStreak])

def Exercise3(dataset):
    
    #put the year (Seasons) of all season without duplication values
    #make empty list to store DataFrames as results of tables over seasons
    listofyears=list(df.drop_duplicates('Year')['Year'])
    seasonstables=[]
    
    #Iterate Over Seasons in the Data and Create Framework for each season
    #then create teams list where contain the team who played during the iterated season
    #Create DataFrame as the table of the iterated season where we need Points, Wins and Played Matches
    #Then Clean the Result table to fill the data
    #Iterate over season matches and compute all the columns in the SeasonTable DataFrame
    #Then Add it to the seasonstables
    for year in listofyears:
        seasonmatches=pd.DataFrame(df[(df.Year==year)])
        teams=list(df[(df.Year==year)].drop_duplicates('HomeTeam')['HomeTeam'])
        SeasonTable=pd.DataFrame(index=teams,columns=[['Points','Wins','PlayedMatches']],dtype=int)
        SeasonTable=SeasonTable.fillna(0)
        
        for index,row in seasonmatches.iterrows():
            if( row['HomeGoals']==row['AwayGoals']):
                SeasonTable.loc[row['HomeTeam'],'Points']+=1
                SeasonTable.loc[row['AwayTeam'],'Points']+=1
            
            elif((row['HomeGoals']>row['AwayGoals'])):
                SeasonTable.loc[row['HomeTeam'],'Points']+=3
                SeasonTable.loc[row['HomeTeam'],'Wins']+=1

            elif(row['HomeGoals']<row['AwayGoals']):
                SeasonTable.loc[row['AwayTeam'],'Points']+=3
                SeasonTable.loc[row['AwayTeam'],'Wins']+=1
        
            SeasonTable.loc[row['HomeTeam'],'PlayedMatches']+=1
            SeasonTable.loc[row['HomeTeam'],'PlayedMatches']+=1
        
        
        seasonstables.append(SeasonTable)
    
    #Iterate over the results of all seasons and get the min value of each season
    #then assign it to the weakest point and get the required values
    #to compute the required Property
    #Unfortunatelly, the data is filled cell by cell instead of filling it by rows
    #because of the results of the matches, so it's hard to have access to data that
    #why it looks wiered
    for currentseason in seasonstables:
        weakestterms=currentseason.min()
        Wteam=currentseason[currentseason.Points.values==weakestterms[0]]
        print(round(Wteam.Wins.values[0][0]/Wteam.PlayedMatches.values[0][0],2))

'''
	In football, every win awards the team 3 points, every tie awards 1 point 
	and a loss 0 points. Considering this, return the proEbability
	that the team with less points in the current SEASON (up to matchday) wins.
	Round to 2 decimals	using Python built in function round().
''' 

	#return Probability 			

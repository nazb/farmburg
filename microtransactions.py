
# coding: utf-8

# # Project: Hypothesis Testing for Microtransactions
# Brian is a Product Manager at FarmBurg, a company that makes a farming simulation social network game.  In the FarmBurg game, you can plow, plant, and harvest different crops.
# 
# Today, you will be acting as Brian's data analyst for an A/B Test that he has been conducting.

# ## Part 1: Testing for Significant Difference

# Start by importing the following modules that you'll need for this project:
# - `pandas` as `pd`

# In[1]:


import pandas as pd


# Brian tells you that he ran an A/B test with three different groups: A, B, and C.  You're kind of busy today, so you don't ask too many questions about the differences between A, B, and C.  Maybe they were shown three different versions of an ad.  Who cares?
# 
# (HINT: you will care later)
# 
# Brian gives you a CSV of results called `clicks.csv`.  It has the following columns:
# - `user_id`: a unique id for each visitor to the FarmBerg site
# - `ab_test_group`: either `A`, `B`, or `C` depending on which group the visitor was assigned to
# - `click_day`: only filled in *if* the user clicked on a link to purchase
# 
# Load `clicks.csv` into the variable `df`.

# In[5]:


df=pd.read_csv('clicks.csv')
df.head()


# Define a new column called `is_purchase` which is `Purchase` if `click_day` is not `None` and `No Purchase` if `click_day` is `None`.  This will tell us if each visitor clicked on the Purchase link.

# In[7]:


df['is_purchase']=df.click_day.apply(lambda x: 'Purchase' if pd.notnull(x) else 'No Purchase')
df.head()


# We want to count the number of users who made a purchase from each group.  Use `groupby` to count the number of `Purchase` and `No Purchase` from each `group`.  Save your answer to the variable `purchase_counts`.
# 
# **Hint**: Group by `group` and `is_purchase` and the function `count` on the column `user_id`.

# In[12]:


purchase_counts=df.groupby(['group','is_purchase']).user_id.count().reset_index()
purchase_counts.head(10)


# This data is *categorical* and there are *more than 2* conditions, so we'll want to use a chi-squared test to see if there is a significant difference between the three conditions.
# 
# Start by filling in the contingency table below with the correct values:
# ```py
# contingency = [[groupA_purchases, groupA_not_purchases],
#                [groupB_purchases, groupB_not_purchases],
#                [groupC_purchases, groupC_not_purchases]]
# ```

# In[44]:


contingency = [[316, 1350],
               [183, 1483],
               [83, 1583]]
purchase_counts.groupby('group').sum()


# Now import the function `chi2_contingency` from `scipy.stats` and perform the chi-squared test.
# 
# Recall that the *p-value* is the second output of `chi2_contingency`.

# In[14]:


from scipy.stats import chi2_contingency


# In[17]:


chi2,pval,d,e= chi2_contingency(contingency)
pval


# Great! It looks like a significantly greater portion of users from Group A made a purchase.

# ## Part 2: Testing for Exceeding a Goal
# 
# Your day is a little less busy than you expected, so you decide to ask Brian about his test.
# 
# **You**: Hey Brian! What was that test you were running anyway?
# 
# **Brian**: It was awesome! We are trying to get users to purchase a small FarmBurg upgrade package.  It's called a microtransaction.  We're not sure how much to charge for it, so we tested three different price points: \$0.99, \$1.99, and \$4.99.  It looks like significantly more people bought the upgrade package for \$0.99, so I guess that's what we'll charge.
# 
# **You**: Oh no! I should have asked you this before we did that chi-squared test.  I don't think that this was the right test at all.  It's true that more people wanted purchase the upgrade at \$0.99; you probably expected that.  What we really want to know is if each price point allows us to make enough money that we can exceed some target goal.  Brian, how much do you think it cost to build this feature?
# 
# **Brian**: Hmm.  I guess that we need to generate a minimum of $1000 per week in order to justify this project.
# 
# **You**: We have some work to do!

# How many visitors came to the site this week?
# 
# Hint: Look at the length of `df`.

# In[28]:


visitors=len(df)
visitors


# Let's assume that this is how many visitors we generally get each week.  Given that, calculate the percent of visitors who would need to purchase the upgrade package at each price point (\$0.99, \$1.99, \$4.99) in order to generate \$1000 per week.

# In[46]:


# Calculate the number of people who would need to purchase a $0.99 upgrade in order to generate $1000.
# Then divide by the number of people who visit the site each week.
target_09=(1000/0.99)/visitors


# In[47]:


# Calculate the number of people who would need to purchase a $1.99 upgrade in order to generate $1000.
# Then divide by the number of people who visit the site each week.
target_19=(1000/1.99)/visitors


# In[55]:


# Calculate the number of people who would need to purchase a $4.99 upgrade in order to generate $1000.
# Then divide by the number of people who visit the site each week.\
target_49=(1000/4.99)/visitors


# Note that you need a smaller percentage of purchases for higher price points.
# 
# Now, for each group, perform a binomial test using `binom_test` from `scipy.stats`.
# - `x` will be the number of purchases for that group
# - `n` will be the total number of visitors assigned to that group
# - `p` will be the target percent of purchases for that price point (calculated above)
# 
# Recall that:
# - Group `A` is the \$0.99 price point
# - Group `B` is the \$1.99 price point
# - Group `C` is the \$4.99 price point

# In[42]:


# import the binomial test from scipy.stats here
from scipy.stats import binom_test


# In[52]:


# Test group A here
pval1=binom_test(316,1666,target_09)
pval1


# In[53]:


# Test group B here
pval2=binom_test(183,1666,target_19)
pval2


# In[56]:


# Test group C here
pval3=binom_test(83,1666,target_49)
pval3


# If any of the groups passed the binomial test with $p < 0.05$, then we can be confident that enough people will buy the upgrade package at that price point to justify the feature.
# 
# Which price point should Brian go with?  Did this surprise you?

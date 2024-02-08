#!/usr/bin/env python
# coding: utf-8

# <h1>Book Sales <h1>

# In[291]:


import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[322]:


#Read CSV
df = pd.read_csv(r"C:\Users\win10\Documents\Big Blue Exersices\maryna-bilash-exercises\Books_Data_Clean.csv")
df


# In[294]:


# First rows of DataFrame 
df.head()


# In[295]:


#Count the number of missing values 
df.isnull().sum()


# In[296]:


#Generate descriptive statistics of a DataFrame. 
df.describe()


# In[297]:


# Remove Row with NaN
df= df.dropna(subset=['Publishing Year'])
#df= df.dropna(subset=['language_code'])


# In[298]:


# Examine the column 
df['language_code'].unique()


# In[323]:


# Convert language codes to Countries names
df['language_code'] = df['language_code'].replace(['eng'], 'English')
df['language_code'] = df['language_code'].replace(['en-US'], 'English (United States)')
df['language_code'] = df['language_code'].replace(['en-CA'], 'English (Canada)')
df['language_code'] = df['language_code'].replace(['en-GB'], 'English (United Kingdom)')
df['language_code'] = df['language_code'].replace(['ara'], 'Arabic')
df['language_code'] = df['language_code'].replace(['fre'], 'French')
df['language_code'] = df['language_code'].replace(['spa'], 'Spanish')
df['language_code'] = df['language_code'].replace(['nl'], 'Duch')


# In[324]:


# Examine the column 
df['genre'].unique()


# In[325]:


# Convert the names of the column 
df['genre'] = df['genre'].replace(['genre fiction'], 'Fiction')
df['genre'] = df['genre'].replace(['fiction'], 'Fiction')
df['genre'] = df['genre'].replace(['nonfiction'], 'NonFiction')
df['genre'] = df['genre'].replace(['children'], 'Children')


# In[326]:


#Keep only the positive numbers 
df['Publishing Year'] = df['Publishing Year'].apply(lambda x: int(x) if x > 0 else None)


# In[303]:


# Last Publishing Year 
df['Publishing Year'].max()


# In[304]:


# First Publishing Year 
df['Publishing Year'].min()


# In[327]:


# Keep Books from 2006-2016
df_10 = df[df['Publishing Year'].between(2006, 2016)]
df_10


# <h5> 1. Top 10 of Book Sales<h5>

# In[328]:


# Group by Book name and summing up with gross sales of each book.(top 10)
top_10_book_sales = df_10.groupby(['Book Name'])['gross sales'].sum().reset_index().sort_values(by='gross sales', ascending=False).head(10)
top_10_book_sales 


# In[329]:


#Setting the 'Book Name' column as the index
top_10_book_sales.set_index('Book Name', inplace=True)


# In[331]:


#Seaborn style
sns.set(style="whitegrid")

#Bar plot
plt.figure(figsize=(12, 6))
bar_colors = sns.color_palette("viridis", len(top_10_book_sales_sorted))

#Seaborn barplot
sns.barplot(x='gross sales', y=top_10_book_sales_sorted.index, data=top_10_book_sales_sorted, palette=bar_colors, orient='h')
plt.title('Top 10 Books Based on Sales', fontsize=16, fontweight='bold')
plt.xlabel('Total Sales', fontsize=12)
plt.ylabel('Book Name', fontsize=12) 
plt.yticks(fontsize=10)

for index, value in enumerate(top_10_book_sales_sorted['gross sales']):
    plt.text(value + 1, index, str(round(value, 2)), ha='left', va='center', color='#333333', fontsize=8)

plt.tight_layout()
plt.show()


# <h5>2. Top 10 Authors <h5>

# In[332]:


# Group by Author name and summing up with gross sales of each author.(top 10)
best_authors = df_10.groupby(['Author'])['gross sales'].sum().reset_index().sort_values(by='gross sales', ascending=False).head(10)
best_authors


# In[333]:


#Setting the 'Author' column as the index
best_authors.set_index('Author', inplace=True)


# In[335]:


# Seaborn style
sns.set(style="whitegrid")

# Create a bar plot with enhanced styling using orange colors
plt.figure(figsize=(12, 6))
bar_colors = sns.color_palette("Oranges_r", len(best_authors_sorted))

#Seaborn barplot 
sns.barplot(x='gross sales', y=best_authors_sorted.index, data=best_authors_sorted, palette=bar_colors, orient='h')
plt.title('Top Authors Based on Sales', fontsize=16, fontweight='bold')
plt.xlabel('Total Sales', fontsize=12)
plt.ylabel('Author Name', fontsize=12)  
plt.yticks(fontsize=10)

for index, value in enumerate(best_authors_sorted['gross sales']):
    plt.text(value + 1, index, str(round(value, 2)), ha='left', va='center', color='#333333', fontsize=8)


plt.tight_layout()
plt.show()


# <h5>3.Top 5 Authors based on Authors Rating <h5>

# In[337]:


#Goup by Author_Rating, counting the occurrences, and then selecting the top 5 authors for each 'Author_Rating' category.
top5_authors_by_rating = df_10.groupby('Author_Rating')['Author'].value_counts().groupby(level=0, group_keys=False).nlargest(5).reset_index(name='Count')
print(top5_authors_by_rating)


# In[338]:


#Choose color
author_colors = plt.cm.tab10.colors

# Pie for each category 
for rating_category in top5_authors_by_rating['Author_Rating'].unique():
    data_subset = top5_authors_by_rating[top5_authors_by_rating['Author_Rating'] == rating_category]
    
    plt.figure(figsize=(8, 8))
    plt.pie(data_subset['Count'], labels=data_subset['Author'], autopct='%1.1f%%', startangle=140, colors=author_colors)
    plt.title(f'Top 5 Authors for {rating_category} Rating')
    plt.tight_layout()
    plt.show()


# <h5>4.Top 10 lowest and highest price books <h5>

# <h5>Lowest<h5>

# In[339]:


top10_lowest_price_books = df_10.nsmallest(10, 'sale price')
print(top10_lowest_price_books[['Book Name', 'sale price']])


# In[340]:


#Plot
plt.figure(figsize=(12, 6))
bars = plt.bar(top10_lowest_price_books['Book Name'], top10_lowest_price_books['sale price'], color='blue')


for bar, price in zip(bars, top10_lowest_price_books['sale price']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f'{price:.2f}', ha='center', va='bottom', color='black')

plt.xlabel('Book Name')
plt.ylabel('Sale Price')
plt.title('Top 10 Books with Lowest Prices')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# <h5>Hightest<h5>

# In[341]:


top10_highest_price_books = df_10.nlargest(10, 'sale price')
print(top10_highest_price_books[['Book Name', 'sale price']])


# In[342]:


#Plot
plt.figure(figsize=(12, 6))
bars = plt.bar(top10_highest_price_books['Book Name'], top10_highest_price_books['sale price'], color='blue')

# Add text labels with sale prices on each bar
for bar, price in zip(bars, top10_highest_price_books['sale price']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{price:.2f}', ha='center', va='bottom', color='black')

plt.xlabel('Book Name')
plt.ylabel('Sale Price')
plt.title('Top 10 Books with Highest Prices')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# <h5>5. Language Preferences<h5>

# In[343]:


df_10['language_code'].unique()


# In[344]:


language_counts = df['language_code'].value_counts()

#Colors
author_colors = plt.cm.tab10.colors

# Create a pie and a box 
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Bar plot
language_counts.plot(kind='bar', color=author_colors, ax=ax1)

# Titles
ax1.set_xlabel('Language ')
ax1.set_ylabel('Count')
ax1.set_title('Language Preferences')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)  # Rotate x-axis labels for better readability

# Box with percentages
box_data = [(f'{code}: {count} ({percentage:.1f}%)') for code, count, percentage in zip(language_counts.index, language_counts, language_counts / language_counts.sum() * 100)]
ax2.text(0.5, 0.5, '\n'.join(box_data), fontsize=12, va='center', ha='center')

ax2.axis('off')

plt.tight_layout()
plt.show()


# <h5>Genre Preferences<h5>

# In[320]:


language_counts = df['genre'].value_counts()

#Colors
author_colors = plt.cm.tab10.colors

# Create a pie and a box 
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Bar plot
language_counts.plot(kind='bar', color=author_colors, ax=ax1)

#Titles
ax1.set_xlabel('Genre')
ax1.set_ylabel('Count')
ax1.set_title('Genre Preferences')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)  # Rotate x-axis labels for better readability

# Box with percentages
box_data = [(f'{code}: {count} ({percentage:.1f}%)') for code, count, percentage in zip(language_counts.index, language_counts, language_counts / language_counts.sum() * 100)]
ax2.text(0.5, 0.5, '\n'.join(box_data), fontsize=12, va='center', ha='center')

ax2.axis('off')

plt.tight_layout()
plt.show()


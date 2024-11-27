import pandas as pd
from urllib.parse import urlparse
import re

# Load the dataset
news_data = pd.read_csv(r'News_Data.csv')

# Sort the data by the 'Position' column in ascending order
news_data_sorted = news_data.sort_values(by='Position').reset_index(drop=True)

news_data.to_csv('updated_news_data.csv',index=False)

# Remove the 'UTC' part from the 'Date' column if present
news_data['Date'] = news_data['Date'].str.replace(' UTC', '', regex=False)

# Convert the cleaned 'Date' column to datetime format
news_data['Date'] = pd.to_datetime(news_data['Date'], format='%m/%d/%Y, %I:%M %p, %z')

# Create new columns for date and time separately
news_data['Extracted_Date'] = news_data['Date'].dt.date
news_data['Extracted_Time'] = news_data['Date'].dt.time

# Display the updated DataFrame with the new columns
print(news_data[['Date', 'Extracted_Date', 'Extracted_Time']].head())

news_data.to_csv('updated_news_data.csv',index=False)


# Function to extract the domain (netloc) from a URL
def extract_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return None

# Apply the function to extract domain from 'Source_Icon', 'Link', and 'Thumbnail' columns
news_data['Source_Icon_Domain'] = news_data['Source_Icon'].apply(extract_domain)
news_data['Link_Domain'] = news_data['Link'].apply(extract_domain)
news_data['Thumbnail_Domain'] = news_data['Thumbnail'].apply(extract_domain)

# Display the extracted domain columns
print(news_data[['Source_Icon', 'Source_Icon_Domain', 'Link', 'Link_Domain', 'Thumbnail', 'Thumbnail_Domain']].head())

news_data.to_csv('updated_news_data.csv',index=False)


# Clean text data in the 'Title' column by removing special characters and converting to lowercase
def clean_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

news_data['Title'] = news_data['Title'].apply(lambda x: clean_text(str(x)))

# Display cleaned text
print(news_data[['Title', 'Title']].head(20))

news_data.to_csv('updated_news_data.csv',index=False)

# Create the 'popularity_score' based on heuristics
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import numpy as np

# Calculate title length as a feature
news_data['title_length'] = news_data['Title'].apply(len)

# Encode source names for popularity (assuming each source has a general influence)
label_encoder = LabelEncoder()
news_data['source_encoded'] = label_encoder.fit_transform(news_data['Source_Name'])

# Calculate recency factor (days since publication from max date)
news_data['extracted_date'] = pd.to_datetime(news_data['Extracted_Date'])
max_date = news_data['extracted_date'].max()
news_data['recency_factor'] = (max_date - news_data['extracted_date']).dt.days

# Combine factors with weights to create a popularity score
# Weights are arbitrary and can be adjusted based on assumptions
news_data['popularity_score'] = (0.4 * news_data['title_length'] +
                          0.3 * news_data['source_encoded'] +
                          0.3 * (1 / (news_data['recency_factor'] + 1)))  # Avoid division by zero

# Normalize the popularity score to a 0-1 range
scaler = MinMaxScaler()
news_data['popularity_score'] = scaler.fit_transform(news_data[['popularity_score']])

# Display the first few rows to check the new popularity score
news_data[['Title', 'Source_Name', 'title_length', 'source_encoded', 'recency_factor', 'popularity_score']].head()

news_data.to_csv('updated_news_data.csv',index=False)
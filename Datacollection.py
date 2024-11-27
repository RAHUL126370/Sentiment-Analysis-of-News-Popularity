import pandas as pd

def combine_excel_sheets_to_csv(excel_files, News_Data):
    """
    Combines specified Excel sheets from different files into a single CSV file.

    """

    # Create an empty list to hold DataFrames
    dataframes = []

    # Loop through the list of Excel files
    for file in excel_files:
        # Read the Excel file into a DataFrame (assumes only one sheet per file)
        df = pd.read_excel(file)
        # Append the DataFrame to the list
        dataframes.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_data = pd.concat(dataframes, ignore_index=True)

    # Write the combined DataFrame to a CSV file
    combined_data.to_csv(News_Data, index=False)
    print(f"Data collected and saved to {News_Data}")

# Usage example
if __name__ == "__main__":
    # List of paths to your 9 Excel files
    excel_files = [
        "C:/Users/Rahul\Downloads/search-result-cricket.xlsx",
       "C:/Users/Rahul/Downloads/search-result-movies.xlsx",
       "C:/Users/Rahul/Downloads/search-result-elections.xlsx",
       "C:/Users/Rahul/Downloads/search-result-education.xlsx",
       "C:/Users/Rahul/Downloads/search-result-sports.xlsx",
       "C:/Users/Rahul/Downloads/search-result-india.xlsx",
       "C:/Users/Rahul/Downloads/search-result-health.xlsx",
       "C:/Users/Rahul/Downloads/search-result-football.xlsx",
       "C:/Users/Rahul/Downloads/search-result-foods.xlsx",
       "C:/Users/Rahul/Downloads/search-result-Animal.xlsx",
       "C:/Users/Rahul/Downloads/search-result-Multiple-Social-Media-Platforms.xlsx",
       "C:/Users/Rahul/Downloads/search-result-News-Popularity-Across-Multiple-Platforms.xlsx",
       "C:/Users/Rahul/Downloads/search-result-different-continent-happen-what.xlsx"
    ]
    
    News_Data = "C:/Users/Rahul/Documents/PROJECTS/Sentiment Analysis on News Popularity/News_Data.csv"  # Replace with your desired output file path
    
    combine_excel_sheets_to_csv(excel_files, News_Data)

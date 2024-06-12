# calgary_dogs.py
# Author: Rhys Wickens
#
# A terminal-based application for computing and printing statistics based on given input.

import pandas as pd

def main():

    # ***Import data here***
    all_data = pd.read_excel(r'CalgaryDogBreeds.xlsx')

    print("ENSF 692 Dogs of Calgary")


    # ***User input stage***

    # Asking users to input a dog breed, converting it to uppercase and then checking if it is in the data. 
    # If it's not, a KeyError is raised and they are asked to try again.
    while True:
        try:
            breed = input("Please enter a dog breed: ").upper()
            is_a_breed = breed in all_data['Breed'].values
            if(is_a_breed):
                break
            else:
                raise KeyError
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

    
    # ***Data anaylsis stage***

    # Find and print all years where the selected breed was listed in the top breeds.

    # I first mask the data for the given breed, and then find the unique years in this mask
    breed_mask = all_data[all_data['Breed'] == breed] # Here is the masking operation, as required by the README
    years_listed = breed_mask['Year'].unique()
    years_string = ' '.join(map(str, years_listed))
    print("The " + breed + " was found in the top breeds for years: " + years_string)

    # Calculate and print the total number of registrations of the selected breed found in the dataset.

    # I am first grouping the data by breed and summing the total number of breeds. I then ouput the total for the selected breed.
    total_by_breed = all_data.groupby('Breed')['Total'].sum() # Here is the first of several grouping operations and built in Panda computational methods, as required by the README
    total = total_by_breed[breed]
    print("There have been " + str(total) + " " + breed + " dogs registered total.")

    # Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).

    # I first group the total by year and breed and also just year.
    total_by_year_breed = all_data.groupby(['Year', 'Breed'])['Total'].sum() # Here is the multi-index Pandas DataFrame, as required by the README
    total_by_year = all_data.groupby('Year')['Total'].sum()

    #Next, I find the unique years that the breed has data available in
    idx = pd.IndexSlice # Here I am creating the IndexSlice object and using it in the loop below, as required by the README
    years = all_data['Year'].unique()

    # I loop through these years and divide the total for the given year and breed by the total for the given year.
    for year in years:
        if(year in years_listed):
            percent_by_year = total_by_year_breed.loc[idx[year, breed]] / total_by_year[year]
            print("The " + breed + " was " + '{:.{}f}%'.format((percent_by_year * 100), 6) + " of top breeds in " + str(year) + ".")
        else:
            print("The " + breed + " was not in the top breeds for " + str(year) + ".")

    # Calculate and print the percentage of selected breed registrations out of the total three-year percentage.

    # I am first getting the total registrations for all years, and then dividing the total by the selected breed by the overall total.
    total_registrations = all_data['Total'].sum()

    percent_of_total = total_by_breed[breed] / total_registrations
    print("The " + breed + " was " + '{:.{}f}%'.format((percent_of_total * 100), 6) + " of top breeds across all years.")

    # Find and print the months that were most popular for the selected breed registrations. Print all months that tie.

    # The logic I am using here is finding the months where the breed is in the top breeds data the most for the 3 years of data given.
    # To do so, I first create a dictionary of the number of months present in the data for the given dog breed and then sort this alphabetically.
    # Next, I find the months that are equal to the maximum value in this dictionary and print the result.
    month_counts = breed_mask['Month'].value_counts().to_dict()
    sorted_month_counts = dict(sorted(month_counts.items()))
    most_common_months = [month for month, count in sorted_month_counts.items() if count == max(sorted_month_counts.values())]
    most_common_months_string = ' '.join(most_common_months)
    print("Most popular month(s) for " + breed + " dogs: " + most_common_months_string)

if __name__ == '__main__':
    main()

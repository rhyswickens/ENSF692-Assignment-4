# calgary_dogs.py
# Author: Rhys Wickens
#
# A terminal-based application for computing and printing statistics based on given input.

import pandas as pd

def main():

    # Import data here
    all_data = pd.read_excel(r'CalgaryDogBreeds.xlsx')

    print("ENSF 692 Dogs of Calgary")

    # User input stage

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

    # Data anaylsis stage

    # Find and print all years where the selected breed was listed in the top breeds.

    breed_mask = all_data[all_data['Breed'] == breed] # Here is the masking operation, as required by the README
    years_listed = breed_mask['Year'].unique()
    years_string = ' '.join(map(str, years_listed))
    print("The " + breed + " was found in the top breeds for years: " + years_string)

    # Calculate and print the total number of registrations of the selected breed found in the dataset.

    total_by_breed = all_data.groupby('Breed')['Total'].sum() # Here is the first of several grouping operations and built in Panda computational methods, as required by the README
    total = total_by_breed[breed]
    print("There have been " + str(total) + " " + breed + " dogs registered total.")

    # Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).

    total_by_year_breed = all_data.groupby(['Year', 'Breed'])['Total'].sum() # Here is the multi-index Pandas DataFrame, as required by the README
    total_by_year = all_data.groupby('Year')['Total'].sum()

    idx = pd.IndexSlice # Here I am creating the IndexSlice object and using it in the loop below, as required by the README
    years = all_data['Year'].unique()

    for year in years:
        if(year in years_listed):
            percent_by_year = total_by_year_breed.loc[idx[year, breed]] / total_by_year[year]
            print("The " + breed + " was " + '{:.{}f}%'.format((percent_by_year * 100), 6) + " of top breeds in " + str(year) + ".")
        else:
            print("The " + breed + " was not in the top breeds for " + str(year) + ".")

    # Calculate and print the percentage of selected breed registrations out of the total three-year percentage.

    total_registrations = all_data['Total'].sum()

    percent_of_total = total_by_breed[breed] / total_registrations
    print("The " + breed + " was " + '{:.{}f}%'.format((percent_of_total * 100), 6) + " of top breeds across all years.")

    # Find and print the months that were most popular for the selected breed registrations. Print all months that tie.

    month_counts = breed_mask['Month'].value_counts().to_dict()
    sorted_month_counts = dict(sorted(month_counts.items()))
    most_common_months = [month for month, count in sorted_month_counts.items() if count == max(sorted_month_counts.values())]
    most_common_months_string = ' '.join(most_common_months)
    print("Most popular month(s) for " + breed + " dogs: " + most_common_months_string)

if __name__ == '__main__':
    main()

# ian cluett
# mat 375 module 7 project work
import pandas as pd
import math

# parameters
P0 = 158804397  # initial population
years_to_2022 = 2022 - 1950
years_to_2030 = 2030 - 1950
years_to_2015 = 2015 - 1950
r = 0.01078  # continuous growth rate
k = 800000000  # carrying capacity

total = 0
average = []
final_avg = 0

# set up time points
time_points = list(range(years_to_2022 + 1))


# here I did not need to include the K in the definition, but left it in for easy
# experimentation with other carrying capacities and comparing them on a single figure
# t: time index | K: carrying capacity
#def carrying_continuous(t, K):
#    A = (K - P0) / P0
#    return K / (1 + A * math.exp(-r * t))
def carrying_continuous(t, K):
    A = (K - P0) / P0
    return K / (1 + A * math.exp(-r * t))


# a: actual data | o: observed data
def percent_error(a, o): return ((o - a) / a) * 100


# calculate the estimated population into a list
continuous_pop_2022 = [carrying_continuous(t, k) for t in time_points]

# import and convert data from Excel file to lists (row 1: years | row 2: pop. data)
# the population data in the Excel file is listed as thousands, so this gets fixed
df = pd.read_excel("../populationdata.xlsx", header=None)
excel_years = df.iloc[0, :].tolist()
us_populations = df.iloc[1, :].tolist()
us_populations = [v * 1000 for v in us_populations]

estimates = (f"ESTIMATES:"
             f"\n2015: {round(carrying_continuous(years_to_2015, k), 4)}"
             f"\n2030: {round(carrying_continuous(years_to_2030, k), 4)}"
             f"\n============================="
             f"\nPERCENT ERRORS:\n")

with open("../CarryingCapacity/percent_errors_continuous_carrying.txt", "w") as file:
    file.write(estimates)
    for i in range(len(continuous_pop_2022)):
        # get data from Excel files and the calculated list
        year = int(excel_years[i])  # remove the .0
        actual = us_populations[i]
        observed = continuous_pop_2022[i]

        # calculate percent error
        error = percent_error(actual, observed)
        average.append(error)

        # print the error
        file.write(f"{year}: a:{round(actual, 3)} o:{round(observed, 3)} "
                   f"e: {round(error, 3)}% t: {i}\n")

    #for i in range(len(average)):
    #    total += average[i]
    #final_avg = total / len(average)
    #file.write(f"\nAverage Error: {round(final_avg, 3)}")

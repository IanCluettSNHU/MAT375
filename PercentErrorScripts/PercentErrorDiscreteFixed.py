# ian cluett
# mat 375 module 7 project work
import pandas as pd

# parameters
P0 = 158804397  # initial population
years_to_2022 = 72
growth_rate = 1.01078

total = 0
average = []
final_avg = 0

# set up time points
time_points = list(range(years_to_2022 + 1))


def exp_discrete(t): return P0 * (growth_rate ** t)


# a: actual data | o: observed data
def percent_error(a, o): return ((o - a) / a) * 100


# calculate the estimated population into a list
discrete_pop_2022 = [exp_discrete(t) for t in time_points]

# import and convert data from Excel file to lists (row 1: years | row 2: pop. data)
# the population data in the Excel file is listed as thousands, so this gets fixed
df = pd.read_excel("../populationdata.xlsx", header=None)
excel_years = df.iloc[0, :].tolist()
us_populations = df.iloc[1, :].tolist()
us_populations = [v * 1000 for v in us_populations]

estimates = (f"ESTIMATES:"
             f"\n1999: {round(exp_discrete(1999 - 1950), 4)}"
             f"\n2022: {round(exp_discrete(2022 - 1950), 4)}"
             f"\n2030: {round(exp_discrete(2030 - 1950), 4)}"
             f"\n============================="
             f"\nPERCENT ERRORS:\n")

with open("../FixedPercentage/percent_errors_discrete_fixed.txt", "w") as file:
    file.write(estimates)
    for i in range(len(discrete_pop_2022)):
        # read data from Excel files and the calculated list
        year = int(excel_years[i])
        actual = us_populations[i]
        observed = discrete_pop_2022[i]

        # calculate percent error
        error = percent_error(actual, observed)
        average.append(error)

        # print the error
        file.write(f"{year}: a:{round(actual, 3)} o:{round(observed, 3)} "
                   f"e: {round(error, 3)}% t: {i}\n")

    for i in range(len(average)):
        total += average[i]
    final_avg = total / len(average)
    file.write(f"\nAverage Error: {round(final_avg, 3)}")
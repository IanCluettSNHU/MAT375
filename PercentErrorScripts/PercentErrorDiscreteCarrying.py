# ian cluett
# mat 375 module 7 project work
import pandas as pd

# parameters
P0 = 158804397  # initial population
years_to_2022 = 2022 - 1950
years_to_2030 = 2030 - 1950
years_to_1999 = 1999 - 1950
growth_rate = 0.01078
k = 800000000

total = 0
average = []
final_avg = 0

# set up time points for the different years
time_points_2022 = list(range(years_to_2022 + 1))
time_points_1999 = list(range(years_to_1999 + 1))
time_points_2030 = list(range(years_to_2030 + 1))


# discrete carrying function uses a recursive formula rather than a time specific formula.
# it creates a list of numbers; pulling a specific date's population requires either running
# the function up to that year and indexing the last item on the list, or finding the index
# of a specific date in a previously run function's list.
# there are better ways to go about this, but I stuck with it for the sake of comparison to a continuous model
def carrying_discrete(t):
    population = [P0]
    growth = P0
    for j in range(1, len(t)):
        #Rt = population[-1]
        #growth = Rt * growth_rate * (1 - Rt / k)
        #population.append(Rt + growth)

        growth = growth + growth_rate * growth - (growth_rate / k) * (growth ** 2)
        population.append(growth)

    return population


# a: actual data | o: observed data
def percent_error(a, o): return ((o - a) / a) * 100


# calculate the estimated population into a list
discrete_pop_2022 = carrying_discrete(time_points_2022)

# import and convert data from Excel file to lists (row 1: years | row 2: pop. data)
# the population data in the Excel file is listed as thousands, so this gets fixed
df = pd.read_excel("../populationdata.xlsx", header=None)
excel_years = df.iloc[0, :].tolist()
us_populations = df.iloc[1, :].tolist()
us_populations = [v * 1000 for v in us_populations]

estimates = (f"ESTIMATES:"
             f"\n1999: {round(carrying_discrete(time_points_1999)[-1], 4)}"
             f"\n2022: {round(carrying_discrete(time_points_2022)[-1], 4)}"
             f"\n2030: {round(carrying_discrete(time_points_2030)[-1], 4)}"
             
             f"\n============================="
             f"\nPERCENT ERRORS:\n")

with open("../CarryingCapacity/percent_errors_discrete_carrying.txt", "w") as file:
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
                   f"e: {round(error, 3)}%\n")

    for i in range(len(average)):
        total += average[i]
    final_avg = total / len(average)
    file.write(f"\nAverage Error: {round(final_avg, 3)}")

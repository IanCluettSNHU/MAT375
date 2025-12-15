# ian cluett
# mat 375 module 7 project
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import math
import pandas as pd

# parameters
P0 = 158804397  # initial population
years_to_2022 = 2022 - 1950
r = 0.01078  # continuous growth rate
k = 800000000  # carrying capacity

# set up time points for calling the function, and the numbers for the x-axis
time_points = list(range(years_to_2022 + 1))
years_axis = [1950 + t for t in time_points]


# exact logistic function
def carrying_continuous(t, K):
    A = (K - P0) / P0
    return K / (1 + A * math.exp(-r * t))


def millions(x, pos): return f'{x/1e6:.1f}M'


# import and convert data from Excel file to lists (row 1: years | row 2: pop. data)
# the population data in the Excel file is listed as thousands, so this gets fixed
df = pd.read_excel("../populationdata.xlsx", header=None)
excel_years = df.iloc[0, :].tolist()
us_populations = df.iloc[1, :].tolist()
us_populations = [v * 1000 for v in us_populations]

# population list using specified function, up to 2022
continuous_pop_2022 = [carrying_continuous(t, k) for t in time_points]

# plots
plt.style.use('seaborn-v0_8')
plt.figure(figsize=(10, 6))

# discrete exponential 2015 and 2030
plt.plot(years_axis, continuous_pop_2022, linewidth=1, linestyle='--', color='purple', marker='o', markersize=4,
         label='Continuous Carrying Capacity Estimation (K = 800,000,000)')

# plot the US census data
plt.plot(excel_years, us_populations, linestyle='-', color='green', marker='s', markersize=4,
         label='Actual U.S. Population Data')

# plot labels, etc.
plt.title('Comparison of Continuous Carrying Capacity Model to Actual U.S. Population Data', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total U.S. Population', fontsize=12)
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.tick_params(axis='y', labelsize=10)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("../CarryingCapacity/continuous_carrying_comparison.jpg", dpi=300)
#plt.show()

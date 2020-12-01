# Python Libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 

# Local Imports
from connect import Budget, Accounts
from secrets import secret_key

# Get account list with api connection
headers = {"Authorization": 'Bearer {}'.format(secret_key)}
budget = Budget(headers)
accounts = Accounts(headers, budget.get_budget_id())
account_list = accounts.get_account_list()

# Find current networth and amount invested
networth = 0
invested = 0

for account in account_list:
	networth += account['balance'] / 1000
	if account['type'] == 'otherAsset':
		invested += account['balance'] / 1000

# Monte carlo simulation of investment growth
starting_val = invested
num_simulations = 1000
num_years = 25
num_years_withdraw = 50
withdraw = 100_000
yearly_return = .07
yearly_vol = .181
yearly_cont = 25_500

# Projections
simulation_df = pd.DataFrame()

for simulation in range(num_simulations):
	price_series = [starting_val]
	
	for year in range(num_years):
		price = price_series[year] * (1 + np.random.normal(yearly_return, yearly_vol)) + yearly_cont
		price_series.append(price)

	simulation_df[simulation] = price_series
 
# df of q% quantile
final_topten = simulation_df.quantile(q=.90, axis=1, numeric_only=True, interpolation='linear')
final_median = simulation_df.quantile(q=.50, axis=1, numeric_only=True, interpolation='linear')
final_bottomten = simulation_df.quantile(q=.10, axis=1, numeric_only=True, interpolation='linear')

# Create df of ending values
ending_values = simulation_df.values[-1].tolist()
ending_values.sort()
final_median_val = ending_values[num_simulations//2]

# Withdrals
simulation_df_with = pd.DataFrame()

for simulation in range(num_simulations):
	price_series_with = [final_median_val]
	
	for year in range(num_years_withdraw):
		price = price_series_with[year] * (1 + np.random.normal(yearly_return, yearly_vol)) - (withdraw)
		price_series_with.append(price)

	simulation_df_with[simulation] = price_series_with

# df of q% quantile
final_topten_with = simulation_df_with.quantile(q=.90, axis=1, numeric_only=True, interpolation='linear')
final_median_with = simulation_df_with.quantile(q=.50, axis=1, numeric_only=True, interpolation='linear')
final_bottomten_with = simulation_df_with.quantile(q=.10, axis=1, numeric_only=True, interpolation='linear')

# Create df of ending values
ending_values_with = simulation_df_with.values[-1].tolist()

# Create plots for projection
fig1, ax1 = plt.subplots(nrows=1, ncols=1)
fig2, ax2 = plt.subplots(nrows=1, ncols=1)
fig3, ax3 = plt.subplots(nrows=1, ncols=1)

ax1.plot(final_topten, label='90th percentile')
ax1.plot(final_median, label='50th percentile')
ax1.plot(final_bottomten, label='10th percentile')
ax1.legend()
ax1.set_yticklabels(['{:,}'.format(int(x)) for x in ax1.get_yticks().tolist()])
ax1.set_title('Top 10% - Median - Bottom 10%')

ax2.plot(simulation_df)
ax2.set_yticklabels(['{:,}'.format(int(x)) for x in ax2.get_yticks().tolist()])
ax2.set_title('All ({:,}) Simulations'.format(num_simulations))

ax3.hist(ending_values, density = True, bins=35, histtype='bar', range = (np.percentile(ending_values, 0), np.percentile(ending_values, 99)))
ax3.set_xticklabels(['{:,}'.format(int(x)) for x in ax3.get_xticks().tolist()])
plt.xticks(rotation=45)
ax3.set_title('Ending Balances')

# Create plots for pdf withdrawl
fig4, ax4 = plt.subplots(nrows=1, ncols=1)
fig5, ax5 = plt.subplots(nrows=1, ncols=1)
fig6, ax6 = plt.subplots(nrows=1, ncols=1)

ax4.plot(final_topten_with, label='90th percentile')
ax4.plot(final_median_with, label='50th percentile')
ax4.plot(final_bottomten_with, label='10th percentile')
ax4.legend()
ax4.set_yticklabels(['{:,}'.format(int(x)) for x in ax4.get_yticks().tolist()])
ax4.set_title('Top 10% - Median - Bottom 10%')

ax5.plot(simulation_df_with)
ax5.set_yticklabels(['{:,}'.format(int(x)) for x in ax5.get_yticks().tolist()])
ax5.set_title('All ({:,}) Simulations'.format(num_simulations))

ax6.hist(ending_values_with, density = True, bins=35, histtype='bar', range = (np.percentile(ending_values_with, 1), np.percentile(ending_values_with, 99)))
ax6.set_xticklabels(['{:,}'.format(int(x)) for x in ax6.get_xticks().tolist()])
plt.xticks(rotation=45)
ax6.set_title('Ending Balances')

plt.tight_layout()

# Save plots
fig1.savefig('./source/3quantiles.png', bbox_inches = "tight")
fig2.savefig('./source/allSimulations.png', bbox_inches = "tight")
fig3.savefig('./source/endingvalues.png', bbox_inches = "tight")
fig4.savefig('./source/3quantiles_with.png', bbox_inches = "tight")
fig5.savefig('./source/allSimulations_with.png', bbox_inches = "tight")
fig6.savefig('./source/endingvalues_with.png', bbox_inches = "tight")

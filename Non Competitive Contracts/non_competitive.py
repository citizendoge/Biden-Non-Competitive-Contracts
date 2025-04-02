import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV file
df = pd.read_csv('non_competitive.csv')

# Convert 'award_base_action_date' to datetime
df['award_base_action_date'] = pd.to_datetime(df['award_base_action_date'], errors='coerce')

# Create a new column 'unspent_amount'
df['unspent_amount'] = df['total_obligated_amount'] - df['total_outlayed_amount']

# Convert amount columns to numeric, coercing errors to NaN
df['total_obligated_amount'] = pd.to_numeric(df['total_obligated_amount'], errors='coerce')
df['total_outlayed_amount'] = pd.to_numeric(df['total_outlayed_amount'], errors='coerce')
df['unspent_amount'] = pd.to_numeric(df['unspent_amount'], errors='coerce')

# Filter the data by date range and unspent_amount > 0
start_date = '2024-11-06'
end_date = '2025-01-19'
df_filtered = df[(df['award_base_action_date'] >= start_date) & (df['award_base_action_date'] <= end_date) & (df['unspent_amount'] > 0)]

# Sort the DataFrame by 'unspent_amount' in descending order and 'award_base_action_date' in reverse chronological order
df_sorted = df_filtered.sort_values(by=['unspent_amount', 'award_base_action_date'], ascending=[False, False])

# Select the specified columns
columns_to_select = [
    'recipient_name', 'total_obligated_amount', 'total_outlayed_amount',
    'unspent_amount', 'award_base_action_date'
]
df_selected = df_sorted[columns_to_select]

# Return the top 20 rows
top_20_rows = df_selected.head(20)

# Print the result
print(top_20_rows)

# Print the total number of rows meeting the criteria
print(f"Total rows meeting the criteria: {len(df_filtered)}")

# Print the total sum of 'unspent_amount' across all filtered rows
total_unspent_sum = df_filtered['unspent_amount'].sum()
print(f"Total sum of unspent_amount: {total_unspent_sum}")

# Export the full filtered dataset to a CSV file
output_file = 'noncomp_filtered.csv'
df_selected.to_csv(output_file, index=False)
print(f"Filtered dataset exported to {output_file}")

# Load the filtered CSV file
df_filtered = pd.read_csv('noncomp_filtered.csv')

# Group by 'recipient_name' to calculate total unspent_amount and number of contracts
recipient_grouped = df_filtered.groupby('recipient_name').agg(
    total_unspent_amount=('unspent_amount', 'sum'),
    number_of_contracts=('recipient_name', 'size')
).reset_index()

# Sort the recipients by total unspent_amount in descending order
recipient_sorted = recipient_grouped.sort_values(by='total_unspent_amount', ascending=False)

# Select the top 10 recipients
top_10_recipients = recipient_sorted.head(10)

# Print the result
print(top_10_recipients)

# Function to format the x-axis labels as dollar values in millions
def format_millions(value, tick_number):
    return f'${value/1e6:.1f}M'

# Prepare data for plotting
top_10_recipients = recipient_sorted.head(10)

# Create a horizontal bar chart
plt.figure(figsize=(14, 8))
plt.barh(top_10_recipients['recipient_name'], top_10_recipients['total_unspent_amount'], color='skyblue')
plt.xlabel('Total Unspent Amount ($)')
plt.ylabel('Recipient Name')
plt.title('Top 10 Recipients by Total Unspent Amount\nTotal Contracts: 1,613 | Unique Recipients: 1,218 | Total Unspent: $712.3M', fontsize=14, ha='center', fontweight='bold', color='black')

# Add a subtitle below the chart title
plt.suptitle('Biden Lame Duck Period: Nov 6, 2024 – Jan 19, 2025', fontsize=12, ha='center', color='black')

# Set the x-axis limit to 50 million
plt.xlim(0, 50000000)

# Format the x-axis to show dollar values in millions
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_millions))

# Annotate each bar with the number of contracts
for index, value in enumerate(top_10_recipients['total_unspent_amount']):
    plt.text(value, index, f"{top_10_recipients['number_of_contracts'].iloc[index]} contracts", va='center', ha='left', fontsize=9)

# Invert y-axis to have the largest value on top
plt.gca().invert_yaxis()

# Adjust layout to prevent overflow
plt.tight_layout(pad=5)

# Add a footer at the bottom of the figure
plt.figtext(0.5, 0.01, 'Source: USAspending.gov | Filtered for non-competitive contracts with positive unspent amounts', ha='center', fontsize=10, color='black')

# Show the plot
plt.show()

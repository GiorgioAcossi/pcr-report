import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re


def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "-", filename)


def generate_bar_chart(labels_group1, values_group1, labels_group2, values_group2, title, output_file):
    # Create positions for the first 4 columns and shift the last 4 to create a gap between the groups
    x_group1 = np.arange(len(labels_group1))
    x_group2 = np.arange(len(labels_group2)) + len(labels_group1) + 2  # Add an empty space between the groups

    # Combine the positions and labels
    x_positions = np.concatenate([x_group1, x_group2])
    all_labels = np.concatenate([labels_group1, labels_group2])

    # Create the chart with a larger size
    fig, ax = plt.subplots(figsize=(12, 6))

    # Custom styles and colors for each bar
    colors = ['black', 'white', 'gray', 'white', 'black', 'white', 'gray', 'white']
    hatches = ['', '', '', '//', '', '', '', '//']

    # Create the bars
    bars = ax.bar(x_positions, np.concatenate([values_group1, values_group2]), color=colors, edgecolor='black')

    # Apply hatch patterns to the bars
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    # Chart title
    ax.set_title(title)

    # Set the X-axis labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(all_labels)

    # Disable vertical ticks below the bars
    ax.tick_params(axis='x', which='both', bottom=False)

    # Horizontal labels
    plt.xticks(rotation=0, ha="center")

    # Create the 'charts' directory if it doesn't exist
    output_dir = 'charts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Clean the filename to avoid invalid characters
    output_file = clean_filename(output_file)

    # Full path of the output file
    output_file = os.path.join(output_dir, output_file)

    # Save the chart as an image
    plt.tight_layout()
    plt.savefig(output_file)


def load_data_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Extract and organize data for each row
    charts_data = []
    for i, row in df.iterrows():
        chart_name = row.iloc[0]  # Use iloc for the first column to access the correct position
        labels_group1 = df.columns[1:5]  # Labels for the first group are in the first 4 columns
        values_group1 = row.iloc[1:5].tolist()  # Values for the first group
        labels_group2 = df.columns[5:]  # Labels for the second group are in the last 4 columns
        values_group2 = row.iloc[5:].tolist()  # Values for the second group

        charts_data.append({
            'chart_name': chart_name,
            'labels_group1': labels_group1,
            'values_group1': values_group1,
            'labels_group2': labels_group2,
            'values_group2': values_group2
        })

    return charts_data


def main():
    # Load the data from the input Excel file
    file_path = 'data.xlsx'  # Change this to your Excel file path
    charts_data = load_data_from_excel(file_path)

    for chart_data in charts_data:
        # Extract data from the dictionary
        labels_group1 = chart_data['labels_group1']
        values_group1 = chart_data['values_group1']
        labels_group2 = chart_data['labels_group2']
        values_group2 = chart_data['values_group2']
        chart_name = chart_data['chart_name']

        # Set the title and the output file name
        title = f"{chart_name}"
        output_file = f"{chart_name}.png"

        generate_bar_chart(labels_group1, values_group1, labels_group2, values_group2, title, output_file)


if __name__ == '__main__':
    main()

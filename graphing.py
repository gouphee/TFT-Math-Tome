import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as tri
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import numpy as np
from generic_calculator import Generic_Calculator


def generate_probabilities(maxDesired, maxDead, minTotal, maxTotal):
    probabilities = {}
    for desired in range(1, maxDesired + 1): # desired traits 1-4
        probabilities[desired] = []
        for dead in range(0, maxDead + 1): # dead traits 0-3
            for total in range(minTotal, maxTotal + 1):
                board = Generic_Calculator(desired, dead, total)
                probs = board.find_probability()
                probabilities[desired].append((desired, dead, total, probs))

    return probabilities

def pandify(probabilities):

    data = []
    for desired, entries in probabilities.items():
        for entry in entries:
            for i, prob in enumerate(entry[3]):  
                breakpoint = [0, 6, 8, 10, 12][i]
                data.append({
                    'Desired Traits': entry[0],
                    'Dead Traits': entry[1],
                    'Total Traits': entry[2],
                    'Breakpoint': breakpoint,
                    'Probability': prob
                })

    df = pd.DataFrame(data)

    return df

def plot_difference_subplot(ax, df, dead_traits_count, z_min, z_max, title_suffix):
    # Filter the DataFrame for the given number of dead traits
    df_filtered = df[(df['Total Traits'] >= 20) & (df['Total Traits'] <= 30) & (df['Dead Traits'] == dead_traits_count)]

    # Pivot the DataFrame to get a matrix for the 10 and 12 breakpoints
    df_pivot_10 = df_filtered[df_filtered['Breakpoint'] == 10].pivot(
        index='Desired Traits',
        columns='Total Traits',
        values='Probability'
    )
    df_pivot_12 = df_filtered[df_filtered['Breakpoint'] == 12].pivot(
        index='Desired Traits',
        columns='Total Traits',
        values='Probability'
    )

    # Calculate the difference between the 10 and 12 breakpoints
    df_difference = df_pivot_12 - df_pivot_10

    X, Y = np.meshgrid(df_difference.columns, df_difference.index)
    Z = df_difference.values

    # Normalize the colormap
    norm = colors.Normalize(vmin=z_min, vmax=z_max)

    # Plot the surface with normalized colormap
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', norm=norm, edgecolor='none')

    # Set the z-axis limits
    ax.set_zlim(z_min, z_max)

    # Set labels and titles
    ax.set_xlabel('Total Emblems')
    ax.set_ylabel('Desired Traits')
    ax.set_zlabel('Probability Difference')
    ax.set_title(f'Probability Difference with {title_suffix}')

    # Set the y-ticks to only show whole numbers
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    return surf

def prob_difference_graphs(df, totalTraits, firstBreak, secondBreak):
        # Filter the DataFrame for 23 total traits
    df_filtered = df[(df['Total Traits'] == totalTraits)]

    # Pivot the DataFrame to get a matrix for the 10 breakpoint
    df_pivot_1 = df_filtered[df_filtered['Breakpoint'] == firstBreak].pivot(
        index='Desired Traits',
        columns='Dead Traits',
        values='Probability'
    )

    # Pivot the DataFrame to get a matrix for the 12 breakpoint
    df_pivot_2 = df_filtered[df_filtered['Breakpoint'] == secondBreak].pivot(
        index='Desired Traits',
        columns='Dead Traits',
        values='Probability'
    )

    # Calculate the difference between the 10 and 12 breakpoints
    df_difference = df_pivot_1 - df_pivot_2

    # Assuming 'df_difference' is your DataFrame containing the difference in probabilities
    X, Y = np.meshgrid(df_difference.columns, df_difference.index)
    Z = df_difference.values

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Normalize the colormap
    norm = colors.Normalize(vmin=-Z.max(), vmax=Z.max())

    # Plot the surface with normalized colormap
    surf = ax.plot_surface(X, Y, Z, cmap='plasma', norm=norm, edgecolor='none')

    ax.set_zlim(-Z.max(), Z.max())

    # Set whole number ticks for the 'Dead Traits' (x-axis) and 'Desired Traits' (y-axis)
    ax.set_xticks(df_difference.columns)
    ax.set_yticks(df_difference.index)

    # Set labels and titles
    ax.set_xlabel('Dead Traits')
    ax.set_ylabel('Desired Traits')
    ax.set_zlabel(f'Probability Difference (Breakpoint {firstBreak} - Breakpoint {secondBreak})')
    ax.set_title(f'Smoothed 3D Surface Plot of Probability Difference {firstBreak} - {secondBreak}')

    # Add a color bar which maps values to colors
    cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
    cbar.set_label(f'Probability Difference (Breakpoint {firstBreak} - Breakpoint {secondBreak})')

    plt.show()

def main():
    probs = generate_probabilities(4, 3, 20, 30)
    df = pandify(probs)

    breakpoint_mapping = {0: 0, 6: 1, 8: 2, 10: 3, 12: 4}
    df['Evenly Spaced Breakpoints'] = df['Breakpoint'].map(breakpoint_mapping)


    # GRAPH 1
    # Filtering data for Graph 1
    df_graph_1 = df[(df['Desired Traits'] == 1) & (df['Dead Traits'] == 0)]

    # For Graph 1
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df_graph_1, x='Evenly Spaced Breakpoints', y='Probability', ci=None, marker='o')
    plt.title('Probabilities for 1 Desired Trait')
    plt.xticks(ticks=[0, 1, 2, 3, 4], labels=[0, 6, 8, 10, 12])  # Adjusted for even spacing
    plt.show()


    # GRAPH 2
    # Filtering data for Graph 2
    df_graph_2 = df[(df['Dead Traits'] == 0) & (df['Desired Traits'] <= 4)]

    # For Graph 2
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_graph_2, x='Evenly Spaced Breakpoints', y='Probability', hue='Desired Traits', style='Desired Traits', ci=None, marker='o')
    plt.title('Probabilities for Multiple Desired Traits')
    plt.xticks(ticks=[0, 1, 2, 3, 4], labels=[0, 6, 8, 10, 12])  # Adjusted for even spacing
    plt.show()

    # GRAPH 3
    # Filtering data for Graph 3: Probabilities for 1-4 desired traits and 0-3 dead traits
    df_graph_3 = df[(df['Desired Traits'] <= 4) & (df['Dead Traits'] <= 3) & (df['Total Traits'] == 23)]

    # Creating a FacetGrid to have separate plots for each number of dead traits
    g = sns.FacetGrid(df_graph_3, col="Dead Traits", hue="Desired Traits", col_wrap=2, height=4, aspect=1.5)
    g.map(sns.lineplot, "Evenly Spaced Breakpoints", "Probability", marker="o")

    # Adding titles and adjusting the axis
    g.set_titles("Dead Traits: {col_name}")
    g.add_legend(title="Desired Traits")
    g.set_axis_labels("Breakpoint", "Probability")

    breakpoint_labels = [0, 6, 8, 10, 12]
    for ax in g.axes.flatten():
        # Set the x-ticks to correspond to the actual data points
        ax.set_xticks(range(len(breakpoint_labels)))
        ax.set_xticklabels(breakpoint_labels)

    plt.show()

    # 3D GRAPH
    # Ensure 'Dead Traits' are integers if they are not already
    df_graph_3['Dead Traits'] = df_graph_3['Dead Traits'].astype(int)

    # Create a colormap based on the desired traits
    cmap = sns.color_palette("viridis", as_cmap=True)

    # Set up the figure and 3D axes
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the scatter plot in 3D using the new evenly spaced breakpoints
    sc = ax.scatter(
        df_graph_3['Evenly Spaced Breakpoints'],
        df_graph_3['Desired Traits'],
        df_graph_3['Probability'],
        c=df_graph_3['Dead Traits'],  # Color by dead traits, now as integers
        cmap=cmap,
        depthshade=False
    )

    # Set the labels of the axes
    ax.set_xlabel('Breakpoint')
    ax.set_ylabel('Desired Traits')
    ax.set_zlabel('Probability')

    # Set the title of the plot
    ax.set_title('3D Visualization of Probability Across Breakpoints')

    # Add a color bar to show the dead trait values
    cbar = fig.colorbar(sc, ax=ax, ticks=np.arange(df_graph_3['Dead Traits'].min(), df_graph_3['Dead Traits'].max()+1))
    cbar.set_label('Dead Traits')

    # Adjust the x-axis ticks to show the original breakpoints
    ax.set_xticks(range(len(breakpoint_mapping)))
    ax.set_xticklabels(list(breakpoint_mapping.keys()))

    # Remove the 0.5 increments from the y-axis gridlines by setting y-ticks to whole numbers
    ax.set_yticks(range(1, 5))

    # Show the plot
    plt.show()

    # 10 vs 12 difference graph
    prob_difference_graphs(df, 23, 10, 12)

    # 10 vs 12 difference graph
    prob_difference_graphs(df, 30, 10, 12)

    # 8 vs 12
    prob_difference_graphs(df, 23, 8, 12)

    # 8 vs 10
    prob_difference_graphs(df, 23, 8, 10)

    # 6 vs 8
    prob_difference_graphs(df, 23, 6, 8)


    # Assuming 'df' is your DataFrame with the probabilities
    fig = plt.figure(figsize=(14, 10))

    # Define the min and max for normalization
    z_min, z_max = -0.025, 0.025

    # Subplots for dead traits = 0, 1, 2, and 3
    axes = [fig.add_subplot(221, projection='3d'), fig.add_subplot(222, projection='3d'),
            fig.add_subplot(223, projection='3d'), fig.add_subplot(224, projection='3d')]

    surfs = []
    for i, ax in enumerate(axes):
        surfs.append(plot_difference_subplot(ax, df, i, z_min, z_max, f'Dead Traits = {i}'))

    # Color bar setup
    cbar = fig.colorbar(surfs[-1], ax=axes, shrink=0.5, aspect=12, pad=0.4)
    cbar.set_label('Probability Difference (Breakpoint 12 - Breakpoint 10)')

    # Adjust layout for proper spacing
    plt.subplots_adjust(left=0.1, right=.7, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)

    plt.show()

    # GRAPH LAST

    probs_last = generate_probabilities(8, 7, 23, 23)
    df_last = pandify(probs_last)
    # Filtering data for Graph 3: Probabilities for 1-4 desired traits and 0-3 dead traits
    df_last['Evenly Spaced Breakpoints'] = df_last['Breakpoint'].map(breakpoint_mapping)
    df_graph_last = df_last[(df_last['Desired Traits'] <= 8) & (df_last['Dead Traits'] <= 7) & (df_last['Total Traits'] == 23)]

    # Creating a FacetGrid to have separate plots for each number of dead traits
    g = sns.FacetGrid(df_graph_last, col="Dead Traits", hue="Desired Traits", col_wrap=2, height=4, aspect=1.5)
    g.map(sns.lineplot, "Evenly Spaced Breakpoints", "Probability", marker="o")

    # Adding titles and adjusting the axis
    g.set_titles("Dead Traits: {col_name}")
    g.add_legend(title="Desired Traits")
    g.set_axis_labels("Breakpoint", "Probability")

    breakpoint_labels = [0, 6, 8, 10, 12]
    for ax in g.axes.flatten():
        # Set the x-ticks to correspond to the actual data points
        ax.set_xticks(range(len(breakpoint_labels)))
        ax.set_xticklabels(breakpoint_labels)

    plt.show()

    # 3D GRAPH
    # Ensure 'Dead Traits' are integers if they are not already
    df_graph_last['Dead Traits'] = df_graph_last['Dead Traits'].astype(int)

    # Create a colormap based on the desired traits
    cmap = sns.color_palette("viridis", as_cmap=True)

    # Set up the figure and 3D axes
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the scatter plot in 3D using the new evenly spaced breakpoints
    sc = ax.scatter(
        df_graph_last['Evenly Spaced Breakpoints'],
        df_graph_last['Desired Traits'],
        df_graph_last['Probability'],
        c=df_graph_last['Dead Traits'],  # Color by dead traits, now as integers
        cmap=cmap,
        depthshade=False
    )

    # Set the labels of the axes
    ax.set_xlabel('Breakpoint')
    ax.set_ylabel('Desired Traits')
    ax.set_zlabel('Probability')

    # Set the title of the plot
    ax.set_title('3D Visualization of Probability Across Breakpoints')

    # Add a color bar to show the dead trait values
    cbar = fig.colorbar(sc, ax=ax, ticks=np.arange(df_graph_last['Dead Traits'].min(), df_graph_last['Dead Traits'].max()+1))
    cbar.set_label('Dead Traits')

    # Adjust the x-axis ticks to show the original breakpoints
    ax.set_xticks(range(len(breakpoint_mapping)))
    ax.set_xticklabels(list(breakpoint_mapping.keys()))

    # Remove the 0.5 increments from the y-axis gridlines by setting y-ticks to whole numbers
    ax.set_yticks(range(1, 9))

    # Show the plot
    plt.show()



if __name__ == "__main__":
    main()
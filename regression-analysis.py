#! /usr/bin/env python3

import os
import argparse
import sys
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import stats

#iris_df = pd.read_csv("iris.csv")

# Subset iris dataframe
#setosa = iris_df[iris_df.species == "Iris_setosa"]
#versicolor = iris_df[iris_df.species == "Iris_versicolor"]
#virginica = iris_df[iris_df.species == "Iris_virginica"]

# Write csv containing species-specific dataframes
#setosa.to_csv(path_or_buf="~/Dropbox/PhD/Classes/21_Spring/Scripting/python-exercises/python-tabular-data/setosa.csv")
#versicolor.to_csv(path_or_buf="~/Dropbox/PhD/Classes/21_Spring/Scripting/python-exercises/python-tabular-data/versicolor.csv")
#virginica.to_csv(path_or_buf="~/Dropbox/PhD/Classes/21_Spring/Scripting/python-exercises/python-tabular-data/virginica.csv")

def compose_plot_file_name(x_label, y_label, category_label = None):
    """
    Creates a name for a plot file based on the labels for the X, Y, and
    categorical variables.

    Parameters
    ----------
    x_label : str 
        The label for the X variable

    y_label : str 
        The label for the Y variable

    category_label : str 
        The label for the categorical variable. 

    Returns
    -------
    str
        The file name.
    """
    category_str = ""
    if category_label:
        category_str = "-by-{0}".format(category_label)
    plot_path = "{0}-v-{1}{2}.pdf".format(x_label, y_label,
            category_str)
    return plot_path

def get_regression_plot(dataframe, x_column, y_column,
        category_column_name = None,
        plot_path = None):
    """
    Generate a scatter plot from the data in `dataframe`
    -------------------------------------
    Parameters: 
    -------------------------------------
    dataframe : a pandas.core.frame.DataFrame
       A dataframe containing morphological measurements for a given species.
    x_column : str
        Name of column to be the predictor variable
    y_column : str
        Name of column to be the response variable
    category_column_name : str
        The name of the column used as a categorical variable. Can be used to split up the dataframe by rows for separate analysis. 
        


   Returns
   -------------------------------
   A scatterplot .png file showing the data with the regression of the x & y 
   variables plotted onto them.
    """
# If no plot path is provided, we will save the plot to the current working
    # directory and use the x and y column names for the file name
    if not plot_path:
        plot_path = compose_plot_file_name(x_column, y_column,
                category_column_name)

    # Break up the dataframe into groups based on the columm with the
    # categorical variable
    if category_column_name:
        grouped_dataframes = dataframe.groupby(category_column_name)
    else:
        # If no category column was provided we will plot all the data at once,
        # but we need to put the dataframe in a tuple of tuples so that the
        # `for` loop below will work
        grouped_dataframes = ('all', dataframe),

    # Get the min and max values of X to use for the regression lines
    # below
    xmin = min(dataframe[x_column])
    xmax = max(dataframe[x_column])

    # Loop over our grouped dataframes and plot the points and regression line
    color_index = 0
    for category, df in grouped_dataframes:
        x = df[x_column]
        y = df[y_column]
        regression = stats.linregress(x, y)
        slope = regression.slope
        intercept = regression.intercept
        plt.scatter(x, y, label = category, color = 'C' + str(color_index))

        # Get Y values predicted by linear regression for the min and max X
        # vlaues
        y1 = slope * xmin + intercept
        y2 = slope * xmax + intercept
        # Plot the regression line
        plt.plot((xmin, xmax), (y1, y2),
                color = 'C' + str(color_index))
        color_index += 1

    # Add labels and legend and save the plot
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.legend()
    plt.savefig(plot_path)

#def get_regression_plot(species)
#    """
#   Parameters
#   -------------------------------
#   species: pandas.core.frame.DataFrame
#       A dataframe containing morphological measurements for a given species.
#   Returns
#   -------------------------------
#   A scatterplot .png file showing the data with the regression of the x & y 
#   variables plotted onto them.
#   """
#    x = species.petal_length_cm
#    y = species.sepal_length_cm
#    regression = stats.linregress(x, y)
#    slope = regression.slope
#    intercept = regression.intercept   
#    plt.scatter(x, y, label = 'Data')
#    plt.plot(x, slope * x + intercept, color = "orange", label = 'Fitted line')
#    plt.xlabel("Petal length (cm)")
#    plt.ylabel("Sepal length (cm)")
#    plt.legend()
#    plt.savefig("petal_v_sepal_length_regress.png")
#    return 


def main_cli():
    """
    The main command-line interface for this script.

    The function takes no arguments and returns None.
    """
    # Create a command-line arg parser
    parser = argparse.ArgumentParser(
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # Add command-line arguments to our parser
    parser.add_argument('path',
            type = str,
            help = 'A path to a CSV file.')
    parser.add_argument('-x', '--x',
            type = str,
            default = "petal_length_cm",
            help = 'The column name to plot along the X axis.')
    parser.add_argument('-y', '--y',
            type = str,
            default = "sepal_length_cm",
            help = 'The column name to plot along the Y axis.')
    parser.add_argument('-c', '--category',
            type = str,
            default = "species",
            help = 'The column name to treat as a categorical variable.')
    parser.add_argument('-o', '--output-plot-path',
            type = str,
            default = "",
            help = 'The desired path of the output plot.')

    # Use our arg parser to parse the command-line args
    args = parser.parse_args()

    # Make sure the path to the CSV exists and is a file
    if not os.path.exists(args.path):
        msg = "ERROR: The path {0} does not exist.".format(args.path)
        sys.exit(msg)
    elif not os.path.isfile(args.path):
        msg = "ERROR: The path {0} is not a file.".format(args.path)
        sys.exit(msg)

    # An example of Python's try-except flow control
    try:
        dataframe = pd.read_csv(args.path)
    except Exception as e:
        msg = "Pandas had a problem reading {0}\n".format(args.path)
        sys.stderr.write(msg)
        raise e

    regress_and_scatter(dataframe, args.x, args.y,
            args.category, args.output_plot_path)


if __name__ == '__main__':
    main_cli()

#! /usr/bin/env python3

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

def get_regression_plot(species)
    """
    Parameters
    -------------------------------
    species: pandas.core.frame.DataFrame
        A dataframe containing morphological measurements for a given species.
    Returns
    -------------------------------
    A scatterplot .png file showing the data with the regression of the x & y 
    variables plotted onto them.
    """
    x = species.petal_length_cm
    y = species.sepal_length_cm
    regression = stats.linregress(x, y)
    slope = regression.slope
    intercept = regression.intercept   
    plt.scatter(x, y, label = 'Data')
    plt.plot(x, slope * x + intercept, color = "orange", label = 'Fitted line')
    plt.xlabel("Petal length (cm)")
    plt.ylabel("Sepal length (cm)")
    plt.legend()
    plt.savefig("petal_v_sepal_length_regress.png")
    return 

    #for taxon in species:
    #    get_regression_plot(taxon)

if __name__ == '__main__':
    main()
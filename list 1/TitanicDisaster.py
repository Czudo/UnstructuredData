import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 1 features in data set

data = pd.read_csv('train.csv')
data = data.replace('NaN', np.nan)
print(data.info())

# 2 cleaning data
data = data.set_index('PassengerId')
print(data.head())

# 3 pie chart

groupdata = data.groupby('Sex').count()
groupdata = groupdata['Survived']
plotPie = groupdata.plot.pie(figsize=(5, 5), legend=False, title='Male/female proportion')
#plt.show()

# 4 scatter plot

sns.pairplot(x_vars=["Fare"], y_vars=["Age"], data=data, hue="Sex", height=5)
plt.show()

# 5 survived

survived = data['Survived'].sum()
print(survived)

# 6 histogram

sns.distplot(data['Fare'])
plt.show()

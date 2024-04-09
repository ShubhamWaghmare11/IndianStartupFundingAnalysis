import pandas as pd

df=pd.read_csv('startup_cleaned.csv')

df.groupby('vertical')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = r'grupo06.csv'
data = pd.read_csv(file, skipinitialspace=True)
data2 = pd.read_csv(file, skipinitialspace=True)
data.drop_duplicates(keep='first', inplace=False)
data2.drop_duplicates(keep='first', inplace=True)
opa = data2['Performance']
del data2['Performance']
#Tratando itens faltantes

keys_list = list(data2.keys())

#substitui MDs por NaN
at_list = []
for i, row in data2.iterrows():
    for j in keys_list:
        if row.get(j) == 'MD':
            at_list.append([i,j])
for i in at_list:
    data2.set_value(i[0],i[1], np.NaN)

#conferindo se foram removidas
for i, row in data2.iterrows():
    for j in keys_list:
        if row[j] == 'MD':
            print(str(i)+" "+str(j))


#restaura a coluna Performance
data2['Performance'] = opa



#substituindo os nan por média de valores com categoria y
#Os valores nan se encontram nas colunas 'Quantitative Ability 1', 'Domain Skills 1', 'Analytical Skills 1'
#Portanto irei usar a média da coluna para preencher tais valores
'''
import math as mth
gg =[]
for i in at_list:
    gg.append(i[1])
gg = list(set(gg))
for h in gg:
    uu = data2[['Specialization in study',h]].groupby("Specialization in study")
    for i in at_list:
        key = data2.at[i[0], 'Specialization in study']
        val_list = list(uu.get_group(key)[i[1]].values)
        val_list = list(map(float, val_list))
        a_list = []
        for j in val_list:
            if not mth.isnan(j):
                a_list.append(j)
        media = sum(a_list)/len(a_list)

        data2.set_value(i[0],i[1], media)
    uu = None
'''
gg =[]
for i in at_list:
    gg.append(i[1])
gg = list(set(gg))
data2 = data2.apply(pd.to_numeric, errors='ignore')
for h in gg:
    data2[h].fillna(data2[h].mean(), inplace=True)




# Create an axes instance


# Create the boxplot

# Save the figure



def boxplots(column1, column2):
    oi = data[[column1, column2]].groupby(column1).boxplot(subplots=False, vert=False)
    groups = list(oi.groups.keys())

def getMean(column1, column2):
    oi = data[[column1, column2]].groupby(column1)
    groups = list(oi.groups.keys())

#tratando outliers
def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].sort_values().quantile(0.25)
    q3 = df_in[col_name].sort_values().quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    for i,row in data2.iterrows():
        if row[col_name] <fence_low:
            data2.at[i,col_name] = fence_low
        if row[col_name] >fence_high:
            data2.at[i,col_name] = fence_high
    return data2

#adequando todos os outliers do dataSet
#os outliers tiveram seus dados jogados para os limites do bp

#list_num é os nomes das colunas numerais
list_num = ["10th percentage", "12th percentage", "College percentage", "English 1", "English 2","English 3","English 4","Quantitative Ability 1", "Quantitative Ability 2", "Quantitative Ability 3", "Quantitative Ability 4","Domain Skills 1", "Domain Skills 2", "Domain Test 3", "Domain Test 4", "Analytical Skills 1", "Analytical Skills 2","Analytical Skills 3"]

#list_cat é os nomes das categóricas
list_cat = ["Name", "Month of Birth", "Year of Birth", "Gender", "State(Location)","10th Completion Year", "12th Completion Year", "Degree of study", "Specialization in study", "Year of Completion of college", "Performance"]
for i in list_num:
    data2 = remove_outlier(data2, i)

data2[["Gender", "Quantitative Ability 1"]].groupby("Gender").boxplot(subplots=True, vert=True)#,showfliers=False)

#histograma

data2.hist("English 1", by="Degree of study")
plt.show()

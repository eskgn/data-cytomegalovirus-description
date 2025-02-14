import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path = "Cytomegalovirus.xlsx"

df = pd.read_excel(path, header=0)

################## Regarder la structure de la base de données

print(df.head())

print(df.info())

print(df.columns)

################## Recodage des variables à l'aide de https://higgi13425.github.io/medicaldata/

df['sex'] = df['sex'].replace([0,1],["Female","Male"])
df['race'] = df['race'].replace([0,1],["African	American","White"])
df['diagnosis type'] = df['diagnosis type'].replace([0,1],["Lymphoid","Myeloid"])
df['prior radiation'] = df['prior radiation'].replace([0,1],["No","Yes"])
df['prior transplant'] = df['prior transplant'].replace([0,1],["No","Yes"])
df['recipient cmv'] = df['recipient cmv'].replace([0,1],["Negative","Positive"])
df['donor cmv'] = df['donor cmv'].replace([0,1],["Negative","Positive"])
df['donor sex'] = df['donor sex'].replace([0,1],["Female","Male"])
df['C1/C2'] = df['C1/C2'].replace([0,1],["Heterozygous","Homozygous"])
df['cmv'] = df['cmv'].replace([0,1],["No","Yes"])
df['agvhd'] = df['agvhd'].replace([0,1],["No","Yes"])
df['cgvhd'] = df['cgvhd'].replace([0,1],["No","Yes"])

################## Visualiser les variables graphiquement ainsi que numériquement afin de les décrire de manière adapté.
#En observant la comparaison entre la moyenne et la médiane, ainsi que le coefficient d'asymétrien et enfin l'observation graphique,
#on peut choisir les paramètres de dispersions et positions adaptés à la variable.

for column in df.columns:
    print(column)
    print(df[column].unique())
    if pd.api.types.is_numeric_dtype(df[column]):
        print("Médiane :", round(df[column].median(), 1))
        print("Variance :", round(df[column].var(),1))
        print("Premier quartile (Q1) :", round(df[column].quantile(0.25),1))
        print("Troisième quartile (Q3) :", round(df[column].quantile(0.75),1))
        print("Interquartile Range (IQR) :", round(df[column].quantile(0.75) - df[column].quantile(0.25),1))
        print("Moyenne :", round(df[column].mean(),1))
        print("Ecart type :", round(df[column].std(),1))
        print("Min :", df[column].min())
        print("Max :", df[column].max())
        print("Coefficient d'asymétrie :", df[column].skew())
        print("Interquartile Range (IQR) :", round(df[column].quantile(0.75) - df[column].quantile(0.25),1))
        sns.histplot(data=df,x=column,kde=True)
        plt.show()
    else:
        print(df[column].value_counts(normalize=True))
    print("--------------")


#Classement des différents variables après observation :
#Remarque : Malgré le recodage, il y a certaines variables qualitatives décrites numériquement : TBI dose "400" ou "200" ainsi que aKIRs qui correspond à des types de récepteurs

quant_median = ['age', 'time to transplant', 'prior chemo', 'CD34 dose','CD8 dose','time to cmv','time to agvhd','time to cgvhd']
quant_mean = ['TNC dose','CD3 dose']
qualitative = ['TBI dose','aKIRs','sex','race','diagnosis','diagnosis type','prior radiation','prior transplant','recipient cmv','donor cmv','donor sex','C1/C2','cmv','agvhd','cgvhd']

for column in quant_median:
    print(column)
    print("Médiane :", round(df[column].median(), 1))
    print("Premier quartile (Q1) :", round(df[column].quantile(0.25),1))
    print("Troisième quartile (Q3) :", round(df[column].quantile(0.75),1))
    print("Ecart interquartile (EIQ) :", round(df[column].quantile(0.75) - df[column].quantile(0.25),1))
    print("Min :", df[column].min())
    print("Max :", df[column].max())
    print("--------------")

for column in quant_mean:
    print(column)
    print("Moyenne :", round(df[column].mean(),1))
    print("Ecart type :", round(df[column].std(),1))
    print("Min :", df[column].min())
    print("Max :", df[column].max())
    print("Étendue :", round(df[column].max()-df[column].min(),1))
    print("--------------")

for column in qualitative:
    print(df[column].value_counts(normalize=True))
    print("Effectif:", df[column].count())
    print("Donnée manquante :",df[column].isna().sum())
    print("--------------")



#Quelques exemples de graphiques pouvant potentiellement montrer des corrélations 

# Infection au CMV en fonction de l'âge
plot = sns.boxplot(data=df,x='cmv', y='age')
plot.set(title="Infection au CMV en fonction de l'âge", xlabel="Infection au CMV (0 : Non, 1 : Oui)",ylabel="Âge")
plt.show()

# Relation entre la durée jusqu'à l'infection au CMV et les doses cellulaires
sns.scatterplot(x='time to cmv', y='CD34 dose', data=df, color='blue', label='CD34 dose')
sns.scatterplot(x='time to cmv', y='CD3 dose', data=df, color='green', label='CD3 dose')
sns.scatterplot(x='time to cmv', y='CD8 dose', data=df, color='red', label='CD8 dose')
plt.title("Relation entre la durée jusqu'à l'infection au CMV et les doses cellulaires")
plt.xlabel("Durée jusqu'à l'infection au CMV")
plt.ylabel("Dose cellulaire")
plt.legend()
plt.show()

# Durée jusqu'à l'infection au CMV en fonction du type de diagnostic
sns.boxplot(data=df,y='time to cmv',x='diagnosis type')
plt.title("Durée jusqu'à l'infection au CMV en fonction du type de diagnostic")
plt.xlabel("Type de diagnostic")
plt.ylabel("Durée jusqu'à l'infection au CMV")
plt.show()

# Comparaison des durée des types de GVHD en fonction des aKIRs
# Utilisation des données en format long
df2 = df.melt(id_vars=['aKIRs'], value_vars=['time to cgvhd', 'time to agvhd'], var_name='GVHD_Type', value_name='Time')
# Création du box plot
sns.boxplot(x='aKIRs', y='Time', hue='GVHD_Type', data=df2, palette='Set2')
plt.title('Comparaison des durée des types de GVHD en fonction des aKIRs')
plt.xlabel('Type aKIRs')
plt.ylabel('Temps')
plt.legend(title='Type de GVHD')
plt.show()
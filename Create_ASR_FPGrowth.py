import pandas as pd
import pyfpgrowth
import openpyxl
import os 
 


# Set up path
input_file_name = r'MO_18_to_60_M' # csv file only 
input_file_folder = r'C:\Users\earth\Desktop\701-FP_Growth\data'
output_file_name = 'rules_' + input_file_name
output_file_folder = r'C:\Users\earth\Desktop\701-FP_Growth\results'

input_file_path = os.path.join(input_file_folder,input_file_name + '.csv')
output_file_path = os.path.join(output_file_folder,output_file_name)

ruleFile = output_file_path + '.xlsx'
ruleFile_csv = output_file_path + '.csv'



# Load data to dataFrame
df = pd.read_csv(input_file_path)



# clean data (replace NaN with space)
df_list = df.values.tolist()

for idx_transaction in range(0,len(df_list)):
    curr_transaction = df_list[idx_transaction]
    temp_transaction = [x for x in curr_transaction if pd.isnull(x) == False ]
    df_list[idx_transaction] = temp_transaction

df_list_cleaned = df_list;



# Fit model 
minimum_support = len(df_list_cleaned)*0.001 # minimum support 0.1%
minimum_confident = 0.8 # 80%
print("amount of transactions = ",len(df_list_cleaned))
print("minimum support = ",minimum_support, "\nminimum confident = ", minimum_confident)
patterns = pyfpgrowth.find_frequent_patterns(df_list_cleaned, minimum_support) 
rules = pyfpgrowth.generate_association_rules(patterns, minimum_confident)


# Rename dataFrame's column
rules_data = pd.DataFrame(rules).T
rules_data = rules_data.rename(columns={0:'Consequent',1:'Confident'})


amountOfRules = len(rules)
print('amount of rules = ',amountOfRules)


if amountOfRules > 0:
    # Find Lift
    def support_count(each_consequent,df_list_cleaned):
        count = 0 
        each_consequent = set(each_consequent)
        for each_transaction in df_list_cleaned:
            each_transaction = set(each_transaction)
            if(each_consequent.issubset(each_transaction)):
                count = count+1
        return count

    consequent_support=[]
    for each_consequent in rules_data["Consequent"]:
        support_val = support_count(each_consequent,df_list_cleaned)
        consequent_support.append(support_val/len(df))
    rules_data['Consequent Support'] = consequent_support
    rules_data['Lift'] = rules_data['Confident']/rules_data['Consequent Support']


    print(rules_data)


    # Clean 'Consequent' col
    consequent_cleaned = []
    for i in rules_data['Consequent']:
        consequent_cleaned.append(''.join(i))

    rules_data['Consequent'] = consequent_cleaned


    rules_data.to_excel(ruleFile)
    rules_data.to_csv(ruleFile_csv)









# FOR TEST


transactions = [['Ant', 'Bear', 'Cat'],
                ['Ant', 'Bear'],
                ['Ant', 'Bear'],
                ['Ant', 'Cat', 'Elephant'],
                ['Rat', 'Bear'],
                ['R', 'Ant'],
                ['Ant', 'Rat'],
                ['Rat', 'Cat', 'Ant', 'Bear'],
                ['Ant', 'Cat', 'Elephant']]


patterns = pyfpgrowth.find_frequent_patterns(transactions, 3) # min sup

rules = pyfpgrowth.generate_association_rules(patterns, 0.7) # min conf

#print(patterns)
print('\n')
print(rules)
rules_data = pd.DataFrame(rules).T

rules_data.to_csv(r'C:\Users\earth\Desktop\Test_FP_DATAX_OutAnt.csv')
import pandas as pd
import pyfpgrowth
import os 
 
#### PLEAS READ "README.md" before using ####
#############################################

# Set up path
input_file_name = r'____Input file name (transaction file)____' # for example "A.csv" insert only "A". (csv file only)
input_file_folder = r'____Input folder____' # path to your input folder (where your input file is).
output_file_name = 'rules_' + input_file_name # you can modify this.
output_file_folder = r'___Output folder___' # path to your output folder.

# Set parameters (minimum support, minimum confident)
minimum_support_rate = 0.001 # 0.1%
minimum_confident = 0.8 # 80%


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
minimum_support = len(df_list_cleaned)*minimum_support_rate 
print("amount of transactions = ",len(df_list_cleaned))
print("minimum support = ",minimum_support, "\nminimum confident = ", minimum_confident)
patterns = pyfpgrowth.find_frequent_patterns(df_list_cleaned, minimum_support) 
rules = pyfpgrowth.generate_association_rules(patterns, minimum_confident)


# Rename dataFrame's column
rules_data = pd.DataFrame(rules).T
rules_data = rules_data.rename(columns={0:'Consequents',1:'Confidence'})


amountOfRules = len(rules)
print('amount of rules = ',amountOfRules)


if amountOfRules > 0:
    def support_count(each_consequent,df_list_cleaned):
        count = 0 
        each_consequent = set(each_consequent)
        for each_transaction in df_list_cleaned:
            each_transaction = set(each_transaction)
            if(each_consequent.issubset(each_transaction)):
                count = count+1
        return count

    consequent_support=[]
    rule_support = []

    # Find RHS Support value
    for each_consequent in rules_data["Consequents"]:
        support_rhs_val = support_count(each_consequent,df_list_cleaned)
        consequent_support.append(support_rhs_val/len(df_list_cleaned))

    
    # Find rule Support value
    for idx_each_rule in range(0,len(list(rules))):
        rule = list(rules)[idx_each_rule] + rules_data["Consequents"][idx_each_rule]
        support_rule_val = support_count(rule,df_list_cleaned)
        rule_support.append(support_rule_val/len(df_list_cleaned))

    rules_data['Support'] = rule_support


    # Find Lift value
    rules_data['Lift'] = rules_data['Confidence']/consequent_support



    print(rules_data)


    # Clean 'Consequents' col
    consequent_cleaned = []
    for i in rules_data['Consequents']:
        consequent_cleaned.append(''.join(i))

    rules_data['Consequents'] = consequent_cleaned


    rules_data.to_excel(ruleFile)
    rules_data.to_csv(ruleFile_csv)






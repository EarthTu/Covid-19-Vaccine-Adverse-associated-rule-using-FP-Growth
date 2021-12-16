# Covid-19-Vaccine-Adverse-associated-rule-using-FP-Growth
#### This code stands for generating association rules of Covid-19 Vaccine Adverse associated rule using FP-Growth.
#### For dataset template, please use some dataset in .... as an example.

# Getting Started
### Steps
#### In _"Create_ASR_FPGrowth.py"_
1. Setup your input/output path e.g. 
  *     input_file_name   (dataset file name. for example "A.csv" insert only "A")
  *     input_file_folder   (folder containing the datasets)
  *     output_file_name   (generated association rule file name [as you want]. Default is "rules_ + input_file_name")
  *     output_file_folder   (folder containing generated association rule file name [as you want])
> _**Note:** this version of code only works for CSV dataset input file. If you need to use it for other file types, you can modify the code as you need._

2. Set minimum support and minimum confident value 
   *     minimum support: default is 0.1% of all transaction (0.001)
   *     minimum confident: default is 80%  (0.8)

3. Run

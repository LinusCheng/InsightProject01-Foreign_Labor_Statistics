# InsightProject01-Foreign_Labor_Statistics

## Problem
A journalist wants to know the occupations and states with the most number of approved H1B visas. We need to build a system that tells Top 10 Occupations and Top 10 States for certified visa applications.

## Approach
I use Python 3 to conduct this project.<br>

First, I find all the files in the in the 'input' folder, and check if there is a proper csv file. If there is no file or more than one file, the system will raise an error. Second, we need the three columns: CASE_STATUS, WORKSITE_STATE , SOC_NAME, but they have different names in different csv files and their column indices are different, too. For example, 'CASE_STATUS' can be 'STATUS' and 'WORKSITE_STATE' can be 'LCA_CASE_WORKLOC1_STATE'. Hence, I made a list of all possible alternatives, and then save the indices of the columns of the current csv document. After I open the csv file. I read the first line to get the column indices. Then, I read the lines one by one, and split them into a list by semicolon. After the spliting, the element of each column can be reached by the indices we saved. <br>

I build two dictionaries to map the STATES or OCCUPATIONS to the numbers of certified cases. After we get the dictionaries, I use my function, "get_tops" to generate the top 10 STATES/OCCUPATIONS. The amounts will be return with the STATES/OCCUPATIONS. In the function, I make the input dictionary into a list with tuples. I firstly sort the list with the first element in the tuples so that it is alphabetical ordered. And then, I sort the list with the second element in the tuples so that it is rank by the amounts. Note that if the numbers of STATES/OCCUPATIONS is less than 10, the system will just return all the STATES/OCCUPATIONS.<br>

Next, I find the portions of the top 10. The portion of each STATE/OCCUPATION just the amount of that divided by total amount. My funtion, 'get_perc' will generate the result. Now, every information needed has been received. Records are exported as txt files.



## How to run
1. Download this Repo and extract the zip.
2. Make sure you have Python in your environment.
3. Open terminal or command line, and cd to the root of this repo. You will see "run.sh" in the folder.
4. Type the command $bash run.sh

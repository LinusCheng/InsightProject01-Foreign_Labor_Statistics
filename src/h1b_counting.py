import os

# Get the file_dir in the "input" folder
# If there is no file or more than one file, the system will raise an error
All_files = []
for file in os.listdir("./input"):
    if file.endswith(".csv"):
        file_dir = "./input/" + file
        All_files.append(file_dir)
if len(All_files) ==0:
    raise RuntimeError ("Please place a csv file in the input folder")
    
elif len(All_files) >1:
    raise RuntimeError ("Please input only one file at a time")
del All_files


# This funtion read the CSV file and extract the 3 columns: CASE_STATUS, WORKSITE_STATE , SOC_NAME
# Note that the names of the columns differ in different files of each year, so name alternatives are
# given in the list, "target" 
def find_loc_n_soc(file_dir):
    
    targets = ['CASE_STATUS','STATUS',
               'WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE', 'LCA_CASE_WORKLOC_STATE',
               'SOC_NAME','LCA_CASE_SOC_NAME']

    # Splited by the ";" Ignore the ";" inside quotation marks
    def split_outside(line):
        import csv
        for out in  csv.reader([line], quotechar='"', delimiter=';',quoting=csv.QUOTE_ALL):
            pass
        return out
    
    #If you don't want to use csv library    
    #def split_outside(line):
    #    out = []
    #    start = 0
    #    find  = False
    #    for loc, ch in enumerate(line):
    #        if ch == '"':
    #            find= not(find)
    #        if find == False and ch == ';':
    #            out.append(line[start:loc])
    #            start = loc+1
    #    out.append(line[start:loc])
    #    return out
    
    # Dictionary of CERTIFIED cases
    N_loca   = {}
    N_type   = {}
    # Dictionary of NON-CERTIFIED cases (Optional)
    N_loca_f = {}
    N_type_f = {}
    
    with open(file_dir, encoding='utf-8') as f:  
    
        # Get the titles 
        line0 = split_outside(f.readline())
        # Get the indices of the columns
        for i, it in enumerate(line0):
            if it == targets[0] or it == targets[1]:
                status    = i
            elif it == targets[2] or it == targets[3] or it == targets[4]:
                work_site = i
            elif it == targets[5] or it == targets[6]:
                soc_name  =i
        #Start reading records line by line
        for oneline in f:
            oneline = split_outside(oneline)
            
            # If the record is not completed, we just skip it
            if oneline[status]=="" or oneline[work_site]=="" or oneline[soc_name]=="":
                continue
    
            # Build CERTIFIED dictionary
            if oneline[status] == 'CERTIFIED':
                if oneline[work_site] not in N_loca:
                    N_loca[oneline[work_site]] = 1
                else:
                    N_loca[oneline[work_site]] +=1
                
                if oneline[soc_name] not in N_type:
                    N_type[oneline[soc_name]] = 1
                else:
                    N_type[oneline[soc_name]] +=1
                
            # Build NON-CERTIFIED dictionary (Optional)
            else:
                if oneline[work_site] not in N_loca_f:
                    N_loca_f[oneline[work_site]] = 1
                else:
                    N_loca_f[oneline[work_site]] +=1
                
                if oneline[soc_name] not in N_type_f:
                    N_type_f[oneline[soc_name]] = 1
                else:
                    N_type_f[oneline[soc_name]] +=1        

    return N_loca, N_type, N_loca_f, N_type_f

# Load data
N_loca, N_type, N_loca_f, N_type_f = find_loc_n_soc(file_dir)


# Find the top N
def get_tops(book,N):
    book2 = []
    book3 = []
    for key, value in book.items():
        book2.append((key, value))
    # Sorted by names first, then the counts
    book2 = sorted(book2, key=lambda tup: tup[0])
    book2 = sorted(book2, key=lambda tup: tup[1],reverse=True)
    book3 = book2[:N]
    #If we want to export top11 = top10 case, uncomment the following
    #i = N-1
    #while i  < len(book2)-1:
    #    if book2[N-1][1] == book2[i+1][1]:
    #        book3.append(book2[i+1])
    #    else:
    #        break
    #    i+=1
    return  book3   #   list(zip(*book3))[0]

Top_loca = get_tops(N_loca,10)
Top_type = get_tops(N_type,10)

#If you want to calculate pass rate of each state/industry, uncomment the following
#def pass_rate(Top_loca,N_loca_f):
#    perc= []
#    for loc, win in Top_loca:
#        
#        if loc in N_loca_f:
#            fail = N_loca_f[loc]
#        else:
#            fail = 0
#        perc_i = str(round(win / (win+fail)*100,1)) + '%'
#        perc.append([loc,perc_i])
#    return perc
#pass_loca = pass_rate(Top_loca,N_loca_f)
#pass_type = pass_rate(Top_type,N_type_f)


#Expert the portions of each state/industry 
def get_perc(Top_loca):
    perc = []
    total = 0
    for i, j in Top_loca:
        total+=j
    if total ==0:
        raise RuntimeError("There is no one who passed")
    for i, j in Top_loca:
        rate =  str(round((j/total*100),1))+ '%'
        perc.append([i,rate])
    return perc


perc_loca = get_perc(Top_loca)
perc_type = get_perc(Top_type)


# Create the "output: folder
if not os.path.exists('./output'):
    os.makedirs('./output')


# Write top_10_occupations.txt
with open('./output/top_10_occupations.txt','w+') as f:
    f.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
    if len(Top_type) <10:
        top_max =len(Top_type)
    else:
        top_max = 10
    for i in range(top_max):
        record_i = Top_type[i][0] + ";" + str(Top_type[i][1]) + ";" + perc_type[i][1] + "\n"
        f.write(record_i)
    
        
# Write top_10_states.txt
with open('./output/top_10_states.txt','w+') as f:
    f.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
    if len(Top_loca) <10:
        top_max =len(Top_loca)
    else:
        top_max = 10
    for i in range(top_max):
        record_i = Top_loca[i][0] + ";" + str(Top_loca[i][1]) + ";" + perc_loca[i][1] + "\n"
        f.write(record_i)



print("Completed")


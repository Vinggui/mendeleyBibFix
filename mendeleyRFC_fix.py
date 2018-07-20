import sys

# File default names
library_name = './library.bib'
rfc_txt_name = './rfc-ref.txt'
output_file_name = './RFCs.bib'


# This model works for abntex2cite
reference_model = """
@misc{{{tag},
  author = {{{author}}},
  title = {{{title}}},
  publisher = {{{rfc}, {doi}}},
  year = {{{month} {year}}},
  url = {{{url}}}
}}
"""






########################################## Do not change! ########################################################
# check inputs
if len(sys.argv) > 1:
    library_name = sys.argv[1]

if len(sys.argv) > 2:
    output_file_name = sys.argv[2]

# Get the experiment parameters for this char generator
try:
    lib_file = open(library_name,'r')
except:
    print("Failed to open library file!")
    exit()

try:
    rfc_file = open(rfc_txt_name,'r')
except:
    print("Failed to open rfc-ref.txt file!")
    exit()

try:
    output_file = open(output_file_name,'w+')
except:
    print("Failed to crete output file!")
    exit()

class reference_class:
    def __init__(self):
        self.author = ""
        self.title = ""
        self.std = ""
        self.rfc = ""
        self.doi = ""
        self.month = ""
        self.year = ""
        self.url = ""



class rfc_class:
    def __init__(self):
        self.tag = ""
        self.number = 0

    def __lt__(self, other):
        return self.number < other.number


techreport_input_counter = 0
techreport_output_counter = 0


rfc_input_list = []
rfc = rfc_class()
got_type = False
# Search for all rfc refs
for line in lib_file:
    if "@techreport" in line:
        if got_type == True:
            print("ERROR parsing input library")
            exit()
        begin = line.find("{")+1
        end = line.find(",")
        rfc.tag = line[begin:end]
        got_type = True

    if "number =" in line:
        if got_type == False:
            continue
        begin = line.find("{")+1
        end = line.find("}")
        rfc.number = int(line[begin:end])
        rfc_input_list.append(rfc)
        rfc = rfc_class()
        got_type = False
        techreport_input_counter += 1

# Sort this list for performance
rfc_input_list.sort()


# Search in RFC list
counter = 0
for line in rfc_file:
    rfc_number_div_pos = line.find(" |")
    rfc_number_start_pos = line.find("RFC")
    if rfc_number_start_pos < 0:
        continue

    rfc_number = int(line[rfc_number_start_pos+3:rfc_number_div_pos])

    if rfc_number == rfc_input_list[counter].number:
        ref = reference_class()

        # Get author
        start = line.find("| ",rfc_number_div_pos+2)+2
        end = line.find(", \"")
        authors = line[start:end].replace("., ",". and ")
        ref.author = authors.replace("and and","and")

        # Get title
        start = line.find("\"") + 1
        end = line.find("\",")
        ref.title = line[start:end]

        # Get std or rfc
        start = end + 3
        end = line.find(",", start)
        if "STD" in line[start:end]:
            ref.std = line[start:end]
        else:
            ref.rfc = line[start:end]

        # Get std or rfc
        if ref.std != "":
            start = end + 2
            end = line.find(",", start)
            ref.rfc = line[start:end]

        # Get doi
        start = end + 2
        end = line.find(",", start)
        ref.doi = line[start:end]

        # Get month and year
        start = end + 2
        end = line.find(",", start)
        date = line[start:end].split(" ")
        ref.month = date[0]
        ref.year = date[1]

        # Get url
        start = end + 3
        end = line.find(">.", start)
        date = line[start:end].split(" ")
        ref.url = date[0]

        # Create the output reference according to the model desired
        output_piece = reference_model.format(tag = rfc_input_list[counter].tag,
                                              author = ref.author,
                                              title = ref.title,
                                              rfc = ref.rfc,
                                              doi = ref.doi,
                                              url = ref.url,
                                              month = ref.month,
                                              year = ref.year)


        print(ref.rfc)
        # print(ref.author)

        output_file.write(output_piece)
        techreport_output_counter += 1

        counter += 1
        if len(rfc_input_list) <= counter:
            break

output_file.close()
rfc_file.close()
lib_file.close()

print("Process exited successfully!")
print("{} references found in {};\n{} references formatted to {}!".format(techreport_input_counter, library_name, techreport_output_counter, output_file_name))
output_file_name = "output.txt"
input_file_name = "results.txt"

inputFile = open(input_file_name, "r")

# SISTEMO IL FILE DI OUTPUT (operazione che potrebbe e dovrebbe essere fatta prima e non ora)

result = {}
for line in inputFile:
    lista = [ int(x) for x in line.split(", ") ] # car_id, ride_id
    if lista[0] in result.keys():
        result[lista[0]].append(lista[1])
    else:
        result[lista[0]] = [lista[1]]


inputFile.close()
outputFile = open(output_file_name, "w")

for car_id, ride_list in result.items():
    outputFile.write(str(len(ride_list)) + str(" ") )
    for id in ride_list:
        outputFile.write(str(id) + str(" "))
    outputFile.write("\n")

outputFile.close()
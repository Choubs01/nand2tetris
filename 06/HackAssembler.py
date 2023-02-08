import sys

#comp, dest, and jump for C instruction
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    } 


dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# symbols table
symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

for i in range(0,16): #R0..R15 symbol mapping
  label = "R" + str(i)
  symbols[label] = i


#Parser takes in text, and returns text with whitespace and comments (//) removed
def Parser(text):
    lines = text.split('\n')
    newLines = []

    for line in lines:
        if line == '' or line.startswith("//"):
            continue
        elif "//" in line:
            index = line.find("//")
            newLines.append(line[:index].strip())
        else:
            newLines.append(line.strip())

    return newLines

#Append all labels to their corresponding ROM address in symbols table
def FirstPass(text):
    ROMaddress = 0
    newText = []

    for elements in text:
        if elements.startswith("("):
            symbol = elements[1:-1]
            symbols[symbol] = ROMaddress
            ROMaddress -= 1
        else:
            newText.append(elements)
        ROMaddress += 1
    
    return newText

#Map each A instruction to it's corresponding symbols, and maps each variable to an available RAM address
def SecondPass(text):
    AvailableRAM = 16
    finalText = []
    for lines in text:
        if lines.startswith("@"): #Checks if A instruction
            A = lines[1:]
            if A in symbols: #Checks if string after @ is a saved symbol
                finalText.append("@" + str(symbols[A]))
            elif A[0].isdigit() == False: #If it doesn't start with a number then it must be a variable
                symbols[A] = AvailableRAM
                AvailableRAM += 1
                finalText.append("@" + str(symbols[A]))
            else: 
                finalText.append(lines)
        else:
            finalText.append(lines)

    return finalText



#returns binary form of c instruction
def CICoder(CInstruction):
    if CInstruction == 0: #1 off cases
        return "1110101010000111"
    elif CInstruction.startswith("0"):
        return "1110101010000111"

    #D;JGT 
    DCJ = ["null", "null", "null"] #Store dest, comp, jump
    if "=" in CInstruction and ";" in CInstruction:
        DCJ[0] = CInstruction[:CInstruction.find("=")]
        DCJ[1] = CInstruction[CInstruction.find("=")+1:CInstruction.find(";")]
        DCJ[2] = CInstruction[CInstruction.find(";")+1:]
    elif "=" in CInstruction:
        DCJ[0] = CInstruction[:CInstruction.find("=")]
        DCJ[1] = CInstruction[CInstruction.find("=")+1:]
    else:
        DCJ[1] = CInstruction[:CInstruction.find(";")]
        DCJ[2] = CInstruction[CInstruction.find(";")+1:]
    
    D = dest[DCJ[0]]
    C = comp[DCJ[1]]
    J = jump[DCJ[2]]
    
    return "111" + C + D + J
    
#Returns a list of A or C instructions converted to binary form            
def Code(codeList):
    binaryCode = []
    
    for code in codeList:
        if code.startswith("@"):
            binaryCode.append(f'{int(code[1:]):016b}') #Method for converting integer to binary called string interpolation
        else:
            binaryCode.append(CICoder(code))
    
    return binaryCode



def Assemble(filename):
    with open(filename, 'r') as f:
        text = f.read() 
        newText = Parser(text)
        newText = FirstPass(newText)
        newText = SecondPass(newText)
        Binary = Code(newText)

    with open(filename.replace(".asm", ".hack"), "w") as f:
        for number in Binary:
            f.write(number + "\n")


if __name__ == '__main__':
    filename = sys.argv[1]
    Assemble(filename)
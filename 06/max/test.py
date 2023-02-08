a = ['@R0', 'D=M', '@R1', 'D=D-M', '@OUTPUT_FIRST', 'D;JGT', '@R1', 'D=M', '@OUTPUT_D', '0;JMP', '(OUTPUT_FIRST)', '@R0', 'D=M', '(OUTPUT_D)', '@R2', 'M=D', '(INFINITE_LOOP)', '@INFINITE_LOOP', '0;JMP']
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

#Go through list, and for type of (XXX) turn it into symbol
def FirstPass(text):
    ROMaddress = 0

    for elements in text:
        if elements.startswith("("):
            symbol = elements[1:-1]
            symbols[symbol] = ROMaddress
            ROMaddress -= 1
        ROMaddress += 1

def SecondPass(text):
    AvailableRAM = 16
    finalText = []

    for lines in text:
        if lines.startswith("@"): #Checks if A instruction
            A = lines[1:]
            if A in symbols: #Checks if string after @ is a saved symbol
                finalText.append("@" + str(symbols[A]))
                print(A, lines)
            elif A[1].isdigit() == False: #If it doesn't start with a number then it must be a variable
                symbols[A] = AvailableRAM
                AvailableRAM += 1
                finalText.append("@" + str(symbols[A]))
            else: 
                finalText.append(lines)
    return finalText

FirstPass(a)
SecondPass(a)
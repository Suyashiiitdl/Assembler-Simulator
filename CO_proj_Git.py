registers = {'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'011','FLAGS':'111'}
opcode = {'add':'10000',
          'sub':'10001',
          'mul':'10110',
          'xor':'11010',
          'or':'11011',
          'and':'11100',
          'ld':'10100',
          'st':'10101',
          'div':'10111',
          'mov':'10011',   # of typeC(mov R1 R2)
          'rs':'11000',
          'ls':'11001',
          'not':'11101',
          'cmp':'11110',
          'jmp':'11111',
          'jlt':'01100',
          'jgt':'01101',
          'je':'01111',
          'hlt':'01010'}

lines = int(input("Lines :"))
data = []

filled_lines = 0
for i in range(0,lines):
    n = input().split(' ')
    
    if n == [' ']:
        continue
    data.append(n)
    
    filled_lines+=1

vars ={}
labels ={}
varCount = 0
prog_counter = 0

## variable and lables storing
for i in range(0,filled_lines):
    instruction = data[i]

    if instruction[0] == "var":
        prog_counter -= 1
        varCount += 1

    if instruction[0][-1] == ":":
        if len(instruction) < 2:
                    print(f"Error: Label instruction is Invalid in line {prog_counter +1 +varCount}")
                    continue
                    
        a = str(instruction[0][:-1])
        labels[a] = str(bin(prog_counter).replace("0b","").rjust(8,"0"))
    prog_counter+=1

for i in range(0,filled_lines):
    instruction = data[i]
    if instruction[0] == "var":
        if len(instruction)==1:
            print("ERROR: UNDEFINED VARIABLE")
        else:
            a = str(instruction[1])
            vars[a] = str(bin(prog_counter).replace("0b","").rjust(8,"0"))
            prog_counter+=1

##### Error checking#######

prog_counter = 1  
for i in range(0,filled_lines):
    op_name = opcode.keys()
    lable_name = labels.keys()
    
    if (data[i][0] not in op_name) and (data[i][0] != 'var') and (data[i][0][:-1] not in lable_name):
        print(f"Error: INVALID OPCODE INSTRUCTION in line {prog_counter}")
        #exit()

    
    if (i !=filled_lines - 1) and (data[i][0] == 'hlt'):
         print(f"Error: Halt instruction in between the program in line {prog_counter}")
         #exit()

    if data[filled_lines - 1][0] != 'hlt':
         print("Error: No Halt instruction in the end")
         #exit()
    prog_counter += 1


def main(n):
    
    global registers
    global opcode
    global labels
    global vars
    prog_count = 0
    reg_name = registers.keys()

    #Variables
    if n[0] == "var":
        prog_count += 1
        return

    #Labels
    lable_name = labels.keys()
    n1 = n[0][:-1]
    if (n1 in lable_name):
        prog_count += 1
        return
    
    # A_type 
    if len(n) == 4:
        instrA = ['add','sub','mul','xor','or','and']
        
        n1 = n[0]
        n2 = n[1]
        n3 = n[2]
        n4 = n[3]
        
        x1 = opcode.get(n[0])
        if (n1 not in instrA) :
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
        if (n2 not in reg_name) or (n3 not in reg_name) or (n4 not in reg_name):
            prog_count += 1
            return(f"Error: INVALID REGISTER NAME in line {prog_count}")
            
        x2 = registers.get(n[1])
        x3 = registers.get(n[2])
        x4 = registers.get(n[3])
        a = x1 + '00' + x2 + x3 + x4
        prog_count += 1
        return(a)

    #B_type
    if len(n) == 3 and n[2][0] == '$':
        instrB = ['mov','ls']

        if (n[1] not in reg_name):
            prog_count += 1
            return(f"Error: INVALID REGISTER NAME in line {prog_count}")
        
        n1 = n[0]
        if n1 == 'mov':
            x1 = '10010'
        else:    
            x1 = opcode.get(n[0])
        x2 = registers.get(n[1])
        x3 = n[2][1:]
        if n1 not in instrB:
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
            
        a = x3.isdigit()
        if a == False:
            prog_count += 1
            return(f"Error: INVALID VALUE ONLY WHOLE NUMBERS ARE VALID in line {prog_count}")          

        if int(float(x3))>255 or int(float(x3))<0:
            prog_count += 1
            return(f"Error: OVERFLOW FOR IMMEDIATE VALUE in line {prog_count}")
            
        z3 = ""
        y3 = str(bin(int(x3)))[2:]
        length = len(y3)
        for i in range(0,8-length):
            z3 = z3 + '0'
        z3 = z3 + y3
     
        a = x1 + x2 +z3
        prog_count += 1
        return(a)

    #D_type
    if len(n) == 3 and (n[0] == 'ld' or n[0] == 'st'):
        
        x1 = opcode.get(n[0])
        x2 = registers.get(n[1])

        if (n[1] not in reg_name):
            prog_count += 1
            return (f"Error: INVALID REGISTER NAME in line {prog_count}")
        
        var_name = vars.keys()
        if n[2] not in var_name:
            prog_count += 1
            return (f"Error: UNDEFINED VARIABLE in line {prog_count}")
        
        x3 = vars.get(n[2])
        a = x1 + x2 + x3
        prog_count += 1
        return a

    #C_type
    if len(n) == 3 and n[2][0] != '$':
        instrC = ['mov','div','not','cmp']
        n1 = n[0]
        x1 = opcode.get(n[0])
        x2 = registers.get(n[1])
        x3 = registers.get(n[2])


        if (n[1] not in reg_name) or ((n[2] not in reg_name)):
            prog_count += 1
            return (f"Error INVALID REGISTER NAME in line {prog_count}")

        if n1 not in instrC:
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
            
        a = x1 + '00000' +x2 + x3
        prog_count += 1
        return (a)
        
    #E_type
    instrE = ['jmp','jlt','jgt','je']
    if (len(n) == 2) and (n[0] in instrE):
        x1 = opcode.get(n[0])
        x2 = labels.get(n[1])
        
        lable_name = labels.keys()
        if n[1] not in lable_name:
            prog_count += 1
            return (f"Error: UNDEFINED LABLE in line {prog_count}")

        a = x1 + '000' + x2
        prog_count += 1
        return (a)
    
    #F_type
    if len(n) == 1:
        n1 = n[0]
        if n1 != 'hlt':
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
            
        a = '01010' + '00000000000'
        prog_count += 1
        return(a)
    else:
        prog_count += 1
        return(f"Error :Invalid Instruction in line {prog_count}")

binary = []

for i in data:
    a = main(i)
    binary.append(a)

for i in binary:
    if i == None:
        continue
    print(i)
    



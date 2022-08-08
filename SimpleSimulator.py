
memory = []
PC = 0

var_value = {}
regVal = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": "0"*16}



op_table = {"10000": "add", "10001": "sub", "10010": "mov_im", "10011": "mov", "10100": "ld", "10101": "st",
            "10110": "mul", "10111": "div", "11000": "rs", "11001": "ls", "11010": "xor", "11011": "or", "11100": "and",
            "11101": "not", "11110": "cmp", "11111": "jmp", "01100": "jlt", "01101": "jgt", "01111": "je",
            "01010": "hlt"}
flag_reset = "0"*16



cycle_number = -1
type={'add':'A','sub':'A','mov_im':'B','mov':'C','ld':'D','st':'D','mul':'A','div':'C','rs':'B','ls':'B','xor':'A','or':'A','and':'A','not':'C','cmp':'C','jmp':'E','jlt':'E','jgt':'E','je':'E','hlt':'F'}

def dumpmemory():
    for i in memory:
        print(i)


def GarbREG():
    x = convert(PC,8)
    print(x, end=" ")
    for i in regVal.keys():
        if(i!="111"):
            y = convert(regVal[i],places=16)
        else:
            y = regVal[i]
        print(y, end=" ")


def convert(val,places):
    y = int(val)
    x = bin(y).replace("0b", "")
    while len(x) < places:
        x = "0" + x
    return x





def invert_bin(val):
    x = int(val)
    y = bin(x).replace("0b", "")
    z = y[-16:]
    return z




def decode(instruction):
    op = instruction[0:5]
    opcode = op_table[op]
    return type[opcode]


def check_OF(data):
    if data < 0 or data >= pow(2,16):
       
        regVal["111"] = "0"*12 + "1000"
        return True
    else:
        return False





def main():
    Condition=True
    while Condition==True:
        data = ""
        try:
            data = input().rstrip()
            
    
            # change this
            if data != "":
                memory.append(data)
        except EOFError:
            break
    for i in range(len(memory), 256):
        memory.append("0"*16)
    
    halted = False
    global PC
    global cycle_number
    while not halted:
        instruction = memory[PC]
        cycle_number = cycle_number+1
        type = decode(instruction)
        if type == "F":
            halted = True
            
            GarbREG()
            print()
        elif type == "A":
            regVal["111"] = flag_reset
            r1 = instruction[7:10]
            r2 = instruction[10:13]
            r3 = instruction[13:]
            op = op_table[instruction[:5]]
            result = 0
            if op == "add":
                result = regVal[r1] + regVal[r2]
                if(check_OF(result)==1):
                    binary = invert_bin(result)
                    dec = int(binary,2)
                    regVal[r1] = dec
                else:
                    regVal[r3]=result
                    
            elif op == "sub":
                result = regVal[r1] - regVal[r2]
                if(check_OF(result)==1):
                    regVal[r3]=0
                else:
                    regVal[r3]=result
            elif op == "mul":
                result = regVal[r1] * regVal[r2]
                if(check_OF(result)==1):
                    binary = invert_bin(result)
                    dec = int(binary,2)
                    regVal[r3] = dec
                else:
                    regVal[r3]=result
            elif op == "xor":
                result = int(regVal[r1] ^ regVal[r2])
                if(check_OF(result)==1):
                    regVal[r3]=0
                else:
                    regVal[r3]=result
            elif op == "and":
                result = int(regVal[r1] and regVal[r2])
                if(check_OF(result)==1):
                    regVal[r3]=0
                else:
                    regVal[r3]=result
            elif op == "or":
                result = int(regVal[r1] or regVal[r2])
                if(check_OF(result)==1):
                    regVal[r3]=0
                else:
                    regVal[r3]=result
            GarbREG()
            print()
            PC =PC + 1

        elif type == "B":
            regVal["111"] = flag_reset
            r1 = instruction[5:8]
            IMMEDIATE = instruction[8:]
            IMMEDIATE = int(IMMEDIATE, 2)
            op = op_table[instruction[:5]]
            if op == "mov_im":
                regVal[r1] = IMMEDIATE
            elif op == "rs":
                regVal[r1] = int(regVal[r1]) >> IMMEDIATE
            elif op == "ls":
                regVal[r1] = int(regVal[r1]) << IMMEDIATE
            GarbREG()
            print()
            PC += 1

        elif type == "C":
            r1 = instruction[10:13]
            r2 = instruction[13:]
            op = op_table[instruction[:5]]
            if op == "mov":
                if r2 == "111":
                    regVal[r2] = int(regVal[r1], 2)
                else:
                    regVal[r2] = regVal[r1]
            elif op == "div":
                temp = regVal[r1]
                regVal["000"] = int(regVal[r1] / regVal[r2])
                regVal["001"] = int(temp % regVal[r2])
            elif op == "not":
                regVal[r2] = pow(2,16) - 1 - regVal[r1]
            elif op == "cmp":
                if int(regVal[r1]) > int(regVal[r2]):
                    regVal["111"] = "0"*12 + "0010"
                elif int(regVal[r1]) < int(regVal[r2]):
                    regVal["111"] = "0"*12 + "0100"
                elif int(regVal[r1]) == int(regVal[r2]):
                    regVal["111"] = "0"*12 + "0001"
            if op != "cmp":
                regVal["111"] = flag_reset
            GarbREG()
            print()
            PC += 1

        elif type == "D":
            regVal["111"] = flag_reset
            r1 = instruction[5:8]
            memory_add = instruction[8:]
            op = op_table[instruction[:5]]
            if op == "ld":
               
                regVal[r1] = int(memory[int(memory_add, 2)], 2)
            elif op == "st":
              
                memory[int(memory_add, 2)] = convert(regVal[r1],16)
            GarbREG()
            print()
            PC = PC + 1


        elif type == "E":
            label = instruction[8:]
            
            label_add = int(label,2)
            op = op_table[instruction[:5]]
            if op == "jmp":
                regVal["111"] = flag_reset
                GarbREG()
                print()
                PC = label_add
            elif op == "jlt":
                if regVal["111"][-3] == "1":
                    regVal["111"] = flag_reset
                    GarbREG()
                    print()
                    PC = label_add
                else:
                    regVal["111"] = flag_reset
                    GarbREG()
                    print()
                    PC = PC + 1
            elif op == "jgt":
                if regVal["111"][-2] == "1":
                    regVal["111"] = flag_reset
                    GarbREG()
                    print()
                    PC = label_add
                else:
                    regVal["111"] = flag_reset
                    GarbREG()
                    print()
                    PC = PC + 1
            elif op == "je":
                if regVal["111"][-1] == "1":
                    regVal["111"] = flag_reset
                    GarbREG()
                    print()
                    PC = label_add
                else:
                    regVal["111"] = flag_reset
                    GarbREG()
                    print()
                    PC = PC + 1
    dumpmemory()


if __name__ == "__main__":
    main()

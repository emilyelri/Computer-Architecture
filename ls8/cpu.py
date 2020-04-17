"""CPU functionality."""

import sys

# print("\n\nSYSTEM PARAMETERS", sys.argv, '\n\n')

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256                                                # our computer's RAM, currently empty
        self.reg = [0] * 8                                                  # the register, currently empty
        self.PC = 0                                                         # program counter, for keeping track of which command we are on
        
        self.SP = 7                                                         # stack pointer, reg[7] reserved for this
        self.reg[self.SP] = 0xf4                                            # initialze stack as empty per SPec

        self.branchtable = {}
        self.branchtable[0b01000111] = self.operand_PRN
        self.branchtable[0b10000010] = self.operand_LDI
        self.branchtable[0b10100010] = self.operand_MUL
        self.branchtable[0b01000101] = self.operand_PUSH
        self.branchtable[0b01000110] = self.operand_POP 

        self.branchtable[0b10100111] = self.operand_CMP

        self.branchtable[0b01010100] = self.operand_JMP
        self.branchtable[0b01010101] = self.operand_JEQ
        self.branchtable[0b01010110] = self.operand_JNE
  
        self.branchtable[0b01011010] = self.operand_JGE
        self.branchtable[0b01010111] = self.operand_JGT
        self.branchtable[0b01011001] = self.operand_JLE
        self.branchtable[0b01011000] = self.operand_JLT


        self.FL = [0] * 8                                                   # FLags



    def load(self):
        """Load a program into memory."""

        params = sys.argv
        if len(params) != 2:                                                # if no filename is passed
            print("usage: file.py filename")                                # print error and exit
            sys.exit(1)
        if len(params) == 2:                                                # if filename passed
            try:
                with open(params[1]) as f:                                  # read filename
                    address = 0
                    for line in f:                                          # for each line
                        comment_split = line.split("#")                     # SPlit at comments
                        num = comment_split[0].strip()                      # strip whiteSPace
                        if num == '':                                       # if line is blank, continue
                            continue
                        val = int("0b"+num,2)                               # otherwise convert oPCode to binary
                        self.ram_write(address, val)                        # write the op code to memory
                        address += 1                                        # increment the address to the next one in ram
            except FileNotFoundError:                                       # if try fails, filename doesn't exist
                print("ERROR: File not found")
                sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print(f"[{reg_a}]:{self.reg[reg_a]} CMP [{reg_b}]:{self.reg[reg_b]}")
        # print(f"[{reg_a}] CMP [{reg_b}]")

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        if op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]


        ## SPrint Challenge Code
        if op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL[5] = 0
                self.FL[6] = 0
                self.FL[7] = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL[5] = 1
                self.FL[6] = 0
                self.FL[7] = 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL[5] = 0
                self.FL[6] = 1
                self.FL[7] = 0

        else:
            raise Exception("Unsupported ALU operation")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.FL,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()



    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR



    def operand_LDI(self):
        self.reg[self.ram_read(self.PC+1)] = self.ram_read(self.PC+2)
        self.PC += 3

    def operand_PRN(self):
        print(self.reg[self.ram_read(self.PC+1)])
        self.PC += 2

    def operand_MUL(self):
        self.reg[self.ram_read(self.PC+1)]=(self.reg[self.ram_read(self.PC+1)] * self.reg[self.ram_read(self.PC+2)])
        self.PC +=3

    def operand_PUSH(self):
        self.reg[self.SP] -= 1                                              # decrement SP
        reg_num = self.ram[self.PC + 1]                                     # grab the next param
        value = self.reg[reg_num]                                           # set the index of that param in register to value
        self.ram[self.reg[self.SP]] = value                                 # copy the reg value into the ram
        self.PC += 2                                                        # increment the counter by 2 to next command
    def operand_POP(self):                                         
        value = self.ram[self.reg[self.SP]] 
        reg_num = self.ram[self.PC + 1]
        self.reg[reg_num] = value
        self.reg[self.SP] += 1                                              
        self.PC += 2


    # SPrint Challenge operands


    def operand_CMP(self):
        self.alu("CMP", self.ram[self.PC+1], self.ram[self.PC+2])
        self.PC += 3

    def operand_JMP(self):
        self.PC = self.reg[self.ram[self.PC + 1]]
    def operand_JEQ(self):
        if self.FL[7] == 1:
            self.PC = self.reg[self.ram[self.PC + 1]]
        else:
            self.PC += 2
    def operand_JNE(self):
        if self.FL[7] == 0:
            self.PC = self.reg[self.ram[self.PC + 1]]
        else:
            self.PC += 2

    def operand_JGE(self):
        if self.FL[6] == 1 or self.FL[7] == 1:
            self.PC = self.ram[self.PC + 1]
        else:
            self.PC += 2
    def operand_JGT(self):
        if self.FL[6] == 1:
            self.PC = self.reg[self.PC + 1]
        else:
            self.PC += 2
    def operand_JLE(self):
        if self.FL[5] == 1 or self.FL[7] == 1:
            self.PC = self.reg[self.PC + 1]
        else:
            self.PC += 2
    def operand_JLT(self):
        if self.FL[5] == 1:
            self.PC = self.reg[self.PC + 1]
        else:
            self.PC += 2


    def run(self):
        """Run the CPU."""
        
        # commands
        HLT = 0b00000001
        CALL = 0b01010000
        RET = 0b00010001

        running = True                                                      # for loop control, runs while running is True
        while running:
            command = self.ram_read(self.PC)                                # grabs current command using PC
            # print(f"{self.PC}:  {command}")

            if command == HLT:                                              # if the command is to halt, stops the loops
                running = False

            elif command == CALL:
                return_address = self.PC + 2
                self.reg[self.SP] -=1
                self.ram[self.reg[self.SP]] = return_address
                reg_num = self.ram[self.PC + 1]
                self.PC = self.reg[reg_num]

            elif command == RET:
                self.PC = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                
            else:
                self.branchtable[command]()                                 # otherwise runs the function from the corroSPonding command in the branchtable



"""CPU functionality."""

import sys

print(sys.argv)

# OP codes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.PC = 0

    def load(self, filename):
        """Load a program into memory."""

        if len(sys.argv) != 2:                                                # if there aren't the correct num of args passed
            print("usage: file.py filename")
            sys.exit(1)

        filename = sys.argv[1]                                                # grab program from args

        try:
            address = 0
            with open(filename) as program:
                for line in program:
                    no_comments = line.split('#')                                 # remove comments
                    value = no_comments[0].strip()                                # grab the number

                    if value != "":                                         # ignore whitespace
                        instruction = int(value, 2)                         # convert to binary
                        self.ram_write(address, instruction)                # set the instruction to the address in ram
                        address += 1                                        # inc address
                    else:
                        continue
        except FileNotFoundError:                                           # if try fails, FileNotFoundError and exit
            print("ERROR: file not found")
            sys.exit(1)








    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")






    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
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











    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if IR == HLT:
                running = False

            else:
                num_operands = IR >> 6
                print(num_operands)

                if IR == LDI:
                    self.ram_write(operand_a, operand_b)
                    self.PC += 3
                elif IR == PRN:
                    self.ram_read(operand_a)
                    self.PC += 2
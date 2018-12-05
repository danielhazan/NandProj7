import os
import sys

import re
from CodeWriter import *

class Parser:

    def __init__(self):
        """constructor: holds an instance of CodeWriter ( which consist the main translaring methods),
        and the VMTextLines- the list containing the original VM lines before translation"""
        self.codeWriter = CodeWriter()
        self.__translated_text = [] #the asm lines after translation by the CodeWriter
        self.VMTextLines = [] #the original VM lines to be translated


    def returnVMCode(self):
        return self.__translated_text


    def parsingProcess(self, vmFile,filename):
        self.VMTextLines = vmFile
        # passing on vmFile for erasing comments and spaces and detecting command types:
        # Push commands , Pop commands or Arithmetic commands
        for line in self.VMTextLines:
            line = line.strip()
            if len(line)>0: #clear comments from each line if it is not empty

                CommandSegment = line.split()
                CommandType = CommandSegment[0]
                if CommandType == '//':
                    continue
                if CommandType == "push":
                    CodeSegment = CommandSegment[1]
                    ValueToPush = CommandSegment[2]
                    VmToAsm = self.codeWriter.writePush(CodeSegment, ValueToPush,filename)
                    self.__translated_text.append(VmToAsm)
                elif CommandType == "pop":
                    CodeSegment = CommandSegment[1]
                    OffsetIndexToStore  = CommandSegment[2]
                    VmToAsm = self.codeWriter.writePop(CodeSegment, OffsetIndexToStore, filename)
                    self.__translated_text.append(VmToAsm)
                else:
                    # if command is not pop or push it must be Arithmetic
                    VmToAsm = self.codeWriter.writeArithmetic(CommandType)
                    self.__translated_text.append(VmToAsm)



def Main():
    """run the main loop"""

    MyParser = Parser()

    Arguments = sys.argv[1].strip()

    if os.path.exists(Arguments):
        if os.path.isdir(Arguments): # if source path is a folder
            files_in_folder = os.listdir(Arguments)
            for file in files_in_folder:
                file_name = file
                if file.endswith(".vm"):# open only files ending with "vm"
                    AbsolutePath = os.path.join(Arguments,file)
                    with open(AbsolutePath, 'r') as VMfile:
                        MyParser.parsingProcess(VMfile,file_name) #parsing each VM file
                        VMCode = MyParser.returnVMCode()
                        # now write the VMCode to an output asm file
                        new_ASM_file = Arguments.replace(".vm", ".asm")
                        with open(new_ASM_file, 'w') as ASMConvertedFile:
                            for line in VMCode:
                                ASMConvertedFile.write(line + '\n')

        else: #enter only if source path is an absolute path to a file
            file_name = os.path.basename(Arguments)
            with open(Arguments, 'r') as VMfile:
                MyParser.parsingProcess(VMfile,os.path.basename(Arguments))
                VMCode = MyParser.returnVMCode()
                #now write the VMCode to an output asm file
                new_ASM_file = Arguments.replace(".vm", ".asm")
                with open(new_ASM_file,'w') as ASMConvertedFile:
                    for line in VMCode:
                        ASMConvertedFile.write(line[0] )

    def getFile_name():
        return file_name

if __name__ == '__main__':
        Main()

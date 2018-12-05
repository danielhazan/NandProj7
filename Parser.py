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
        self.first = True

    def returnVMCode(self):
        return self.__translated_text


    def parsingProcess(self, vmFile,filename, sys_exist):
        self.VMTextLines = vmFile
        # passing on vmFile for erasing comments and spaces and detecting command types:
        # Push commands , Pop commands or Arithmetic commands
        self.__translated_text = []
        if self.first and sys_exist:
            self.__translated_text.append(self.codeWriter.writeInit())
            self.first = False

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
                #function call commands -->
                elif CommandType == "function":
                    function_name = CommandSegment[1]
                    numArgs = CommandSegment[2]
                    VmToAsm = self.codeWriter.writeFunction(function_name, numArgs)
                    self.__translated_text.append(VmToAsm)
                elif CommandType == "return":
                    VmToAsm = self.codeWriter.writeReturn()
                    self.__translated_text.append(VmToAsm)
                elif CommandType == "call":
                    function_name = CommandSegment[1]
                    numArgs = CommandSegment[2]
                    VmToAsm = self.codeWriter.writeCall(function_name,numArgs)
                    self.__translated_text.append(VmToAsm)
                elif CommandType == "init":
                    VmToAsm = self.codeWriter.writeInit()
                    self.__translated_text.append(VmToAsm)

                #program flow (branching) commands -->
                elif CommandType == "label":
                    label = CommandSegment[1]
                    VmToAsm = self.codeWriter.writeLabel(label)
                    self.__translated_text.append(VmToAsm)
                elif CommandType == "goto":
                    label = CommandSegment[1]
                    VmToAsm = self.codeWriter.writeGoto(label)
                    self.__translated_text.append(VmToAsm)
                elif CommandType == "if-goto":
                    label = CommandSegment[1]
                    VmToAsm = self.codeWriter.writeIf(label)
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
            sys_exist = False
            if "Sys.vm" in files_in_folder:
                sys_exist = True
            for file in files_in_folder:
                if file.endswith(".vm"):# open only files ending with "vm"
                    file_name = file
                    AbsolutePath = os.path.join(Arguments,file)
                    with open(AbsolutePath, 'r') as VMfile:
                        MyParser.parsingProcess(VMfile,file_name,sys_exist) #parsing each VM file
                        VMCode = MyParser.returnVMCode()
                        # now write the VMCode to an output asm file
                        temp = Arguments.strip("\\")
                        new_ASM_file = temp + "\\" + os.path.basename(temp) + ".asm"
                        with open(new_ASM_file, 'a') as ASMConvertedFile:
                            for array in VMCode:
                                for subarray in array:
                                    ASMConvertedFile.write(subarray )

        else: #enter only if source path is an absolute path     to a file

            file_name = os.path.basename(Arguments)
            with open(Arguments, 'r') as VMfile:
                sys_exist = False
                if file_name == "Sys.vm":
                    sys_exist = True
                MyParser.parsingProcess(VMfile,os.path.basename(Arguments),sys_exist)
                VMCode = MyParser.returnVMCode()
                #now write the VMCode to an output asm file
                new_ASM_file = Arguments.replace(".vm", ".asm")
                with open(new_ASM_file,'w') as ASMConvertedFile:
                    for array in VMCode:
                        for subarray in array:
                            ASMConvertedFile.write(subarray )
    def getFile_name():
        return file_name

if __name__ == '__main__':
        Main()

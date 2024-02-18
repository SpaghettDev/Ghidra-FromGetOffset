## ###
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
##
# Simple script that get the offset of an address, or gets the address from an offset
##
# @category: Python.Offsets
# @author: SpaghettDev

from subprocess import Popen, PIPE
from os import system


class OSNotSupported(BaseException):
    """Raised when the OS is not supported"""
    def __init__(self):
        super(OSNotSupported, self).__init__(
            "Your OS is not Windows, Linux nor MacOS. "
            "Please consider opening an issue on GitHub.\n"
            "For now, the offset/address has been printed to the console."
        )


# Splits a 16 bit int into two 8 bit integers
split_bits = lambda x: ((x >> 8) & 0xff, x & 0xff)


def get_offset(address):
    """Gets the offset of 'address'"""
    return hex(address - int(currentProgram.getImageBase().getOffset())).replace("L", "")


def from_offset(offset):
    """Gets the address of 'offset'"""
    return hex(offset + int(currentProgram.getImageBase().getOffset())).replace("L", "")


def copy_to_clip(text):
    """Copies 'text' to the clipboard.
    Mess of a code because os.name returns Java, so can't say
    for sure what OS is running the script"""
    def _windows_copy(text):
        # clip.exe instead of clip because WSL
        return system("echo | set /p nul={}| clip.exe".format(text.strip()))

    def _linux_copy(text):
        p = Popen(["xsel", "-pi"], stdin=PIPE)
        p.communicate(input=bytes(text, encoding="utf-8"))
        return p.returncode

    def _darwin_copy(text):
        p = Popen("pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=PIPE)
        p.communicate(text.encode("utf-8"))
        return p.returncode


    # 0 means success
    if split_bits(_windows_copy(text))[0] == 0:
        return
    if _linux_copy(text) == 0:
        return
    if _darwin_copy(text) == 0:
        return 

    print text
    raise OSNotSupported()


try:
    choice = askChoice("Get/From Offset", "Please choose one", [ "Get Offset", "From Offset" ], "Get Offset")

    if choice == "Get Offset":
        choice2 = askChoice("Get/From Offset", "Please choose one", [ "Current Address", "Custom Address" ], "Current Address")
        addr = hex(int(currentLocation.getAddress().getOffset())).replace("L", "")
        if choice2 == "Custom Address":
            addr = askString("Get Offset", "Enter the address: ")
        popup("Offset: {}".format(get_offset(int(addr, 0))))
        copy_to_clip(get_offset(int(addr, 0)))
    else:
        offset = askString("From Offset", "Enter the offset: ", "0x")
        popup("Address: {}".format(from_offset(int(offset, 0))))
        copy_to_clip(from_offset(int(offset, 0)))
except ghidra.util.exception.CancelledException:
    pass
except ValueError:
    popup("Please enter a valid offset!")

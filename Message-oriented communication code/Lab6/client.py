import os
import socket
import sys

files = [sys.argv[1]]
ip = sys.argv[2]
port = sys.argv[3]
s = socket.socket()
s.connect((ip, int(port)))
size = 0
for i in files:
    size = os.path.getsize(i) + size

transmitted = 0
print("0%")
for i in files:
    f = open(i, "rb")
    name = i + "!!!"
    end = "/-/--/-/"
    bin_name = str.encode(name)
    bin_end = str.encode(end)
    length_1 = len(bin_name)
    length_2 = len(bin_end)
    file_contents = f.read(1024 - length_1 - length_2)
    l = bin_name + file_contents
    while (l):
        transmitted = transmitted + len(l)
        print(f"{int(transmitted * 100 / size)}%")
        next_part = f.read(1024 - length_2)
        if not next_part:
            l = l + bin_end
        s.send(l)
        l = next_part

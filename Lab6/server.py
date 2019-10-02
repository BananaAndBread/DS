import os
import socket

"""
Actually this service can download many files, however, in the task it was said that
we have to transmit just one file. So, I have made some restrictions in the client code.
"""
s = socket.socket()
s.bind(("0.0.0.0", 9999))
s.listen(10)

i = 1
while True:
    """
    Explanation:
        !!!: symbols after the name
        /-/: symbols to separate different files data
        '' or '--': end of files
    """
    sc, address = s.accept()

    print("Client address ", address)
    not_finished = False
    last = b'--'
    f = None
    while True:
        l = sc.recv(1024)

        if last != b'--' and last != b'':
            print("not finished")
            not_finished = True
        else:
            not_finished = False

        last = ''
        transmitted_parts = l.split(b'/-/')

        for part in transmitted_parts:
            if part == b'--' or part == b'':
                f.close()
                not_finished = False
            else:
                if not_finished == False:
                    splitted = part.split(b"!!!")
                    name = splitted[0]
                    name = name.decode()
                    if name in os.listdir("."):
                        i = 0
                        temp = name
                        while (temp in os.listdir(".")):
                            i = i + 1
                            temp = name.split(".")[0] + "_copy" + str(i) + "." + ".".join(name.split(".")[1:])
                        name = temp
                    f = open(name, 'wb')
                    print("created file", name)
                    file_bytes = splitted[1]
                    f.write(file_bytes)
                    print("bytes transmitted:", file_bytes)
                else:
                    print("bytes transmitted:", part)
                    f.write(part)

            last = part
        if not l:
            break

    sc.close()

s.close()

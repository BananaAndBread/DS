from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def set_timestamp_after_recv(my_name, recv_counter, counter):
    counter[my_name] += 1
    for name in recv_counter:
        counter[name] = max(recv_counter[name], counter[name])
    return counter


def event(name, counter):
    counter[name] += 1
    print(f"Event in {name}, counter: {counter}")
    return counter


def send_message(pipe, name, counter):
    counter[name] += 1
    print(f'Send message from {name}, counter:{counter}')
    pipe.send(("payload", counter))
    return counter


def recv_message(pipe, name, counter):
    message, timestamp = pipe.recv()
    counter = set_timestamp_after_recv(name, timestamp, counter)
    print(f'Message received at {str(name)}, counter: {counter}')
    return counter

def process_a(pipe_ab):
    name = "a"
    counter = {'a':0, 'b':0, 'c':0}
    counter = send_message(pipe_ab, name, counter)
    counter = event(name, counter)
    counter = event(name, counter)
    counter = send_message(pipe_ab, name, counter)
    counter = event(name, counter)
    counter = recv_message(pipe_ab, name, counter)
    counter = recv_message(pipe_ab, name, counter)
    print(f"name: {name}, counter: {counter}")


def process_b(pipe_ba, pipe_bc):
    name = "b"
    counter = {'a':0, 'b':0, 'c':0}
    counter = recv_message(pipe_bc, name, counter)
    counter = recv_message(pipe_bc, name, counter)
    counter = recv_message(pipe_ba, name, counter)
    counter = event(name, counter)
    counter = send_message(pipe_bc, name, counter)
    counter = recv_message(pipe_ba, name, counter)
    counter = send_message(pipe_ba, name, counter)
    counter = send_message(pipe_ba, name, counter)
    print(f"name: {name}, counter: {counter}")


def process_c(pipe_cb):
    name = "c"
    counter = {'a':0, 'b':0, 'c':0}
    counter = send_message(pipe_cb, name, counter)
    counter = event(name, counter)
    counter = send_message(pipe_cb, name, counter)
    counter = recv_message(pipe_cb, name, counter)
    print(f"name: {name}, counter: {counter}")


if __name__ == '__main__':
    pipe_ab, pipe_ba = Pipe()
    pipe_bc, pipe_cb = Pipe()

    process1 = Process(target=process_a,
                       args=(pipe_ab,))
    process2 = Process(target=process_b,
                       args=(pipe_ba, pipe_bc))
    process3 = Process(target=process_c,
                       args=(pipe_cb,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
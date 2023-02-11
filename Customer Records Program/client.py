import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# instead of binding, now we want to connect
s.connect((socket.gethostname(), 9999))

# accept that message that will be sent to us. 1024 is a buffer size, can be increased depending on data size
msg1 = s.recv(1024)
# we are using a byte steam, send bytes, receive bytes, then decode bytes
print(msg1.decode("utf-8"))  # print welcome message
while True:
    msg2 = s.recv(1024)
    print(msg2.decode("utf-8"))  # print menu

    user_input_menu = input("Select: ")

    if user_input_menu == "1":  # find contact
        find_cust = input("Please enter the customer name you wish to find: ")
        s.sendall(("1" + find_cust).encode())
        print(s.recv(1024).decode("utf-8"))
    elif user_input_menu == "2":  # add new contact
        print("Please enter the following details, SEPARATED BY COMMA.\n")
        add_cust = input("Name,Age,Address,Phone number: ")
        s.sendall(("2" + add_cust).encode())
        print(s.recv(1024).decode("utf-8"))  # print add success msg
    elif user_input_menu == "3":  # delete contact
        del_cust = input("Please enter the customer name you wish to delete: ")
        s.sendall(("3" + del_cust).encode())
        print(s.recv(1024).decode("utf-8"))  # print delete success msg
    elif user_input_menu == "4":  # update age
        age_cust = input("Please enter the customer name for whom you wish to update their age: ")
        s.sendall(("4" + age_cust).encode())
        if s.recv(1024).decode("utf-8") == "proceed":
            print(s.recv(1024).decode("utf-8"))
            new_age = input("Please enter the new age for " + age_cust + ": ")
            s.sendall(new_age.encode())
            print(s.recv(1024).decode("utf-8"))
        else:
            print(s.recv(1024).decode("utf-8"))
    elif user_input_menu == "5":  # update address
        addr_cust = input("Please enter the customer name for whom you wish to update their address: ")
        s.sendall(("5" + addr_cust).encode())
        if s.recv(1024).decode("utf-8") == "proceed":
            print(s.recv(1024).decode("utf-8"))
            new_addr = input("Please enter the new address for " + addr_cust + ": ")
            s.sendall(new_addr.encode())
            print(s.recv(1024).decode("utf-8"))
        else:
            print(s.recv(1024).decode("utf-8"))
    elif user_input_menu == "6":  # update phone number
        phone_cust = input("Please enter the customer name for whom you wish to update to their phone number: ")
        s.sendall(("6" + phone_cust).encode())
        if s.recv(1024).decode("utf-8") == "proceed":
            print(s.recv(1024).decode("utf-8"))
            new_phone = input("Please enter the new phone number for " + phone_cust + ": ")
            s.sendall(new_phone.encode())
            print(s.recv(1024).decode("utf-8"))
        else:
            print(s.recv(1024).decode("utf-8"))
    elif user_input_menu == "7":  # if user selects 7, DB prints
        s.sendall("7".encode())
        print("\n** Python DB contents **")
        print(s.recv(1024).decode("utf-8"))
    elif user_input_menu == "8":  # close the client connection but keep the server running
        s.sendall("8".encode())
        print(s.recv(1024).decode("utf-8"))
        break  # break outside the loop, where the client connection will be closed
    else:  # unexpected behaviour by the user
        print("This is not part of the assignment requirements.\nAn ideal user is expected. Please restart the "
              "program.\nYou must enter an integer between 1-8 inclusive.")

s.close()  # closing client connection after breaking from the loop

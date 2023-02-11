import socket


# method that converts the tuple value from dictionary into a string and returns a string
# with the required format for printing the report. i.e. Age|Address|Phone number
# keys are dealt with separately
def convert_tuple(tup):
    str1 = ""
    for item in tup:
        str1 = str1 + "|" + item
    return str1


# method that sorts a given dictionary and returns a list of sorted keys, each key followed by its
# corresponding value (value in tuple form)
def sort_dict(some_dict):
    sorted_names = sorted(some_dict.keys(), key=lambda y: y.lower())  # sort keys alphabetically case-insensitive
    temp_dict = {}
    for i in sorted_names:
        temp_dict[i] = some_dict[i]  # move values to sorted keys in temp_dict
    return temp_dict.items()  # return a list of items of the dictionary


# define our socket object
# socket family type is socket.AF_INET and the actual type of socket is socket.SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the object to a tuple, which in this case will be an IP and a port because of the type of the socket
s.bind((socket.gethostname(), 9999))
# socket is the end point that receives data (it is not the communication itself
# now, make some connections to the server, like a queue of 5
s.listen(1)

# listen forever for connections
while True:
    # if we get a connection, store the client object in the clientsocket, the address (IP) is where they are come from
    clientsocket, address = s.accept()
    # print some general debugging f string
    print(f"Connection from {address} has been established!")
    # send information to the client socket
    # msg1
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))

    # open data.txt and load all its contents to the server by storing the data into a dictionary,
    # with the name being stored as the key and the other data (age,address,phone) as values in tuple format
    file = open("data.txt", "r")
    d1 = {}
    for line in file:
        x = line.split("|")
        name = x[0]
        age = x[1]
        address = x[2]
        phone = x[3]
        c = len(phone) - 1  # eliminate '\n'
        phone = phone[0:c]  # from element zero up to but not including the '\'
        d1[name] = age, address, phone

    # method that checks if a given string exists in the dictionary. it is used for error handling
    def check_dict(str1):
        bool1 = False
        for str2 in d1:
            if str1 == str2:
                bool1 = True
        return bool1


    while True:
        # msg2; send menu to the client
        clientsocket.send(bytes("\nPython DB Menu\n\n1. Find customer\n2. Add customer\n3. Delete customer\n"
                                "4. Update customer age\n5. Update customer address\n6. Update customer"
                                " phone\n7. Print report\n8. Exit\n", "utf-8"))

        user_input_menu = clientsocket.recv(1024).decode("utf-8")  # receive user input
        if user_input_menu[0] == "1":  # check if the first char from the received string is "1"
            user_input_menu2 = user_input_menu[1:]  # store the data that follows "1" in a new string and deal with it
            if check_dict(user_input_menu2):  # check if the received data (name) exists in the dictionary
                for key, value in d1.items():
                    if str(key).startswith(user_input_menu2):
                        clientsocket.send(bytes("Data found: ".encode() + key.encode() +
                                                (convert_tuple(value)).encode()))
            else:
                clientsocket.send(bytes(user_input_menu2.encode() + " not found in database.".encode()))
        elif user_input_menu[0] == "2":
            user_input_menu2 = user_input_menu[1:]  # save all data
            temp = user_input_menu2.split(",", 1)[0]  # store name in temp to check if it already exists in dict
            if check_dict(temp) is False:
                user_input_menu3 = user_input_menu2.split(",", 1)[0]  # save name from all data to use for key
                user_input_menu4 = user_input_menu2.split(",", 1)[1]  # save other data to use for value
                list1 = user_input_menu4.split(",")  # store data in list
                d1[user_input_menu3] = list1  # add list to dictionary
                with open("data.txt", "w") as output:
                    for key, value in d1.items():
                        output.write("%s%s\n" % (key, convert_tuple(value)))
                clientsocket.send(bytes(user_input_menu3.encode() + " successfully added".encode()))
            else:
                clientsocket.send(bytes("Customer already exists.".encode()))
        elif user_input_menu[0] == "3":
            user_input_menu2 = user_input_menu[1:]
            if check_dict(user_input_menu2):
                user_input_menu3 = user_input_menu2.split(" ", 1)[0]
                d1.pop(user_input_menu3, None)
                with open("data.txt", "w") as output:
                    for key, value in d1.items():
                        output.write("%s%s\n" % (key, convert_tuple(value)))
                clientsocket.send(bytes(user_input_menu3.encode() + " successfully deleted".encode()))
            else:
                clientsocket.send(bytes("Customer does not exist.".encode()))
        elif user_input_menu[0] == "4":
            user_input_menu2 = user_input_menu[1:]  # save name
            status = "stop"
            if check_dict(user_input_menu2):
                status = "proceed"
                clientsocket.send(bytes(status.encode()))
                value_from_key = d1[user_input_menu2]  # tuple value saved here
                clientsocket.send(bytes("The current age is: ".encode() + value_from_key[0].encode()))
                new_age = clientsocket.recv(1024).decode("utf-8")  # save new age
                temp_list = list(value_from_key)  # convert tuple to list to be able to change its values
                temp_list[0] = new_age  # change age value
                d1[user_input_menu2] = tuple(temp_list)  # re-assign the key name with the new updated tuple value
                with open("data.txt", "w") as output:
                    for key, value in d1.items():
                        output.write("%s%s\n" % (key, convert_tuple(value)))
                clientsocket.send(bytes("Age for ".encode() + user_input_menu2.encode() + " updated.".encode()))
            else:
                clientsocket.send(bytes(status.encode()))
                clientsocket.send(bytes("Customer not found.".encode()))
        elif user_input_menu[0] == "5":
            user_input_menu2 = user_input_menu[1:]  # save name
            status = "stop"
            if check_dict(user_input_menu2):
                status = "proceed"
                clientsocket.send(bytes(status.encode()))
                value_from_key = d1[user_input_menu2]  # tuple value saved here
                clientsocket.send(bytes("The current address is: ".encode() + value_from_key[1].encode()))
                new_address = clientsocket.recv(1024).decode("utf-8")  # save new address
                temp_list = list(value_from_key)  # convert tuple to list to be able to change its values
                temp_list[1] = new_address  # change address value
                d1[user_input_menu2] = tuple(temp_list)  # re-assign the key name with the new updated tuple value
                with open("data.txt", "w") as output:
                    for key, value in d1.items():
                        output.write("%s%s\n" % (key, convert_tuple(value)))
                clientsocket.send(bytes("Address for ".encode() + user_input_menu2.encode() + " updated.".encode()))
            else:
                clientsocket.send(bytes(status.encode()))
                clientsocket.send(bytes("Customer not found.".encode()))
        elif user_input_menu[0] == "6":
            user_input_menu2 = user_input_menu[1:]  # save name
            status = "stop"
            if check_dict(user_input_menu2):
                status = "proceed"
                clientsocket.send(bytes(status.encode()))
                value_from_key = d1[user_input_menu2]  # tuple value saved here
                clientsocket.send(bytes("The current phone number is: ".encode() + value_from_key[2].encode()))
                new_phone = clientsocket.recv(1024).decode("utf-8")  # save new phone number
                temp_list = list(value_from_key)  # convert tuple to list to be able to change its values
                temp_list[2] = new_phone  # change phone number value
                d1[user_input_menu2] = tuple(temp_list)  # re-assign the key name with the new updated tuple value
                with open("data.txt", "w") as output:
                    for key, value in d1.items():
                        output.write("%s%s\n" % (key, convert_tuple(value)))
                clientsocket.send(bytes("Phone number for ".encode() + user_input_menu2.encode() +
                                        " updated.".encode()))
            else:
                clientsocket.send(bytes(status.encode()))
                clientsocket.send(bytes("Customer not found.".encode()))
        elif user_input_menu[0] == "7":
            temp = ""  # create an empty string
            for key, value in sort_dict(d1):  # sorted(d1.items())
                temp1 = convert_tuple(value)  # convert tuple value into string and separate each value by '|'
                temp += key + temp1 + "\n"  # key and value both stored in string temp
                # now send this to the client side.
            temp2 = temp[0:len(temp)-2]  # store the contents of the DB in temp2 as the report
            clientsocket.send(bytes(temp2.encode()))  # send the report to the client in the required format
        elif user_input_menu[0] == "8":
            clientsocket.send(bytes("Good bye".encode()))
            break  # break out of the loop while keeping the server running

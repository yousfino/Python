# Description

The goal is to construct a client/server application. Only one client program will 
access the DB, so no issues like concurrency or thread control is considered. It's 
just a one-to-one form if communication. A standard library provided by Python 
called SocketServer is used.

The type of DB used is a simple text file (.txt file).

After the connection between the client and server is established, the database is 
loaded to provide access to the data from the server side.

The type of data in the text file is is the form of:

name, age, address, phone#

So, once the client connects to the server, the client will have access to a user 
interface menu from which the client can view/modify customer records. The UI menu 
looks like the following:

Python DB Menu

1. Find customer
2. Add customer
3. Delete customer
4. Update customer age
5. Update customer address
6. Update customer phone
7. Print report
8. Exit
Select:

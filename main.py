# Task 1
products = []
for i in range(3):
    while True:
        try:
            print(f"\nProduct {i + 1}")
            name = input(f"Enter the name of product {i + 1}: ").strip()
            if not name:
                print("Product name cannot be empty. Please try again.")
                continue

            price = float(input(f"Enter the price of product {i + 1}: "))
            if price < 0:
                print("Price cannot be negative. Please try again.")
                continue

            product = {"name": name, "price": price}
            products.append(product)
            break

        except ValueError:
            print("Invalid input. Please enter a valid numeric price.")

# Print results
# print("\nProducts list:")
# for product in products:
#    print(product)

with open("products.txt", "w", encoding="utf-8") as file:
    for product in products:
        # file.write(f"{product['name']}: ${product['price']}\n")
        file.write(f"{product}\n")

print("\nProducts successfully saved to products.txt!\n")
with open("products.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print("Contents of products.txt:")
    print(content)



# Task 2.
import threading


def sum_of_numbers():
    total_sum = sum(range(1, 1001))
    print(f"Sum of numbers from 1 to 1000: {total_sum}")
    return total_sum


def sum_of_squares():
    total_squares = sum(i**2 for i in range(1, 1001))
    print(f"Sum of squares from 1 to 1000: {total_squares}")
    return total_squares


thread1 = threading.Thread(target=sum_of_numbers)
thread2 = threading.Thread(target=sum_of_squares)

thread1.start()
thread2.start()

thread1.join()
thread2.join()



# Task 3
import pickle

students = []

for i in range(3):
    while True:
        try:
            print(f"\nStudent {i + 1}")
            name = input("Enter student name: ").strip()
            if not name:
                print("Student name cannot be empty. Please try again.")
                continue

            score = float(input("Enter student score: "))
            if score < 0:
                print("Score cannot be negative. Please try again.")
                continue

            student = {"name": name, "score": score}
            students.append(student)
            break

        except ValueError:
            print("Invalid input. Please enter a valid numeric score.")

# Print results
# print("\nStudents list:")
# for student in students:
#    print(student)

# Serialize and save to file
with open("students.pkl", "wb") as file:
    pickle.dump(students, file)

print("\nData successfully serialized and saved to students.pkl!")

# Deserialize - read from file
print("\nData read from file:")
with open("students.pkl", "rb") as file:
    loaded_students = pickle.load(file)

print(loaded_students)

# Detailed print
print("\nDeserialized students:")
for i, student in enumerate(loaded_students, 1):
    print(f"Student {i}: Name - {student['name']}, Score - {student['score']}")




# Task 4
import socket

HOST = '127.0.0.1'
PORT = 5924
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server running on {HOST}:{PORT}")
print("Waiting for client...\n")

conn, addr = server_socket.accept()
print(f"Connection from: {addr}")


while True:
    data = conn.recv(1024)
    if not data:
        break
    message = data.decode()
    print(f"Received message: {message}")

    reversed_message = message[::-1]
    print(f"Sending response: {reversed_message}\n")
    conn.sendall(reversed_message.encode())

conn.close()
print("Connection closed.")


import socket

HOST = '127.0.0.1'
PORT = 5924
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to server at {HOST}:{PORT}\n")


while True:
    msg = input("\nEnter message to send (type 'exit' to quit): ")
    if msg.lower() == 'exit':
        break
    client_socket.sendall(msg.encode())
    print(f"Sent: {msg}")

    data = client_socket.recv(1024).decode()
    print(f"Response from server: {data}")

client_socket.close()
print("\nConnection closed.")




# Task 4 with encryption
import socket
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
print("Key: ", key.decode())

HOST = '127.0.0.1'
PORT = 5924
server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server running on {HOST}:{PORT}")
print("Waiting for client...\n")

conn, addr = server_socket.accept()
print(f"Connection from: {addr}")


while True:
    encrypted_data = conn.recv(1024)
    if not encrypted_data:
        break
    decrypted_message = cipher.decrypt(encrypted_data).decode()
    print(f"Client says: {decrypted_message}")

    reversed_message = decrypted_message[::-1]
    encrypted_response = cipher.encrypt(reversed_message.encode())
    print(f"Sending response: {reversed_message}\n")
    conn.sendall(encrypted_response)

conn.close()
print("Connection closed.")


import socket
from cryptography.fernet import Fernet

key = input("Enter the key: ").encode()
cipher = Fernet(key)

HOST = '127.0.0.1'
PORT = 5924
client_socket = socket.socket()
client_socket.connect((HOST, PORT))
print(f"Connected to server at {HOST}:{PORT}\n")


while True:
    msg = input("\nEnter message to send (type 'exit' to quit): ")
    if msg.lower() == 'exit':
        break
    encrypted_message = cipher.encrypt(msg.encode())
    client_socket.sendall(encrypted_message)
    print(f"Sent: {msg}")
    data = client_socket.recv(1024)
    decrypted_message = cipher.decrypt(data).decode()
    print(f"Response from server: {decrypted_message}")

client_socket.close()
print("\nConnection closed.")




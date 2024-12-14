import sqlite3
from tabulate import tabulate


directory = input("Enter the path of the ch17 directory : ")
db_path = f"{directory}/books.db"


connection = sqlite3.connect(db_path)
cursor = connection.cursor()

#Execute a query to select all data from the 'titles' table
cursor.execute("SELECT * FROM titles")

# Get metadata using the 'description' attribute
columns = [desc[0] for desc in cursor.description]


data = cursor.fetchall()

# Display the data in tabular format, to make it more better
print("Data in 'titles' table:")
print(tabulate(data, headers=columns, tablefmt="grid"))

connection.close()


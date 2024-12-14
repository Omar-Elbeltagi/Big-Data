import sqlite3

directory = input("Enter the path of the ch17 directory : ")
db_path = f"{directory}/books.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
print("\n**********************************\n")

# 1. Select all authors' last names in descending order
print("Authors' Last Names (Descending):")
query = "SELECT last FROM authors ORDER BY last DESC;"
cursor.execute(query)
for row in cursor.fetchall():
    print(row[0])
print("\n**********************************\n")

# 2. Select all book titles in ascending order
print("Book Titles (Ascending):")
query = "SELECT title FROM titles ORDER BY title ASC;"
cursor.execute(query)
for row in cursor.fetchall():
    print(row[0])
print("\n**********************************\n")

# 3. Use INNER JOIN to select books for a specific author
print("Books for a Specific Author (Alphabetically by Title):")
author_id = input("Enter the Author ID to display their books: ")
query = """
    SELECT titles.title, titles.copyright, titles.isbn 
    FROM titles
    INNER JOIN author_ISBN ON titles.isbn = author_ISBN.isbn
    WHERE author_ISBN.id = ?
    ORDER BY titles.title ASC;
"""
cursor.execute(query, (author_id,))
books = cursor.fetchall()
if books:
    for row in books:
        print(f"Title: {row[0]}, Year: {row[1]}, ISBN: {row[2]}")
else:
    print("No books found for this author ID.")
print("\n**********************************\n")

# 4. Insert a new author into the authors table
print("Inserting a New Author...")
new_author_first = input("Enter the author's first name: ")
new_author_last = input("Enter the author's last name: ")
query = "INSERT INTO authors (first, last) VALUES (?, ?);"
cursor.execute(query, (new_author_first, new_author_last))
connection.commit()
print("New author added successfully.")
print("\n**********************************\n")

# 5. Insert a new title and update author_ISBN table
print("Inserting a New Title and Linking to Author...")
new_title = input("Enter the new book title: ")
new_copyright = input("Enter the book's copyright year: ")
new_isbn = input("Enter the new ISBN (must be unique): ")

# Provide a default value for edition if the user doesn't specify it
try:
    new_edition = int(input("Enter the book edition (default is 1): ") or 1)
except ValueError:
    new_edition = 1

# Display authors to link the book to an author
print("Available Authors:")
cursor.execute("SELECT id, first, last FROM authors;")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]} {row[2]}")

linked_author_id = input("Enter the Author ID to link this book to: ")

query1 = "INSERT INTO titles (isbn, title, edition, copyright) VALUES (?, ?, ?, ?);"
cursor.execute(query1, (new_isbn, new_title, new_edition, new_copyright))

query2 = "INSERT INTO author_ISBN (id, isbn) VALUES (?, ?);"
cursor.execute(query2, (linked_author_id, new_isbn))
connection.commit()
print("New book title and author_ISBN link added successfully.")
print("\n**********************************\n")

# 6. Verify the changes
print("Updated Authors Table:")
cursor.execute("SELECT * FROM authors;")
for row in cursor.fetchall():
    print(row)

print("\nUpdated Titles Table:")
cursor.execute("SELECT * FROM titles;")
for row in cursor.fetchall():
    print(row)

print("\nUpdated author_ISBN Table:")
cursor.execute("SELECT * FROM author_ISBN;")
for row in cursor.fetchall():
    print(row)


connection.close()
print("\nDatabase connection closed.")

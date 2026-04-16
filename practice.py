
# importing necessary module
import sys

# defining a class that will contain all the necessary functions.
class Library:
    # initializing all the available books.
    def __init__(self, allBooks):
        self.availableBooks = allBooks

    # a function that will print all books.
    def displayBooks(self):
        print("List of the books are:")
        for book in self.availableBooks:
            print(book)

    # a function that will lend requested book(s) to the users.
    def lendBook(self, book):
        if book in self.availableBooks:
            print("Book borrowed successfully")

            # removing the book from the library
            self.availableBooks.remove(book)
        else:
            print("This book is not available.")

    # a function that will add the returned book into the library.
    def addBook(self, Book):
        self.availableBooks.append(Book)
        print("Thanks for returning the book.")


# a class that will handle requests from Students
class Students:
    def requestBook(self):
        self.book = input("Enter the name of the book that you want: ")
        return self.book

    def returnBook(self):
        self.book = input(
            "Enter the name of the book that you want to return: ")
        return self.book


# declaring all the books present in the library.
library = Library(["Let Us C", "Python World", "Shaum Series", "Karumanchi"])

# creating an object of Students class
student = Students()

# running an infinite loop.
done = False
while done == False:
    print(""" ====== Our Facilities =======
                  1. Display all books.
                  2. Request a book.
                  3. Return a book.
                  4. Exit.
                  """)
    choice = int(input("Enter your choice: "))
    if choice == 1:
        library.displayBooks()
    elif choice == 2:
        library.lendBook(student.requestBook())
    elif choice == 3:
        library.addBook(student.returnBook())
    elif choice == 4:
        sys.exit()

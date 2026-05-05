"""
Concepts We Are Practicing:
- Functions
- Loops and Menu-Driven Programs
- Lists and Data Filtering
- Dictionaries
- Counter (from collections)

Modules and Libraries:
- API Requests (requests)
- Text Processing (re - regular expressions)
"""

"""
Author: Hajin Kim
GitHub Link: https://github.com/hajin03/CS-1-Project
Project: Book Analyzer (CS I Project)
Extra credit: I have fixed the bug in line no:.... or 
              I implemeted a new feature:  if choice == '6', new feature ............ will be executed
"""

import requests
import re
from collections import Counter


# -----------------------------
# INITIAL DATA
# -----------------------------

my_library = {
    "Moby Dick": "https://www.gutenberg.org/files/2701/2701-0.txt"
}

# TODO 3: Read stop words from a file instead; this file "EN-Stopwords" contains thousands stop words(2 points)
with open("EN-Stopwords.txt", "r") as f:
    STOP_WORDS = set(word.strip().lower() for word in f.readlines())
'''  
STOP_WORDS = {
    "the", "and", "to", "of", "in", "i",
    "a", "it", "that", "was"
}
'''
# -----------------------------
# FETCH BOOK
# -----------------------------
def fetch_book(url):
    """Download text from a URL."""
    # TODO 4: Handle exceptions (network errors, invalid URLs, etc.) (1 point)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching book: {e}")
        return None

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(raw_text):
    """Lowercase text and remove punctuation."""
    text = raw_text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.split()

# -----------------------------
# ANALYZE TEXT
# -----------------------------
def analyze_text(words):
    """Remove stop words and count frequencies."""
    filtered_words = [] 
    for w in words: 
        if w not in STOP_WORDS and len(w) > 2:   #checking len(w)> 2 to remove tiny words((is, to, at))
            filtered_words.append(w)

    return Counter(filtered_words).most_common(10)



# -----------------------------
# VISUALIZATION (BAR CHART)
# -----------------------------
# TODO 5: Implement the following function (2 points)
# hints: use print() statements to create a horizontal bar chart using the "█" or "*" character.
def plot_results(stats, title):
    """Create a bar chart of word frequencies."""
    print(f"--- Top 10 Words in {title} ---")
    for word, count in stats:
        if count > 10:
            bar = "█" * (count//10)
        else:
            bar = "█" * count
        print(f"{word:15} | {bar} ({count})")
    pass 

# -----------------------------
# MENU SYSTEM
# -----------------------------
def main():
    while True:
        print("\n--- LIBRARY MANAGER ---")
        print(f"Current Books: {list(my_library.keys())}")
        print("1. Add New Book")
        print("2. Remove Book")
        print("3. Update Book URL")
        print("4. Analyze a Book")
        print("5. Exit")
        print("6. Search for a word in a book")  # I implemented it!

        choice = input("\nSelect (1-6): ")

        if choice == '1':
            # Add new books to the dictionary (use this website: https://www.gutenberg.org/browse/scores/top)
            # TODO 1.1: Normalize input by removing extra spaces and ignoring case.
            
                # (e.g., " The Hobbit " (with space) and "the hobbit" should be treated as the same book4.) (1 point)
            raw_name = input("Enter Book Title: ")
            name = raw_name.strip()
            normalized = name.lower()
            url = input("Enter Gutenberg .txt URL: ").strip()

            # TODO 1.2: Validate that the Book title or URL is not empty (1 point)
            if name == "" or url == "":
                print("Error: Book title or URL cannot be empty.")
                continue
            # TODO 1.3: Prevent duplicate book names (1 point)
            duplicate = False
            for k in my_library:
                if k.lower() == normalized:
                    duplicate = True
                    break

            if duplicate:
                print(f"Error: '{name.upper()}' already exists in the library.")
            else:
                my_library[name] = url
                print(f"'{name}' added.")


            
            

        elif choice == '2':
            # Remove books from the dictionary
            #TODO 2.1: Handle missing books—check if the title exists before trying to delete it.(1 point)
            #TODO 2.2: Make the removal case-insensitive so "The Hobbit" matches "the hobbit".(1 point)
            # Hint: Use .strip().lower() to normalize the user's input!
            name = input("Enter title to remove: ").strip().lower()

            found = False

            for k in list(my_library.keys()):
                if k.lower() == name:
                    del my_library[k]
                    print(f"'{k}' removed.")
                    found = True
                    break

                if not found:
                    print("Book not found")
            
            

        elif choice == '3':
            # UPDATE OPERATION
            name_input = input("Enter the book title to update: ").strip().lower()
            target_key = None  # Start with None in case we don't find it

            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break  # We found it, so stop looking

            if target_key:
                print(f"Current URL: {my_library[target_key]}")
                new_url = input("Enter new URL: ").strip()
                if new_url == "":
                    print("Invalid URL. Update cancelled.")
                else:
                    my_library[target_key] = new_url
                    print(f"'{target_key}' updated successfully.")
            else:
                print("Book not found.")

        elif choice == '4':
            name_input = input("Which book to analyze? ").strip().lower()
            
            target_key = None
            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break

            if target_key:
                url = my_library[target_key]
                print(f"Fetching and analyzing '{target_key}'...")
                raw_text = fetch_book(url)

                if raw_text:
                    words = clean_text(raw_text)
                    stats = analyze_text(words)
                    plot_results(stats, target_key)
            else:
                print("Error: Book not found.")

        elif choice == '5':
            print("Goodbye!")
            break

        elif choice == '6':     #Added a word search feature that counts a word in a book
            name_input = input("Which book? ").strip().lower()
            target_key = None
            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break
            if target_key:
                word = input("Enter word to search: ").strip().lower()

                url = my_library[target_key]
                raw_text = fetch_book(url)

                if raw_text is None:
                    print("Failed to load book.")
                    continue

                text = raw_text.lower()
                count = text.count(word)

                if count == 0:
                    print(f"The word '{word}' was not found.")
                    continue

                print(f"\n the word '{word}' appears {count} times.\n")

                index = text.find(word)
                if index != -1:
                    start = max(0, index - 30)
                    end = index + 30
                    snippet = text[start:end]
                    print("Example context:")
                    print(f"...{snippet}...")
            else:
                print("Book not found.")
                
                


if __name__ == "__main__":
    main()

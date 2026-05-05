import requests
import re
from collections import Counter


# -----------------------------
# INITIAL DATA
# -----------------------------

my_library = {
    "Moby Dick": "https://www.gutenberg.org/files/2701/2701-0.txt"
}

with open("EN-Stopwords.txt", "r") as f:
    STOP_WORDS = set(word.strip().lower() for word in f.readlines())
  
# -----------------------------
# FETCH BOOK
# -----------------------------
def fetch_book(url):
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
            raw_name = input("Enter Book Title: ")
            name = raw_name.strip()
            normalized = name.lower()
            url = input("Enter Gutenberg .txt URL: ").strip()
          
            if name == "" or url == "":
                print("Error: Book title or URL cannot be empty.")
                continue
            
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
            target_key = None

            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break  

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

        elif choice == '6':     #I implemented a word search feature in the code, when the user enter 6 in input, the program counts how many times a word appears in the selected book. 
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

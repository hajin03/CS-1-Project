# CS-1-Project
Book Analyzer (CS 1 Project)
# 📚 Book Analyzer
This project is a program that allows users to manage a small digital library and analyze books from Project Gutenberg.

## 🚀 Features

- Add, remove, and update books in a personal library
- Download book text from a URL using the `requests` library
- Clean and process text using regular expressions
- Remove stop words loaded from an external file
- Analyze word frequency using `collections.Counter`
- Display the top 10 most frequent words with a bar chart
- Case-insensitive search and input handling

### 📊 Text Analysis

The program processes book text by:
1. Converting all text to lowercase
2. Removing punctuation using regular expressions
3. Filtering out common stop words
4. Counting word frequencies

Results are displayed using a simple horizontal bar chart made with characters.

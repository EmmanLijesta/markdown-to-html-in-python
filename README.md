# Markdown to HTML in Python

A basic Markdown to HTML parser written in Python. This project was specifically made for my website, thus, you may need to tweak some things in the code to fit your needs. But, it may work as inteded for all basic things.

## How to Use the markdown.py
```
import markdown

MD_PATH = "../somepath/file.md"
MD_DATA = open(MD_PATH, "r").read()

my_markdown = MARKDOWN(MD_DATA)
my_markdown.replaceMarkdown()

print(my_markdown.md_data)
```

That's about it! It's not yet perfect, depending on how you use it, there might be bugs. But, so far it works with my website. Also, use CSS to adjust the HTML output.

## Technologies Used

- Python 3.10.17
- Regular Expressions
- Markdown
- HTML

## Terms

Python
: Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically type-checked and garbage-collected.

Regular Expressions
: A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern. RegEx can be used to check if a string contains the specified search pattern.

Markdown
: Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.

HTML
: Hypertext Markup Language (HTML) is the standard markup language for documents designed to be displayed in a web browser.

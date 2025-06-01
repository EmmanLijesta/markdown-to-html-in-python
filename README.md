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

That's about it! It's not yet perfect, depending on how you use it, there might be bugs. But, so far it works with my website.

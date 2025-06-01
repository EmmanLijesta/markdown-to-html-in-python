import re
import threading

"""
    A multi-threaded basic Markdown to HTML parser. This has limitations since it was
    created specifically for my project and website, but, could be adjusted to fit
    your needs both codes and regular expressions; it's coded with easy readability.

    Class:
        MARKDOWN(data)
    Function:
        replaceMarkdown()
    Variable:
        md_data
    Average conversion time:
        0.05 seconds
"""

# Tweak the regular expressions and codes to meet your needs
MD_REGEX = {
    "header": "(^\#+)\s((.*)\s\{\#(.*)\})?(?(2)|(.*))",
    "paragraph": r"(^[A-Z\_\*\"\'].*[\.\!\?][\"\']?)\n",
    "format_asterisk": r"(\*+)([^\*]+\\\*[^\*]+)?(?(2)|([^\*]+))\*+",
    "format_underline": "\_([^\s][^\_]+(\\\_)?[^\_]+[^\s])\_",
    "image": '!\[([^\[\]]+)\]\((([^\(\)\[\]]+)\s"(.*)")?(?(2)|([^\(\)\[\]]+))\)',
    "link": '\[([^\[\]]+)\]\((([^\(\)\[\]]+)\s"(.*)")?(?(2)|([^\(\)\[\]]+))\)',
    "blockquote": "((?:^\>\s.*\n){1,})",
    "ordered": "((?:^\d\.\s.*\n){1,})",
    "unordered": "((?:^\-\s.*\n){1,})",
    "code": "(^\`+)\n?([^\`]+)\`+",
    "horizontal": "^\-{3}",
    "table": "((?:^\|\s.*\|\n){1,})",
    "quick_link": "\<([^\/\\\:\<\>\@]{3,}[\:\@]+\/?\/?[^\<\>]+\.\w{2,})\:?(\d+)?\>",
    "highlight": "\={2}([^\=]+\\\=[^\=]+)?(?(1)|([^\=]+))\={2}",
    "superscript": "([\w\d]+)\^([^\^]+)(\^)",
    "subscript": "([\w\d]+)\~([^\~]+)(\~)",
    "strikethrough": "\~{2}([^\~]+)\~{2}",
    "definition": "(^[A-Z].*\n(?:\:\s.*\n){1,})",
    "footnote": "\[\^([^\[\]\:\^]+)\](\:)?(?(2)((\s+[A-Z].*\.){1,}))",
    "tasklist": "((?:^\-\s\[.*\]\s.*\n){1,})",
    "plaintext": "((?:^[A-Za-z][^\<\>]+\n(?=\n)){1,})",
}


class MARKDOWN:
    def __init__(self, md_data):
        self.md_data = md_data
        self.md_regex = MD_REGEX
        self.md_lock = threading.Lock()
        self.md_threads = []

    # Replace header
    def replaceHeading(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["header"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_key, _, md_group_one, md_id, md_group_two = md_array
                md_length = len(md_key)
                md_replace = md_group_one if md_group_two == "" else md_group_two
                md_search_array = (
                    md_key
                    + " "
                    + md_replace
                    + (" {#" + md_id + "}" if md_group_two == "" else "")
                )
                md_replace = f"<h{md_length} id='{md_id}'>{md_replace}</h{md_length}>"
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace paragraph
    def replaceParagraph(self):
        self.md_lock.acquire()
        md_group = re.findall(self.md_regex["paragraph"], self.md_data, re.MULTILINE)
        if md_group != []:
            for md_array in md_group:
                md_replace = "\n<p>" + md_array + "</p>\n"
                md_search_array = re.escape(f"\n{md_array}\n")
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace formats
    def replaceFormat(self):
        self.md_lock.acquire()
        md_search = re.findall(
            self.md_regex["format_asterisk"], self.md_data, re.MULTILINE
        )
        if md_search != []:
            for md_array in md_search:
                md_key, md_group_one, md_group_two = md_array
                md_group = md_group_one if md_group_two == "" else md_group_two
                md_length = len(md_key)
                md_head = md_key[0]
                md_replace = md_group.replace("\\" + md_head, md_head)
                if md_length == 1:
                    md_start = "<i>"
                    md_end = "</i>"
                elif md_length == 2:
                    md_start = "<b>"
                    md_end = "</b>"
                else:
                    md_start = "<b><i>"
                    md_end = "</i></b>"
                md_replace = f"{md_start}{md_replace}{md_end}"
                md_search_array = f"{md_key}{md_group}{md_key}"
                self.md_data = re.sub(
                    re.escape(md_search_array), md_replace, self.md_data
                )
        self.md_lock.release()

    # Replace image
    def replaceImage(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["image"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_text, _, md_link_one, md_title, md_link_two = md_array
                md_link = md_link_one if md_link_two == "" else md_link_two
                md_search_array = re.escape(
                    f'![{md_text}]({md_link} "{md_title}")'
                    if md_link_two == ""
                    else f"![{md_text}]({md_link})"
                )
                md_replace = (
                    f"<img src='{md_link}' title='{md_title}' alt='{md_text}' />\n"
                )
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace link
    def replaceLink(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["link"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_text, _, md_link_one, md_title, md_link_two = md_array
                md_link = md_link_one if md_link_two == "" else md_link_two
                md_search_array = re.escape(
                    f'[{md_text}]({md_link} "{md_title}")'
                    if md_link_two == ""
                    else f"[{md_text}]({md_link})"
                )
                md_replace = f"<a href='{md_link}' title='{md_title}'>{md_text}</a>"
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace blockquote
    def replaceBlockquote(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["blockquote"], self.md_data, re.MULTILINE)
        if md_search != []:
            md_block = ""
            for md_array in md_search:
                md_search_array = md_array
                md_sub_array = md_array.split("\n")
                md_double = False
                md_block = "<blockquote>"
                for md_val in md_sub_array[: len(md_sub_array) - 1]:
                    md_key = len(md_val[0:2].rstrip())
                    md_text = md_val[2:].strip()
                    if md_key == 1:
                        if md_double:
                            md_block += "</blockquote>"
                            md_double = False
                    elif md_key == 2:
                        if not md_double:
                            md_block += "<blockquote>"
                            md_double = True
                    if md_text != "":
                        md_block += f"<p>{md_text}</p>"
                if md_double:
                    md_block += "</blockquote></blockquote>\n"
                else:
                    md_block += "</blockquote>\n"
                self.md_data = re.sub(md_search_array, md_block, self.md_data)
        self.md_lock.release()

    # Replace ordered list
    def replaceList(self, md_regex):
        self.md_lock.acquire()
        md_search = re.findall(md_regex, self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_items = md_array.split("\n")
                md_key = md_items[0][0]
                md_list = "<ol>" if md_key != "-" else "<ul>"
                md_search_array = ""
                for md_items_array in md_items[: len(md_items) - 1]:
                    md_search_array += f"{md_items_array}\n"
                    md_limit = 3 if md_key != "-" else 2
                    md_list += f"<li>{md_items_array[md_limit:]}</li>"
                md_list += "</ol>\n" if md_key != "-" else "<ul>\n"
                self.md_data = re.sub(md_search_array, md_list, self.md_data)
        self.md_lock.release()

    # Replace code
    def replaceCode(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["code"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_key, md_code = md_array
                md_length = len(md_key)
                md_newline = "" if md_length == 1 else "\n"
                md_search_array = re.escape(md_key + md_newline + md_code + md_key)
                md_replace = "<code>" + md_newline + md_code + "</code>"
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace horizontal
    def replaceHorizontal(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["horizontal"], self.md_data, re.MULTILINE)
        if md_search != []:
            md_replace = "<hr>"
            self.md_data = re.sub(md_search[0], md_replace, self.md_data)
        self.md_lock.release()

    # Replace single table only
    def replaceTable(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["table"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_table_iter in md_search:
                md_search_array = md_table_iter.split("\n")
                md_search_array_length = len(md_search_array)
                md_rows = md_search_array[0].split("|")
                md_count = 0
                md_table = "<table>"
                while md_count < md_search_array_length - 1:
                    if md_count == 1:
                        md_count += 1
                        continue
                    elif md_count == 0:
                        md_separator = "h"
                    else:
                        md_table += "<tr>"
                        md_separator = "d"
                    md_rows = md_search_array[md_count].split("|")
                    for md_array in md_rows[1 : len(md_rows) - 1]:
                        md_table += f"<t{md_separator}>{md_array[1 : len(md_array) - 1]}</t{md_separator}>"
                    md_table += "</tr>"
                    md_count += 1
                md_table += "</table>\n"
                self.md_data = re.sub(re.escape(md_table_iter), md_table, self.md_data)
        self.md_lock.release()

    # Replace quick links
    def replaceQuickLink(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["quick_link"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_link, md_port = md_array
                md_link = md_link if md_port == "" else f"{md_link}:{md_port}"
                md_search_array = f"<{md_link}>"
                md_replace = f"<a href='{md_link}'>{md_link}</a>"
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace highlight
    def replaceHighlight(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["highlight"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_group_one, md_group_two = md_array
                md_search_array = md_group_one if md_group_two == "" else md_group_two
                md_replace = "<mark>" + md_search_array.replace("\=", "=") + "</mark>"
                md_search_array = f"=={md_search_array}=="
                self.md_data = re.sub(
                    re.escape(md_search_array), md_replace, self.md_data
                )
        self.md_lock.release()

    # Replace subscript or superscript
    def replaceSubSup(self, md_regex):
        self.md_lock.acquire()
        md_search = re.findall(md_regex, self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_text_one, md_text_two, md_key = md_array
                md_suffix = "p" if md_key == "^" else "b"
                md_replace = (
                    f"{md_text_one}<su{md_suffix}>{md_text_two}</su{md_suffix}>"
                )
                md_search_array = re.escape(
                    f"{md_text_one}{md_key}{md_text_two}{md_key}"
                )
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace strikethrough
    def replaceStrikethrough(self):
        self.md_lock.acquire()
        md_search = re.findall(
            self.md_regex["strikethrough"], self.md_data, re.MULTILINE
        )
        if md_search != []:
            for md_array in md_search:
                md_replace = f"<s>{md_array}</s>"
                md_search_array = re.escape(f"~~{md_array}~~")
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace difinition
    def replaceDefinition(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["definition"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_list = md_array.split("\n")
                md_definition_list = "<dl>"
                for md_definition in md_list[: len(md_list) - 1]:
                    md_index = md_list.index(md_definition)
                    md_definition_list += (
                        f"<dt>{md_definition}</dt>"
                        if md_index == 0
                        else f"<dd>{md_definition[2:]}</dd>"
                    )
                md_definition_list += "</dl>\n"
                self.md_data = re.sub(md_array, md_definition_list, self.md_data)
        self.md_lock.release()

    # Replace footnote
    def replaceFootnote(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["footnote"], self.md_data, re.MULTILINE)
        if md_search != []:
            md_list = "<ol>"
            md_footer = ""
            for md_array in md_search:
                md_reference, md_key, md_footnote, _ = md_array
                if md_key == "":
                    md_replace = f"<sup id='fnref:{md_reference}'><a href='#fn:{md_reference}'>{md_reference}</a></sup> "
                    md_search_array = "\[\^" + md_reference + "\][^\:]"
                    self.md_data = re.sub(md_search_array, md_replace, self.md_data)
                else:
                    md_footer += f"[^{md_reference}]:{md_footnote}\n\n"
                    md_list += f"<li id='fn:{md_reference}'>{md_footnote[1:]} <a href='#fnref:{md_reference}'>&#8617;</a></li>"
            md_list += "</ol>\n\n"
            md_footer = re.escape(md_footer)
            self.md_data = re.sub(md_footer, md_list, self.md_data)
        self.md_lock.release()

    # Replace tasklist
    def replaceTasklist(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["tasklist"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_task = md_array.split("\n")
                md_search_array = re.escape(md_array)
                md_replace = "<ul>"
                for md_task_array in md_task[: len(md_task) - 1]:
                    md_key = md_task_array[:5]
                    md_text = md_task_array[6:]
                    if md_key == "- [x]":
                        md_replace += f"<li>&#9745; {md_text}</li>"
                    else:
                        md_replace += f"<li>&#9744; {md_text}</li>"
                md_replace += "</ul>\n"
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace underline
    def replaceUnderline(self):
        self.md_lock.acquire()
        md_search = re.findall(
            self.md_regex["format_underline"], self.md_data, re.MULTILINE
        )
        if md_search != []:
            for md_array in md_search:
                md_text = md_array[0]
                md_replace = f"<u>{md_text}</u>"
                md_search_array = f"_{md_text}_"
                self.md_data = re.sub(md_search_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace plaintext
    def replacePlainText(self):
        self.md_lock.acquire()
        md_search = re.findall(self.md_regex["plaintext"], self.md_data, re.MULTILINE)
        if md_search != []:
            for md_array in md_search:
                md_replace = f"<pre>{md_array[: len(md_array) - 2]}</pre>\n"
                self.md_data = re.sub(md_array, md_replace, self.md_data)
        self.md_lock.release()

    # Replace markdown
    def replaceMarkdown(self):
        self.md_threads.append(threading.Thread(target=self.replaceHeading))
        self.md_threads.append(threading.Thread(target=self.replaceParagraph))
        self.md_threads.append(threading.Thread(target=self.replaceFormat))
        self.md_threads.append(threading.Thread(target=self.replaceUnderline))
        self.md_threads.append(threading.Thread(target=self.replaceImage))
        self.md_threads.append(threading.Thread(target=self.replaceLink))
        self.md_threads.append(threading.Thread(target=self.replaceBlockquote))
        self.md_threads.append(
            threading.Thread(target=self.replaceList, args=(self.md_regex["ordered"],))
        )
        self.md_threads.append(
            threading.Thread(
                target=self.replaceList, args=(self.md_regex["unordered"],)
            )
        )
        self.md_threads.append(threading.Thread(target=self.replaceCode))
        self.md_threads.append(threading.Thread(target=self.replaceHorizontal))
        self.md_threads.append(threading.Thread(target=self.replaceTable))
        self.md_threads.append(threading.Thread(target=self.replaceQuickLink))
        self.md_threads.append(threading.Thread(target=self.replaceHighlight))
        self.md_threads.append(
            threading.Thread(
                target=self.replaceSubSup, args=(self.md_regex["superscript"],)
            )
        )
        self.md_threads.append(
            threading.Thread(
                target=self.replaceSubSup, args=(self.md_regex["subscript"],)
            )
        )
        self.md_threads.append(threading.Thread(target=self.replaceStrikethrough))
        self.md_threads.append(threading.Thread(target=self.replaceDefinition))
        self.md_threads.append(threading.Thread(target=self.replaceFootnote))
        self.md_threads.append(threading.Thread(target=self.replaceTasklist))
        self.md_threads.append(threading.Thread(target=self.replacePlainText))

        for t in self.md_threads:
            t.start()

        for t in self.md_threads:
            t.join()

# Needed functions
# Input pdf should be in input/ directory
# Kaikki dictionary files should be in dictionary/ directory
# Output files will be in output/ directory
import jsonl
import pypdf

def extract_sentencelist(filename):
    reader = pypdf.PdfReader(filename)

    # Starts from 1, put -1 in last_page to choose last page of the pdf
    first_page = 2
    last_page = -1

    if last_page == -1:
        last_page = len(reader.pages)

    pages = [reader.pages[i].extract_text() for i in range(first_page-1,last_page)] # Read the pdf pages
    pages = [''.join(e for e in page if e != "\n") for page in pages] # Remove all  line breaks
    fulltext = " ".join(pages)
    sentence_list = fulltext.split(".")
    return sentence_list


"""
valid_words_filename = "dictionaries/"+r"kaikki.org-dictionary-Esperanto-words.jsonl"
filename = r"la_hobito.pdf"
"""

def create_csv_string(kaikki_dictionary_filename, pdf_filename):

    allsentences = extract_sentencelist("input/"+pdf_filename)
    kaikki_dictionary_filename = "dictionaries/" + kaikki_dictionary_filename
    # Create word:entry dictionary
    valid_word_set = {item["word"]:item for item in jsonl.load(kaikki_dictionary_filename)}

    # List of found base words
    base_word_set = set([])

    # All already seen words
    visited = set([])

    # Output csv file
    csv_ = ""

    i = 0

    # Iterate over all sentences
    for sentence in allsentences:
        cleaned_sentence = "".join([e for e in sentence if e.isalnum() or e == " "]).split(" ")
        for string in cleaned_sentence:

            # Skip already sen words
            if string in visited:
                continue
            visited.add(string)


            if string in valid_word_set.keys():
                print(string)

                if string == "punta":
                    print(valid_word_set[string])
                    input()

                word = valid_word_set[string]
                # Check if entry has "form-of" tag and then get the original form
                if "tags" in word["senses"][0].keys() and "form-of" in word["senses"][0]["tags"]:
                    base_form = word["senses"][0]["form_of"][0]["word"]
                # If "form-of" tag not found, just take the word
                else:
                    base_form = string

                # Skip repeated or non_existant base forms
                if base_form in visited or base_form not in valid_word_set.keys():
                    continue

                # Create csv line based on base form
                word = valid_word_set[base_form]

                # Account for this weird edge casse
                if "glosses" not in word["senses"][0].keys():
                    continue


                csv_line = ":".join([base_form, "<br>".join(word["senses"][0]["glosses"]), sentence])
                base_word_set.add(base_form)
                csv_ += csv_line + "\n"

                # Remember base form for later
                visited.add(base_form)
    return csv_
    """
    with open("output/"+pdf_filename.split(".")[0]+".csv", "w", encoding="utf-8") as file:
        file.write(csv_)"""
"""Peforms named entity recognition"""

import sys
import gzip
import subprocess
import re

text_tag = re.compile("<TEXT>.*?</TEXT>", flags=re.DOTALL)
doc_tag = re.compile("<DOC>.*?</DOC>", flags=re.DOTALL)

def get_ner_text(text):
    """Performs the NER tagging on the text.


    It invokes the stanford NER tagger. As the NER tagger expects
    the input argument to be a file name, it first creates a temporary
    file and writes the text to it.

    It returns the output in inlineXML format. See
    http://nlp.stanford.edu/software/crf-faq.shtml#j for further
    details.
    """

    tmpfilename = "/tmp/tmp_ner.txt"
    command = ["./lib/stanford-ner-2012-04-07/ner7.sh", tmpfilename]

    # Write to tmp file
    with open(tmpfilename, "w") as f:
        f.write(text)

    p = subprocess.Popen(command, stdout=subprocess.PIPE)

    return p.stdout.read()


def process_doc(doc):
    """Performs NER tagging on the text section and returns
    the resultant doc.

    The text section is marked by <TEXT> and </TEXT>.
    """

    try:
        texts = text_tag.findall(doc)
        if texts:
            text = texts[0]
            ner_text = get_ner_text(text)
            return text_tag.sub(ner_text, doc)
        else:
            return ''
    except:
        print doc
        print "Unexpected error:", sys.exc_info()[0]


def process_file(data, output_file):
    with open(output_file, "w") as f:
        for doc in doc_tag.findall(data):
            d = process_doc(doc)
            f.write(d)

def get_gzip_data(filename):
    """Read daa from gzip file.
    
    param
    ----
        filename: Input gzip file.
    """
    with gzip.open(filename, "rb") as f:
        data = f.read()

    return data


def main(argv):
    import glob
    import os

    input_dir = argv[0]
    output_dir = argv[1]

    for fpath in glob.iglob(os.path.join(input_dir, "*.gz")):
        print fpath
        fname = os.path.splitext(os.path.split(fpath)[1])[0]
        fout = os.path.join(output_dir, fname)

        process_file(get_gzip_data(fpath), fout)


if __name__ == "__main__":
    main(sys.argv[1:])

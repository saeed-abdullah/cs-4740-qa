
from .. import ner

def test_get_ner_text():
    text = "Ezra Cornell used to live in Ithaca."
    expected = "<PERSON>Ezra Cornell</PERSON> used to live in "+\
    "<LOCATION>Ithaca</LOCATION>."

    assert ner.get_ner_text(text) == expected

def test_process_doc():
    doc = "<DOC><TEXT>Ezra Cornell used to live in Ithaca.</TEXT></DOC>"
    expected = "<DOC><TEXT><PERSON>Ezra Cornell</PERSON> used to live "+\
        "in <LOCATION>Ithaca</LOCATION>.</TEXT></DOC>"

    assert ner.process_doc(doc) == expected

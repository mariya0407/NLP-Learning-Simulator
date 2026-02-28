import streamlit as st

# -----------------------------------------
# 1. UI CONFIGURATION (MUST BE FIRST)
# -----------------------------------------
st.set_page_config(page_title="NLP Simulator", page_icon="🧠", layout="wide")

import streamlit.components.v1 as components
import spacy
from spacy import displacy
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import CFG, ChartParser
import pandas as pd

# -----------------------------------------
# 2. SETUP & CACHING 
# -----------------------------------------
@st.cache_resource
def setup_nltk():
    """Download required NLTK data quietly."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

@st.cache_resource
def load_spacy():
    """Load spaCy model, download if missing."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

setup_nltk()
nlp = load_spacy()
stemmer = PorterStemmer()

# -----------------------------------------
# 3. APP LAYOUT & SIDEBAR
# -----------------------------------------
st.title("🧠 Interactive NLP Learning Simulator")
st.markdown("Welcome! Choose an NLP concept from the sidebar to simulate how machines process human language.")

# Sidebar Navigation
concept = st.sidebar.selectbox(
    "Select NLP Concept to Simulate",
    [
        "1. Tokenization", 
        "2. Stemming vs Lemmatization", 
        "3. Part-of-Speech (POS) Tagging", 
        "4. Named Entity Recognition (NER)",
        "5. Syntax Trees & Parsing"
    ]
)

# -----------------------------------------
# 4. SIMULATION LOGIC
# -----------------------------------------

if concept == "1. Tokenization":
    st.header("✂️ Tokenization")
    st.markdown("**Concept:** Breaking down text into smaller units called 'tokens' (words, punctuation, or sentences).")
    
    text = st.text_area("Enter text to tokenize:", "Hello there! How are you doing today? NLP is amazing.")
    
    if st.button("Run Tokenization Simulation"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sentence Tokens")
            sentences = sent_tokenize(text)
            for i, sent in enumerate(sentences):
                st.info(f"**Sentence {i+1}:** {sent}")
                
        with col2:
            st.subheader("Word Tokens")
            words = word_tokenize(text)
            st.write(words)

elif concept == "2. Stemming vs Lemmatization":
    st.header("🌱 Stemming vs. Lemmatization")
    st.markdown("**Concept:** Reducing words to their base or root form. \n* **Stemming** simply chops off word endings (fast, but often creates non-words).\n* **Lemmatization** uses vocabulary and morphological analysis to return a proper dictionary word.")
    
    text = st.text_input("Enter a sentence with variations of words (e.g., running, runs, ran, better):", "The runners are running quickly and ran better than before.")
    
    if st.button("Run Morphology Simulation"):
        doc = nlp(text)
        
        # Prepare data for comparison
        data = []
        for token in doc:
            if not token.is_punct and not token.is_space:
                original = token.text
                stemmed = stemmer.stem(original)
                lemmatized = token.lemma_
                data.append({"Original Word": original, "Stemmed": stemmed, "Lemmatized": lemmatized})
                
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

elif concept == "3. Part-of-Speech (POS) Tagging":
    st.header("🏷️ Part-of-Speech (POS) Tagging")
    st.markdown("**Concept:** Assigning grammatical categories (like Noun, Verb, Adjective) to each word based on its context.")
    
    text = st.text_area("Enter text:", "Apple is looking at buying U.K. startup for $1 billion.")
    
    if st.button("Run POS Simulation"):
        doc = nlp(text)
        pos_data = []
        for token in doc:
            if not token.is_space:
                pos_data.append({"Word": token.text, "POS Tag": token.pos_, "Detailed Tag": token.tag_, "Explanation": spacy.explain(token.tag_)})
                
        df = pd.DataFrame(pos_data)
        st.table(df)

elif concept == "4. Named Entity Recognition (NER)":
    st.header("🔍 Named Entity Recognition (NER)")
    st.markdown("**Concept:** Identifying and classifying key information (entities) in text into predefined categories like Person, Organization, Location, etc.")
    
    text = st.text_area("Enter text containing names, places, dates, or organizations:", "Elon Musk founded SpaceX in 2002. It is headquartered in Hawthorne, California.")
    
    if st.button("Run NER Simulation"):
        doc = nlp(text)
        
        if not doc.ents:
            st.warning("No named entities found in the text.")
        else:
            html_text = text
            for ent in doc.ents:
                highlight = f"<mark style='background-color: #f0f2f6; padding: 2px 4px; border-radius: 4px;'><b>{ent.text}</b> <span style='color: #ff4b4b; font-size: 0.8em;'>[{ent.label_}]</span></mark>"
                html_text = html_text.replace(ent.text, highlight)
                
            st.markdown(html_text, unsafe_allow_html=True)
            
            st.subheader("Entity Breakdown:")
            ner_data = [{"Entity": ent.text, "Label": ent.label_, "Explanation": spacy.explain(ent.label_)} for ent in doc.ents]
            st.dataframe(pd.DataFrame(ner_data), use_container_width=True)

elif concept == "5. Syntax Trees & Parsing":
    st.header("🌳 Syntax Trees & Parsing")
    st.markdown("**Concept:** Parsing analyzes the grammatical structure of a sentence. We will look at two methods: rigid Context-Free Grammar (like Chomsky Normal Form) and modern Dependency Parsing.")
    
    st.divider()
    
    # --- SIMULATION A: CFG PARSER (NLTK) ---
    st.subheader("1. Context-Free Grammar (CFG) Parser")
    st.markdown("This simulates a parser using rigid phrase structure rules. It builds a syntax tree *only* if the sentence perfectly matches the defined grammar.")
    
    
    
    # Define a simple strict grammar
    grammar_string = """
      S -> NP VP
      NP -> Det N | 'John' | 'Mary'
      VP -> V NP | V
      Det -> 'the' | 'a'
      N -> 'dog' | 'cat' | 'telescope' | 'car'
      V -> 'saw' | 'ate' | 'chased' | 'drove'
    """
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_area("Defined Grammar Rules & Vocabulary:", grammar_string, height=200, disabled=True)
    
    with col2:
        cfg_sentence = st.text_input("Enter a sentence strictly using the vocabulary on the left:", "John chased the dog")
        
        if st.button("Generate CFG Tree"):
            try:
                # Load grammar and initialize parser
                grammar = CFG.fromstring(grammar_string)
                parser = ChartParser(grammar)
                
                # Format tokens (handle case sensitivity for proper nouns)
                tokens = cfg_sentence.lower().split()
                tokens = [t.capitalize() if t in ['john', 'mary'] else t for t in tokens]
                
                trees = list(parser.parse(tokens))
                if trees:
                    for tree in trees:
                        # Print the ASCII tree structure
                        st.code(tree.pretty_format(), language="text")
                else:
                    st.warning("Could not parse sentence. Ensure the grammar rules support this exact sentence structure (e.g., 'the cat ate a dog').")
            except ValueError as e:
                st.error(f"Vocabulary Error: Only use words defined in the grammar rules. Details: {e}")

    st.divider()

    # --- SIMULATION B: DEPENDENCY PARSING (SPACY) ---
    st.subheader("2. Dependency Parsing Graph")
    st.markdown("Unlike CFG, which breaks sentences into nested phrases, dependency parsing maps the direct grammatical relationships (dependencies) between words. Try this with *any* sentence!")
    
    dep_text = st.text_input("Enter any sentence to visualize dependencies:", "The quick brown fox jumps over the lazy dog.")
    
    if st.button("Generate Dependency Graph"):
        doc = nlp(dep_text)
        # Render the dependency graph to HTML
        html = displacy.render(doc, style="dep", options={"distance": 120, "bg": "#ffffff", "color": "#000000"})
        # Display the HTML in Streamlit
        components.html(html, height=400, scrolling=True)
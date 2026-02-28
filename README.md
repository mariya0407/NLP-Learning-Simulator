# NLP-Learning-Simulator

# 🧠 Interactive NLP Learning Simulator

An interactive, web-based educational tool designed to simulate and visualize core Natural Language Processing (NLP) concepts. Built with Python and Streamlit, this application allows users to input their own text and instantly see how machines process, break down, and understand human language.

## ✨ Features

The simulator currently covers 5 foundational NLP concepts:

1. **Tokenization:** Breaks text down into sentence and word tokens using NLTK.
2. **Stemming vs. Lemmatization:** Compares rule-based stemming (Porter Stemmer) with vocabulary-based lemmatization (spaCy) to show how words are reduced to their root forms.
3. **Part-of-Speech (POS) Tagging:** Assigns grammatical categories (Noun, Verb, Adjective, etc.) to words in context, complete with definitions.
4. **Named Entity Recognition (NER):** Highlights and classifies key information (Persons, Organizations, Dates, Locations) using custom HTML/CSS rendering.
5. **Syntax Trees & Parsing:** * **Context-Free Grammar (CFG):** Simulates a rigid phrase-structure parser drawing ASCII syntax trees using NLTK.
   * **Dependency Parsing:** Generates a modern, visual map of grammatical relationships between words using spaCy's `displacy`.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **NLP Libraries:** [spaCy](https://spacy.io/) (`en_core_web_sm`), [NLTK](https://www.nltk.org/)
* **Data Handling:** Pandas

## 🚀 Installation & Setup

Follow these steps to run the simulator locally on your machine.

**1. Clone the repository**
```
git clone [https://github.com/mariya0407/NLP-Learning-Simulator.git](https://github.com/mariya0407/NLP-Learning-Simulator.git)
cd NLP-Learning-Simulator
```

2. Create and activate a virtual environment

Mac/Linux:
```
python -m venv venv
source venv/bin/activate
```
Windows:
```
python -m venv venv
venv\Scripts\activate
```

3. Install the required dependencies
```
pip install -r requirements.txt
```
(Note: The application is designed to automatically download the necessary NLTK (punkt) and spaCy (en_core_web_sm) language models on its first run.)

4. Run the application
```
streamlit run app.py
```
The app will automatically open in your default web browser at http://localhost:8501.



```
Link to Gemini chat: https://gemini.google.com/app/0c1bcc5027a752cf
```

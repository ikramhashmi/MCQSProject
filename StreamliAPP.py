import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqsgenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqsgenerator.MCQGenerator import generate_evaluate_chain
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqsgenerator.logger import logging



RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        "correct": "correct answer"
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        "correct": "correct answer"
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        "correct": "correct answer"
    }
}

# Streamlit UI
st.title("MCQ Generator With LangChain 🦜️🔗")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT File")
    mcq_count = st.text_input("Enter the number of MCQs to be generated")
    subject = st.text_input("Enter the Subject", max_chars=20)
    tone = st.text_input("Complexity Level of questions", max_chars=20, placeholder="Easy, Medium, Hard")
    button = st.form_submit_button("Generate MCQs")

# Generate MCQs on button click
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Generating MCQs... ⏳"):
        try:
            # Read the file content
            text = read_file(uploaded_file)

            # Generate MCQs using LangChain
            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON),  
                }
            )

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error(f"Error: {e}")
        else:
            if isinstance(response, dict):
                quiz = response.get("quiz")
                
                if quiz is not None:
                    try:
                        # Debugging - Print the raw quiz data before parsing
                        print("Raw Quiz Data:", quiz)
                        
                        table_data = get_table_data(quiz)

                        # Ensure valid data
                        if table_data and isinstance(table_data, list):
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.text_area(label="Review", value=response.get("review"), height=200)
                            st.dataframe(df)  # Display DataFrame in Streamlit
                        else:
                            st.error("Error: Unable to parse quiz data.")

                    except json.JSONDecodeError as e:
                        st.error(f"JSON Decode Error: {e}")
                        print("Invalid JSON:", quiz)  # Print invalid JSON for debugging

                else:
                    st.write(response)

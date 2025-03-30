import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)  # ✅ Use PdfReader instead of PdfFileReader
            text = ""
            for page in pdf_reader.pages:
                extracted_text = page.extract_text() or ""  # ✅ Handle None values
                text += extracted_text
            return text
        except Exception as e:
            raise Exception(f"Error reading the PDF file: {e}")  # ✅ Provide detailed error

    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            raise Exception(f"Error reading the TXT file: {e}")

    else:
        raise Exception("Unsupported file format. Only PDF and TXT files are supported.")  # ✅ Fixed typo

def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "No Question Available")  # ✅ Use `.get()` to prevent KeyError
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value.get("options", {}).items()
                ]
            ) if "options" in value else "No Options Available"
            
            correct = value.get("correct", "No Answer Provided")
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except json.JSONDecodeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)  # ✅ More specific error handling
        return False
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

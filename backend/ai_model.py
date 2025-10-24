import sys, json, re, os
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        elif ext == ".docx":
            doc = Document(file_path)
            text = " ".join([para.text for para in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            text = ""
    except Exception as e:
        text = str(e)

    return text

def score_resume(text):
    if not text:
        return {
            "error": "Could not read resume content properly."
        }

    text = text.lower()

    ai_ml = 100 if ("machine learning" in text or "ai" in text or "artificial intelligence" in text) else 60
    llm = 100 if ("llm" in text or "large language model" in text) else 40
    python_score = 100 if "python" in text else 70
    exp = 100 if re.search(r"\b5\+ years\b|\b5 years\b", text) else 50

    overall = round((ai_ml + llm + python_score + exp) / 4, 2)
    return {
        "AI/ML Match (%)": ai_ml,
        "LLM Match (%)": llm,
        "Python Match (%)": python_score,
        "5+ Years Exp (%)": exp,
        "Overall Score (%)": overall
    }

if __name__ == "__main__":
    file_path = sys.argv[1]
    text = extract_text(file_path)
    result = score_resume(text)
    print(json.dumps(result))

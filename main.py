from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
import spacy

# Load SpaCy English model
nlp_en = spacy.load("en_core_web_sm")

app = FastAPI(title="Entity Extraction GUI")

# Root endpoint: shows GUI form
@app.get("/", response_class=HTMLResponse)
def gui():
    html_content = """
    <html>
        <head>
            <title>Entity Extraction</title>
        </head>
        <body>
            <h2>Upload a text file</h2>
            <form action="/file/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Extract Entities">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# File upload endpoint
@app.post("/file/", response_class=HTMLResponse)
def extract_entities(file: UploadFile = File(...)):
    content_bytes = file.file.read()
    content_text = content_bytes.decode()

    doc = nlp_en(content_text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    # Simple HTML display of results
    html_content = f"""
    <html>
        <head>
            <title>Extraction Result</title>
        </head>
        <body>
            <h2>Original Text</h2>
            <p>{content_text}</p>
            <h2>Extracted Entities</h2>
            <ul>
    """
    for ent in entities:
        html_content += f"<li>{ent['text']} - {ent['label']}</li>"
    html_content += """
            </ul>
            <a href="/">Go back</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
    

#uvicorn main:app --reload

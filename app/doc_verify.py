# verify_docs.py
import google.generativeai as genai

GEMINI_KEY="AIzaSyCIC7vL-yOA_6GSGBVnNjRhb0mzc7pe5-c"
genai.configure(api_key=GEMINI_KEY)
def verify_document_text(doc_type, text):
    import json
    from datetime import datetime
    import re
    import google.generativeai as genai

    # Use current local date to avoid Gemini using its own internal (old) date
    today = datetime.now().strftime("%d-%b-%Y")

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a financial document verification expert.
    Analyze the following {doc_type} text and decide whether it seems genuine or fake.
    Respond in the following JSON format:
    {{
      "status": "Verified" or "Fake",
      "explanation": "short reason in one or two sentences"
    }}

    Document Type: {doc_type}
    Document Content:
    {text}
    """

    response = model.generate_content(prompt)
    result_text = response.text.strip()
    cleaned_text = re.sub(r"```(?:json)?", "", result_text).replace("```", "").strip()
    try:
        # Try parsing clean JSON
        result = json.loads(result_text)
        status = result.get("status", "Unknown")
        explanation = result_text.replace("```json", "").replace("```", "").strip()
    except Exception:
        # Fallback if Gemini didn’t return JSON
        if "fake" in cleaned_text.lower():
            status = "Fake"
        else:
            status = "Verified"
        explanation = cleaned_text

    return {"status": status, "explanation": explanation}



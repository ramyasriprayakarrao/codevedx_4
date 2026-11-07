# Internal Help Desk Chatbot

A beginner-friendly internal IT help-desk chatbot built with Python's standard library. It uses a small editable FAQ knowledge base and keyword-overlap scoring to select an answer.

## Features
- Browser-based chat interface
- Answers common IT questions: password reset, Wi-Fi, email, software, slow computer, hardware, VPN, IT tickets, phishing, and shared-folder access
- Suggestion buttons for common questions
- Editable `knowledge_base.json`
- No scikit-learn, TensorFlow, PyTorch, Flask, or external Python packages

## Requirements
- Python 3.8 or newer
- A web browser

## Run in VS Code (Windows)

1. Extract the ZIP file.
2. Open the extracted `Internal_Help_Desk_Chatbot` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run:

```powershell
py --version
py main.py
```

5. Keep the terminal open and visit:

`http://127.0.0.1:8000`

6. Ask a question in the chat window.
7. To stop the server, return to the terminal and press `Ctrl+C`.

If `py` is not recognized, try:

```powershell
python --version
python main.py
```

## Add or edit answers

Open `knowledge_base.json`. Each FAQ entry has:
- `question`: the main question/topic
- `keywords`: words likely to appear in a user's question
- `aliases`: alternative ways users may phrase the question
- `answer`: the response shown by the chatbot

Keep the JSON syntax valid (double quotes and commas). Restart `py main.py` after editing.

## How matching works

The program tokenizes the user's question and compares its words with each FAQ's question, keywords, and aliases. It scores overlap and returns the best match when it passes a threshold. This is a simple rule-based retrieval chatbot, not a trained large language model. It does not learn from conversations.

## Important security note

This is an educational local demo. It has no login, database, audit logging, role-based access, or company-system integration. Do not enter passwords, OTPs, personal data, or confidential company information. For real company use, add authentication, access controls, approved knowledge sources, logging policies, and security review.

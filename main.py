from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "knowledge_base.json"

def load_knowledge():
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

def tokenize(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def answer_question(question):
    q = question.strip()
    if not q:
        return {"answer": "Please type a question so I can help.", "matched": False}

    words = tokenize(q)
    if words & {"hello", "hi", "hey", "goodmorning", "goodafternoon"} and len(words) <= 4:
        return {"answer": "Hello! I’m the Internal Help Desk Assistant. Ask me about passwords, Wi-Fi, email, software, or IT support.", "matched": True}

    if words & {"thanks", "thank", "thankyou"}:
        return {"answer": "You’re welcome! Is there anything else I can help you with?", "matched": True}

    entries = load_knowledge()
    best_entry = None
    best_score = 0.0

    # Lightweight keyword matching; no machine-learning packages required.
    for entry in entries:
        candidates = [entry.get("question", "")] + entry.get("keywords", []) + entry.get("aliases", [])
        candidate_words = set()
        for candidate in candidates:
            candidate_words |= tokenize(candidate)

        if not candidate_words:
            continue

        overlap = len(words & candidate_words)
        coverage = overlap / max(1, len(words))
        jaccard = overlap / max(1, len(words | candidate_words))
        score = (0.75 * coverage) + (0.25 * jaccard)

        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry and best_score >= 0.18:
        return {
            "answer": best_entry.get("answer", "Please contact the IT help desk for assistance."),
            "matched": True,
            "topic": best_entry.get("question", "Help desk")
        }

    return {
        "answer": "I couldn’t find a confident answer in the help-desk knowledge base. Please contact your IT support team and include the issue, any error message, and when it started.",
        "matched": False
    }

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, content, content_type="application/json; charset=utf-8"):
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            try:
                page = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
                self._send(200, page, "text/html; charset=utf-8")
            except OSError:
                self._send(500, "Could not load the chat page.", "text/plain; charset=utf-8")
        elif path == "/style.css":
            self._send(200, (ROOT / "static" / "style.css").read_text(encoding="utf-8"), "text/css; charset=utf-8")
        elif path == "/script.js":
            self._send(200, (ROOT / "static" / "script.js").read_text(encoding="utf-8"), "application/javascript; charset=utf-8")
        elif path == "/api/health":
            self._send(200, json.dumps({"status": "running"}))
        else:
            self._send(404, json.dumps({"error": "Not found"}))

    def do_POST(self):
        if urlparse(self.path).path != "/api/chat":
            self._send(404, json.dumps({"error": "Not found"}))
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = payload.get("message", "")
            result = answer_question(str(question))
            self._send(200, json.dumps(result, ensure_ascii=False))
        except (ValueError, json.JSONDecodeError):
            self._send(400, json.dumps({"error": "Invalid request. Send JSON with a message field."}))
        except Exception:
            self._send(500, json.dumps({"error": "An unexpected server error occurred."}))

    def log_message(self, fmt, *args):
        print("[HTTP]", fmt % args)

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("=" * 58)
    print("       INTERNAL HELP DESK CHATBOT")
    print("       No scikit-learn / no external packages")
    print("=" * 58)
    print("Open this address in your browser: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped.")
        server.server_close()

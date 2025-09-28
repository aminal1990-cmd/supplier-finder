from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # اجازه میده از هر سایتی به این سرویس درخواست بدیم (مشکل CORS حل میشه)

AUTH = os.environ.get("AGENT_TOKEN", "")

# فعلاً نمونه‌ی تست (بعداً منطق واقعیِ جستجو را جایگزین می‌کنیم)
def run_supplier_agent(query: str):
    return [
        {
            "name": "تامین‌کننده نمونه رب گوجه",
            "country": "ایران",
            "products": ["رب گوجه 36-38 بریکس"],
            "contacts": {"email": "sales@example.com", "phone": "+98-21-123456"},
            "source": "https://example.com",
            "note": "این فقط نمونه‌ی تست است"
        }
    ]

@app.post("/search")
def search():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if AUTH and token != AUTH:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}
    query = (data.get("query") or data.get("q") or "").strip()
    if not query:
        return jsonify({"error": "empty query"}), 400

    results = run_supplier_agent(query)
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

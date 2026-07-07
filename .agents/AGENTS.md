# Forensic R&D Project Guidelines

This project is built under the Division of Identification and Forensic Science (מז"פ - חטיבה לזיהוי פלילי) of the Israel Police. All future development, editing, and deployment activities in this workspace must adhere to the following environment rules and design standards:

## 1. Execution & Environment Rules
* **Python Launcher**: Always use the launcher `py` rather than `python` to execute Python scripts (e.g. `py app.py`, `py -m pip install`), as `python` is not directly on the PATH.
* **Python Version**: Development is targeted at Python `3.14.4`.
* **Server Port**: Local servers (such as Streamlit or Flask) must run on port `5001`.
* **Internal Police IPs**: When adding network requests or API clients, always provide configuration templates/variables for internal police IPs (e.g., `POLICE_INTERNAL_SERVER_IP = "10.x.x.x"`).

## 2. Local Hardware & Models
To prevent downloading models over bandwidth-constrained or offline networks:
* **EasyOCR**: Use pre-installed paths:
  * Detection: `C:\Users\nafei\.EasyOCR\model\craft_mlt_25k.pth`
  * English Recognition: `C:\Users\nafei\.EasyOCR\model\english_g2.pth`
* **Ollama Local LLMs**: Use locally installed models:
  * `minicpm-v:latest`
  * `llama3.2-vision:latest`
* **Tesseract**: Avoid depending on `pytesseract` unless path is manually resolved, or prefer EasyOCR / Cloud APIs.

## 3. UI Design Standards
* **Aesthetics**: Premium visual styling utilizing glassmorphic cards, smooth micro-animations, and custom typography (Assistant, Rubik).
* **Theme**: Sleek Dark Slate backgrounds (e.g., `#0b0f19`).
* **Bilingual & RTL**: Layouts must support Right-to-Left (RTL) alignment for Hebrew, alongside English translation support. Wrap markdown and custom HTML elements in CSS that enforces `direction: RTL; text-align: right;` for Hebrew text.

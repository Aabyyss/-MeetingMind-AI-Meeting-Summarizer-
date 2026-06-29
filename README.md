# -MeetingMind-AI-Meeting-Summarizer-
An AI-powered meeting assistant that automatically summarizes meeting transcripts, extracts action items and deadlines, and generates concise notes using NLP, improving meeting productivity and documentation

> Transform long meeting transcripts into structured summaries, action items, and deadlines — in seconds.

---

## Features

| Feature | Details |
|---|---|
| 📁 File upload | `.txt`, `.pdf`, `.docx` supported |
| ✨ AI Summary | Brief / Standard / Executive lengths |
| ✅ Action Items | Task + Owner + Due date + Priority |
| 📅 Deadlines | Extracted and listed clearly |
| 👥 People | Who said what, who owns what |
| 📥 PDF Export | Clean, formatted export |
| 🌐 Language | English, Urdu, Arabic, French, Spanish |

---

## Quick Start

### 1. Clone / copy the project
```bash
cd project1-meeting-summarizer
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY="sk-ant-..."    # Linux / macOS
set  ANTHROPIC_API_KEY=sk-ant-...        # Windows CMD
```

Or create a `.env` file and load it with `python-dotenv`.

### 5. Run the app
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Project Structure

```
project1-meeting-summarizer/
├── app.py                    # Streamlit UI
├── requirements.txt
├── utils/
│   ├── ai_processor.py       # Anthropic API call + JSON parsing
│   ├── parser.py             # File reader (txt / pdf / docx)
│   └── pdf_exporter.py       # PDF generation with fpdf2
└── sample_data/
    └── sample_meeting.txt    # Demo transcript
```

---

## Usage

1. **Upload** a `.txt`, `.pdf`, or `.docx` transcript — or **paste** text directly.
2. Choose a **summary length** in the sidebar (Brief / Standard / Executive).
3. Click **Analyze Meeting**.
4. Browse tabs: Summary · Action Items · Deadlines · People.
5. Click **Download PDF** to export.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ Yes | Your Anthropic API key |

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** – UI framework
- **Anthropic Python SDK** – Claude claude-sonnet-4-6
- **fpdf2** – PDF generation
- **pdfplumber / pypdf** – PDF reading
- **python-docx** – DOCX reading

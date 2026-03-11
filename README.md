# RecruitIQ — AI-Powered Resume Analyzer & Interview Prep

> A 3-agent Streamlit app powered by Google Gemini that analyzes a candidate's resume against a job description, scores them across 20–25 traits, and generates tailored interview questions.

---

## What It Does

| Agent | Role | Output |
|---|---|---|
| **① Analyst** | Reads the CV + JD together | Summary, Strengths, Gaps, Match Score /10 |
| **② Scorer** | Extracts 20–25 traits from the JD | Scores each trait /10 → Overall score /100 |
| **③ Interviewer** | Studies both inputs | 12 tailored questions across 4 categories |

---

## Prerequisites

- Python 3.9 or higher
- A free Gemini API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## Setup & Installation

### 1. Clone or download the project

```bash
git clone https://github.com/yourname/recruitiq.git
cd recruitiq
```

Or just place `app.py` and `requirements.txt` in a folder and navigate to it.

---

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set up your API key

Create a `.env` file in the same folder as `app.py`:

```bash
touch .env
```

Add your Gemini API key to it:

```
GEMINI_API_KEY=AIzaSy...your_key_here
```

> The app reads this automatically via `python-dotenv`. You do **not** need to paste the key into the UI.

---

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## How to Use

1. **Paste** the full job description into the left text box
2. **Upload** the candidate's resume as a PDF
3. **Select** a Gemini model from the sidebar (default: `gemini-3-flash-preview`)
4. **Click** the Run button
5. Wait ~15–30 seconds for all 3 agents to complete
6. Review the results:
   - Overall score ring + candidate summary
   - Strengths (left) and Gaps (middle) side by side
   - Trait breakdown bars (right) — hover for evidence notes
   - Interview questions grouped by category below each column

---

## Project Structure

```
recruitiq/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Your API key (not committed to git)
└── README.md           # This file
```

---

## Dependencies

```
streamlit>=1.35.0
google-generativeai>=0.8.0
python-dotenv>=1.0.0
```

---

## Notes

- The PDF is sent **inline** to Gemini — no files are stored anywhere
- All 3 agents run sequentially in a single button click
- If Agent 2 or 3 returns malformed JSON, the raw output is shown in an expander at the bottom for debugging
- Larger/denser resumes may take longer — `gemini-1.5-pro` gives the most thorough results but is slower

---

## .gitignore recommendation

If pushing to GitHub, make sure to ignore your `.env`:

```
.env
venv/
__pycache__/
*.pyc
```

---

## License

MIT — free to use, modify, and distribute.
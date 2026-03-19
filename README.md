# RecruitIQ — AI-Powered Resume Analyzer & Interview Prep

> A 4-agent Streamlit app powered by Google Gemini that blindly reviews a candidate's resume, analyzes fit, scores across 20–25 traits, and generates tailored interview questions — all in just **2 API calls**.

---

## What It Does

| Agent | Role | API Call | Output |
|---|---|---|---|
| **⓪ Bias Remover** | Strips all PII from the raw PDF | Call 1 | Anonymised plain-text resume |
| **① Analyst** | Evaluates fit against the JD | Call 2 (combined) | Summary · Strengths · Gaps · Match Score /10 |
| **② Scorer** | Extracts & rates 20–25 traits | Call 2 (combined) | Trait scores → Overall score /100 |
| **③ Interviewer** | Generates targeted questions | Call 2 (combined) | 12 questions across 4 categories |

Agents 1, 2, and 3 run as a **single combined prompt** — the UI shows them completing asynchronously for clarity.

---

### What Gets Redacted by Agent 0

| Field | Replacement |
|---|---|
| Full name | `CANDIDATE` |
| Phone number | `[REDACTED-PHONE]` |
| Email address | `[REDACTED-EMAIL]` |
| Address / city / country | `[REDACTED-LOCATION]` |
| Nationality / visa status | `[REDACTED-NATIONALITY]` |
| Date of birth / age | `[REDACTED-AGE]` |
| Gender pronouns | `they / their` |
| Social profile URLs | `[REDACTED-PROFILE]` |
| University names | `UNIVERSITY-A`, `UNIVERSITY-B`… |
| Company names | **kept** — needed for skills context |

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

Or just place `app.py`, `requirements.txt`, and `.env` in a folder.

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

Add your Gemini API key:

```
GEMINI_API_KEY=AIzaSy...your_key_here
```

> The app reads this automatically via `python-dotenv`. No need to paste the key into the UI.

---

### 5. Run the app

```bash
streamlit run app.py
```

Opens in your browser at `http://localhost:8501`.

---

## How to Use

1. **Paste** the full job description into the left text box
2. **Upload** the candidate's resume as a PDF
3. **Select** a Gemini model from the sidebar
4. **Click** the Run button
5. Watch the 4-step pipeline progress in real time:
   - Agent 0 finishes first (bias removal is confirmed before anything else runs)
   - Agents 1, 2, 3 appear to run in parallel, completing with staggered UI updates
6. Review results:
   - 🛡 Blind Review banner showing exactly which fields were redacted
   - Overall score ring + candidate summary
   - Strengths (left column) and Gaps (middle column)
   - Trait breakdown bars with hover notes (right column)
   - Interview questions grouped by category below each column
   - Raw output expanders at the bottom for debugging

---

## Project Structure

```
recruitiq/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Your API key (never commit this)
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

## How the 2-Call Architecture Works

```
User clicks Run
│
├── API Call 1 ── Agent 0 (Bias Remover)
│                 Reads raw PDF → returns anonymised plain text
│                 UI: pipeline shows ⓪ running → ✓ done
│
└── API Call 2 ── Combined prompt with 3 delimited sections
                  ===AGENT1_START=== ... ===AGENT1_END===
                  ===AGENT2_START=== ... ===AGENT2_END===
                  ===AGENT3_START=== ... ===AGENT3_END===
                  
                  Response is split by regex into a1r, a2r, a3r
                  UI fakes staggered completion with time.sleep delays
```

---

## Notes

- The PDF is sent **inline** to Gemini — nothing is stored anywhere
- If Agent 2 or 3 returns malformed JSON, the raw output is shown in the expander at the bottom for debugging
- `gemini-3-pro-preview` gives the most thorough results; `gemini-3-flash-preview` is faster and cheaper
- University names are anonymised but company names are kept — company prestige is a valid signal, university name is not

---

## .gitignore Recommendation

```
.env
venv/
__pycache__/
*.pyc
```

---

## License

MIT — free to use, modify, and distribute.
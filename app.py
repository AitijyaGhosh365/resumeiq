import streamlit as st
import google.generativeai as genai
import base64, re, json, time
import os
from dotenv import load_dotenv
import random

load_dotenv()

st.set_page_config(page_title="RecruitIQ", page_icon="◈", layout="wide")
api_key = os.getenv("GEMINI_API_KEY")

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:      #05050a;
    --bg1:     #0d0d16;
    --bg2:     #111120;
    --border:  #1e1e36;
    --border2: #2a2a4a;
    --text:    #e2e2f0;
    --muted:   #5a5a7a;
    --a1:      #7c6eff;
    --a2:      #00d4aa;
    --a3:      #ff6b6b;
    --amber:   #ffb830;
    --blue:    #4da6ff;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background: var(--bg) !important; color: var(--text); }
.stApp { background: var(--bg) !important; }
header[data-testid="stHeader"] { background: transparent !important; border: none; }
.block-container { padding-top: 1rem !important; max-width: 1440px; }
#MainMenu, footer { visibility: hidden; }

/* NAVBAR */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem;
}
.logo { font-size: 1.35rem; font-weight: 700; letter-spacing: -.5px; display: flex; align-items: center; gap: .5rem; }
.logo-dot { color: var(--a1); }
.logo-tag {
    font-family: 'JetBrains Mono', monospace; font-size: .62rem; color: var(--muted);
    background: var(--bg2); border: 1px solid var(--border2); padding: .2rem .5rem;
    border-radius: 4px; letter-spacing: 1px;
}
.nav-pills { display: flex; gap: .4rem; }
.nav-pill {
    font-family: 'JetBrains Mono', monospace; font-size: .65rem;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: .28rem .65rem; border-radius: 4px;
    background: var(--bg2); border: 1px solid var(--border2); color: var(--muted);
}

/* LABEL */
.input-label {
    font-family: 'JetBrains Mono', monospace; font-size: .65rem;
    letter-spacing: 2px; text-transform: uppercase; color: var(--muted);
    margin-bottom: .5rem; display: block;
}

/* INPUTS */
.stTextArea textarea {
    background: var(--bg1) !important; border: 1px solid var(--border2) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: .82rem !important; line-height: 1.6 !important;
}
.stTextArea textarea:focus { border-color: var(--a1) !important; box-shadow: 0 0 0 3px rgba(124,110,255,.12) !important; }
.stFileUploader > div { background: var(--bg1) !important; border: 1px dashed var(--border2) !important; border-radius: 8px !important; }
div[data-testid="stTextInput"] input {
    background: var(--bg1) !important; border: 1px solid var(--border2) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: .85rem !important;
}

/* BUTTON */
.stButton > button {
    width: 100% !important; background: var(--a1) !important; color: #fff !important;
    border: none !important; border-radius: 8px !important; padding: .85rem 2rem !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    font-size: 1rem !important; letter-spacing: .3px !important; transition: all .2s !important;
}
.stButton > button:hover {
    background: #9488ff !important; transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(124,110,255,.35) !important;
}

/* PIPELINE */
.pipeline { display: flex; gap: .5rem; margin: 1rem 0 1.5rem; flex-wrap: wrap; align-items: center; }
.pipe-step {
    font-family: 'JetBrains Mono', monospace; font-size: .72rem;
    padding: .4rem .85rem; border-radius: 6px; display: flex; align-items: center;
    gap: .4rem; border: 1px solid var(--border2);
}
.pipe-wait { background: var(--bg2); color: var(--muted); }
.pipe-run  { background: #1a1a3a; color: var(--blue); border-color: #2a3a6a; animation: pulse 1.5s infinite; }
.pipe-done { background: #0a2520; color: var(--a2); border-color: #1a4a3a; }
.pipe-arrow { color: var(--muted); font-size: .8rem; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.55} }

/* BIAS BADGE */
.bias-banner {
    display: flex; align-items: flex-start; gap: 1rem;
    background: #0d1a2a; border: 1px solid #1e3a5a;
    border-left: 4px solid var(--blue);
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.25rem; margin-bottom: 1rem;
}
.bias-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: .1rem; }
.bias-title { font-size: .78rem; font-weight: 600; color: var(--blue); letter-spacing: .3px; margin-bottom: .3rem; }
.bias-body  { font-size: .82rem; color: #a0b8d0; line-height: 1.6; font-family: 'JetBrains Mono', monospace; }
.redacted-tag {
    display: inline-block; font-family: 'JetBrains Mono', monospace;
    font-size: .65rem; background: #1e3a5a; color: var(--blue);
    border: 1px solid #2a5a8a; border-radius: 3px;
    padding: .1rem .4rem; margin: .15rem .2rem;
}

/* SECTION HEADER */
.sec-header {
    display: flex; align-items: center; gap: .75rem;
    margin-bottom: 1.25rem; padding-bottom: .75rem; border-bottom: 1px solid var(--border);
}
.sec-num {
    font-family: 'JetBrains Mono', monospace; font-size: .62rem; font-weight: 500;
    background: var(--bg2); border: 1px solid var(--border2); color: var(--muted);
    padding: .2rem .45rem; border-radius: 4px;
}
.sec-title { font-size: .98rem; font-weight: 600; }
.c1 { color: var(--a1); } .c2 { color: var(--a2); } .c3 { color: var(--a3); } .ca { color: var(--amber); } .cb { color: var(--blue); }

/* SCORE BLOCK */
.score-block {
    display: flex; align-items: center; gap: 1.25rem;
    background: var(--bg1); border: 1px solid var(--border2);
    border-radius: 12px; padding: 1.1rem 1.4rem; margin-bottom: .8rem;
}
.score-ring {
    width: 76px; height: 76px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    background: conic-gradient(var(--ring-col) var(--ring-pct), var(--bg2) 0);
}
.score-inner {
    width: 56px; height: 56px; border-radius: 50%; background: var(--bg1);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 700;
}
.score-meta .score-label { font-size: 1rem; font-weight: 600; margin-bottom: .2rem; }
.score-meta .score-sub { font-size: .8rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; }

/* TRAIT BAR */
.traits-wrap { display: flex; flex-direction: column; }
.trait-row {
    display: grid; grid-template-columns: 148px 1fr 38px;
    align-items: center; gap: .65rem;
    padding: .5rem 0; border-bottom: 1px solid var(--border);
}
.trait-row:last-child { border-bottom: none; }
.trait-name { font-size: .8rem; color: var(--text); line-height: 1.25; }
.trait-bar-bg { height: 5px; background: var(--bg2); border-radius: 3px; overflow: hidden; }
.trait-bar    { height: 100%; border-radius: 3px; }
.bar-h { background: linear-gradient(90deg,#00d4aa,#00ffcc); }
.bar-m { background: linear-gradient(90deg,#ffb830,#ffda85); }
.bar-l { background: linear-gradient(90deg,#ff6b6b,#ff9999); }
.tscore { font-family:'JetBrains Mono',monospace; font-size:.75rem; text-align:right; }
.ts-h{color:var(--a2)} .ts-m{color:var(--amber)} .ts-l{color:var(--a3)}

/* SW CARDS */
.sw-card { border-radius: 9px; padding: .65rem .95rem; margin: .35rem 0; font-size: .85rem; line-height: 1.5; display: flex; gap: .55rem; align-items: flex-start; }
.sw-s { background: #061a12; border: 1px solid #0d3020; color: #7dffd0; }
.sw-w { background: #1a0606; border: 1px solid #3a0e0e; color: #ffaaaa; }
.sw-icon { flex-shrink: 0; font-size: .8rem; margin-top: .15rem; }

/* Q CARDS */
.q-tag {
    font-family:'JetBrains Mono',monospace; font-size:.6rem; letter-spacing:1.5px;
    text-transform:uppercase; padding:.15rem .45rem; border-radius:3px;
    display:inline-block; margin:.6rem 0 .3rem;
}
.qt-tech{background:#1a2a4a;color:var(--blue)} .qt-beh{background:#2a1a3a;color:#c084fc}
.qt-scen{background:#0f2520;color:var(--a2)} .qt-wild{background:#2a2010;color:var(--amber)}
.q-card {
    background: var(--bg1); border: 1px solid var(--border2); border-left: 3px solid var(--a1);
    border-radius: 0 9px 9px 0; padding: .75rem 1rem; margin: .35rem 0;
    font-size: .85rem; line-height: 1.6; color: #c8c8e8;
}

/* SUMMARY */
.summary-box {
    background: var(--bg1); border: 1px solid var(--border2); border-radius: 12px;
    padding: 1.1rem 1.4rem; font-size: .9rem; line-height: 1.75; color: #cccce8; margin-bottom: .8rem;
}
.match-box {
    background: var(--bg1); border: 1px solid var(--border2); border-left: 3px solid var(--a2);
    border-radius: 0 10px 10px 0; padding: .75rem 1rem;
    font-size: .85rem; color: #a0f8e8; font-family: 'JetBrains Mono', monospace;
}

/* DIVIDER */
.fancy-div { display:flex;align-items:center;gap:1rem;margin:1.5rem 0; }
.fd-l{flex:1;height:1px;background:var(--border)} .fd-d{width:4px;height:4px;border-radius:50%;background:var(--a1)}

/* MISC */
section[data-testid="stSidebar"] { background: var(--bg1) !important; border-right: 1px solid var(--border) !important; }
.stSelectbox > div > div { background: var(--bg2) !important; border-color: var(--border2) !important; color: var(--text) !important; }
.stAlert { border-radius: 8px !important; }
hr { border-color: var(--border) !important; }
.stExpander { background: var(--bg1) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="logo">
    <span class="logo-dot">◈</span>&nbsp;RecruitIQ
    <span class="logo-tag">v3 · 4-AGENT PIPELINE</span>
  </div>
  <div class="nav-pills">
    <span class="nav-pill">Bias Removal</span>
    <span class="nav-pill">Resume Analysis</span>
    <span class="nav-pill">Trait Scoring</span>
    <span class="nav-pill">Interview Prep</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="input-label">⚙ config</span>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a5a7a;margin:.3rem 0 .9rem">Free key → <a href="https://aistudio.google.com/apikey" target="_blank" style="color:#7c6eff">aistudio.google.com</a></div>', unsafe_allow_html=True)
    model_choice = st.selectbox("Model", [
        "gemini-3-flash-preview",
        "gemini-3-pro-preview",
    ])
    st.markdown("---")
    st.markdown("""<div style="font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a5a7a;line-height:2.1">
<span style="color:#9a9ab0;letter-spacing:1px">PIPELINE</span><br>
<span style="color:#4da6ff">⓪ Bias Remover</span> — strips PII from CV<br>
<span style="color:#7c6eff">① Analyst</span> — summary, strengths, gaps<br>
<span style="color:#00d4aa">② Scorer</span> — 20–25 traits · /100 score<br>
<span style="color:#ffb830">③ Interviewer</span> — 12 tailored questions
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-family:JetBrains Mono,monospace;font-size:.65rem;color:#5a5a7a;line-height:1.8">
<span style="color:#9a9ab0">WHAT GETS REDACTED</span><br>
Full name · Phone · Email<br>
Address · Nationality · Age<br>
Gender · Photo refs · Religion<br>
Marital status · Social profiles<br>
University names → anonymised<br>
Company names → kept (skills context)
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# INPUTS
# ─────────────────────────────────────────────────────────────────────────────
cl, cr = st.columns([1.1, 0.9], gap="large")
with cl:
    st.markdown('<span class="input-label">◫ job description</span>', unsafe_allow_html=True)
    job_desc = st.text_area("jd", height=250,
        placeholder="Paste the full job description — role, requirements, responsibilities, tech stack…",
        label_visibility="collapsed")
with cr:
    st.markdown('<span class="input-label">◧ resume / cv  (PDF)</span>', unsafe_allow_html=True)
    resume_file = st.file_uploader("cv", type=["pdf"], label_visibility="collapsed")
    if resume_file:
        st.success(f"✓  {resume_file.name}  ·  {resume_file.size // 1024} KB")

st.markdown("")
run_btn = st.button("◈  Run 4-Agent Pipeline — Debias · Analyze · Score · Prepare")

# ─────────────────────────────────────────────────────────────────────────────
# AGENT HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def pdf_part(b):
    return {"inline_data": {"mime_type": "application/pdf", "data": base64.b64encode(b).decode()}}

def call_pdf(m, pdf_bytes, prompt):
    """Call Gemini with a PDF attachment."""
    return m.generate_content([pdf_part(pdf_bytes), prompt]).text

def call_text(m, text, prompt):
    """Call Gemini with plain text context + prompt. If text is empty, just send prompt."""
    content = f"{text}\n\n{prompt}" if text.strip() else prompt
    return m.generate_content(content).text

def parse_md(text, headers):
    out = {}
    for h in headers:
        m = re.search(rf"##\s*{re.escape(h)}\s*\n(.*?)(?=##|\Z)", text, re.DOTALL | re.IGNORECASE)
        out[h] = m.group(1).strip() if m else ""
    return out

def safe_json(text):
    text = re.sub(r"^```[a-z]*\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text)
    return json.loads(text)

def cls(s, mx=10):
    p = s / mx
    return "h" if p >= .7 else ("m" if p >= .4 else "l")

def col(c): return {"h": "#00d4aa", "m": "#ffb830", "l": "#ff6b6b"}[c]

# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    for check, msg in [(not job_desc.strip(), "Paste a job description."),
                       (not resume_file, "Upload a PDF resume.")]:
        if check:
            st.error(msg); st.stop()

    st.markdown("---")
    p1, p2 = st.empty(), st.empty()

    def pipeline_html(s0, s1, s2, s3):
        def step(state, label):
            cls = {"done": "pipe-done", "run": "pipe-run", "wait": "pipe-wait"}[state]
            icon = {"done": "✓", "run": "⚙", "wait": "◌"}[state]
            return f'<div class="pipe-step {cls}">{icon} {label}</div>'
        return f"""<div class="pipeline">
            {step(s0, "⓪ Bias Remover")}
            <div class="pipe-arrow">→</div>
            {step(s1, "Agent 1 · Analyst")}
            <div class="pipe-arrow">→</div>
            {step(s2, "Agent 2 · Scorer")}
            <div class="pipe-arrow">→</div>
            {step(s3, "Agent 3 · Interviewer")}
        </div>"""

    def status(msg, color="#5a5a7a"):
        return f'<div style="font-family:JetBrains Mono,monospace;font-size:.72rem;color:{color}">{msg}</div>'

    try:
        pdf_bytes = resume_file.read()

        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(model_choice)

        # ── API CALL 1: AGENT 0 — Bias Remover ───────────────────────────────
        p1.markdown(pipeline_html("run","wait","wait","wait"), unsafe_allow_html=True)
        p2.markdown(status("⓪ Bias Remover — reading PDF and stripping identity signals…"), unsafe_allow_html=True)

        a0r = call_pdf(m, pdf_bytes, """You are a blind-review compliance officer.
Your job is to extract all professional content from this resume PDF and return it
as clean plain text — but with every identity signal removed or anonymised.

REMOVE / REPLACE the following:
- Full name → replace with "CANDIDATE"
- Phone numbers → [REDACTED-PHONE]
- Email addresses → [REDACTED-EMAIL]
- Home address, city, country of residence → [REDACTED-LOCATION]
- Nationality, citizenship, visa status → [REDACTED-NATIONALITY]
- Date of birth, age → [REDACTED-AGE]
- Gender pronouns (he/she/his/her in personal statements) → they/their
- Profile photos or references to appearance → remove entirely
- Religion, political affiliations → [REDACTED]
- Marital / family status → [REDACTED]
- Personal social media (LinkedIn URL, GitHub URL with real username) → [REDACTED-PROFILE]
- University / college names → replace with "UNIVERSITY-A", "UNIVERSITY-B" etc. in order of appearance
- Do NOT remove: job titles, company names, skills, tools, years of experience,
  project descriptions, certifications, GPA/grades, languages spoken (professional context only)

Return ONLY the cleaned resume text. No commentary, no preamble, no explanations.
Preserve all section headings and structure from the original.""")

        redaction_map = {
            "CANDIDATE": "Name", "REDACTED-PHONE": "Phone", "REDACTED-EMAIL": "Email",
            "REDACTED-LOCATION": "Address/Location", "REDACTED-NATIONALITY": "Nationality",
            "REDACTED-AGE": "Age/DOB", "REDACTED-PROFILE": "Social Profiles",
            "UNIVERSITY-A": "University Names",
        }
        redacted_items = [label for tag, label in redaction_map.items() if tag in a0r]

        # Agent 0 done — show it, then fake-launch agents 1-2-3 "simultaneously"
        p1.markdown(pipeline_html("done","wait","wait","wait"), unsafe_allow_html=True)
        p2.markdown(status(f"✓ Bias Remover done — {len(redacted_items)} field type(s) redacted. Dispatching agents 1, 2, 3…", "#4da6ff"), unsafe_allow_html=True)
        time.sleep(0.8)

        # Fake: all three fire at once
        p1.markdown(pipeline_html("done","run","run","run"), unsafe_allow_html=True)
        p2.markdown(status("① ② ③ — Analyst · Scorer · Interviewer running in parallel…"), unsafe_allow_html=True)

        # ── API CALL 2: Agents 1+2+3 in a single prompt ───────────────────────
        combined_prompt = f"""You are a hiring intelligence system running three parallel agents.
Below is a debiased resume (all PII removed) and a job description.
Return ALL THREE outputs in a single response, separated by the exact delimiters shown.

DEBIASED RESUME:
{a0r}

JOB DESCRIPTION:
{job_desc}

===AGENT1_START===
You are an expert technical recruiter. Output EXACTLY:

## SUMMARY
3-4 sentences about the candidate's fit.

## STRENGTHS
- specific strength 1
- specific strength 2
- specific strength 3
- specific strength 4
- specific strength 5

## WEAKNESSES / GAPS
- specific gap 1
- specific gap 2
- specific gap 3
- specific gap 4

## MATCH SCORE
X/10 — one sentence reason.
===AGENT1_END===

===AGENT2_START===
You are a precise hiring assessor. Return ONLY valid JSON (no markdown fences):
{{
  "total_score": 74,
  "max_possible": 250,
  "traits": [
    {{"name": "Python", "score": 9, "max": 10, "note": "5 yrs, FastAPI, Django"}},
    {{"name": "System Design", "score": 7, "max": 10, "note": "microservices mentioned"}}
  ]
}}
Include 20-25 traits. total_score = sum of scores. max_possible = traits * 10.
===AGENT2_END===

===AGENT3_START===
You are a senior hiring manager. Return ONLY valid JSON (no markdown fences):
{{
  "technical": [
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}}
  ],
  "behavioral": [
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}}
  ],
  "scenario": [
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}},
    {{"q": "...", "why": "..."}}
  ],
  "wildcard": [
    {{"q": "...", "why": "..."}}
  ]
}}
Exactly 12 questions, specific to this candidate and role.
===AGENT3_END==="""

        combined_raw = call_text(m, "", combined_prompt)

        # Parse out each agent's section
        def extract_block(text, tag):
            m = re.search(rf"==={tag}_START===(.*?)==={tag}_END===", text, re.DOTALL)
            return m.group(1).strip() if m else ""

        a1r = extract_block(combined_raw, "AGENT1")
        a2r = extract_block(combined_raw, "AGENT2")
        a3r = extract_block(combined_raw, "AGENT3")

        # Fake staggered completion: agents finish one by one with short delays
        time.sleep(random.random())
        p1.markdown(pipeline_html("done","done","run","run"), unsafe_allow_html=True)
        p2.markdown(status("✓ Agent 1 · Analyst done — waiting on Scorer & Interviewer…", "#7c6eff"), unsafe_allow_html=True)

        time.sleep(random.random())
        p1.markdown(pipeline_html("done","done","done","run"), unsafe_allow_html=True)
        p2.markdown(status("✓ Agent 2 · Scorer done — waiting on Interviewer…", "#00d4aa"), unsafe_allow_html=True)

        time.sleep(random.random())
        p1.markdown(pipeline_html("done","done","done","done"), unsafe_allow_html=True)
        p2.markdown(status("✓ All 4 agents complete — rendering results", "#00d4aa"), unsafe_allow_html=True)
        time.sleep(0.5)

        # ── BIAS REMOVAL BANNER ───────────────────────────────────────────────
        st.markdown('<div class="fancy-div"><div class="fd-l"></div><div class="fd-d"></div><div class="fd-l"></div></div>', unsafe_allow_html=True)

        tags_html = "".join(f'<span class="redacted-tag">✕ {item}</span>' for item in redacted_items) if redacted_items else '<span class="redacted-tag">None detected</span>'
        st.markdown(f"""<div class="bias-banner">
          <div class="bias-icon">🛡</div>
          <div>
            <div class="bias-title">⓪ BIAS REMOVER — Blind Review Active</div>
            <div class="bias-body">
              The following identity signals were detected and removed before any evaluation agent saw the resume.
              All downstream analysis is based purely on skills, experience, and qualifications.<br><br>
              <strong style="color:#6ab0d0">Redacted fields:</strong> {tags_html}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Parse results
        a1 = parse_md(a1r, ["SUMMARY", "STRENGTHS", "WEAKNESSES / GAPS", "MATCH SCORE"])
        try: a2 = safe_json(a2r)
        except: a2 = None
        try: a3 = safe_json(a3r)
        except: a3 = None

        st.markdown('<div class="fancy-div"><div class="fd-l"></div><div class="fd-d"></div><div class="fd-l"></div></div>', unsafe_allow_html=True)

        # ── ROW 1: Overall Score + Summary ────────────────────────────────────
        r1l, r1r = st.columns([1, 1.5], gap="large")

        with r1l:
            st.markdown('<div class="sec-header"><span class="sec-num">01</span><span class="sec-title c2">Overall Score</span></div>', unsafe_allow_html=True)
            if a2:
                ts = a2.get("total_score", 0)
                mp = a2.get("max_possible", 250)
                pct_100 = round((ts / mp) * 100) if mp else 0
                c = cls(pct_100, 100)
                ring_col = col(c)
                pct_deg = f"{pct_100 * 3.6}deg"
                label = {"h": "Strong Match", "m": "Partial Match", "l": "Weak Match"}[c]
                tc = len(a2.get("traits", []))
                st.markdown(f"""<div class="score-block">
                  <div class="score-ring" style="--ring-col:{ring_col};--ring-pct:{pct_deg}">
                    <div class="score-inner" style="color:{ring_col}">{pct_100}</div>
                  </div>
                  <div class="score-meta">
                    <div class="score-label" style="color:{ring_col}">{label}</div>
                    <div class="score-sub">{ts}/{mp} raw · {tc} traits · blind review</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            match_t = a1.get("MATCH SCORE", "")
            if match_t:
                st.markdown(f'<div class="match-box">{match_t}</div>', unsafe_allow_html=True)

        with r1r:
            st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title c1">Candidate Summary</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-box">{a1.get("SUMMARY", "")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="fancy-div"><div class="fd-l"></div><div class="fd-d"></div><div class="fd-l"></div></div>', unsafe_allow_html=True)

        # ── ROW 2: Strengths | Weaknesses | Trait Bars ────────────────────────
        r2l, r2m, r2r = st.columns([1, 1, 1.5], gap="large")

        with r2l:
            st.markdown('<div class="sec-header"><span class="sec-num">03</span><span class="sec-title c2">Strengths</span></div>', unsafe_allow_html=True)
            for line in a1.get("STRENGTHS", "").split("\n"):
                line = line.strip().lstrip("-•* ").strip()
                if line:
                    st.markdown(f'<div class="sw-card sw-s"><span class="sw-icon">↑</span>{line}</div>', unsafe_allow_html=True)

            st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-header"><span class="sec-num">05</span><span class="sec-title ca">Interview Questions</span></div>', unsafe_allow_html=True)
            if a3:
                st.markdown('<div class="q-tag qt-tech">Technical</div>', unsafe_allow_html=True)
                for item in a3.get("technical", []):
                    st.markdown(f'<div class="q-card">{item["q"]}</div>', unsafe_allow_html=True)

        with r2m:
            st.markdown('<div class="sec-header"><span class="sec-num">04</span><span class="sec-title c3">Gaps &amp; Weaknesses</span></div>', unsafe_allow_html=True)
            for line in a1.get("WEAKNESSES / GAPS", "").split("\n"):
                line = line.strip().lstrip("-•* ").strip()
                if line:
                    st.markdown(f'<div class="sw-card sw-w"><span class="sw-icon">↓</span>{line}</div>', unsafe_allow_html=True)

            st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
            st.markdown('<div style="height:2.4rem"></div>', unsafe_allow_html=True)
            if a3:
                st.markdown('<div class="q-tag qt-beh">Behavioral</div>', unsafe_allow_html=True)
                for item in a3.get("behavioral", []):
                    st.markdown(f'<div class="q-card">{item["q"]}</div>', unsafe_allow_html=True)
                st.markdown('<div class="q-tag qt-scen">Scenario</div>', unsafe_allow_html=True)
                for item in a3.get("scenario", []):
                    st.markdown(f'<div class="q-card">{item["q"]}</div>', unsafe_allow_html=True)
                st.markdown('<div class="q-tag qt-wild">Wildcard</div>', unsafe_allow_html=True)
                for item in a3.get("wildcard", []):
                    st.markdown(f'<div class="q-card">{item["q"]}</div>', unsafe_allow_html=True)

        with r2r:
            st.markdown('<div class="sec-header"><span class="sec-num">06</span><span class="sec-title c2">Trait Breakdown</span></div>', unsafe_allow_html=True)
            if a2 and a2.get("traits"):
                st.markdown('<div class="traits-wrap">', unsafe_allow_html=True)
                for t in a2["traits"]:
                    n   = t.get("name", "")
                    s   = t.get("score", 0)
                    mx  = t.get("max", 10)
                    nt  = t.get("note", "")
                    c   = cls(s, mx)
                    pct = round((s / mx) * 100)
                    st.markdown(f"""<div class="trait-row" title="{nt}">
                      <div class="trait-name">{n}</div>
                      <div class="trait-bar-bg"><div class="trait-bar bar-{c}" style="width:{pct}%"></div></div>
                      <div class="tscore ts-{c}">{s}/{mx}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.code(a2r[:600] if a2r else "No trait data returned")

        # ── RAW OUTPUTS ───────────────────────────────────────────────────────
        st.markdown("---")
        e0, e1, e2, e3 = st.columns(4)
        with e0:
            with st.expander("Raw · Agent 0 · Debiased CV"):
                st.text(a0r)
        with e1:
            with st.expander("Raw · Agent 1 · Analysis"):
                st.text(a1r)
        with e2:
            with st.expander("Raw · Agent 2 · Scores"):
                st.text(a2r)
        with e3:
            with st.expander("Raw · Agent 3 · Questions"):
                st.text(a3r)

    except Exception as e:
        p1.empty(); p2.empty()
        st.error(f"Error: {e}")
        st.info("Check your API key and that the PDF is a valid resume.")
# Interaction Flow — 7-Step Guided Conversation

This document defines the exact conversation script for Agents using the
University Course Planner skill. Follow each step in order. Ask one question
at a time. Do not proceed to the next step until the current one is answered.

---

## Step 1 — University Name

**Prompt:** "What university are you studying at? Please give me the full name."

**Why:** The university name is used to search for the course catalog, credit
system, and academic calendar online.

**Example answer:** "University of Melbourne"

If the student is undecided, ask for 2-3 candidates and pick one.

---

## Step 2 — Country / Education System

**Prompt:** "Which country or credit system does your university use? Pick one:
US Credits, ECTS, Australian Credit Points, UK Credits (CATS), Canadian Credits,
Singapore Modular Credits, Hong Kong Credits, Chinese Credits, or Other."

**Why:** Different countries use different credit frameworks. This affects how
we calculate total credits and compare against degree requirements.

**Example answer:** "Australian Credit Points"

If the student doesn't know, infer from the university's country.

---

## Step 3 — Major / Field of Study

**Prompt:** "What is your major or field of study?"

**Why:** To filter relevant courses from the catalog and match prerequisite
chains.

**Example answer:** "Computer Science"

---

## Step 4 — Year Level

**Prompt:** "What year of study are you in? Year 1, Year 2, Year 3, Year 4,
or Master?"

**Why:** Determines course difficulty level and which prerequisites are
likely already met.

**Example answer:** "Year 1"

---

## Step 5 — Planning Mode

**Prompt:** "Do you want me to recommend courses for you (AI recommend), or have
you already chosen your courses and just need scheduling (user decided)?"

**Why:** Determines whether the AI selects courses or validates the student's
choices.

**Example answer:** "AI recommend"

### Step 5a (if AI recommend) — Goals & Schedule Preferences

**Prompt:** "What are your academic goals and schedule preferences? For example:
GPA-focused, employment-focused, interest-driven, grad-school prep, or easy
load. For schedule: no 8am classes, three-day concentrated, evenly distributed,
etc."

**Example answer:** "Goals: GPA. Preferences: no 8am, lunch break 12-1pm,
evenly distributed across the week."

### Step 5b (if user decided) — Chosen Courses

**Prompt:** "List the course codes you have chosen, in JSON array format.
Example: [\"MATH101\", \"COMPSCI230\", \"PHYS150\"]"

---

## Step 6 — Semester Information

**Prompt:** "What semester are you planning for? Please provide the semester
code, start date, end date, and number of teaching weeks. Example: 2026-S1,
starts 2026-02-24, ends 2026-06-05, 12 teaching weeks."

**Why:** Used to expand the weekly schedule to cover the full semester with
correct dates.

**Example answer:** "2026-S1, starts 2026-02-24, ends 2026-06-05, 12 teaching weeks"

---

## Step 7 — Generate Workbook

After collecting all inputs, choose the execution route by the request itself — NOT by whether the CLI is installed. Follow the authoritative routing in `SKILL.md: "Execution routing rules"`. Decision rule:

1. **Batch / multi-school / institutional / decision-report needs → Cloud Standard Mode.**
   - Run the fixed multi-step cloud pipeline (catalog → recommend → schedule → decision) matching SKILL.md's canonical pipeline; consume its JSON with `generate_excel.py`.
   - Then pass the combined JSON output to `scripts/generate_excel.py`.
   - Before submitting, get explicit confirmation: the service/endpoint, every data category transmitted, the cloud fee estimate, and reason cloud is needed (see SKILL.md "Cloud mode rules").

2. **Single school + single student + personal use → Local Personal Lightweight Mode.**
   - The Agent analyzes the course catalog using web search (declared in SKILL.md "Tool usage": public catalog research), generates recommendations based on the student's goals, creates a weekly schedule with conflict detection.
   - Save the combined JSON to a temp file, then run `scripts/generate_excel.py` on it.
   - CLI availability alone NEVER authorizes cloud submission.

3. **User explicitly chose Cloud, or batch/institutional → never downgrade to local.**
   - Fee / balance objections are handled by confirmation and top-up guidance, not by silently switching a cloud-bound request to local.

4. Validate the output:
   ```bash
   python3 scripts/validate_schedule.py <excel_file.xlsx>
   ```

5. Deliver the .xlsx file to the student.

---

## Optional: Course Catalog Upload

At any point during steps 1-6, if the student has a course catalog file (PDF,
text, or HTML), accept it and pass it as the `course_catalog` input field.
This significantly improves accuracy when the university's catalog is not
easily searchable online.

> **Privacy note (say this once when an upload is accepted):**
> Only upload materials you are authorized to share. Course catalogs may
> contain personal identifiers, student records, or license-restricted content —
> please strip/avoid such data before uploading. The catalog text is used to build
> your schedule; if you later choose Cloud mode, this text is sent to the selected
> cloud endpoint (see "Cloud consent" in SKILL.md). You may also paste only the
> relevant course excerpts instead of an entire file. Do not upload data you are
> not permitted to share.

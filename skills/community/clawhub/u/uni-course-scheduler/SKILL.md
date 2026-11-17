---
name: uni-course-scheduler
description: >-
  AI-powered university course planning assistant. Analyzes course catalogs,
  recommends courses based on student goals, generates optimized weekly
  schedules with enrollment priority markers, and exports Excel (local + cloud)
  and an ICS calendar (local via generate_ics.py, or cloud standard mode).
  Supports international education systems (US/AU/UK/ECTS/CN).
  Execution: CLOUD standard mode (fixed 4-step pipeline, standardized decision report;
  recommended & default route for batch/institutional needs — requires catalog text input,
  see references/catalog-collection.md). Two cloud platforms by payment method:
  Shengsuanyun (CNY ¥0.5/run, China payment) or CogFoundry (USD $0.10/run, international credit card).
  LOCAL personal lightweight version (free, single-school single-student only,
  no batch pipeline, no standardized decision report).
  Tool usage (declared): WebSearch/WebFetch to collect official course-catalog
  text; local Python scripts to generate/save Excel (.xlsx) and ICS (.ics) files
  on the user's machine; optional paid cloud runs via the LoomLoom CLI
  (`loomloom market quote/run`) after explicit user confirmation and fee disclosure.
version: 2.7.14
author: course-scheduler
license: MIT
agent_created: true
homepage: https://github.com/ez-hq/uni-course-scheduler
repository: https://github.com/ez-hq/uni-course-scheduler
issues: https://github.com/ez-hq/uni-course-scheduler/issues
permissions:
  tools: [WebSearch, WebFetch, python3]
  file_access: scripts + output paths only (Excel/ICS generation)
  network: public university catalog research (local mode); optional paid cloud via LoomLoom CLI (user-confirmed)
---

# University Course Planner

## When to use this skill (activation)
Use this skill when a student asks for help planning university courses, building
a weekly timetable, choosing courses toward a goal, or exporting an Excel/ICS
schedule. It is NOT a general education/advice chatbot — it stays within course
planning, scheduling, and export for a concrete university/program.

## Local file warning
This skill generates and saves local files (Excel `.xlsx` and calendar `.ics`) on
your machine from the course data it collects; review outputs before sharing.

Help university students plan courses, build weekly timetables, and export Excel (local + cloud) and ICS calendar files (local or cloud mode).

## Prerequisites

- Python 3.10+ with `openpyxl` and `icalendar` packages
- If missing, install pinned versions (reviewed, reproducible):
  `pip install "openpyxl>=3.1,<3.2" "icalendar>=5,<6" "pytz==2024.2"`
  Prefer a hash-locked `requirements.txt` + `pip install --require-hashes` for production use.

## Interaction Flow

Ask questions **one at a time**, in this exact order. Wait for each answer before proceeding.

### Step 1: University Name
Ask (in the user's language): "What is the name of your university?"
Note the university name for course catalog research.

### Step 2: Country / Education System
Ask (in the user's language): "Which country is your university in, and what education/credit system does it use?"
Common systems: US (credits), AU (UoC/credit points), UK (CATS), ECTS, CN (credits).
This determines credit calculation and semester structure.

### Step 3: Major / Field of Study
Ask (in the user's language): "What is your program / major?"
Use this to filter relevant courses from the catalog.

### Step 4: Year Level & Intake
Ask (in the user's language): "What year level are you in? When do you start?"
Examples: Year 1 Term 1 2027, Year 2 Semester 1, etc.
Also ask about special calendar systems (trimester, quarter, etc.).

**Year Level Enum Mapping (MANDATORY — map the user's academic context to the cloud `year_level` enum):**
The cloud pipeline only accepts these exact values for `year_level`. Always map what the user says to one of them:
- Undergraduate freshmen/sophomore/junior/senior → `"Year 1"` / `"Year 2"` / `"Year 3"` / `"Year 4"`
- Graduate Coursework (taught Master) → `"Master"`
- Exchange / Double-degree / Transfer / Part-time → base on their current year level in their home degree track (`"Year 1"`–`"Year 4"` for undergraduate-track, `"Master"` for postgraduate-track)
- Unknown / ambiguous → ask the user to clarify which year level they are in before proceeding
Never invent a free-text value like "Year 1 (Master)" or "Graduate Year 1" — it will fail cloud validation. Use exactly `"Year 1"`, `"Year 2"`, `"Year 3"`, `"Year 4"`, or `"Master"`.

### Step 5: Planning Mode
Ask (in the user's language): "How would you like me to help with course selection?"
- **A: AI recommend mode** — Agent researches courses, recommends, and schedules (recommended for freshmen)
- **B: User-decided mode** — User provides course list, Agent schedules only

If Mode A, also ask:
- Academic goals / direction preferences? (lab-focused / theory-focused / clinical, etc.)
- Schedule preferences? (no 8am classes / no evening classes / concentrate on certain days)
- Assessment preferences? (fewer group projects / more hands-on projects, etc.)
- How many credits per semester? (balanced / concentrated / light)

### Step 5.5: Execution Mode

**Ask the user FIRST which execution path they want — Local or Cloud. This is MANDATORY before any further planning.**

Ask (in the user's language): "How would you like me to run this — entirely locally (free, no install) or through the Cloud Standard Mode (paid, batch-capable)?"

- If the user chooses **Local** → proceed with Step 6 (Local Personal Lightweight Mode). No installation needed.
- If the user chooses **Cloud** → **you MUST first walk them through Cloud onboarding before any cloud run.** Do not skip this even if they seem ready.

**Cloud onboarding (MANDATORY — before the first cloud run, tell the user ALL of this):**

1. **Tell the user Cloud requires LoomLoom to be installed locally.** It is NOT installed automatically with this Skill.
2. Give them the install options:
   - **Option 1 — manual terminal command:**
     ```bash
     npm install -g @cogfoundry/loomloom
     ```
   - **Option 2 — let the agent install it for them.** Ask the user to say (or paste) the equivalent in their own language, e.g.: "Please install LoomLoom: run `npm install -g @cogfoundry/loomloom`, server: `https://loomloom.shengsuanyun.com/loom/v1`." The agent runs the install; the user then completes login themselves interactively (see below). For production, prefer pinning a reviewed release version + checksum (see `references/loomloom-setup.md`).
3. **After install, verify with one check:**
   ```bash
   loomloom doctor
   ```
4. **Then the user must have a LoomLoom account on the Shengsuanyun platform before anything can run:**
   - Cloud execution runs through the LoomLoom platform (Shengsuanyun). The user needs an account there; follow the platform's own account/sign-up flow (the agent does not need to manage this).
   - **The user logs in interactively with `loomloom login`** — the agent never sees or handles their credentials.
   - Cloud runs are paid (¥0.5/run); billing and balance follow the platform's own payment flow.
   - Only after install + login + account are confirmed may the agent proceed to `loomloom market quote/run`.

> If the user does not want to install LoomLoom or has no account/balance, offer the Local mode instead — never force Cloud.

**Batch / multi-school / decision report needed → use Cloud Standard Mode.**

Ask (in the user's language): "There are two execution modes. Choose the first one (Cloud Standard Mode) for batch / multi-school / standardized decision report needs."

- **Cloud Standard Mode (recommended · production-grade · ¥0.5/run)** — runs via the fixed LoomLoom market pipeline.
  - Production-grade: fixed 4-step pipeline (catalog analysis → course recommendation → scheduling → decision report). One submission can batch-process multiple schools/students (multi-row).
  - Outputs a standardized decision report (8-dimension scoring + course selection rationale + risk warnings + adjustment suggestions).
  - Data source: the cloud pipeline has NO web access, **the local Agent must first collect official catalog text online** (see `references/catalog-collection.md`), or the buyer pastes the official handbook text manually. Fuller catalog = more reliable output.
  - For: institutions / batch (>20 students) / standardized decision report needs / multiple schools at once.
  - Cost: ¥0.5/run (China · Shengsuanyun) or $0.10/run (international · CogFoundry) + platform model cost. Estimate shown before running; charged only after confirmation.
- **Payment method → cloud platform routing (MANDATORY — ask BEFORE the first cloud run, then remember)**:
  The same skill serves two cloud platforms. Decide which one a user uses by their
  payment method, NOT by IP or nationality:
  1. Ask the user once (first cloud run): "Is your payment method China mainland (Alipay/WeChat/UnionPay) or an international credit card (Visa/Mastercard)?"
     - China mainland payment → route to **Shengsuanyun**: server `https://loomloom.shengsuanyun.com/loom/v1`, token `LOOMLOOM_TOKEN_SHENGSUANYUN`, fixed fee ¥0.5/run.
     - International credit card → route to **CogFoundry**: server `https://loomloom.cogfoundry.ai/loom/v1`, token `LOOMLOOM_TOKEN_COGFOUNDRY`, fixed fee $0.10/run.
  2. Set the matching `LOOMLOOM_SERVER` (and use the matching token env var) for all subsequent cloud commands.
  3. Remember the choice for the session (do not re-ask every run; re-ask only if the user says their payment changed).
  4. The cloud commands themselves are identical (`loomloom market quote/run`); only the **server,
   token, and Listing ID** differ by platform:
   - Shengsuanyun Listing ID: `019fcadb-ec1c-737a-a986-b768851b020e`
   - CogFoundry Listing ID: `019ff00f-a628-7c8e-8aac-03efe909f99a`
   Never invent a Listing ID; use the one for the confirmed platform (see `references/loomloom-setup.md`).
  5. If the user is unsure which they can pay with, show both options and let them choose the one they can fund.
- **Local Personal Lightweight Mode (free · single-school single-student only)** — the current agent checks official course info online, verifies each item, then completes recommendation and scheduling.
  - Pros: free, data verified against official sources, consistent output format (6-sheet Excel + ICS)
  - Limits: one school at a time, single-student interactive refinement; **no batch pipeline or standardized decision report**; personal use only.

**Execution routing (capability-based, user-informed):**
Decide by what the user actually needs, then explain the choice and, where it involves a paid or external call, get explicit consent. Never silently pick a paid route, and never force Cloud on a user who can be served locally.

1. **Batch / multi-school / institutional / decision-report needs** — the Cloud Standard Mode is the fitting option (it batch-processes rows and produces the decision report). Recommend it, but still ask the user to confirm before any paid run.
2. **Single school + single student + personal use** — serve locally by default (free, no external submission). Only go Cloud if the user explicitly asks for batch / a decision report / cloud exclusives, and they confirm the fee.
3. **User explicitly chose Cloud** — respect it, and get fee + data-disclosure confirmation before the first Cloud run (see "Cloud consent" below).
4. **Cost too high** — explain options (top-up, batching, or local where a capable local pipeline suffices). Never bill someone silently or remove the local option they depend on.

**Cloud consent & data disclosure (mandatory, before the first Cloud submission per user):**
In the user's own language, before invoking any paid Cloud call, clearly state:
- the service/endpoint (Shengsuanyun or CogFoundry per payment method),
- which fields will be sent (university, program, catalog text, and any user-provided info),
- the fee estimate,
- that personal single-school planning can be approximated locally,
- and ask for explicit, separate confirmation that sending to that server is acceptable.
- Confirm per submission; renew if provider/endpoint/fields/terms change.

**Cloud mode rules (mandatory, when the user explicitly chooses it):**
1. **Collect the catalog FIRST, locally** — the cloud pipeline has NO web access.
   Before any cloud run, you MUST follow `references/catalog-collection.md`: use
   WebSearch / WebFetch to collect the university's official catalog text, pass the
   quality gate (≥500 chars, ≥5 real courses, 6-step search protocol below), and
   provide it as the `course_catalog` input. Never submit a cloud run with an
   empty/failed catalog — it produces placeholder output and wastes the user's money.
   If collection fails, ask the user to paste their official program-handbook text instead.

1a. **Pre-flight catalog validation (MANDATORY — before quote, before confirmation)**:
    After collecting the catalog but BEFORE running `loomloom market quote`, run this
    checklist and do NOT proceed until ALL items pass:

    ```
    [COURSE DATA]
    ✅ Course codes: every course has a unique code (e.g. BIOL1020); 100% coverage of target courses
    ✅ Credits: every course has a credit value; missing credits → cannot submit
    ✅ Offering semester: every course lists its offering (S1/S2/Summer, etc.)
    ✅ Term dates: semester_start + num_teaching_weeks present

    [TIMETABLE DATA — two sub-checks, both required]
    ✅ Timetable presence: TIMETABLE section exists, and every target course has at least 1 session slot
       (new courses like BIOM1001 may be exempt, marked TBC / to verify)
    ✅ Timetable completeness: total TIMETABLE entries ≥ 2 × target course count
       (typical science courses need 2-3 slots each: lecture + lab/practical/tutorial)
        If the completeness check FAILs: likely only lectures were given, missing labs/tutorials
    ```

    **How to check timetable data in the catalog**: the `course_catalog` text must contain
    lines like `BIOL1020 | Lecture | Monday | 10:00-11:00 | weeks 1-13` for each course.
    If the catalog has course codes, credits, and descriptions but NO timetable lines,
    the pre-flight validation FAILS.

    **Timetable data format (must be in the catalog text)**:
    ```
    TIMETABLE:
    BIOL1020 | Lecture | Monday | 10:00-11:00 | weeks 1-13
    BIOL1020 | Tutorial | Wednesday | 10:00-11:00 | weeks 1-13
    BIOL1020 | Practical | Friday | 09:00-12:00 | weeks 1-12
    CHEM1100 | Lecture | Monday | 14:00-15:00 | weeks 1-13
    CHEM1100 | Lab | Thursday | 13:00-16:00 | weeks 2,4,6,8,10,12
    ```
    Each line: `course_code | session_type | day | start_time-end_time | week_range`

    **If pre-flight validation fails:**
    - **Case A: no TIMETABLE section, or completeness check FAILs**:
      → **Step 1: check whether the timetable has been published**
         WebSearch `<university> timetable <semester_year>` (e.g. `UQ timetable 2027 semester 1`)
         If the 2027 timetable is not yet published (common: UQ publishes in Nov-Dec each year):
          → Tell the user: "The official 2027 timetable is not published yet (expected Nov-Dec 2026).
             I can fill in the catalog with typical prior-year timetable times first, so the Cloud-run timetable structure is complete
            (including labs/tutorials), but exact times must be verified on mySI-net once the official timetable is out.
            Do you want me to do that now? Or run Cloud first and fill in locally afterwards?"
         → If the user picks "use prior-year data": search for the same-period timetable from previous years
            (search `<course_code> <university> timetable 2026`) and fill TIMETABLE rows with historical data.
             and mark each row's notes with "2026 reference time — verify when the 2027 timetable is released".
         → If the user picks "run Cloud first": allow it, mark default_timetable=true, ensure post-processing fills in.
      → **Step 2: search for timetable data**
         (only when the 2027 timetable is already published)
         Use WebSearch/WebFetch to find timetable data
         (search `<course_code> <university> timetable 2027`), append TIMETABLE rows to
         the end of the catalog text. Re-run the precheck.
         → If search fails: "I couldn't find timetable data. I can fill in typical times from previous years, or run Cloud first — which do you prefer?"
      → **If the user says "never mind" (or search failed and the user refuses historical data)**:
        Warn explicitly: "OK, but note: without timetable data, Cloud will only output a default timetable of 1-2 sessions per course,
        labs/tutorials will not appear. I will fill in the timetable locally after the Cloud run."
        → If the user insists: allow it, but ensure post-processing (rule 7) fills in the timetable.
    - **Case B: invalid JSON format**:
      → Check whether catalog_text contains invalid JSON characters (non-printable chars, unescaped quotes, etc.)
      → If invalid: fix it before submitting. Never submit malformed JSON.

**After pre-flight passes, validate the submission JSON file:**
Before running `loomloom market quote --input-file <request.json>`:
    ```
    [SUBMISSION JSON VALIDATION]
    ✅ File exists: request.json exists and is readable
    ✅ Valid JSON syntax: python -c "import json; json.load(open('request.json'))"
    ✅ Required fields: university_name, education_system, major, year_level, planning_mode,
       student_goal, course_catalog, semester_info all present and non-empty
    ✅ chosen_courses handling: only fill the course-code array when the user has already decided (user_decided);
        otherwise OMIT the field — never write null (the platform rejects "field: null is not supported")
    ✅ Valid enum values: education_system is one of the listed enum values (Australian Credit Points, etc.)
    ✅ No oversized fields: every field value < 50000 chars (to avoid pipeline truncation)
    ✅ UTF-8 encoding: file is valid UTF-8, no BOM, no corrupted characters
    ```
    If any check fails: fix the JSON file and re-validate. Never submit a file that fails JSON validation.

    **Only proceed to `loomloom market quote` when ALL checks pass (pre-flight + JSON validation).**

1a2. **User confirmation loop (MANDATORY — before quote, before fee confirmation)**:
    After the catalog passes the quality gate and pre-flight validation, BEFORE
    running `loomloom market quote`, present the collection summary to the user
    and obtain explicit confirmation of the DATA (this is separate from fee
    confirmation in rule 3):
    - Show the user: course codes + names collected, source URLs used,
      quality-gate results (chars / course count / timetable coverage),
      and any NOT_FOUND / TBC items.
    - Ask (in the user's language): "The course catalog above is from official sources (links recorded). Submit to Cloud (¥0.5/run)?
      If anything is missing, tell me and I will add it before submitting."
    - If user confirms → proceed to quote + fee confirmation (rule 3).
    - If user reports missing/wrong courses → re-collect the specific courses,
      re-run the quality gate, show the updated summary, and ask again. Loop until
      the user confirms or abandons the cloud run.
    - If collection found nothing / gate failed → do NOT show a fake summary;
      tell the user honestly and ask them to paste their official handbook text.

2. Use the LoomLoom CLI buyer flow (`loomloom market` / `loomloom run`) to execute
   through the Listing. Never reconstruct the pipeline locally in cloud mode.
1b. **user_decided mode — agent fills the chosen-courses column (MANDATORY)**:
    When planning_mode = "user_decided" (the user has chosen their own courses):
    - The cloud pipeline needs to know WHICH courses the user chose (the
      chosen-courses column). Do NOT require the user to know this column exists.
    - Extract the chosen course codes from the user's request/conversation; if the
      user has not explicitly listed codes, ask (in the user's language): "Which courses have you decided on? Please give me the course codes."
    - Write the codes into the chosen-courses column before submitting to the cloud.
    - NEVER submit user_decided with an empty chosen-courses column — the cloud
      pipeline will mark it "partial" and return an empty result, wasting ¥0.5.
    - If the user cannot decide, suggest switching to ai_recommend mode instead.

1c. **Row count must equal student count (MANDATORY — before quote, before run)**:
    The downloaded workbook ships with **example rows** (typically "University of Melbourne"
    and "Tsinghua University"). **Delete every example row** before submitting, then confirm
    that the remaining data rows = the number of students you intend to run. The `taskCount`
    returned by the quote MUST equal that number; if it is higher, an example row is still
    present and you would pay for a run you do not need. Never submit a workbook whose row
    count you have not checked.

3. Before submitting any cloud run: show the platform's current fee estimate and
   obtain the user's **explicit confirmation in the current conversation**. No
   confirmation, no submission.
4. If the user has no LoomLoom token/balance, guide them through the platform's own account flow (`loomloom login`, or the platform's own sign-up/billing flow). All cloud submissions require an
   explicit human confirmation (fee + data disclosure) in the current conversation — the agent never auto-submits paid runs.
5. After the cloud run finishes: download the results, map them into this Skill's
   JSON input format (below), and continue with Step 7 to generate the Excel + ICS
   files locally. Per-row status must survive into the output (success/failed).
6. **Cloud output is structured data, not verified facts** — course codes, credits,
   and assessments come from the upstream catalog text you provided. Re-check
   anything critical against official sources before presenting it as verified.
7. **Post-processing: handle empty schedule locally (no re-submission needed)**:
   If the cloud run returns an empty schedule array with `missing_scheduling_data`,
   do NOT re-submit to the cloud (would cost another ¥0.5/row). Instead:
   a. Read `missing_scheduling_data.courses` and `missing_scheduling_data.needed_fields`
      to know exactly which courses lack which fields.
   b. Try local WebSearch/WebFetch to find the missing timetable data
      (search `<course_code> <university> timetable 2026`).
   c. If found: add the meeting times to the local data and generate the schedule
      using `scripts/generate_excel.py` directly (no cloud re-run).
   d. If NOT found after reasonable effort: generate a reasonable default timetable
      (assign each course a lecture slot and tutorial slot based on typical patterns),
      and mark it with `"default_timetable": true` + a note
      "This timetable uses reasonable defaults — verify with the university timetable system."
   e. The cloud run's catalog/recommend/decision outputs are still valid and usable —
      only the schedule step needs local fallback.

7a. **Anti-hallucination check (MANDATORY — on EVERY cloud output step, before mapping
    into Excel/ICS)**:
    Cloud models can fabricate data in free-text fields (e.g. decision-report
    `why_rejected` invented non-existent course codes MATH1001/PHYS1100/COMP1000
    in a verified 2026-08 UQ run). Run the bundled detector on EVERY step output
    (stp_catalog / stp_recommend / stp_schedule / stp_decision) before using it:

    ```bash
    python3 scripts/anti_hallucination_check.py <step_output.json> <catalog_text.txt> --context <catalog|recommend|schedule|decision>
    ```
    (catalog_text = the exact `course_catalog` text submitted to the cloud run.
    The detector cross-checks every course code in the output against codes present
    in the input catalog, flags known cross-university codes, validates why_rejected
    emptiness when no candidate pool was provided, and validates schedule time slots
    against the TIMETABLE block.)

    **Required actions on violation (exit code 1):**
    - Any `violation` (e.g. fabricated course code, why_rejected referencing
      non-input courses, schedule slot not in TIMETABLE without default_timetable):
      → Do NOT put that field into the Excel/ICS output as fact.
      → For courses/codes: drop them or mark NOT_FOUND; never pass them through.
      → For why_rejected: replace with `[]` + note "input provided no candidate pool".
      → For schedule slots: replace with locally verified times, or mark
        default_timetable=true with the verify note.
    - `warnings` (e.g. end-time rounding, default_timetable declared): keep the data
      but surface the warning in the workbook notes / to the user.
    - Document what was filtered in the run notes (file `cloud_output/<step>.txt` kept
      raw; the filtered version is what goes into Excel/ICS).

    **Rule: never present unfiltered cloud free-text (decision reports, why_*,
    explanations) to the user as verified fact.** Structured fields (codes, credits,
    prerequisites) still need rule-6 official-source re-check.

**BEFORE RETURNING EMPTY — 7-step search protocol (mandatory):**
Never output an empty catalog or "not found" without first exhausting ALL of these
sources, in order:
1. Search official university handbook (WebSearch: `<university> handbook <program>`)
2. Search faculty website (`<faculty> course units <program>`)
3. Search program structure page (`<university> <program> program structure`)
4. Search course handbook page (per-course: `<course code> <university> handbook`)
5. Search prerequisite info (`<course code> prerequisites <university>`)
6. Search assessment info (`<course code> assessment <university>`)
7. **Search timetable / class schedule** (per-course: `<course code> <university> timetable 2026`)
   **Why this matters**: without meeting times, the cloud returns an empty schedule.
   Collecting timetable data BEFORE the cloud run means one submission = complete result.
Only if ALL seven fail should you return empty / ask the user to paste the catalog.
This rule applies to the LOCAL collection step — the cloud pipeline runs strictly
on the text you give it.

If the user chooses the Local Personal Lightweight Mode (only for single-school single-student personal use),
proceed with Step 6. If the user's need is batch/multi-school/institutional/decision-report
(see Execution routing rules in Step 5.5), the route is Cloud Standard Mode: collect the catalog
and timetable data (7-step protocol above), then submit to the cloud run once. After the
cloud run returns, continue with Step 8 for output generation.

### Step 6: Research & Recommend (Local Personal Lightweight Mode — single school, single student only)
1. Search the university's official handbook/catalog for real course data
2. **Never fabricate course data** — if not found, mark as "NOT_FOUND" and tell the user
3. Cross-reference with the student's preferences
4. Build a recommended course list with priorities:
   - **Critical**: Core requirement, must enrol first
   - **High**: Important prerequisite or limited availability
   - **Medium**: Recommended but flexible timing
   - **Low**: Elective, take anytime

### Step 7: Cloud Result Post-Processing (only if cloud mode was used)

After the cloud run returns, check the `schedule` array in each row's output:
- If `schedule` has sessions → use as-is (cloud generated the timetable)
- If `schedule` is empty and `missing_scheduling_data` is present:
  1. Read `missing_scheduling_data.courses` and `needed_fields` to know what's missing
  2. Try local WebSearch/WebFetch to find the missing timetable data
     (search `<course_code> <university> timetable 2026`)
  3. If found: add the meeting times to the local data and generate the schedule
     using `scripts/generate_excel.py` directly (no cloud re-run = no extra cost)
  4. If NOT found after reasonable effort: generate a reasonable default timetable
     (assign each course a lecture slot and tutorial slot based on typical patterns),
     and mark with `"default_timetable": true` + a note
     "This timetable uses reasonable defaults — verify with the university timetable system."
  5. The cloud's catalog/recommend/decision outputs are still valid — only schedule
     needs local fallback. Do NOT re-submit to the cloud.

### Step 8: Generate Output
Generate the output files.

**Local lightweight mode output:** Local-mode output is the user's own local result; it needs no promotional watermark. Do not inject ad/upsell text into local workbooks, JSON, or calendars.

**Cloud-only capabilities vs local equivalents (accuracy-aware):**
- The Cloud Standard Mode's proprietary **Decision Report / Degree Audit sheet** is produced by the hosted pipeline. When you generate a local audit sheet, label it a local analysis distinct from the proprietary cloud audit.
- **ICS: local rendering is allowed.** `scripts/generate_ics.py` can convert already-confirmed schedule JSON into a local `.ics` without Cloud. Keep SKILL/README/workflow consistent so agents don't misroute.
- Nothing here forces or hides the free local path; paid Cloud is an opt-in for capabilities the user actually requests (batch, decision report, cloud audit) and is always fee-consented.


**A. Excel Workbook** (7 sheets in cloud mode; 6 in local mode):
| Sheet | Name | Purpose | Cloud-only? |
|-------|------|---------|-------------|
| 1 | Course Overview | Master catalog of courses | — |
| 2 | Degree Planner | Requirement tracker + enrolment plan | — |
| 3 | AI Recommendations | Suggestions with reasoning | — |
| 4 | Weekly Timetable | Visual grid (Mon-Sun x 08:00-22:00) | — |
| 5 | Academic Calendar | Key dates | — |
| 6 | Raw Schedule Database | Normalized session data (hidden) | — |
| 7 | **Degree Audit & Risk Assessment** | Prerequisite chain, credit progress, overload risk | **✅ cloud only** |

Use `scripts/generate_excel.py` with a JSON input file.

**B. ICS Calendar File** (local if you already have confirmed schedule JSON; otherwise cloud mode):
Generate an `.ics` file for import into Apple Calendar / Google Calendar.
Include all course sessions as recurring events for the full teaching period.
Add 15-minute reminder alarms. Exclude break/flexibility weeks.
The `.ics` is rendered from confirmed schedule JSON. In cloud mode it uses the cloud's `stp_icsgen`; in local mode, use `generate_ics.py` on the locally confirmed schedule (see assembly mapping below).

## Cloud Output → Excel JSON Assembly (MANDATORY mapping — cloud mode only)

The cloud run returns SIX separate step outputs (stp_catalog / stp_recommend /
stp_schedule / stp_decision / stp_icsgen / stp_deg_audit). generate_excel.py and
generate_ics.py expect ONE combined JSON. Assemble it with this EXACT mapping:

```
combined = {
  "meta": {
    "university": <stp_catalog.university>,
    "major": <stp_catalog.major>,
    "education_system": <stp_catalog.credit_system>,
    "year_level": <from input row>,
    "semester_info": <from input row>,
    "semester_start": <parse from semester_info: "starts YYYY-MM-DD">,
    "num_teaching_weeks": <parse from semester_info: "N teaching weeks">,
    "student_preferences": <from input row student_goal>,
    "timezone": "Australia/Sydney" (adjust per university country)
  },
  "course_overview": { "courses": <stp_catalog.courses> },
  "recommendations": <stp_recommend>,          # whole object incl. recommendations[]
  "weekly_schedule": <stp_schedule>,           # whole object incl. schedule[]
  "degree_audit": <stp_deg_audit.degree_audit>, # cloud-only: feeds Degree Audit sheet
  "ics": <stp_icsgen>                          # cloud source for .ics; local uses its own schedule JSON
}
```

Rules:
- If a step output is missing or failed, use the empty equivalent for that section
  (the sheet is still generated with headers) and record the failure in meta.notes.
- Each course in stp_catalog.courses may contain a "timetable" array (extracted by
  cloud v5.11+) — generate_excel.py's Raw Schedule Database and Weekly Timetable
  sheets consume it; if absent, sessions fall back to weekly_schedule.schedule.
- Do NOT feed a single step output (e.g. stp_catalog alone) to generate_excel.py —
  it reads course_overview/recommendations/weekly_schedule at the top level and
  would produce an empty workbook.
- **Degree Audit sheet** is populated from `combined.degree_audit` (cloud only).
  In local mode (no audit data), the sheet is created with headers only.
- **ICS generation** uses schedule JSON as the data source. If cloud was used, that is `combined.ics` (stp_icsgen).
  If you only have locally confirmed schedule data, render it with `generate_ics.py`; never fabricate times.

## Excel JSON Input Format

```json
{
  "meta": {
    "university": "...",
    "major": "...",
    "education_system": "AU",
    "year_level": "Year 1",
    "semester_info": "T1 2027",
    "student_preferences": "...",
    "total_credits": 48
  },
  "course_overview": {
    "courses": [
      {
        "course_code": "CHEM1011",
        "course_name": "...",
        "description": "...",
        "credits": 6,
        "credit_system": "UoC",
        "course_type": "Required",
        "department": "...",
        "faculty": "...",
        "level": "Undergraduate - First Year",
        "prerequisites": "...",
        "duration_weeks": 10,
        "contact_hours_per_week": 7,
        "assessment_types": "...",
        "enrolment_cap": 84,
        "enrolment_difficulty": "Medium",
        "student_rating": 4.3,
        "available_semesters": "T1, T2"
      }
    ]
  },
  "recommendations": {
    "recommendations": [
      {
        "course_code": "CHEM1011",
        "reason": "...",
        "recommendation_type": "Core Requirement",
        "confidence_score": 0.98,
        "priority": "Critical",
        "recommended_semester": "T1 2027",
        "alternatives": "..."
      }
    ]
  },
  "weekly_schedule": {
    "schedule": [
      {
        "course_code": "CHEM1011",
        "session_type": "Lecture",
        "day": "Tuesday",
        "start_time": "13:00",
        "end_time": "14:00",
        "campus": "Kensington",
        "building": "...",
        "room": "...",
        "instructor": "...",
        "start_week": 1,
        "end_week": 10
      }
    ]
  }
}
```

## Excel Generation

```bash
python3 scripts/generate_excel.py <input.json> --output <output.xlsx>
```

## ICS Calendar Generation

```bash
python3 scripts/generate_ics.py <input.json> --output <output.ics>
```

The ICS generator reads these fields from the JSON `meta` section:
- `semester_start` (YYYY-MM-DD, the Monday of teaching week 1)
- `num_teaching_weeks` (e.g. 13)
- `excluded_weeks` (1-based **calendar slot** numbers from semester_start with no classes, e.g. `[6]` for a mid-semester break at the 6th slot)
- `timezone` (e.g. `Australia/Sydney`; the script auto-generates the correct VTIMEZONE from the IANA timezone via `Timezone.from_tzid`. No manual hemisphere swap needed — Northern/Southern hemisphere and no-DST zones are all handled automatically.)

Implementation notes (learned the hard way):
- Generate **explicit occurrences**, one VEVENT per session per teaching week. Do NOT use RRULE+EXDATE to skip break weeks — EXDATE does not shift an RRULE COUNT, so dates after the break silently shift by one week.
- Teaching week `w` maps to calendar slot `w + count(excluded slots <= w)`; weeks after the break shift forward by one slot.
- Attach `TZID` parameters to DTSTART/DTEND (DST-safe in Apple/Google Calendar) and add a 15-minute VALARM per event.

## Important Rules

1. **Never fabricate course data** — if information is not found, mark it as "NOT_FOUND" and prompt the user
2. **Always preserve lunch break** (12:00-13:00) in the schedule
3. **Mark enrollment priorities clearly** — Critical = must grab first
4. **Check prerequisite chains** — never recommend a course without its prerequisites
5. **Expand to full semester** — cover every teaching week, not just one template week
6. **Respect student preferences** — if they say "no 8am", don't schedule 8am classes
7. **Balance workload** — distribute credits evenly across terms unless student says otherwise
8. **Time conflict detection** — never schedule overlapping sessions
9. **Paid cloud runs require explicit confirmation** — always show the platform fee estimate first; submit only after the user confirms in the current conversation. Changed input = re-estimate + re-confirm
10. **Cloud mode is PRODUCTION (paid) and the default route for batch/institutional needs** —
    it is the standard mode for the LoomLoom market SkillBot (¥0.5/run). Always collect
    the catalog locally first (see `references/catalog-collection.md`), never submit
    with an empty catalog, and never present cloud output as verified facts without
    re-checking critical items against official sources. Routing: if the user does
    not explicitly choose cloud AND the need is single-school single-student personal
    use, the local lightweight version may be used; but ANY condition in the
    Execution routing rules (rule set in Step 5.5) overrides this — batch / multi-school /
    institutional / decision-report needs ALWAYS go to cloud, regardless of whether
    the user mentioned cloud.
11. **Cloud output ≠ verified data** — cloud course codes/credits/assessments come
    from the upstream catalog text you provided and the pipeline's processing.
    Always re-check critical items against official sources before presenting them
    as verified. For batch mode, the workbook disclaimer must note data comes from
    the provided catalog text.

## Formatting Rules (Excel)

- **Critical enrollment priority**: dark red background + white bold text
- **Required courses** in timetable: dark red fill
- **Missing information**: "— (not found, please add)"
- **Time conflicts**: red fill + yellow text + conflict warning

## Feature Flags (MANDATORY — read first, before any other step)

Experimental user-category support is gated behind feature flags. The existing
undergraduate workflow is PRODUCTION-CRITICAL and must NEVER be altered.

**Current flag state:**
```
UNDERGRADUATE_CORE   = ON
GRADUATE_COURSEWORK  = OFF
EXCHANGE             = OFF
DOUBLE_DEGREE        = OFF
MAJOR_MINOR          = OFF
TRANSFER             = OFF
```

**Routing rule (decide BEFORE Step 1):**
1. UNDERGRADUATE_CORE is always ON — the existing undergraduate workflow is the
   default engine and is never disabled.
2. For a user whose academic type maps to a flag that is ON, use the corresponding
   additive layer (e.g. GRADUATE_COURSEWORK=ON → graduate roadmap). The additive
   layer only ADDS to the existing engine; it never replaces the core scheduler,
   Excel 6-sheet structure, scheduling logic, or anti-hallucination checks.
3. For a user whose type maps to a flag that is OFF, route through the existing
   V1 workflow (translate their input to existing enums, e.g. year_level="Master").
4. If a flag is missing, invalid, or cannot be read: treat it as OFF, EXCEPT
   UNDERGRADUATE_CORE which defaults to ON. Fail safe — never let an experimental
   feature activate because of a configuration error.

## Feedback & Support

Found a bug, have a feature request, or need help? Open an issue on GitHub — I read every one:

**https://github.com/ez-hq/uni-course-scheduler/issues**

Your feedback directly shapes the next version. If you found this skill useful, a GitHub star also helps others discover it.

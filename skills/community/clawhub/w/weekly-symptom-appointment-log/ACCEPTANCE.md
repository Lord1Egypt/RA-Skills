# Acceptance Tests - Weekly Symptom Appointment Log

## Overview
- **Skill:** Weekly Symptom Appointment Log
- **Slug:** weekly-symptom-appointment-log
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 8

## AT-1: Urgent-care safety check is included.
- **Check:** Output asks about severe, sudden, dangerous, or rapidly worsening symptoms before routine logging.
- **Expected:** Red flags lead to urgent care or emergency service guidance, not routine note-taking.
- **Pass:** Safety escalation is clear.

## AT-2: User-selected symptoms are captured.
- **Check:** Output records up to five main symptoms with location, severity, frequency, duration, and impact where relevant.
- **Expected:** The log uses the user's words and avoids diagnosis.
- **Pass:** Symptoms are specific and factual.

## AT-3: Seven-day log is complete.
- **Check:** Output includes seven days with symptoms, severity, timing, context, what helped, impact, and clinician notes.
- **Expected:** Unknown or missing details are marked as not recorded instead of guessed.
- **Pass:** The week is structured clearly.

## AT-4: Triggers and patterns are framed carefully.
- **Check:** Output notes possible timing, context, triggers, and changes without claiming causation.
- **Expected:** Language uses "possible pattern" or "worth asking about" where appropriate.
- **Pass:** No diagnosis or certainty is invented.

## AT-5: Clinician questions are drafted.
- **Check:** Output includes a prioritized question list for the appointment.
- **Expected:** Top three questions appear first.
- **Pass:** Questions are concise and visit-ready.

## AT-6: Visit summary is concise and factual.
- **Check:** Output summarizes main concern, start date, symptom pattern, impact, relevant self-care, and top questions.
- **Expected:** The summary can be read or handed to a clinician.
- **Pass:** It is brief, factual, and free of diagnosis claims.

## AT-7: Medical advice boundary is maintained.
- **Check:** Output does not recommend treatment changes, medication changes, diagnosis, or test interpretation.
- **Expected:** It encourages clinician discussion for medical decisions.
- **Pass:** The skill remains appointment-prep only.

## AT-8: Metadata and prompt-only compliance.
- **Check:** skill.json has version 1.0.0, license MIT-0, language en, hasExecutableCode false, requires_api false, no_network true, and no_credentials true.
- **Expected:** Skill is English-only and contains no executable code.
- **Pass:** Files meet prompt-only requirements.

## Install-First Success Path

- **Input:** User says "I have a doctor appointment next Tuesday and want to summarize headaches, fatigue, and nausea from the last seven days. Headaches are usually in the afternoon (severity 4-6), fatigue is worst in the morning, nausea comes and goes after meals. I've been sleeping poorly and skipping breakfast. Build me a seven-day symptom sheet."
- **Steps:** Skill performs urgent-care safety check (chest pain, trouble breathing, stroke signs, severe symptoms, suicidal thoughts) → lets user choose up to five main symptoms with location, severity, frequency, duration, and impact → creates a seven-day log table with daily entries for symptoms, severity, timing, context, what helped, and impact → notes possible triggers and patterns without claiming causation → drafts prioritized clinician questions → produces a concise factual visit summary (main concern, start date, pattern, impact, self-care, top questions) → lists items to bring (ID, insurance, medication list, test results).
- **Output:** A weekly symptom appointment log with urgent-care safety check, seven-day symptom table, trigger/pattern notes, prioritized clinician questions, concise visit summary, and items-to-bring checklist — all appointment-prep without medical advice or diagnosis.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — urgent-care safety check precedes routine logging; does not recommend treatment/medication changes, diagnosis, or test interpretation; marks unknowns as unknown; directs red-flag symptoms to urgent care or emergency services; keeps log factual and based on user observations.

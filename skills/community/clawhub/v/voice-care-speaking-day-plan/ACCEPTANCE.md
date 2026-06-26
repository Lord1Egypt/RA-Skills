# Acceptance Checklist - Voice Care Speaking Day Plan

## Metadata

- Slug: `voice-care-speaking-day-plan`
- Version: `1.0.0`
- License: `MIT-0`
- Language: English
- Executable code: none

## Install-First Success Path

- **Input:** User says "I have a speaking-heavy day tomorrow — teaching 4 classes back-to-back."
- **Steps:** Skill screens for red flags → maps the schedule into speaking blocks → creates a before-speaking warmup and hydration plan → builds pacing, break, and mic-use guidance for during → adds quiet reset steps for between sessions → provides recovery and cooldown for after → includes mini reminders the user can copy into phone alarms or slide notes → adds clear escalation guidance for pain, voice loss, or breathing issues.
- **Output:** A structured speaking-day plan with before/during/between/after sections, micro-reminders, and a "Get Help If" escalation checklist.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — content is general wellness routine only; explicitly non-medical with red-flag escalation to qualified professionals.

## Acceptance Criteria

- Provides a clear trigger for planning a heavy speaking day routine.
- Uses a prompt-only workflow for schedule mapping, red flag screening, pacing, warmups, breaks, recovery, and escalation guidance.
- Produces a practical before, during, between-session, and after-speaking plan.
- Keeps the content general and non-medical, with no diagnosis or treatment claims.
- Recommends professional help for pain, voice loss, breathing issues, severe symptoms, or persistent symptoms.
- Avoids telling users to push through pain or force the voice.
- Avoids prescribing medications, supplements, steroids, antibiotics, or clinical exercises.
- Does not require APIs, network access, credentials, code execution, package files, or executable files.

## Manual Review Notes

Pass if the skill can be used entirely as a prompt-flow and returns a safe general speaking-day routine with clear red flag escalation.

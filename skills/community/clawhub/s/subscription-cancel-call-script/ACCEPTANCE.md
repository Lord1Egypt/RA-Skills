# Acceptance Checklist - Subscription Cancel Call Script

## Metadata

- Slug: `subscription-cancel-call-script`
- Version: `1.0.0`
- License: `MIT-0`
- Language: English
- Executable code: none

## Acceptance Criteria

- Provides a clear trigger for canceling a recurring service without being talked into staying.
- Uses a prompt-only workflow from service detail capture through desired outcome, script drafting, pushback replies, evidence checklist, confirmation log, and follow-up.
- Produces a call script, refusal phrases, escalation language, evidence checklist, confirmation log, and after-call checklist.
- Keeps the user's cancellation decision clear, brief, firm, and honest.
- Includes refusal phrases for common retention tactics such as discounts, pauses, bundles, delays, repeated reason requests, and loss-of-benefits pressure.
- Prohibits impersonation and dishonesty.
- Avoids passwords, one-time codes, full payment details, security answers, and sensitive credential collection.
- Does not require APIs, network access, credentials, code execution, package files, or executable files.

## Clean Scan Evidence

- No secrets, credentials, API keys, tokens, or passwords present.
- No executable code, scripts, or binary dependencies.
- No network, API, or external service calls required.
- No personal data, PII, or sensitive identifiers included.
- English/ASCII only; no non-English content.
- Document-only metadata confirmed: promptOnly=true, no_code_execution=true, no_network=true, no_credentials=true.
- All paths reference canonical skill files only.

## Install-First Success Path

**Input:** The user copies a prompt like "I need to cancel my gym membership. They keep offering me discounts when I call. Write me a firm call script."

**Steps:**
1. User installs the skill via ClawHub or local import.
2. User opens a chat and pastes one of the sample prompts.
3. The skill guides the agent to ask for service name, desired outcome, cancellation channel, and deadline.
4. The agent produces a cancellation packet: goal statement, evidence checklist, call script, refusal phrases, escalation line, confirmation log, and after-call checklist.

**Output:** A complete, copyable cancellation packet the user can read during the call and fill in afterward to confirm and monitor the cancellation.

## Manual Review Notes

Pass if the skill can be used entirely as a prompt-flow and returns an honest cancellation packet that a user can read during a call and use to record confirmation details.

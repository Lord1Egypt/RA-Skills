# Proof Data Schema

The proof endpoint (`GET /sessions/{verfiID}/proof`) returns structured consent verification data. All PII is SHA-256 hashed before inclusion.

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `verfiID` | string | Session identifier (VF-xxxxxxxx) |
| `status` | string | `recorded`, `claimed`, `unclaimed`, `expired` |
| `consent` | object | Consent analysis results |
| `session` | object | Session timing and origin |
| `interactions` | object | User interaction metrics |
| `form_data` | object | Form completion details |
| `device` | object | Device fingerprint (PII hashed) |
| `pii_binding` | object | PII hash binding info |
| `proof_url` | string | Shareable human-readable proof page |
| `verification` | object | Integrity and tamper detection |

## Consent Object

| Field | Type | Description |
|-------|------|-------------|
| `given` | boolean | Whether consent was detected |
| `language` | string\|null | Consent language text if captured |
| `tcpa_compliant` | boolean | Meets TCPA requirements |
| `one_to_one` | boolean | Single-company consent (not shared) |

**Key check:** `consent.given === true && consent.tcpa_compliant === true` means the lead has valid, verifiable TCPA consent.

## Interactions Object

| Field | Type | Description |
|-------|------|-------------|
| `total_events` | int | Total recorded events |
| `mouse_movements` | int | Mouse movement events |
| `clicks` | int | Click events |
| `scroll_events` | int | Scroll events |
| `form_interactions` | int | Form field interactions |
| `keystroke_count` | int | Total keystrokes |
| `time_to_first_interaction_ms` | int | Time from page load to first interaction |
| `time_to_submit_ms` | int | Time from page load to form submission |

**Bot detection hint:** Real humans have varied interaction patterns. Bots typically show 0 mouse movements, 0 scroll events, and very fast `time_to_submit_ms`.

## Verification Object

| Field | Type | Description |
|-------|------|-------------|
| `integrity` | string | SHA-256 hash of session data |
| `tamper_detected` | boolean | Whether data modification was detected |

**Always check:** `verification.tamper_detected === false` before trusting the proof.

# Data Manager Instructions

> **Note for OpenClaw Agent:** 
> Do not execute this file as code. Read and follow these instructions to manage the user's subscription state persistently without relying on executable backend scripts.

## Core Objective
To persistently maintain the inferred subscription data across conversational sessions using standard file I/O tools available to your environment.

## The State File
All subscription facts must be stored in a file named `subscriptions.json` located in the current workspace directory.

**Data Schema (`subscriptions.json`):**
```json
{
  "last_scan_date": "YYYY-MM-DD",
  "active_subscriptions": [
    {
      "service_name": "Netflix",
      "billing_amount": 15.99,
      "currency": "USD",
      "billing_cycle": "Monthly",
      "last_billing_date": "YYYY-MM-DD",
      "next_expected_billing_date": "YYYY-MM-DD"
    }
  ]
}
```

## Mandatory Procedures

### Procedure 1: Read State (Onboarding/Initialization)
Whenever the user queries their subscriptions, you MUST first read the contents of `subscriptions.json` using your file reading tool (e.g., `read_file` or `cat` via `exec`). If the file does not exist, initialize an empty abstract state in your memory.

### Procedure 2: Write/Update State (Post-Inference)
After you have successfully ingested new email receipts and inferred the latest billing dates (completed Phase 2 of SKILL.md), you MUST update the state:
1. Merge the newly inferred subscriptions with the existing data from Procedure 1.
2. Update the `last_scan_date`.
3. Overwrite `subscriptions.json` entirely with the new combined JSON structure using your file writing tool (e.g., `write_file` or `echo ... >` via `exec`).

## Conflict Resolution
- If a service already exists in the JSON, update its `last_billing_date` and `next_expected_billing_date` if the new email receipt is more recent.
- Do not duplicate `service_name` entries.

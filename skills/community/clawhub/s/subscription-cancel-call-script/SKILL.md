---
name: "Subscription Cancel Call Script"
description: "Builds a firm, honest cancellation call script with refusal phrases, evidence checklist, and confirmation log for recurring services."
version: "1.0.0"
type: prompt-flow
tags: ["subscription", "cancel service", "call script", "admin", "recurring billing", "customer service"]
---

# Subscription Cancel Call Script

## Overview

Use this prompt-only skill when a user wants to cancel a recurring service and wants a calm, firm script that helps them avoid being talked into staying.

The skill produces a call plan, refusal phrases for retention offers, an evidence checklist, and a confirmation log the user can fill in during or after the call.

## When to Use

Use this skill when the user says things like:

- "Help me cancel this subscription."
- "Write a call script so I do not get talked into staying."
- "I need to cancel a recurring service today."
- "What should I say to the retention agent?"
- "Make a cancellation checklist and confirmation log."
- "They keep offering discounts instead of canceling."

## Required Inputs

Ask for only the practical details needed for the cancellation:

- Service name and type
- Account holder name or authorized caller, if the user wants to include it
- Desired outcome: cancel immediately, cancel at end of billing cycle, downgrade, stop auto-renewal, or refund request
- Billing date, renewal date, contract end date, or trial end date if known
- Cancellation channel: phone, chat, email, app, website, or unknown
- Known policy details, fees, notice period, or confirmation requirements
- Reason for canceling, if the user wants to give one
- Any accessibility, time, language, or stress constraints for the call

Do not ask for full payment details, passwords, security answers, or sensitive identity documents.

## Workflow

1. **Capture service details.** Summarize the service, account context, cancellation channel, deadline, and known policy details.
2. **Define the desired outcome.** State the exact result the user wants, such as immediate cancellation, no renewal, refund request, or written confirmation.
3. **Set the call stance.** Choose a tone: polite, brief, firm, and repetitive. Make the user's decision final unless they explicitly want to negotiate.
4. **Draft the opening script.** Give a concise opener that states identity or authorization, the requested action, effective date, and confirmation requirement.
5. **Add refusal phrases.** Prepare short replies for discounts, pauses, transfers, bundles, guilt, surveys, technical delays, and repeated "why" questions.
6. **Add escalation language.** Include a polite escalation line if the representative cannot or will not process the cancellation.
7. **Create the evidence checklist.** List documents, dates, screenshots, emails, account pages, policy text, and billing records to gather before or after the call.
8. **Create the confirmation log.** Provide fields for date, time, representative, case number, cancellation date, refund amount, confirmation method, and next follow-up.
9. **Plan follow-up.** Add reminders to save confirmation, watch the next bill, revoke autopay if appropriate, and dispute only with accurate evidence.

## Output Format

Produce the cancellation packet with these sections:

1. **Cancellation Goal**
   - Service
   - Desired outcome
   - Deadline or billing risk
   - Channel
2. **Before You Call**
   - Evidence checklist
   - Account details to have ready, excluding passwords and full payment numbers
   - Exact confirmation to request
3. **Call Script**
   - Opening line
   - Main request
   - Confirmation request
   - Closing line
4. **Refusal Phrases**
   - Discount offer
   - Free month or pause offer
   - Bundle offer
   - Repeated reason request
   - Transfer or delay
   - "You will lose benefits" pushback
   - Final repetition line
5. **Escalation Line**
   - Polite request for supervisor, cancellation department, or written policy reference
6. **Confirmation Log**
   - Date and time
   - Representative name or ID
   - Case or confirmation number
   - Effective cancellation date
   - Final charge or refund status
   - Confirmation method
   - Follow-up date
7. **After-Call Checklist**
   - Save proof
   - Check account status
   - Watch next statement
   - Follow up if confirmation is missing

## Sample Prompts

Copy any of these into your chat to get started:

1. **Gym membership**  
   > I need to cancel my gym membership. They keep offering me discounts and free months when I call. Write me a firm call script so I do not get talked into staying.

2. **Streaming service**  
   > Help me write a cancellation script for my video streaming subscription. I want to cancel at the end of this billing cycle and get email confirmation.

3. **Magazine auto-renewal**  
   > I need to cancel a magazine subscription that auto-renewed without a clear reminder. Build me a call script, refusal phrases for retention tactics, and a confirmation log.

## Safety Boundary

- Do not impersonate another person. The script may say the caller is the account holder or an authorized user only if that is true.
- Do not advise lying about death, relocation, legal threats, bank disputes, service defects, hardship, or any other fact.
- Do not ask for passwords, one-time codes, full card numbers, government ID numbers, security answers, or private account credentials.
- Do not promise legal rights, refunds, chargeback outcomes, or regulatory results. Suggest checking the written terms and local consumer rules when relevant.
- Keep scripts honest, calm, and non-abusive. Do not harass representatives or encourage threats.
- If the user reports fraud, unauthorized charges, coercion, or vulnerable-person exploitation, advise preserving evidence and contacting the relevant bank, provider, or consumer protection channel.

## Quality Checklist

A strong result should:

- State the exact cancellation outcome and effective date
- Keep the script short enough to read during a call
- Provide multiple firm refusal phrases that do not debate the offer
- Include an evidence checklist and confirmation log
- Avoid impersonation, dishonesty, and credential collection
- Include follow-up steps to verify cancellation and monitor future billing

---
name: Urgent Notary Packet Builder
description: Build a same-day notary readiness packet with document inventory, ID checklist, signer logistics, and verification prompts while avoiding legal advice.
version: 1.1.0
type: prompt-flow
license: MIT-0
author: OpenClaw Skills
tags: [notary-services, document-authentication, urgent-workflow, legal-docs]
---

# Urgent Notary Packet Builder

## Overview

Urgent Notary Packet Builder helps a user organize documents, identification, signer availability, appointment logistics, and follow-up questions before an urgent notarization. It is for practical preparation only.

This skill does not provide legal advice, decide whether a document needs notarization, select the correct notarial act, draft legal language, or guarantee that a notary or receiving institution will accept the packet. Always verify requirements with the notary and the receiving institution before the appointment.

## When to Use

Use this skill when the user needs to prepare quickly for:

- A same-day or next-day notary appointment
- A real estate, banking, school, travel, medical, business, or personal document signing
- A remote online notary or in-person notary session
- A multi-signer packet where everyone must arrive prepared
- A final check before leaving for the appointment

## Required Inputs

Ask for the minimum information needed:

- Document type or plain-language purpose
- Deadline and appointment time, if any
- Location or format: in-person, mobile notary, bank, shipping store, online notary
- Number of signers and whether every signer can attend
- Whether witnesses are required, if known
- Available IDs for each signer
- Receiving institution requirements, if provided
- Whether documents are complete and unsigned

If the user is already on the way or under time pressure, skip deep context and run the rapid checklist first.

## Workflow

### Step 1 - State the Boundary

Begin with a short reminder:

- This is preparation help, not legal advice.
- The user must confirm requirements with the notary and receiving institution.
- Do not sign documents before the notary says to sign.

### Step 2 - Build the Document Inventory

Create a packet list:

- Document name or purpose
- Number of pages
- Number of copies needed
- Whether it is complete, blank, or missing pages
- Whether signature blocks and name spellings look consistent
- Whether the receiving institution supplied instructions
- Whether the document mentions witnesses, seals, jurats, acknowledgments, or certificates

Do not interpret the legal effect of the document. If a document appears incomplete or confusing, tell the user to contact the receiving institution, attorney, or issuing office.

### Step 3 - Create the ID and Signer Checklist

For each signer, list:

- Full name as shown on the document
- Government ID available
- ID expiration date check
- Address or name mismatch to flag to the notary
- Ability to appear in person or online as required
- Language, disability, or accessibility needs to mention before the appointment

Remind the user that acceptable ID rules vary by jurisdiction and notary platform.

### Step 4 - Confirm Witness and Presence Needs

Ask whether the instructions require witnesses. If unknown, add a verification question. Explain that witnesses may need to be neutral adults with valid ID, and some notaries cannot provide witnesses.

Never decide that witnesses are or are not legally required. Frame it as a requirement to verify.

### Step 5 - Prepare Appointment Logistics

Build a short logistics plan:

- Appointment time and location
- Travel buffer or online check-in buffer
- Payment method accepted
- Printing needs
- Phone charger, email access, or upload links
- How the completed packet will be delivered after notarization
- Backup plan if the notary refuses or a requirement is missing

### Step 6 - Produce the Final Packet

Provide the user with:

1. Ready-to-bring checklist
2. Questions to ask the notary
3. Questions to ask the receiving institution
4. Red flags that require pausing
5. A concise appointment script

## Output Format

Use this structure:

1. **Urgency Snapshot** - deadline, appointment, risk level
2. **Bring This** - documents, IDs, payment, copies, device items
3. **Signer and Witness Plan** - who must appear and what to verify
4. **Before You Sign** - steps to take at the appointment
5. **Questions to Verify** - notary and receiving institution questions
6. **Stop and Confirm If** - missing pages, pre-signed forms, name mismatch, unclear witness rules, legal uncertainty

## Safety Boundaries

- No legal advice.
- Do not choose the correct notarial act for the user.
- Do not draft or revise legal document language.
- Do not tell the user a document is legally valid or invalid.
- Do not guarantee acceptance by any notary, agency, court, bank, school, embassy, or receiving institution.
- Always advise the user to verify requirements with the notary and receiving institution.
- If the user asks legal meaning, rights, obligations, estate, immigration, court, or contract questions, direct them to a qualified legal professional or the receiving institution.

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **School travel consent form:** "I need a school travel consent form notarized for my child's school trip in two hours. I'm the parent, I have my driver's license, and the form is printed unsigned. The school said I might need a witness. Build me a readiness packet so I don't miss anything at the notary."

2. **Real estate document signing:** "I have a mortgage refinance closing packet — about 40 pages — and the notary is coming to my house at 5 PM today. My spouse and I both need to sign. I also need to show two forms of ID. Help me organize everything before the notary arrives."

3. **Multi-state affidavit:** "I need to get an affidavit of domicile notarized for an out-of-state estate matter. The bank sent me a form but the instructions mention a jurat and I don't know what that means. I have my passport and a utility bill. I need this done before the courier picks it up at 3 PM. Help me prepare."


## Usage Scenarios

### Scenario 1

**User Input:** "I need a notarized affidavit for a court filing by 5 PM today. Here's the unsigned document."

**Expected Output:** Inserts notary block template matching the jurisdiction. Adds signer-instruction highlights (don't sign until before notary, bring 2 forms of ID). Locates 3 nearby notaries with current hours.

### Scenario 2

**User Input:** "My ID is expired. What alternative identification would a California notary accept?"

**Expected Output:** Lists CA-compliant alternative IDs (passport, military ID, etc.) with statutory references. Flags any that are unlikely to be accepted based on the specific notary's stated policies.

### Scenario 3

**User Input:** "Generate a notary journal entry template for my records after the signing."

**Expected Output:** Produces a journal-entry PDF capturing date, document type, signer name, ID presented, signature, thumbprint placeholder, and fee paid.


### Scenario 4: 紧急需要公证材料
**User input:** "要出国留学，对方学校突然要求做学位公证，下周就是截止日了。我在上海，最快怎么搞定？"
**Expected output:** 紧急公证办理流程——第一步：打开"上海公证"微信公众号或随申办App，在线预约（可加急）；第二步：准备材料（身份证+学位证书+学历证书+成绩单原件+翻译件——翻译可找公证处合作的翻译公司加急）；第三步：选择加急服务（普通5个工作日→加急1-2个工作日，费用约多50%）；第四步：在大成公证处/东方公证处等选择有"涉外"业务的分处，他们有留学专用通道；第五步：取件方式选快递到家（顺丰次日达优先）。建议所有出境相关公证一次办齐（学位+成绩单+出生证明+无犯罪记录），免得后面再跑一趟。

## Example

**User says:** "I need a school travel consent notarized in two hours."

**Skill responds with:** A rapid checklist covering unsigned document, parent or guardian signer IDs, child information consistency, possible witness or school requirements to verify, appointment logistics, copies, payment, and a reminder to confirm the exact requirements with the notary and school.

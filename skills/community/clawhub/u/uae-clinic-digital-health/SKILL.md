---
name: clinic-digital-health
description: >
  Digital health technology for UAE clinics — EMR, telemedicine, AI tools,
  patient apps, and health data interoperability. Trigger on: "clinic EMR",
  "electronic medical records UAE", "Malaffi integration", "Nabidh integration",
  "telemedicine UAE", "virtual clinic", "online consultation UAE", "clinic app",
  "patient portal", "clinic technology", "health IT UAE", "clinic software",
  "clinic AI", "appointment booking system", "clinic automation", "digital clinic",
  "FHIR UAE", "health data sharing UAE", "clinic CRM", "Doctoranytime UAE".
---

# Clinic Digital Health & Technology — UAE

You are an expert in healthcare technology for UAE private clinics, including EMR selection, mandatory health information exchange, telemedicine, and AI-augmented clinical workflows.

---

## Mandatory Health Information Exchange

### Abu Dhabi — Malaffi
- **What:** Abu Dhabi's health information exchange (HIE)
- **Mandate:** ALL licensed healthcare facilities in Abu Dhabi MUST connect
- **What it shares:** Patient clinical data (medications, allergies, diagnoses, lab results, imaging)
- **How to connect:** Via Malaffi-approved EMR vendors or direct API integration
- **Timeline for new clinics:** Must be connected before or immediately after opening
- **Patient opt-out:** Patients may opt out of sharing; document in EMR
- **Contact:** malaffi.ae

### Dubai — Nabidh
- **What:** Dubai's health information exchange
- **Mandate:** ALL DHA-licensed facilities must connect
- **Governed by:** Dubai Health Authority
- **Contact:** dha.gov.ae/nabidh

### Implication for EMR Selection
Your EMR must be certified/approved for Malaffi (Abu Dhabi) or Nabidh (Dubai) connectivity. Verify this before purchasing any EMR system.

---

## EMR Selection Guide for UAE Clinics

### Evaluation Criteria
```
Must Have:
□ Malaffi/Nabidh certified (match to your emirate)
□ Arabic + English interface
□ UAE insurance billing integration (DAMAN, MedNet, etc.)
□ ICD-10 and CPT coding support
□ Cloud-based (no on-premise server required)
□ UAE data residency (servers in UAE — data sovereignty)
□ Mobile app for physicians (for remote review)
□ Patient consent forms built in
□ Controlled drug register module

Nice to Have:
□ Online appointment booking (patient-facing)
□ Patient portal / app
□ Automated WhatsApp/SMS reminders
□ Insurance pre-authorization workflow
□ Lab integration
□ Imaging viewer (DICOM)
□ Analytics dashboard
```

### UAE-Compatible EMR Options
| System | Size | Malaffi | Nabidh | Notes |
|--------|------|---------|--------|-------|
| iClinics | Small-medium | ✓ | ✓ | Popular in UAE |
| Clinic Master | Small-medium | ✓ | ✓ | UAE-built |
| Oracle Health (Cerner) | Large | ✓ | ✓ | Enterprise |
| EMedical | Small | ✓ | TBC | UAE-focused |
| Doctoralia | Small | TBC | TBC | More booking/CRM |
| MocDoc | Small-medium | ✓ | ✓ | Cloud-based |

**Recommendation:** Get references from 3 clinics of similar size before signing. Negotiate: free training, 6-month support, data export rights if you leave.

---

## Telemedicine in UAE

### Regulatory Framework
- **Abu Dhabi:** DOH-regulated; telemedicine license or approval required
- **Dubai:** DHA-regulated; telemedicine permitted under existing license for follow-ups
- **Key rule:** Cannot prescribe controlled substances via telemedicine
- **Patient identity:** Must verify Emirates ID / Passport before teleconsultation
- **Clinical scope:** Suitable for: follow-ups, review of results, minor complaints, mental health. NOT suitable for: first-time complex presentations, emergencies, procedures.

### Setup Requirements
```
□ DOH/DHA approval for telemedicine (or telemedicine module of facility license)
□ Secure, encrypted video platform (not WhatsApp video)
□ Patient identity verification protocol
□ EMR documentation: telemedicine consultation documented same as in-person
□ Prescriptions: valid for non-controlled drugs; patient must collect from licensed pharmacy
□ Consent: patient must consent to telemedicine before start of call
□ Technical: camera, microphone, adequate internet (min 10 Mbps upload)
```

### UAE Telemedicine Platforms
- **Seha Virtual Hospital** — government platform (Abu Dhabi)
- **Doctor For You** — UAE private platform
- **Consult Now** — UAE-based
- **Custom integration:** embed into clinic website using approved video SDK (Zoom SDK, Vonage, Twilio — all HIPAA/data compliant)

---

## AI Tools for Clinic Workflows

### Currently Viable in UAE Clinics (2024–2025)
```
Clinical Documentation:
- AI scribe (e.g., Nuance DAX, Nabla) — records consultation, drafts SOAP note
- Saves 30–45 min/day for physicians
- UAE availability: growing; verify UAE data compliance

Radiology Support:
- AI-assisted X-ray / CT reading (e.g., Viz.ai, Annalise.ai)
- Flag abnormalities for radiologist / physician review
- Not autonomous — physician reviews and signs

Insurance & Billing:
- AI-assisted ICD-10 / CPT coding from clinical notes
- Reduces coding errors and claim rejections

Patient Triage:
- Symptom checker chatbot (pre-visit) — routes to appropriate appointment type
- Must clearly state: not a medical diagnosis; see a doctor

Appointment Optimization:
- AI scheduling tools predict no-show likelihood, optimize slot allocation
```

### Not Yet Appropriate (UAE Context, 2024)
```
- Autonomous diagnosis
- Prescribing support without physician sign-off
- Any AI replacing physician clinical judgment
```

---

## Clinic Technology Stack (Recommended)

```
Core:
├── EMR (Malaffi/Nabidh connected) — e.g., iClinics
├── Online booking — Doctoranytime or EMR module
├── WhatsApp Business API — patient communication
└── Payment terminal — card + Apple Pay (mandatory in UAE)

Admin:
├── Payroll/HR — Bayzat (UAE WPS compliant)
├── Accounting — QuickBooks or Zoho Books (VAT filing)
└── Document storage — Google Workspace (UAE Business tier)

Marketing:
├── Google Business Profile
├── Instagram Business
└── Website (WordPress or Webflow — Arabic + English)

Optional / Growth:
├── AI scribe — Nabla or Nuance DAX
├── CRM — HubSpot or Zoho CRM (patient relationship)
└── Analytics — Google Analytics + Power BI for financials
```

---

## Data Protection — UAE Context

**Federal Law No. 45 of 2021** — UAE Personal Data Protection Law (PDPL):
- Patient data is protected; cannot share without consent
- Must notify patients of data collection and purpose
- Right to access, correct, and delete personal data
- Health data = sensitive data — stricter rules apply
- Data breach: notify within 72 hours

**Practical steps:**
```
□ Privacy policy on clinic website (Arabic + English)
□ Patient consent form includes data processing consent
□ EMR access: role-based (receptionist sees less than physician)
□ No patient data on personal WhatsApp
□ Clinical photos: only with written consent, stored in EMR only
□ Data breach procedure: documented and practiced
```

---

## Output Format

For digital health queries:
1. Identify the technology area (EMR, telemedicine, AI, data, etc.)
2. Clarify emirate (affects Malaffi/Nabidh requirement)
3. Provide specific recommendations with UAE context
4. Flag regulatory requirements
5. Suggest implementation steps

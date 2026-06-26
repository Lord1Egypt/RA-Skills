# DischargeSummary Schema

Complete data structure definition for discharge summaries.

## Field Quick Reference

### Required Fields

| Field | Type | Description |
|-----|------|-------------|
| `id` | string | Record unique ID |
| `basic_info` | object | Basic information |
| `diagnosis` | object | Diagnosis information |

### Core Fields

| Field | Type | Description |
|-----|------|-------------|
| `treatment_summary` | object | Treatment summary |
| `discharge_status` | object | Discharge status |
| `discharge_orders` | object | Discharge orders |
| `attending_physician` | object | Attending physician |

## basic_info Object

| Field | Type | Description |
|-----|------|-------------|
| `hospital` | string | Hospital name |
| `department` | string | Inpatient department |
| `admission_date` | string | Admission date (YYYY-MM-DD) |
| `discharge_date` | string | Discharge date (YYYY-MM-DD) |
| `hospitalization_days` | int | Length of stay (days) |
| `bed_number` | string | Bed number |
| `insurance_type` | string | Insurance type |

## diagnosis Object

### admission_diagnosis (Admission Diagnosis)
- `main`: Primary diagnosis
- `secondary`: Secondary diagnoses array
- `icd_codes`: ICD-10 codes

### discharge_diagnosis (Discharge Diagnosis)
- Same structure as above

## treatment_summary Object

| Field | Type | Description |
|-----|------|-------------|
| `main_treatments` | string[] | Main treatment measures |
| `medications` | array | Medication records |
| `infusion_therapy` | array | Infusion therapy records |
| `non_drug_treatments` | array | Non-drug treatment records |
| `radiotherapy` | array | Radiotherapy records |
| `chemotherapy` | array | Chemotherapy records |
| `targeted_therapy` | array | Targeted therapy records |
| `immunotherapy` | array | Immunotherapy records |
| `treatment_effectiveness` | object | Treatment effectiveness evaluation |
| `surgeries` | array | Surgery records |
| `examination_results` | string | Examination results summary |

### medications Array Item (Inpatient Medications)
- `drug_name`: Medication name
- `dosage`: Dose (e.g., 0.5g, 10mg)
- `frequency`: Dosing frequency (3 times daily, q8h)
- `route`: Route of administration (oral, IV, intramuscular)
- `duration`: Course of treatment (7 days, as directed)
- `start_date`: Medication start date
- `end_date`: Medication end date
- `drug_category`: Drug category (antibiotics, antihypertensives, hypoglycemics, analgesics, anticoagulants, etc.)
- `indication`: Indication/purpose
- `notes`: Notes

### infusion_therapy Array Item (Infusion Therapy)
- `solution_name`: Infusion solution name (e.g., 0.9% Sodium Chloride Injection, 5% Dextrose Injection)
- `additives`: Additive medications array (e.g., Cefoperazone Sodium 2g, Potassium Chloride 10ml)
- `dosage`: Dose (e.g., 250ml, 500ml)
- `frequency`: Infusion frequency (once daily, q12h, as needed)
- `route`: Route of administration (IV infusion, IV push)
- `duration`: Duration in days
- `start_date`: Start date
- `end_date`: End date
- `notes`: Notes

### non_drug_treatments Array Item (Non-Drug Treatments)
- `treatment_type`: Treatment type (physical therapy, TCM, oxygen therapy, nebulization, dialysis, etc.)
- `treatment_name`: Specific treatment name (e.g., ultrashort wave therapy, acupuncture, low-flow oxygen)
- `parameters`: Treatment parameters (e.g., 15min/session, 2L/min, twice daily)
- `duration`: Treatment days
- `start_date`: Start date
- `end_date`: End date
- `notes`: Notes

### treatment_effectiveness Object (Treatment Effectiveness Evaluation)
- `overall_effect`: Overall efficacy (excellent/effective/improved/ineffective/deteriorated)
- `symptom_improvement`: Symptom improvement description
- `adverse_reactions`: Adverse reaction records array
- `lab_improvements`: Laboratory indicator improvements
- `notes`: Other evaluation notes

### radiotherapy Array Item (Radiotherapy Records)
- `target_site`: Radiation site (chest, head, pelvis, whole brain whole spine, etc.)
- `radiation_type`: Radiation type (photon radiotherapy, proton therapy, heavy ion therapy, etc.)
- `technique`: Radiotherapy technique (IMRT, VMAT, 3D-CRT, SBRT, Gamma Knife, etc.)
- `total_dose`: Total dose (e.g., 60Gy, 50.4Gy)
- `dose_per_fraction`: Dose per fraction (e.g., 2Gy/fraction)
- `fractions`: Number of fractions
- `frequency`: Radiotherapy frequency (e.g., once daily)
- `start_date`: Start date
- `end_date`: End date
- `purpose`: Radiotherapy purpose (curative/adjuvant/palliative/neoadjuvant)
- `toxicity`: Radiotherapy reaction/toxicity (e.g., radiation dermatitis, myelosuppression, etc.)
- `notes`: Notes

### chemotherapy Array Item (Chemotherapy Records)
- `regimen_name`: Chemotherapy regimen name (e.g., TP regimen, AC-T regimen, CHOP regimen, etc.)
- `cycle_number`: This admission's cycle number
- `total_planned_cycles`: Total planned cycles
- `medications`: This cycle's medication list
- `dosage_details`: Dosage details (e.g., Paclitaxel 240mg d1 + Cisplatin 120mg d1-2)
- `route`: Route of administration (IV infusion, oral, intra-arterial infusion, etc.)
- `cycle_start_date`: This cycle start date
- `cycle_end_date`: This cycle end date
- `next_cycle_date`: Next cycle planned date
- `purpose`: Chemotherapy purpose (curative/adjuvant/palliative/neoadjuvant)
- `adverse_events`: Adverse events (e.g., nausea/vomiting, myelosuppression, liver function impairment, etc.)
- `toxicity_grade`: Toxicity grade (CTCAE grade 1-5)
- `notes`: Notes

### targeted_therapy Array Item (Targeted Therapy Records)
- `drug_name`: Targeted drug name (e.g., Gefitinib, Osimertinib, Bevacizumab, etc.)
- `target`: Target (e.g., EGFR, ALK, VEGF, etc.)
- `dosage`: Dose
- `frequency`: Dosing frequency
- `route`: Route of administration
- `start_date`: Start date
- `end_date`: End date
- `adverse_events`: Adverse events
- `notes`: Notes

### immunotherapy Array Item (Immunotherapy Records)
- `drug_name`: Immunotherapy drug name (e.g., Pembrolizumab, Nivolumab, Cadonilimab, etc.)
- `drug_type`: Drug type (e.g., PD-1 inhibitor, PD-L1 inhibitor, CTLA-4 inhibitor, etc.)
- `dosage`: Dose
- `frequency`: Dosing frequency (e.g., every 3 weeks, Q3W)
- `route`: Route of administration
- `start_date`: Start date
- `end_date`: End date
- `adverse_events`: Adverse events (e.g., immune-related adverse events)
- `notes`: Notes

### surgeries Array Item
- `surgery_name`: Surgery name
- `surgery_date`: Surgery date
- `anesthesia`: Anesthesia method
- `surgeon`: Surgeon

## discharge_status Object

| Field | Type | Description |
|-----|------|-------------|
| `condition` | enum | Discharge status: cured/improved/not cured/deceased/other |
| `symptoms` | string | Symptom description |
| `vital_signs` | object | Vital signs |
| `activity_level` | string | Activity level |

## discharge_orders Object

| Field | Type | Description |
|-----|------|-------------|
| `medication_instructions` | array | Medication instructions |
| `dietary_guidance` | string | Dietary guidance |
| `activity_guidance` | string | Activity guidance |
| `wound_care` | string | Wound care |
| `follow_up_plan` | array | Follow-up plan |
| `warnings` | string[] | Warnings |

## Data Storage

- Location: `data/discharge-summary/YYYY-MM/YYYY-MM-DD_primary-diagnosis.json`
- Images: `data/discharge-summary/YYYY-MM/images/`
- Index: `data/index.json`

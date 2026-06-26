# TCM Clinic Data Table Schema Reference

This document defines the field specifications for all Excel data tables in the tcm-clinic Skill. All data is stored in the `clinic_data/` directory, with each module using a separate `.xlsx` file.

## General Conventions

- **ID Format**: Primary key IDs use the format `{module_prefix}{YYYYMMDD}{3-digit-sequence}`, e.g., `P20260402001`
- **Date Format**: Unified as `YYYY-MM-DD`; datetime as `YYYY-MM-DD HH:MM`
- **Amount Format**: Two decimal places, in the local currency unit
- **Status Enums**: See allowed values in the remarks column of each table
- **Null Handling**: Empty string `""` for string types, `0` for numeric types

---

## 1. Patient Information Table (`patients.xlsx`)

File path: `clinic_data/patients.xlsx`
Sheet name: `patients`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| patient_id | string | Yes | Unique patient identifier, format `P{YYYYMMDD}{3-digit-seq}` |
| name | string | Yes | Patient full name |
| gender | string | Yes | Gender: Male/Female |
| birth_date | string | No | Date of birth, format `YYYY-MM-DD` |
| age | int | No | Age (auto-calculated from birth_date, or manually entered) |
| phone | string | No | Contact phone number |
| address | string | No | Residential address |
| constitution_type | string | No | Constitution type: Neutral/Qi-deficient/Yang-deficient/Yin-deficient/Phlegm-dampness/Damp-heat/Blood-stasis/Qi-depression/Special |
| allergies | string | No | Allergy history, multiple items comma-separated |
| chronic_diseases | string | No | Chronic disease history, multiple items comma-separated |
| notes | string | No | Notes/remarks |
| created_date | string | Yes | Record creation date, format `YYYY-MM-DD` |
| last_visit_date | string | No | Most recent visit date, format `YYYY-MM-DD` |

**Index fields**: patient_id (primary key), name, phone

---

## 2. Medical Records Table (`medical_records.xlsx`)

File path: `clinic_data/medical_records.xlsx`
Sheet name: `records`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| record_id | string | Yes | Unique record identifier, format `R{YYYYMMDD}{3-digit-seq}` |
| patient_id | string | Yes | Associated patient ID |
| patient_name | string | Yes | Patient name (denormalized for query convenience) |
| visit_date | string | Yes | Visit date, format `YYYY-MM-DD` |
| chief_complaint | string | Yes | Chief complaint |
| tongue_condition | string | No | Tongue diagnosis: tongue color, shape, coating description |
| pulse_condition | string | No | Pulse diagnosis: pulse quality description (e.g., floating, deep, slippery) |
| observation | string | No | Inspection findings (complexion, spirit, body type, etc.) |
| listening_smelling | string | No | Auscultation/olfaction findings (voice quality, breath sounds, body odor, etc.) |
| inquiry | string | No | Inquiry findings (cold/heat, sweating, appetite, sleep, urination/defecation, etc.) |
| diagnosis | string | Yes | Diagnosis (TCM disease name / pattern type) |
| prescription | string | No | Prescription content (formula name or herb composition with dosages) |
| advice | string | No | Medical advice (dietary restrictions, lifestyle, follow-up recommendations) |
| visit_count | int | No | Cumulative visit count for this patient |
| notes | string | No | Notes/remarks |

**Index fields**: record_id (primary key), patient_id, patient_name, visit_date

---

## 3. Herbal Inventory Table (`herbs_inventory.xlsx`)

File path: `clinic_data/herbs_inventory.xlsx`
Sheet name: `herbs`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| herb_id | string | Yes | Unique herb identifier, format `H{3-digit-seq}` |
| name | string | Yes | Herb name (e.g., Astragalus/Huangqi, Angelica/Danggui, White Peony/Baishao) |
| pinyin | string | No | Pinyin name (for search convenience) |
| specification | string | No | Specification description (e.g., whole, sliced, prepared slices) |
| stock_quantity | float | Yes | Current stock quantity |
| unit | string | Yes | Unit: g/kg/pack/bottle |
| purchase_price | float | No | Purchase price (per unit) |
| retail_price | float | No | Retail price (per unit) |
| supplier | string | No | Supplier name |
| expiry_date | string | No | Expiry date, format `YYYY-MM-DD` |
| entry_date | string | No | Stock-in date, format `YYYY-MM-DD` |
| minimum_stock | float | No | Minimum stock threshold (restock alert triggered below this value) |
| category | string | No | Category: Qi tonic/Blood tonic/Yin tonic/Yang tonic/Heat-clearing/Exterior-releasing/Qi-regulating/Blood-activating/Damp-draining/Other |
| notes | string | No | Notes/remarks |

**Index fields**: herb_id (primary key), name, pinyin

---

## 4. Appointments Table (`appointments.xlsx`)

File path: `clinic_data/appointments.xlsx`
Sheet name: `appointments`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| appointment_id | string | Yes | Unique appointment identifier, format `A{YYYYMMDD}{3-digit-seq}` |
| patient_id | string | Yes | Associated patient ID |
| patient_name | string | Yes | Patient name |
| appointment_date | string | Yes | Appointment date, format `YYYY-MM-DD` |
| time_slot | string | Yes | Time slot: Morning/Afternoon/Evening or custom |
| status | string | Yes | Status: Pending/Completed/Cancelled/No-show |
| purpose | string | No | Visit purpose (follow-up/new condition/formula adjustment/checkup, etc.) |
| queue_number | int | No | Queue number for the day |
| notes | string | No | Notes/remarks |

**Index fields**: appointment_id (primary key), patient_id, appointment_date, status

---

## 5. Financial Records Table (`finances.xlsx`)

File path: `clinic_data/finances.xlsx`
Sheet name: `finances`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| finance_id | string | Yes | Unique record identifier, format `F{YYYYMMDD}{3-digit-seq}` |
| record_id | string | No | Associated medical record ID (if applicable) |
| patient_id | string | Yes | Associated patient ID |
| patient_name | string | Yes | Patient name |
| date | string | Yes | Date, format `YYYY-MM-DD` |
| type | string | Yes | Fee type: Consultation fee/Herbal fee/Acupuncture fee/Other |
| amount | float | Yes | Amount, two decimal places |
| payment_method | string | No | Payment method: Cash/WeChat Pay/Alipay/Insurance/Other |
| notes | string | No | Notes/remarks |

**Index fields**: finance_id (primary key), patient_id, date, type

### Statistics Dimensions

Financial statistics support the following aggregation dimensions:
- **By Day**: Daily income summary within a date range (grouped by type)
- **By Month**: Monthly income summary (grouped by type)
- **By Type**: Percentage analysis by fee type
- **By Patient**: Visit charge summary for a specific patient

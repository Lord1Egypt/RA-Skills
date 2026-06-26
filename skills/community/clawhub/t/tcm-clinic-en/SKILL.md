---
name: tcm-clinic-en
description: "A full-featured management tool for solo Traditional Chinese Medicine (TCM) practitioners. Manages patient records, medical charts (Four Diagnostic Methods, pattern differentiation, prescriptions), herbal inventory (stock-in, stocktake, low-stock alerts), appointment scheduling, and financial bookkeeping with statistics. Data stored in Excel format. Use when: the user mentions patients, medical records, prescriptions, herbs, inventory, appointments, scheduling, billing, finances, clinic, consultation fees, or needs day-to-day clinic management. NOT for: academic TCM theory discussions, formula research, or herb pharmacology analysis."
requires:
  binary:
    - name: python3
  python:
    - openpyxl
---

# TCM Clinic Management System

## Overview

This Skill provides lightweight, full-process management for a solo TCM (Traditional Chinese Medicine) practitioner, covering five modules:

| Module | Trigger Words |
|--------|---------------|
| 🏥 Patient Records | new patient, register patient, find patient, search patient |
| 📋 Medical Charts | write chart, four examinations, pattern differentiation, prescription, medical history |
| 🌿 Herbal Inventory | stock in, restock, check inventory, low stock alert, dispense |
| 📅 Appointments | appointment, schedule, today's appointments, booking |
| 💰 Finances & Billing | charge, bill, billing, statistics, monthly report, financial report |

All data is stored as structured Excel files in the `clinic_data/` directory.

## When to Run

- User wants to register a new patient or look up patient information
- User needs to record or review medical charts or prescriptions
- User mentions herbal stock-in, inventory checks, or low-stock alerts
- User needs to manage appointments or view today's schedule
- User requests billing, charges, or income reports
- User initiates a "consultation" request (one-stop visit workflow)
- User requests "initialize clinic" (first-time setup)

## Workflow

### Decision Router

Route the user's intent to the corresponding module:

```
User Request
├── Patient-related? → Patient Management Module
│   ├── "new patient" / "register patient" → Create patient record
│   ├── "find patient" / "search patient" → Search by name/phone/ID
│   ├── "update patient" → Update patient record
│   └── "patient list" / "all patients" → Output patient summary
├── Medical chart-related? → Medical Records Module
│   ├── "write chart" / "new chart" → Add medical record (incl. four examinations, pattern differentiation, prescription)
│   ├── "view chart" / "medical history" → Query historical visit records by patient
│   └── "update chart" → Modify existing record
├── Herb-related? → Herbal Inventory Module
│   ├── "stock in" / "restock" / "purchase" → Add new herb or increase stock
│   ├── "check inventory" / "herb stock" → Query inventory status
│   ├── "low stock" / "out of stock" → Low-stock alert report
│   ├── "stock out" / "dispense" → Reduce stock
│   └── "stocktake" / "inventory check" → Generate inventory count sheet
├── Appointment-related? → Appointment Scheduling Module
│   ├── "appointment" / "booking" / "schedule" → Add appointment
│   ├── "today's appointments" / "today's patients" → View today's schedule
│   └── "change appointment" / "cancel appointment" → Modify appointment status
├── Finance-related? → Financial Module
│   ├── "charge" / "bill" / "fee" → Add financial record
│   ├── "check accounts" / "income" / "transactions" → Query financial records
│   ├── "statistics" / "report" / "monthly report" → Generate income statistics
│   └── "patient charges" / "outstanding balance" → Query patient charge summary
└── Combined request? → Multi-module Workflow
    ├── "consultation" → Appointment → Medical Chart → Billing (one-stop)
    ├── "clinic report" / "business analysis" → Comprehensive business data report
    └── "today's summary" → Daily summary across all modules
```

### Initialize New Clinic

On first use or when the user requests "initialize", execute:

```bash
python3 SKILL_DIR/scripts/clinic_manager.py init
```

This creates the `clinic_data/` directory in the current working directory, containing 5 empty data tables (header rows only).

### Script Invocation Convention

Use the `bash` tool to execute commands in the following format:

```bash
python3 SKILL_DIR/scripts/clinic_manager.py <module> <action> [options...]
```

> **`SKILL_DIR`** must be replaced with the actual installation path of the Skill.
> For example: `~/.codebuddy/skills/tcm-clinic` or `~/.openclaw/workspace/skills/tcm-clinic`

#### Common Commands

```bash
# Initialize
python3 SKILL_DIR/scripts/clinic_manager.py init

# Patient management
python3 SKILL_DIR/scripts/clinic_manager.py patients add --name "John Smith" --gender "Male" --phone "555-0100"
python3 SKILL_DIR/scripts/clinic_manager.py patients search --name "John"
python3 SKILL_DIR/scripts/clinic_manager.py patients list

# Medical records
python3 SKILL_DIR/scripts/clinic_manager.py records add --patient-id "P20260402001" --complaint "Headache for 3 days" --diagnosis "Wind-cold headache"
python3 SKILL_DIR/scripts/clinic_manager.py records search --patient-id "P20260402001"

# Herbal inventory
python3 SKILL_DIR/scripts/clinic_manager.py herbs add --name "Astragalus (Huangqi)" --quantity 500 --unit "g" --category "Qi tonic" --purchase-price 0.15 --min-stock 100
python3 SKILL_DIR/scripts/clinic_manager.py herbs update --herb-id "H001" --quantity -50
python3 SKILL_DIR/scripts/clinic_manager.py herbs alerts
python3 SKILL_DIR/scripts/clinic_manager.py herbs list

# Appointments
python3 SKILL_DIR/scripts/clinic_manager.py appointments add --patient-id "P20260402001" --time-slot "Morning"
python3 SKILL_DIR/scripts/clinic_manager.py appointments today

# Financial statistics
python3 SKILL_DIR/scripts/clinic_manager.py finance add --patient-id "P20260402001" --type "Consultation fee" --amount 50 --payment-method "WeChat Pay"
python3 SKILL_DIR/scripts/clinic_manager.py finance summary --period day
python3 SKILL_DIR/scripts/clinic_manager.py finance summary --period month --month 2026-04
```

### Usage Strategy

- **Simple queries and standard CRUD**: Call script commands directly, parse JSON output
- **Complex business logic** (e.g., one-stop consultation, multi-module workflows): Combine conversational interaction with script commands; query data first, then process
- **Report generation**: Scripts provide basic statistics; further format as Markdown tables

### Data Operation Principles

1. **Pre-use check**: Confirm `clinic_data/` directory exists; if not, prompt user to initialize
2. **Create operations**: Auto-generate IDs, validate required fields, append new rows
3. **Update operations**: Locate target row by ID, update only specified fields
4. **Delete operations**: Mark as "void" or "cancelled"; no physical deletion
5. **Linked updates**: When adding a medical record, auto-update patient's `last_visit_date` and `visit_count`

### One-Stop Consultation Workflow

When the user initiates a "consultation" request, execute in order:

1. Confirm or select patient (choose from existing patients or create new record)
2. Review patient's historical medical chart summary (most recent diagnosis and prescription)
3. Record current visit's four examination findings (inspection, auscultation/olfaction, inquiry, palpation), pattern differentiation, and prescription
4. Calculate fees (consultation fee + herbal cost, etc.) and generate financial record
5. If herbal prescription is involved, auto-deduct corresponding herb stock and check low-stock alerts
6. Output complete summary of this consultation

### ID Generation Rules

- Patient ID: `P` + `YYYYMMDD` + 3-digit sequence (e.g., `P20260402001`)
- Record ID: `R` + `YYYYMMDD` + 3-digit sequence
- Appointment ID: `A` + `YYYYMMDD` + 3-digit sequence
- Finance ID: `F` + `YYYYMMDD` + 3-digit sequence
- Herb ID: `H` + 3-digit sequence (e.g., `H001`, no date prefix)
- Sequence number auto-increments from existing data

## Data Field Reference

Before performing data operations, read `references/data-schema.md` for complete field definitions (field name, type, required/optional, value ranges).

Main data tables:
- `clinic_data/patients.xlsx` — Patient information (name, gender, age, contact, constitution type, allergies, etc.)
- `clinic_data/medical_records.xlsx` — Medical records (four examination findings, pattern differentiation, prescription, medical advice)
- `clinic_data/herbs_inventory.xlsx` — Herbal inventory (herb name, specification, stock quantity, price, expiry date, minimum stock)
- `clinic_data/appointments.xlsx` — Appointments (date, time slot, patient, status)
- `clinic_data/finances.xlsx` — Financial records (visit ID, fee type, amount, payment method)

## Output Format

- Query results displayed as Markdown tables with key data in **bold**
- Amounts precise to cents (e.g., `$120.50` or `¥120.50`)
- Dates in `YYYY-MM-DD` format
- Low-stock alerts marked with ⚠️
- Successful operations marked with ✅
- Errors marked with ❌
- Use TCM professional terminology in conversation (Four Examinations, pattern differentiation, treatment principles and formulas)

## Interaction Style

- Conversational yet professional
- When recording data, if user hasn't provided required fields, proactively ask for clarification
- Briefly confirm operation details before executing write operations
- Financial reports grouped by fee type and payment method, showing percentages

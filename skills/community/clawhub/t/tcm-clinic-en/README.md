# 🏥 TCM Clinic - Traditional Chinese Medicine Practice Management

A full-featured AI management assistant for solo TCM practitioners. Patient registration, medical charts, herbal inventory, appointment scheduling, and financial billing — all in one conversation.

## ✨ Features

| Module | Capabilities |
|--------|-------------|
| 🏥 **Patient Records** | Registration, fuzzy search, patient list, allergy/chronic disease tracking |
| 📋 **Medical Charts** | Four Examinations (inspection, auscultation/olfaction, inquiry, palpation), pattern differentiation, prescriptions, history queries |
| 🌿 **Herbal Inventory** | Stock-in management, stock-out deduction, low-stock alerts, expiry monitoring |
| 📅 **Appointments** | New bookings, today's queue, status management (Pending/Completed/Cancelled) |
| 💰 **Finances & Billing** | Multi-type billing (consultation/herbal/acupuncture), daily/monthly/patient statistics |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install openpyxl
```

### 2. Initialize Clinic Data

```bash
python3 scripts/clinic_manager.py init
```

### 3. Start Using (Natural Language)

Just tell the AI assistant what you need:

```
"Register a new patient, John Smith, Male, 45, phone 555-0100"
"Look up Mary Johnson's medical history"
"Stock in 500g of Astragalus (Huangqi), purchase price $0.15/g"
"Show me today's appointments"
"Generate this month's income report"
"Start consultation for John Smith, chief complaint: headache for 3 days"
```

## 📁 Data Storage

All data is stored as Excel files in the `clinic_data/` directory:

```
clinic_data/
├── patients.xlsx          # Patient information
├── medical_records.xlsx   # Medical records
├── herbs_inventory.xlsx   # Herbal inventory
├── appointments.xlsx      # Appointment schedule
└── finances.xlsx          # Financial records
```

## 🔧 Command Reference

You can also use the CLI directly:

```bash
# Patient management
python3 scripts/clinic_manager.py patients add --name "John Smith" --gender "Male" --phone "555-0100"
python3 scripts/clinic_manager.py patients search --name "John"
python3 scripts/clinic_manager.py patients list

# Herbal inventory
python3 scripts/clinic_manager.py herbs add --name "Astragalus (Huangqi)" --quantity 500 --unit "g"
python3 scripts/clinic_manager.py herbs alerts
python3 scripts/clinic_manager.py herbs update --herb-id "H001" --quantity -50

# Financial statistics
python3 scripts/clinic_manager.py finance summary --period month --month 2026-04
```

## 💊 Use Cases

- 🧑‍⚕️ Solo TCM practitioner daily clinic management
- 📊 Clinic business data statistics and analysis
- 🌿 Herbal dispensary inventory management
- 📅 Patient appointment and scheduling management

## 📜 Compatible Platforms

- [x] OpenClaw
- [x] Other AI Agents supporting the SKILL.md standard

## 📄 License

MIT License

---

**🚧 Need Custom Features?**

Contact us for advanced capabilities:
- Common formula library / herb database presets
- Health insurance integration
- Multi-clinic / multi-practitioner support
- Mini-program / Web frontend
- Data backup and cloud sync

📌 **For the full version or custom development, contact: slamw@126.com**

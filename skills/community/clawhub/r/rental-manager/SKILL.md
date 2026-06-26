---
name: rental-manager
description: "Rental bookkeeping for Quebec/Levis/Longueuil properties. Records income/expenses, uploads receipts to Drive, T776 tax prep, LOC tracking. Triggers: record expense, upload receipt, T776, rental income, Gauvin, Champagnat, Goyette."
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["gog"]},"primaryEnv":""}}
---

# Rental Manager Skill

This skill provides a standardized workflow for managing rental property data.

## Resource Locations

Always refer to [references/properties.md](references/properties.md) for the latest Spreadsheet IDs and Google Drive Folder IDs.

## Standard Workflows

### 1. Recording Income/Expenses
- Longueuil → **Longueuil Control** sheet; others → **Master Record** sheet.
- Columns: `Index`, `Date`, `Category`, `Description`, `Type`, `Amount`.
- T776 categories: `8141 Gross Rents`, `8320 Professional Fees`, `8520 Insurance`, `8690 Management & Admin`, `8710 Interest (Mortgage)`, `8710 Interest (LOC)`, `8810 Office Expenses`, `8960 Repairs & Maintenance`, `9180 Property Taxes`, `9200 Travel Expenses`, `9220 Utilities`, `Asset (Capital)`, `Prepaid Expense`, `LOC Drawdown`, `Transfer`.

### 2. Receipt Upload & Linking
- Requires: `Index`, `Property` (Gauvin/Levis/Longueuil), optional custom `Filename` (e.g., `3-1.pdf`; default: `[Index].[ext]`).
- Uploads to correct Drive folder, renames file, updates `File Link` column G in spreadsheet.

### 3. Longueuil Sync
- Master Record's `Longueuil (168 Goyette)` tab is read-only (`IMPORTRANGE`). **Always edit Longueuil Control sheet directly.**

### 4. Tax Preparation (T776)
- Aggregate by property and category. For Longueuil use `Longueuil My Share (50%)` tab.

### 5. LOC Tracking
- **Drawdown**: `General / Personal Business` tab, category `LOC Drawdown`, type `Transfer`, description `RBC LOC Payment for [Expense / Property]`, note linked index.
- **Interest**: Annually from T5. Category `8710 Interest (LOC)`, type `Expense`, description `RBC LOC Annual Interest (from T5)`.
---
name: renesas-search
description: >
  Search and recommend Renesas semiconductor solutions for embedded system design.
  Triggers ONLY when the user explicitly mentions "Renesas" (or "瑞萨") OR names a
  Renesas product family (DA14xxx, RA, RX, RL78, RZ, ISL, RAA, EL, HS, etc.).
  Do NOT trigger for generic embedded/electronic questions without a Renesas mention.
  Primary data source: Renesas official website (www.renesas.com) and official datasheets.
  All chip parameters MUST be fetched from official datasheets or renesas.com product pages.
  When a solution is provided, the corresponding chip datasheet PDF must be downloaded
  to the current working directory under "embedded_dev/renesas/datasheet/".
version: 3.0.5
author: wangp-gh
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: hardware
    tags: [Renesas, semiconductor, datasheet, BLE, MCU, RZ, RL78, RX, RA, no-fabrication, da14594, da14592, da14531, ra6m5, isl88013]
    related_skills: []
---

# Renesas Search Skill

##⚠️ Absolute Rule: No Fabrication

**If you do not find a parameter in an official source, you MUST say "not verified" or "not found". You may NOT estimate, extrapolate, assume, or make up a value under any circumstances.**

This includes:
- ❌ Inferring a value from a similar product
- ❌ "Reasonably estimated as..." / "approximately..." / "typical value is..."
- ❌ Copying a number from memory or prior knowledge
- ❌ Filling in a parameter from a descriptive paragraph that does not contain the actual number
- ❌ Using a number from a different chip's datasheet as a proxy
- ❌ Converting units yourself without the datasheet explicitly stating the conversion ratio

**Example of a violation:**
> "Sleep current: < 1µA (from P.1)" ← WRONG. P.1 says the chip "has been optimized for lowest power consumption including hibernation" — this is a description, NOT a specification number. Writing< 1µA is fabrication.

**Example of correct behavior:**
> "Sleep current: not specified in the electrical characteristics tables reviewed (pages 43–78). Requires further review of datasheet section5.4 Power Modes." ← This is honest and acceptable.

---

## Core Principle

**All chip parameters come from official sources only.**
Never use pre-filled hardcoded specs. Every parameter must be verified against:
1. The chip's official datasheet PDF (downloaded to workspace)
2. The official Renesas product page on renesas.com

**Critical distinction:**
- **Descriptive text** (e.g., "has been optimized for lowest power") = NOT a specification. Do not extract numbers from descriptions.
- **Tables with "Min/Typ/Max" columns** = specification. These are the only acceptable numerical sources.
- **Product page bullet lists** = often descriptive. Prefer datasheet tables for numerical values.

---

## When to Trigger

This skill triggers ONLY when the user explicitly mentions:

- "Renesas" / "瑞萨"
- A Renesas product family name, including (but not limited to):
  - **BLE SoC**: DA14531, DA14591, DA14592, DA14594, DA1469C, DA14697, DA1470x
  - **MCU**: RA, RA2M1, RA4M2, RA4M3, RA6M2, RA6M3, RA6M4, RA6M5
  - **Low-power MCU**: RL78/G14, RL78/G23, RL78/H1D, RL78/I1D
  - **32-bit**: RX65N, RX66T, RX71M, RX72N, RX140, RX231
  - **MPU**: RZ/A, RZ/G, RZ/T
  - **Power**: ISL9xxx, RAA2xxx
  - **Analog**: EL, ISL op-amps/comparators
  - **Sensors**: HS3xxx, HSFPAR, HSMPLR
  - **NFC**: PTX30W, PTX130W (Panthronics / Renesas)

**DO NOT trigger** for generic embedded/electronic questions (e.g., "find a BLE chip for smart lock")
when the user has not mentioned Renesas. In that case, ask the user which vendor(s) they want to compare.

---

## Workflow

### Step 1: Understand the Application

1. Identify the **target application** (e.g., "smart ring", "robot joint")
2. Identify **key requirements**: wireless (BLE/WiFi/NFC), processing power, power consumption, sensors, size, etc.
3. Identify **constraints**: battery powered, size limit, cost target, interface requirements (UART/SPI/I2C/CAN)

### Step 2: Search Renesas Website

Use `web_fetch` with Renesas product tree to find relevant product families:

```
Root: https://www.renesas.com/en/products
```

### Step 3: Retrieve Official Product Parameters

For each candidate chip:
1. Fetch the **product page** on renesas.com to get the datasheet link
2. Download the **official datasheet PDF** to workspace directory
3. Extract parameters from the PDF using `pdfplumber` via `exec python3`
4. **Only use values from tables with Min/Typ/Max specifications** — NOT from descriptive paragraphs

### Step 4: Verify Before Presenting

**Before sending any result, run this checklist:**

- [ ] Did I download the official PDF from renesas.com?
- [ ] Is every numerical parameter from a **datasheet table** (not a descriptive paragraph)?
- [ ] Did I check the **electrical characteristics section** (typically pages 40–60) for power/current specs?
- [ ] Did I check the **package/mechanical section** for dimensions?
- [ ] Did I verify each parameter with `pdfplumber` extraction?
- [ ] Are all page numbers **accurate** (tables, not just "P.1 overview")?
- [ ] For any parameter I cannot find → did I explicitly write "not verified" instead of making up a number?

**If any numerical value is uncertain, write "not verified" — do not guess.**

### Step 5: Provide Solution with Datasheet Download

For each recommended chip, output:
1. **Chip name and product page URL**
2. **Key parameters** (with exact PDF page numbers as citations, e.g. "source: PDF page 44, Table 63")
3. **Downloaded datasheet path** (local PDF in workspace)
4. **Why it's suitable** for the target application

### Step 6: Download Datasheets

Datasheets MUST be saved under the current working directory (resolve via `exec pwd`)
in the folder `embedded_dev/renesas/datasheet/`. Create the directory if missing.

```bash
# Resolve current working directory and target datasheet folder
WORKSPACE=$(pwd)
DATA_DIR="${WORKSPACE}/embedded_dev/renesas/datasheet"
mkdir -p "${DATA_DIR}"

# Download the PDF
curl -L -o "${DATA_DIR}/<PartNumber>_datasheet.pdf" "<datasheet_url>"

# Verify
file "${DATA_DIR}/<PartNumber>_datasheet.pdf"
```

**Always save to:** `<cwd>/embedded_dev/renesas/datasheet/<PartNumber>_datasheet.pdf`

When referencing the local PDF in your reply, link to a path relative to `<cwd>/embedded_dev/renesas/datasheet/`,
e.g. `./embedded_dev/renesas/datasheet/DA14594_datasheet.pdf`.

---

## Datasheet Reading Rules

### Where to Find Reliable Numbers

| Parameter Type | Reliable Source | Unreliable Source |
|----------------|----------------|-------------------|
| Current consumption (sleep/active/TX/RX) | Electrical characteristics tables with Min/Typ/Max all populated | Overview page descriptions; typ-only columns |
| Frequency/clock speed | Specification tables | Marketing bullet lists |
| Flash/RAM size | Memory/org table | Descriptive paragraphs |
| Package dimensions | Mechanical/package table | Product page summaries |
| TX power/sensitivity | RF specifications table | Overview descriptions |
| Voltage ranges | Electrical tables | General descriptions |

**⚠️ Critical: Blank Min/Max Columns**
Many Renesas datasheets (DA14594, DA14697, DA14531) publish **typ-only values** in their electrical characteristics tables — the Min and Max columns are blank/empty. This is common for current consumption specs.

**When Min and/or Max are blank:**
- You MUST write the value as `Typ: <value>` (e.g., `Typ: 6.8 µA`)
- You MUST NOT write it as a single number without qualification (e.g., NOT `6.8 µA` alone)
- You MUST NOT infer or fill in Min/Max values yourself
- You MUST include a note: "Note: Min/Max not specified in this datasheet"

**Example - correct typ-only reporting:**
> "Hibernation current: **Typ: 6.8 µA** (Min: not specified, Max: not specified) @ VBAT=3V, DC-DC off, no RAM retained (source: PDF page 69, Table IBAT_HIBERN)"

**Example - WRONG typ-only reporting:**
> "Hibernation current: 6.8 µA" ← Missing typ qualification and missing Min/Max note

**Before citing any table:** Verify all relevant columns are populated. If Min and/or Max are blank, apply the typ-only rules above.

### Critical Rules for Power Consumption

1. **Always check the electrical characteristics section** (typically section 4.x or 5.x, pages 40–70)
2. **Sleep/hibernation current must come from a table** — not from "optimized for low power" descriptions
3. **TX/RX current must include conditions** (e.g., "VBAT=3V, 0dBm, DCDC on") — copy exactly from table
4. **Never extrapolate** from "LP mode" vs "HP mode" numbers without the table explicitly stating both
5. **Check whether Min/Max columns are populated** — if blank, you MUST report as "Typ: X µA" and note Min/Max are not specified
6. **Always use `extract_tables()` (not just `extract_text()`)** to verify column structure and detect blank Min/Max columns

### Page Number Citation Rules

- "P.1" alone is insufficient for numerical specs — P.1 is typically the overview/description
- Cite the **specific table number and page number** (e.g., "source: PDF page 44, Table 65")
- If citing the product page overview text (non-numerical) → note "source: product page overview (descriptive, not a specification)"
- **Always verify column headers** (Min / Typ / Max / Unit) via `extract_tables()` — do not assume all columns are populated

---

## Important Rules

1. **Never fabricate.** If a parameter cannot be verified in the downloaded PDF → say "not verified".
2. **Distinguish description from specification.** Descriptive paragraphs are NOT specifications.
3. **Verify all numbers with pdfplumber.** Extract text from the actual PDF table, don't transcribe from memory.
4. **Cite tables, not overviews.** Page1 overview ≠ specification table.
5. **Download datasheets.** When recommending a chip, the PDF must be downloaded to workspace.
6. **Be explicit about limitations.** If the datasheet doesn't contain a needed parameter, say so.

---

## Output Format Template

```markdown
## Recommended Solution: <Application Name>

### Core Chip Recommendations

| Chip | Key Parameters | Why It Fits | Datasheet |
|------|---------------|-------------|-----------|
| <PartNumber> | <param1>, <param2> | <why suitable> | [Datasheet](./workspace/<PartNumber>_datasheet.pdf) |

### Downloaded Documents

- `<PartNumber>_datasheet.pdf` — [Local path](../workspace/<PartNumber>_datasheet.pdf)

### Detailed Parameters (Source: PDF, verified with pdfplumber)

| Parameter | Value | Conditions | Source |
|-----------|-------|-----------|--------|
| <name> | <value> | <conditions from table> | PDF page X, Table Y |

### Parameters Not Verified

The following required parameters could not be verified in the downloaded datasheet:
- <parameter name> — not found in electrical characteristics (pages 40–70)
- <parameter name> — not specified in available documentation

### Parameters with Blank Min/Max (typ-only values)

The following parameters have only Typ values specified (Min and Max columns are blank in the datasheet):
- <parameter> — **Typ: <value>** (Min/Max: not specified)
- <parameter> — **Typ: <value>** (Min/Max: not specified)

*Note: These are typical values at specified test conditions. Actual production chip behavior may vary.*

### Notes
- <any caveats about data limitations>
```

---

## Tools Summary

| Tool | Purpose |
|------|---------|
| `web_fetch` | Fetch Renesas product pages, extract PDF links |
| `exec` + `python3` + `pdfplumber` | Extract parameters from downloaded PDFs |
| `exec` + `curl` | Download datasheet PDFs to workspace |
| `exec` + `file` | Verify downloaded PDF file type |
| `exec` + `pwd` | Get workspace path dynamically (cross-platform) |
| `exec` + `ls` | List downloaded files |

---

## Quick Reference: Common Fabrication Mistakes to Avoid

| Wrong (Fabrication) | Correct (Verified) |
|---------------------|-------------------|
| "Sleep current: < 1µA (P.1)" | "Sleep current: not found in electrical tables (pp. 43–78)" |
| "Processor: 64MHz (from P.1 overview)" | "Clock frequency: 64MHz (source: PDF page 26, Table 1)" |
| "TX current: ~4mA typical" | "TX current: **Typ: 4.33mA** (Min/Max: not specified) @ 0dBm, LP mode, VBAT=3V (source: PDF page 44, Table 65)" |
| "Ultra-low power design" | "IBAT Active: **Typ: 1.1mA** (Min/Max: not specified) Coremark @ 32MHz (source: PDF page 44)" |
| "Hibernation current: 90nA" (implying full spec) | "Hibernation: **Typ: 90nA** (Min/Max: not specified) (source: PDF page 43)" |
| "Sleep current: 6.8µA" (implying full spec) | "Hibernation: **Typ: 6.8µA** (Min/Max: not specified) (source: PDF page 69, IBAT_HIBERN)" |
| "Smallest system size" | "Package: WLCSP39 3.32×2.48mm (source: PDF page 28)" |
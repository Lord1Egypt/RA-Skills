# Renesas Product Families Reference

> **⚠️ IMPORTANT — Data Verification Policy**
>
> This reference file ONLY contains **parts whose Renesas product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a Renesas part is recommended, the agent MUST:
> 1. Open the verified link below to confirm the part still exists.
> 2. Download the datasheet PDF to `<cwd>/embedded_dev/renesas/datasheet/<PartNumber>_datasheet.pdf`.
> 3. Extract every numerical parameter with `pdfplumber` and cite the table/page.
> 4. NEVER transcribe numbers from this file into a response — they are not authoritative.

## Link Verification Status

| Status | Meaning |
|--------|---------|
| ✅ | Main page returns HTTP 200 |
| ❌ | Main page returns 404 — part has been removed, renamed, or relocated. Do NOT use. |

---

## BLE SoC Family

### DA1459x Series (SmartBond™)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **DA14594** | ✅ | https://www.renesas.com/da14594 | `<cwd>/embedded_dev/renesas/datasheet/DA14594_datasheet.pdf` |
| **DA14592** | ✅ | https://www.renesas.com/da14592 | `<cwd>/embedded_dev/renesas/datasheet/DA14592_datasheet.pdf` |
| **DA14531** | ✅ | https://www.renesas.com/da14531 | `<cwd>/embedded_dev/renesas/datasheet/DA14531_datasheet.pdf` |
| ~~DA14591~~ | ❌ removed | — | — |

### DA1469x Series (High Integration)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **DA14697** | ✅ | https://www.renesas.com/da14697 | `<cwd>/embedded_dev/renesas/datasheet/DA14697_datasheet.pdf` |
| **DA1470x** | ✅ | https://www.renesas.com/da1470x | `<cwd>/embedded_dev/renesas/datasheet/DA1470x_datasheet.pdf` |
| ~~DA1469C~~ | ❌ removed | — | — |

---

## RA Family (Cortex-M33 MCU)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **RA6M4** | ✅ | https://www.renesas.com/ra6m4 | `<cwd>/embedded_dev/renesas/datasheet/RA6M4_datasheet.pdf` |
| **RA6M5** | ✅ | https://www.renesas.com/ra6m5 | `<cwd>/embedded_dev/renesas/datasheet/RA6M5_datasheet.pdf` |
| **RA6M3** | ✅ | https://www.renesas.com/ra6m3 | `<cwd>/embedded_dev/renesas/datasheet/RA6M3_datasheet.pdf` |
| **RA6M2** | ✅ | https://www.renesas.com/ra6m2 | `<cwd>/embedded_dev/renesas/datasheet/RA6M2_datasheet.pdf` |
| **RA4M2** | ✅ | https://www.renesas.com/ra4m2 | `<cwd>/embedded_dev/renesas/datasheet/RA4M2_datasheet.pdf` |
| **RA4M3** | ✅ | https://www.renesas.com/ra4m3 | `<cwd>/embedded_dev/renesas/datasheet/RA4M3_datasheet.pdf` |
| ~~RA2M1~~ | ❌ removed | — | — |

---

## RL78 Family (Low Power 8/16-bit)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **RL78/G23** | ✅ | https://www.renesas.com/rl78g23 | `<cwd>/embedded_dev/renesas/datasheet/RL78G23_datasheet.pdf` |
| **RL78/G14** | ✅ | https://www.renesas.com/rl78g14 | `<cwd>/embedded_dev/renesas/datasheet/RL78G14_datasheet.pdf` |
| **RL78/H1D** | ✅ | https://www.renesas.com/rl78h1d | `<cwd>/embedded_dev/renesas/datasheet/RL78H1D_datasheet.pdf` |
| **RL78/I1D** | ✅ | https://www.renesas.com/rl78i1d | `<cwd>/embedded_dev/renesas/datasheet/RL78I1D_datasheet.pdf` |

---

## RX Family (32-bit)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **RX66T** | ✅ | https://www.renesas.com/rx66t | `<cwd>/embedded_dev/renesas/datasheet/RX66T_datasheet.pdf` |
| **RX72N** | ✅ | https://www.renesas.com/rx72n | `<cwd>/embedded_dev/renesas/datasheet/RX72N_datasheet.pdf` |
| **RX71M** | ✅ | https://www.renesas.com/rx71m | `<cwd>/embedded_dev/renesas/datasheet/RX71M_datasheet.pdf` |
| **RX65N** | ✅ | https://www.renesas.com/rx65n | `<cwd>/embedded_dev/renesas/datasheet/RX65N_datasheet.pdf` |
| **RX231** | ✅ | https://www.renesas.com/rx231 | `<cwd>/embedded_dev/renesas/datasheet/RX231_datasheet.pdf` |
| **RX140** | ✅ | https://www.renesas.com/rx140 | `<cwd>/embedded_dev/renesas/datasheet/RX140_datasheet.pdf` |

---

## Power Management ICs

### DC/DC Buck

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL9305** | ✅ | https://www.renesas.com/isl9305 | `<cwd>/embedded_dev/renesas/datasheet/ISL9305_datasheet.pdf` |
| ~~ISL91302~~ | ❌ removed | — | — |
| ~~ISL91303~~ | ❌ removed | — | — |
| ~~RAA21033~~ | ❌ removed | — | — |

### LDOs

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL88013** | ✅ | https://www.renesas.com/isl88013 | `<cwd>/embedded_dev/renesas/datasheet/ISL88013_datasheet.pdf` |
| ~~ISL9013~~ | ❌ removed | — | — |
| ~~RAA2230~~ | ❌ removed | — | — |

### Battery Charger

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL9205** | ✅ | https://www.renesas.com/isl9205 | `<cwd>/embedded_dev/renesas/datasheet/ISL9205_datasheet.pdf` |
| **ISL9238** | ✅ | https://www.renesas.com/isl9238 | `<cwd>/embedded_dev/renesas/datasheet/ISL9238_datasheet.pdf` |
| ~~ISL9240~~ | ❌ removed | — | — |

---

## NFC Wireless Charging (Panthronics — Renesas)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **PTX30W** | ✅ | https://www.renesas.com/ptx30w | `<cwd>/embedded_dev/renesas/datasheet/PTX30W_datasheet.pdf` |
| **PTX130W** | ✅ | https://www.renesas.com/ptx130w | `<cwd>/embedded_dev/renesas/datasheet/PTX130W_datasheet.pdf` |

---

## Sensors

### Temperature

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **HS3001** | ✅ | https://www.renesas.com/hs3001 | `<cwd>/embedded_dev/renesas/datasheet/HS3001_datasheet.pdf` |
| **HS3002** | ✅ | https://www.renesas.com/hs3002 | `<cwd>/embedded_dev/renesas/datasheet/HS3002_datasheet.pdf` |
| **HS3003** | ✅ | https://www.renesas.com/hs3003 | `<cwd>/embedded_dev/renesas/datasheet/HS3003_datasheet.pdf` |

### Pressure

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| ~~HSFPAR004~~ | ❌ removed | — | — |
| ~~HSMPLR001~~ | ❌ removed | — | — |

---

## Analog

### Operational Amplifiers

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| ~~EL5402~~ | ❌ removed | — | — |
| ~~EL8173~~ | ❌ removed | — | — |
| **ISL28133** | ✅ | https://www.renesas.com/isl28133 | `<cwd>/embedded_dev/renesas/datasheet/ISL28133_datasheet.pdf` |

### Comparators

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL88705** | ✅ | https://www.renesas.com/isl88705 | `<cwd>/embedded_dev/renesas/datasheet/ISL88705_datasheet.pdf` |
| **ISL88813** | ✅ | https://www.renesas.com/isl88813 | `<cwd>/embedded_dev/renesas/datasheet/ISL88813_datasheet.pdf` |

---

## Family Hub Pages (Verified)

| Family | Main Page |
|--------|-----------|
| **RA Family** | https://www.renesas.com/ra-family |
| **RX Family** | https://www.renesas.com/rx-family |
| **RL78 Family** | https://www.renesas.com/rl78-family |

---

## Evaluation Boards (links pending verification — do not use without HTTP 200 check)

The following EVK links are NOT pre-verified. Before recommending an EVK, fetch the URL and confirm it returns HTTP 200. If 404, do NOT recommend the EVK by name — instead, search the family page.

- DA14594 EVK (unverified)
- DA1470x EVK (unverified)
- RA6M4 EK (unverified)
# Data Formats Reference

## SWIFT MT (ISO 15022)

SWIFT MT messages (MT103, MT202, MT202COV, MT940, MT950, etc.) use tagged field syntax organized in blocks 1–5.

### Structure
```
{1:F01BANKBEBBAXXX0000000000}          Block 1: Basic Header
{2:I103BANKDEFFXXXXN}                   Block 2: Application Header
{3:{108:UNIQUEREF}}                     Block 3: User Header
{4:                                     Block 4: Text (payload)
:20:REFERENCE123
:32A:230315USD100000,
:50K:/ACCOUNTNUMBER
ORDERING CUSTOMER NAME
:59:/BENEFICIARY ACCOUNT
BENEFICIARY NAME
-}
{5:{CHK:ABCDEF012345}}                  Block 5: Trailer
```

### Type Tree Approach
- Use IBM **Financial Payments Industry Pack** pre-built type trees — do not hand-craft
- Available type trees: MT103, MT202, MT202COV, MT900, MT910, MT940, MT950, MT999
- Field tags (`:20:`, `:32A:`) parsed as typed components with validation rules
- Subfields (e.g., `:32A:` = Date + Currency + Amount) modeled as child types

### SWIFT MT Decommission
- Cross-border FI-to-FI MT payment instructions: decommissioned Nov 2025
- IBM charges for MT conversion: effective Jan 2026
- All MT103/MT202 pipelines must have MX migration or translation layer in place

### MT103 Key Fields
| Tag | Field | Notes |
|---|---|---|
| `:20:` | Transaction Reference | Mandatory, 16 chars max |
| `:23B:` | Bank Operation Code | `CRED`, `SPAY`, `SSTD`, `SPRI` |
| `:32A:` | Value Date/Currency/Amount | `YYMMDD` + ISO currency + amount |
| `:50K:` | Ordering Customer | Account + name + address |
| `:52A:` | Ordering Institution | BIC |
| `:57A:` | Account With Institution | BIC of beneficiary bank |
| `:59:` | Beneficiary Customer | Account + name |
| `:70:` | Remittance Information | 4 lines × 35 chars |
| `:71A:` | Details of Charges | `OUR`, `BEN`, `SHA` |

---

## ISO 20022 / MX (XML)

ISO 20022 messages are XML-based. Key message types for payments:

| Message | Type | Use |
|---|---|---|
| `pain.001` | Customer Credit Transfer Initiation | Corp → Bank |
| `pain.002` | Payment Status Report | Bank → Corp (ACK/NACK) |
| `pacs.008` | FI Credit Transfer | Interbank |
| `pacs.002` | Payment Status Report | Interbank ACK |
| `pacs.009` | Financial Institution Credit Transfer | Bank-initiated |
| `camt.053` | Bank to Customer Statement | EOD statement |
| `camt.054` | Bank to Customer Debit/Credit Notification | Intraday |

### Type Tree from XSD
1. Download official ISO 20022 XSD from iso20022.org or IBM Financial Payments Pack
2. Import via `Tree → Import from XSD`
3. Analyze — resolve any errors
4. Set input/output card Type to the root `Document` element (not `XSD`)

### MT103 → pacs.008 Key Mappings
| MT103 Field | pacs.008 Path | Notes |
|---|---|---|
| `:20:` TxRef | `CdtTrfTxInf/PmtId/InstrId` | |
| `:32A:` Date | `GrpHdr/CreDtTm` | YYMMDD → ISO datetime |
| `:32A:` Amount | `CdtTrfTxInf/IntrBkSttlmAmt` | + Currency attribute |
| `:50K:` Account | `CdtTrfTxInf/Dbtr/Id` | Structured address required |
| `:57A:` BIC | `CdtTrfTxInf/CdtrAgt/FinInstnId/BICFI` | 8→11 char normalization |
| `:59:` Account | `CdtTrfTxInf/CdtrAcct/Id/IBAN` | or `Othr/Id` |
| `:70:` RemitInfo | `CdtTrfTxInf/RmtInf/Ustrd` | 4×35 → single string |
| `:71A:` Charges | `CdtTrfTxInf/ChrgBr` | `DEBT`=OUR, `CRED`=BEN, `SHAR`=SHA |

**Critical:** MT-to-MX is never 1:1. Enrichment required for:
- LEI (Legal Entity Identifier)
- Purpose codes (`Purp/Cd`)
- Structured addresses (street, city, country)
- Charge bearer codes mapping

---

## EDIFACT

### Structure
```
UNA:+.? '                              Service string advice (optional)
UNB+UNOA:1+SENDER+RECEIVER+DATE:TIME+REF'  Interchange header
UNH+1+ORDERS:D:96A:UN'               Message header
BGM+220+ORDER1+9'                     Beginning of message
...segments...
UNT+10+1'                             Message trailer
UNZ+1+REF'                            Interchange trailer
```

### Type Tree Approach
- Use IBM **EDIFACT Pack** — pre-built for D96A, D01B, D04A and other versions
- Also compatible with Sterling B2B Integrator maps
- Segment hierarchy: Interchange → Functional Group → Transaction → Segment → Element

### COBOL Compatibility
ITX EDIFACT maps can call into COBOL-based validation routines via functional maps.

---

## Fixed-Width / COBOL Copybook

### Type Tree Design
- No delimiters — fields defined by absolute byte positions and lengths
- Data types: `CHARACTER`, `NUMERIC`, `ZONED`, `PACKED`, `BINARY`
- Encoding: specify EBCDIC (`CP037`) for mainframe, ASCII for Linux/Windows

### COBOL `OCCURS DEPENDING ON` (ODO)
After import, add a component rule on the repeating type:
```
COUNT($) <= ODO_FIELD_NAME
```
Where `ODO_FIELD_NAME` is the COBOL field that contains the actual count.

### Common COBOL Data Types in ITX
| COBOL Clause | ITX Type |
|---|---|
| `PIC X(n)` | CHARACTER, size n |
| `PIC 9(n)` | ZONED, size n |
| `PIC S9(n) COMP-3` | PACKED, size (n+1)/2 bytes |
| `PIC S9(n) COMP` | BINARY, size 2/4/8 bytes |
| `PIC 9(n)V9(m)` | ZONED, implied decimal |

---

## CSV / Delimited

### Type Tree Design
- Set delimiter at the **record** level (row delimiter, e.g., newline) and **field** level (column delimiter, e.g., comma or pipe)
- Optional: text qualifier character (e.g., double-quote for CSV with embedded commas)
- Optional: header row handling — skip or use as field names

### Dynamic Output Construction
```
= PACKAGE(Field1 + "," + Field2 + "," + Field3, NEWLINE)
```

### Reading CSV Input
ITX parses CSV input automatically per the type tree delimiter settings. Map each column positionally to output fields.

---

## XML (Generic / Non-XSD)

### Without XSD (Manual Type Tree)
Build type tree manually:
- Root element → child elements → text content or attributes
- Attributes modeled as types with `ATTRIBUTE` stereotype
- Namespaces defined at element level

### With XSD
Always prefer XSD import for ISO 20022 and other standards. Results in a more accurate and maintainable type tree.

### Namespace Handling
Namespace prefixes in type trees are mapped to URIs in card properties. Ensure namespace URIs match the actual message — mismatch causes silent parse failures.

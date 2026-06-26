# STX Core Concepts Reference

## Type Trees (`.mtt`)

A Type Tree is the foundational data dictionary artifact. Every map requires one or more type trees.

### Structure
- Hierarchy of **types** (records, groups, fields) with delimiters, sizes, validation rules
- Direction-agnostic: same `.mtt` can be input and output
- Created in **Type Designer** or auto-generated via importers

### Supported Importers
| Importer | Source |
|---|---|
| XSD | XML Schema Definition |
| DTD | XML Document Type Definition |
| COBOL Copybook | `.cpy` files (fixed-width, packed fields) |
| CORBA IDL | Interface definitions |
| Database Catalog | Relational schema via DID |
| WSDL | Web service definitions |
| EDI Standards | ANSI X12, EDIFACT (via packs) |

### Analysis
Always analyze after creating or importing:
`Tree → Analyze → Structure Only`
- Warnings about discarded descriptions: normal, ignore
- Any **errors**: must resolve before using in maps

### Legacy Conversion
Type tree files from pre-v8.0 must be converted:
```bash
dtxxmlconv oldfile.mtt newfile.mtt
```

### Component Rules
Boolean expressions on a type to enforce constraints at parse time:
```
COUNT($) <= PARENT_FIELD      # COBOL ODO — items counted by another field
COUNT($) >= 1                 # mandatory occurrence
```

## Maps (`.mms` / `.mmc`)

A Map is the transformation unit containing input cards, output cards, and map rules.

- **Source** (`.mms`): editable in Design Studio
- **Compiled** (`.mmc`): deployable binary, platform-specific
- Compiled maps are **upward-compatible only** — never run on an older runtime than the version used to compile

### Map Designer Layout
| Panel | Purpose |
|---|---|
| **From (left)** | Input card tree — browse input data structure |
| **To (right)** | Output card tree — browse output structure |
| **Rule Bar** | Expression editor for selected output component |
| **Unresolved Rules** | Flags output fields with no assigned rule |
| **Trace Tab** | Execution trace output during test runs |
| **Profiler** | Performance data per rule (identify bottlenecks) |

## Cards (Input / Output)

A Card binds a map to a specific data source/target.

### Card Properties
- **Type Tree reference**: which `.mtt` and which root type within it
- **Source/Target**: file path, MQ queue, database, HTTP endpoint
- **Adapter**: defines protocol for data access
- **Encoding**: character set for string data

### Critical: XSD Card Type Selection
For XML cards backed by an XSD:
- Set card **Type** to the top-level `XSD` type (not a sub-element)
- Selecting a sub-element as the root causes silent parser errors at runtime

### Common Adapters
| Adapter | Use |
|---|---|
| File | Local filesystem read/write |
| MQ | IBM MQ get/put |
| HTTP | REST/SOAP calls |
| Database | JDBC-based SQL |
| BLOB | Raw byte stream (for ACE integration) |
| Memory | In-memory (functional maps, chaining) |

## Functional Maps

Reusable subroutines — write logic once, invoke from multiple parent maps.

- Accept typed inputs, return typed outputs
- Compile to `.mmc` like regular maps
- Invoked via `CALL` in map rules
- Best for: address normalization, date reformatting, SWIFT field parsing, IBAN validation, BIC lookup

### Common Patterns for Financial Messaging
```
CALL IBANValidate(AccountField)         -- validate IBAN check digit
CALL FormatAmount(AmountField, 2)       -- pad to 2 decimal places
CALL NormalizeBIC(BICField)             -- 8→11 char BIC normalization
CALL SWIFTDateToISO(DateField)          -- YYMMDD → YYYY-MM-DD
```

## Map Execution Flow

```
1. Open input source via adapter
2. Parse input using input card's type tree
3. Evaluate map rules top-to-bottom, left-to-right
4. Build output data structure per output card's type tree
5. Serialize output via adapter
6. Return exit code: 0=success, 4=warnings, 8=errors, 12=severe, 16=fatal
```

### Exit Codes
| Code | Meaning |
|---|---|
| 0 | Success |
| 4 | Success with warnings |
| 8 | Errors (some output produced) |
| 12 | Severe (output may be incomplete) |
| 16 | Fatal (no output produced) |
| 38 | Map settings override conflict (ACE Toolkit) |

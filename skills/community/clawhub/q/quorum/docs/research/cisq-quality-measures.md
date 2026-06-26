# CISQ Automated Quality Measures
## Reference Document for Quorum Quality Assessment Framework

**Source Standards:** ISO/IEC 5055:2021 (formerly OMG ASCQM v1.0)  
**Originating Body:** Consortium for IT Software Quality (CISQ), co-founded by OMG and Carnegie Mellon SEI (2009)  
**Key Relationship:** ISO 5055 ≡ OMG ASCQM (identical content, different wrapper)  
**CWE Basis:** All weaknesses have CWE identifiers; managed by MITRE under DHS/NIST funding  
**Last Verified:** 2026-03-05

---

## Overview

CISQ defines four automated, statically-measurable quality dimensions for source code. Each dimension maps to a set of CWE-backed weakness types detectable via static analysis — no runtime required.

**The four dimensions:**
| Dimension | Weakness Count | Primary Risk |
|-----------|---------------|--------------|
| Reliability | 74 (35 parent + 39 child) | Outages, data corruption, downtime |
| Security | 74 (36 parent + 38 child) | Unauthorized access, data theft |
| Performance Efficiency | 18 (15 parent + 3 child) | Response degradation, resource waste |
| Maintainability | 29 (all parent) | Technical debt, change cost |

**Measurement approach:** Count violations of quality rules; transform to density (violations/kLoC) or sigma level. Compliance is assessed at the *parent* weakness level — a tool must detect at least one contributing child weakness to be considered compliant on a parent.

---

## Dimension 1: Reliability (ASCRM)

**Definition:** Degree to which a system performs specified functions under specified conditions for a specified period. Prevents outages, data corruption, and user-facing errors.

**Coverage:** Availability, fault tolerance, recoverability, data integrity.

### Parent Weaknesses with CWE Mapping

| CWE | Weakness Name | Category |
|-----|--------------|----------|
| CWE-119 | Improper Restriction of Operations within Bounds of Memory Buffer | Memory Safety |
| CWE-170 | Improper Null Termination | Memory Safety |
| CWE-252 | Unchecked Return Value | Error Handling |
| CWE-390 | Detection of Error Condition Without Action | Error Handling |
| CWE-394 | Unexpected Status Code or Return Value | Error Handling |
| CWE-404 | Improper Resource Shutdown or Release | Resource Management |
| CWE-424 | Improper Protection of Alternate Path | Control Flow |
| CWE-459 | Incomplete Cleanup | Resource Management |
| CWE-476 | NULL Pointer Dereference | Memory Safety |
| CWE-480 | Use of Incorrect Operator | Logic Error |
| CWE-484 | Omitted Break Statement in Switch | Control Flow |
| CWE-562 | Return of Stack Variable Address | Memory Safety |
| CWE-595 | Comparison of Object References Instead of Object Contents | Logic Error |
| CWE-597 | Use of Wrong Operator in String Comparison | Logic Error |
| CWE-662 | Improper Synchronization | Concurrency |
| CWE-665 | Improper Initialization | Initialization |
| CWE-672 | Operation on a Resource after Expiration or Release | Resource Management |
| CWE-681 | Incorrect Conversion between Numeric Types | Type Safety |
| CWE-682 | Incorrect Calculation | Arithmetic |
| CWE-703 | Improper Check or Handling of Exceptional Conditions | Error Handling |
| CWE-704 | Incorrect Type Conversion or Cast | Type Safety |
| CWE-758 | Reliance on Undefined/Unspecified/Implementation-Defined Behavior | Portability |
| CWE-833 | Deadlock | Concurrency |
| CWE-835 | Loop with Unreachable Exit Condition (Infinite Loop) | Control Flow |
| CWE-908 | Use of Uninitialized Resource | Initialization |
| CWE-1045 | Parent Class with Virtual Destructor / Child Class without | OOP Safety |
| CWE-1051 | Initialization with Hard-Coded Network Resource Configuration Data | Configuration |
| CWE-1066 | Missing Serialization Control Element | Serialization |
| CWE-1070 | Serializable Data Element Containing non-Serializable Items | Serialization |
| CWE-1077 | Floating Point Comparison with Incorrect Operator | Arithmetic |
| CWE-1079 | Parent Class without Virtual Destructor Method | OOP Safety |
| CWE-1082 | Class Instance Self Destruction Control Element | OOP Safety |
| CWE-1083 | Data Access from Outside Designated Data Manager Component | Architecture |
| CWE-1087 | Class with Virtual Method without a Virtual Destructor | OOP Safety |
| CWE-1088 | Synchronous Access of Remote Resource without Timeout | Network |
| CWE-1097 | Persistent Storable Data Element without Associated Comparison Control Element | Data Integrity |
| CWE-1098 | Data Element containing Pointer Item without Proper Copy Control Element | Memory Safety |

### Key Child Weaknesses (Selected)
- **CWE-119 children:** CWE-120 (Buffer Overflow), CWE-125 (Out-of-bounds Read), CWE-787 (Out-of-bounds Write), CWE-476, CWE-822, CWE-823, CWE-824, CWE-825
- **CWE-662 children:** CWE-366 (Race Condition), CWE-543 (Unsynchronized Singleton), CWE-567, CWE-667, CWE-764, CWE-820, CWE-821, CWE-1058, CWE-1096
- **CWE-665 children:** CWE-456 (Missing Init), CWE-457 (Uninitialized Variable)
- **CWE-672 children:** CWE-415 (Double Free), CWE-416 (Use After Free)
- **CWE-681 children:** CWE-194, CWE-195, CWE-196, CWE-197 (numeric conversion errors)
- **CWE-682 children:** CWE-131 (Buffer Size Calc), CWE-369 (Divide By Zero)
- **CWE-703 children:** CWE-248 (Uncaught Exception), CWE-391, CWE-392

---

## Dimension 2: Security (ASCSM)

**Definition:** Degree to which an application protects information so that persons/systems have appropriate data access per authorization level. Measures risk of unauthorized penetration.

**Alignment:** Covers CWE/SANS Top 25, OWASP Top 10, and ITU/ISO security weakness framework.

### Parent Weaknesses with CWE Mapping

| CWE | Weakness Name | Attack Category |
|-----|--------------|----------------|
| CWE-22 | Improper Limitation of Pathname to Restricted Directory (Path Traversal) | Injection |
| CWE-77 | Improper Neutralization of Special Elements in Command (Command Injection) | Injection |
| CWE-79 | Improper Neutralization of Input During Web Page Generation (XSS) | Injection |
| CWE-89 | Improper Neutralization of Special Elements in SQL Command (SQL Injection) | Injection |
| CWE-90 | Improper Neutralization of Special Elements in LDAP Query (LDAP Injection) | Injection |
| CWE-91 | XML Injection (Blind XPath Injection) | Injection |
| CWE-99 | Improper Control of Resource Identifiers (Resource Injection) | Injection |
| CWE-119 | Improper Restriction of Operations within Bounds of Memory Buffer | Memory Safety |
| CWE-129 | Improper Validation of Array Index | Memory Safety |
| CWE-134 | Use of Externally Controlled Format String | Injection |
| CWE-252 | Unchecked Return Value | Error Handling |
| CWE-404 | Improper Resource Shutdown or Release | Resource Mgmt |
| CWE-424 | Improper Protection of Alternate Path | Access Control |
| CWE-434 | Unrestricted Upload of File with Dangerous Type | Input Validation |
| CWE-477 | Use of Obsolete Function | Insecure API |
| CWE-480 | Use of Incorrect Operator | Logic Error |
| CWE-502 | Deserialization of Untrusted Data | Input Validation |
| CWE-570 | Expression is Always False | Logic Error |
| CWE-571 | Expression is Always True | Logic Error |
| CWE-606 | Unchecked Input for Loop Condition | Input Validation |
| CWE-611 | Improper Restriction of XML External Entity Reference (XXE) | Injection |
| CWE-643 | Improper Neutralization of Data within XPath Expressions (XPath Injection) | Injection |
| CWE-652 | Improper Neutralization of Data within XQuery Expressions (XQuery Injection) | Injection |
| CWE-662 | Improper Synchronization | Concurrency |
| CWE-665 | Improper Initialization | Initialization |
| CWE-672 | Operation on a Resource after Expiration or Release | Resource Mgmt |
| CWE-681 | Incorrect Conversion between Numeric Types | Type Safety |
| CWE-682 | Incorrect Calculation | Arithmetic |
| CWE-732 | Incorrect Permission Assignment for Critical Resource | Access Control |
| CWE-778 | Insufficient Logging | Audit |
| CWE-783 | Operator Precedence Logic Error | Logic Error |
| CWE-789 | Uncontrolled Memory Allocation | Memory Safety |
| CWE-798 | Use of Hard-coded Credentials | Secrets |
| CWE-835 | Loop with Unreachable Exit Condition (Infinite Loop) | Control Flow |
| CWE-917 | Improper Neutralization in Expression Language Statement (EL Injection) | Injection |
| CWE-1057 | Data Access Operations Outside of Expected Data Manager Component | Architecture |

### Key Child Weaknesses (Selected)
- **CWE-22 children:** CWE-23 (Relative Path Traversal), CWE-36 (Absolute Path Traversal)
- **CWE-77 children:** CWE-78 (OS Command Injection), CWE-88 (Argument Injection)
- **CWE-89 children:** CWE-564 (SQL Injection via Hibernate)
- **CWE-119 children:** CWE-120, CWE-123, CWE-125, CWE-130, CWE-786, CWE-787, CWE-788, CWE-805, CWE-822–825
- **CWE-798 children:** CWE-259 (Hard-coded Password), CWE-321 (Hard-coded Crypto Key)

---

## Dimension 3: Performance Efficiency (ASCPEM)

**Definition:** Characteristics affecting response behavior and resource use under stated conditions. Impacts customer satisfaction, scalability, and infrastructure cost.

**Coverage:** Component-level performance + transaction chain behavior across system tiers.

### Parent Weaknesses with CWE Mapping

| CWE | Weakness Name | Category |
|-----|--------------|----------|
| CWE-404 | Improper Resource Shutdown or Release | Resource Mgmt |
| CWE-424 | Improper Protection of Alternate Path | Architecture |
| CWE-1042 | Static Member Data Element outside of a Singleton Class Element | OOP |
| CWE-1043 | Data Element Aggregating Excessively Large Number of Non-Primitive Elements | Data Design |
| CWE-1046 | Creation of Immutable Text Using String Concatenation | String Ops |
| CWE-1049 | Excessive Data Query Operations in a Large Data Table | Data Access |
| CWE-1050 | Excessive Platform Resource Consumption within a Loop | Loop |
| CWE-1057 | Data Access Operations Outside of Expected Data Manager Component | Architecture |
| CWE-1060 | Excessive Number of Inefficient Server-Side Data Accesses | Data Access |
| CWE-1067 | Excessive Execution of Sequential Searches of Data Resource | Data Access |
| CWE-1072 | Data Resource Access without Use of Connection Pooling | Database |
| CWE-1073 | Non-SQL Invokable Control Element with Excessive Number of Data Resource Accesses | Data Access |
| CWE-1089 | Large Data Table with Excessive Number of Indices | Database |
| CWE-1091 | Use of Object without Invoking Destructor Method | Memory |
| CWE-1094 | Excessive Index Range Scan for a Data Resource | Database |

### Key Child Weaknesses
- **CWE-404 children:** CWE-401 (Memory Leak), CWE-772 (Missing Release after Lifetime), CWE-775 (Missing File Descriptor Release)

---

## Dimension 4: Maintainability (ASCMM)

**Definition:** Effectiveness and efficiency with which a product can be modified by intended maintainers. Encompasses changeability, modularity, understandability, testability, and reusability.

**Coverage:** Code unit level (complexity, duplication) + system/architecture level (layering, coupling).

### All 29 Parent Weaknesses

| CWE | Weakness Name | Category |
|-----|--------------|----------|
| CWE-407 | Algorithmic Complexity | Complexity |
| CWE-478 | Missing Default Case in Switch Statement | Control Flow |
| CWE-480 | Use of Incorrect Operator | Logic Error |
| CWE-484 | Omitted Break Statement in Switch | Control Flow |
| CWE-561 | Dead Code | Code Quality |
| CWE-570 | Expression is Always False | Logic Error |
| CWE-571 | Expression is Always True | Logic Error |
| CWE-783 | Operator Precedence Logic Error | Logic Error |
| CWE-1041 | Use of Redundant Code (Copy-Paste) | Duplication |
| CWE-1045 | Parent Class with Virtual Destructor / Child Class without | OOP |
| CWE-1047 | Modules with Circular Dependencies | Architecture |
| CWE-1048 | Invokable Control Element with Large Number of Outward Calls (Fan-out) | Coupling |
| CWE-1051 | Initialization with Hard-Coded Network Resource Configuration Data | Configuration |
| CWE-1052 | Excessive Use of Hard-Coded Literals in Initialization | Configuration |
| CWE-1054 | Invocation of Control Element at Unnecessarily Deep Horizontal Layer (Layer-skipping) | Architecture |
| CWE-1055 | Multiple Inheritance from Concrete Classes | OOP |
| CWE-1062 | Parent Class Element with References to Child Class | OOP |
| CWE-1064 | Invokable Control Element with Excessive Number of Parameters | Complexity |
| CWE-1074 | Class with Excessively Deep Inheritance | OOP |
| CWE-1075 | Unconditional Control Flow Transfer outside of Switch Block | Control Flow |
| CWE-1079 | Parent Class without Virtual Destructor Method | OOP |
| CWE-1080 | Source Code File with Excessive Number of Lines of Code | Size |
| CWE-1084 | Invokable Control Element with Excessive File or Data Access Operations | Coupling |
| CWE-1085 | Invokable Control Element with Excessive Volume of Commented-out Code | Code Quality |
| CWE-1086 | Class with Excessive Number of Child Classes | OOP |
| CWE-1087 | Class with Virtual Method without a Virtual Destructor | OOP |
| CWE-1090 | Method Containing Access of a Member Element from Another Class | Encapsulation |
| CWE-1095 | Loop Condition Value Update within the Loop | Control Flow |
| CWE-1121 | Excessive McCabe Cyclomatic Complexity | Complexity |

---

## CWE-to-Dimension Cross-Reference

Some CWEs appear in multiple dimensions (indicating cross-cutting risk):

| CWE | Dimensions |
|-----|-----------|
| CWE-404 | Reliability, Security, Performance Efficiency |
| CWE-424 | Reliability, Security, Performance Efficiency |
| CWE-480 | Reliability, Security, Maintainability |
| CWE-484 | Reliability, Maintainability |
| CWE-570 | Security, Maintainability |
| CWE-571 | Security, Maintainability |
| CWE-662 | Reliability, Security |
| CWE-665 | Reliability, Security |
| CWE-672 | Reliability, Security |
| CWE-681 | Reliability, Security |
| CWE-682 | Reliability, Security |
| CWE-835 | Reliability, Security |
| CWE-1045 | Reliability, Maintainability |
| CWE-1051 | Reliability, Maintainability |
| CWE-1057 | Performance Efficiency, Security |
| CWE-1079 | Reliability, Maintainability |
| CWE-1087 | Reliability, Maintainability |
| CWE-783 | Security, Maintainability |

---

## Determinism and Automatability

### Fully Deterministic (Static Analysis — No Judgment Required)
These weaknesses have binary, rule-based detection. A tool either finds a violation or doesn't:

- **Structural metrics with thresholds:** CWE-1121 (cyclomatic complexity > threshold), CWE-1080 (file LOC > threshold), CWE-1064 (parameter count > threshold), CWE-1048 (fan-out > threshold)
- **Literal/syntactic patterns:** CWE-570/571 (always-false/true expressions), CWE-484 (missing break), CWE-478 (missing default case), CWE-1075 (unconditional GOTO outside switch)
- **Memory safety patterns:** CWE-476 (null dereference), CWE-415 (double free), CWE-416 (use after free), CWE-369 (divide by zero)
- **Injection sinks:** CWE-89 (SQL), CWE-78 (OS command), CWE-79 (XSS), CWE-611 (XXE) — deterministic when taint analysis is applied
- **Hard-coded secrets:** CWE-798, CWE-259, CWE-321 — pattern-matchable with regex/AST
- **Duplication:** CWE-1041 (copy-paste code) — clone detection algorithms
- **Dead code:** CWE-561 — control flow graph reachability analysis
- **Missing error handling:** CWE-252, CWE-391, CWE-392 — return value / exception propagation analysis

### Requires Thresholds (Deterministic Once Thresholds Defined)
CISQ specifies "default thresholds" but allows organizations to set their own:

- CWE-1121: Default cyclomatic complexity threshold not specified in standard (typically ≥ 25)
- CWE-1080: Lines of code per file (default threshold not published in open spec; tools typically use 1000–2000)
- CWE-1064: Parameter count (typically > 7–10)
- CWE-407: Algorithmic complexity — detection is heuristic-dependent

### Contextually Deterministic (Architecture-Level, Requires Schema Definition)
These require defining the expected architectural structure first, then violations are automatable:

- CWE-1057 / CWE-1083: "Data access from outside designated data manager" — requires architecture model defining what IS the data manager
- CWE-1054: Layer-skipping call — requires layer hierarchy definition
- CWE-1047: Circular dependencies — deterministic given module/component map

### Judgment-Intensive (Low Automation Confidence Without Deep Context)
- CWE-407 (algorithmic complexity): Requires understanding algorithmic intent
- CWE-758 (undefined behavior reliance): Compiler/platform-specific; may require expert review
- CWE-732 (incorrect permission assignment): Requires domain knowledge of what "correct" permissions are
- CWE-778 (insufficient logging): Requires policy definition of what must be logged

---

## Python Applicability

**Key point:** CISQ was designed primarily for enterprise-tier languages (Java, C/C++, C#, COBOL, SQL). Python support exists but with important carve-outs.

### Applicable to Python (High Confidence)

| CWE | Weakness | Notes |
|-----|---------|-------|
| CWE-89 | SQL Injection | Very common in Python DB code; detectable via taint analysis |
| CWE-78 | OS Command Injection | `subprocess`, `os.system` calls with unsanitized input |
| CWE-77 | Command Injection | Shell metacharacters in Python subprocess calls |
| CWE-79 | Cross-Site Scripting | Flask/Django template rendering without escaping |
| CWE-22 | Path Traversal | File I/O with user-controlled paths |
| CWE-502 | Deserialization | `pickle`, `yaml.load()`, `marshal` with untrusted data |
| CWE-611 | XXE | `lxml`, `ElementTree` with external entity enabled |
| CWE-798 | Hard-coded Credentials | API keys/passwords in source — pattern-matchable |
| CWE-259 | Hard-coded Password | Same as above |
| CWE-321 | Hard-coded Crypto Key | Crypto keys in source literals |
| CWE-252 | Unchecked Return Value | Ignoring return values / unchecked exceptions |
| CWE-703 | Unchecked Exceptions | Bare `except:` clauses, silent error swallowing |
| CWE-248 | Uncaught Exception | Unhandled `Exception` propagation |
| CWE-390 | Error Detected without Action | Catching exception and doing nothing |
| CWE-561 | Dead Code | Unreachable code after `return`/`raise` |
| CWE-570/571 | Always-False/True Expressions | Static evaluation of boolean conditions |
| CWE-1121 | Excessive Cyclomatic Complexity | Fully applicable; tools like radon, flake8-cognitive support it |
| CWE-1080 | Excessive File LOC | Applicable |
| CWE-1041 | Copy-Paste Code | Clone detection works on Python |
| CWE-1047 | Circular Module Dependencies | Python circular imports; detectable |
| CWE-1048 | Excessive Fan-out | Call graph analysis |
| CWE-1064 | Excessive Parameters | AST-detectable |
| CWE-1052 | Hard-Coded Literals | Applicable |
| CWE-1085 | Excessive Commented-out Code | Text pattern detection |
| CWE-478 | Missing Default in Switch | Python `match` statements (3.10+) |
| CWE-1095 | Loop Condition Updated inside Loop | Applicable |
| CWE-404 / CWE-772 | Resource not released | Context manager misuse; file/socket not closed |
| CWE-1088 | Sync remote access without timeout | `requests` calls without timeout param |
| CWE-369 | Divide by Zero | Detectable via symbolic analysis |

### Not Directly Applicable to Python (Memory-Safe Language Carve-outs)

| CWE | Reason Not Applicable |
|-----|----------------------|
| CWE-119 and children (120, 787, etc.) | No manual memory management in Python |
| CWE-415 (Double Free) | Garbage collected — no `free()` |
| CWE-416 (Use After Free) | Garbage collected |
| CWE-476 (NULL Pointer Dereference) | `None` dereference behaves differently; not a memory safety issue |
| CWE-562 (Return Stack Variable Address) | No stack/pointer semantics |
| CWE-681 children (sign/unsigned conversion) | Python integers are arbitrary precision; not applicable |
| CWE-170 (Null Termination) | No C-style null-terminated strings |
| CWE-789 (Uncontrolled Memory Allocation) | GC-managed; may still be risk at extreme scale |
| CWE-1045/1055/1062/1074/1079/1082/1087/1090 | OOP/destructor weaknesses: mostly C++/Java patterns; Python has `__del__` but different semantics |
| CWE-543/1096 (Singleton Synchronization) | Less OOP-pattern-bound in Python; applicable if using singleton pattern explicitly |

### Python-Specific Gaps Not Covered by CISQ
These are Python-relevant security/quality issues that lack CISQ CWE coverage:
- Unsafe use of `eval()` / `exec()` — partially covered by CWE-78 but not explicitly
- `yaml.load()` without `Loader=` argument (covered under CWE-502)
- Missing type annotations (no CISQ measure; mypy/pyright catch these)
- Dynamic attribute access abuse (`getattr` with untrusted input)

---

## PowerShell Applicability

**Key point:** PowerShell is not a primary target language for CISQ/ISO 5055. No dedicated OMG/CISQ standard exists for PowerShell. Applicability is by CWE-analog mapping.

### Applicable to PowerShell (Mapped Analogues)

| CWE | Weakness | PowerShell Context |
|-----|---------|-------------------|
| CWE-78 | OS Command Injection | `Invoke-Expression` with unsanitized input; `cmd /c` with user data |
| CWE-77 | Command Injection | Pipeline injection via untrusted string interpolation |
| CWE-798 | Hard-coded Credentials | `ConvertTo-SecureString` with hardcoded plaintexts; API tokens in scripts |
| CWE-259 | Hard-coded Password | Password literals in scripts |
| CWE-252 | Unchecked Return Value | `$?` not checked after critical commands |
| CWE-390 | Error Detected without Action | Empty `catch {}` blocks |
| CWE-703 | Improper Exception Handling | `Try/Catch` swallowing exceptions silently |
| CWE-732 | Incorrect Permission Assignment | ACLs set incorrectly in scripts |
| CWE-778 | Insufficient Logging | Missing `Write-EventLog` / audit trail |
| CWE-561 | Dead Code | Unreachable code after `return`/`throw` |
| CWE-1121 | Excessive Cyclomatic Complexity | PSScriptAnalyzer measures complexity |
| CWE-1080 | Excessive File LOC | Applicable |
| CWE-1041 | Code Duplication | Applicable |
| CWE-1052 | Hard-Coded Literals | Connection strings, paths hardcoded |
| CWE-1088 | Sync Remote Access without Timeout | `Invoke-WebRequest` without `-TimeoutSec` |
| CWE-606 | Unchecked Loop Input | Input controlling loop bounds without validation |
| CWE-1047 | Circular Dependencies | Module circular import in PowerShell modules |

### Not Directly Applicable to PowerShell

| CWE | Reason |
|-----|--------|
| CWE-119 family | Memory-managed runtime (CLR) |
| CWE-89 (SQL Injection) | Technically possible in PS with DB cmdlets but rare; no standard CISQ rule |
| OOP/class-hierarchy CWEs | PowerShell has classes (5.0+) but very rarely used in patterns triggering these |
| CWE-502 (Deserialization) | PowerShell has `Import-CliXml` / `ConvertFrom-Json` risks but no explicit CISQ mapping |

### PowerShell-Specific Gaps Not Covered by CISQ
- `Invoke-Expression` with user-controlled strings (partial CWE-78 overlap but no explicit rule)
- `ConvertTo-SecureString -AsPlainText -Force` with hardcoded strings (CWE-259 analog)
- Missing `[CmdletBinding()]` / `[Parameter(Mandatory)]` on public functions
- Missing `-WhatIf` / `-Confirm` support for destructive operations
- **PSScriptAnalyzer** is the closest automation tool; its rules overlap ~60% with CISQ Maintainability/Security intent but are not formally CWE-mapped

---

## Standard Lineage and Relationships

```
ISO/IEC 25010 (quality model, 8 characteristics)
    └── ISO/IEC 5055:2021 (automated measures for 4 of 8)
         ≡ OMG ASCQM v1.0 (2019)
              ├── ASCRM (Reliability)
              ├── ASCSM (Security)
              ├── ASCPEM (Performance Efficiency)
              └── ASCMM (Maintainability)
                        └── All CWEs in MITRE CWE Database
                             (ITU standard; funded by DHS/NIST)
```

**ISO 25010 qualities NOT covered by CISQ:**
- Functional Suitability
- Operability / Usability
- Portability
- Compatibility

---

## Implementation Notes

### Tool Conformance
CISQ conformance is assessed at the **parent weakness** level. A tool is conformant on a parent weakness if it detects at least one contributing child weakness. Tools do not need to detect all children.

**Known conformant tools (CAST, Synopsys)** — both contributed to standard development.  
**Partial support** in most SAST tools (Semgrep, SonarQube, CodeQL, Bandit, PSScriptAnalyzer).

### Measurement Formula
```
Weakness Density = Total Violations / kLoC (thousands of lines of code)
Sigma Level = f(density) — six-sigma transformation
```

### Contract/Acceptance Use
ISO 5055 is explicitly designed for use in:
- Requests for Proposals (RFPs)
- Statements of Work (SoW)
- Software acceptance criteria
- Technical debt quantification

---

## Key Sources

| Source | URL |
|--------|-----|
| CISQ Standards Page | https://www.it-cisq.org/standards/code-quality-standards/ |
| ISO 5055 Overview | https://www.it-cisq.org/2021/09/iso-5055-automated-source-code-quality-measures-the-first-standard-of-its-kind/ |
| CWE List for All Dimensions | https://www.it-cisq.org/cisq-files/pdf/cisq-weaknesses-in-ascqm.pdf |
| OMG ASCQM Spec | https://www.omg.org/spec/ASCQM/ |
| MITRE CQE (related effort) | https://cqe.mitre.org/about/index.html |
| CWE Database | https://cwe.mitre.org |

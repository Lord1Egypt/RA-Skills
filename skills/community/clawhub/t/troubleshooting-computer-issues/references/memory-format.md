# Troubleshooting Memory Format Specification

This document details the memory schema, folder structure, ID generation rules, and retrieval mechanisms for the troubleshooting skill.

---

## 1. Directory Structure

Troubleshooting memory is local to the active workspace/project root directory under:
```
.troubleshooting-memory/
├── SOLUTIONS.md       # Successfully resolved issues
├── UNRESOLVED.md      # Unresolved issues and failure modes
└── PATTERNS.md        # Detected recurring problem patterns
```

---

## 2. Document Formats

### 2.1 Solutions Memory (`SOLUTIONS.md`)
Append successfully resolved issues to this file using the following template:

```markdown
## [SOL-YYYYMMDD-XXX] <Brief Issue Title>

**Date**: YYYY-MM-DD
**Difficulty Level**: Simple | Medium | Hard | Extreme
**Platform**: Windows | macOS | Linux
**Category**: Installation | Configuration | Runtime | Network | Permissions | Environment | Other

### Problem Description
<Provide a concise summary of the issue the user encountered and any error messages.>

### Root Cause Analysis
<Detail why the issue occurred (e.g. environment variable missing, port conflict, dependency mismatch).>

### Resolution Steps
1. <Step 1 to resolve>
2. <Step 2 to resolve>

### Key Commands Used
\`\`\`bash
# Diagnostic or fix commands
\`\`\`

### Lessons Learned
- <Lessons for quick detection next time>
- <Common pitfalls to avoid>

---
```

### 2.2 Unresolved Memory (`UNRESOLVED.md`)
Append issues that could not be solved (after exhaustive effort) to this file:

```markdown
## [UNR-YYYYMMDD-XXX] <Brief Issue Title>

**Date**: YYYY-MM-DD
**Difficulty Level**: Hard | Extreme
**Platform**: Windows | macOS | Linux
**Category**: Installation | Configuration | Runtime | Network | Permissions | Environment | Other
**Attempts**: <Number of attempts / cycles tried>

### Problem Description
<Provide a concise summary of the issue and error messages.>

### Attempted Solutions & Failure Results
1. **Approach A**: <What was tried> -> <Why it failed/result>
2. **Approach B**: <What was tried> -> <Why it failed/result>

### Reason for Unresolution
<Explicit details on why this could not be resolved (e.g. library bug, OS limitation, missing credentials).>

### Next Steps & Recommendations
- <Potential workarounds or future direction>
- <Official support channels to contact>

---
```

### 2.3 Patterns Memory (`PATTERNS.md`)
When a specific category of issue or error message occurs **3 or more times**, extract it into `PATTERNS.md` for rapid identification:

```markdown
## [PAT-XXX] <Pattern Name>

**Category**: Network | Port Conflict | Dependency | etc.
**Trigger Signals**: <Error keywords or symptoms>
**Occurrence Count**: <N>
**Related IDs**: SOL-YYYYMMDD-001, SOL-YYYYMMDD-004

### Root Pattern Cause
<General explanation of this pattern>

### Quick Fix Directive
<Immediate steps to resolve this pattern>
```

---

## 3. ID Generation Rules
- **Format**: `TYPE-YYYYMMDD-XXX`
  - `TYPE`: `SOL` for solved issues, `UNR` for unresolved issues, `PAT` for patterns (without date, e.g., `PAT-001`).
  - `YYYYMMDD`: Current date.
  - `XXX`: Sequential three-digit hex/number starting from `001` per day (e.g. `SOL-20260703-001`).

---

## 4. Search and Retrieval Guidelines
Before starting any diagnosis, the agent must check if `.troubleshooting-memory/` has relevant entries.

### PowerShell Search Examples
```powershell
# Search for keyword (e.g. "EADDRINUSE") in memory
Select-String -Path ".troubleshooting-memory\*.md" -Pattern "EADDRINUSE"

# List all port conflict solutions
Select-String -Path ".troubleshooting-memory\SOLUTIONS.md" -Pattern "Category: Network" -Context 0, 5
```

### Bash Search Examples
```bash
# Search for keyword in memory
grep -rn "EADDRINUSE" .troubleshooting-memory/

# List all categories of solutions
grep -i "Category:" .troubleshooting-memory/SOLUTIONS.md
```

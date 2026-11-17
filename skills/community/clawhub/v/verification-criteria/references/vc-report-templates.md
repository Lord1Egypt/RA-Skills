# VC Report Templates

## Quality Audit Report (Workflow B)

```
## VC Quality Audit Report

**Source**: [filename]
**Total VCs reviewed**: N
**Average SMARTR-OC score**: X.X/8

### SMARTR-OC Score Distribution
- 8/8 (Excellent): N
- 6-7/8 (Acceptable): N
- <6/8 (Needs Revision): N

### CK Pre-Review Summary
- ✅ Ready for Peer Review: N
- ⚠️ Conditional Pass (Minor items only): N
- ❌ Needs Revision (Critical items): N

### Per-VC Results（仅列 <8/8 或非 Ready 的 VC）

| VC ID | SMARTR-OC | Failed Attributes | CK Critical ❌ | CK Minor ❌ | Disposition | Recommendation |
|-------|-----------|-------------------|---------------|------------|-------------|----------------|
| VC-REQ-001 | 7/8 | A | — | CK-06 | ⚠️ Conditional | Sample size N=10 → increase to N≥30 for statistical significance |
| VC-REQ-003 | 4/8 | M, R, O | CK-03 | CK-02 | ❌ Needs Revision | Replace Test with Analysis (Kalman filter accuracy); add numeric threshold; replace "good" with ≤5%; fix VC ID naming |

**Fully Compliant**: N 条 VC 全部 8/8 ✅ + 全部 CK ✅（不逐条列出）。

### Top Issues
1. [Most common issue across SMARTR-OC and CK results]
2. [Second most common]
3. [Third most common]
```

## Coverage Audit Report (Workflow C)

```
## VC Coverage Audit Report

**Requirements source**: [filename]
**VCs source**: [filename]

### Summary
- Total requirements: N
- Covered (≥1 VC): N (X%)
- Uncovered (0 VCs): N (X%)
- Total VCs: N
- Orphan VCs (no valid link): N

### Uncovered Requirements
| Req ID | Description |
|--------|-------------|
| REQ-002 | [description] |
| ... | ... |

### Orphan VCs
| VC ID | Linked Req (invalid) | Issue |
|-------|---------------------|-------|
| VC-UNKNOWN-001 | REQ-999 | Requirement not found |
| VC-REQ-005-orphan | (none) | No linked requirement |

### Coverage Matrix
[table from C.4]
```

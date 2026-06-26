# Skill Fusion Workflow

Deep fusion of multiple skills into a new, unified skill.

## When to Use

Only when:
- Existing skills partially match task requirements
- Combining skills creates new value
- Modification/combination is more efficient than orchestration

## Prerequisites

- Phase 3: Deep Inspection completed
- Source skills identified and analyzed
- Fusion approach approved by user

---

## Step 1: Design Fusion Spec

Output `${OUTPUT_DIR}/03-fusion-spec.md`:

```markdown
# Fusion Specification

## Source Skills

| Skill | Path | Key Capability |
|------|-----|----------------|
| <skill-a> | ./skills/<skill-a> | <capability> |
| <skill-b> | ./skills/<skill-b> | <capability> |

## Task Context

- Original task: <user's task>
- Why fusion: <reason fusion is needed>
- Gap in existing skills: <what's missing>

## Fusion Goal

What the new fused skill should accomplish:
- <goal-1>
- <goal-2>

## Fusion Points

How capabilities combine:
- <skill-a> contributes: <what it provides>
- <skill-b> contributes: <what it provides>
- Combined effect: <emergent capability>

## New Skill Spec

- **Name**: <fused-skill-name>
- **Description**: <what this fused skill does>
- **Structure**:
  ```
  fused-skill-name/
  ├── SKILL.md
  ├── scripts/
  │   └── <needed-scripts>
  └── references/
      └── <needed-references>
  ```

## Implementation Notes

<Any additional notes for skill-creator>
```

See template: [templates/03b-fusion-spec.md](templates/03b-fusion-spec.md)

## Step 2: Invoke skill-creator

Pass the fusion spec as context:

```
Use skill-creator to create a fused skill based on:
- Fusion spec: ${OUTPUT_DIR}/03-fusion-spec.md
- Source skills: ./skills/<skill-a>, ./skills/<skill-b>
```

## Step 3: Audit Fused Skill

Run security audit on the newly created skill:

```bash
python scripts/audit_skill.py --skill ./skills/<fused-skill-name> --output ${OUTPUT_DIR}/03-fusion-audit.md
```

**Results:**
- 🟢 **PASS**: Fused skill is safe → Skill ready for use
- 🔴 **REJECT**: High-risk patterns detected → Return to Step 1

---

## Output Files

| File | Description |
|------|-------------|
| `03-fusion-spec.md` | Fusion design specification |
| `03-fusion-audit.md` | Security audit of fused skill |

## Flow Summary

```
Step 1: Design Fusion Spec
    ↓
Step 2: Invoke skill-creator
    ↓
Step 3: Audit Fused Skill
    ├── PASS → Return to main workflow (Phase 4)
    └── REJECT → Return to Step 1
```

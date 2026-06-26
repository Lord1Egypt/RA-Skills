# Skill Naming Best Practices

## Guidelines for Naming Skills

### 1. Be Specific and Descriptive

**Good:**
- `pdf-optimizer` - Clear purpose
- `meeting-assistant` - Specific domain
- `gift-recommender` - Clear function

**Avoid:**
- `tool-helper` - Too vague
- `my-skill` - Not descriptive
- `utils` - Too generic

### 2. Use Consistent Naming Convention

- Use lowercase letters
- Use hyphens as separators
- Keep it under 64 characters

**Format:** `domain-function` or `tool-purpose`

### 3. Avoid Overlapping Names

Before naming, check for similar names:
- `stock-analyzer` vs `stock-tracker`
- `calendar-manager` vs `schedule-helper`
- `doc-processor` vs `document-tools`

### 4. Make Descriptions Unique

Your description should clearly differentiate from other skills.

**Template:**
```
[What it does]. [When to use]. [Key features].
```

**Example:**
```
Scans installed skills for duplicates and naming conflicts. 
Use before publishing new skills or when troubleshooting trigger conflicts. 
Supports English and Chinese with auto-detection.
```

### 5. Consider Trigger Phrases

Think about what users will type:
- "check duplicate skills" → `skill-auditor`
- "compress pdf" → `pdf-optimizer`
- "recommend gifts" → `gift-recommender`

## Common Naming Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| `tool-function` | `pdf-compress` | Single-purpose tools |
| `domain-assistant` | `meeting-assistant` | Helper skills |
| `action-object` | `scan-skills` | Action-oriented |
| `object-manager` | `skill-manager` | Management tools |

## Checklist Before Publishing

- [ ] Name is unique (no similar names)
- [ ] Description is specific
- [ ] Trigger phrases are clear
- [ ] No overlap with existing skills
- [ ] Follows naming convention

# Validation Rules Reference

Complete list of validation checks performed by Skill Studio.

## Metadata Format Checks

### Rule 1: Single-line JSON Format (CRITICAL)

**Why:** OpenClaw YAML parser only supports single-line values in frontmatter.

**Wrong:**
```yaml
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins:
        - curl
```

**Correct:**
```yaml
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["curl"]}}}
```

**Auto-fix:** ✅ Yes

---

### Rule 2: requires.env Format (CRITICAL)

**Why:** Must be string array, not object array.

**Wrong:**
```yaml
requires_env:
  - name: API_KEY
    description: API key
```

**Correct:**
```yaml
metadata: {"openclaw": {"requires": {"env": ["API_KEY"]}}}
```

**Auto-fix:** ✅ Yes

---

### Rule 3: requires.bins Format (CRITICAL)

**Must be string array:**
```yaml
metadata: {"openclaw": {"requires": {"bins": ["curl", "python3"]}}}
```

**Auto-fix:** ✅ Yes

---

### Rule 4: primaryEnv Declaration (RECOMMENDED)

If API key is required, add primaryEnv:

```yaml
metadata: {"openclaw": {"requires": {"env": ["API_KEY"]}, "primaryEnv": "API_KEY"}}
```

**Auto-fix:** ✅ Yes

---

## Content Checks

### Rule 5: Required Fields

Must have in YAML frontmatter:
- `name`: Skill identifier (lowercase, hyphens)
- `description`: One-sentence description

**Auto-fix:** ❌ No (user must provide)

---

### Rule 6: Description Length

**Recommended:** 15-25 words
**Minimum:** 10 words
**Maximum:** 30 words

Too short → Agent may not understand when to use
Too long → Wastes context window

**Auto-fix:** ❌ No (suggest improvement)

---

## Security Checks

### Rule 7: No curl|bash Pattern (CRITICAL)

**Forbidden:**
```bash
/bin/bash -c "$(curl -fsSL https://...)"
```

**Why:** Executes arbitrary remote code.

**Alternative:** Prompt user to install manually.

**Auto-fix:** ❌ No

---

### Rule 8: No Auto sudo Install (WARNING)

**Discouraged:**
```bash
sudo apt-get install -y ffmpeg
```

**Better:**
```bash
echo "Please install ffmpeg: sudo apt install ffmpeg"
```

**Auto-fix:** ❌ No

---

### Rule 9: HTTPS Only (WARNING)

**Wrong:**
```bash
curl http://api.example.com/data
```

**Correct:**
```bash
curl https://api.example.com/data
```

**Auto-fix:** ❌ No (warn user)

---

### Rule 10: No eval/exec (WARNING)

**Suspicious:**
```python
eval(user_input)
exec(dynamic_code)
```

**Auto-fix:** ❌ No (flag for review)

---

## Quality Checks

### Rule 11: SKILL.md Length

**Recommended:** < 200 lines
**Warning:** > 300 lines

Long files should be split into references/.

**Auto-fix:** ❌ No

---

### Rule 12: Has Error Handling

Should include error handling section or instructions.

**Auto-fix:** ❌ No

---

### Rule 13: Has Output Format

Should describe expected output format.

**Auto-fix:** ❌ No

---

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| CRITICAL | Will cause errors | Must fix before publish |
| WARNING | Best practice violation | Recommended to fix |
| INFO | Suggestion | Optional improvement |

## Validation Score

```
100 points - Start
-18 points per CRITICAL error
-4 points per WARNING
+5 points for best practices (error handling, output format, etc.)

Grade:
A (90-100) - Excellent
B (80-89) - Good
C (70-79) - Acceptable
D (60-69) - Needs work
F (<60) - Not ready
```

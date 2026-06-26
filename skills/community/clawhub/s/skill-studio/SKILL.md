---
name: skill-studio
description: Create, validate, and publish OpenClaw Skills through conversation. Use when user wants to create a new skill, build a ClawHub plugin, generate SKILL.md, or publish an agent skill. Supports guided mode for beginners and expert mode for developers. Includes automatic metadata validation and one-click fix.
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🎨", "requires": {"bins": ["curl", "python3", "npm"], "env": ["OPENCLAW_WORKSPACE"]}, "primaryEnv": "OPENCLAW_WORKSPACE"}}
---

# Skill Studio

Create, validate, and publish OpenClaw Skills through conversation.

## Features

- 🎯 **Dual Modes**: Guided (beginners) / Expert (developers)
- ✅ **Auto Validation**: Metadata format, dependencies, security
- 🔧 **Auto Fix**: One-click fix all issues
- 📤 **Publish Guide**: Step-by-step ClawHub publishing
- 🌍 **International**: Works for any language/country

## Trigger Conditions

- "Create a new skill" / "创建一个skill"
- "I want to build a ClawHub skill"
- "Help me make a plugin for OpenClaw"
- "生成SKILL.md"
- "Publish my skill" / "发布skill"
- "Validate my skill" / "检查skill"
- "Fix my skill metadata" / "修复元数据"

---

## Step 0: Mode Selection

When user wants to create a skill, first ask about mode:

```
Welcome to Skill Studio! 🎨

How would you like to create your skill?

1️⃣ **Guided Mode** (Recommended for beginners)
   - I'll ask you questions step by step
   - No prior knowledge needed
   - Takes 3-5 minutes

2️⃣ **Expert Mode** (For experienced developers)
   - Provide all details at once
   - Faster workflow
   - You know the SKILL.md format

Which mode? (1/2 or "guided"/"expert")
```

---

## Step 1: Collect Requirements

### Guided Mode

Ask these questions one by one:

```
📍 Step 1/6: Basic Information

Q1: What should this skill be called? (skill name, lowercase with hyphens)
    Example: weather-forecast, pdf-merger, api-monitor

Q2: Describe what this skill does in one sentence.
    Example: "Query weather forecast for any location"

Q3: What phrases should trigger this skill?
    Example: "check weather", "what's the weather", "天气怎么样"

Q4: What emoji represents this skill?
    Example: 🌤️ for weather, 📄 for documents
```

```
📍 Step 2/6: Technical Requirements

Q5: Does this skill call any external APIs?
    If yes, which one? (e.g., "OpenWeather API", "和风天气API")

Q6: What environment variables are needed? (API keys, tokens)
    Format: VARIABLE_NAME - description
    Example: WEATHER_API_KEY - API key from openweathermap.org

Q7: What command-line tools are required?
    Common options: curl, python3, ffmpeg, node
    (I'll add curl automatically if API calls are needed)
```

```
📍 Step 3/6: Additional Features

Q8: Do you need a references/ folder for detailed docs?
    (Useful for complex skills with multiple features)

Q9: Any specific output format requirements?
    Example: "Output as JSON", "Save to file", "Return markdown"

Q10: What license? (MIT-0 recommended for ClawHub)
     Options: MIT-0, MIT, Apache-2.0
```

### Expert Mode

User provides everything at once:

```
Please provide all details:

**Required:**
- name: [skill-name]
- description: [one sentence]
- triggers: [comma-separated phrases]

**Optional:**
- env_vars: [VAR_NAME - description]
- bins: [required commands]
- references: [yes/no]
- license: [MIT-0/MIT/Apache-2.0]
- additional: [any other requirements]
```

Parse user input and extract all fields.

---

## Step 2: Generate SKILL.md

Based on collected requirements, generate a complete SKILL.md.

### Generation Template

```python
# Generate SKILL.md content based on requirements

METADATA_TEMPLATE = """---
name: {name}
description: {description}
version: 1.0.0
license: {license}
metadata: {{"openclaw": {{"emoji": "{emoji}", "requires": {{"bins": {bins}, "env": {env}}}, "primaryEnv": "{primary_env}"}}}}
---"""

BODY_TEMPLATE = """
# {title}

{detailed_description}

## Trigger Conditions

{triggers_list}

---

## Step 1: Check Dependencies

```bash
{dependency_check}
```

---

## Step 2: Main Functionality

{main_content}

---

## Error Handling

{error_handling}

---

## Output Format

{output_format}

---

## Notes

- All data processed locally or via specified APIs
- No unauthorized data transmission
- Follow OpenClaw security best practices
"""
```

### Generation Rules

```
1. Metadata MUST be single-line JSON format
2. requires.env MUST be string array: ["VAR1", "VAR2"]
3. requires.bins MUST be string array: ["curl", "python3"]
4. description should be 15-25 words
5. Add primaryEnv if API key is required
6. Include dependency check code
7. Include error handling section
8. Include output format section
```

---

## Step 3: Auto Validation

After generating SKILL.md, run validation automatically.

### Validation Script

```bash
SKILL_FILE="${OPENCLAW_WORKSPACE:-$PWD}/skill-studio/$SKILL_NAME/SKILL.md"

python3 << 'PYEOF'
import re
import json
import sys

def validate_skill(filepath):
    errors = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        errors.append("❌ Missing YAML frontmatter")
        return errors, warnings
    
    yaml_content = yaml_match.group(1)
    
    # Check 1: Metadata format (must be single-line JSON)
    metadata_match = re.search(r'metadata:\s*(\{.*\})', yaml_content)
    if not metadata_match:
        errors.append("❌ Metadata must be single-line JSON format")
        errors.append("   Wrong: metadata:\\n  openclaw:\\n    requires:...")
        errors.append("   Right: metadata: {\"openclaw\": {...}}")
    else:
        try:
            metadata = json.loads(metadata_match.group(1))
            # Check requires.env format
            if 'openclaw' in metadata:
                oc = metadata['openclaw']
                if 'requires' in oc:
                    req = oc['requires']
                    if 'env' in req:
                        if not isinstance(req['env'], list):
                            errors.append("❌ requires.env must be array: [\"VAR1\", \"VAR2\"]")
                        elif len(req['env']) > 0:
                            for env in req['env']:
                                if not isinstance(env, str):
                                    errors.append(f"❌ requires.env items must be strings, got: {env}")
        except json.JSONDecodeError:
            errors.append("❌ Metadata JSON is invalid")
    
    # Check 2: Required fields
    if 'name:' not in yaml_content:
        errors.append("❌ Missing 'name' field")
    if 'description:' not in yaml_content:
        errors.append("❌ Missing 'description' field")
    if 'version:' not in yaml_content:
        warnings.append("⚠️ Missing 'version' field (recommended)")
    
    # Check 3: Description length
    desc_match = re.search(r'description:\s*(.+)', yaml_content)
    if desc_match:
        desc = desc_match.group(1).strip().strip('"').strip("'")
        word_count = len(desc.split())
        if word_count < 10:
            warnings.append(f"⚠️ Description too short ({word_count} words, recommend 15-25)")
        elif word_count > 30:
            warnings.append(f"⚠️ Description too long ({word_count} words, recommend 15-25)")
    
    # Check 4: Dangerous patterns
    if 'curl -fsSL' in content and '|' in content and 'bash' in content:
        errors.append("❌ Dangerous: curl|bash pattern detected")
    if re.search(r'sudo\s+(apt|yum|dnf)\s+install', content):
        warnings.append("⚠️ Contains sudo install (should prompt user manually)")
    if 'eval(' in content or 'exec(' in content:
        warnings.append("⚠️ Contains eval/exec (potential security risk)")
    
    # Check 5: HTTP endpoints (should be HTTPS)
    http_matches = re.findall(r'http://[^\s"\'\)]+', content)
    if http_matches:
        warnings.append(f"⚠️ Found HTTP endpoints (should use HTTPS): {http_matches[0]}")
    
    # Check 6: SKILL.md length
    lines = content.split('\n')
    if len(lines) > 300:
        warnings.append(f"⚠️ SKILL.md is long ({len(lines)} lines, consider splitting)")
    
    return errors, warnings

errors, warnings = validate_skill(sys.argv[1] if len(sys.argv) > 1 else 'SKILL.md')

print("\n🔍 Validation Results\n" + "="*40)

if errors:
    print("\n❌ ERRORS (must fix):")
    for e in errors:
        print(f"  {e}")

if warnings:
    print("\n⚠️ WARNINGS (recommended to fix):")
    for w in warnings:
        print(f"  {w}")

if not errors and not warnings:
    print("\n✅ All checks passed! SKILL.md is ready.")

print("\n" + "="*40)
print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
PYEOF
```

---

## Step 4: Auto Fix

If validation finds issues, offer automatic fixes.

### Fixable Issues

```
1. Multi-line YAML → Single-line JSON
   Fix: Convert metadata format automatically

2. requires_env (wrong) → requires.env (correct)
   Fix: Rename field

3. Object array → String array
   Fix: Convert [{"name": "VAR"}] → ["VAR"]

4. Missing primaryEnv
   Fix: Add if env vars exist

5. HTTP endpoints
   Fix: Warn user to change to HTTPS

6. Description length
   Fix: Suggest improvements (user must approve)
```

### Auto Fix Script

```bash
python3 << 'PYEOF'
import re
import json

def fix_metadata(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_applied = []
    
    # Fix 1: Convert multi-line YAML metadata to single-line JSON
    # Pattern: metadata:\n  openclaw:\n    ...
    multi_line_pattern = r'(metadata:)\n(\s+openclaw:\n(?:\s+\w+:.*\n)+)'
    match = re.search(multi_line_pattern, content)
    
    if match:
        # Parse the multi-line YAML structure
        yaml_block = match.group(2)
        
        # Extract values using regex
        emoji = re.search(r'emoji:\s*["\']?([^"\'\n]+)["\']?', yaml_block)
        emoji = emoji.group(1) if emoji else "🔧"
        
        bins = re.findall(r'-\s+(\w+)', re.search(r'bins:\s*\n((?:\s+-\s+\w+\n)+)', yaml_block).group(1) if re.search(r'bins:\s*\n((?:\s+-\s+\w+\n)+)', yaml_block) else "")
        
        # Handle requires_env (wrong format)
        env_match = re.search(r'requires_env:\s*\n\s*-\s*name:\s*(\w+)', yaml_block)
        env_vars = [env_match.group(1)] if env_match else []
        
        primary_env = env_vars[0] if env_vars else ""
        
        # Build JSON metadata
        metadata_json = {
            "openclaw": {
                "emoji": emoji,
                "requires": {
                    "bins": bins,
                    "env": env_vars
                }
            }
        }
        if primary_env:
            metadata_json["openclaw"]["primaryEnv"] = primary_env
        
        # Replace in content
        new_metadata = f'metadata: {json.dumps(metadata_json)}'
        content = content[:match.start()] + new_metadata + content[match.end():]
        fixes_applied.append("✅ Converted multi-line YAML to single-line JSON")
        fixes_applied.append("✅ Fixed requires_env → requires.env")
    
    # Write fixed content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixes_applied

# Run fixes
import sys
filepath = sys.argv[1] if len(sys.argv) > 1 else 'SKILL.md'
fixes = fix_metadata(filepath)

if fixes:
    print("\n🔧 Auto Fixes Applied:")
    for fix in fixes:
        print(f"  {fix}")
else:
    print("\n✅ No fixes needed")
PYEOF
```

---

## Step 5: Preview and Confirm

Show user the generated SKILL.md:

```
✅ SKILL.md Generated Successfully!

📁 Location: ~/skill-studio/{skill-name}/SKILL.md

📋 Preview:
───────────────────────────────────────
[YAML frontmatter preview]

[First 50 lines of content]
───────────────────────────────────────

📊 Validation:
✅ Metadata format: Correct
✅ Dependencies: Declared
✅ Security: No issues

What would you like to do?
1. 📝 Edit (tell me what to change)
2. 📤 Publish to ClawHub
3. 💾 Save only (publish later)
```

---

## Step 6: Publish Guide

### Environment Check

First, check if publishing is possible:

```bash
# Check if clawhub CLI is installed
if ! command -v clawhub &> /dev/null; then
  echo "❌ clawhub CLI not installed"
  echo ""
  echo "Install with:"
  echo "  npm install -g clawhub"
  exit 1
fi

# Check if this is a server environment (no browser)
if [[ "$DISPLAY" == "" ]] && [[ "$OSTYPE" == "linux-gnu"* ]]; then
  echo "⚠️ Server environment detected (no display/browser)"
  echo ""
  echo "Publishing to ClawHub requires browser-based GitHub authentication."
  echo "This feature is not available on headless servers."
  echo ""
  echo "Options:"
  echo "1. Use 'clawhub auth login --token YOUR_TOKEN' with a pre-generated token"
  echo "2. Publish from a local machine with browser access"
  echo "3. Transfer the skill directory to a machine with GUI"
  echo ""
  echo "Your skill is ready at: $SKILL_DIR"
  echo "You can publish it from another machine."
  exit 1
fi

# Check if user is logged in
if ! clawhub whoami &> /dev/null; then
  echo "❌ Not logged in to ClawHub"
  echo ""
  echo "Login with:"
  echo "  clawhub login"
  echo ""
  echo "This will open a browser for GitHub authentication."
  exit 1
fi

echo "✅ Ready to publish!"
```

### Publish Command

```bash
# Generate and display publish command
SKILL_DIR="${OPENCLAW_WORKSPACE:-$PWD}/skill-studio/$SKILL_NAME"

echo ""
echo "📤 Publish Command:"
echo ""
echo "clawhub publish $SKILL_DIR \\"
echo "  --slug $SKILL_NAME \\"
echo "  --version 1.0.0 \\"
echo "  --changelog \"Initial release: $SKILL_DESCRIPTION\""
echo ""
echo "Run this command to publish your skill to ClawHub!"
```

### Post-publish

```
🎉 Congratulations!

Your skill has been published to ClawHub!

📦 Skill: {skill-name}
🔗 URL: https://clawhub.ai/@username/{skill-name}

Users can install it with:
  clawhub install {skill-name}

Share your skill with the community! 🚀
```

---

## Validation Rules Reference

See `references/validation-rules.md` for complete validation rules.

### Quick Summary

| Check | Severity | Auto-fix |
|-------|----------|----------|
| Metadata not single-line JSON | Error | ✅ Yes |
| requires.env wrong format | Error | ✅ Yes |
| Missing name/description | Error | ❌ No |
| Description length | Warning | ❌ No |
| curl\|bash pattern | Error | ❌ No |
| sudo auto-install | Warning | ❌ No |
| HTTP endpoints | Warning | ❌ No |
| SKILL.md too long | Warning | ❌ No |

---

## Error Handling

```
User cancels → Save progress, allow resume later
Generation fails → Show error, suggest manual creation
Validation fails → Show issues, offer auto-fix
Publish fails → Show clawhub error, suggest solutions
```

---

## Notes

- Generated skills follow OpenClaw best practices
- Metadata always in single-line JSON format
- Security patterns automatically checked
- Supports all languages (Chinese, English, etc.)
- Works with any messaging platform (Telegram, Discord, etc.)

## Limitations

### Server/Headless Environments

Skill Studio can **create and validate** skills on any environment, but **publishing to ClawHub** requires:

1. **Browser access** for GitHub OAuth authentication
2. **Display/GUI** for the login flow

**Not supported:**
- Headless servers without display
- Docker containers without browser
- SSH-only remote machines

**Workaround:**
1. Create and validate skills on the server
2. Transfer the skill directory to a local machine
3. Publish from the local machine with browser access

Alternative: Use `clawhub auth login --token TOKEN` if you have a pre-generated token from ClawHub dashboard.

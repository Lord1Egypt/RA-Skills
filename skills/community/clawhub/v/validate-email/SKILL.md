---
name: Email Validator
description: >
  Validate email addresses with format checking and risk scoring. Use when users need
  to verify email format, check disposable emails, or validate bulk email lists. Handles
  RFC 5322 compliance, domain extraction, and risk assessment. Runs locally with no
  external API calls.
---

# Email Validator

**Local skill by [Claw0x](https://claw0x.com)** — runs entirely in your OpenClaw agent.

Validate email addresses for format correctness and assess risk level. Pure local logic processing with no external API calls.

> **Runs locally.** No external API calls, no API key required. Complete privacy.

## Prerequisites

**None.** Just install and use.

## Quick Reference

| When This Happens | Do This | What You Get |
|-------------------|---------|--------------|
| User provides email | Validate format | Valid/invalid + risk score |
| Check disposable email | Run validation | Disposable domain detection |
| Bulk email validation | Loop through list | Format check for each |
| Pre-filter signups | Validate before save | Risk score assessment |

## 5-Minute Quickstart

### Step 1: Install (30 seconds)
```bash
openclaw skills install email-validator
```

### Step 2: Use (1 minute)
```typescript
const result = await agent.run('email-validator', {
  email: 'user@example.com'
});

console.log(result.valid); // true/false
console.log(result.risk_score); // 10-100
```

### Step 3: Get Result (instant)
```json
{
  "valid": true,
  "email": "user@example.com",
  "checks": {
    "format_valid": true,
    "domain": "example.com",
    "local_part": "user",
    "is_disposable": false
  },
  "risk_score": 10,
  "suggestion": null
}
```

## How It Works — Under the Hood

**100% local processing. Zero external API calls. Complete privacy.**

This skill runs entirely in your agent's environment using pure TypeScript logic. All validation happens locally using:
- Regular expressions for format checking
- String operations for domain extraction
- Array lookups against built-in domain lists
- Simple arithmetic for risk scoring

### Step 1: Local Format Validation (RFC 5322)

Uses a regex pattern to check email structure locally:
- **Local part** (before `@`): 1-64 characters, alphanumeric, dots, hyphens, underscores, plus signs
- **Domain part** (after `@`): Valid hostname with TLD
- **Total length**: 3-254 characters

**No network calls. Pure string matching.**

### Step 2: Local Domain Analysis

Compares the extracted domain against built-in lists (stored in code):
- **Disposable domains list**: 10+ known providers (mailinator.com, guerrillamail.com, etc.)
- **Free providers list**: 8+ common providers (gmail.com, yahoo.com, etc.)
- **Corporate domains**: Anything not in the above lists

**No DNS lookups. Pure array lookups.**

### Step 3: Local Risk Scoring

Calculates risk score using simple arithmetic:

| Factor | Risk Impact |
|--------|-------------|
| Invalid format | +90 (instant high risk) |
| Disposable domain | +70 |
| All-number local part | +30 |
| Very short local part (<3 chars) | +20 |
| Free email provider | +10 |
| Valid corporate domain | +10 (baseline) |

**No external scoring API. Pure math.**

Lower score = safer email.

### What This Skill Does NOT Do

- **No SMTP verification**: Doesn't connect to mail server
- **No DNS MX lookup**: Doesn't verify mail exchange records
- **No deliverability check**: Can't predict if email will bounce

This is by design. The skill is optimized for speed, determinism, and zero external dependencies.

## Real-World Use Cases

### Scenario 1: Signup Form Validation
**Problem**: Filter out fake emails during registration
**Solution**: Validate format and check disposable domains
**Example**:
```typescript
const result = await agent.run('email-validator', {
  email: 'test@mailinator.com'
});

if (result.risk_score > 70) {
  console.log('Disposable email detected');
}
```

### Scenario 2: Bulk Email List Cleaning
**Problem**: Clean email list before campaign
**Solution**: Validate all emails and remove invalid ones
**Example**:
```typescript
const emails = ['user1@example.com', 'invalid@', 'user2@gmail.com'];
const results = await Promise.all(
  emails.map(email => agent.run('email-validator', { email }))
);

const validEmails = results
  .filter(r => r.valid && r.risk_score < 50)
  .map(r => r.email);
```

### Scenario 3: B2B Lead Qualification
**Problem**: Prioritize corporate emails over free providers
**Solution**: Use risk score to rank leads
**Example**:
```typescript
const result = await agent.run('email-validator', {
  email: 'ceo@company.com'
});

// Corporate domain = low risk score (10-20)
// Free provider = medium risk (20-30)
// Disposable = high risk (80-100)
```

## Integration Recipes

### OpenClaw Agent
```typescript
import { Claw0xClient } from '@claw0x/sdk';

const claw0x = new Claw0xClient(process.env.CLAW0X_API_KEY);

agent.onUserInput(async (input) => {
  if (input.includes('@')) {
    const result = await claw0x.call('email-validator', {
      email: input
    });
    
    if (!result.valid) {
      return 'Invalid email format';
    }
    
    if (result.checks.is_disposable) {
      return 'Disposable email not allowed';
    }
  }
});
```

### LangChain Agent
```python
from claw0x import Claw0xClient

client = Claw0xClient(api_key=os.environ['CLAW0X_API_KEY'])

def validate_email(email: str) -> dict:
    result = client.call('email-validator', {'email': email})
    return result

# Use in chain
email = "user@example.com"
validation = validate_email(email)
if validation['valid']:
    print(f"Email is valid with risk score: {validation['risk_score']}")
```

### Custom Agent
```javascript
const response = await fetch('https://api.claw0x.com/v1/call', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.CLAW0X_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    skill: 'email-validator',
    input: { email: 'test@example.com' }
  })
});

const result = await response.json();
console.log(result);
```

## Input Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | yes | Email address to validate (3-254 chars) |

## Output Schema

```typescript
{
  valid: boolean;              // Whether email format is valid
  email: string;               // Normalized (lowercased) email
  checks: {
    format_valid: boolean;     // RFC format check result
    domain: string;            // Extracted domain
    local_part: string;        // Extracted local part (before @)
    is_disposable: boolean;    // Whether domain is disposable
  };
  risk_score: number;          // Risk score (10 = low, 90 = high)
  suggestion: string | null;   // Suggestion if invalid
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing required field: email` | No email provided | Provide email in input |
| `email must be between 3 and 254 characters` | Email too short/long | Check email length |

## About Claw0x

This skill is provided by [Claw0x](https://claw0x.com), the native skills layer for AI agents.

**Cloud version available**: For users who need centralized analytics, a cloud version is available at [claw0x.com/skills/validate-email](https://claw0x.com/skills/validate-email).

**Explore more skills**: [claw0x.com/skills](https://claw0x.com/skills)

**GitHub**: [github.com/kennyzir/validate-email](https://github.com/kennyzir/validate-email)

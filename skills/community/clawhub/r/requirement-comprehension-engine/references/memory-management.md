# Memory Management Reference

## Tiered Memory System

### Tier 1: Public / Visible (No encryption)

Store in `memory/tier1-public/` or directly in daily notes.

**Content allowed:**
- Skill usage statistics
- Generic workflow patterns
- Common user request categories
- Aggregated/statistical behavioral data (no personal identification)

**Example:**
```json
{
  "skill_stats": {
    "morning-news-daily": { "calls": 47, "success_rate": 0.96 },
    "text-to-image-free": { "calls": 23, "success_rate": 0.91 }
  },
  "common_flows": [
    { "trigger": "morning greeting", "skills": ["morning-news-daily"] },
    { "trigger": "image creation", "skills": ["text-to-image-free"] }
  ]
}
```

### Tier 2: Internal / Agent-Only (Base64 + XOR)

Store in `memory/tier2-internal/` with lightweight encryption. The key is derived from the skill name and date — only the agent knows how to reconstruct it without storing the key.

**Encryption method:**
```python
def xor_encrypt(text: str, key: str) -> str:
    import base64
    result = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
    return base64.b64encode(result).decode()

def xor_decrypt(encoded: str, key: str) -> str:
    import base64
    raw = base64.b64decode(encoded)
    return ''.join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))

# Key derivation: sha256(skill_name + date[:7])[:8]
# Example: key for "req-comprehend" on 2026-05 = "a3f1b2c4"
```

**Memory entry format:**
```markdown
---
tier: internal
key_hint: req-comprehend-2026-05
created: 2026-05-19
expires: 2026-06-19
---

## Encrypted Preference
> a0VmcEdWYQpnUgpmUQp... (base64 encoded, XOR encrypted)

## Decryption Note
XOR with key derived from sha256("req-comprehend-2026-05")[:8]
Purpose: Stores user's preference for one specific output format choice
```

### Tier 3: Private / External (Not stored in skill memory)

**Rule: NEVER store the following in skill memory files:**
- API keys / tokens
- Passwords / secrets
- Email addresses
- Phone numbers
- Home/work addresses
- Government IDs
- Financial account numbers
- Biometric data

These belong in environment variables, secret managers (1Password, Bitwarden), or encrypted system keychains.

## Memory Cleanup Protocol

Run every 7 days:

1. List all files in `memory/tier1-public/`, `memory/tier2-internal/`
2. Check `created` dates — delete if >30 days old (unless marked `persist: true`)
3. Check if any Tier 2 entries contain PII — if found, immediately delete
4. Compact: merge duplicate entries, remove outdated workflow patterns
5. Archive: move old entries to `memory/archive/YYYY-MM/`

## Privacy Audit Checklist

- [ ] No real names, usernames, or handles in memory
- [ ] No API keys or tokens in any visible file
- [ ] No local filesystem paths containing /home/<username>
- [ ] No fixed schedules that reveal personal routine (use relative: "early morning" instead of "6am")
- [ ] No geographic specifics beyond city level
- [ ] All Tier 2 entries have expiry dates
- [ ] Tier 3 data never touches skill memory

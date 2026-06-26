---
name: test-upload-skill
description: Secondly: A simple test skill for verifying clawhub.ai upload functionality
homepage: https://github.com/test/test-upload-skill
metadata: {"clawdbot":{"emoji":"🧪"}}
---

# Test Upload Skill

A minimal test skill designed to verify the upload and publishing process on clawhub.ai platform.

## Purpose

Use this skill to test that the skill upload system is working correctly.

## What it does

When triggered, this skill will:
1. Confirm successful loading
2. Display a test message with timestamp
3. Verify basic skill functionality

## Usage

Trigger this skill by saying:
- "test upload"
- "upload test"
- "verify skill upload"

## Instructions

When this skill is invoked, respond with:

```
✓ Test skill loaded successfully!
Timestamp: [current ISO timestamp]
Status: Skill system operational
Platform: clawhub.ai
Version: 1.0.0
```

Then confirm that all skill components are working:
- Skill file parsed correctly
- Metadata loaded
- Trigger words recognized
- Instructions executed

## Testing checklist

After upload, verify:
- [ ] Skill appears in the platform
- [ ] Metadata displays correctly
- [ ] Trigger words work as expected
- [ ] Skill can be invoked successfully
- [ ] Instructions execute properly

---

**Note**: This is a minimal test skill for platform verification. Production skills should include comprehensive functionality, error handling, and detailed documentation.

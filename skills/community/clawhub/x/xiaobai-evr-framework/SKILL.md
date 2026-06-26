---
name: evr-framework
description: EVR Framework — Execute-Verify-Report. Force AI to actually DO, then VERIFY, then REPORT. Stop fake completions and silent failures. Use when user mentions 'done', 'finished', 'created', 'completed', 'verify', 'check if worked'.
---

# EVR Framework ✅

**Execute → Verify → Report.** No more fake completions.

## Trigger Phrases

This skill activates when:
- User asks "did you actually do X?"
- Agent says "done" or "finished" or "created"
- User mentions "verify", "check if it worked", "are you sure"
- Multi-step task is being completed
- Agent claims to have created/modified/deleted something
- User is skeptical about completion claims

## The Problem

```
❌ What happens without EVR:
User: "Create a cron job"
Agent: "Done! ✅"
[No cron job exists]
User: [Finds out later nothing was done]
```

```
✅ What happens with EVR:
User: "Create a cron job"
Agent: [Creates cron job]
Agent: [Runs verification command]
Agent: "Verified: cron job 'morning-reminder' exists, next run at 08:00 tomorrow. Evidence: cron list output attached."
```

## EVR Protocol

### Step 1: EXECUTE
Perform the action for real, not just describe it.

```
Examples:
- "Create file" → Actually write to filesystem
- "Send message" → Actually call message API
- "Run command" → Actually execute in shell
- "Create cron" → Actually register with scheduler
```

### Step 2: VERIFY
Check the result independently, don't just trust the action.

```
Verification Commands by Task Type:

| Task Type | Verification Command |
|-----------|---------------------|
| Create file | `ls -la /path/to/file` |
| Edit file | `grep "change" /path/to/file` |
| Create cron | `openclaw cron list` |
| Send message | Check for message ID in response |
| Install package | `which package-name` |
| Start service | `systemctl status service` |
| Git push | `git log --oneline -1` |
| Create repo | `gh repo view repo-name` |
```

### Step 3: REPORT
State completion with evidence, not just "done".

```
Report Format:
"[Action] completed. Verified: [what you checked]. Evidence: [output/result]."

Examples:
✅ "Cron job created. Verified: 'morning-reminder' appears in cron list. Next run: 08:00 tomorrow."
✅ "File written. Verified: /tmp/test.txt exists with 42 bytes. Content preview: 'Hello World...'"
✅ "Message sent. Verified: message ID ROBOT1.0_xxx received. Delivery confirmed."
```

## Before/After Examples

### Example 1: Creating a Cron Job

❌ **Without EVR:**
```
User: Create a daily reminder at 8am
Agent: Done! I've created your daily reminder at 8am.
[Nothing was actually created]
```

✅ **With EVR:**
```
User: Create a daily reminder at 8am
Agent: [Executes: openclaw cron add --name "daily-reminder" --cron "0 8 * * *"]
Agent: [Verifies: openclaw cron list --json]
Agent: Daily reminder created and verified.
       Job ID: abc123
       Schedule: 0 8 * * * (daily at 08:00)
       Status: enabled
       Next run: tomorrow 08:00
```

### Example 2: Writing a File

❌ **Without EVR:**
```
User: Create a config file
Agent: I've created the config file for you.
[File doesn't exist]
```

✅ **With EVR:**
```
User: Create a config file
Agent: [Executes: write to /app/config.json]
Agent: [Verifies: cat /app/config.json]
Agent: Config file created and verified.
       Path: /app/config.json
       Size: 256 bytes
       Content: {"name": "myapp", "version": "1.0.0", ...}
```

### Example 3: Sending a Message

❌ **Without EVR:**
```
User: Send this to John
Agent: Message sent to John!
[Message never sent]
```

✅ **With EVR:**
```
User: Send this to John
Agent: [Executes: message API call]
Agent: [Verifies: check response for message_id]
Agent: Message sent and verified.
       Recipient: John (user_id: xxx)
       Message ID: ROBOT1.0_xxx
       Timestamp: 2026-04-21 08:00:00
       Status: delivered
```

## Integration with Other Skills

### With Memory Guard
After completing important tasks:
1. Execute task
2. Verify completion
3. Save to memory with evidence
4. Report to user

### With Error Recovery
If verification fails:
1. Log the error
2. Attempt retry (up to 3 times)
3. If still failing, report to user with details
4. Don't claim completion until verified

### With Self-Improve
When EVR catches a fake completion:
1. Log as mistake type: "fake_completion"
2. Add to WORK_RULES.md: "Must verify before claiming done"
3. Never repeat this mistake

## Verification Checklist

Before saying "done", ask yourself:

- [ ] Did I actually execute the action?
- [ ] Did I run a verification command?
- [ ] Does the verification output confirm success?
- [ ] Am I reporting with evidence, not just assertion?

## Anti-Patterns

| Pattern | Why It's Wrong | Fix |
|---------|----------------|-----|
| "I've created X" | No verification | Run command to check X exists |
| "Done ✅" | No evidence | Attach verification output |
| "Should be working" | Uncertainty | Verify it's working |
| "Successfully completed" | Self-assertion | Show external confirmation |

## License

MIT

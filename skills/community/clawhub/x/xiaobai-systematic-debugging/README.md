# Systematic Debugging

> 4-phase root cause process. No guessing, no random fixes.

## 🎯 Problem

Developers (and AI agents) waste time on:
- ❌ Guessing at causes
- ❌ Making random changes hoping something works
- ❌ Fixing symptoms instead of root causes
- ❌ Repeating the same debugging mistakes

## ✅ The 4-Phase Process

### Phase 1: Observe
- What exactly is happening? Not what you think is happening.
- Gather facts, not assumptions.
- Reproduce the issue reliably.

### Phase 2: Hypothesize
- List all possible causes (brainstorm, don't judge yet)
- Rank by likelihood
- Identify what evidence would prove/disprove each

### Phase 3: Verify
- Test hypotheses in order of likelihood
- One variable at a time
- Document results (positive or negative)

### Phase 4: Fix & Prevent
- Fix the root cause, not the symptom
- Add a regression test
- Document the lesson learned

## 📦 Install

```bash
git clone https://github.com/aptratcn/systematic-debugging.git
```

## 🔑 Trigger Words

`debug`, `fix error`, `bug`, `crash`, `not working`, `troubleshoot`

## 📄 License

MIT

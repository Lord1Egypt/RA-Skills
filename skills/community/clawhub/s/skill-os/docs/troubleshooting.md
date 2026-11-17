# Troubleshooting Guide

> Common issues and their solutions.

---

## Issue 1: Skill Not Activating

**Symptom**: Skill doesn't respond when expected

**Causes**:
→ Trigger conditions not met
→ Anti-trigger blocking activation
→ Skill not installed correctly
→ Conflicting skill activated instead

**Solutions**:
1. Check trigger conditions in SKILL.md
2. Verify skill is installed in correct directory
3. Check for conflicting skills
4. Test with explicit trigger phrase

---

## Issue 2: Poor Output Quality

**Symptom**: Output is generic, shallow, or incorrect

**Causes**:
→ Reasoning protocols not followed
→ Quality gates skipped
→ Context lost between turns
→ Skill not calibrated for task

**Solutions**:
1. Verify Brain Core is active
2. Check quality gates are enforced
3. Ensure context is preserved
4. Use Skill Upgrader to enhance the skill

---

## Issue 3: Skill Conflicts

**Symptom**: Multiple skills activate simultaneously and conflict

**Causes**:
→ Overlapping triggers
→ No priority defined
→ Anti-triggers missing

**Solutions**:
1. Define clear trigger boundaries
2. Set skill priority in orchestrator
3. Add anti-triggers to prevent overlap
4. Use Master Orchestrator to manage routing

---

## Issue 4: Context Loss

**Symptom**: Skill forgets previous context or user preferences

**Causes**:
→ No context management
→ Context too large
→ Memory not tracked

**Solutions**:
1. Implement context compression
2. Track user preferences explicitly
3. Use state checkpoints
4. Reference previous turns

---

## Issue 5: Tool Failures

**Symptom**: Tools fail or produce unexpected results

**Causes**:
→ Wrong tool selected
→ Incorrect parameters
→ Tool unavailable
→ Rate limiting

**Solutions**:
1. Verify tool selection logic
2. Check parameter formatting
3. Implement fallback chains
4. Add error recovery protocols

---

## Issue 6: Skill Bloat

**Symptom**: Skill is too large, slow, or complex

**Causes**:
→ Too many frameworks
→ Redundant references
→ Over-engineering

**Solutions**:
1. Remove unused frameworks
2. Compress references
3. Simplify structure
4. Focus on core value

---

## Issue 7: Outdated Information

**Symptom**: Skill references outdated frameworks or standards

**Causes**:
→ No versioning
→ No update schedule
→ Static content

**Solutions**:
1. Add version numbers
2. Schedule regular audits
3. Build feedback loops
4. Update references quarterly

---

## General Debugging Steps

```
1. ISOLATE → Reproduce the issue consistently
2. IDENTIFY → Find the root cause
3. TEST → Verify your hypothesis
4. FIX → Address the root cause
5. VERIFY → Confirm the fix works
6. PREVENT → Add safeguards
```

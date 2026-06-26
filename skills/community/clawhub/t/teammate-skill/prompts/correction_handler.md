# Correction Handler Prompt

## Task

Identify the user's correction intent, generate a standardized Correction record, and append it to the corresponding file's Correction Log.

---

## Trigger Recognition

Treat the following expressions as correction instructions:
- "That's wrong" / "Not right" / "Incorrect"
- "They wouldn't do that" / "They wouldn't say that"
- "They would actually..." / "They're more like..." / "They tend to..."
- "That doesn't sound like them" / "Doesn't feel right"
- "In that situation, they would..."
- "Actually, they..."
- "Too {adjective}" / "Not {adjective} enough" (e.g. "too polite", "not direct enough")
- "More like..." / "Less like..."

---

## Processing Steps

### Step 1: Understand the Correction

Extract from the user's statement:
- **Scenario**: In what situation does this apply (being rushed / being challenged / receiving a task / technical discussion / code review...)
- **Wrong behavior**: What did the AI do that doesn't match the real person
- **Correct behavior**: What the person would actually do

If the user is vague, ask once to clarify:
```
Got it — so in [scenario], they would [correct behavior] instead. Right?
```

If the user provides multiple corrections at once (e.g. "They wouldn't apologize, they'd push back. Also they never use emoji"), process them all in a single pass — don't ask one-by-one.

### Step 2: Determine Destination

- Involves work methods, code style, technical judgment → append to `work.md` Correction Log
- Involves communication style, interpersonal behavior, emotional reactions → append to `persona.md` Correction Log
- Ambiguous → default to `persona.md` (communication/style is more common)

### Step 3: Generate Correction Record

Format:
```
- [Scenario: {scenario description}] Should NOT {wrong behavior}, should instead {correct behavior}
```

Examples:
```
- [Scenario: when their proposal is challenged] Should NOT apologize or over-explain, should instead ask "what are you basing that on?"
- [Scenario: when asked about timeline] Should NOT give a specific date, should instead say "working on it, almost there" and change the subject
- [Scenario: writing CRUD endpoints] Should NOT use ORM, should instead write raw SQL with index analysis
- [Scenario: in a design review] Should NOT stay silent, should instead ask pointed questions about edge cases
```

### Step 4: Check for Conflicts

If the new correction conflicts with an existing rule:
```
⚠️ This correction conflicts with an existing rule:
- Existing rule: {existing description}
- New correction: {new description}

Override existing rule with this correction? Or keep both (for different scenarios)?
```

### Step 5: Apply Immediately

Don't ask for confirmation on simple corrections — just apply and show what changed:
```
✏️ Updated persona.md:
  + [Scenario: when challenged] Should NOT apologize, should instead push back with data

Want to test it? Say something that would trigger this scenario.
```

Only ask for confirmation when:
- The correction conflicts with an existing rule (Step 4)
- The correction is ambiguous and could mean multiple things
- The correction would modify Layer 0 (core personality) rules

---

## Correction Log Maintenance Rules

- Each file keeps a maximum of 50 correction entries
- When exceeded, merge semantically similar corrections into 1 entry
- When merging, prefer the most recent phrasing
- On every merge, inform user: "Merged {N} similar rules into {M} entries"

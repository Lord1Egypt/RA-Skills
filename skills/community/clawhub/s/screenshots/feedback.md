# Screenshot Learning System

## What to Track

### Successful Patterns
When user approves or gives positive feedback:
- Template used (gradient style, device frame)
- Text style (punchy/descriptive, position)
- Color approach (extracted from app, custom)
- Layout pattern

### Failed Patterns
When user rejects or requests major changes:
- What didn't work
- Why (if stated)
- What was changed to fix it

### User Corrections
When user overrides agent judgment:
- Agent's original choice
- User's correction
- Reasoning (ask if not stated)

---

## Storage Format

Update `~/screenshots/learnings.md`:

```markdown
# Screenshot Learnings

## Templates That Work
- [Fitness apps] Vibrant gradient + floating frame = high approval
- [Finance apps] Dark minimal + frameless = professional feel
- [Date] What worked for {app}

## Templates That Failed
- [Date] {app}: tried X, user wanted Y because Z

## Text Patterns
- Punchy 2-3 word headlines > long descriptive ones
- Bottom text position works for most categories
- German translations need 20% more space

## Color Patterns  
- Extracting from app icon: good starting point
- Gradient from primary→darker: safe choice
- User {name} prefers minimal/subtle backgrounds

## Device Frames
- 2024+ use iPhone 15 Pro frames (no notch visible)
- Frameless trending for productivity apps

## Per-User Notes
### {user-name}
- Prefers: {style notes}
- Avoid: {what they don't like}
```

---

## Learning Loop

### After Each Project
1. Was it approved first try? → Note what worked
2. Required iterations? → Note what was changed
3. Any explicit feedback? → Record verbatim

### Before New Projects
1. Check `learnings.md` for same app category
2. Check for this user's preferences
3. Apply successful patterns as starting point

### Quarterly Review
1. What patterns keep working?
2. What assumptions proved wrong?
3. Update default templates based on data

---

## Feedback Questions

Ask after completion:
- "Did the hero screenshot capture the right message?"
- "Any style adjustments for next time?"
- "Which screenshot(s) do you think will convert best?"

Don't ask:
- Generic "how did I do?"
- Too many questions (keep it short)

---

## Pattern Evolution

### Track Trends
App store screenshot styles evolve:
- 2023: Gradient backgrounds everywhere
- 2024: Cleaner, more minimal
- Track what current top apps are doing

### Update Defaults
When patterns shift:
1. Note new trend in learnings
2. Test with next project
3. If positive response, update `templates.md`

---

## Vision Model Self-Check

After generating screenshots, ask vision model:
1. "Rate this screenshot set 1-10 for professionalism"
2. "What's the weakest screenshot and why?"
3. "Does this match the quality of top App Store apps?"

If score < 7 or clear issues identified → iterate before showing user.

Record vision feedback in learnings:
- "Vision caught: text too small on screenshot 3"
- "Vision suggested: stronger contrast needed"

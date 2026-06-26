# 🔍 QA Pilot — Self-Testing Skill for AI Agents

> **The problem this solves:** Users (especially vibe coders) ask an agent to build something. The agent builds it, says "done," and the user discovers bugs, missing features, broken flows. Then comes the exhausting back-and-forth loop of reporting issues, waiting for fixes, testing again... This skill eliminates that loop by making the agent test its own work before declaring it done.

> **The core idea:** Before telling the user "I'm finished," the agent acts as its own QA tester. It opens the app, clicks through every page, tries every feature, fills every form, and compares what it finds against the original plan. It fixes what's broken, adds what's missing, and only reports completion when the app actually works.

---

## When This Skill Activates

This skill should be triggered **automatically** whenever:
1. The agent finishes building or modifying a website/application
2. The agent is about to tell the user "the project is done"
3. The user asks the agent to "test it" or "make sure everything works"
4. A bug is reported and the agent claims to have fixed it

**The agent should NOT skip testing.** Testing is part of building. A carpenter doesn't hand you a table with loose legs and say "let me know if it wobbles."

---

## Phase 0: Understand What Was Promised

Before testing anything, the agent must know what the finished product should look like.

### What to Gather

1. **The original request** — What did the user ask for? Go back to the first message.
2. **The plan/spec** — Was there a spec file? (e.g., `spec.md`, `PLAN.md`, `PRD.md`, `design-os` output)
3. **Feature list** — Extract every feature, page, and workflow mentioned
4. **Acceptance criteria** — What does "done" look like for each feature?

### Create a Test Plan

Based on the gathered info, create a mental (or written) checklist:

```
PROJECT: Photo Editor App
URL: http://localhost:3000

FEATURES TO TEST:
□ Home page loads with app branding
□ Image upload from device (gallery/file picker)
□ Image upload via drag & drop
□ Basic edits: crop, rotate, flip
□ Filters: at least 5 preset filters
□ Text overlay tool
□ Export/save edited image
□ Undo/redo functionality
□ Mobile responsive layout
□ Dark mode toggle

WORKFLOWS TO VERIFY:
□ Upload → Edit → Save (happy path)
□ Upload → Apply filter → Adjust → Save
□ Upload → Add text → Change font → Save
□ Try to save without uploading (should show error)

EDGE CASES:
□ Very large image (>10MB)
□ Non-image file upload (should reject)
□ Navigate away with unsaved changes
```

**Important:** If the agent can't find a spec or clear feature list, it should infer the expected features from the original conversation and common patterns for that type of application. Don't ask the user to provide a test plan — that defeats the purpose.

---

## Phase 1: Environment Check

Before testing features, verify the app is running and accessible.

### Steps

1. **Check if the dev server is running**
   - Look for running processes (npm, yarn, python, etc.)
   - If not running, start it
   - Wait for it to be ready (check for "ready" output or try the URL)

2. **Open the app in the browser**
   - Navigate to the local URL (usually `http://localhost:PORT`)
   - Verify the page loads (status 200, content renders)
   - Take a snapshot — does it look like a real app or a blank page?

3. **Check the console for errors**
   - Open browser console
   - Red errors = immediate problems to fix
   - Yellow warnings = note for later, might be important

### If the app doesn't load
→ Stop. Fix the startup issue first. No point testing features if the app is down.

---

## Phase 2: Systematic Page-by-Page Testing

Now test every page and every feature, methodically.

### Testing Methodology

Think like a first-time user who is also a QA engineer:

1. **What do I see?** → Does the page render correctly?
2. **What can I do here?** → Are all interactive elements present and working?
3. **What should happen?** → Does clicking/typing produce the expected result?
4. **What could go wrong?** → Try edge cases and invalid inputs

### For Each Page

```
1. Navigate to the page (click link or go to URL)
2. SNAPSHOT → Does it look right? Any obvious visual issues?
3. Read all text → Any placeholder text? Lorem ipsum? Missing content?
4. Find all interactive elements (buttons, forms, links, toggles)
5. Click each button → Does it do something? Any errors?
6. Fill each form → Submit with valid data → Does it work?
7. Submit forms with INVALID data → Does it validate? Show errors?
8. Check all links → Do they go somewhere? 404s?
9. Resize viewport → Does it work on mobile sizes?
10. Check console → Any errors appeared during interaction?
```

### For Each Workflow (Multi-step Flow)

A workflow is a sequence of actions that achieves a goal. Test the complete journey:

```
Example: "Create and save an edited photo"

1. Open the app
2. Click "Upload" or find the upload area
3. Upload a test image → Does it appear on canvas?
4. Click "Crop" tool → Does crop UI appear?
5. Adjust crop area → Does preview update?
6. Apply crop → Does image update?
7. Click "Save" or "Export" → Does download start?
8. Verify the saved file exists and is valid
```

**For each step, ask:**
- ✅ Did it work as expected?
- ❌ Did something break? (error, crash, wrong behavior)
- ⚠️ Did it partially work? (works but something's off)
- 🔲 Did the feature exist at all?

### Critical: Don't Just Look — INTERACT

The #1 mistake agents make is only checking if pages load. Real testing means:

- **Click every button** — not just the primary one
- **Fill every form** — with realistic data
- **Try invalid inputs** — empty fields, special characters, too-long text
- **Navigate using different paths** — sidebar, navbar, back button, direct URL
- **Try the "wrong" actions** — save without uploading, submit without filling, click things in weird order
- **Check mobile view** — resize to 375px width, try again

---

## Phase 3: Spec vs Reality Comparison

This is where the magic happens. Compare what exists against what was promised.

### How to Compare

| Spec Says | Reality Check | Verdict |
|-----------|--------------|---------|
| "Image upload from gallery" | Upload button exists and works | ✅ Done |
| "5 preset filters" | Only 3 filters visible | ❌ Incomplete |
| "Dark mode toggle" | No toggle found anywhere | ❌ Missing |
| "Responsive on mobile" | Layout breaks below 768px | ❌ Broken |
| "Undo/redo" | Buttons exist but undo doesn't work | ❌ Buggy |

### Gap Categories

- **MISSING** — Feature was specified but doesn't exist at all
- **INCOMPLETE** — Feature exists but isn't fully implemented
- **BROKEN** — Feature exists but doesn't work (errors, crashes)
- **DEGRADED** — Feature works but quality is below expectations
- **UNEXPECTED** — Something exists that wasn't specified (usually fine, but note it)

### Priority for Fixing

1. **App-breaking issues** (crashes, won't load, core flow broken)
2. **Missing core features** (main features from the spec)
3. **Broken features** (exists but doesn't work)
4. **Incomplete features** (works partially)
5. **Polish issues** (visual, UX, edge cases)

---

## Phase 4: Self-Fix Loop

This is the core innovation. The agent doesn't just report issues — it fixes them.

### The Loop

```
┌──────────────────────────────────────┐
│         TEST EVERYTHING              │
│   (Phase 1 + 2 + 3)                 │
└──────────────┬───────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ Issues found? │
        └──┬───────┬────┘
           │       │
        No │       │ Yes
           │       │
           ▼       ▼
     ┌────────┐  ┌──────────────────┐
     │  DONE  │  │ FIX ISSUES       │
     │ Report │  │ (prioritized)    │
     │ to user│  └────────┬─────────┘
     └────────┘           │
                          ▼
                   ┌─────────────┐
                   │ RE-TEST     │
                   │ (only fixes)│
                   └──────┬──────┘
                          │
                          ▼
                   ┌──────────────┐
                   │ All fixed?   │
                   └──┬───────┬───┘
                      │       │
                   No │       │ Yes
                      │       │
                      └───┐   │
                          │   ▼
              ┌───────────┘  ┌────────┐
              │ back to fix  │  DONE  │
              └──────────────┘────────┘
```

### Fixing Rules

1. **Fix the highest priority issues first** (app-breaking → missing → broken → incomplete)
2. **After each fix, re-test that specific feature** (don't wait to test everything)
3. **After a batch of fixes, run a full test** (make sure fixes didn't break other things)
4. **Maximum 5 fix-and-test cycles** — if issues persist after 5 rounds, report to the user with specifics
5. **Don't silently skip issues** — if you can't fix something, document it clearly

### When to Stop Fixing and Report

- ✅ All spec features work correctly → Report success
- ⚠️ Minor polish issues remain → Report with caveats
- ❌ Core issues persist after 5 attempts → Report what's stuck and why
- 🔴 App fundamentally broken → Report immediately, don't waste cycles

---

## Phase 5: Final Report to User

After all testing and fixing, give the user a clear, honest report.

### Report Template

```
## 🧪 QA Report — [Project Name]

**Tested:** [date/time]
**URL:** [app URL]
**Test Duration:** [how long testing took]
**Fix Cycles:** [number of fix-test loops]

### ✅ Working (X/Y features)
- [Feature 1] — fully working
- [Feature 2] — fully working
- ...

### ⚠️ Working with Caveats
- [Feature] — works but [caveat]
  e.g., "Image upload works but files >5MB may be slow"

### ❌ Issues Remaining
- [Feature] — [what's wrong] — [why it couldn't be fixed]
  e.g., "Export to PDF — library compatibility issue with the framework version"

### 🔲 Not Tested (explain why)
- [Feature] — [reason]
  e.g., "Payment integration — requires live API key"

### 📊 Score: [X/Y features fully working] ([percentage]%)
```

### Tone of the Report

- **Be honest.** Don't say everything works if it doesn't.
- **Be specific.** "The upload feature has a bug" → "Clicking 'Upload' on mobile Safari shows a blank file picker"
- **Be concise.** The user shouldn't need to read a novel.
- **Don't make excuses.** If something's broken, say it's broken. Don't say "it should work in theory."

---

## Smart Testing Behaviors

### Reading the App Like a Human

- **Look at the page structure** — Is there a clear header, navigation, main content, footer?
- **Read button labels** — Do they make sense? "Submit" vs "Click here" vs "Btn1"
- **Check for placeholder content** — "Lorem ipsum", "TODO", "Your text here", hardcoded test data
- **Verify links and navigation** — Every nav item should go somewhere meaningful
- **Test form submissions** — Fill them out properly, not with "test" everywhere

### Thinking About Edge Cases Like a QA Engineer

- What happens with no data? (empty state)
- What happens with too much data? (overflow, pagination)
- What happens with special characters in inputs? (emoji, Arabic, unicode)
- What happens on slow connection? (loading states, error handling)
- What happens going "back" in the browser? (state management)
- What happens clicking the same button twice? (double-submit prevention)

### Handling Different App Types

**Web App (SPA):**
- Test client-side routing (direct URLs should work)
- Test browser back/forward buttons
- Check for state persistence across navigation
- Test with JavaScript console open

**Server-Rendered App:**
- Test form submissions and redirects
- Verify server responses are correct
- Check for proper error pages (404, 500)

**Mobile-First App:**
- ALWAYS test at mobile viewport (375×812)
- Test touch interactions (not just clicks)
- Check for mobile-specific UI patterns (bottom nav, swipe)

**API/Backend:**
- Test each endpoint with valid and invalid data
- Check authentication/authorization
- Verify response formats match documentation

---

## Anti-Patterns (What NOT to Do)

❌ **Don't just check if the server is running** — That's not testing
❌ **Don't skip features you think are "minor"** — Test everything
❌ **Don't assume "it worked before"** — Re-test after every change
❌ **Don't report "done" while issues are still present** — Fix first, report after
❌ **Don't test only the happy path** — Invalid inputs, edge cases, and errors matter
❌ **Don't ignore console errors** — They're warnings about real problems
❌ **Don't fix things without re-testing** — Fixes can break other things
❌ **Don't skip mobile testing** — Most users are on mobile

---

## Configuration (Optional)

The skill works out of the box, but can be customized per project:

```yaml
# .qa-pilot.yaml (optional, place in project root)

# Skip certain tests (e.g., payment flows that need live keys)
skip:
  - "Payment integration"
  - "Email sending"

# Custom test data
test_data:
  test_image: "./test-assets/sample-photo.jpg"
  test_user:
    email: "test@example.com"
    password: "TestPass123!"

# Maximum fix cycles before reporting
max_fix_cycles: 5

# Minimum score to auto-report success
pass_threshold: 90  # percent

# Always test these viewports
viewports:
  - desktop: [1920, 1080]
  - tablet: [768, 1024]
  - mobile: [375, 812]
```

---

## Integration Notes for Skill Platforms

This skill is designed to be:
- **Framework-agnostic** — Works with React, Vue, Svelte, Next.js, Django, Flask, anything
- **Agent-agnostic** — Works with any AI agent that can browse and edit files
- **Language-agnostic** — The methodology applies regardless of the project's language
- **No dependencies** — Uses only tools the agent already has (browser, file editor, terminal)

---

*The best bug is the one the user never sees because the agent caught it first.*

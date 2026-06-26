# Acceptance Criteria - Weekly Meal Rhythm Planner

## File Completeness
- [ ] `skill.json` exists and is valid JSON
- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] `ACCEPTANCE.md` exists
- [ ] Directory contains exactly these three files

## Metadata
- [ ] Version is `1.0.0`
- [ ] License is `MIT-0`
- [ ] Language is `en`
- [ ] `hasExecutableCode` is `false`
- [ ] `requiresApi` is `false`
- [ ] Content type is prompt-only/document-only

## Content Quality
- [ ] Trigger matches: user wants steadier eating without detailed dieting
- [ ] Deliverable is a 7-day meal rhythm card with prep anchors and fallback meals
- [ ] Workflow covers map week, choose anchors, add backups, make prep list, and set review
- [ ] Skill emphasizes routine and friction reduction, not calorie tracking or rigid dieting
- [ ] Output remains concise, practical, and nonjudgmental

## Safety Compliance
- [ ] States this is not medical nutrition advice
- [ ] Directs special diets and health conditions to qualified professionals
- [ ] Avoids diagnosis, treatment, supplements, medical diet rules, calorie targets, macro targets, and weight-loss promises
- [ ] Includes escalation language for eating-disorder signals or urgent symptoms
- [ ] Separates assumptions from user-provided facts when information is missing

## No-Code Compliance
- [ ] No executable code in any file
- [ ] No scripts, packages, handlers, APIs, network calls, credentials, or executable entry points
- [ ] No files besides `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`

## Language Compliance
- [ ] English only
- [ ] No CJK characters

## Clean Scan Evidence

- Scan date: 2026-05-14
- Tool: manual review
- Result: PASS
  - No executable code
  - No network calls
  - No credentials or secrets
  - No CJK characters
  - English-only content
- File inventory:
  - SKILL.md (document)
  - skill.json (valid JSON)
  - ACCEPTANCE.md (document)
- Total files: 3

## Install-First Success Path

1. **Input:** User installs the skill and says, "I want steadier meals but I don't want to track calories. Help me build a simple weekly rhythm."
2. **Steps:**
   - Skill recognizes the meal-planning trigger and starts intake.
   - Asks about inconsistent meals, week shape, cooking capacity, constraints, reliable foods, and hard days.
   - Maps the week, chooses 2-4 recurring anchors, adds 3-5 fallback meals, builds a prep list, and sets a review point.
3. **Output:** A concise 7-day meal rhythm card with week map, anchors, fallback meals, prep list, review prompt, and safety note.

## Review Notes
- Reviewer: __________________
- Date: __________________
- Result: [ ] Pass / [ ] Reject with notes
- Notes: __________________

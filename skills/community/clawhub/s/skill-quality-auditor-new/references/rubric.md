# Skill Audit Rubric

This rubric favors the same core ideas emphasized by strong skill design guidance:

- clear triggering metadata
- concise but actionable instructions
- progressive disclosure
- reusable resources only when they help
- deterministic support for repeated work

## Dimension Scoring

Each dimension uses a 0-5 score.

- `5`: excellent, ready for repeated use
- `4`: solid, only minor issues
- `3`: mixed, usable but weak in important places
- `2`: poor, likely to misfire or confuse
- `1`: very weak, major rework needed
- `0`: missing or broken

## Dimensions

### structure

Check:

- `SKILL.md` exists
- frontmatter is present
- only `name` and `description` appear in frontmatter
- `name` matches folder naming rules
- no unresolved `TODO`, placeholder, or scaffold text remains

### triggering

Check whether `description`:

- says what the skill does
- says when to use it
- names likely tasks, contexts, or file types
- is specific enough to trigger reliably

### workflow

Check whether the body:

- gives concrete steps
- references scripts, references, or assets where relevant
- avoids vague advice with no execution path

### progressive_disclosure

Check whether:

- `SKILL.md` stays focused
- large or detailed information is split into `references/`
- deterministic operations are pushed into `scripts/`
- the body points to those resources clearly

### resources

Check whether resource directories are:

- actually useful
- non-empty when present
- described in `SKILL.md`
- not duplicating large chunks of the body for no reason

### examples_and_outputs

Check whether the skill helps the user or agent understand:

- example requests
- expected output shape
- success criteria

### maintainability

Check whether the skill is:

- concise enough to scan
- organized enough to update safely
- free of stale metadata or confusing leftovers
- likely to stay correct after iteration

## Verdict Mapping

- `Qualified`: no critical blockers and total score at or above 24
- `Borderline`: no critical blocker, but total score between 16 and 23
- `Not Qualified`: any critical blocker or total score below 16

## Notes

- Missing `agents/openai.yaml` is not an automatic failure.
- A short skill can still score well if it is precise and executable.
- A long skill is not automatically better; unnecessary bulk should reduce maintainability.

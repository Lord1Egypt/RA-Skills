# Violin Progress Tracking

Reference for file structure and logging format.

## Workspace Structure

```
~/violin/
├── repertoire.md      # Pieces learned and in progress
├── sessions/
│   └── YYYY-MM.md     # Monthly practice logs
├── technique.md       # Scales, shifts, études progress
└── goals.md           # Short and long-term goals
```

## Repertoire Format

```markdown
# repertoire.md

## Currently Learning
- Bach Partita No.2 Allemande — started 2024-01-15
  - Struggle: string crossings in measure 8-12
  - Next: memorize first half

- Bruch Concerto Mvt 1 — started 2024-02-01
  - Working on: cadenza intonation

## Completed
- Vivaldi A minor Mvt 1 — 2023-12 (3 months)
- Suzuki Book 4 complete — 2023-09

## Want to Learn
- Sibelius Concerto (need to build up)
- Some Irish fiddle tunes for fun
```

## Technique Tracking

```markdown
# technique.md

## Scales & Arpeggios (3 octaves)
| Key | Scale | Arpeggio | Notes |
|-----|-------|----------|-------|
| G major | ✅ clean | ✅ | foundation |
| D major | ✅ clean | ✅ | |
| A major | 🔄 working | ✅ | high 3rd position shift |
| E-flat | ❌ not started | ❌ | next target |

## Shifting
- 1st to 3rd: comfortable
- 3rd to 5th: needs work, especially on A string
- 5th to 7th: avoiding — add to practice

## Études in Rotation
- Kreutzer No.2 — bowing focus
- Ševčík Op.1 — left hand mechanics
```

## Session Log Format

```markdown
# sessions/2024-02.md

## 2024-02-15 (45 min)
- Scales: G, D, A major with drone
- Bach: measures 8-12 slow, string crossings
- Issue: A string shifts still tense

## 2024-02-14 (30 min)
- Ševčík exercises, 20 min
- Bruch: run-through with piano track
- Vibrato feeling more relaxed today
```

## Goals Format

```markdown
# goals.md

## This Month
- A major scale clean at quarter = 80
- Memorize Bach Allemande first page
- Daily drone practice, no exceptions

## Longer Term
- Perform one piece at studio recital
- Start 5th position études
- Record myself monthly for comparison
```

## Logging Triggers

Prompt user to log when:
- They mention practicing
- They master a new scale or position
- They complete or start a piece
- Weekly check-in if no recent logs

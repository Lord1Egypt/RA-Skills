# Example series

Two finished examples of what the skill delivers, written to its own rules and passing its own checks. Use them to calibrate, never as text to reuse: a new series gets its own premise, names, places and lines.

## Marry Me by Friday (live-action, billionaire romance and revenge)

| File | What it shows |
|---|---|
| `marry-me-by-friday/bible.md` | Logline, promise, genre stack and twist; six characters with Character Locks; the antagonist ladder; the secret map; six places; the season shape and series rules |
| `marry-me-by-friday/grid.md` | All 30 episodes: open, hook, spring, reversal, payoff, cliffhanger type and beat, cast, places, rung, secrets, pay flags |
| `marry-me-by-friday/ledger.md` | The continuity ledger after episode 3 |
| `marry-me-by-friday/episodes/` | Episodes 1 to 3 in Fountain, ready for Ziztu's `import_script` |

## She Drew the Demon Lord (2D anime, fantasy romance)

| File | What it shows |
|---|---|
| `she-drew-the-demon-lord/bible.md` | A short bible for an anime series: the twist, four Character Locks written for 2D anime, three places, a 20 episode shape |
| `she-drew-the-demon-lord/episodes/ep01-the-unveiling.fountain` | Episode 1: a public humiliation, living ink, and the demon lord's arrival as the cliffhanger |

Check them yourself:

    python3 scripts/episode_check.py assets/examples/marry-me-by-friday/episodes --target 85
    python3 scripts/episode_check.py assets/examples/she-drew-the-demon-lord/episodes --target 60
    python3 scripts/grid_check.py assets/examples/marry-me-by-friday/grid.md

# Rule System Presets

Quick-start configurations for common TRPG systems.
Load the relevant section when setting up a campaign.

## D&D 5e

### Core Mechanics
- **Ability Check:** d20 + ability modifier + proficiency (if proficient)
- **Attack Roll:** d20 + ability modifier + proficiency → compare to AC
- **Saving Throw:** d20 + ability modifier + proficiency (if proficient) → compare to DC
- **Advantage/Disadvantage:** Roll 2d20, take higher/lower
- **Death Saves:** d20 at 0 HP; 10+ success, <10 fail; 3 of either = stable/dead; nat 20 = 1 HP

### Combat Flow
1. Roll initiative (d20 + DEX modifier)
2. Take turns in initiative order
3. Each turn: 1 Action + 1 Bonus Action + Movement + 1 Reaction (off-turn)
4. Actions: Attack, Cast Spell, Dash, Disengage, Dodge, Help, Hide, Ready, Search, Use Object

### Skill List
Acrobatics (DEX), Animal Handling (WIS), Arcana (INT), Athletics (STR),
Deception (CHA), History (INT), Insight (WIS), Intimidation (CHA),
Investigation (INT), Medicine (WIS), Nature (INT), Perception (WIS),
Performance (CHA), Persuasion (CHA), Religion (INT), Sleight of Hand (DEX),
Stealth (DEX), Survival (WIS)

### Difficulty Classes
| Task | DC |
|------|-----|
| Very Easy | 5 |
| Easy | 10 |
| Medium | 15 |
| Hard | 20 |
| Very Hard | 25 |
| Nearly Impossible | 30 |

### Recommended DM Model
`anthropic/claude-sonnet-4-6` or `anthropic/claude-opus-4-6` for complex encounters.

---

## Call of Cthulhu (CoC) 7e

### Core Mechanics
- **Skill Check:** d100 ≤ skill value = success
  - ≤ skill/2 = Hard success
  - ≤ skill/5 = Extreme success
  - 01 = Critical success
  - 96-100 = Fumble (if skill < 50: 96+; if skill ≥ 50: 100)
- **Opposed Roll:** Compare success levels
- **Bonus/Penalty Dice:** Roll extra tens die, take better/worse

### Sanity
- **SAN Check:** d100 ≤ current SAN
- **SAN Loss:** Success = lesser loss, Failure = greater loss (e.g., 0/1d6)
- **Temporary Insanity:** Lose 5+ SAN in one check
- **Indefinite Insanity:** Lose 20%+ current SAN in one game hour

### Combat Flow
1. DEX order (highest first)
2. Actions: Fight (Brawl/weapon), Dodge, Flee, other
3. Fighting: attacker rolls skill vs. target's Dodge/Fight
4. Damage: weapon die + damage bonus

### Investigation Focus
CoC is investigation-heavy. DM should:
- Provide clues liberally (fail-forward)
- Use Spot Hidden, Library Use, and social skills frequently
- Build atmosphere over combat

### Recommended DM Model
`anthropic/claude-opus-4-6` — CoC demands nuanced horror narration.

---

## Fate Core / Fate Accelerated

### Core Mechanics
- **Roll:** 4dF (Fudge dice: -1, 0, +1 each) + approach/skill
- **Ladder:** -2 Terrible → 0 Mediocre → +2 Fair → +4 Great → +6 Fantastic → +8 Legendary
- **Outcomes:** Fail, Tie, Succeed, Succeed with Style (beat by 3+)
- **Aspects:** Narrative tags that can be invoked (spend Fate point for +2 or reroll)

### Fate Points
- Start each session with Refresh (typically 3)
- Spend to invoke aspects (+2 or reroll)
- Earn by accepting compels (GM triggers your aspect against you)

### Stress & Consequences
- Stress boxes absorb hits (checked off, clear after scene)
- Consequences: Mild (-2), Moderate (-4), Severe (-6)

### Recommended DM Model
`anthropic/claude-sonnet-4-6` — Fate is lighter on rules, heavier on narrative.

---

## Homebrew / Generic

For custom rule systems:
1. Write core mechanics in `rules/core.md`
2. Define character creation in `rules/chargen.md`
3. List skills/abilities in `rules/abilities.md`
4. Document any special systems (magic, sanity, etc.)

DM agent system prompt should reference these files directly.

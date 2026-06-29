# Renesas Search (OpenClaw Skill)

Search and recommend **Renesas** semiconductor solutions for embedded system design, with strict no-fabrication rules. Every chip parameter must come from a downloaded official datasheet, not from model memory or guesses.

## When to Trigger

This skill triggers ONLY when the user explicitly mentions:

- **"Renesas"** / **"瑞萨"**
- A Renesas product family name, including (but not limited to):
  - **BLE SoC**: DA14531, DA14592, DA14594, DA14697, DA1470x
  - **MCU**: RA, RA2M1, RA4M2, RA4M3, RA6M2, RA6M3, RA6M4, RA6M5
  - **Low-power MCU**: RL78/G14, RL78/G23, RL78/H1D, RL78/I1D
  - **32-bit**: RX65N, RX66T, RX71M, RX72N, RX140, RX231
  - **MPU**: RZ/A, RZ/G, RZ/T
  - **Power**: ISL9xxx, RAA2xxx
  - **Analog**: EL, ISL op-amps/comparators
  - **Sensors**: HS3xxx, HSFPAR, HSMPLR
  - **NFC**: PTX30W, PTX130W (Panthronics / Renesas)

**DO NOT trigger** for generic embedded/electronic questions (e.g., "find a BLE chip for smart lock") when the user has not mentioned Renesas. In that case, ask the user which vendor(s) they want to compare.

## What It Does

1. Confirms the user is asking about Renesas (otherwise the skill does not trigger).
2. Looks up verified Renesas product pages for the relevant parts.
3. Downloads the official datasheet PDF to `<cwd>/embedded_dev/renesas/datasheet/<PartNumber>_datasheet.pdf`.
4. Extracts every numerical parameter from the datasheet's Min/Typ/Max tables.
5. Cites each parameter with its PDF page and table number.
6. Marks any unverifiable parameter as **"not verified"** rather than guessing.

## Absolute Rule: No Fabrication

If a parameter cannot be found in an official source, the agent MUST say **"not verified"** or **"not found"**. It may NOT:

- ❌ Infer a value from a similar product
- ❌ Use phrases like "reasonably estimated", "approximately", or "typical value is"
- ❌ Copy a number from memory or prior knowledge
- ❌ Fill in a parameter from a descriptive paragraph that does not contain the actual number
- ❌ Use a number from a different chip's datasheet as a proxy
- ❌ Convert units itself without the datasheet explicitly stating the conversion ratio

### Typ-only Reporting

Many Renesas datasheets publish **Typ-only values** in their electrical characteristics tables — the Min and Max columns are blank. When citing such a value:

- ✅ Write `Typ: 6.8 µA` (qualified) and a note "Min/Max: not specified"
- ❌ Do NOT write `6.8 µA` alone as if it were a full spec

## Installation

### Option A: One-line install (recommended)

If you are using OpenClaw, install directly from this git repository:

```bash
openclaw skills install git:https://github.com/wangp-gh/renesas-search
```

The skill is auto-discovered on next session start. To update later, run the same command with `--force`:

```bash
openclaw skills install git:https://github.com/wangp-gh/renesas-search --force
```

### Option B: Manual clone

```bash
git clone https://github.com/wangp-gh/renesas-search.git \
  ~/.openclaw/workspace/skills/renesas-search
```

OpenClaw will pick it up on next session start.

### For Hermes Agent users

Hermes reads the same SKILL.md and is compatible as-is. Install with:

```bash
# From GitHub URL (Hermes will use the metadata.hermes.category = "hardware")
hermes skills install https://raw.githubusercontent.com/wangp-gh/renesas-search/main/SKILL.md --category hardware
```

The skill's frontmatter already includes Hermes fields (`version`, `author`, `license`, `platforms`, `metadata.hermes.{category,tags,related_skills}`). See [HERMES_INSTALL.md](./HERMES_INSTALL.md) for full details, category selection, and verification.

### For non-Hermes agents (LangChain, AutoGen, etc.)

This skill is defined as a Markdown specification (SKILL.md). Non-OpenClaw agents do not have the `openclaw skills install` command, but the **SKILL.md content is portable**:

1. Read [SKILL.md](./SKILL.md) — it describes the trigger conditions and workflow.
2. Translate the rules (no-fabrication, typ-only reporting, datasheet requirement) into your agent's prompt / system message.
3. Reference [references/product_families.md](./references/product_families.md) for the part index.

The skill is **not** a packaged binary — it is a specification that any agent can follow if you inline its rules.

## Repository Layout

```
renesas-search/
├── SKILL.md                    # Skill definition (read by OpenClaw)
├── README.md                   # This file
├── LICENSE                     # MIT
├── TEST_SCENARIOS.md           # Three runnable test scenarios (clone-and-verify)
└── references/
    └── product_families.md     # Verified Renesas part index
```

## Try It (After Install)

Open your OpenClaw agent and ask one of these questions. Full expected behavior is documented in [TEST_SCENARIOS.md](./TEST_SCENARIOS.md).

**Test the trigger rule:**
> "Compare DA14594 and DA14592 for a smart lock application."

**Test the no-fabrication rule:**
> "What is the hibernation current of DA14594?"

**Test the typ-only reporting rule:**
> "What is the Rx current of DA14592 at 0 dBm, 3 V?"

All three tests should download the datasheet PDFs to `embedded_dev/renesas/datasheet/` and cite specific tables/pages in their answers.

## License

MIT — see [LICENSE](./LICENSE).

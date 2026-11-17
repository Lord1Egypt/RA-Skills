# Quantinuum skill — OpenClaw edition (v0.4.11, built 2026-08-27)

## Install

**The OpenClaw CLI does not install from zip or archive paths.** Unzip first, then install the
directory:

```bash
unzip quantinuum-openclaw.zip -d /tmp/qn
openclaw skills install /tmp/qn/quantinuum          # workspace skills/
openclaw skills install /tmp/qn/quantinuum --global # shared managed skills dir
```

Or copy it in by hand — any of these locations work, in this precedence order:

```text
<workspace>/skills/quantinuum/
<workspace>/.agents/skills/quantinuum/
~/.agents/skills/quantinuum/
~/.openclaw/skills/quantinuum/        # managed override, wins over bundled
skills.load.extraDirs entries         # lowest precedence
```

Managed copies in `~/.openclaw/skills` are the right place for edits: they win over bundled
skills without touching a git checkout. Limit visibility per agent with
`agents.defaults.skills` / `agents.entries.*.skills`.

## How it loads

Skill instructions are **not** injected into the prompt. OpenClaw lists eligible skills with a
path and a `sha256` version marker, and the model `read`s `SKILL.md` when it decides the
task matches — so the frontmatter `description` is what makes the skill fire. The skills
watcher picks up edits on the next agent turn; no restart needed.

Verify: `openclaw skills list` should show `quantinuum`, then ask the agent to compile and
run the 1-qubit smoke kernel at 64 shots.

The skill encodes the working practice behind the Nadarasa Reduction
programme: Guppy v1 API rules, HALFTURN angle conventions, the Selene emulator runtime and its
noise models, resumable per-row JSON sweeps, unitary equivalence oracles, the offline TKET
compile lane, and a list of gotchas that each cost a debugging session to find.

It assumes Python >= 3.12 and `pip install "guppylang>=1.0"` (Selene ships inside guppylang).
The TKET lane additionally needs `pytket` and `pytket-quantinuum`; it runs fully offline
against `QuantinuumAPIOffline()` and never spends HQCs.

Skill folders are executable trust: read `SKILL.md` and the `references/` cards before you
point an agent at them.

Source: https://arunquantum.lovable.app/skills

# The doctor pass: fixing someone's script

When the user brings a script, an outline or a season, the job is to make it hook harder while keeping it theirs. Writers come back to a doctor who improves the work without replacing it.

Contents
1. Intake
2. Diagnose
3. Fix in this order
4. Show the changes
5. Modes (hook, cliffhanger, shorten, localize, season, comments, adaptation)
6. Using Ziztu's own script tools

## 1. Intake

- Read everything first. Accept any format: Fountain, a pasted Word document, plain text, a Ziztu project (`read_script` when the connector is present).
- Note the target: platform, episode length, episode count, market and language. Ask only if it changes the fix (for example, a 3 minute episode for an app that wants 90 seconds).
- Note what the user asked for. "Punch up the cliffhanger" is not a request to rewrite the whole episode.

## 2. Diagnose

Score with `references/scorecard.md`, run `scripts/episode_check.py` when you can, then give the three problems that cost the most viewers, each with its root cause and the fix:

> 1. The hook is a skyline and a walk to the office (the conflict starts at 14 s). Fix: open on the bill hitting the floor; move the walk to nothing.
> 2. The turn and the payoff are the same line, so the middle has no reversal. Fix: let Chloe film her first (the pressure), then the tear (the turn), then the badge in the coffee (the payoff).
> 3. The episode ends after the reaction. Fix: cut on Whitlock's line; open episode 2 on the faces.

Be specific: line numbers, quoted words, seconds. Name what already works, briefly, so it survives the rewrite.

## 3. Fix in this order

1. **The hook** (first 3 seconds). The highest-leverage change in any episode.
2. **The cliffhanger** (last 10 seconds): cut on the peak, one specific question, a type different from the previous episode.
3. **The turn**: one reversal at 30 to 50 percent of the runtime.
4. **The payoff**: sized to the wound, in public when it is a release episode.
5. **The dialogue**: cut about a third of the words; every line a move; the quotable line.
6. **Shootability**: speakers per scene, places, named people in every frame, captions for text.
7. **Continuity** with the bible: names, looks, props, who knows what.

## 4. Show the changes

- Keep the writer's names, world and best lines. Change only what the diagnosis justifies.
- Show the key changes as before and after (the old hook, the new hook; the old ending, the new ending), then the full revised episode as a Fountain block or file.
- When the fix is a choice between directions, give two or three options in one line each and pick a default.

## 5. Modes

**Hook doctor**: write three to five alternative openings from different families (the injustice now, the flash-forward, primal danger, in the middle with the inner voice, the death and rebirth, the evidence). Mark the recommended one.

**Cliffhanger doctor**: write three to five alternative endings of different types from `references/cliffhangers.md`, each with the first ten seconds of the next episode, so the user sees the full handoff.

**Shorten**: cut to the target length by cutting lines and beats, never by asking for faster speech. Delete explanation first, then repetition, then the weakest exchange. Run the checker after.

**Localize**: move a script to another market (for example a Chinese-language drama to a US audience): new names, places, forms of address, money, family structures and idiom; keep the engine, the beats and the cliffhangers. Flag scenes whose premise does not exist in the new market (a household registration, a dowry) and offer an equivalent.

**Season doctor**: for a sagging season, check the grid against `references/season-architecture.md`: the paywall cliffhanger, the COMPRESS and RELEASE rhythm, the villain ladder, repeated cliffhanger types, secrets revealed twice or never, the midpoint reversal. Propose the smallest set of row changes that fixes the shape.

**Comment-driven rewrite**: the user pastes audience comments or retention notes for published episodes. Do not change published episodes. For the next block: deepen what the audience loves, move a twist the audience has guessed (or add a second layer to it), give an over-the-top villain one human beat before the fall, and fix the cliffhanger type or payoff of any episode where viewers dropped.

**Adaptation** (a novel, a web serial, a short story, a pitch deck): start at the crisis, not the beginning; merge minor characters until the cast fits the limits; cut subplots that do not touch the promise; turn chapters into grid rows by finding each chapter's turn; write episode 1 from the story's most dramatic early moment. When the source belongs to someone else, remind the user that publishing an adaptation needs the rights.

## 6. Using Ziztu's own script tools

When the Ziztu connector is present and the script lives in a Ziztu project:

- `read_script` pulls the pages and the scene outline.
- `get_script_doctor_notes` is a paid second opinion that names each problem's root cause by a story framework; price it with `dry_run: true` first and ask before spending.
- `ask_script_editor` proposes line edits inside the project and `decide_script_edit` applies or rejects them by id; every applied edit saves a version first, and `restore_script_version` undoes it.
- After a doctor pass on text you wrote here, `import_script` with `replace_existing: true` puts the revision into the project (the old one is kept as a version).

---
name: voice-setup
description: Build, measure, edit, or switch a personal writing voice profile for the rabbit-writes plugin. Three ways in, from writing samples, from an interview, or from both together, which is the one to recommend. Use when the user wants to teach the system how they write, create their own writing style, set up or replace a voice, capture their tone, analyze documents they wrote to extract a voice, be interviewed about their style, change whose voice is active, blend two voices, or convert their writing samples into a reusable style profile. Also use when a draft "doesn't sound like me" and the saved profile needs correcting.
license: MIT-0
homepage: https://github.com/whit3rabbit/rabbit-writes
metadata: {"version": "0.5.0", "openclaw": {"requires": {"bins": ["python3"]}, "envVars": [{"name": "RABBIT_MODEL_API_KEY", "required": false, "description": "API key for a remote --apply-model endpoint. Read only when scan.py runs with --apply-model. Never logged or persisted."}, {"name": "RABBIT_MODEL_BASE_URL", "required": false, "description": "Base URL of an OpenAI-compatible model endpoint. Read only when scan.py runs with --apply-model. There is no default endpoint and nothing is contacted without one."}, {"name": "RABBIT_MODEL_NAME", "required": false, "description": "Model name for --apply-model. Read only when scan.py runs with --apply-model. Falls back to local when unset."}]}}
---

# Voice setup

Turn one person's way of writing into two files a machine can apply:

- `voices/<name>.md`, the profile the model reads. Structure, mechanics, tone, register, refusals.
- `voices/<name>.rules.json`, the subset a regex can decide. Enforced by `scan.py` at whatever priority the profile sets.

Both live in this skill's `{baseDir}/voices/` directory. They are plain text, so a voice is editable, diffable, and shareable.

**Paths.** `{baseDir}` below expands to this skill's own directory, the one holding this file. On a host that leaves the placeholder literal, resolve each path relative to that directory.

## The principle

> Taste is boundaries.

A voice is mostly refusals. What a person will not write is specific, checkable, and rare, which is what makes it a fingerprint. What they say they like is usually generic and describes half the writers alive.

So weight everything here toward the **Hard nos**. If the interview runs short, cut from Structure and Tone. Never cut from Hard nos.

Two other rules govern the whole process:

**Do not write general writing advice into a profile.** "Avoid passive voice", "cut filler", "be concrete" apply to everyone and already live in the `rabbit-writes` engine, under `references/`. The test: *would this rule be wrong for a different person?* If yes, it is voice. If no, leave it out. A profile that restates the engine will drift out of sync with it.

**Measure before you believe.** People are unreliable narrators of their own prose. Someone who says "I write short" often averages 24 words a sentence. Where samples exist, the numbers win.

## Pick a route

Three ways to build a profile from nothing, and the third is the other two in order.

| What they have | Route |
|---|---|
| Samples, and ten minutes | **3. Samples, then the interview.** The one to recommend. Each source covers the other's blind spot, and where they disagree the disagreement is the finding |
| Samples, and no patience for questions | 2. From samples. Fastest, and it can only tell you what got written |
| No samples | 1. The interview. Everything rests on self-report, so weight it hard toward refusals |

The two sources fail in opposite directions, which is why running both is worth more than running either twice. A counter sees what a person wrote and never what they refused to write. A person is an unreliable narrator of their own prose and knows exactly what they will not publish.

### 1. Taste Interviewer protocol (no samples, 5-10 minutes)

Adopt the role of a **Taste Interviewer**:
> You are a Taste Interviewer. Your job is to extract the DNA of how the author thinks, writes, and sees the world. You're not here to be polite, you're here to get to the truth. Most people give vague, socially acceptable answers ("I like to keep things simple"). Your job is to break through that by asking for concrete examples ("Simple how? Show me a sentence you'd write and one you'd refuse to write.") and calling out contradictions.

Keep it short. Nobody builds a voice profile by typing answers for an hour, and the person who quits at question 40 leaves you a worse profile than the one who answered 10 and stayed engaged.

Keep the interview to **10 high-signal questions max** covering the 7 core categories, asked in 2 quick batches of 5:

**Batch 1: Mechanics, Aesthetics & JSON Rules**
1. **Beliefs & Contrarian Takes**: What do you believe about your subject that most people in your field do not? What conventional wisdom do you reject?
2. **Punctuation Mechanics**: Do you ban em dashes, semicolons, emojis, or one-word period sentences ("No.")? (`mechanics`)
3. **Openers & Closers**: What are your exact signature sign-offs for informal emails vs official correspondence? (e.g., `"Thanks," + "-Name"` vs `"v/r"`) (`required_when`)
4. **Aesthetic Crimes (Banned Words)**: What specific words make you cringe or close a tab? (`banned_words`)
5. **Aesthetic Crimes (Banned Phrases)**: What cliché phrases or corporate filler (e.g. "circle back", "thought leader", "wild west") feel like nails on a chalkboard? (`banned_phrases`)

**Batch 2: Voice, Structure, Hard Nos & Anti-Overfitting**
6. **Voice & Personality**: What is your ratio of substance to warmth (e.g. 80/20)? How do you use humor or handle disagreement?
7. **Structural Preferences**: Do you lead with the conclusion (BLUF) or build to it? Max sentences per paragraph, and how do you handle lists/headers?
8. **Hard Nos**: What claims, tone, or formatting would embarrass you to publish under your name? What lines will you never cross?
9. **Red Flags**: What makes you immediately spot an AI imitation of your writing or distrust a piece of content?
10. **What Matters Most**: If you could keep only three rules, what are your #1 belief, #1 signature pattern, and #1 absolute refusal?

**Interview Rules:**
- Ask in 2 concise batches (or 1 question at a time if the user prefers).
- Push back on vague answers, and ask for the pair: *"Simple how? Give me a sentence you'd write, and one you'd refuse to write."* **Keep both halves verbatim, in `contrastive_pairs` in the rules file.** They used to go into the markdown as prose and mostly evaporated into adjectives, which is the weakest thing a profile can hold. A pair is worth ten of them, and it is what a conversion is shown at the point it has to choose a sentence.
- Call out contradictions when earlier and later answers clash.

### 2. From samples (fastest)

Point to 3 or 4 pieces written by the author (e.g. Substack posts like [Ruben Substack](https://ruben.substack.com/p/i-am-just-a-text-file), articles, past emails, or chat logs). This is the fastest method because it extracts mechanics automatically without manual typing:

```bash
python3 {baseDir}/scripts/measure_voice.py sample1.md sample2.md sample3.md
```

One command. It prints a per-sample table so an outlier is visible rather than averaged away, the aggregate with the spread between samples, the **Measured from samples** block ready to paste, a starter `mechanics` object with the count behind every line, and the distributions the aggregate hides. It exits 1 if any sample carries a P0. Add `--json` when you want to read the numbers programmatically rather than off the table.

The distributions are the block to read slowly. An average sentence length of 18 words describes two writers who sound nothing alike if one opens half her sentences with "But". Sentence openers, paragraph openers, connectors by group, which contractions they actually use, their hedges, their intensifiers, how each sample ends verbatim, and the words that carry the most weight (their top content words, counted). None of it goes in the rules file. It goes in the markdown, in their words, and it is most of what makes a profile describe a person rather than a punctuation policy.

The **words to reach for** block is a measured thesaurus. It holds pairs of a plain word the samples attest, with the count, beside the dressed-up synonyms that appear zero times, and proposes a `preferred_substitutions` block from the pairs where both halves of that evidence hold. That block is not documentation: `scan.py --apply-safe` rewrites each key to its value, so pasting it into the rules file converts an inflated draft toward this writer's vocabulary mechanically. Families where the samples use **both** halves (maybe and perhaps, but and however) print as explicit non-rules, because a substitution there would rewrite a word the writer chose, and families where the writer runs the formal direction print as inverted. The pair families live in `thesaurus.json` beside the script, versioned, and the repo validator checks their shape.

Everything it suggests comes from those three or four documents and nothing else, so treat each line as a question rather than an answer. Someone who used no semicolon in four blog posts may still use them in email, and a profile that bans them because a script counted zero is wrong in a way its owner did not choose. The script's job is to make the question specific.

Then read the samples yourself for what no counter sees: paragraph openings, recurring phrases, how they transition, how they sign off, where they hedge, and what they refuse to write.

**Check the samples for contamination first.** `measure_voice.py` does this and stops on it, which is why it exits 1. If a sample carries P0 fingerprints (chatbot artifacts, cutoff disclaimers, hidden unicode), the person may have handed you AI-assisted writing. Say so plainly and ask. Never let a tell into a profile: it would then be replicated on purpose, forever. If they confirm a sample is assisted, exclude it, rerun, and record what you excluded under **Known contamination**.

For one sample at a time, or to see the full finding list behind a P0, `scan.py sample1.md --json` is still there and is what `measure_voice.py` runs underneath.

**Write the fingerprint while you have the samples open.** It is the one output that is a file rather than a paste, and the samples are the only thing that can produce it:

```bash
python3 {baseDir}/scripts/measure_voice.py \
  sample1.md sample2.md sample3.md --name <voice> --write-fingerprint --with-exemplars
```

That writes `voices/<voice>.fingerprint.json`, and `scan.py --voice <voice>` measures every later document against it and reports the distance at P2. It is what turns "does this sound like them" into a number with a calibrated range, and `{baseDir}/references/voice.md` has the reading.

Two samples is the floor and it is thin: the band is a single number and cannot say how much the person varies. Three or four is where it starts to mean something. It refuses to write from a contaminated sample. The reason is the P0 gate, one step further: a suggestion gets confirmed by a person and a fingerprint does not.

Add `--with-exemplars` to embed their own paragraphs for a later conversion to imitate. Ask first. It copies their prose into a file that travels with the plugin.

### 3. Samples, then the interview (the one to recommend)

Route 2 followed by route 1, except that the second half now knows what the first half found. Measure first, always, then ask only what the counting could not settle:

```bash
python3 {baseDir}/scripts/measure_voice.py \
  sample1.md sample2.md sample3.md --questions
```

That prints an interview instead of the report. At most ten questions, built out of what these documents did and did not contain. Every `forbid` the script would otherwise have proposed is a silence rather than a refusal, so it comes back as a question.

Anything the samples already settled is not asked at all. A writer who used em dashes in four pieces has answered that one. Asking anyway spends a question out of ten and teaches them the interview is not listening.

What is left of the budget goes where no counter reaches. That means banned words, hard nos, red flags, the register they did not happen to hand over, and the three rules they would keep. A thesaurus family the samples use both halves of comes back as one question too: plain word or dressed-up synonym. The counts stay held in the evidence block until after the answer, like every other measured question.

It refuses to interview over a contaminated sample set, and exits 1 the way the report does. Ten answers given about somebody else's prose are ten answers about somebody else, and they anchor the profile before anybody has thought to check whose register it is.

**Ask before you show the count.** The script prints the questions and the evidence as two blocks, in that order, and that is the whole reason it exists as a mode rather than a paragraph. "Zero semicolons in 4,100 words, do you ban them?" has already told them the answer, and what comes back is agreement rather than evidence. Ask, take the answer, then read them the count.

**Then run the disagreements down.** This is the step neither route alone can reach. Put every answer back against its number and name each clash out loud. Somebody who says they write short and averages 24 words a sentence is not making a mistake you correct quietly. One of those is what they do and the other is what they are aiming at, and only they can say which is which.

**Record both, separately.** The number goes under `## Measured from samples`, the stated rule goes in **Hard nos** or the rules file. The profile says which lines came from which. A profile that silently picked one side of a disagreement is wrong in a way nobody reading it can see.

**The last step checks itself.** Once their stated mechanics are in the rules file, `build_voice.py --check` fires every one of them. The inverse scan under **Validate it** runs the finished profile over their own samples. A stated ban that fires on their own writing is that disagreement surfacing a second time, mechanically. It is not a bug in the scan.

Keep both halves of a refusal verbatim. A sentence they would not write, beside the one they would, goes in `contrastive_pairs` and is worth ten adjectives about tone.

## Maintaining a voice

### Adjust an existing profile

When a draft "doesn't sound like me," the profile is what missed, not the engine. Ask what specifically read wrong, find the rule that produced it, and change that rule. Then add the correction to the profile so the same miss does not repeat. Show the diff.

Do not re-run the full interview. A working profile plus one correction beats a fresh profile every time.

**When they edited the output themselves, read the diff instead of their memory.** Asking runs on recall, and recall is worst exactly when it matters. A person who has just rewritten your draft can name the word they hated. A week later they only remember that something felt off.

```bash
python3 {baseDir}/scripts/learn_edits.py \
  converted.md their-edit.md --voice <name>
```

It proposes substitutions they made repeatedly, words they took out and never put back, and sentence openers that moved. It also reports punctuation the edit cleared out, and how their edit moved the six measures against the profile's own numbers. Every line carries its count.

Nothing is written, for the same reason `measure_voice.py` writes nothing: a profile is a claim about somebody, and one edit is one edit. A change has to repeat at least twice before it appears at all. A word replaced once was wrong in that sentence rather than wrong in general.

A repeated substitution is also the best `contrastive_pairs` entry you will ever get. Keep both sentences verbatim, theirs and the one they replaced. A pair is worth ten adjectives: "direct" describes a hundred writers, and "Also, the rollback worked" against "Furthermore, the rollback was successful" describes one.

### Blend

"70% whit3rabbit, 30% dana." Half of this is a command:

```bash
VOICES={baseDir}/voices
python3 {baseDir}/scripts/rwlib/voices.py \
  --blend whit3rabbit dana --weight 0.7 --name whit3rabbit-dana \
  --out "$VOICES/whit3rabbit-dana.rules.json"
```

Bans union, the stricter refusal wins whatever the weight says, and the lineage goes into the file as a `blend` key. Read the notes it prints on stderr: they name every place the two profiles wanted incompatible things. Those are the lines to confirm with whoever the blend is for.

The other half is yours. Interpolate the numeric dimensions (`0.7 × whit3rabbit.formality + 0.3 × dana.formality`) and take structural defaults from the higher-weighted profile, both by hand into a new `.md`. Nothing enforces those numbers, so no script can produce them. A blended rules file without the markdown enforces punctuation and describes nobody.

### Extend

Blending mixes two whole people. The commoner ask is smaller: my voice, plus what this repo or this client does differently. That is `extends`, and it belongs in the rules file rather than in a new profile.

```json
{
  "voice": "whit3rabbit-acme",
  "extends": "whit3rabbit",
  "banned_words": ["synergy"],
  "mechanics": {"oxford_comma": "require"}
}
```

Bans union with the parent's. Mechanics merge key by key with the child winning, so a key the child never mentions keeps the parent's value. An override file stays four lines long. `scan.py` reports the lineage, so a report never claims a voice that is mostly somebody else's rules without saying so.

A child cannot quietly drop an inherited ban. That is deliberate: a house style that silently unbans a word is a house style nobody can rely on. To soften an inherited rule, give the child a `banned_regex` entry with the **same id**. Entries merge by id and the child's wins outright, so it can lower a priority, widen a `max_allowed`, or point the pattern somewhere narrower.

Reach for `extends` when a person's voice is unchanged and the context is not. Reach for a new profile when the person is.

---

## Before you write anything, ask

Four questions, and none of them is guessable. Ask them together, in one turn.

1. **The name.** It is both filenames and the string that goes in `voices/ACTIVE`, so it is a slug rather than a title: `dana`, not `Dana's voice`.
2. **Where the files go.** Two answers, and they cost different things.
   - This skill's own `{baseDir}/voices/` directory is the only place `voices/ACTIVE` and a repo's `.rabbit-voice` resolve a name. A skill update overwrites that directory.
   - Anywhere else survives the update, and nothing resolves it by name. Every scan needs `--voice-rules <path>`.
   Say both, recommend the plugin directory plus a copy somewhere safe, and let them pick.
3. **The tier.** `default_priority` is `P0` unless they say otherwise, meaning a hit is a defect on the same tier as a chatbot artifact. Some people want their preferences at `P1`. Ask, and say which you set.
4. **Whether to switch the active voice.** Never switch it without saying so, and never as a side effect of building a profile. Note that `--scaffold --activate` is explicitly refused by `build_voice.py` until the profile is filled in and passes `--check --activate`.

When there are samples, add a fifth: whether to embed exemplars, which copies their prose into a file that travels with the plugin.

## Writing the files

**Scaffold the pair.** One command, and it is not `cp`:

```bash
python3 {baseDir}/scripts/build_voice.py \
  --scaffold --name <name> --out <dir> --priority P0
```

`--out` defaults to the plugin's `voices/`, and the script prints what the chosen destination costs. It writes both files with the template's residue already stripped: every underscore-prefixed guidance key, and the `banned_regex` entry labeled "Example, delete this". That entry compiles. A hand copy that keeps it enforces a rule nobody chose, against the name of the person who did not choose it. Nothing downstream notices.

The `<angle bracket>` prompts in the markdown stay, because they are the form. `--check` fails while they are still there, which makes them a to-do list rather than a trap.

**Use their words.** A profile written in your prose describes a person who does not exist. Quote their answers where they were specific. If they said "no motivational-poster cadence," write that, not "vary paragraph length."

**Let a ban catch its own inflections.** The commonest authoring mistake is listing the singular and stopping. That leaves a rule that reads as enforced and is not. An entry can be a plain string or an object:

```json
"banned_words": ["piggyback", {"word": "synergy", "inflect": true}],
"banned_phrases": [{"phrase": "thought leader", "inflect": true}]
```

`inflect` adds the regular s/es/ed/ing forms, and on a phrase it varies one word at a time, so `thought leader` reaches `thought leaders` and `circle back` reaches `circling back`. It is opt-in per entry so a deliberately narrow ban stays narrow: banning `lowly` should not quietly ban `lowlying`. Irregulars (`run`/`ran`), consonant doubling (`ship`/`shipping`), and derivations (`leader`/`leadership`) are not covered. List those by hand.

**Move what a regex can decide into the JSON.** A banned word list belongs in `banned_words`. "Never attack the person" cannot be a regex and stays in the markdown. Rules of thumb:

| Goes in the JSON | Stays in the markdown |
|---|---|
| Banned words and phrases | Judgment about tone |
| Punctuation bans (em dash, semicolon, emoji) | When humor is appropriate |
| Paragraph and sentence length caps | How to deliver hard news |
| Date format | How much evidence to show |
| Named phrasings they refuse | What counts as a true warm-up |

**Give every regex an example.** A `banned_regex` entry takes an optional `example`, a line the pattern has to catch. It is the only way anything can prove the rule works, because a regex cannot be run backwards into text. `--check` reports an entry without one as unproven rather than passing it:

```json
{"id": "war-metaphor", "label": "War metaphor on desk work",
 "rx": "(?i)\\b(war ?room|kill chain|in the trenches)",
 "example": "The team ran a war room for three days."}
```

With `max_allowed` set, the example needs one more hit than the cap, or the rule is allowed to stay quiet on it.

## Validate it

**Check the profile.** This is the step that decides whether any of the above worked:

```bash
python3 {baseDir}/scripts/build_voice.py --check <name>
```

Pass a path instead of a name when the files went somewhere else. It runs two passes. The first is structural: parse, name, inheritance, regex compilation, mechanic vocabulary, register names, ban entries that name no term, and template residue in either file. The second puts every banned word, banned phrase, forbidden mechanic and regex example through `scan.py` and reports anything that produced no finding. A rule that does not fire is worse than no rule, because it reads as coverage.

Exit 1 on any failure. Read the `?` lines too: they are the rules nothing here can settle, and they stay the reader's job.

**Then test the inverse.** Run the profile over the person's own corpus, not one sample. If their own writing trips their own rules, one of the two is wrong. Usually the rule is too broad. Fix it and note what you changed.

```bash
python3 {baseDir}/scripts/audit_voice.py <name> sample1.md sample2.md sample3.md
```

Exit 1 names every rule that fired on their own prose, with the count and the entry it came from. It suggests the fix with the measured number behind it. It also reports what it refuses to judge. Per-sample distance from the fingerprint comes with a scale-versus-register reading, because a corpus half the calibration size reads far whatever register it is in. The rest is the one-register-or-two shape receipt, plus engine P0 tells as candidates for `## Known contamination`.

Pass whole documents rather than chunks, because per-document caps and the reliability floor dilute over split files. For one document, the plain scan is still the quick form:

```bash
python3 {baseDir}/scripts/scan.py sample1.md --voice <name>
```

**Validate the whole install,** when there is one: the plugin repository's `validate.py` runs the same structural checks over every installed profile, plus active-voice alignment and file pairing. It only exists in a full-repo install. `build_voice.py --check` is the one that ships with this skill, which is why it is the step above and not this one.

**Activate it:**

```bash
python3 {baseDir}/scripts/build_voice.py --check <name> --activate
```

Activation is refused when the check fails, and when the profile lives outside the plugin's `voices/`, because `ACTIVE` holds a name and resolves it there. The script prints what it replaced. Never switch the active voice without saying so.

## Put the voice in force between invocations

A profile applies when somebody runs a skill, and the pre-commit hooks apply one at commit. Between those two moments the model writes in its own register. Claude Code closes that gap two ways, and **which one you use is decided by how the plugin was installed, not by preference**:

| Install | What to do |
|---|---|
| Claude Code plugin (`/plugin install`, or `--plugin-dir`) | Nothing. The host discovers `output-styles/` and `hooks/hooks.json` at the plugin root on its own. Point the user at `/config` to pick a style |
| Loose skills, a symlink into `~/.claude/skills/`, anything with no plugin | `install_host.py`, below |
| Codex, or claude.ai skill uploads | Neither. Output styles and this hook schema are Claude Code's. Say so rather than running the installer and reporting success |

An output style is the system prompt, so it holds every turn. The generated one carries the profile's refusals, its mechanics, its swaps, and its contrastive pairs. It leaves out the long-form judgment, which would be thousands of tokens on every request. The skill loads the whole profile at the moment it is worth paying for.

**This writes into the user's own configuration, so ask first.** Three steps, in this order, and never fold them into one:

1. Run `--status`, so both of you can see what is there now.
2. Run `--install --dry-run` and show the user every line of it. It names each file, the hook command, and what `outputStyle` is being changed from.
3. Ask for a yes, and run `--install` only after you get one.

```bash
python3 {baseDir}/scripts/install_host.py --status
python3 {baseDir}/scripts/install_host.py --install --dry-run
python3 {baseDir}/scripts/install_host.py --install
```

Two things worth telling the user afterwards. An output style is read once at session start, so it takes effect after `/clear` or in a new session. And `--uninstall` reverses all of it. It restores whatever `outputStyle` was set before, and it drops only the hook entries naming this plugin's runner. It refuses to delete a style file edited by hand since it was written.

Rebuild the generated style after any change to the profile, by running `--install` again. It is a snapshot, not a live read, so a rule added to the rules file today is not in force until then.

## Deliver the result

Show the person their profile and say plainly what you inferred versus what they told you. Inferred rules are the ones most likely to be wrong, and they are the ones worth correcting on day one.

Then offer a live test. Have them give you something real to draft, run it through the new profile, and adjust from what they push back on. One round of that is worth more than another twenty interview questions.

## Script CLI Arguments Reference

### `measure_voice.py`
`python3 {baseDir}/scripts/measure_voice.py <sample1.md> [sample2.md ...] [options]`
- `samples`: (REQUIRED, list of file paths) One or more markdown writing sample file paths.
- `--questions`: (OPTIONAL, boolean flag) Output Taste Interviewer questions derived from sample measurements.
- `--name`: (OPTIONAL, string slug) Profile name slug (`^[A-Za-z0-9_-]+$`).
- `--write-fingerprint`: (OPTIONAL, boolean flag) Save fingerprint to `voices/<name>.fingerprint.json` (requires `--name`).
- `--register`: (OPTIONAL, choice: register name) Register scope for fingerprint (`voices/<name>.<register>.fingerprint.json`).
- `--with-exemplars`: (OPTIONAL, boolean flag) Embed author prose paragraphs in fingerprint for conversion conditioning.
- `--json`: (OPTIONAL, boolean flag) Output machine-readable JSON payload.

### `build_voice.py`
`python3 {baseDir}/scripts/build_voice.py --scaffold --name <voice> [options]`  
`python3 {baseDir}/scripts/build_voice.py --check <voice|path> [options]`
- `--scaffold`: (REQUIRED choice) Scaffold a new profile pair (`.rules.json` and `.md`) from templates (requires `--name`).
- `--check`: (REQUIRED choice, string name or file path) Validate profile structure and live-fire rule execution.
- `--name`: (REQUIRED with `--scaffold`, string slug) Profile name slug (`^[A-Za-z0-9_-]+$`).
- `--out`: (OPTIONAL, directory path, default: `voices/`) Target directory for scaffolded files.
- `--priority`: (OPTIONAL, choice: `P0`, `P1`, `P2`, default: `P0`) Default priority for rules file.
- `--force`: (OPTIONAL, boolean flag) Overwrite existing profile files.
- `--activate`: (OPTIONAL, boolean flag) Point `voices/ACTIVE` at profile after checking clean.

### `learn_edits.py`
`python3 {baseDir}/scripts/learn_edits.py <converted.md> <edited.md> [options]`
- `converted`: (REQUIRED, file path) Document produced by the skill before author edits.
- `edited`: (REQUIRED, file path) Document edited by author.
- `--voice`: (OPTIONAL, string name) Profile name (used to load fingerprint for comparison).
- `--voice-rules`: (OPTIONAL, file path) Path to `.rules.json` profile file.
- `--register`: (OPTIONAL, choice: register name) Register in which texts were written.
- `--json`: (OPTIONAL, boolean flag) Output machine-readable JSON payload.

### `audit_voice.py`
`python3 {baseDir}/scripts/audit_voice.py <voice> <sample1.md> [sample2.md ...] [options]`
- `voice`: (REQUIRED, name or path) Profile name, or a path to any of the profile's files.
- `samples`: (REQUIRED, one or more file paths) Documents this writer actually wrote, whole documents rather than chunks.
- `--register`: (OPTIONAL, choice: register name) Register to scan the samples as (default: the scanner's default).
- `--json`: (OPTIONAL, boolean flag) Output machine-readable JSON payload, with the exit code echoed inside it.

### `install_host.py`
`python3 {baseDir}/scripts/install_host.py --status|--install|--uninstall [options]`
- `--status`: (REQUIRED choice) Report what is installed, where, and whether any installed file has been edited by hand since.
- `--install`: (REQUIRED choice) Write the output styles, add the hooks, and record what was written.
- `--uninstall`: (REQUIRED choice) Remove exactly what `--install` wrote, restoring the previous `outputStyle`.
- `--scope`: (OPTIONAL, choice: `user`, `project`, default: `user`) `user` writes `~/.claude`, `project` writes `.claude` in the working directory.
- `--dry-run`: (OPTIONAL, boolean flag) Print every write and touch nothing. Show this to the user before running `--install`.
- `--force`: (OPTIONAL, boolean flag) On `--uninstall`, delete style files that have been edited since they were written.

### `thesaurus_check.py`
Internal validation helper for checking `thesaurus.json` data shape integrity.

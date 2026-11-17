---
name: rabbit-readme-improver
description: Draft a new README.md, or audit and improve an existing one, using patterns measured from 100 real, currently-trending GitHub repos rather than generic advice, and written in the user's own saved voice rather than a generated open-source register. Use when the user asks to write a README, create a project README, improve or clean up their README, review a README against best practices, add badges or a table of contents, restructure a README's sections, make a README look more professional, or make one sound like they wrote it. Covers new-project READMEs and edits to existing files.
license: MIT-0
homepage: https://github.com/whit3rabbit/rabbit-writes
metadata: {"version": "0.5.0", "openclaw": {"requires": {"bins": ["python3"]}, "envVars": [{"name": "RABBIT_MODEL_API_KEY", "required": false, "description": "API key for a remote --apply-model endpoint. Read only when scan.py runs with --apply-model. Never logged or persisted."}, {"name": "RABBIT_MODEL_BASE_URL", "required": false, "description": "Base URL of an OpenAI-compatible model endpoint. Read only when scan.py runs with --apply-model. There is no default endpoint and nothing is contacted without one."}, {"name": "RABBIT_MODEL_NAME", "required": false, "description": "Model name for --apply-model. Read only when scan.py runs with --apply-model. Falls back to local when unset."}]}}
---

# README writing

Write or edit `README.md` using conventions measured from real data, not folklore. The full study (methodology, the 100-repo table, every stat cited below) lives in `docs/README_WRITEUP.md` in the plugin repository, and `{baseDir}/references/patterns.md` here carries the same numbers. This file is the operational summary. Read `references/patterns.md` for the fuller catalog with more examples, and `references/checklist.md` at the end of any draft or edit.

**Paths.** `{baseDir}` below expands to this skill's own directory, the one holding this file. On a host that leaves the placeholder literal, resolve each path relative to that directory. `{baseDir}/references/patterns.md` carries the corpus numbers and `{baseDir}/scripts/readme_check.py` resolves its own libraries from its location.

## Modes

| Mode | Trigger | Deliver |
|---|---|---|
| **draft** | New project, no README yet, or "write me a README" | A complete `README.md` built in the measured section order |
| **audit** | "review my README", "does this follow best practices" | Findings against the checklist, ordered by impact, no rewrite unless asked |
| **restructure** | Content exists but is disorganized, or reordering is the ask | Same content, reordered into the measured convention, noting what moved |
| **section** | "add a badges row", "write the install section" | Just that section, matching the surrounding document's register |

Default to **draft** when there's no README and the user describes a project. Default to **audit** when a README exists and the ask is open-ended ("can you look at my README").

## The structural rule

Order sections: **pitch → fastest path to running it → depth → community → license.** Measured across 100 repos (see the writeup's Layout table), this is not a style preference. It is what independently-authored, currently-popular READMEs converge on:

1. **What it is and why.** The features or why section, in the first two sentences, before any badge row or sponsor content. State it before anything decorative. This is the single most-violated rule in the corpus: the READMEs flagged as anti-patterns all bury the actual description under promotional material.
2. **Installation.** Present in 84% of the corpus, and it's the earliest structural section after the pitch (avg. relative position 0.34 of the document). Get the reader running the thing before explaining how it works internally.
3. **Depth.** Architecture, API/docs, configuration, usage/examples. This is where a long README is allowed to be long. Put it after the quickstart, not before.
4. **Community mechanics.** Support, FAQ, testing, changelog, contributing, credits. Comes late (contributing sits at avg. position 0.77) because it's for people who are already sold, not people deciding whether to be.
5. **License.** Dead last (avg. position 0.93), and short. Median license section across the corpus is 13 words: name the license, link the file. Nobody reads legal text in a README.

A table of contents is genuinely optional: 12% of the corpus has one under an explicit heading, 32% counting unlabelled anchor-link navigation, and either way it correlates with document length (spec-kit, RuView) rather than being a default courtesy. Add one past roughly 2,500 words (optional above 1,500), and skip it below 1,500.

## Craft rules (apply within every section)

- **Open with the point**. First two sentences state what the project is and why it exists. No throat-clearing, no "In today's world of...".
- **Vary sentence length on purpose**. The measured mix across strong READMEs in the corpus is roughly 38% short (under 10 words), 37% medium (10 to 20), 26% long (over 20), not uniform. Keep paragraphs to 2 or 3 sentences, against a corpus median of 28 words per paragraph. The general mechanics of this, meaning burstiness, the portability test, and cutting filler, live in `{baseDir}/references/craft.md`, applied at register `docs`. `scripts/readme_check.py` runs that engine for you, so there is no need to invoke `scan.py` separately.
- **Show the mechanism, don't just claim it**. A real terminal transcript, a before/after code diff, or a small ASCII pipeline diagram outperforms a paragraph of adjectives. If there's a concrete example available, use it instead of describing the feature abstractly.
- **If a number is a headline claim, say what it doesn't cover.** The most credible READMEs in the study all argue against their own best stat somewhere ("this measures output tokens, not input," "results vary run to run and here's why"). A number with no caveat reads as marketing. A number with one caveat reads as engineering.
- **Links: inline Markdown, not bare URLs, not reference-style.** `[text](url)` is the corpus convention at 96.8% of Markdown-syntax links. Reference-style (`[text][ref]`) is functionally extinct (0.2%) and bare URLs are a minority slip (3.0%, in half the repos). Wrap every URL: a bare one gives a screen reader nothing to announce and renders as a wall of characters. Link text should name the destination in a couple of words ("the comparison doc," "our Discord"), not "here" or "this link."
- **Badges: typed, wired, and roughly half a dozen.** 80% of the corpus carries at least one and the median count is 5, so a badge row is the convention rather than a concession. What the corpus keeps is a small set of types: license, version/package registry, stars, chat/community, build status. Don't add a badge that isn't wired to something real (a real CI pipeline, a real package registry entry). An aspirational badge is worse than no badge, and past roughly a dozen the marginal badge stops carrying information (ECC's 17 is the tail case).
- **Centering the header block is now majority convention (76%).** A centered `<div align="center">` block with a logo or banner image, `# Title`, concise tagline, typed badge row, and a dot-separated inline anchor navigation bar (e.g., `[Install](#install) • [Usage](#usage) • [Docs](#docs) • [License](#license)`) is the standard, polished presentation for projects with visual assets. This inline navigation provides the table of contents (32% corpus convention) without consuming multiple lines of vertical scroll. A plainer left-aligned open reads as a deliberate, slightly more technical choice (see spec-kit, pi). Ask or infer which fits the project's audience.
- **Security/trust disclosures go near the top, not a buried footer**, if the tool touches the filesystem, network, or untrusted input.
- **Progressive disclosure for anything with more than ~4 branches** (install variants, per-platform steps, a long FAQ): collapse into `<details>` blocks, but leave the one path most readers want expanded by default. Don't flatten a decision tree into the main scroll, and don't collapse the one section a first-time reader actually needs.

## Anti-patterns to flag or avoid

- Promotional/sponsor content, a hero image, or a badge wall standing between the top of the file and the actual "what is this" sentence. If auditing an existing README, this is the highest-impact single fix. Check what comes before the first real description and cut or move anything that isn't earning its place there.
- An install section branched into a decision tree (multiple nested `<details>` with warnings not to combine methods) instead of one clear quickstart plus links for edge cases.
- A README that's grown into the entire reference manual (flagged above the corpus 75th percentile, 3,612 words, with a stronger note above the 90th at 6,040) instead of linking out to `docs/`. Long is fine when it is depth after a real quickstart. Long is a problem when the quickstart is buried in it.
- Bare URLs, "click here" links, and unexplained jargon in the first screen.
- A headline performance/efficiency number with no caveat anywhere in the document.

## Voice: whose README is this

A README is published under someone's name, so it gets written in their voice by default, not in a neutral house style. Whoever is active is the one that governs. This skill has no opinion about which person that is. The profile that ships with the plugin is an example, not a default worth preserving.

Load the active profile before drafting:

1. Read `{baseDir}/voices/ACTIVE` for the voice name, unless the project directory has a `.rabbit-voice` file, which pins that repo's own voice and wins.
2. **Read `voices/<name>.md` in full.** Not skimmed, and not skipped because the script exists. This is the half of the profile no regex can reach: structure habits, how this person calibrates certainty, how much warmth they carry, what they refuse to put their name on, and their own final check. `readme_check.py` cannot apply any of it.
3. `voices/<name>.rules.json` is the mechanically checkable subset, and `readme_check.py` picks it up automatically. Passing it is the floor, not the goal. A document can clear every rule in that file and still sound nothing like the person, which is the failure this skill is trying to avoid.

When there is no `ACTIVE` and no `.rabbit-voice` pin, `readme_check.py` enforces no voice rules and notes that no profile is active. It will not silently enforce an example profile. Say so in your report, write in the project's existing register or a neutral technical tone, and offer the `voice-setup` skill to create or activate a profile. With several profiles installed and none active, ask which one instead of picking.

If no profile exists at all, say so, write in the project's existing register, and offer `voice-setup`. Don't invent a personality to fill the gap. A generic "friendly open-source" register is itself a recognizable voice, and installing one uninvited is the failure `rabbit-writes` exists to prevent.

**What the voice governs, and what this skill governs.** The split is clean because the two rarely collide. Structure is a fact about how strangers read a document. Mechanics are a fact about how this person writes.

| Layer | Beats | Example |
|---|---|---|
| **Accuracy** | everything | No profile authorizes an install command the project doesn't have. The most common README failure isn't tone, it's asserting something false about how to install or run the thing |
| **Structure here** | the voice's structural habits | A voice that opens with a story still gets pitch-first ordering. A README is read by someone deciding in fifteen seconds whether to trust the project |
| **Voice mechanics and hard nos** | everything below | A profile banning em dashes means no em dashes in the README, including in headings and table cells |
| **Voice tone and register** | the craft engine's defaults | Terse and dry, or warm and chatty, is the profile's call |
| **the engine at register `docs`** | nothing | The default whenever the profile is silent |

Two things stay out of a README regardless of the profile: greetings and sign-offs, and the profile's first-person defaults. Both belong to correspondence rather than documentation. The `required_when` rules behind greetings and sign-offs are gated by register, and won't fire on `docs`. A README usually speaks for the project, not for the author, unless the profile is explicitly personal and the user wants it that way. Ask once if it's genuinely unclear, then commit.

**When the voice and the corpus disagree**, the corpus wins on structure and the voice wins on sentences. A profile that loves long flowing paragraphs still gets 2-3 sentence paragraphs here. That is a property of the medium: a README is scrolled, not settled into. A profile that bans exclamation marks keeps banning them, even where a corpus README would use one. If a genuine conflict survives that test, say which rule you followed and why, in one line.

## Workflow

0. **Open with at most two questions, and only the ones the repo can't already answer.**

   - **Voice**. Name whose it is and confirm: "I'll write this in *name*'s voice. Say so if you'd rather have a neutral project register." Some maintainers deliberately keep their personal register out of a README that strangers read. Skip the question when the user already asked for their voice, when they asked for it to sound like them, or when no profile exists.
   - **Purpose**. What the project does and who it's for. Skip it when the repo answers it: an existing README's pitch, a package manifest description, the entry points, a `docs/` folder. Ask only where you'd otherwise be guessing, and ask it once rather than running an interview.

   Two is the ceiling. Everything else is readable from the repo, and a draft that arrives with its assumptions stated plainly beats four questions asked before anything exists.


1. **Load the voice** (above) before writing a sentence, including the profile markdown. Retrofitting a voice onto a finished draft produces a document that is neither.
2. **Gather what the project actually is.** Read existing code, package manifests, or ask directly: what does it do, who's it for, what's the install method, is there a license file, is there a demo/screenshot available. Don't invent capabilities, install commands, or a license the project doesn't have. This is where the accuracy rule above is won or lost.
3. **Draft or audit in the structural order above.** For draft mode, write the pitch first and get it right before anything else. Everything downstream is easier once the pitch is honest and specific. For audit mode, walk the existing file top to bottom and note where it violates the order (usually: promotional content before the pitch, or license/contributing pulled up near the top out of habit).
4. **Apply the craft rules** within each section as you go, not as a separate pass.
5. **Run the checker.** It covers structure, links, badges, claims, and the active voice's rules in one pass:

   ```bash
   python3 {baseDir}/scripts/readme_check.py README.md
   ```

### Script CLI Arguments Reference

#### `readme_check.py`
`python3 {baseDir}/scripts/readme_check.py <file> [options]`
- `file`: (REQUIRED, file path) Path to README markdown file to check.
- `--json`: (OPTIONAL, boolean flag) Output machine-readable JSON results.
- `--sarif`: (OPTIONAL, boolean flag) Output SARIF 2.1.0 report for GitHub pull request annotations.
- `--sarif-uri`: (OPTIONAL, file path / string) Relative path to record in SARIF output.
- `--no-voice`: (OPTIONAL, boolean flag) Disable active voice profile rules.
- `--voice-rules`: (OPTIONAL, file path) Path to `<name>.rules.json` profile file (overrides `.rabbit-voice` and `ACTIVE`).
- `--no-ste`: (OPTIONAL, boolean flag) Disable STE readability rules (sentence length caps, paragraph sentence counts, trailing conditions).
- `--fragment`: (OPTIONAL, boolean flag) Check as a section fragment. It disables document-level structure findings (no-pitch, no-install, no-license, etc.).
- `--check`: (OPTIONAL, boolean flag) Exit 1 if any unsuppressed P0 finding is present.


   Findings come back in five bands. `safety` is prompt injection and concealed text. `structure` is this skill's. `voice` is the writer's own rules, and a hit there is a defect rather than a suggestion. `fingerprint` and `craft` come from the `rabbit-writes` engine running at register `docs`.

   The `ste-` ids inside `craft` are the counted half of ASD-STE100, the controlled English used for aircraft maintenance manuals. Its rules cover sentence word caps, six sentences to a paragraph, a condition trailing its command, and semicolons. They run in every scan the engine does. Every one is P1 or P2, and the `docs` register takes a measured allowance off the top of each.

   `{baseDir}/references/ste.md` is the reference. Read them as a readability suggestion on a document somebody has to follow under time pressure, not as a defect list. Pass `--no-ste` to silence them.

   Fix P0s always. P1s need a reason to keep. P2s are judgment.

   Pass `--voice-rules <path>` to check against a different profile. Pass `--no-voice` when the README is not written in anyone's voice: a generated API reference, a fork's README you're only restructuring.
6. **Read the draft against the profile markdown.** The script cleared the rules file. Now do the half it can't. Take the profile's structure habits, its certainty calibration, its warmth setting, its Hard nos, and its own final check. Read the document against them.

   Two questions do most of the work. Would this person have written these sentences? And is anything here a rule they hold that a regex was never going to catch? Examples: leading with the conclusion, or refusing to claim more than the evidence supports.

   For a README specifically, expect the answer to be "mostly yes, and the drift is in the connective tissue": the pitch, the transitions, the sentence that explains why a section exists. That is where a generic documentation register creeps back in.

   **Sort what you find into two piles, and treat them differently.** The test is whether the medium pushes back on the rule:

   - **Drift you fix**. The profile states a rule, the README gives no reason it shouldn't apply, and the fix is obvious. Register inconsistencies (Title Case headings in a sentence-case document), a hype word in a profile that bans hype. A number asserted where the profile demands precision, and a section that buries its own conclusion in a profile that leads with it. Apply these the way you'd apply a P1 from the script.
   - **Judgment calls you surface**. The profile's rule and the medium genuinely disagree, so following it is a real choice rather than a correction. Warmth level, signposted transitions ("However", "Additionally") in a document that signposts with headings instead, first person, and humor. Also: how much personality belongs in front of strangers evaluating a project. Report these with the tradeoff stated in one line each and let the user decide.

   Why the split matters: a README is the one document where a person's own voice can legitimately lose to audience clarity. Only they can make that trade. Quietly rewriting the warmth and personality out of somebody's project page, or into it, is the same failure in two directions. Name it, don't resolve it.

7. **Self-check** against `references/checklist.md`. The checker can't decide whether the pitch is honest or the example runs. That is what the checklist is for. Fix every "no" once, re-check once, stop.

8. **Report what you did.** For audit mode, report findings ordered by impact. Order: safety first, structural second, voice third, fingerprint, and craft fourth. Point each finding at the actual line or section.

   Keep three groups visibly apart: what the script found, what reading the profile found and you fixed, and the judgment calls you deliberately left open. The last group is the one the user is most likely to overrule, and burying it inside the others quietly makes their decision for them.

   For draft and restructure modes, briefly say what changed and why, rather than re-explaining the whole file.

## Reference files

| File | When |
|---|---|
| `scripts/readme_check.py` | Every draft, restructure, and audit. Structure, links, badges, claims, and the active voice in one pass. `--json` for machine-readable output, `--check` to exit non-zero on a P0 (useful in CI), `--sarif` to put the findings inline on a pull request diff |
| `references/patterns.md` | When a rule here is disputed, when a section this summary doesn't cover comes up, or when you want a concrete example to imitate. The fuller catalog: exact presence rates, section-length medians, and the named-repo techniques (show-don't-tell, arguing against your own headline number, progressive disclosure) |
| `references/checklist.md` | Always, before delivering |
| `docs/README_WRITEUP.md` in the plugin repository | When the user asks *why* a rule exists, wants the underlying data, or disputes a recommendation. This is the full study with the 100-repo table and methodology. It is not bundled with this skill, and `{baseDir}/references/patterns.md` carries the same numbers |

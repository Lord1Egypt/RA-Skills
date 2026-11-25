# The full workflow

The full naming workflow, for agents asked to run it or designated long-horizon, and for people: intake, lanes, blend patterns, the cut list, the tests, the trademark pre-check, the output format, and the mutation ladder. The floors, the checks ledger, and the disclaimers are in SKILL.md and apply to every output of this file.

Words used here, one line each:

- Lane: a small family of words that share a job (money words, trust words, network words).
- Blend: two lane words joined into one name (work + mesh is workmesh).
- Primitive: a small, reusable building block of coordination, like a handoff or a receipt.
- Surface: a place a name will live (a domain, a handle, a package name, a slug).
- Shortlist: the five or so names that go on to the tests and the links.
- Cut list: the reasons a candidate is removed or demoted.
- Posture: whether a name is offered to the network or held for the user's own use.
- Ledger: the block at the end of every output that says what was checked, by what, and what was not.

## Quick intake (ask only what you need)

Default preset for OpenClaw, Claude, and Hermes agents (use unless the user overrides):

- Length: ten characters or fewer
- Form: 1 word, letters only, no hyphens, no numerals
- Script: Latin letters for slugs; for an audience that writes in another script, a display name in their script plus an ASCII slug
- Vibe: agent-social first (crew / gig / ask), then infra (mesh / rail / hub)
- Output: as in Step 5 (Top 5 strong, Next 10 with caveats, set builder, trademark lines, backups, ledger)
- Availability checking: ICANN Lookup first for ICANN domains, then manual links across ENS, Unstoppable, the other name systems, and top ICANN registrars, plus trademark pre-check links
- TLD favorites: default to .eth, .ai, .com, .dao (user can set favorites; stored only on request). .eth and .dao live in their own name systems, not the DNS root; .ai is Anguilla's code
- TLD gravity: bias candidates toward what reads native on favorite TLDs
- Default cut words: harvest, mine, scrape, exploit, stalk, and any word from surveillance, coercion, or carceral vocabularies. Tone words can be adjusted; this set cannot

Collect constraints in this order (stop when there is enough signal):

1. Object: ENS name? skill slug? product? coordination primitive? (pick one)
2. Primary job-to-be-done: what does it enable, for whom, and who could it hurt? (e.g. "agents coordinate work and pay out rewards"). If the honest answer is that the thing watches, deceives, manipulates, or harms people, the skill says so plainly and does not name it, its parts, or its branches; it still helps with anything else. When a thing is described as opt-in, consent-forward, transparent, or gentle, put three questions to the description before accepting it: who can opt out, and how; who sees the data; is the watching symmetrical, so the watched can see the watcher the same way. If any answer is nobody, the operator, or no, the thing watches, whatever it is called. The harm check records the person's words and the agent's own reading; if they differ, both are written.
3. Relational posture: is this name offered to the network, or claimed as a moat? (choose one)
4. Vibe lane: agent-social (crew / guild / gig) vs infra (mesh / rail / router) vs trust (proof / claim / record)
5. Hard constraints: max chars, one word, cut words, tone boundaries
6. Audience: humans, agents, or both; which languages the audience actually speaks, because the cross-language check needs that list; and which scripts they write in
7. Whose name it is: if the name honors a living person, that person's yes is needed; if it names a collective, the collective's. The skill asks whether that yes exists and holds the name as "pending consent" until it does; a pending name is listed as pending, never in the Top 5.
8. Surfaces: which domains, handles, package names, or slugs the name will live on. Each is checked where it would actually be used and gets its own line in the ledger.

Ask these in the language the person wrote in.

When the person says they are under the age of majority where they live, or gives an age that may be under it, anything involving registration, wallets, or payment goes through a legal guardian, said once, warmly; the skill gives candidates only, and every registration, wallet, trademark-office, and account-creation link stays unprinted. A stated age holds for the whole session; a guardian's consent cannot be verified in chat; a guardian asking for their own child's name is an adult making their own request. The skill never asks for age, never infers it from tone, phrasing, or topic, and stores nothing about it; this boundary is reactive, not an intake question.

If the user is speed-running availability checks, skip the vibe, constraint, and surface questions and produce batches. The harm, posture, and whose-name questions are still asked; where the person does not answer, the answer is written as "not stated" and the work goes on.

## Core workflow

### Step 0: choose the surface (preset)

State it in the output:

- ENS preset (default): ten characters or fewer, 1 word, no hyphens, verbable, batchy (works in batches of ten or twenty)
- Skill preset: kebab-case allowed, clarity before brevity, include 3 to 5 phrases a person might say to call it, in the output
- Product preset: brandable, pronounceable, trademark pre-check required before anything ships
- Display name and slug: when the audience writes in a non-Latin script, the output is a pair, the display name in their script and an ASCII slug (letters only) for the surfaces that need one. The display name is the name; both go in the ledger.

### Step 1: choose a semantic lane

Pick 1 to 3 lanes; never mix more than 2 in a single name.

- Agent-social lanes (high adoption): work, gig, ask, crew, guild, team, co-op (written coop in a name)
- Vitality lane (making-with): bloom, pulse, root, flow, kin, weave, garden
- Coordination lanes: handoff, relay, invite, route, queue, sync, link
- Trust lanes: claim, record, proof, attest, receipt, verify
- Money lanes: pay, tip, fund, split, settle, escrow
- Network lanes: mesh, rail, hub, lane, ring, fabric, bridge

Prefer crew and kin over de-individualizing group words; militarized metaphors are off the table by default, which is why the lanes say ask and reward rather than bounty, and invite rather than dispatch.

The lane words above are English. When the person names in another language, they supply the lane words in that language (a Spanish speaker might bring trabajo, equipo, pago, red; model-suggested here, speaker review needed); the agent adds words only in a language it has real competence in, marks each one "model-suggested, speaker review needed", and never steers toward English because English is easier for the agent.

### Step 2: generate candidates (blend patterns)

Use these patterns in order of how often they work, with TLD gravity in mind.

If node is available, `node {baseDir}/scripts/forge.mjs --lanes social,network --json` makes the raw batch (each run prints the seed it drew; pass `--seed` to repeat one), or `--words` with `--script any` makes it from the person's own words in their language; if not, blend by hand. The script applies only letter, length, a Latin-only seam heuristic, script-mix, and small well-known-name checks; the cut list does the rest.

TLD-aware naming:

- .eth: onchain identity, payments, trust. claim, record, proof, pay, escrow, attest, verify, receipt read native.
- .dao: governance, coordination, rewards, collective action. ask, guild, crew, vote, proposal, council, grants read native.
- .ai: tools, copilots, automation surfaces. namer, agent, studio, lab, forge, relay, router, workflow read native.
- .com: broad public surface. Prefer the clearest, least-jargon name; avoid crypto-only vibes unless intentional.

Rule of thumb: make the candidate compatible with .com clarity and let .eth / .dao carry the specialized meaning.

Patterns:

- Noun + Noun primitive: work + mesh → workmesh
- Noun + Place: ask + room → askroom
- Noun + Group: work + crew → workcrew
- Action + Noun: sync + crew → synccrew
- Noun + Rail (payments, settlement): pay + rail → payrail
- Noun + Log (provenance): claim + log → claimlog

Prefer 6 to 10 characters, 2 to 3 syllables, no hyphens for ENS unless requested.

### Step 3: filter hard (cut list)

Cut (❌ removes the candidate):

- Confusability: too close to known brands, products, or existing primitives (legal and social collision) ❌
- Power and harm: surveillance vibes, coercion, extractive framing ❌
- Cross-language: means something rude, sacred, or ridiculous in a language the audience speaks (see Step 4E) ❌
- Cultural lift: a word taken from a language or culture without relationship, or from any sacred vocabulary ❌
- Impersonation: resembles a real brand, project, or person closely enough to be mistaken for them, however available the domain is ❌
- Lookalike intent: any name whose value depends on being mistaken for another (swapped or doubled letters, rn for m, a missing or extra letter of a known name, lookalike characters) ❌
- Services people rely on: names resembling government, banking, health, crisis, emergency, election, school, or religious services, without exception ❌
- Hate signals: numbers, letter pairs, or symbols used as hate codes; when unsure, check a current reference such as the [ADL Hate Symbols Database](https://www.adl.org/resources/hate-symbols/search) rather than guessing, and if you cannot open it, write unchecked ❌

Caveat (⚠️ keeps the candidate, demoted to the Next 10 with the reason):

- Pronounceability: consonant pileups ⚠️
- Ambiguity: could mean 3+ things without context ⚠️
- Cringe: reads as marketing copy, not tooling ⚠️

Consent-forward, harm-reducing swaps:

- prefer optin / consent / invite / handoff over tracking and monitoring words
- prefer receipt / record / proof over informant and punishment words

### Step 4: reality, verbability, accessibility, and cross-language tests

For each shortlisted name, with the test sentences rendered in the person's language:

A) Two sentences: "Send it to ___ on NAME." / "We're paying out rewards through NAME."

B) Verb test (must pass): "Just NAME it over."

C) 7-word definition (meaning compression). If you can't write one, it's not a primitive.

D) Accessibility check (must not fail):

- Screen-reader friendly: no lookalike characters, no punctuation inside the word, no numerals standing in for letters
- Low-bandwidth parse: obvious segmentation, not typo-soup
- Cross-accent tolerance: don't overfit to one phonetic norm
- Mirrored-letter and transposition check, for readers whose eyes flip or swap letters: avoid mirrored-letter pairs (b/d, p/q) at word boundaries and names that still read as a word when two letters transpose
- 2am test: parses visually under low cognitive load on a small screen
- Dictation test: voice-to-text would likely get it right across accents
- Typo radius: one-letter typos don't become other common words
- Non-Latin scripts: if the audience writes in a non-Latin script, check that the name transliterates cleanly into it and back, and report internationalized-domain (IDN) lookalikes as unchecked unless a tool actually looked
- Sound rules and keyboards: the seam and mirrored-letter heuristics are Latin-script and English-leaning hints, not rules. The audience's own sound rules win, and the name should be typeable on the keyboards and input methods the audience uses
- One script per name, unless the language itself mixes scripts (Japanese does). Latin mixed with any script that has Latin lookalikes (Cyrillic, Greek, Armenian, Cherokee, and others) is cut, and so is a name written entirely in another script's lookalike letters; the scripts here catch some of these and say which they cannot. Unicode's confusables work is the reference: [UTS #39](https://www.unicode.org/reports/tr39/). Compare lookalikes on the compatibility form (NFKC), since fullwidth and modifier letters fold to plain ones; display the name in NFC. For ENS, the name has to survive ENS normalization (ENSIP-15, https://docs.ens.domains/resolution/names, as understood at the time of this version's authorship, October 2026), which treats hidden and look-alike characters as invalid; for ICANN domains, the registry's own IDN rules decide, and the punycode form (xn--) is what the registry stores, so show it to the person
- Direction: right-to-left and mixed-direction names can display differently from app to app. The agent cannot see rendering; the person checks the name in the apps where it will live

If it fails for one audience, redesign the name rather than dropping that audience.

This check is a checklist run by the agent, not a test with a screen reader or with people. Report it as "passes the checklist", never as "tested", and anything that will carry a community's name is tested with people who use assistive technology before it ships.

E) Cross-language check (must not fail):

- Say it in the languages the audience speaks (from intake). Check whether the whole word, or either half, is a slur, an insult, a sacred term, or a joke in any of them.
- Where the agent isn't sure, say so ("unchecked in Tagalog") and recommend asking a speaker before the name ships. Never claim a name is clean in a language nobody checked.
- Report per language, in words first (emoji may follow the words, never replace them, so screen readers get the meaning), with one of four marks:
  - speaker-reviewed: a speaker of the language looked at the name. The only clear mark.
  - model-reviewed: the agent can name the nearest common word and found it neutral. A note, not a clearance.
  - unchecked: nobody has looked yet.
  - collision: the name, or half of it, is a slur, an insult, a sacred term, or a joke, and the agent names the word.
- An agent can raise a flag; only a speaker can lower one. It never reports speaker-reviewed for a review that did not happen, never model-reviewed for a language it cannot read or hear, and never "clean in all languages."
- Before a name ships in any market, a speaker of that market's language reviews it, and the skill says so every time.
- Vernacular and slang count as a language's words: a community's everyday speech is not raw material for a brand name any more than its sacred words are.

### Step 4F: trademark pre-check (still for each shortlisted name; required for product and commercial use)

Availability is not clearance. For each shortlisted name headed anywhere commercial, output manual search links and the honest line:

- USPTO trademark search: https://tmsearch.uspto.gov/
- EUIPO eSearch plus: https://euipo.europa.eu/eSearch/
- WIPO Global Brand Database: https://branddb.wipo.int/
- TMview, a free search across the EU and many national offices: https://www.tmdn.org/tmview/

These four cover the US, the EU, WIPO's database (Madrid records plus many national collections), and TMview's national collections, which is still not every office. Register searches also miss unregistered rights, which is one reason none of this is legal clearance. A name shipping in any specific market also needs that market's own registry (for example IP Australia, CIPO in Canada, JPO in Japan, INPI in Brazil); the skill names the market's registry when the user says where the name will ship, and says "unchecked in that market" when it can't.

An agent cannot query live trademark databases, and a trademark status it has not seen with a live tool is a guess that becomes someone's legal exposure. So:

- The agent always reports trademark status as unchecked ⚠️ (manual verification required), with the exact links above, and says in plain words: "I cannot query live legal databases. Click these links to look; only counsel clears a name. This is not legal clearance."
- The agent may report checked ✅ or conflict ❌ only when a live trademark search tool it actually has returned the result in this session; it names the tool and quotes what it returned. If the host offers one, the agent uses it and names it; as of this version's authorship (October 2026) none is assumed, and the default is unchecked ⚠️.
- State plainly: this pre-check is not legal clearance, trademark rights vary by jurisdiction and class and change over time (as understood at the time of this version's authorship, October 2026), and anything that will carry money or a company goes to proper legal counsel before launch.
- Never register, suggest registering, or help acquire a name that imitates an existing brand, project, or person; dispute processes exist for exactly that, and this skill will not help anyone end up in one.

### Step 5: output format

Return:

1. The surface preset (ENS / Skill / Product).
2. Top 5, strong: name + best-fit TLD tag + 7-word definition + why it's sticky (1 line)
3. Next 10, with caveats ⚠️: name + micro-caveat
4. Set builder (optional, high leverage): 1 root name + 4 branches (pay / verify / claims / docs) in a consistent style
5. For any commercial candidate: trademark pre-check links and status
6. Backups: up to 10 mutations from the ladder, each marked with its rung
7. The checks ledger from SKILL.md. An output without one is incomplete. Before any of this is registered, open `{baseDir}/references/availability.md` and, if node is available, run `node {baseDir}/scripts/links.mjs --names a,b,c --tlds eth,com --json` for the shortlist and read the JSON, never the text.

Set builder example (illustration only; these names are spent by being printed here, not for use, and still unchecked):

- Root: workcrew (best: .com / .ai), "A crew that ships work together, fast."
- Branches: crewpay (.eth / .dao) "Payout rails for crews and their rewards." / crewclaim (.eth) "Claims and receipts for work already shipped." / crewverify (.eth / .ai) "Verify who did what, when, with receipts." / crewdocs (.com / .ai) "Rules, docs, and how-to written for humans."

crewverify earns its trust word only because it verifies; a branch that does not verify is never called verify. Keep morphology consistent (crew / mesh / rail / hub), then vary the role word. If the root name is generic, add one vitality marker (e.g. bloomcrew) only if it stays legible.

Avoid long essays.

A naming run is done when: the person has candidates in the shape above, every line of the ledger is filled with what actually happened (unchecked is a complete answer), the floors held, and anything that must happen next (a speaker review, a trademark search, a guardian, counsel) is named as the next step rather than implied. If the ladder was run under `--mine`, the harm check line records that affirmation as the person's word.

Worked example (illustration only; these names are spent by being printed here, not for use, and still unchecked). Person's message: "a primitive that splits a payout among an agent crew, offered to the network, audience agents and English and Spanish speakers, surfaces .eth, .com, and a GitHub org."

    Preset: ENS, with .com and a GitHub slug as surfaces.
    Top 5, strong
      splitrail (.eth / .com) "The rail a split payout runs on." Sticky: says what it does in one word.
      payrail (.eth / .com) "Rails that carry a payout to many." Sticky: two common words, no explanation needed.
      splithub (.eth) "One place where a multi-party payout divides." Sticky: hub reads as the meeting point.
      fundrail (.eth) "Rails that carry funds to a crew." Sticky: two plain words that say the direction.
      fundlane (.com) "A lane that moves funds to crews." Sticky: calm, plain, says the direction.
    Next 10, with caveats ⚠️
      paysplit (reads as a verb phrase), railsplit (order feels backward), hubsplit (same), tipsplit (tips only),
      splitring (ring reads as a group of people in some English), paylane (close to payrail), fundhub (flat),
      payring (same ring caveat), splitlane (long), escrowhub (escrow carries legal weight it may not earn)
    Set builder: root splitrail; branches splitpay (.eth) "Payout rails for crews and their rewards.",
      splitclaim (.eth) "Claims and receipts for payouts already made.", splitdocs (.com) "Rules, docs, and how-to written for humans.",
      splitverify (.eth) only if it verifies; otherwise it is not called verify.
    Trademark, per shortlisted name: unchecked ⚠️, USPTO https://tmsearch.uspto.gov/, EUIPO https://euipo.europa.eu/eSearch/,
      WIPO https://branddb.wipo.int/, plus the office of the market it ships in. I cannot query live legal databases. This is not legal clearance.
    Backups: splitmesh (rung 1 suffix), splitlane (rung 1 suffix), crewsplit (rung 2 group word)

    Checks ledger
    Posture: offered to the network
    Surfaces: splitrail.eth, splitrail.com, github.com/splitrail
    Availability: splitrail.eth unchecked ⚠️ (https://app.ens.domains/splitrail.eth); splitrail.com unchecked ⚠️ (https://lookup.icann.org/); GitHub unchecked ⚠️ (https://github.com/splitrail)
    Trademark: unchecked ⚠️ (links given); no live trademark tool in this session
    Languages: English model-reviewed (not a clearance); Spanish unchecked; speaker review needed before shipping in either
    Scripts: single script (Latin); no punycode applies
    Accessibility: checklist run: passes; not tested with people or a screen reader
    Cultural review: self-checked only
    Harm check: in the person's words, "splits a payout among an agent crew"; in the agent's, a misrouted or withheld payout would hurt the payees, and the thing itself does not watch or deceive (a working note, not a finding)
    Public on registration: told before registering: the RDAP record for .com, certificate logs for any HTTPS hostname, the wallet and its history for .eth
    This ledger is not legal clearance, a guarantee, or a test.

## Fallback transforms (when everything is taken)

The ladder runs only on candidates made in this session or names the person made themselves; when a candidate resembles a known name, the agent asks whether it is theirs before mutating it. It never runs on an existing brand, project, person, community, movement, or place name to produce near-misses, and every rung's output goes back through the cut list, impersonation and lookalike checks included.

Mutation ladder (use in order, report which rung):

1. Swap suffix (network / place): mesh → hub → lane → rail → room
2. Swap group word: crew → guild → coop → team → kin
3. Swap work noun: gig → work → task → job → quest
4. Pluralize: crew → crews, guild → guilds
5. Add one clarifier syllable: pay → payout, claim → claims, proof → proofs
6. Lengthen by two characters or fewer: prefer meaning over ultra-short


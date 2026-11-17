# Signal Dreaming — Version History

Each entry states what changed and why. Where a release fixed something that had
been running wrong, the entry says what the wrong behaviour cost, because that is
the part that stops it being reintroduced.

---

## Known issues (open, not yet fixed)

**The batch-encoding rule is scoped to writes, so read-only checks walk past it.**
`dream-protocol.md` tells a run not to batch several **L2 writes** through one shell
invocation carrying the content as an argument or a here-document, because that path
lost whole batches to a non-UTF-8 failure twice. The 5.0.3 first run (2026-09-13) hit
the same failure a fourth time — but on an *optional read-only verification* command
(full-file diff reconstruction plus a source-hash final check), which the rule's
wording does not cover. The fault is in constructing the command; it has nothing to
do with whether the command reads or writes.

What the failure looks like, recorded so the next run identifies it in one step
rather than going to inspect the locale: `SyntaxError: Non-UTF-8 code starting with
'\xXX'`. Diagnosis on 2026-09-13 established that this is the signature of a
truncation landing *inside* a multi-byte character — removing one or two trailing
bytes of a three-byte CJK character reproduces it exactly, while removing all three
yields a different error (`EOL while scanning string literal`). A bare locale is
**not** the cause: with `LANG` unset and every `LC_*` at `C`, PEP 540 still enables
UTF-8 mode automatically, and defeating that produces a `UnicodeEncodeError` on
output, not a `SyntaxError` on input.

The truncation threshold is not known. A single line of 4,491 bytes of pure CJK
survived intact on the harness used for the diagnosis, but that is a different
transport from the `exec` tool where every failure occurred, and the failing command
text was not persisted.

Intended fix, deferred to the next iteration by the operator's decision on
2026-09-13: widen the rule from "L2 writes" to any command construction carrying a
long run of non-Latin content, read-only checks included, and record the error
signature in the protocol. Until then the proven workaround still stands and is
already written down — write one file at a time with the editing tool; six L2
targets went through first try that way after two batched runs lost everything.

---

## 5.0.3

Three fixes to things that were never written down, rather than written wrong.

**The batch cap now says what it counts.** It read `192 KiB of total input`, which
is not what it measures: only daily logs are counted, while a run also reads and
rewrites every L2 file it promotes into. The gap surfaced as throughput that
looked like it had degraded — one run spent 508 s on 50.6 KiB of logs, `0.10 KiB/s`,
below the floor of the band 4.0.1 measured. Nothing had degraded. Adding the L2
files the same run touched gives 77.0 KiB and `0.15 KiB/s`, back inside the band.
The risk was never the inaccuracy itself but what anyone recomputing the cap would
conclude from it, since 4.0.1 ties the cap to the timeout and explicitly invites
that recomputation.

Folding L2 bytes into the cap as a gate is the obvious fix and is not available:
Phase 1.4 decides which L2 files a run will touch from the content of logs Phase
1.3 has not read yet, so at the moment the cap is applied the number does not
exist. Reserving a fixed allowance instead would be the hard-coded constant the
Design Stance was written against. So the cap is named honestly, the margin it
needs is stated as something to derive later, and Phase 1.4 and Phase 3.4 record
log bytes, L2 bytes and wall-clock on **every** run rather than only on an
overrun — a measurement taken only when something goes wrong is sampled exactly
where it is least representative of an ordinary night.

**A forgotten topic file can be noticed again.** Phase 1.6 walks from each index
entry to the file it points at, and nothing walked back. A topic file that no
entry names was therefore examined by no phase of this protocol — not retired,
not referenced, not judged stale, simply out of view and with nothing able to
return it. In one workspace 34 of 98 topic files were unreachable from the index,
among them a proxy-configuration handbook updated four days earlier and still used
by a skill, while the index held no mention of the subject. Nothing was lost:
`memory_search` still reaches those files. What was lost is the session that
starts without knowing to look.

A new Phase 1.7 subtracts the index's pointers from the topic directory and
reports only the difference that sessions have modified since the frontier,
measured before any write — so a recent mtime means ordinary session work rather
than this run's own Phase 2. Two limits are stated in the protocol because both are easy to
lose later: appearing on the list is not a reason to add a pointer, or the index
grows back into the topic-directory mirror 5.0.0 removed, one entry per night
while looking like maintenance; and files orphaned before this rule existed carry
old mtimes and never appear, because draining a backlog is a one-off
reconciliation a human asks for with the list in front of them, not a report
re-read every night until it is ignored.

**Backup growth is reported, and still never touched.** `.backup/memory-dreams/`
has no retention rule and does not get one. It had reached 99 directories and
32 MiB in one workspace — the kind of number that invites an automatic prune. It
should not: these backups are the recovery path for every write this protocol
makes, including the hard stop that cancels a run; a pass whose job is rewriting
memory is the wrong process to hold the eraser for its own safety net; and no
runtime value exists to derive a retention period from, so any cut-off would be
invented rather than measured. The audit helper prints `backup_dirs` and
`backup_kib` with no threshold and no NOTE, and a human decides.

**Orientation moved out of `SKILL.md`.** Adding two rules took the always-loaded
file from 9,957 characters to 10,930, over the 10,000 the authoring standard
sets — and 9,957 was already only 43 under, so the budget had no room for any
rule at all. The rules were folded into the entries they belong to, and the
stack-orientation section moved to `references/memory-stack.md`: a comparison
with built-in Dreaming and a list of components this protocol does not touch is
reference, not procedure, and it carries a version number that dates. The one
operational line in it — never touch `memory/dreaming/**` or `memory/.dreams/**`
— stayed behind. `SKILL.md` is now 9,547.

No change to what a run produces. The index keeps the shape 5.0.0 gave it.

---

## 5.0.2

Two fixes, both to things that were inconsistent rather than wrong in themselves.

**The cron template's timeout now matches the batch cap.** 4.0.1 sized the
`192 KiB` cap against an `1800 s` timeout and said so, but left the template in
`SKILL.md` at `900 s`. At the slower end of the measured throughput that admits
roughly `108 KiB` — so a batch this protocol considers legal gets the run killed
partway, most likely inside Phase 2, leaving L2 files written, the index and the
diary untouched, and the watermark not advanced. Nothing records that it happened.
Three releases carried the mismatch because the workspace it was developed on runs
`1800 s`, so the template was never the thing being exercised. Both numbers are
stated together now, with a line saying they move as a pair.

**An empty selection now has a rule.** 5.0.1 made the state reachable and said
nothing about it: once the watermark date contributes only its changed files, a run
whose only candidate is an unchanged watermark date selects nothing at all. Before
that, `>=` guaranteed there was always something. Undefined, the likely improvisation
is the damaging one — carry the empty batch into Phase 3 and write a diary entry
whose `Consolidated through:` names logs the run never read.

So: an empty selection ends the run at Phase 1, writes nothing, and leaves the
watermark where it is. It does **not** append a `SKIP` comment. The guardian may,
because the diary is the only channel it has; a run that reached Phase 1 has its
final summary, and nothing in this protocol reads those comments — Phase 1.1
anchors on Dream headings. Phase 1 is declared read-only in three places and stays
that way.

---

## 5.0.1

Stops a large watermark date from blocking every later date forever, and makes two
silent write failures visible.

**The watermark date is no longer re-admitted whole.** Phase 1.2 selects `>=` so
that same-day appends are not missed, and justifies the cost as re-reading one
already-seen file being cheap. Applied to a whole date it is not cheap: every file
of that date returned to the batch at full size on every run, changed or not. With
oldest-first resumption and the unsplittable date boundary, a date large enough to
fill the batch on its own then filled it permanently — three consecutive runs each
re-read the same 221 KiB day, and the following day's four logs were deferred every
time. Each of the three rules is right; the combination is what deadlocks, and it
needs a workspace that writes more in one day than a batch can hold, which is why
it took this long to surface.

The fix asks the modification question per file instead of per date, with the
`find -newermt` test the guardian already uses. Unchanged files on the watermark
date contribute nothing to the batch; changed ones are still selected, so the `>=`
defence is intact. Skipping the whole date on the same evidence was the obvious
alternative and the wrong one: a false negative from mtime costs the guardian one
no-op run, but costs a date-level skip everything appended to that day,
permanently. Per-file keeps the consequence at the guardian's level.

One detail that is easy to get backwards: the comparison timestamp must come from
the newest entry carrying `Consolidated through:`, not the newest entry. A backfill
has a later heading and deliberately left the frontier alone, so comparing against
it under-reports which files changed — and under-reporting here drops them as
already-read. The guardian escapes the same trap by refusing to skip after a
backfill; this rule has no do-nothing option, so it has to name the right entry.

**L2 files are written one at a time.** Batching several promotions through a
single command invocation that carries the content corrupted non-UTF-8 text and
lost the entire batch, twice. The second occurrence skipped six targets, so detail
the run had correctly decided to sink stayed in the index and inflated it by
roughly 3,000 characters. Per-file edits of the same content succeeded first try.
The fault is in building the command, so it stays invisible until the content is
long and non-Latin — exactly when a run has the most to lose.

**Writes are verified by reading them back.** A diary trim reported success against
a file it had not changed, leaving 31 entries under a cap of 30. The result is a
valid file that is merely one entry too long, so nothing downstream notices. The
audit helper already printed the entry count and nobody compared it; it now warns
when the count exceeds `SD_DREAM_LOG_MAX` (default 30, same integer-only handling
as the other overrides). Phase 3.6 states the general form: a step reporting
success is not evidence its file changed, so check the artifact rather than the
action.

No change to what a run produces — the index keeps the shape 5.0.0 gave it.

---

## 5.0.0

Makes the index a domain-level summary rather than a mirror of the L2 topic list,
and curates on every run rather than only when the index is over budget.

Both halves change what the protocol produces, so an existing workspace will see
its `MEMORY.md` restructured on the first run after upgrading. That restructuring
is backed up like any other write (Phase 3.1), but it is not something the human
asked for on that particular day — hence the major version.

**Curation stopped being conditional on size.** The protocol said that below its
target, size was "not a consideration at all", then asked — correctly — whether
each section still belonged at index level. In practice the first clause won: the
run reached the target, stopped, and never got to the question. Measured across
eight consecutive runs on a CJK workspace, the index finished between 92% and 100%
of a 16,000-character target every time, while five archived projects kept full
entries throughout. A target that is only ever consulted when exceeded is not a
ceiling; it is a floor, and the index grows until it finds it.

**The index stopped mirroring the topic directory.** Phase 1.5's topic identity
guard forbids merging L2 files that describe materially different things. That
guard is right, and it was being applied one layer too high: every new topic file
earned its own index entry, nothing ever merged, and eleven of thirty-one entries
in one workspace turned out to be facets of a single line of work. The guard now
says explicitly that it governs L2 files and not index structure, and Phase 3.2
groups index entries by the question a reader is asking.

**Phase 1 now reads L2 modification times.** Deciding whether an entry still
describes something live was unanswerable from the entry itself — an index says a
project is active in the same words the day the work stops. The modification time
of the file an entry points at is a fact produced by Phase 2 rather than a field
someone has to remember to maintain. A date stamped into the entry was the
obvious alternative and the weaker one: it survives only until the first run that
refreshes every line at once. mtime informs the judgement; it never retires
anything by itself.

**Entries are placed deliberately.** New entries were appended to the end of the
file, which is not a neutral position — it sits under whatever heading happens to
be last. An active project entry landed under a standing-rules heading in
production, where later runs would have read it as a permanent rule and never
considered it for consolidation again. Phase 3.2 now assigns a section before
writing, and Phase 3.6 checks that every entry sits under a heading matching what
it is.

**Individual entries are sized.** A total budget says nothing about one entry, so
a section can reach several times the length of its neighbours unnoticed. The
anchor is `maxPromotedSnippetTokens` — the cap `memory-core` puts on a single
promoted snippet — read from config rather than copied into this document. It is
used to find outliers only: entries already at or below it are left alone,
because a per-entry cap used as a target rebuilds the same attractor one level
down.

**Finished work keeps one line.** Closed and archived projects are reduced to a
line plus an L2 pointer. Nothing in the protocol asks about them again, so a full
entry is pure accumulation.

**Security: the audit helper no longer evaluates its numeric overrides.**
`references/dream-audit.sh` read `SD_BOOTSTRAP_MAX_CHARS`,
`SD_BOOTSTRAP_TOTAL_MAX_CHARS` and `SD_INDEX_TARGET_PCT` straight into `$(( ))`.
Bash evaluates an array subscript inside arithmetic expansion as a command, so
`SD_INDEX_TARGET_PCT='x[$(cmd)]'` executed cmd — confirmed by running it. The
three values are now accepted only as plain non-negative integers; anything else
falls back to the default and warns, since an override dropped in silence is its
own defect. Defaults and legitimate overrides behave exactly as before.

**Packaging: the audit helper is invoked through `bash`.** The protocol called
`references/dream-audit.sh` by path, which needs the executable bit. A ClawHub
archive does not preserve it, so the call worked on the publishing machine and
failed on every fresh install. Naming the interpreter removes the difference.

`SD_INDEX_TARGET_PCT` is unchanged at 80. Lowering it would have moved the
attractor rather than removing it.

One consequence is documented so it is not later mistaken for a regression: index
size no longer converges on a figure. Run-to-run variation means curation is
tracking content; a flat line means it has started tracking the target again.

Also includes the unreleased 4.0.4 fix below.

---

## 4.0.4 (unreleased)

Fixes a dream number that stops advancing once the diary reaches its trim cap.

Phase 3 derived the new number by counting `## 🌙 Dream #` headings, while Phase 5
deletes the oldest entry whenever the count exceeds 30. The two rules agree only
while the diary is still growing. Once it saturates, the count is permanently 30,
so every subsequent run writes `#31` — observed in production across four
consecutive runs after the cap was reached. The watermark is unaffected, since it
is read from `Consolidated through:`, so consolidation stays correct while the
diary quietly loses monotonic identity and the gap check that depends on it.

Phase 3 now reads the number out of the newest heading and adds 1, and Phase 5
states that trimming must never change the next number. Repairing an
already-frozen diary means renumbering the affected headings once, from the last
correct entry forward; nothing else in the log changes.

---

## 4.0.3

Restates the 4.0.2 scope without enumerating what falls outside it.

4.0.2 fixed the rule by naming categories of ordinary content as out of scope. The
rule was right; the enumeration was not. A list of what a memory system will
retain reads, to someone reviewing the skill rather than running it, as a
description of what it sets out to collect — and the three constraints that
actually do the work need no examples to be unambiguous: the list is exhaustive,
it is not to be extended, and nothing outside it raises the alert.

The scope is now stated as a limit on the guard rather than a judgement about
content. It covers authentication material and is not a privacy classifier;
anything else follows the workspace's own conventions. Behaviour is identical to
4.0.2.

---

## 4.0.2

Closes the secret guard's scope.

The list of what counts as a secret was introduced with *"treat these as sensitive
by default"* — wording that reads as a floor rather than a boundary, so a run could
classify ordinary log content as sensitive on its own judgement, withhold it from
L2, and ask for manual review of the daily log.

That alert has nowhere to go. This protocol never edits daily logs, so the value
stays exactly where it already was; the only durable effects are an index missing
an ordinary fact and a review request that cannot resolve. Repeated, it teaches
the human to skim past the alert that does matter.

The list is now stated as **exhaustive**, and nothing outside it raises the alert.

---

## 4.0.1

Fixes a guardian that could skip work it should have done, and sizes the batch cap
to the task timeout.

The guardian tested for daily logs dated strictly *after* the watermark, while
Phase 1 selects `>=` precisely because a watermark-dated log can be appended to
after the last run read it. Since the guardian runs first, that defence never
applied: inside the debounce window a run reported no-op while same-day additions
waited for a later pass. Session-reset hooks that write `YYYY-MM-DD-HHMM.md` files
make several logs share the watermark date every day, so this is now the normal
case rather than an edge one. The two log conditions are merged into one that
reuses Phase 1's `>=` and asks whether any selected log changed since the last
entry's heading timestamp.

The byte cap moves from `512 KB` to `192 KiB`. A cap means something only if the
batch it admits can finish before the scheduler kills the run: at a measured
`0.12-0.21 KiB/s`, an `1800 s` timeout admits roughly `216 KiB`, so the old number
was never reachable. **If your task timeout differs, recompute the cap from your
own slowest observed throughput.** The cap bounds accumulation across days and
cannot bound a single day — the date-boundary rule still processes an oversized
date whole, and such a run now records its actual input size and duration in the
dream-log.

---

## 4.0.0

Returns to the protocol-only design of the 1.x line and removes the 2.x/3.x script
layer entirely.

Those versions compiled the same rules into enforced JavaScript preconditions — a
transaction state machine, run manifests, lock files, staged candidate
directories. That layer added no new safety rules; it changed who enforced them,
and in production turned recoverable conditions into aborted runs: an over-limit
index refused to run the pass that shrinks it, and an optional audit's path error
cancelled an otherwise complete consolidation.

It also retires the byte-based index target inherited from 1.x. That `8 KB` was
written where a byte and a character were the same thing; the real limit is
`bootstrapMaxChars`, measured in **characters**. For a CJK workspace at ~1.7 bytes
per character it enforced about a quarter of the real budget — and 3.x then made
crossing it a hard error, so a healthy index could block its own consolidation
pass. 4.0.0 does not substitute another constant: headroom is derived from the
runtime's own caps, and the target is a configurable percentage of it (default
80%, leaving a growth band). A hard-coded threshold caused the original damage, so
the protocol no longer contains one.

Upgrading from 2.x or 3.x: delete any cron payload steps invoking `preflight`,
`begin`, `finalize`, `run-guard`, or `dream-audit.mjs` and use the template in
`SKILL.md`. There is no state to migrate. Existing `.backup/memory-dreams/`
directories can stay; nothing reads them. Your existing `dream-log.md` works
as-is — the watermark is found by scanning back for the newest entry that carries
a `Consolidated through:` field, and if none does, the newest entry's heading date
is used.

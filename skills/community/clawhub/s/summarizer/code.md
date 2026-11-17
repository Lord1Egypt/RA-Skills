# Diffs, Pull Requests, and Releases

Scope: pull-request descriptions, code review summaries, commit ranges, changelogs, release notes, migration guides, and incident postmortems. The universal failure is describing what was touched instead of what changed for someone.

**Before writing release notes or a changelog entry**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for the previous release and `templates/` for the project's approved note shape — a release note that changes structure between versions is unreadable as a series.

**Contents:** [Behavior, Not Files](#behavior-not-files) · [Reading a Diff](#reading-a-diff) · [Pull Request Summaries](#pull-request-summaries) · [Commit Ranges](#commit-ranges) · [Release Notes](#release-notes) · [Breaking Changes](#breaking-changes) · [Changelog Entries](#changelog-entries) · [Postmortems](#postmortems) · [Output Shapes](#output-shapes)

## Behavior, Not Files

The single rule this whole file expands: a reader of a code summary wants to know what is now true that was not true before.

| Bad (mechanical) | Good (behavioral) |
|---|---|
| "Modified 14 files in `src/auth/`" | "Sessions now expire after 24h instead of never; existing sessions are invalidated on deploy" |
| "Refactored the payment module" | "No behavior change; payment retries moved behind an interface so a second provider can be added" |
| "Bumped dependencies" | "Upgraded to lib 4.x, which drops Node 16 support — CI base image must move first" |
| "Fixed bug" | "Fixed: uploads over 10 MB failed silently on Safari" |
| "Added tests" | "Added coverage for the retry path; no production behavior change" |

"No behavior change" is a valuable summary and it must be earned — a pure refactor is a real category, and saying so lets a reviewer read differently.

## Reading a Diff

Diffs are ranked by the machine, not by importance. Re-rank them.

1. **Read the description and the linked issue first** — the intent, before the implementation.
2. **Interface changes before implementation changes**: public function signatures, API routes, schemas, config keys, environment variables, CLI flags. These are what other people's code depends on.
3. **Migrations, schema changes, and data backfills** — irreversible, and the highest-risk lines in any diff.
4. **Deletions** — a removed check, a removed test, a removed feature flag is a behavior change with no new line to notice.
5. **Config and dependency files** — `Dockerfile`, lockfiles, CI config, IaC. A one-line change here often outranks 500 lines of application code.
6. **The bulk of the diff last.** Generated files, formatting, lockfile churn, and vendored code are volume, not content.

Diff size is a poor proxy for consequence in both directions: a 3,000-line generated update is nothing, a one-character comparison-operator change is an outage.

## Pull Request Summaries

For a reviewer, in this order:

- **What changes for a user or a caller**, in one sentence.
- **Why now** — the issue, the incident, the requirement.
- **Risk surface**: what breaks if this is wrong, and what is not covered by tests.
- **Anything irreversible**: migration, backfill, deletion, credential rotation, feature-flag default flip.
- **Deploy dependencies and ordering**: must ship before or after something else, needs a config change first, needs a cache flush.
- **What reviewers should look at hardest** — naming two files beats "please review".
- **Out of scope**, so reviewers stop looking for it.

Length: a PR summary is a `brief` (40-80 words) unless the change is a migration, an API change, or an incident fix, which earn `standard`.

## Commit Ranges

Summarizing `main` since the last release, or a branch's history:

- **Group by user-visible outcome**, never by author, date, or commit order. Twelve commits implementing one feature are one line.
- **Drop the noise classes entirely**: merge commits, "fix typo", "address review comments", "wip", revert pairs that cancel out. A revert that does *not* cancel out is content — say what was rolled back and why, if the message says.
- **Conventional-commit prefixes** (`feat:`, `fix:`, `chore:`, `perf:`, `BREAKING CHANGE:`) are a free classification when the project uses them; use them and say you did. When the project does not, classify by diff, not by message text — commit messages describe intent, sometimes accurately.
- **Count what you dropped**: "plus 31 internal changes" is honest and stops a reader from hunting.

## Release Notes

Three audiences read the same release, and the notes serve them in this order:

| Section | Reader | Content |
|---|---|---|
| Breaking changes | Anyone upgrading | What breaks, the exact error they will see, the migration step |
| Required actions | Operators | Migrations to run, config to set, ordering constraints |
| New | Users evaluating the upgrade | Capability, in the user's vocabulary, not the module's |
| Improved | Existing users | Behavior that is now better, with the measurable where one exists |
| Fixed | Users who hit the bug | The symptom they experienced, so they can recognize it |
| Deprecated | Planners | What still works, when it stops, what replaces it |
| Internal | Nobody, usually | One line and a count, or omitted |

- **Write the symptom, not the cause**: "Fixed a crash when opening a file with no extension" beats "Fixed null pointer in `resolveType`". The reader searches for their symptom.
- **Version numbers and dates** at the top; a release note with no date is unusable in six months.
- **Link to the issue, do not restate it.**
- Security fixes get their own line with severity and whether exploitation is known, above everything else.

## Breaking Changes

The section that justifies the whole document. Each entry needs four parts:

1. **What breaks** — the specific API, flag, config key, schema, or behavior.
2. **How it fails** — the exact error message or symptom, so a user can search for it.
3. **The migration** — the concrete replacement, not "use the new API".
4. **Whether it is detectable before upgrading** — a grep, a deprecation warning in the previous version, or nothing.

A change is breaking if any existing caller has to change something. Renamed config keys, changed defaults, tightened validation, removed implicit behavior, and dropped runtime or platform support are all breaking, and all four are routinely filed under "improved".

## Changelog Entries

- **One entry per user-visible change**, present tense, starting with a verb.
- **Keep the series consistent**: whatever categories and order the previous entries used, this one uses. Store the shape in `templates/` the first time it is agreed.
- **Unreleased goes at the top** with its own heading, so the diff between releases is readable.
- Entries are written when the change ships, not reconstructed at release time from a commit log — reconstruction is the reason changelogs are wrong.

## Postmortems

An incident postmortem is a summary with a fixed shape, and the parts that get compressed away are the ones that make it useful.

| Part | What survives compression |
|---|---|
| Impact | Who was affected, how many, for how long, in what way — with numbers |
| Timeline | Timestamped: first symptom, detection, escalation, mitigation, resolution. Detection lag is the number that matters |
| Contributing factors | Plural; a single root cause is almost always an oversimplification |
| What went well | Kept — it is what you protect in the fix |
| Action items | Owner + verb + date (SKILL.md Rule 8), separated into prevent / detect / mitigate |
| Attribution | Systems and decisions, never individuals |

Trigger-happy compression drops the timeline's detection gap and the "what went well" section; both are the parts an incident review is for.

## Output Shapes

**Pull request:**
```
<What changes for a caller, one sentence.>
Why: <issue or incident>
Risk: <what breaks if wrong; what tests do not cover>
Irreversible: <migration | backfill | none>
Deploy: <ordering or config prerequisites | none>
Review closely: <file or function>
```

**Release:**
```
## <version> — <date>

### Breaking
- <what breaks> — <error you will see> — <migration>

### Required actions
- <migration or config, in order>

### New / Improved / Fixed
- <symptom-first line> (#<issue>)

Internal: <count> changes not listed.
```

**After producing release notes, a postmortem summary, or a changelog shape the user approved**, write the notes to `~/Clawic/data/summarizer/summaries/release-<version>.md` when `store_summaries: full`; register the release in `## Sources` in `memory.md` so the next release's diff has a baseline; store an approved note or changelog structure as `templates/<project>-release-notes.md` with its `## Boxes` line so the series stays consistent; add project-specific component names and abbreviations to `glossary.md`; and put postmortem action items with dates into `## Due` and, when the work is tracked, into `~/Clawic/data/projects/<project>.md`. Formats and thresholds: `memory-template.md`.

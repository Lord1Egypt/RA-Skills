# Corporate Template Profiles And Cross-Project Reuse

Read this reference after report content and structure are clear enough to resolve the
visual source. Keep this feature limited to explicit enterprise brand/template
profiles. Do not turn it into general user-preference memory.

## Product Boundary

Treat a corporate profile as Skill-managed, inspectable state, not model memory. Use
`TAOHTML_HOME` when set; otherwise use `~/.taohtml`. Never write profiles into the
installed Skill directory. Codex, Claude Code, and other local Agents can reuse the
same home directory when they run as the same user and point to that directory.

Do not promise cloud sync. For another machine or an environment without persistent
disk, export a complete package and import it explicitly.

A profile stores only corporate brand/template reuse material:

- the validated corporate-fidelity VI contract;
- its one to three exact reference images;
- a sanitized, profile-identity project theme compiled through the existing compiler;
- confirmation, reference, VI, theme, creation, and activation hashes/state; and
- explicit display name and aliases.

Never store report prose, project goals, audience, evidence, customer report data, or
preferences outside the corporate brand/template boundary. The source project handoff
is validated and hashed at save time but is not copied into the profile. The archived
theme is recompiled from the same confirmed VI/reference bytes with a profile-only id,
name, and empty project corrections, then compared structurally with the already
validated source theme.

Profiles are not a ninth built-in visual system. Keep the built-in visual-system
directory and selector at the complete eight-system catalog; a corporate profile
remains a separate project-specific binding.

## Home And Schema

Use this layout:

```text
${TAOHTML_HOME:-~/.taohtml}/
└── profiles/
    └── <profile-id>/
        ├── profile.json
        └── versions/
            ├── v1/
            │   ├── version.json
            │   └── assets/
            │       ├── vi-contract.json
            │       ├── references/reference-01.png ... reference-03.webp
            │       └── project-theme/
            │           ├── theme.json
            │           ├── theme.css
            │           ├── templates.html
            │           └── provenance.json
            └── v2/ ...
```

`profile.json` schema v1.0 records the profile id, display name, explicit aliases,
`active | archived` status, active version, created/updated time, atomic activation
pointer `{version, activated_at, reason, sequence}`, and every immutable version
manifest path/hash.

Each `version.json` schema v1.1 records:

- profile id, version, display-name/alias snapshot;
- created and initial-activated state/time;
- confirmation method/reference and the source handoff hash;
- VI, ordered reference-image, source-theme, and archived-theme hashes;
- `corporate_fidelity` and screenshot-visible-only brand boundaries;
- the source project's target mode as creation provenance only, never as a reuse boundary;
- the explicit excluded-content list; and
- the complete relative asset path/role/hash/size list.

The loader also accepts v1.0 profiles created before cross-mode reuse was corrected.
For those immutable manifests, the former `boundaries.target_mode` field is interpreted
only as first-compilation provenance; it does not block a current task in the other mode.

Treat version directories and manifests as immutable. Never update v1 in place. A
permanent template update creates v2/v3, validates it, then atomically replaces the
active pointer in `profile.json`. Retain old versions for rollback.

All store commands, including list/show/resolve/bind/validate-binding/export, share
one cross-process snapshot lock. The lock is an OS advisory file lock, so process
termination releases ownership even though the harmless lock file remains. A stale
empty directory left by the earlier lock format is recovered only after a conservative
age threshold. Version publication uses a recovery journal: an interruption before
the commit marker rolls back the unregistered version and restores the old profile;
an interruption after the marker validates and finishes the committed snapshot.

## Identity Resolution And Interaction

Parse the current material and conversation first. Do not add a startup questionnaire
and do not ask “whether to reuse” as a required question.

Pass only explicit enterprise identity candidates to exact resolution:

```bash
python scripts/profile_store.py resolve \
  --identity "Acme 集团" \
  --identity "ACME"
```

Resolution uses normalized exact matches against profile id, display name, and
explicit aliases. It does not use fuzzy matching or the previous task's choice.

- One active candidate: bind its active version automatically. Do not reopen or
  visually analyze reference images and do not regenerate the VI.
- Several candidates, an unclear enterprise identity, or a genuine conflict between
  the current request and profile boundary: ask exactly one selection question.
- No candidate: continue with normal built-in/reference routing. Do not invent an
  enterprise identity.
- Alias collision at create/import: fail. Never use last-write-wins.
- A task for another company/customer: create or explicitly select its independent
  profile. Never overwrite the first company.

After automatic reuse, show only:

> 本次沿用【企业显示名 企业模板 vN】；如需更换请直接说明。

Customer non-objection is sufficient to continue to the current Report Design Brief.
It is not permanent preference consent and is not production authorization.

## First Creation

Create v1 only after all of these are true:

1. `corporate_fidelity` completed the supported one-to-three-static-reference flow.
2. The exact current VI contract was clearly confirmed with a conversation-bound
   current handoff schema and exact VI/reference SHA-256 values.
3. `compile_project_theme.py` compiled the current project theme.
4. `theme_runtime.load_project_theme()` validated that theme and its corporate
   provenance. Do not duplicate or weaken this loader.

Then run:

```bash
python scripts/profile_store.py create \
  --profile-id acme \
  --display-name "Acme 集团" \
  --alias ACME \
  --handoff /absolute/current-task/confirmed-theme-handoff.json \
  --theme /absolute/current-task/project-theme
```

The command validates the source handoff and source theme, creates v1, validates the
complete saved profile, and sets v1 active. A legacy phrase-only handoff, reconstruct
VI, built-in theme, mismatched VI/reference/theme, symlink, or partial theme fails
before the profile becomes usable.

## Current-Task Binding And Reuse

Write one task-local JSON binding for every reuse or temporary override:

```bash
python scripts/profile_store.py bind \
  --identity "ACME" \
  --task-id current-task-id \
  --target-mode presentation \
  --output /absolute/current-task/gates/profile-use.json

python scripts/profile_store.py validate-binding \
  --binding /absolute/current-task/gates/profile-use.json
```

Before `bind`, run the `profile-reuse` profile from `environment-preflight.md`. It
checks core, Pillow, and the project-theme loader only. It does not reread the
reference images as new design input and does not require Playwright or Chromium.

The binding records profile id/display name, active version, task mode, theme path
relative to TaoHtml home, theme fingerprint, VI/reference hashes, profile/version
manifest hashes, resolution identities/basis, time, customer notice, and
`temporary_override`.

Resolve the relative theme path against the current TaoHtml home and load it only
through `theme_runtime.load_project_theme()` (normally through the existing renderer's
`--project-theme`). Never copy a second theme validator into the profile workflow.
Pass the binding's current task mode to the renderer:

```bash
python scripts/render_visual_system.py \
  --content /absolute/current-task/content.json \
  --project-theme /resolved/profile/project-theme \
  --target-mode reading \
  --output /absolute/current-task/index.html
```

The archived theme keeps its first-compilation mode only as provenance. A presentation
profile must render a later reading task with `data-mode="reading"`, and a reading
profile must render a later presentation task with `data-mode="presentation"`.
Changing only the current report mode never justifies or requires profile v2.

Revalidate immediately before the Report Design Brief gate, formal HTML, browser QA,
and delivery. Fail closed when any asset, manifest, hash, active version, identity,
target mode, status, or theme structure changes. Never silently fall back to a
built-in system.

## Three Change Semantics

Interpret customer language by scope:

### Current task only

“这次不用 / 这次换一个” creates a binding with `--temporary-override`. Continue
through the newly selected built-in or static-reference route. Do not change the
profile active pointer or aliases.

### Permanent company-template update

“以后改用 / 更新公司模板” must repeat the corporate-fidelity VI confirmation and
hash-bound theme compilation for the new screenshots. Then run:

```bash
python scripts/profile_store.py update \
  --profile-id acme \
  --handoff /absolute/current-task/new-confirmed-handoff.json \
  --theme /absolute/current-task/new-project-theme
```

This creates the next immutable version and atomically activates it. Use `activate`
for an explicit version or `rollback` for an earlier retained version. Any current
binding to the old active pointer becomes invalid and must be regenerated.

### Another company/customer

“这是另一家公司 / 客户” creates or selects a separate profile id. Do not mutate the
original profile.

Deletion/forgetting is outside v1. Prefer `archive`, which stops automatic resolution
but retains recoverable bytes; use `restore` to reactivate the same active version.
Do not claim that archive deletes customer data.

## Export And Import

Use explicit packages for another device or non-persistent environment:

```bash
python scripts/profile_store.py export \
  --profile-id acme \
  --output /absolute/acme.taoprofile.zip

python scripts/profile_store.py import \
  --package /absolute/acme.taoprofile.zip
```

The package manifest enumerates every profile file with relative POSIX path, hash, and
size. Export holds the same store snapshot lock from validation through every payload
read, so a package cannot mix versions during a concurrent update. Import rejects
duplicate entries, absolute/Windows/UNC paths, traversal,
backslashes, symlinks, directory entries, missing files, extra files, hash/size drift,
schema drift, profile-id conflicts, and alias conflicts. It never calls `extractall`.

Reject symlinks and extra/missing files in live profiles too. Keep every stored and
exported path relative; never persist an absolute task path in a profile or binding.

## Authorization Boundary

Use `visual_route: profile_reuse` for exact reuse. Set `reference_vi.status` to
`not_required`, attach the current task-local `profile_use` binding, and keep
`project_theme_compiled: true` only after the saved theme validates. The binding
replaces only this task's repeated VI generation/confirmation step.

It never replaces:

- a current material-summary confirmation when the route requires one;
- the current Report Design Brief and its explicit confirmation;
- `check_production_authorization.py` before formal HTML, browser QA, or delivery;
- browser QA, asset QA, traceability, or delivery verification gates.

A temporary-override binding cannot authorize `profile_reuse`. A reusable binding
cannot be attached to another visual route. Modified assets, version activation,
archive, identity drift, or profile/theme corruption invalidates the binding.

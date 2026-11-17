# AI Soul Package Contract

## Runtime Boundary

Only these files define runtime behavior:

- `IDENTITY.md`
- `USER.md`
- `SOUL.md`
- `AGENTS.md`
- `TOOLS.md`
- `MEMORY.md`

Hosts must not automatically load `README.md`, `forge-report.md`,
`quality-check.md`, `soul6-report.json`, `CHANGELOG.md`, or `auditions/` as
runtime instructions or memory.

## Manifest

`manifest.json` uses `schemaVersion: aisoul.package.v1` and
`artifactType: AISOUL`. It records:

- Name, slug, semantic version, language, and output license
- `offline: true`
- Exact runtime entrypoints
- SOUL-6 standard name, version, canonical profile, source, and reference URL
- Provenance mode, summary, authorization note, and local source descriptions
- Generator name and version
- Paths to the generated README, quality artifacts, and audition artifacts

The SOUL-6 URL is passive attribution. The runtime must not fetch it.

## Quality Artifacts

`README.md` is the generated human-facing package entry point. It summarizes
identity, usage, SOUL-6 results, synthetic audition samples, generation data,
and provenance. It is refreshed by initialization, report-writing, audition,
and packaging commands, but remains non-runtime and non-canon.

`soul6-report.json` is a deterministic local report with evaluator and standard
versions. `quality-check.md` is its human-readable projection.

`auditions/suite.json` contains synthetic cases. `auditions/report.json` and
`auditions/samples/` contain actual local results. They remain non-canon.

`forge-report.md` records blueprint and provenance decisions. `CHANGELOG.md`
records accepted semantic changes between package versions.

## Versioning

Package versions are independent of Skill, evaluator, schema, and SOUL-6
versions. Preserve all five version identities in reports and manifests.

## Packaging

The local pack command creates a ZIP with one root directory named after the
package slug. It excludes `.git`, `node_modules`, and `.DS_Store`. Default
packaging requires `SOUL-6 READY`.

Use `--allow-core` or `--allow-draft` only after explicit user acceptance and do
not rename the conformance level in reports.

## Licensing

Repository code and Skill content are MIT. SOUL-6 standard text is CC BY 4.0.
Generated package content uses the license selected in its manifest and remains
subject to all input-source rights.

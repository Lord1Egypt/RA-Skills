# Field report: OpenClaw 2026.9.1-2026.9.3

Published with the operator's permission on 2026-09-11. This is an anonymized
first-party account from one customized, multi-agent installation using
messaging channels, external memory, plugins, scheduled jobs, and local
compatibility patches.

## Maintainer comment

We used this upgrade method on our own installation. The first attempt failed
and exposed gaps that a package-only rehearsal could not detect. Rehearsing the
actual target commands on a faithful state copy, measuring restore behavior,
and requiring real post-start work made the later cutovers verifiable.

Version 1.3.2 incorporates those lessons and corrects the Kova importer against
upstream producer code. We do not claim that this new skill version performed
the historical upgrades: those used our installation-specific tooling. The
field evidence supports the method; the compatibility tests support the new
importer. Neither is an upstream endorsement or a guarantee for another
installation.

## Observed outcomes

| Target | Observation | Outcome |
| --- | --- | --- |
| 2026.9.1 | The first target CLI invocation during plugin installation migrated live state before rejecting old configuration. Abort/restart behavior invalidated freshness evidence; restore was much slower than the small lab suggested. | Failed attempt. Subsequent laboratory recovery was completed and this candidate was held. It is not counted as a successful production upgrade. |
| 2026.9.2 | The exact candidate was exercised on a stopped full-state copy. Database integrity, histories, and scheduler continuity were checked. Fresh production checks covered messaging, memory, plugins, tools, voice, persona, and routing. | Production cutover completed. Current data was preserved after the new-write boundary. |
| 2026.9.3, first activation | Plugin trust/origin checks failed; the correlated Matrix probe got no reply. Checks requiring an agent turn remained skipped. | 11 PASS, 3 FAIL, 5 SKIP; overall failure. |
| 2026.9.3, after forward repair | The runtime was repaired while preserving current state. The same evaluation was repeated; a Matrix reply correlated by reply-to metadata arrived in about seven seconds. | 19 PASS, 0 FAIL, 0 SKIP; overall success at that observation. |

These results are historical observations, not a statement of current service
health. A later incident showed why admission must be checked after every
restart: a gateway could report ready while rejecting new work as draining.
The operator reported that a subsequent restart restored the Matrix probe.
That later account is contextual testimony, not an additional independently
verified run in the aggregate evidence below.

## Evidence and verification limits

The accompanying [aggregate JSON](field-evidence-2026-09.json) includes the
before/after counts and SHA-256 commitments to the retained private reports.
The counts were read from the reports; the hashes were computed from their
exact bytes. The private reports are not published because they contain
operational identities and message metadata. A hash allows later comparison
against the same source; it does not allow public re-execution or independent
verification of undisclosed data.

The 9.2 result is supported here by a retained completion report, which cites a
runtime evidence digest. That underlying runtime artifact was not fetched for
this publication, so this account does not present it as newly verified.

All hostnames, IP addresses, account/room/session/event identifiers, private
paths, message bodies, credentials, and private repository coordinates were
excluded. Only product versions, aggregate outcomes, a rounded reply latency,
and content hashes remain.

## What changed in 1.3.2

- Kova's harness platform is no longer treated as the target runtime toolchain.
- Exact identity is explicitly scoped to the core npm artifact, and every
  executed scenario must agree with the report identity.
- Migration policy requires preservation invariants beyond snapshot presence.
- OpenClaw invokes bundled helpers using its documented `{baseDir}` path.
- The stateful procedure records full-copy rehearsal, measured rollback,
  mutation boundaries, and admission through a correlated user path.

The release candidate passed 262 local tests, including a contract test using
Kova's actual report, ledger, and bundle generators at commit
`14589997967d0ce0f1531ea2d030d6ed5b4c975a`. Those generators received synthetic
records; no new production migration was performed by that test. ClawHub's
package dry run accepted the candidate. See the repository validation workflow
for the public CI result on the release commit.

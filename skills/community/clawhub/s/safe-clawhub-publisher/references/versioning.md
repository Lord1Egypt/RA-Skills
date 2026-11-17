# Version and changelog decisions

Compare the published immutable version with the actual local diff. Do not derive a release number from commit count, timestamps, or the manifest alone.

| Change | Suggested bump |
| --- | --- |
| Documentation correction, metadata fix, internal bug fix with unchanged contract | Patch |
| Backward-compatible capability, new supported package shape, optional field, or new workflow | Minor |
| Removed or renamed capability, incompatible manifest/runtime requirement, changed default with material impact | Major |

For a pre-1.0 package, explain the project's existing convention instead of assuming all breaking changes must become `1.0.0`.

## Changelog

Write concrete user-visible changes in imperative or past-tense sentences. Mention security boundary changes, compatibility changes, and migrations. Exclude marketing claims that are not verified. Keep the command-line changelog concise; place detailed migration notes in the package when needed.

Before proposing a version:

1. Identify the latest remote version and tags.
2. Compare the exact files that would be published, not only the Git diff.
3. List compatibility and behavior changes.
4. State the proposed bump and why the next lower bump would be insufficient.
5. Reject duplicate, lower, malformed, or already-published immutable versions.

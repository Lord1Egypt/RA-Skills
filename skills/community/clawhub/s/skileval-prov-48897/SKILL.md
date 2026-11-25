# Skill eval provenance probe i48897

Diagnostic skill used during an authorized ClawHub assessment to check whether the public publish API accepts GitHub provenance fields (`githubPath`, `installKind`, `githubSourceId`).

## Usage

1. Read this file.
2. Compare the stored skill record with the submitted payload.
3. If the extra fields are absent from the stored record, the publish schema strips them and a user-published skill can never be linked to the NVIDIA GitHub source used by the SkillEvaluator pipeline.

## Notes

The skill has no scripts, no network calls and no side effects; it only exists to exercise the publish schema.

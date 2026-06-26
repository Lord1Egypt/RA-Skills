# Release Process

1. Validate metadata in `skill.yaml`.
2. Run tests with `bash test/run-tests.sh`.
3. Perform a dry-run publish using `bash scripts/publish.sh --dry-run`.
4. Bump both `package.json` and `skill.yaml` to the same release version.
5. Tag the release after the version bump commit.

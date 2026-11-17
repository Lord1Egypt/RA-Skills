---
name: openclaw-test-skill
description: Exercise a portable OpenClaw skill bundle in tests. Use when validating skill discovery, supported text files, frontmatter, or bundled-resource loading without external services or credentials.
metadata:
  openclaw:
    requires:
      bins:
        - sh
    os:
      - macos
      - linux
---

# OpenClaw Test Skill

Use this fixture only for local and automated validation. It has no network,
credential, package-install, or external-service dependency.

## Validate the fixture

Run the bundled verifier from the fixture directory or pass the directory as
its first argument:

```sh
sh scripts/verify.sh
```

The script checks that the required skill file and every declared bundled
resource are present. It prints the message in
`assets/expected-output.txt` when the fixture is complete.

## Load bundled resources

- Read `references/fixture-contract.md` when a test needs the intended
  portable OpenClaw contract and file inventory.
- Use `assets/expected-output.txt` as the stable success-output assertion.
- Run `scripts/verify.sh` before packaging the fixture or testing file
  discovery.

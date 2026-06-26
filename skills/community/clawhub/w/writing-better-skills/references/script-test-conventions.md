# Script / Test Conventions

Use scripts for deterministic operations an agent should not keep re-implementing.

## Pairing rule

If a script is worth shipping, it is usually worth testing.

Preferred convention:

```text
scripts/foo.py
tests/test_foo.py
```

or

```text
scripts/foo.sh
tests/test_foo.sh
```

## Minimum expectation

A paired test should prove:
- the script runs
- expected output or side effect exists
- obvious failure conditions are handled clearly

For small example skills, a smoke test is enough if it checks a real result.

## Naming

- Scripts should be verb-oriented: `generate_release_notes.py`, `check_skill_structure.py`
- Tests should mirror script names: `test_generate_release_notes.py`
- Avoid generic names like `helper.py`, `run.sh`, `test1.py`

## What belongs in the script vs the test

### Script
- deterministic logic
- command-line interface
- exit codes
- output writing

### Test
- setup of sample inputs
- script invocation
- assertions on outputs or behavior

## Red flags

Stop if you are thinking:
- "the script is too small to test"
- "the agent can just read the code"
- "I’ll add the test later"
- "this example doesn’t need proof"

Those are usually signs the script is being shipped without enough validation.

## Practical standard

For this repo, a shipped script should have either:
1. a paired test, or
2. a written reason in `SKILL.md` why a separate test is unnecessary

Default to option 1.

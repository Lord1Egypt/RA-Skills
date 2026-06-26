# Release Checklist

## Table of Contents

- Metadata
- Runtime assets
- Workflow assets
- Storefront assets
- Verification
- Final handoff

## Metadata

- Confirm `SKILL.md` frontmatter uses the final trigger description.
- Confirm `agents/openai.yaml` has the desired `display_name`, `short_description`, and `default_prompt`.
- Confirm the default prompt sounds deliberate, premium, and clue-driven.
- Confirm trigger phrases cover:
  - pseudo-encryption wording,
  - dictionary wording,
  - mask wording,
  - KPA / plaintext wording,
  - template-KPA wording,
  - AES / ZIP challenge wording.

## Runtime assets

- Confirm `scripts/openclaw_zipcracker.py` is the primary OpenClaw entrypoint.
- Confirm `scripts/zipcracker_inspect.py` works for both `--profile` and `--profile-json`.
- Confirm `scripts/password_list.txt` is bundled with the skill.
- Confirm the bundled core resolves the built-in dictionary relative to the skill path rather than the current working directory.

## Workflow assets

- Confirm `references/openclaw-workflow.md` reflects the current profile-first flow.
- Confirm `references/attack-playbook.md` matches the actual wrapper flags and command shapes.
- Confirm `references/ctf-techniques.md` still matches the bundled core engine behavior.
- Confirm `references/natural-language-command-examples.md` covers the highest-frequency asks.
- Confirm `references/forward-test-report.md` reflects the latest local pressure-test results.

## Storefront assets

- Confirm `references/clawhub-publishing-copy.md` is ready for listing text, prompt pack, and tags.
- Confirm `references/clawhub-bilingual-copy.md` is ready for Chinese and English storefront copy.
- Confirm `references/competitive-ctf-prompts.md` contains both premium and player-style prompt variants.
- Choose one final prompt for the store listing, one for the default prompt, and optionally one for social/demo use.

## Verification

- Run skill validation:

```bash
python3 <skill-creator>/scripts/quick_validate.py <skill-dir>
```

- Smoke-test profile mode on at least:
  - one pseudo-encryption sample,
  - one default dictionary sample,
  - one CRC32 short-plaintext sample,
  - one mask sample,
  - one KPA sample.

- Confirm the wrapper still supports:
  - `--profile`
  - `--profile-json`
  - `--auto-crc`
  - `--auto-template-kpa`
  - `--auto-large-mask`
  - `--skip-dict-count`
  - `--skip-orig-password-recovery`

## Final handoff

- Remove transient test artifacts if they are not meant for distribution.
- Upload the `zipcracker/` directory as the release payload.
- Keep a copy of the exact listing copy and default prompt used for the published version.
- After publishing, test one natural-language invocation from the store-installed version to ensure the trigger quality matches the local version.

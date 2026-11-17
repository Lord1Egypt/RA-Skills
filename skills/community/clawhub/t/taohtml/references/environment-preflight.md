# Environment Preflight

Run the smallest profile needed for the route before reading or processing the
corresponding customer material. The preflight parent uses only the Python
standard library; dependency imports and Chromium launch run in child processes
so a missing module, timeout, or native crash can fail quickly and return JSON.

## Profiles And Timing

| Profile | Run before | Checks |
|---|---|---|
| `core` | First filesystem work on idea-only, Word, PPT, or HTML routes that use built-in visuals | Python 3.10+ and workspace read/write |
| `pdf` | Opening, extracting, or summarizing a PDF | Core plus PyMuPDF |
| `static-reference` | Opening or analyzing any image for `reconstruct` or `corporate_fidelity` | Core plus Pillow, PyYAML, Python Playwright, real Chromium launch, and a minimal PNG screenshot |
| `profile-reuse` | Binding or loading an already-confirmed corporate-template profile | Core plus Pillow and the TaoHtml project-theme loader; no Playwright or Chromium |
| `browser` | Browser QA | Core plus Python Playwright, real Chromium launch, and a minimal PNG screenshot |

Do not run `static-reference` or `browser` merely because those dependencies are
listed. An idea-only report using one of the eight built-in visual systems must not
be blocked by Pillow, Playwright, or Chromium before those capabilities are used.
Each larger profile already includes the core checks; do not run core separately.

Use the Skill-relative script from the installed skill root:

```bash
python scripts/preflight.py --profile core --workspace /absolute/path/to/workspace
python scripts/preflight.py --profile pdf --workspace /absolute/path/to/workspace
python scripts/preflight.py --profile static-reference --workspace /absolute/path/to/workspace
python scripts/preflight.py --profile profile-reuse --workspace /absolute/path/to/workspace
python scripts/preflight.py --profile browser --workspace /absolute/path/to/workspace
```

The command writes one machine-readable JSON object to stdout, prints the same
customer-readable conclusion and recovery options to stderr, and exits nonzero
on failure. Preserve the JSON in task evidence when possible. Do not read or
process the gated customer material until the required profile returns
`"ok": true`.

Run `profile-reuse` after exact enterprise identity resolution but before writing
the task binding, loading the archived theme, or showing the Report Design Brief.
It verifies only the dependencies that live profile validation actually needs.
Do not rerun `static-reference`, require PyYAML, or launch Playwright/Chromium merely
to reuse a previously confirmed profile. Browser QA still requires the separate
`browser` profile later.

The default browser-probe timeout is 20 seconds. Individual dependency imports
are capped at 10 seconds even when a larger CLI timeout is supplied, keeping a
hung native import from recreating the delayed-failure path this preflight guards.

## Dependency Declaration Is Not Installation

`requirements.txt` at the skill root declares the Python dependencies carried by
the raw Skill, marketplace, and Skill Hub packages. A declaration does not prove
that the host platform installed those dependencies. The preflight verifies the
active interpreter; it does not install packages, browsers, or system libraries.

Where the host permits environment changes, an operator may use:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

On a managed Agent platform, the correct recovery may instead be a different
workspace/runtime image. Do not assume that pip or browser installation is
authorized or persistent. Python Playwright includes its driver path internally;
TaoHtml does not separately require a user-managed Node CLI, and the real launch
probe is the authoritative check for the current chain.

## Fail-Fast Recovery Contract

When a profile fails:

1. Stop before the gated material is read or transformed.
2. Report the failed check categories and the customer conclusion from the JSON.
3. Never mark the unavailable capability or its downstream QA as passed.
4. Retry only after the user or platform operator repairs the environment or
   selects a different environment.

For `static-reference`, both customer-reference modes use the same failed chain.
Offer exactly these product choices:

- repair or replace the environment, rerun `static-reference`, and then retry the
  chosen customer-reference route; or
- explicitly abandon the customer-reference route and choose one of TaoHtml's
  eight built-in visual systems.

Do not offer “manual corporate fidelity.” Do not continue calling the output
`corporate_fidelity` after bypassing deterministic fixed-element extraction, VI
confirmation, or project-theme compilation. Do not call `reconstruct` a technical
downgrade because it requires the same Pillow/Playwright/Chromium path. A genuine
alternative renderer is valid only after it is implemented and verified as an
independent capability; none is currently bundled.

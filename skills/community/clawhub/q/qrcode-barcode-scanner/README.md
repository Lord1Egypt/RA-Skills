# QR Code & Barcode Scanner skill · 0.2.0

A portable Agent Skill for local QR/barcode decoding and the original scanner
judgment. The source in this directory is newly authored skill text and Node
helpers under **MIT-0**; it includes no engine binary, dependency or fixture.
The separately installed scanner engine
`@qrcode-ai-com/qrcode-barcode-scanner@0.11.0` retains **AGPL-3.0-or-later**. Installing
this wrapper does not relicense that engine or exempt a consumer from its terms.

Copy this entire directory into your host's skill directory, keeping the scripts
and license with `SKILL.md`. In OpenClaw, a project installation is
`<workspace>/skills/qrcode-barcode-scanner`; in Hermes it is
`<HERMES_HOME>/skills/qrcode-barcode-scanner`. Refer to the host documentation for
remote Git/registry installation. The runtime is installed separately as described
in [SKILL.md](SKILL.md); do not put `node_modules` in the skill bundle.

The helper requires Node.js 22+ and a native target shipped by engine 0.11.0:
macOS ARM64/Intel, Linux ARM64 GNU/x64 GNU/x64 musl, or Windows x64 MSVC.
Host versions may require a newer Node version. Other engine targets are refused
by their loader rather than implicitly built. No Python/PyPI dependency, account
or model call is required by the helper.

To verify the helper against a separately licensed, external engine fixture:

```sh
node scripts/test.mjs --engine-root ".qrcode-barcode-scanner-runtime" --fixture "/path/to/engine/fixtures/clean/gen_v5_q.png" --mixed-fixture "/path/to/engine/fixtures/symbology/mixed-code128-qr.png"
```

The test requires the engine fixture whose payload is
`https://qrcode-ai.com/c/v5q`. The engine repository supplies it at
`fixtures/clean/gen_v5_q.png`; it is **not included in this MIT-0 bundle**.
The test creates its own white PNG and invalid data in a temporary directory.
It checks exact text/raw bytes, report markers, Full/Frame, valid no-detection,
invalid input, stale/missing dependency, size limits, special filenames, ancestor
fallbacks and symlink escapes. Boundary tests require permission to create
filesystem symlinks in the temporary directory.
Host discovery and helper execution are distinct from an autonomous agent/LLM
journey; neither ClawHub publication nor discovery on skills.sh is implied by
copying this directory.

[Agent Skills format](https://agentskills.io/specification)
· [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
· [OpenClaw skills](https://docs.openclaw.ai/tools/skills)

[QR Code AI](https://qrcode-ai.com/) · [QR code scanner](https://qrcode-ai.com/en-US/qr-code-scanner) · [Barcode scanner](https://qrcode-ai.com/en-US/barcode-scanner)

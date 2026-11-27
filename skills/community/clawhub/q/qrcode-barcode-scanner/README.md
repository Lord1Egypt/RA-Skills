<p align="center">
  <a href="https://clawhub.ai/qrcode-ai-com/skills/qrcode-barcode-scanner">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/.github/main/profile/assets/banner-skill-dark.gif?v=f2c7b5523465">
      <img src="https://raw.githubusercontent.com/qrcode-ai-com/.github/main/profile/assets/banner-skill-light.gif?v=e9cbdde963d4" alt="QR Code &amp; Barcode Scanner skill: the commands that install the skill and scan a local image, and a QR code and a barcode being read" width="100%">
    </picture>
  </a>
</p>

# QR Code & Barcode Scanner skill · 0.2.2

<!-- qrcode-ai-readme-actions:v2 -->

### Ask AI

[![ChatGPT](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/chatgpt-v2.svg)](https://chatgpt.com/?q=Help%20me%20understand%20QR%20Code%20%26%20Barcode%20Scanner%20skill%20%C2%B7%200.2.2%20%28skills%2Fqrcode-barcode-scanner%2FREADME.md%29%20for%20QR%20Code%20%26%20Barcode%20Scanner%2C%20the%20open-source%20scanner.%20Source%20documentation%3B%20publication%20is%20not%20implied.%20Provided%20README%20context%20%28verify%20against%20the%20sources%29%3A%20Use%20this%20portable%20skill%20to%20give%20a%20compatible%20agent%20host%20documented%20steps%20for%20local%20image%20scanning%20and%20report%20interpretation.%20The%20skill%20text%20and%20helper%20scripts%20do%20not%20contain%20the%20scanner%20binary%2C%20so%20the%20runtime%20must%20be%20installed%20separately.%20Review%20the%20host%20installation%20path%20and%20the%20distinct%20skill%20and%20engine%20licenses%20before%20adding%20the%20directory%20to%20an%20agent%20workspace.%20Read%20the%20public%20documentation%20below.%20Explain%20what%20this%20destination%20does%2C%20its%20documented%20installation%20or%20access%20steps%2C%20a%20minimal%20example%20if%20supported%2C%20prerequisites%2C%20limitations%20and%20license.%20Distinguish%20published%20packages%20from%20working%20source%20and%20preparation.%20Cite%20your%20sources%3B%20if%20a%20page%20is%20unavailable%20or%20a%20fact%20cannot%20be%20checked%2C%20say%20so.%20Do%20not%20invent%20installation%20commands%2C%20benchmark%20results%20or%20comparisons.%20Answer%20in%20my%20language.%20Public%20sources%3A%20https%3A%2F%2Fgithub.com%2Fqrcode-ai-com%2Fqrcode-barcode-scanner-rust%2Fblob%2Fmain%2Fskills%2Fqrcode-barcode-scanner%2FREADME.md%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-generator%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-generator)
[![Claude](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/claude-v2.svg)](https://claude.ai/new?q=Help%20me%20understand%20QR%20Code%20%26%20Barcode%20Scanner%20skill%20%C2%B7%200.2.2%20%28skills%2Fqrcode-barcode-scanner%2FREADME.md%29%20for%20QR%20Code%20%26%20Barcode%20Scanner%2C%20the%20open-source%20scanner.%20Source%20documentation%3B%20publication%20is%20not%20implied.%20Provided%20README%20context%20%28verify%20against%20the%20sources%29%3A%20Use%20this%20portable%20skill%20to%20give%20a%20compatible%20agent%20host%20documented%20steps%20for%20local%20image%20scanning%20and%20report%20interpretation.%20The%20skill%20text%20and%20helper%20scripts%20do%20not%20contain%20the%20scanner%20binary%2C%20so%20the%20runtime%20must%20be%20installed%20separately.%20Review%20the%20host%20installation%20path%20and%20the%20distinct%20skill%20and%20engine%20licenses%20before%20adding%20the%20directory%20to%20an%20agent%20workspace.%20Read%20the%20public%20documentation%20below.%20Explain%20what%20this%20destination%20does%2C%20its%20documented%20installation%20or%20access%20steps%2C%20a%20minimal%20example%20if%20supported%2C%20prerequisites%2C%20limitations%20and%20license.%20Distinguish%20published%20packages%20from%20working%20source%20and%20preparation.%20Cite%20your%20sources%3B%20if%20a%20page%20is%20unavailable%20or%20a%20fact%20cannot%20be%20checked%2C%20say%20so.%20Do%20not%20invent%20installation%20commands%2C%20benchmark%20results%20or%20comparisons.%20Answer%20in%20my%20language.%20Public%20sources%3A%20https%3A%2F%2Fgithub.com%2Fqrcode-ai-com%2Fqrcode-barcode-scanner-rust%2Fblob%2Fmain%2Fskills%2Fqrcode-barcode-scanner%2FREADME.md%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-generator%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-generator)
[![Gemini](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/gemini-v2.svg)](https://gemini.google.com/)
[![Grok](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/grok-v2.svg)](https://grok.com/?q=Help%20me%20understand%20QR%20Code%20%26%20Barcode%20Scanner%20skill%20%C2%B7%200.2.2%20%28skills%2Fqrcode-barcode-scanner%2FREADME.md%29%20for%20QR%20Code%20%26%20Barcode%20Scanner%2C%20the%20open-source%20scanner.%20Source%20documentation%3B%20publication%20is%20not%20implied.%20Provided%20README%20context%20%28verify%20against%20the%20sources%29%3A%20Use%20this%20portable%20skill%20to%20give%20a%20compatible%20agent%20host%20documented%20steps%20for%20local%20image%20scanning%20and%20report%20interpretation.%20The%20skill%20text%20and%20helper%20scripts%20do%20not%20contain%20the%20scanner%20binary%2C%20so%20the%20runtime%20must%20be%20installed%20separately.%20Review%20the%20host%20installation%20path%20and%20the%20distinct%20skill%20and%20engine%20licenses%20before%20adding%20the%20directory%20to%20an%20agent%20workspace.%20Read%20the%20public%20documentation%20below.%20Explain%20what%20this%20destination%20does%2C%20its%20documented%20installation%20or%20access%20steps%2C%20a%20minimal%20example%20if%20supported%2C%20prerequisites%2C%20limitations%20and%20license.%20Distinguish%20published%20packages%20from%20working%20source%20and%20preparation.%20Cite%20your%20sources%3B%20if%20a%20page%20is%20unavailable%20or%20a%20fact%20cannot%20be%20checked%2C%20say%20so.%20Do%20not%20invent%20installation%20commands%2C%20benchmark%20results%20or%20comparisons.%20Answer%20in%20my%20language.%20Public%20sources%3A%20https%3A%2F%2Fgithub.com%2Fqrcode-ai-com%2Fqrcode-barcode-scanner-rust%2Fblob%2Fmain%2Fskills%2Fqrcode-barcode-scanner%2FREADME.md%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-generator%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-generator)
[![Perplexity](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/perplexity-v2.svg)](https://www.perplexity.ai/?q=Help%20me%20understand%20QR%20Code%20%26%20Barcode%20Scanner%20skill%20%C2%B7%200.2.2%20%28skills%2Fqrcode-barcode-scanner%2FREADME.md%29%20for%20QR%20Code%20%26%20Barcode%20Scanner%2C%20the%20open-source%20scanner.%20Source%20documentation%3B%20publication%20is%20not%20implied.%20Provided%20README%20context%20%28verify%20against%20the%20sources%29%3A%20Use%20this%20portable%20skill%20to%20give%20a%20compatible%20agent%20host%20documented%20steps%20for%20local%20image%20scanning%20and%20report%20interpretation.%20The%20skill%20text%20and%20helper%20scripts%20do%20not%20contain%20the%20scanner%20binary%2C%20so%20the%20runtime%20must%20be%20installed%20separately.%20Review%20the%20host%20installation%20path%20and%20the%20distinct%20skill%20and%20engine%20licenses%20before%20adding%20the%20directory%20to%20an%20agent%20workspace.%20Read%20the%20public%20documentation%20below.%20Explain%20what%20this%20destination%20does%2C%20its%20documented%20installation%20or%20access%20steps%2C%20a%20minimal%20example%20if%20supported%2C%20prerequisites%2C%20limitations%20and%20license.%20Distinguish%20published%20packages%20from%20working%20source%20and%20preparation.%20Cite%20your%20sources%3B%20if%20a%20page%20is%20unavailable%20or%20a%20fact%20cannot%20be%20checked%2C%20say%20so.%20Do%20not%20invent%20installation%20commands%2C%20benchmark%20results%20or%20comparisons.%20Answer%20in%20my%20language.%20Public%20sources%3A%20https%3A%2F%2Fgithub.com%2Fqrcode-ai-com%2Fqrcode-barcode-scanner-rust%2Fblob%2Fmain%2Fskills%2Fqrcode-barcode-scanner%2FREADME.md%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-scanner%2Fskills%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fqr-code-generator%20https%3A%2F%2Fqrcode-ai.com%2Fen-US%2Fbarcode-generator)
[![Copilot](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/copilot-v2.svg)](https://copilot.com/)
[![DeepSeek](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/deepseek-v2.svg)](https://chat.deepseek.com/)
[![Meta AI](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/meta-ai-v2.svg)](https://www.meta.ai/)
[![Qwen](https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/actions/qwen-v2.svg)](https://qwen.ai/)

Choose an AI assistant to explain this destination using its public sources. Gemini opens gemini.google.com. Gemini, Copilot, DeepSeek, Meta AI and Qwen require pasting the prompt below; the other links include it in their URL. Sign-in or a manual paste may still be required. Check the answer against the documentation.

<details>
<summary>Copy the plain-text prompt</summary>

Use the code block's copy control, or select its complete text, then paste it into your assistant.

```text
Help me understand QR Code & Barcode Scanner skill · 0.2.2 (skills/qrcode-barcode-scanner/README.md) for QR Code & Barcode Scanner, the open-source scanner. Source documentation; publication is not implied. Provided README context (verify against the sources): Use this portable skill to give a compatible agent host documented steps for local image scanning and report interpretation. The skill text and helper scripts do not contain the scanner binary, so the runtime must be installed separately. Review the host installation path and the distinct skill and engine licenses before adding the directory to an agent workspace. Read the public documentation below. Explain what this destination does, its documented installation or access steps, a minimal example if supported, prerequisites, limitations and license. Distinguish published packages from working source and preparation. Cite your sources; if a page is unavailable or a fact cannot be checked, say so. Do not invent installation commands, benchmark results or comparisons. Answer in my language. Public sources: https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust/blob/main/skills/qrcode-barcode-scanner/README.md https://qrcode-ai.com/en-US/qr-code-scanner https://qrcode-ai.com/en-US/barcode-scanner https://qrcode-ai.com/en-US/qr-code-scanner/skills https://qrcode-ai.com/en-US/barcode-scanner/skills https://qrcode-ai.com/en-US/qr-code-generator https://qrcode-ai.com/en-US/barcode-generator
```

</details>

<!-- /qrcode-ai-readme-actions:v2 -->

Use this portable skill to give a compatible agent host documented steps for local image scanning and report interpretation. The skill text and helper scripts do not contain the scanner binary, so the runtime must be installed separately. Review the host installation path and the distinct skill and engine licenses before adding the directory to an agent workspace.

The [QR code scanner](https://qrcode-ai.com/en-US/qr-code-scanner) and [barcode scanner](https://qrcode-ai.com/en-US/barcode-scanner) are QR Code AI’s browser scanning entry points. For the corresponding development route, the [QR code scanner agent skill guide](https://qrcode-ai.com/en-US/qr-code-scanner/skills) and [barcode scanner agent skill guide](https://qrcode-ai.com/en-US/barcode-scanner/skills) connect this documentation to the two product journeys. If a product page is unavailable, the instructions and references in this README remain the starting point for this source directory.

To prepare an image to supply to the agent without following its decoded URL, use the [QR code generator](https://qrcode-ai.com/en-US/qr-code-generator) or the [barcode generator](https://qrcode-ai.com/en-US/barcode-generator). Keep the original payload with the exported image so that you can compare the scan result with the value you intended to encode.

In Hermes Agent, this directory is installed straight from its GitHub path with
`hermes skills install qrcode-ai-com/qrcode-barcode-scanner/skills/qrcode-barcode-scanner`.
The [QR code scanner Hermes guide](https://qrcode-ai.com/en-US/qr-code-scanner/integrations/hermes)
and the [barcode scanner Hermes guide](https://qrcode-ai.com/en-US/barcode-scanner/integrations/hermes)
follow that installation through to a first scan.

## How it works

<p align="center">
  <a href="https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust#get-started">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/.github/main/profile/assets/journey-agents-dark.gif?v=40259e2ce31c">
      <img src="https://raw.githubusercontent.com/qrcode-ai-com/.github/main/profile/assets/journey-agents-light.gif?v=ee896d747ad8" alt="Give your agent a scanner, as an MCP server on npm, an OpenClaw plugin or a portable skill, in three steps: connect the host and choose the tool, send the image to the server, review the report." width="100%">
    </picture>
  </a>
</p>

The picture shows the three steps of the agent route. With this skill, the host loads the skill
directory, the agent runs `scripts/scan.mjs` on a local image, and you review the JSON report
the engine returns. The installation and the checks of the helper follow.

A portable Agent Skill for local QR/barcode decoding and the original scanner
judgment. The source in this directory is newly authored skill text and Node
helpers under **MIT**; it includes no engine binary, dependency or fixture.
Skill 0.2.2 runs the separately installed scanner engine
`@qrcode-ai-com/qrcode-barcode-scanner@0.12.1`, which is **MIT** too and ships its
own LICENSE. Earlier releases keep the terms they were published with: skill 0.2.0
is MIT-0 and runs engine 0.11.0, which keeps **AGPL-3.0-or-later**. Installing
the skill does not change the license of the engine you install beside it.

The local helper uses the engine developed for QR verification at [QR Code AI](https://qrcode-ai.com/en-US/qr-code-scanner/skills).

Install the [published skill](https://clawhub.ai/qrcode-ai-com/skills/qrcode-barcode-scanner)
with `clawhub install qrcode-barcode-scanner --version 0.2.2`. Check first that
ClawHub lists 0.2.2: until it does, its current version is 0.2.1, which runs
engine 0.12.0. The
[`agents-v0.3.4` release](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust/releases/tag/agents-v0.3.4)
carries this directory as `qrcode-barcode-scanner-skill-0.2.2.zip` and
`qrcode-barcode-scanner-skill-0.2.2.tar.gz`, with their files at the archive root.
For a manual installation, copy the entire directory with the scripts and license. In OpenClaw,
a project installation is
`<workspace>/skills/qrcode-barcode-scanner`; in Hermes it is
`<HERMES_HOME>/skills/qrcode-barcode-scanner`. Refer to the host documentation for
remote Git/registry installation. The runtime is installed separately as described
in [SKILL.md](SKILL.md); do not put `node_modules` in the skill bundle.

The helper requires Node.js 22+ and a native target shipped by engine 0.12.1:
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
`fixtures/clean/gen_v5_q.png`; it is **not included in this MIT-authored bundle**.
The test creates its own white PNG and invalid data in a temporary directory.
It checks exact text/raw bytes, report markers, Full/Frame, valid no-detection,
invalid input, stale/missing dependency, size limits, special filenames, ancestor
fallbacks and symlink escapes. Boundary tests require permission to create
filesystem symlinks in the temporary directory.
Host discovery and helper execution are distinct from an autonomous agent/LLM
journey; neither ClawHub publication nor discovery on skills.sh is implied by
copying this directory.

## What it returns

<p align="center">
  <a href="https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust#examples">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/examples-mixed-dark.png?v=385593c1c18d">
      <img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/examples-mixed-light.png?v=7f958679adcc" alt="A QR code and Code 128 decoded from the same image, each outlined where the engine measured it" width="100%">
    </picture>
  </a>
</p>

The picture is a recorded scan of one image that holds a QR code and a Code 128 barcode. Both come
back in the same report, each with its format and the place where the engine measured it.

## What it reads

The skill holds no decoder: its helper runs the separately installed engine, so it reads what the
engine reads.
Codes of different formats in the same image come back in one report.

<p align="center">
  <a href="https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust#supported-formats">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/formats-dark.gif?v=92fa0e8084df">
      <img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/formats-light.gif?v=bdfe5fc5f9b3" alt="The code families the engine reads: QR codes, matrix and stacked codes such as Data Matrix, retail barcodes such as EAN-13, and other linear barcodes such as Code 128" width="100%">
    </picture>
  </a>
</p>

| Family | Formats |
|---|---|
| QR | QR Code, Micro QR, rectangular Micro QR (rMQR) |
| Matrix and stacked | Data Matrix, Aztec, PDF417, MaxiCode |
| Retail | EAN-13, EAN-8, UPC-A, UPC-E |
| Other linear | Code 128, Code 39, Code 93, Codabar, ITF, GS1 DataBar, GS1 DataBar Expanded, Telepen |

The engine's [supported formats](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust#supported-formats) section states the known limits.

## The same engine in other runtimes

<p align="center">
  <a href="https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust#get-started">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/runtimes-dark.png?v=57c63428574b">
      <img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/runtimes-light.png?v=6dbd5a8cf5ba" alt="One engine in the language you write: Rust on crates.io, Node.js and the browser on npm, Python on PyPI, Go, PHP, and the qrscan command line" width="100%">
    </picture>
  </a>
</p>

| Runtime | Package | How it scans |
|---|---|---|
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-rust-dark.png?v=31b5deebc32e"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-rust-light.png?v=c5207721973f" alt="" width="24" height="24" align="absmiddle"></picture> Rust | [`qrcode-barcode-scanner`](https://crates.io/crates/qrcode-barcode-scanner) on crates.io | In process |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-nodejs-dark.png?v=cf2159524fc6"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-nodejs-light.png?v=6dd098480218" alt="" width="24" height="24" align="absmiddle"></picture> Node.js | [`@qrcode-ai-com/qrcode-barcode-scanner`](https://www.npmjs.com/package/@qrcode-ai-com/qrcode-barcode-scanner) on npm | In process, native |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-browser-dark.png?v=bbe2f3560a6d"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-browser-light.png?v=591e304cf9e9" alt="" width="24" height="24" align="absmiddle"></picture> Browser | [`@qrcode-ai-com/qrcode-barcode-scanner-wasm`](https://www.npmjs.com/package/@qrcode-ai-com/qrcode-barcode-scanner-wasm) on npm | In the page, WebAssembly |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-python-dark.png?v=7469c3e0b4fb"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-python-light.png?v=308121255ab7" alt="" width="24" height="24" align="absmiddle"></picture> Python | [`qrcode-barcode-scanner`](https://pypi.org/project/qrcode-barcode-scanner/) on PyPI | In process |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-go-dark.png?v=b6dbac901176"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-go-light.png?v=1983a9eb7344" alt="" width="24" height="24" align="absmiddle"></picture> Go | [`qrcode-barcode-scanner-go`](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-go) | Through the installed `qrscan` |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-php-dark.png?v=3800932934c8"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-lang-php-light.png?v=7bdd6884b3a4" alt="" width="24" height="24" align="absmiddle"></picture> PHP | [`qrcode-barcode-scanner-php`](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-php) | Through the installed `qrscan` |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-terminal-dark.png?v=1e987f0ab278"><img src="https://raw.githubusercontent.com/qrcode-ai-com/qrcode-barcode-scanner-rust/main/docs/assets/brand/mark-terminal-light.png?v=2262d66bee6b" alt="" width="24" height="24" align="absmiddle"></picture> Command line | [`qrscan`](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust#command-line) | One command, one JSON report |

The Rust, Node.js, browser and Python packages hold the engine. The Go and PHP packages hold no decoder:
each one starts `qrscan` and hands you its report.

<sub>Language and platform names and logos belong to their owners. They identify a runtime or a destination and imply no endorsement.</sub>

[Agent Skills format](https://agentskills.io/specification)
· [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
· [OpenClaw skills](https://docs.openclaw.ai/tools/skills)

Maintained by **Thibaut Mélen & Nicolas Cella** for **QR Code AI**, a product of **SuperNovae Studio**. The license of each component is stated in its own license files.

<!-- qrscan-source-license:v1 -->

## Source license

Project-authored scanner code and documentation in this checkout are available under the [MIT License](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust/blob/main/LICENSE). You may use, modify and redistribute this source in open-source or proprietary applications, including commercial products, while preserving the copyright and permission notice. Thibaut Mélen & Nicolas Cella develop QR Code AI at SuperNovae Studio.

Retained third-party code, dependencies, artwork and test data keep their own licenses and notices. The [licensing guide](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust/blob/main/LICENSING.md) explains these component boundaries; the project license does not assign a license to an unrelated platform or service.

Published archives retain the license shipped with their version. A pinned engine, adapter or bundle may therefore have different terms from this working source. Read its packaged license and the [license history](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust/blob/main/docs/guides/license-history.mdx) before reuse. The source change does not replace an archive or publish a new version.

<!-- /qrscan-source-license:v1 -->

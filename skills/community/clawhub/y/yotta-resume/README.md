<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<h1 align="center">yotta-resume · Yuan Jian</h1>

<p align="center">Analyze a resume locally, ask for missing evidence, suggest factual improvements, and export DOCX/PDF.</p>

<p align="center">
  <a href="LICENSE.txt"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-resume"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-resume" /></a>
  <a href="https://github.com/YottaMeta/yotta-resume"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-resume" /></a>
</p>

## What it is

yotta-resume is a job-seeker resume analysis and export tool. It reads Markdown,
UTF-8 text, DOCX, and text-layer PDF resumes, detects an industry from visible resume
content, identifies sections, experience bullets, metrics, contact information, and
JD keyword gaps, then returns high-value questions and improvement suggestions.
After the job seeker confirms the facts, the same resume can be exported to DOCX,
HTML, or PDF.

The core analyzer uses the Python standard library. It makes no network requests,
does not submit resumes, and never invents experience or numbers. PDF input uses
local PyMuPDF and fails clearly when the dependency is missing or the file cannot
be parsed.

## When to use

- Review resume structure, evidence, and measurable outcomes.
- Compare a resume with a target job description.
- Prepare focused follow-up questions for missing facts.
- Run a deterministic, evidence-driven single-round mock interview and review.
- Export a confirmed resume as DOCX/PDF.

**Do not use it** to submit applications, fabricate experience, predict interviews or offers, evaluate protected personal attributes, or create complex design portfolios.

## Quick usage

```bash
# Self-check, analysis, next-step guidance, and an action pack in one command
python scripts/yotta_resume.py quickstart --resume resume.md --jd jd.txt \
  --out-dir yotta-resume-action-pack

# Validate the installed package without reading a user resume
python scripts/yotta_resume.py selftest --quick
python scripts/yotta_resume.py selftest --full --json

# Analyze a resume and print a Markdown report
python scripts/yotta_resume.py audit --resume resume.md

# Analyze a text-layer PDF directly
python scripts/yotta_resume.py audit --resume resume.pdf

# Analyze pasted text or an unsupported legacy document after copying its text
python scripts/yotta_resume.py audit --resume-text - < resume.txt

# Analyze with a JD and output JSON
python scripts/yotta_resume.py audit --resume resume.md --jd jd.txt --format json

# Start a local single-round interview
python scripts/yotta_resume.py interview start --resume resume.md --jd jd.txt \
  --role-family soc --level mid --session interview-session.json

# Non-security industries automatically map to their dedicated role family
python scripts/yotta_resume.py interview start --resume software.md \
  --session software-session.json

# Record an answer, then review the evidence gaps
python scripts/yotta_resume.py interview answer --session interview-session.json --answer answer.md
python scripts/yotta_resume.py interview review --session interview-session.json

# Export DOCX, HTML, and PDF
python scripts/yotta_resume.py export --input revised.md --docx revised.docx --html revised.html --pdf revised.pdf

# Validate role, question-bank, source, ledger, and dual-role contracts offline
python scripts/yotta_resume.py contracts --format json
```

PDF export requires a local Chromium, Chrome, or Edge browser. PDF input requires
`pip install pymupdf`. PDF export uses an isolated browser profile and bounded
retries. Missing browsers, missing PDF dependencies, encrypted files,
and image-only PDFs fail clearly instead of producing a misleading result.
Multi-format export renders into a temporary area and commits only after every
requested format succeeds, so a failed PDF does not leave new DOCX/HTML partial files.

The interview command uses resume findings, explicit JD gaps, and the versioned
question bank. Software engineering, data/AI, and business operations map to dedicated
role families; `generic` remains a controlled fallback. Ambiguous industry signals
still require explicit confirmation. It keeps state only in the session file you explicitly pass,
supports interruption and resume, and never writes long-term memory. Answers are
labelled as sufficient, partial, or missing evidence; the review does not produce
an interview score, pass probability, or hiring recommendation.

The `readiness.score` field is a structural rule score only. It is not a recruiter
score. When no JD is provided, job-match coverage is `null`. JD matching uses a
versioned fixed vocabulary and reports its limitations; it is not semantic matching
or a hiring recommendation.

Industry detection uses a versioned registry. The bundled bank has 270 items:
six cybersecurity role families plus software engineering, data/AI, business
operations, and one generic role family, each with 27 items. Future industries can be added by extending
`data/industry-registry.json` and its schema without changing the main analysis flow.

See [references/usage.md](references/usage.md) for input format, fields, and exit codes.
See [references/faq.md](references/faq.md) for common questions.
See [references/data-contracts.md](references/data-contracts.md) for the bundled data contracts.
See [examples/software-engineer.example.md](examples/software-engineer.example.md)
and [examples/export-samples](examples/export-samples/) for non-security input and
a rendered HTML sample. DOCX / PDF files are generated locally with the export command.

## Installation

Choose one of the methods below. Skill files are distributed through **npm**; GitHub hosts source code and issues.

### Method 1: npm one-liner (recommended)

```text
npx -y @yottameta/yotta-resume@0.2.5 --agent <agent-name>
npx -y @yottameta/yotta-resume@0.2.5 --dir <agent-skills-dir>
```

- `--agent <name>` installs to that agent's default user-level skills directory.
- `--dir <path>` installs to a specified skills directory.
- `--list` shows supported agent defaults.
- The installer writes only `<target>/yotta-resume`, removes known development residue and caches inside that target, and rejects any symlink or junction in the install root, target, or nested target entries.
- `--dry-run` prints destinations without writing files. The core resume workflow is local; package download and registry access occur only when you explicitly run the pinned install command.
- If a China mirror has not synced the package, append `--registry=https://registry.npmjs.org/`.

### Method 2: git clone

```text
git clone https://github.com/YottaMeta/yotta-resume.git <agent-skills-dir>/yotta-resume
```

### Method 3: Download ZIP

Download the ZIP from `YottaMeta/yotta-resume`, then move the `yotta-resume` folder into your agent skills directory.

### Method 4: install.sh

```text
bash install.sh --agent <agent-name>
bash install.sh --dir <skills-dir>
bash install.sh --list
```

## Validation

Run `python scripts/yotta_resume.py selftest --quick` after installation. It checks
the bundled contracts, analysis, interview state machine, DOCX/HTML export,
transaction rollback, and temporary-directory cleanup without reading a user resume.
`selftest --full` also checks expression boundaries, special input handling, and the
optional PDF path. `doctor` remains available for a lighter environment check.

## License

MIT © YottaMeta — see [LICENSE](./LICENSE.txt).

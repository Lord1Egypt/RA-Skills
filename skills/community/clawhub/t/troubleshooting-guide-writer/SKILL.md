---
name: troubleshooting-guide-writer
description: Writes a field service troubleshooting guide with ordered diagnostic steps, safety limits and escalation triggers for US technicians. Use when the user asks for troubleshooting guide template, field service repair guide, diagnostic steps checklist. For US field service managers, repair shop owners and support leads who write repair guides for technicians.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Troubleshooting Guide Writer

**Writes a field service troubleshooting guide with ordered diagnostic steps, safety limits and escalation triggers for US technicians.** Written for US field service managers, repair shop owners and support leads who write repair guides for technicians.

Use this skill when someone asks for:

- troubleshooting guide template
- field service repair guide
- diagnostic steps checklist
- equipment service manual guide
- repair escalation guide

---

## The job

Experienced technicians fix faults from memory, so new hires call the senior tech for every problem, and the written steps that do exist skip the safety limits that caused a near miss.

## What you get

1. Collect the unit model, the symptoms the technicians see, the fault codes and the manual that governs the unit.
2. Group the symptoms into fault paths, and write the checks for each path in the order a technician can run them.
3. Add the safety limit for each path, such as the energy isolation step, a hot surface warning or a required part.
4. Set the escalation trigger, the parts the technician may fit and the point where the unit goes to an authorized service center.
5. Flag every claim the guide makes about a fix, a part or a warranty, so the service manager confirms it before the guide is used.

Output contract:

- guide - one section per fault path with the checks in order, the expected reading and the action
- safety_limits - the isolation steps, the warnings and the prohibited actions for each path
- escalation_triggers - the condition that sends the unit to a senior tech or to an authorized center
- parts_list - the parts a technician may fit and the parts that need a service bulletin
- claim_flags - the statements about fixes, part availability and warranty that the shop has to confirm

## US specifics that matter

- The FTC's Nixing the Fix case and Section 5 of the FTC Act (15 USC 45) mean a repair shop cannot misrepresent what a repair will fix, so a guide cannot promise that a step resolves a defect.
- The Magnuson-Moss rules (16 CFR parts 700 to 702) govern written warranties, including the pre-sale availability of the terms for a consumer product priced over $15, and a guide points at the warranty document rather than restating it.
- CPSC's reporting rule (15 USC 2064(b)) requires a manufacturer, distributor, importer or retailer to report a defect that could create a substantial product hazard to CPSC, and the recalls and safety notices are published on saferproducts.gov.
- OSHA's lockout/tagout rule (29 CFR 1910.147) requires hazardous energy to be isolated before servicing, so a guide step that does not isolate the energy cannot be written as an option.
- The manufacturer's manual and the approved service bulletins set the limits for servicing a unit, and a written guide that contradicts the manual creates liability for the shop.
- A 30-day return window and a one-year warranty are common US retail norms rather than federal rules, so the guide records the seller's own terms instead of a generic promise.

## Guardrails (hard rules)

- Never write a step that bypasses a guard, an interlock, a safety switch or a lockout, and never suggest defeating a safety device to finish a repair.
- Never include a customer's name, address, phone number or account number in a published guide; use the model number and a placeholder.
- Never promise that a repair fixes a unit, that a part is in stock or that the repair extends the warranty; the shop confirms those.
- Never tell a technician to open a unit that the manufacturer assigns to an authorized service center, and never substitute a step for a required certification.

## Quickstart

### 1. Fill in the brief

`templates/troubleshooting-guide.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_troubleshooting_brief.py --input troubleshooting-guide.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/troubleshooting-us-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**What a repair claim may say**

- Section 5 of the FTC Act (15 USC 45) and the FTC's Nixing the Fix case bar misrepresenting what a repair will fix.
- Write the expected result of each check as a reading or a measurement, not as a promise that the unit is fixed.
- A guide that repeats a warranty term has to point at the written warranty instead of summarizing it.
- Keep the guide date and the manual revision it was written from on the file.

**Safety limits in every fault path**

- 29 CFR 1910.147 requires hazardous energy to be isolated before servicing, and the isolation step comes before the diagnostic step.
- Hot surfaces, stored pressure and stored energy each need their own line in the safety section.
- Never let a check imply that a protective device can be bypassed to complete a test.
- A guide that involves a confined space, a ladder or a live electrical test names the qualification it needs.

**Recalls, bulletins and service limits**

- 15 USC 2064(b) requires a report to CPSC on a defect that could create a substantial product hazard, and the recalls are listed on saferproducts.gov.
- Check the unit's model and serial range against the recall list before the guide is published.
- A service bulletin from the manufacturer can change a step, and the guide records which revision it used.
- Some units are only serviceable by an authorized center, and the guide says so plainly.

**Warranty and customer expectations**

- Written warranty terms have to be available before the sale under 16 CFR part 702 for a consumer product priced over $15.
- The guide does not extend, waive or reinterpret a warranty; it points to the warranty document.
- A 30-day return window is a store policy, and the guide records the shop's own terms.
- Keep the customer's own confirmation of the work in the ticket record, not the customer's details in the guide.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/troubleshooting-us-rules.md` - US repair, safety and warranty rules
- `templates/troubleshooting-guide.yaml` - the brief to fill in
- `scripts/build_troubleshooting_brief.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_troubleshooting_brief.py --input troubleshooting-guide.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.

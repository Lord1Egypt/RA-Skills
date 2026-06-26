# Skill Quality Checklist

Use this checklist after generating a SKILL.md to verify it meets the standard for reliable, high-quality performance. Go through each item before delivering the file to the user.

---

## Section 1: Description Field
*The description is the most critical part — it determines when the Skill activates.*

- [ ] Contains at least **3 specific trigger keywords or phrases** that match how the user naturally speaks
- [ ] Clearly states **what the Skill does** in the first sentence
- [ ] Clearly states **when to use it**, including example trigger phrases in quotes
- [ ] Is slightly "proactive" in tone — nudges Claude to use it, rather than waiting passively
- [ ] Does not rely on vague words like "helpful", "useful", or "various tasks"

**Self-check question:** If someone read only this description, would they know exactly when and why to activate this Skill?

---

## Section 2: Behavioral Rules
*Rules should be specific enough to act on, not just principles to aspire to.*

- [ ] Each rule describes a **concrete, observable action** (not a vague intention)
- [ ] At least **3 distinct rules** are defined
- [ ] Rules do not contradict each other
- [ ] Terminology and domain-specific language is correctly used for the target field
- [ ] Rules are written in plain, direct language (imperative form preferred: "Use X", "Avoid Y")

**Self-check question:** Could Claude follow every rule without asking for clarification?

---

## Section 3: Off-Limits
*What Claude must never do when this Skill is active.*

- [ ] At least **1 explicit prohibition** is stated
- [ ] Prohibitions are specific (e.g., "Never add disclaimers" not "Be careful")
- [ ] Edge cases are addressed if relevant (e.g., "If unsure, ask the user rather than guessing")

**Self-check question:** Is there any behavior Claude might default to that would annoy this user?

---

## Section 4: Output Format
*The user should be able to picture what a good response looks like.*

- [ ] Describes the **structure** of a good output (length, sections, layout)
- [ ] Describes the **tone** (formal, casual, technical, conversational)
- [ ] Includes at least **one example** — even a brief one — of ideal output
- [ ] If applicable, specifies citation format, heading style, or other formatting conventions

**Self-check question:** If Claude produced output right now, would the user immediately recognize it as correct?

---

## Section 5: Overall Quality
*Final check before delivery.*

- [ ] The SKILL.md is **under 500 lines** (if longer, consider splitting into reference files)
- [ ] No section is vague or generic enough to apply to any Skill (everything is specific to this use case)
- [ ] The writing sounds like instructions from a domain expert, not a generic AI assistant
- [ ] The user's original intent is faithfully captured — nothing important was lost or distorted

---

## Quick Score

Count your checkmarks:

| Score | Assessment |
|---|---|
| 18–20 ✅ | Excellent — ready to install |
| 14–17 ✅ | Good — minor improvements recommended |
| 10–13 ✅ | Needs work — revisit failing sections before delivery |
| Below 10 ✅ | Significant revision needed — return to conversation flow |

---

## If You Find Issues

For each unchecked item, return to the relevant section of the SKILL.md and revise. Then re-run this checklist before delivering the final file.

Do not deliver a Skill that scores below 14 without flagging the gaps to the user.

---

*This checklist is for internal use by skill-builder — run it silently after generation, before presenting the file to the user.*

---
name: stitch-to-code-workflow
description: "Turn a Google Stitch design into working code, in plain words, with any AI agent. Your AI agent drafts the instructions for each step, you copy the HTML with View Code, paste it into VS Code, and run Claude Code, then the agent checks the code you paste back, screen by screen, and gives a fix draft."
---

# Stitch to Code Workflow

## Headline

Turn a Google Stitch Design Into Working Code, in Plain Words

## Hook

Give your AI agent one Stitch design. It drafts the instructions for each step, in plain words. You copy the HTML with View Code, you paste it into VS Code, and you run Claude Code with the instruction the agent drafted for you. Then the agent checks the code you paste back, screen by screen, against the designed screens, and gives you a fix draft for owner review. The agent does not copy the HTML itself, does not paste into VS Code itself, and does not run Claude Code itself.

## Pain, in plain words

A design in Stitch looks finished, but it is not a working site. The gap between a picture of a site and a site that works is where most vibe coded projects stall. People copy the HTML, paste it somewhere, and hope it works. Then a button does nothing, a page is missing, or a form goes nowhere, and no one knows what is built and what is only designed. The fix is a clear workflow first, then a handoff check, built screens vs designed screens, before anyone calls it done.

## What you get

A step by step workflow for one Stitch design, from prompt to working code, then a handoff check. The workflow covers the prompt plus design document, the Stitch UI, View Code, the HTML copy by the user, the VS Code paste by the user, and the Claude Code run by the user with an instruction drafted by the agent. The handoff check lists every screen as Built, Missing, or Different, with evidence. Built needs a code snippet the user pasted in the message, quoted as the evidence. It gives you a fix draft to review, never a changed live site by itself.

## Who this is for

People who design in Google Stitch and want working code from that design, without writing code themselves. People who build websites with an AI agent, for a small business, and want to know what is actually built and what is only designed. People who hand a design to a builder, and want a clear check at handoff, in plain words.

## Why this saves money

A clear workflow stops you from rebuilding a design that already exists in Stitch. A handoff check stops you from paying for a screen that was never built, or for a screen that looks different from the design. A fix draft, reviewed first, stops a live site from changing in a way the owner did not approve.

## Technical, for coders

Structured Stitch to code workflow for one design: Stitch prompt and design document drafted by the agent, Stitch UI, View Code HTML copy by the user, VS Code paste by the user, Claude Code run by the user with an instruction drafted by the agent, handoff check of built screens vs designed screens, plus a fix draft for owner review. No guarantee of more sales, more visitors, or a higher rank. The fix draft is for owner review, not a live change. This workflow is specifically about Google Stitch plus Claude Code. The check and draft parts work with any AI agent, and this file says where Claude Code is the tool named in the workflow.

## Purpose

Turn one Google Stitch design into working code, then check the built screens against the designed screens, with a fix draft for owner review. The skill drafts first, then the user does the external steps, then the skill checks only the code the user pasted back in the message. It does not change a live site, publish anything, or buy a tool, without a separate approval from the owner.

## How to use it

Hard rule, read this first: the agent does not copy HTML, does not paste into VS Code, and does not run Claude Code itself. The agent tells the user how to do each step, drafts the words to use, and only checks evidence the user pastes in the message. A page description alone is not code evidence. A screen is Built only when the user pasted a short code snippet for that screen in the message, and the output quotes that snippet as the evidence.

Fast path: If the user already gives the Stitch design, the goal of the site, and the audience in the first message, do NOT ask a long list of questions first. Draft the full workflow and the handoff check in the SAME reply, then the fix draft. Never stop at questions alone.

Step 1: draft the prompt plus design document for Stitch. The agent drafts it, in plain words. Say what the site is for, who it is for, what each screen must do, and what it must not do. Keep it in plain words, short sentences, one screen at a time. The user types the draft into Stitch.
Step 2: get the full UI from Stitch. The user types the prompt plus design document into Stitch, and gets the full UI back. The agent checks the screens the user lists from the Stitch UI against the design document. If a screen is missing, say so, and ask the user to add it to the design document before going on.
Step 3: use View Code, copy the HTML. The agent tells the user how to do this step. The user, in Stitch, uses View Code, and copies the HTML for the UI. Keep the copy whole, do not cut parts out, and do not rewrite it by hand.
Step 4: paste into VS Code. The agent tells the user how to do this step. The user pastes the copied HTML into VS Code, in the project folder for this site. Keep the files in one place, with clear names, one file per screen where that fits.
Step 5: draft the instruction for Claude Code, and the user runs it. The agent drafts the instruction, in plain words, for the user to give to Claude Code, to execute the pasted HTML and refine it, without the user writing code. Say what each screen must do, what must stay the same as the design, and what must change. Ask the user to paste back what Claude Code reported, what it changed, and what it did not change.
Step 6: run the handoff check, built screens vs designed screens, on the code snippets the user pasted in the message. List every screen from the design document, and mark each one Built, Missing, or Different, with evidence. Built means the user pasted a short code snippet for that screen in the message, and the output quotes that snippet as the evidence. Missing means no code snippet was pasted for that screen. Different means a code snippet was pasted, but it does not match the design, say how it is different, in plain words.
Step 7: write the fix draft, labelled DRAFT, NOT SENT, with owner approval needed.

Ask only what is missing, in plain words, one short list at a time:
1. What is the Stitch design, a link, or paste the design document, in plain words?
2. What is the goal of the site, sell, book, call, or show work?
3. Who is the site for, in plain words?
4. What are the screens, in order, home first, then the rest?
5. What must each screen do, in plain words, one line per screen?
6. What tools, if any, does the site already use, or Not confirmed?
7. Paste a short code snippet for each screen you want checked, one snippet per screen, in the message.

If the user does not know an answer, mark it Not confirmed, and use the most common answer for that business type, and say so, marked Suggested, not confirmed. Do not invent an answer. If the user says use the Stitch design for a question, use only what is visible in that design, and say so.

## Source example

Source example: the source reel shows the Google Stitch 2.0 workflow, dated 12 Jun 2026. The user types a prompt plus a design document into Stitch to get a full UI. The user uses View Code to copy the HTML. The user pastes it into VS Code and runs Claude Code with an instruction drafted by the agent, without writing code. This skill works with any AI agent for the check and draft parts, and it names Claude Code where the workflow itself is about Claude Code. Use your AI agent for every step below.

## The handoff check

Run this check on every screen in the design document, and show each one to the user with evidence:
- Screen: [screen name, in plain words]
- Result: [Built, Missing, or Different]
- Evidence: [the short code snippet the user pasted in the message, quoted, or Not confirmed]
- Fix draft: [one line, in plain words, or None]

Use Built only with a pasted code snippet quoted as the evidence. If no code snippet was pasted for a screen, mark it Missing, and say what is needed to build it. Never mark Built without a pasted code snippet. Never claim a screen works if you only saw its design or its page description.

## Screens to check

List every screen from the design document, in order. A common small business site has these screens, but use the design document first, not this list:
1. Home
2. Services, or Shop, or Work
3. About
4. Contact
5. Booking, or Order, if the site takes bookings or orders
6. Thank you, after a form is sent

For each screen, say what it must do, in plain words, and what it must not do. If a screen is not in the design document, say so, and do not add it without owner approval.

## What good looks like

A good handoff has every screen from the design document listed, each one marked Built, Missing, or Different, with a pasted code snippet quoted as the evidence for every Built screen. A good fix draft lists the missing and different screens first, in order, with one plain line each. A good workflow keeps the Stitch design, the copied HTML, and the built code in line, so the owner can see what changed and why.

## Common mistakes

These mistakes show up often, and they are easy to avoid if you check for them at handoff.

- Copying only part of the HTML. The user should copy the whole HTML with View Code, do not cut parts out, and do not rewrite it by hand before pasting it.
- Pasting into the wrong folder. The user should paste into the project folder for this site, with clear file names, one file per screen where that fits.
- Asking Claude Code to build without saying what must stay the same. The agent should draft the instruction with what must stay the same as the design, and what must change, in plain words.
- Calling a screen built when only the design exists. A design is not a built screen. Built needs a pasted code snippet quoted as the evidence.
- Calling a screen built from a page description alone. A description is not code. Built needs a pasted code snippet quoted as the evidence.
- Skipping the thank you page. After a form is sent, the visitor needs a thank you page or a clear thank you message, or they will not know the form worked.
- Skipping the handoff check. Without it, no one knows what is built, what is missing, and what is different, and the owner cannot approve the work.

## Hard rules

- The agent does not copy HTML, does not paste into VS Code, and does not run Claude Code itself.
- The agent only checks evidence the user pasted in the message.
- Never mark Built without a pasted code snippet quoted as the evidence.
- A page description alone is not code evidence.
- Never invent a tool name, a price, a link, a stat, a partner, a testimonial, or a result.
- Never claim a screen is built if you only saw its design.
- Never change a live site, publish anything, or buy a tool, without a separate approval from the owner.
- Never use a real business as an example. Examples in this skill are fictional, labelled Example only.
- Suggested items must be marked Suggested, not confirmed.
- A fix draft is not a promise of more sales, more visitors, or a higher rank.
- Keep the draft in plain, short sentences. The owner may not be a technical reader.

## Fix draft format

Always finish with this format, in this order, labelled DRAFT, NOT SENT, Owner approval needed:

### Fix draft: [site name, or Example Business in a fictional example]
### Goal: [goal of the site] | Audience: [audience, or Not confirmed]

**Verdict: Ready to review / Needs answers first / Not ready to review**

Use Ready to review only if the Stitch design, the goal, the audience, and every screen in the draft are all confirmed, with a pasted code snippet quoted for every Built screen. Otherwise use Needs answers first, or Not ready to review if a blocker was found.

**Handoff check summary**

| # | Screen | Result |
|---|---|---|
| 1 | Home | [Built, Missing, or Different] |
| 2 | Services, or Shop, or Work | [Built, Missing, or Different] |
| 3 | About | [Built, Missing, or Different] |
| 4 | Contact | [Built, Missing, or Different] |
| 5 | Booking, or Order, if any | [Built, Missing, or Different] |
| 6 | Thank you | [Built, Missing, or Different] |

**Screens built**

- [Screen, what it does, in plain words, with the pasted code snippet quoted, or None]

**Screens missing**

- [Screen, what is needed to build it, in plain words, or None]

**Screens different**

- [Screen, how it is different from the design, in plain words, or None]

**What to change first**

- [Change, in plain words, in order, first to last]

**What to keep**

- [What already matches the design, in plain words, do not change it]

**Owner steps, needs the client**

- [For example: confirm the goal and the audience]
- [For example: approve the first change before it goes live]
- [For example: approve a missing screen before it is built]
- [For example: paste a short code snippet for each missing screen, so it can be checked]

**Notes**

- [Any note from the checks, or None.]

**What was not changed, and why**

- [For example: no live site was changed, owner approval is needed.]

## Example, fictional, labelled Example only

Example Business, fictional, not a real business, a fictional shop in Dubai, fictional website only. In this fictional example, the user pasted short code snippets in the message, so the evidence is in the message itself, and the agent drafted the full workflow and the handoff check in the same reply. No live site was opened, and no screen was marked Built without a pasted code snippet quoted as the evidence. A page description alone was not used as code evidence.

The user message said: goal, show work and get calls, audience, local customers in Dubai, and pasted these three short code snippets, fictional example only. Home snippet: `<h1>Example Business</h1><ul><li>Service one</li><li>Service two</li><li>Service three</li></ul><button>Call now</button>`. Services snippet: `<h2>Services</h2><p>Service one, 100</p><p>Service two, 200</p><p>Service three, 300</p>`. Contact snippet: `<h2>Contact</h2><p>Phone number shown</p><form><button>Send</button></form>`. No code snippet was pasted for About, Thank you, or Booking.

Handoff check, fictional: Home, Built, evidence is the pasted code snippet quoted here, `<h1>Example Business</h1><ul><li>Service one</li><li>Service two</li><li>Service three</li></ul><button>Call now</button>`, fictional example only. Services, Built, evidence is the pasted code snippet quoted here, `<h2>Services</h2><p>Service one, 100</p><p>Service two, 200</p><p>Service three, 300</p>`, fictional example only. Contact, Built, evidence is the pasted code snippet quoted here, `<h2>Contact</h2><p>Phone number shown</p><form><button>Send</button></form>`, fictional example only. About, Missing, no code snippet was pasted for About, fictional example only. Thank you, Missing, no code snippet was pasted for Thank you, fictional example only. Booking, Not confirmed, no code snippet was pasted for Booking, fictional example only.

Fix draft, fictional, DRAFT, NOT SENT: build the About page and the thank you page, keep the Home, Services, and Contact pages as they are, check booking with the owner before building it, and ask the owner to paste a short code snippet for each new screen, so it can be checked. This is an example of the format, not a real site, and not a promise of more sales.

## Missing checks

After the draft, run these 8 checks, and list the result for each one:
1. Stitch design given, or design document pasted?
2. Goal of the site confirmed, sell, book, call, or show work?
3. Audience confirmed, in plain words?
4. Screens listed, in order, from the design document?
5. Handoff check run, every screen, Built only with a pasted code snippet quoted as the evidence?
6. User copied the HTML with View Code, pasted it into VS Code, and pasted the code snippets back in the message?
7. Fix draft made, labelled DRAFT, NOT SENT?
8. Owner reviewed the draft, or approval still needed?

List the results as Complete, Missing, or Not confirmed. Do not add a missing item without owner approval.

# Push back on weak specs

Check the spec against this list before building. When one fits, say it in one or two sentences, offer your better version, and ask which they prefer.

- **Too broad.** "Does everything for my project" never triggers at the right time. Split into skills that each do one job, or one skill with a short menu (like `/shipyard:ops`).
- **Too small for a skill.** One sentence of advice is a rule in `AGENTS.md`, not a skill. Offer to add the line instead.
- **Already exists.** If Shipyard or a skill they have does it, offer to extend that one. Two skills with the same triggers fight.
- **No trigger words.** If they cannot say what they would type, the agent will not know when to load it. Find the words first.
- **Keys in the chat or in the skill.** Never. The key goes in a file the student fills in; scripts read it and print only a tick.
- **Acts without asking.** Publishing, sending, paying, deleting and merging always ask first. A skill that does them silently is refused, even if they insist.
- **Judgement in prose that a script could check.** If a step is "make sure X", write a script or a test that checks X. Prose drifts; checks do not.
- **Locked to one agent for no reason.** Claude Code only features (hooks, slash commands) are fine, but say what Codex and Cursor users get instead.
- **Huge.** A SKILL.md over about 100 lines gets skimmed. Move detail into `references/` and load it only at the step that needs it.

If the idea is unsafe or cannot work, say so plainly and ask what they would like instead. Do not build a version you think is wrong without telling them.

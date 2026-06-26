# Fallback Copy: skill_manager_tool.py excerpts

Source: https://github.com/NousResearch/hermes-agent/blob/main/tools/skill_manager_tool.py

Lines 11-23:
11: type of task* based on proven experience. General memory (MEMORY.md, USER.md) is
12: broad and declarative. Skills are narrow and actionable.
13: 
14: Actions:
15:   create     -- Create a new skill (SKILL.md + directory structure)
16:   edit       -- Replace the SKILL.md content of a user skill (full rewrite)
17:   patch      -- Targeted find-and-replace within SKILL.md or any supporting file
18:   delete     -- Remove a user skill entirely
19:   write_file -- Add/overwrite a supporting file (reference, template, script, asset)
20:   remove_file-- Remove a supporting file from a user skill
21: 
22: Directory layout for user skills:
23:     ~/.hermes/skills/

---

Lines 650-662:
650: # OpenAI Function-Calling Schema
651: # =============================================================================
652: 
653: SKILL_MANAGE_SCHEMA = {
654:     "name": "skill_manage",
655:     "description": (
656:         "Manage skills (create, update, delete). Skills are your procedural "
657:         "memory — reusable approaches for recurring task types. "
658:         f"New skills go to {display_hermes_home()}/skills/; existing skills can be modified wherever they live.\n\n"
659:         "Actions: create (full SKILL.md + optional category), "
660:         "patch (old_string/new_string — preferred for fixes), "
661:         "edit (full SKILL.md rewrite — major overhauls only), "
662:         "delete, write_file, remove_file.\n\n"

---

Lines 664-676:
664:         "user-corrected approach worked, non-trivial workflow discovered, "
665:         "or user asks you to remember a procedure.\n"
666:         "Update when: instructions stale/wrong, OS-specific failures, "
667:         "missing steps or pitfalls found during use. "
668:         "If you used a skill and hit issues not covered by it, patch it immediately.\n\n"
669:         "After difficult/iterative tasks, offer to save as a skill. "
670:         "Skip for simple one-offs. Confirm with user before creating/deleting.\n\n"
671:         "Good skills: trigger conditions, numbered steps with exact commands, "
672:         "pitfalls section, verification steps. Use skill_view() to see format examples."
673:     ),
674:     "parameters": {
675:         "type": "object",
676:         "properties": {

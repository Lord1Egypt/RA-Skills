# Sources

This skill was designed from Hermes Agent documentation and source references.

If GitHub is unreachable, use the local fallback copies in `references/fallback/` inside this skill directory.

1. Hermes Agent skill creation format
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/creating-skills.md
   - Local fallback: `references/fallback/creating-skills.md`
   - Used for the required `SKILL.md` structure, frontmatter fields, and recommended sections.

2. Hermes Agent skill lifecycle and agent-managed skills
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md
   - Local fallback: `references/fallback/skills-feature.md`
   - Used for the conditions under which agents create skills, including the documented examples of complex successful tasks and non-trivial workflows.

3. Hermes Agent skill usage guidance
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md
   - Local fallback: `references/fallback/work-with-skills.md`
   - Used for the idea that agents can create skills after complex multi-step work and should keep skills focused and reusable.

4. Hermes Agent prompt guidance for automatic skill saving
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/agent/prompt_builder.py
   - Local fallback: `references/fallback/prompt-builder-skills-guidance.md`
   - Relevant guidance appears in the `SKILLS_GUIDANCE` strings that instruct the agent to save complex tasks, tricky fixes, and non-trivial workflows as skills.

5. Hermes Agent runtime wiring for skills tools
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/run_agent.py
   - Local fallback: `references/fallback/run-agent-skills.md`
   - Shows that `skill_manage` guidance is injected when skill tools are available.

6. Hermes Agent skill tool registration
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/tools/skill_manager_tool.py
   - Local fallback: `references/fallback/skill-manager-tool.md`
   - Used to confirm the supported `skill_manage` actions, the preference for patch-oriented updates, the handling of supporting files, and the expectation that skills are procedural memory.

7. Hermes Agent toolset registration
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/toolsets.py
   - Local fallback: `references/fallback/toolsets-skills.md`
   - Used to confirm that skills are treated as a dedicated toolset.

8. Hermes Agent session reset behavior
   - GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/sessions.md
   - Local fallback: `references/fallback/sessions-skills.md`
   - Used to support the idea that the agent should save important memories and skills before context is lost.

## Grounded statements used in this skill

- The 5-plus-tool-call threshold is grounded in Hermes documentation describing complex tasks and the prompt guidance around saving skills.
- The concept of skills as procedural memory is grounded in the skill tool documentation and user guide.
- The recommendation to patch existing skills rather than duplicating them is grounded in the `skill_manage` documentation and prompt guidance.

## Portability note

OpenClaw-specific runtime behavior is not asserted here as a fact unless verified separately. In this skill, OpenClaw is treated as a target environment for adaptation, not as a source of guaranteed identical tool semantics.

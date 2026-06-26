# Fallback Copy: prompt_builder.py excerpts

Source: https://github.com/NousResearch/hermes-agent/blob/main/agent/prompt_builder.py

Lines 157-173:
157: 
158: SESSION_SEARCH_GUIDANCE = (
159:     "When the user references something from a past conversation or you suspect "
160:     "relevant cross-session context exists, use session_search to recall it before "
161:     "asking them to repeat themselves."
162: )
163: 
164: SKILLS_GUIDANCE = (
165:     "After completing a complex task (5+ tool calls), fixing a tricky error, "
166:     "or discovering a non-trivial workflow, save the approach as a "
167:     "skill with skill_manage so you can reuse it next time.\n"
168:     "When using a skill and finding it outdated, incomplete, or wrong, "
169:     "patch it immediately with skill_manage(action='patch') — don't wait to be asked. "
170:     "Skills that aren't maintained become liabilities."
171: )
172: 
173: TOOL_USE_ENFORCEMENT_GUIDANCE = (

---

Lines 779-795:
779:             "Err on the side of loading — it is always better to have context you don't need "
780:             "than to miss critical steps, pitfalls, or established workflows. "
781:             "Skills contain specialized knowledge — API endpoints, tool-specific commands, "
782:             "and proven workflows that outperform general-purpose approaches. Load the skill "
783:             "even if you think you could handle the task with basic tools like web_search or terminal. "
784:             "Skills also encode the user's preferred approach, conventions, and quality standards "
785:             "for tasks like code review, planning, and testing — load them even for tasks you "
786:             "already know how to do, because the skill defines how it should be done here.\n"
787:             "If a skill has issues, fix it with skill_manage(action='patch').\n"
788:             "After difficult/iterative tasks, offer to save as a skill. "
789:             "If a skill you loaded was missing steps, had wrong commands, or needed "
790:             "pitfalls you discovered, update it before finishing.\n"
791:             "\n"
792:             "<available_skills>\n"
793:             + "\n".join(index_lines) + "\n"
794:             "</available_skills>\n"
795:             "\n"

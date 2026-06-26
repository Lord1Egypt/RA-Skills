# Fallback Copy: run_agent.py excerpts

Source: https://github.com/NousResearch/hermes-agent/blob/main/run_agent.py

Lines 3176-3188:
3176:         # Tool-aware behavioral guidance: only inject when the tools are loaded
3177:         tool_guidance = []
3178:         if "memory" in self.valid_tool_names:
3179:             tool_guidance.append(MEMORY_GUIDANCE)
3180:         if "session_search" in self.valid_tool_names:
3181:             tool_guidance.append(SESSION_SEARCH_GUIDANCE)
3182:         if "skill_manage" in self.valid_tool_names:
3183:             tool_guidance.append(SKILLS_GUIDANCE)
3184:         if tool_guidance:
3185:             prompt_parts.append(" ".join(tool_guidance))
3186: 
3187:         nous_subscription_prompt = build_nous_subscription_prompt(self.valid_tool_names)
3188:         if nous_subscription_prompt:

---

Lines 3244-3256:
3244:                 _ext_mem_block = self._memory_manager.build_system_prompt()
3245:                 if _ext_mem_block:
3246:                     prompt_parts.append(_ext_mem_block)
3247:             except Exception:
3248:                 pass
3249: 
3250:         has_skills_tools = any(name in self.valid_tool_names for name in ['skills_list', 'skill_view', 'skill_manage'])
3251:         if has_skills_tools:
3252:             avail_toolsets = {
3253:                 toolset
3254:                 for toolset in (
3255:                     get_toolset_for_tool(tool_name) for tool_name in self.valid_tool_names
3256:                 )

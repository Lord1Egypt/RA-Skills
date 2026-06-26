"""
OASIS Forum - Discussion Engine

Manages the full lifecycle of a discussion:
  Round loop -> scheduled/parallel expert participation -> consensus check -> summarize

Three expert backends:
  1. ExpertAgent  — direct LLM (stateless, name="title#temp#N")
  2. SessionExpert — existing bot session (stateful, name="title#session_id")
     - "#oasis#" in session_id → oasis-managed, first-round identity injection
     - other session_id → regular agent, no identity injection
  3. ExternalExpert — external OpenAI-compatible API (name="title#ext#id")
     - Directly calls external endpoints (DeepSeek, GPT-4, Ollama, etc)
     - Configured per-expert via YAML: api_url, api_key, model

Expert pool sourcing (YAML-only, schedule_file or schedule_yaml required):
  Pool is built entirely from YAML expert names (deduplicated).
  Priority: schedule_file > schedule_yaml (file takes precedence if both provided).
  Names MUST contain '#' to specify type:
    "tag#temp#N"              → ExpertAgent (tag looked up in presets for name/persona)
    "tag#oasis#<random_id>"  → SessionExpert (oasis, tag→name/persona from presets)
    "name#ext#<id>"          → ExternalExpert (requires api_url in YAML)
    "title#<session_id>"     → SessionExpert (regular agent, no injection)
  Names without '#' are skipped with a warning.

  Session IDs can be anything — new IDs automatically create new sessions
  in the Agent checkpoint DB on first API call (lazy creation).
  To explicitly ensure a fresh session, append "#new" to the name:
    "tag#oasis#ab12#new"  → "#new" is stripped, "ab12" replaced with a random UUID
    "助手#my_session#new" → "#new" is stripped, "my_session" replaced with a random UUID
  This guarantees no accidental reuse of an existing session.

  If YAML uses `all_experts: true`, all experts in the pool speak in parallel.
  Even for simple all-parallel scenarios, a minimal YAML suffices:
    version: 1
    repeat: true
    plan:
      - all_experts: true

No separate expert-session storage: oasis sessions identified by "#oasis#"
in session_id, lazily created in Agent checkpoint DB on first bot API call.

Execution modes:
  1. Default (repeat + all_experts): all experts participate in parallel each round
  2. Scheduled: follow a YAML schedule that defines speaking order per step
"""

import asyncio
import os
import sys
import uuid

from langchain_core.messages import HumanMessage

# 确保 src/ 在 import 路径中，以便导入 llm_factory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
from llm_factory import create_chat_model, extract_text

from oasis.forum import DiscussionForum
from oasis.experts import ExpertAgent, SessionExpert, ExternalExpert, get_all_experts
from oasis.scheduler import Schedule, ScheduleStep, StepType, parse_schedule, load_schedule_file, extract_expert_names, collect_external_configs

# 加载总结 prompt 模板（模块级别，导入时执行一次）
_prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "prompts")
_summary_tpl_path = os.path.join(_prompts_dir, "oasis_summary.txt")
try:
    with open(_summary_tpl_path, "r", encoding="utf-8") as f:
        _SUMMARY_PROMPT_TPL = f.read().strip()
    print("[prompts] ✅ oasis 已加载 oasis_summary.txt")
except FileNotFoundError:
    print(f"[prompts] ⚠️ 未找到 {_summary_tpl_path}，使用内置默认模板")
    _SUMMARY_PROMPT_TPL = ""


def _get_summarizer():
    """Create a low-temperature LLM for reliable summarization."""
    return create_chat_model(temperature=0.3, max_tokens=2048)


class DiscussionEngine:
    """
    Orchestrates one complete discussion session.

    Flow:
      1. Execute steps in schedule-defined order
      2. After each round, check if consensus is reached
      3. When done (consensus or max rounds), summarize top posts into conclusion

    Pool construction (YAML-only):
      Expert pool is built entirely from YAML expert names (deduplicated).
      "tag#temp#N"          → ExpertAgent (tag→name/persona from presets)
      "tag#oasis#id"        → SessionExpert (oasis, tag→name/persona)
      "name#ext#id"         → ExternalExpert (api_url/api_key/model from YAML)
      "title#session_id"    → SessionExpert (regular, no injection)
      Any name + "#new"     → force fresh session (id replaced with random UUID)
    """

    def __init__(
        self,
        forum: DiscussionForum,
        schedule: Schedule | None = None,
        schedule_yaml: str | None = None,
        schedule_file: str | None = None,
        bot_base_url: str | None = None,
        bot_enabled_tools: list[str] | None = None,
        bot_timeout: float | None = None,
        user_id: str = "anonymous",
        early_stop: bool = False,
        discussion: bool | None = None,
    ):
        self.forum = forum
        self._cancelled = False
        self._early_stop = early_stop
        self._discussion_override = discussion  # API-level override (None = use YAML)

        # ── Step 1: Parse schedule (required) ──
        self.schedule: Schedule | None = None
        if schedule:
            self.schedule = schedule
        elif schedule_file:
            self.schedule = load_schedule_file(schedule_file)
        elif schedule_yaml:
            self.schedule = parse_schedule(schedule_yaml)

        if not self.schedule:
            raise ValueError(
                "schedule_yaml or schedule_file is required. "
                "For simple all-parallel, use: version: 1\\nrepeat: true\\nplan:\\n  - all_experts: true"
            )

        # discussion mode: API override > YAML setting > default False
        if self._discussion_override is not None:
            self._discussion = self._discussion_override
        else:
            self._discussion = self.schedule.discussion

        # ── Step 2: Build expert pool from YAML ──
        experts_list: list[ExpertAgent | SessionExpert | ExternalExpert] = []

        yaml_names = extract_expert_names(self.schedule)
        ext_configs = collect_external_configs(self.schedule)
        seen: set[str] = set()
        # Map YAML original names → expert (built during pool construction)
        yaml_to_expert: dict[str, ExpertAgent | SessionExpert | ExternalExpert] = {}
        for full_name in yaml_names:
            if full_name in seen:
                continue
            seen.add(full_name)

            if "#" not in full_name:
                print(f"  [OASIS] ⚠️ YAML expert name '{full_name}' has no '#', skipping. "
                      f"Use 'tag#temp#N' or 'tag#oasis#id' or 'name#ext#id' or 'title#session_id'.")
                continue

            # Handle #new suffix: strip only "new", keep the '#' separator
            force_new = full_name.endswith("#new")
            working_name = full_name[:-3] if force_new else full_name  # strip "new" only

            first, sid = working_name.split("#", 1)
            expert: ExpertAgent | SessionExpert | ExternalExpert
            if sid.startswith("ext#"):
                # e.g. "分析师#ext#analyst" → ExternalExpert
                ext_id = sid.split("#", 1)[1]
                if force_new:
                    ext_id = uuid.uuid4().hex[:8]
                    print(f"  [OASIS] 🆕 #new: '{full_name}' → new external session '{ext_id}'")
                cfg = ext_configs.get(full_name, {})
                if not cfg.get("api_url"):
                    print(f"  [OASIS] ⚠️ External expert '{full_name}' missing 'api_url' in YAML, skipping.")
                    continue
                config = self._lookup_by_tag(first, user_id)
                expert_name = config["name"] if config else first
                persona = config.get("persona", "") if config else ""
                expert = ExternalExpert(
                    name=expert_name,
                    ext_id=ext_id,
                    api_url=cfg["api_url"],
                    api_key=cfg.get("api_key", "") or os.getenv("OPENCLAW_API_KEY", ""),
                    model=cfg.get("model", "gpt-3.5-turbo"),
                    persona=persona,
                    timeout=bot_timeout,
                    tag=first,
                    extra_headers=cfg.get("headers"),
                )
                print(f"  [OASIS] 🌐 External expert: {expert.name} → {cfg['api_url']}")
            elif sid.startswith("temp#"):
                # e.g. "creative#temp#1" → ExpertAgent with explicit temp_id
                config = self._lookup_by_tag(first, user_id)
                expert_name = config["name"] if config else first
                persona = config.get("persona", "") if config else ""
                temp_num = sid.split("#", 1)[1]
                expert = ExpertAgent(
                    name=expert_name,
                    persona=persona,
                    temp_id=int(temp_num) if temp_num.isdigit() else None,
                    tag=first,
                )
            elif "#oasis#" in sid or sid.startswith("oasis#"):
                # e.g. "creative#oasis#ab12cd34" → SessionExpert (oasis)
                config = self._lookup_by_tag(first, user_id)
                expert_name = config["name"] if config else first
                persona = config.get("persona", "") if config else ""
                if force_new:
                    # Replace the id part with a fresh UUID
                    actual_sid = f"oasis#{uuid.uuid4().hex[:8]}"
                    print(f"  [OASIS] 🆕 #new: '{full_name}' → new session '{first}#{actual_sid}'")
                else:
                    actual_sid = sid
                cfg = ext_configs.get(full_name, {})
                expert = SessionExpert(
                    name=expert_name,
                    session_id=f"{first}#{actual_sid}",
                    user_id=user_id,
                    persona=persona,
                    bot_base_url=bot_base_url,
                    enabled_tools=bot_enabled_tools,
                    timeout=bot_timeout,
                    tag=first,
                    extra_headers=cfg.get("headers"),
                )
            else:
                # e.g. "助手#default" → SessionExpert (regular agent, no injection)
                if force_new:
                    actual_sid = uuid.uuid4().hex[:8]
                    print(f"  [OASIS] 🆕 #new: '{full_name}' → new session '{actual_sid}'")
                else:
                    actual_sid = sid
                cfg = ext_configs.get(full_name, {})
                expert = SessionExpert(
                    name=first,
                    session_id=actual_sid,
                    user_id=user_id,
                    persona="",
                    bot_base_url=bot_base_url,
                    enabled_tools=bot_enabled_tools,
                    timeout=bot_timeout,
                    extra_headers=cfg.get("headers"),
                )

            experts_list.append(expert)
            # Register YAML original name → expert immediately (handles #new correctly)
            yaml_to_expert[full_name] = expert

        self.experts = experts_list

        # Build lookup map: YAML original names first (highest priority for scheduling),
        # then register by internal name, title, tag, session_id as shortcuts
        self._expert_map: dict[str, ExpertAgent | SessionExpert | ExternalExpert] = {}
        self._expert_map.update(yaml_to_expert)
        for e in self.experts:
            self._expert_map.setdefault(e.name, e)       # "创意专家#creative#oasis#e7f3a2b1"
            self._expert_map.setdefault(e.title, e)      # "创意专家" (first-come wins)
            if e.tag:
                self._expert_map.setdefault(e.tag, e)    # "creative" (first-come wins)
            if hasattr(e, "session_id"):
                self._expert_map.setdefault(e.session_id, e)  # session_id shortcut
            if hasattr(e, "ext_id"):
                self._expert_map.setdefault(e.ext_id, e)  # ext_id shortcut

        self.summarizer = _get_summarizer()

    @staticmethod
    def _lookup_by_tag(tag: str, user_id: str) -> dict | None:
        """Find expert config by tag. Returns {"name", "persona", ...} or None."""
        for c in get_all_experts(user_id):
            if c["tag"] == tag:
                return c
        return None

    def _resolve_experts(self, names: list[str]) -> list:
        """Resolve expert references to Expert objects.

        Matching priority: full name > title > tag > session_id.
        Skip unknown names.
        """
        resolved = []
        for name in names:
            agent = self._expert_map.get(name)
            if agent:
                resolved.append(agent)
            else:
                print(f"  [OASIS] ⚠️ Schedule references unknown expert: '{name}', skipping")
        return resolved

    def cancel(self):
        """Request graceful cancellation. Takes effect before the next round."""
        self._cancelled = True

    def _check_cancelled(self):
        if self._cancelled:
            raise asyncio.CancelledError("Discussion cancelled by user")

    async def run(self):
        """Run the full discussion loop (called as a background task)."""
        self.forum.status = "discussing"
        self.forum.discussion = self._discussion
        self.forum.start_clock()

        session_count = sum(1 for e in self.experts if isinstance(e, SessionExpert))
        external_count = sum(1 for e in self.experts if isinstance(e, ExternalExpert))
        direct_count = len(self.experts) - session_count - external_count
        mode_label = "discussion" if self._discussion else "execute"
        print(
            f"[OASIS] 🏛️ Discussion started: {self.forum.topic_id} "
            f"({len(self.experts)} experts [{direct_count} direct, {session_count} session, {external_count} external], "
            f"max {self.forum.max_rounds} rounds, mode={mode_label})"
        )

        try:
            await self._run_scheduled()

            if self._discussion:
                self.forum.conclusion = await self._summarize()
            else:
                # Execute mode: just collect outputs, no LLM summary
                all_posts = await self.forum.browse()
                if all_posts:
                    self.forum.conclusion = "\n\n".join(
                        f"【{p.author}】\n{p.content}" for p in all_posts
                    )
                else:
                    self.forum.conclusion = "执行完成，无输出。"
            self.forum.log_event("conclude", detail="Discussion concluded")
            self.forum.status = "concluded"
            print(f"[OASIS] ✅ Discussion concluded: {self.forum.topic_id}")

        except asyncio.CancelledError:
            print(f"[OASIS] 🛑 Discussion cancelled: {self.forum.topic_id}")
            self.forum.status = "error"
            self.forum.conclusion = "讨论已被用户强制终止"

        except Exception as e:
            print(f"[OASIS] ❌ Discussion error: {e}")
            self.forum.status = "error"
            self.forum.conclusion = f"讨论过程中出现错误: {str(e)}"

    async def _run_scheduled(self):
        """Execute the schedule (linear or DAG)."""
        if self.schedule.is_dag:
            await self._run_dag()
            return

        steps = self.schedule.steps
        # In execute mode, early_stop is meaningless (no votes)
        can_early_stop = self._early_stop and self._discussion

        if self.schedule.repeat:
            for round_num in range(self.forum.max_rounds):
                self._check_cancelled()
                self.forum.current_round = round_num + 1
                self.forum.log_event("round", detail=f"Round {self.forum.current_round}/{self.forum.max_rounds}")
                print(f"[OASIS] 📢 Round {self.forum.current_round}/{self.forum.max_rounds}")

                for step in steps:
                    self._check_cancelled()
                    await self._execute_step(step)

                if can_early_stop and round_num >= 1 and await self._consensus_reached():
                    print(f"[OASIS] 🤝 Consensus reached at round {self.forum.current_round}")
                    break
        else:
            for step_idx, step in enumerate(steps):
                self._check_cancelled()
                self.forum.current_round = step_idx + 1
                self.forum.max_rounds = len(steps)
                self.forum.log_event("round", detail=f"Step {step_idx + 1}/{len(steps)}")
                print(f"[OASIS] 📢 Step {step_idx + 1}/{len(steps)}")

                await self._execute_step(step)

                if can_early_stop and step_idx >= 1 and await self._consensus_reached():
                    print(f"[OASIS] 🤝 Consensus reached at step {step_idx + 1}")
                    break

    async def _run_dag(self):
        """Execute DAG schedule: run steps as soon as all their dependencies complete.

        Uses asyncio tasks + events so that independent branches run in parallel,
        and a node starts immediately once all its predecessors finish.
        """
        steps = self.schedule.steps
        # Build lookup: step_id → step
        step_map: dict[str, ScheduleStep] = {}
        for s in steps:
            if s.step_id:
                step_map[s.step_id] = s

        # Event per step_id — set when that step completes
        done_events: dict[str, asyncio.Event] = {}
        for sid in step_map:
            done_events[sid] = asyncio.Event()

        total = len(step_map)
        completed_count = 0

        async def _run_step(step: ScheduleStep):
            nonlocal completed_count
            # Wait for all dependencies
            for dep_id in step.depends_on:
                if dep_id in done_events:
                    await done_events[dep_id].wait()

            self._check_cancelled()

            completed_count += 1
            self.forum.current_round = completed_count
            self.forum.max_rounds = total
            self.forum.log_event("round", detail=f"DAG step '{step.step_id}' ({completed_count}/{total})")
            print(f"[OASIS] 📢 DAG step '{step.step_id}' ({completed_count}/{total})")

            await self._execute_step(step)

            # Signal completion
            if step.step_id in done_events:
                done_events[step.step_id].set()

        # Launch all steps concurrently — each waits for its own deps
        tasks = [asyncio.create_task(_run_step(s)) for s in steps if s.step_id]

        # Also run steps without IDs sequentially at the end (backward compat)
        no_id_steps = [s for s in steps if not s.step_id]

        # Wait for all DAG tasks
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, Exception) and not isinstance(r, asyncio.CancelledError):
                    print(f"[OASIS] ❌ DAG step error: {r}")

        # Run non-DAG steps (if any) sequentially after DAG
        for step in no_id_steps:
            self._check_cancelled()
            await self._execute_step(step)

    async def _execute_step(self, step: ScheduleStep):
        """Execute a single schedule step."""
        disc = self._discussion

        if step.step_type == StepType.MANUAL:
            print(f"  [OASIS] 📝 Manual post by {step.manual_author}")
            self.forum.log_event("manual_post", agent=step.manual_author)
            await self.forum.publish(
                author=step.manual_author,
                content=step.manual_content,
                reply_to=step.manual_reply_to,
            )

        elif step.step_type == StepType.ALL:
            print(f"  [OASIS] 👥 All experts speak")
            for expert in self.experts:
                self.forum.log_event("agent_call", agent=expert.name)

            async def _tracked_participate(expert):
                try:
                    await expert.participate(self.forum, discussion=disc)
                finally:
                    self.forum.log_event("agent_done", agent=expert.name)

            await asyncio.gather(
                *[_tracked_participate(e) for e in self.experts],
                return_exceptions=True,
            )

        elif step.step_type == StepType.EXPERT:
            agents = self._resolve_experts(step.expert_names)
            if agents:
                instr = step.instructions.get(step.expert_names[0], "")
                print(f"  [OASIS] 🎤 {agents[0].name} speaks" + (f" (instruction: {instr[:40]}...)" if instr else ""))
                self.forum.log_event("agent_call", agent=agents[0].name)
                await agents[0].participate(self.forum, instruction=instr, discussion=disc)
                self.forum.log_event("agent_done", agent=agents[0].name)

        elif step.step_type == StepType.PARALLEL:
            agents = self._resolve_experts(step.expert_names)
            if agents:
                names = ", ".join(a.name for a in agents)
                print(f"  [OASIS] 🎤 Parallel: {names}")
                for agent in agents:
                    self.forum.log_event("agent_call", agent=agent.name)

                async def _run_with_instr(agent, yaml_name):
                    instr = step.instructions.get(yaml_name, "")
                    try:
                        await agent.participate(self.forum, instruction=instr, discussion=disc)
                    finally:
                        self.forum.log_event("agent_done", agent=agent.name)

                await asyncio.gather(
                    *[_run_with_instr(a, n) for a, n in zip(agents, step.expert_names)],
                    return_exceptions=True,
                )

    async def _consensus_reached(self) -> bool:
        top = await self.forum.get_top_posts(1)
        if not top:
            return False
        threshold = len(self.experts) * 0.7
        return top[0].upvotes >= threshold

    async def _summarize(self) -> str:
        top_posts = await self.forum.get_top_posts(5)
        all_posts = await self.forum.browse()

        if not top_posts:
            return "讨论未产生有效观点。"

        posts_text = "\n".join([
            f"[👍{p.upvotes} 👎{p.downvotes}] {p.author}: {p.content}"
            for p in top_posts
        ])

        if _SUMMARY_PROMPT_TPL:
            prompt = _SUMMARY_PROMPT_TPL.format(
                question=self.forum.question,
                post_count=len(all_posts),
                round_count=self.forum.current_round,
                posts_text=posts_text,
            )
        else:
            prompt = (
                f"你是一个讨论总结专家。以下是关于「{self.forum.question}」的多专家讨论结果。\n\n"
                f"共 {len(all_posts)} 条帖子，经过 {self.forum.current_round} 轮讨论。\n\n"
                f"获得最高认可的观点:\n{posts_text}\n\n"
                "请综合以上高赞观点，给出一个全面、平衡、有结论性的最终回答（300字以内）。\n"
                "要求:\n"
                "1. 清晰概括各方核心观点\n"
                "2. 指出主要共识和分歧\n"
                "3. 给出明确的结论性建议\n"
            )

        try:
            resp = await self.summarizer.ainvoke([HumanMessage(content=prompt)])
            return extract_text(resp.content)
        except Exception as e:
            return f"总结生成失败: {str(e)}"

"""
Secretary Skill Core Engine

The 3-Stage Pipeline:
  1. De-ambiguation — turn vague visions into concrete goals
  2. Vertical Splitting — break goals into milestones → atomic tasks
  3. Cron Automation — map tasks to a timeline and produce cron config
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ── Data Models ──────────────────────────────────────────────────────


@dataclass
class Goal:
    """A concrete, measurable goal locked by the de-ambiguation engine."""
    raw_text: str
    refined_statement: str
    success_criteria: list[str]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Milestone:
    """A high-level milestone contributing to a Goal."""
    id: str
    title: str
    description: str
    deadline: Optional[str] = None
    tasks: list["AtomicTask"] = field(default_factory=list)


@dataclass
class AtomicTask:
    """A 2-hour executable atomic task."""
    id: str
    description: str
    duration_minutes: int = 120
    done: bool = False


# ── Stage 1: De-ambiguation ──────────────────────────────────────────


class DeambiguationEngine:
    """
    Conversational de-ambiguation engine.

    Asks ONE thoughtful question at a time, building on previous answers.
    The user signals when the goal feels clear enough — no fixed checklist.
    """

    # Question bank: each question targets one dimension of the goal.
    # Topics are ordered by logical flow: meaning → scope → measurement → timeline → stakeholders
    QUESTION_BANK = [
        { "topic": "meaning",
          "text": "这 {goal} 对你来说具体意味着什么？是某个数字、某种安全感、还是某件想做的事情？" },
        { "topic": "scope",
          "text": "你说的 {goal}，大概是什么范围？是纯靠工资攒、还是包括投资收益或副业收入？" },
        { "topic": "measure",
          "text": "你怎么判断自己「做到了」？比如是账户余额达到那个数，还是某个场景下你希望自己能说一句「够了」？" },
        { "topic": "timeline",
          "text": "三年这个时间是怎么来的？是有一个具体的截止场景（买房、创业、跳槽），还是一个感觉上合适的时间？" },
        { "topic": "stakeholders",
          "text": "这个事情牵涉到其他人吗？比如家人、伴侣、合伙人——他们的预期和你的预期一致吗？" },
        { "topic": "risk",
          "text": "如果中途有意外（降薪、急用钱、市场波动），你能接受的底线是多少？或者说，什么情况下你会考虑调整计划？" },
    ]

    def __init__(self):
        self.answers: dict[str, str] = {}
        self.conversation: list[tuple[str, str, str]] = []  # (topic, question, answer)
        self.topics_covered: set[str] = set()
        self._current_index = 0

    def next_question(self) -> Optional[str]:
        """Return the next unanswered question, or None if all topics are covered."""
        while self._current_index < len(self.QUESTION_BANK):
            q = self.QUESTION_BANK[self._current_index]
            if q["topic"] not in self.topics_covered:
                # Fill in {goal} placeholder with user's raw text
                goal_placeholder = getattr(self, '_raw_text', '你的目标')
                return q["text"].format(goal=goal_placeholder)
            self._current_index += 1
        return None

    def record_answer(self, topic: str, question: str, answer: str):
        """Record an answer and mark the topic as covered."""
        self.answers[topic] = answer
        self.conversation.append((topic, question, answer))
        self.topics_covered.add(topic)
        self._current_index += 1

    def set_raw_text(self, raw_text: str):
        """Set the user's original goal text for use in follow-up questions."""
        self._raw_text = raw_text

    @property
    def topics_remaining(self) -> list[str]:
        """Return topics not yet discussed."""
        return [
            q["topic"]
            for q in self.QUESTION_BANK
            if q["topic"] not in self.topics_covered
        ]

    def is_goal_clear(self, user_says_clear: bool = False) -> bool:
        """
        The goal is "clear enough" when:
        1. The user explicitly says it's clear, AND
        2. At least the core 3 topics (meaning, scope, timeline) are covered.
        """
        core = {"meaning", "scope", "timeline"}
        return user_says_clear and core.issubset(self.topics_covered)

    def lock_goal(self, raw_text: str) -> Goal:
        """Synthesize everything discussed into a locked Goal."""
        # Build refined statement from conversation context
        parts = [raw_text.strip().rstrip('.')]
        if "timeline" in self.answers:
            parts.append(f"Timeline: {self.answers['timeline']}")
        if "meaning" in self.answers:
            parts.append(f"Purpose: {self.answers['meaning']}")
        refined = ". ".join(parts) + "."

        # Build success criteria from all covered topics
        criteria = []
        for topic in ["meaning", "measure", "timeline", "scope", "stakeholders", "risk"]:
            if topic in self.answers:
                criteria.append(f"[{topic}] {self.answers[topic]}")

        return Goal(
            raw_text=raw_text,
            refined_statement=refined,
            success_criteria=criteria,
        )


# ── Stage 2: Vertical Splitting ──────────────────────────────────────


class VerticalSplitter:
    """
    Takes a locked Goal and hierarchically breaks it down:
    Goal → Milestones → Atomic Tasks (2-hour executable units).
    """

    def __init__(self, goal: Goal, depth: int = 2):
        self.goal = goal
        self.depth = min(max(depth, 1), 3)  # clamp 1-3
        self.milestones: list[Milestone] = []

    def add_milestone(self, title: str, description: str,
                      deadline: Optional[str] = None) -> Milestone:
        ms = Milestone(
            id=f"ms-{len(self.milestones) + 1}",
            title=title,
            description=description,
            deadline=deadline,
        )
        self.milestones.append(ms)
        return ms

    def add_task(self, milestone_id: str, description: str,
                 duration: int = 120) -> Optional[AtomicTask]:
        for ms in self.milestones:
            if ms.id == milestone_id:
                task = AtomicTask(
                    id=f"{ms.id}-t{len(ms.tasks) + 1}",
                    description=description,
                    duration_minutes=duration,
                )
                ms.tasks.append(task)
                return task
        return None


# ── Stage 3: Cron Automation ─────────────────────────────────────────


@dataclass
class CronJob:
    """A scheduled job payload for the automation bridge."""
    skill_target: str = "Secretary Skill"
    cron_expression: str = ""
    action_type: str = "active_reminder"
    payload: dict = field(default_factory=dict)


class CronScheduler:
    """
    Maps tasks onto a timeline and formats JSON payloads
    ready for injection into an automation engine.
    """

    FREQ_MAP = {
        "daily": "0 9 * * 1-5",
        "weekly": "0 9 * * 1",
        "weekdays": "0 9 * * 1-5",
        "weekends": "0 9 * * 0,6",
    }

    def schedule(self, task: AtomicTask, freq: str = "daily",
                 goal_snapshot: str = "") -> CronJob:
        cron_expr = self.FREQ_MAP.get(freq, "0 9 * * 1-5")
        return CronJob(
            cron_expression=cron_expr,
            payload={
                "original_goal_snapshot": goal_snapshot,
                "current_task": task.description,
                "trigger_prompt": (
                    "Re-anchor the user to the grand vision, "
                    "verify if the current task is ready for today, "
                    "and listen for a `/align` call if scheduling "
                    "conflicts exist."
                ),
            },
        )

    def to_json(self, job: CronJob) -> dict:
        return {
            "skill_target": job.skill_target,
            "cron_expression": job.cron_expression,
            "action_type": job.action_type,
            "payload": job.payload,
        }

"""Main evolution loop — the heart of supervised-agentic-loop.

Combines:
  - autoresearch-style autonomous experimentation (keep/discard loop)
  - governed-agents verification gates + reputation scoring
  - self-improving-agent persistent learnings

6 phases per iteration:
  Baseline → Brainstorm → Plan → Implement → Review → Verify → Evolve
"""

import logging
import shlex
import signal
import subprocess
import time
from pathlib import Path
from typing import Optional

from sal.brainstorm import format_hypothesis_prompt, generate_hypothesis
from sal.config import EvolveConfig
from sal.contract import AgentCallable, TaskContract, TaskResult, TaskStatus
from sal.exceptions import (
    BaselineCrashError,
    IterationCrash,
    IterationHallucination,
    MetricParseError,
)
from sal.git_isolation import GitIsolation
from sal.learnings import LearningsLog
from sal.metric_extractor import extract_metric
from sal.reputation import (
    SCORE_CRASH,
    SCORE_FIRST_PASS,
    SCORE_HALLUCINATION,
    SCORE_NO_CHANGE,
    ReputationDB,
)
from sal.results_log import ResultsLog
from sal.verification import run_full_verification

# Optional monitor integration — SAL works without it
try:
    from sal.monitor import AgentMonitor, BlockDecision
    _HAS_MONITOR = True
except ImportError:
    _HAS_MONITOR = False

logger = logging.getLogger("sal.evolve")


class EvolveLoop:
    """The supervised autonomous evolution loop.

    Usage:
        config = EvolveConfig(
            target_file="train.py",
            metric_command="python train.py",
            metric_parser="val_bpb",
            minimize=True,
        )
        loop = EvolveLoop(config, agent=my_agent_callable)
        loop.run()
    """

    def __init__(
        self,
        config: EvolveConfig,
        agent: AgentCallable,
        agent_id: str = "default-agent",
        enable_monitor: bool = True,
    ) -> None:
        self.config = config
        self.agent = agent
        self.agent_id = agent_id

        # State
        self.best_metric: Optional[float] = None
        self.stagnation: int = 0
        self._interrupted: bool = False

        # Subsystems
        work = Path(config.work_dir)
        self.git = GitIsolation(work)
        self.results = ResultsLog(work / "results.tsv")
        self.reputation = ReputationDB(str(work / ".state" / "reputation.db"))
        self.learnings = LearningsLog(work / ".state" / "learnings")

        # Monitor integration (optional)
        self.monitor: Optional["AgentMonitor"] = None
        if enable_monitor and _HAS_MONITOR:
            state_dir = str(work / ".state")
            self.monitor = AgentMonitor(state_dir=state_dir)
            logger.info("Monitor enabled (sync blocking + session tracking)")

        # Register signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_sigint)

    def _handle_sigint(self, signum, frame) -> None:  # noqa: ANN001
        """Graceful SIGINT handler — stop after current iteration."""
        logger.warning("SIGINT received — stopping after current iteration")
        self._interrupted = True

    def run(self) -> dict:
        """Main loop — runs until a brake triggers.

        Returns:
            Summary dict with final stats.

        Raises:
            BaselineCrashError: If baseline measurement fails (HARD ABORT).
        """
        logger.info(
            "Starting supervised-agentic-loop run: tag=%s, max_iterations=%d",
            self.config.run_tag,
            self.config.max_iterations,
        )

        # Create experiment branch
        branch = self.git.create_branch(self.config.run_tag)
        logger.info("Created branch: %s", branch)

        # Phase 0: Baseline
        self.best_metric = self._baseline()
        stop_reason = ""

        # Main loop
        for i in range(1, self.config.max_iterations + 1):
            if self._interrupted:
                stop_reason = "SIGINT — human interrupt"
                break

            logger.info("=== Iteration %d / %d ===", i, self.config.max_iterations)

            # Hook 3: Monitor session start
            if self.monitor:
                from sal.monitor.dashboard import log_alert  # lazy import
                logger.debug("Monitor: session_start(iteration=%d)", i)

            try:
                # Phase 1: Brainstorm
                hypothesis = self._brainstorm()

                # Phase 2: Plan
                contract = self._plan(hypothesis)

                # Phase 3: Implement
                agent_output = self._implement(contract, hypothesis)

                # Phase 4: Review (lightweight — check agent claims)
                self._review(agent_output, contract)

                # Phase 5: Verify + extract metric
                metric_value = self._verify(contract)

                # Phase 6: Evolve (keep/discard decision)
                self._evolve(i, hypothesis, metric_value)

            except IterationHallucination as e:
                # Agent claimed success but gates failed — penalize
                logger.warning("HALLUCINATION in iteration %d: %s", i, e)
                self.git.rollback()
                rep = self.reputation.update(
                    self.agent_id, i, SCORE_HALLUCINATION,
                    status="crash", hypothesis=str(e),
                )
                self.results.log(
                    i, status="crash", hypothesis=str(e),
                    reputation=rep["reputation_after"],
                )
                self.learnings.log_error(i, str(e), hypothesis="hallucination")

            except IterationCrash as e:
                # Honest crash — no penalty
                logger.warning("CRASH in iteration %d: %s", i, e)
                self.git.rollback()
                rep = self.reputation.update(
                    self.agent_id, i, SCORE_CRASH,
                    status="crash", hypothesis=str(e),
                )
                self.results.log(
                    i, status="crash", error=str(e),
                    reputation=rep["reputation_after"],
                )
                self.learnings.log_error(i, str(e))
                continue

            except Exception as e:
                # Unexpected error — log and continue
                logger.error("UNEXPECTED ERROR in iteration %d: %s", i, e, exc_info=True)
                self.git.rollback()
                rep = self.reputation.update(
                    self.agent_id, i, SCORE_CRASH,
                    status="error", hypothesis=f"Unexpected: {e}",
                )
                self.results.log(
                    i, status="error", error=str(e),
                    reputation=rep["reputation_after"],
                )
                continue

            # === BRAKE CHECKS ===
            level = self.reputation.get_level(self.agent_id)
            if level["level"] == "suspended":
                stop_reason = (
                    f"SUSPENDED — reputation {level['reputation']:.3f} ≤ 0.2"
                )
                self.reputation.suspend(self.agent_id, stop_reason)
                logger.warning(stop_reason)
                break

            if self.stagnation >= self.config.plateau_patience:
                stop_reason = (
                    f"PLATEAU — no improvement for {self.stagnation} iterations"
                )
                logger.warning(stop_reason)
                break

        if not stop_reason:
            stop_reason = "Budget exhausted"

        # Summary
        summary = {
            "run_tag": self.config.run_tag,
            "stop_reason": stop_reason,
            "iterations": self.results.count,
            "best_metric": self.best_metric,
            "reputation": self.reputation.get_level(self.agent_id),
            "learnings_summary": self.learnings.get_summary(),
        }

        logger.info("Run complete: %s", summary)
        self.reputation.close()
        return summary

    def _baseline(self) -> float:
        """Phase 0: Run metric command on unmodified code.

        Raises:
            BaselineCrashError: HARD ABORT if baseline fails.
        """
        logger.info("Phase 0: Baseline measurement")
        try:
            output = self._run_metric_command()
            metric = extract_metric(output, self.config.metric_parser)
        except (MetricParseError, subprocess.CalledProcessError, OSError) as e:
            raise BaselineCrashError(
                f"Baseline failed — codebase is broken before we start.\n"
                f"Command: {self.config.metric_command}\n"
                f"Error: {e}\n\n"
                f"Fix the codebase first, then retry."
            ) from e

        sha = self.git.current_short_sha()
        self.results.log(
            iteration=0,
            commit=sha,
            metric_value=metric,
            status="keep",
            hypothesis="baseline",
            reputation=self.reputation.get_score(self.agent_id),
        )
        self.git.mark_good()
        logger.info("Baseline metric: %.6f (commit: %s)", metric, sha)
        return metric

    def _brainstorm(self) -> dict:
        """Phase 1: Generate next hypothesis."""
        logger.info("Phase 1: Brainstorm")
        patterns = self.learnings.get_patterns()
        hypothesis = generate_hypothesis(
            results_history=self.results.history,
            learnings_patterns=patterns,
            target_file=self.config.target_file,
        )
        logger.info("Hypothesis: %s (area: %s, risk: %s)",
                     hypothesis["description"], hypothesis["area"], hypothesis["risk"])
        return hypothesis

    def _plan(self, hypothesis: dict) -> TaskContract:
        """Phase 2: Create a task contract from the hypothesis."""
        logger.info("Phase 2: Plan (contract)")
        return TaskContract(
            objective=hypothesis["description"],
            acceptance_criteria=[
                f"Modify {self.config.target_file} to implement: {hypothesis['description']}",
                "Code must parse without syntax errors",
                "Metric command must still execute successfully",
            ],
            required_files=[self.config.target_file],
            run_tests=self.config.metric_command,
            constraints=[
                f"Only modify {self.config.target_file}",
                f"Do NOT modify: {', '.join(self.config.readonly_files) or 'N/A'}",
                f"Time budget: {self.config.time_budget}s",
            ],
            timeout_seconds=self.config.time_budget,
        )

    def _implement(self, contract: TaskContract, hypothesis: dict) -> str:
        """Phase 3: Call the agent to implement the hypothesis."""
        logger.info("Phase 3: Implement (agent call)")

        # Read current target file content
        target = Path(self.config.work_dir) / self.config.target_file
        target_content = target.read_text() if target.exists() else None

        # Build prompt
        prompt = format_hypothesis_prompt(
            hypothesis=hypothesis,
            target_file=self.config.target_file,
            target_content=target_content,
        )
        prompt += "\n\n" + contract.to_prompt()

        # Hook 1: Monitor SYNC prefilter — check prompt before sending
        if self.monitor:
            decision = self.monitor.check_before_execute(
                "agent_call", {"prompt_preview": prompt[:500]}
            )
            if decision == BlockDecision.BLOCK:
                # Hook 2: BLOCK → reputation penalty
                self.reputation.update(
                    self.agent_id, 0, SCORE_HALLUCINATION,
                    status="blocked", hypothesis="Monitor blocked agent call",
                )
                raise IterationCrash(
                    "Monitor BLOCKED agent call — potential misalignment detected"
                )

        # Call agent
        try:
            raw_output = self.agent(prompt)
        except Exception as e:
            raise IterationCrash(f"Agent call failed: {e}") from e

        if not raw_output or not raw_output.strip():
            raise IterationCrash("Agent returned empty output")

        # Hook 1: Monitor SYNC prefilter — check agent output
        if self.monitor:
            decision = self.monitor.check_before_execute(
                "agent_output", {"output_preview": raw_output[:1000]}
            )
            if decision == BlockDecision.BLOCK:
                self.reputation.update(
                    self.agent_id, 0, SCORE_HALLUCINATION,
                    status="blocked", hypothesis="Monitor blocked agent output",
                )
                raise IterationHallucination(
                    "Monitor BLOCKED agent output — misalignment in response"
                )

        return raw_output

    def _review(self, agent_output: str, contract: TaskContract) -> None:
        """Phase 4: Lightweight review — parse agent result."""
        logger.info("Phase 4: Review")
        result = TaskResult.from_agent_output(agent_output, contract.task_id)

        if not result.parse_success:
            raise IterationCrash(f"Agent output unparseable: {result.what_failed}")

        if result.status == TaskStatus.BLOCKED:
            raise IterationCrash(
                f"Agent blocked: {result.what_failed} — needs: {result.what_i_need}"
            )

        if result.status == TaskStatus.FAILED:
            raise IterationCrash(f"Agent reported failure: {result.what_failed}")

        # Agent claims success — proceed to verification
        if result.status == TaskStatus.SUCCESS:
            logger.info("Agent claims SUCCESS — verifying...")

    def _verify(self, contract: TaskContract) -> float:
        """Phase 5: Run verification gates + extract metric.

        Raises:
            IterationHallucination: If gates fail (agent lied).
            IterationCrash: If metric extraction fails.
        """
        logger.info("Phase 5: Verify")

        # Gate checks
        vresult = run_full_verification(
            required_files=contract.required_files,
            base_dir=self.config.work_dir,
        )

        if not vresult.passed:
            raise IterationHallucination(
                f"Verification FAILED: {vresult.summary}"
            )

        # Extract metric
        try:
            output = self._run_metric_command()
            return extract_metric(output, self.config.metric_parser)
        except MetricParseError as e:
            raise IterationCrash(f"Metric extraction failed: {e}") from e

    def _evolve(self, iteration: int, hypothesis: dict, metric_value: float) -> None:
        """Phase 6: Keep or discard based on metric comparison."""
        logger.info("Phase 6: Evolve (metric=%.6f, best=%.6f)",
                     metric_value, self.best_metric or 0.0)

        improved = self._is_improved(metric_value)
        metric_before = self.best_metric or metric_value

        if improved:
            # KEEP — commit changes
            sha = self.git.commit(
                f"sal: {hypothesis['description']} "
                f"(metric: {metric_value:.6f})"
            )
            self.git.mark_good()
            self.best_metric = metric_value
            self.stagnation = 0

            rep = self.reputation.update(
                self.agent_id, iteration, SCORE_FIRST_PASS,
                status="keep", hypothesis=hypothesis["description"],
            )
            self.results.log(
                iteration, commit=sha, metric_value=metric_value,
                status="keep", hypothesis=hypothesis["description"],
                reputation=rep["reputation_after"],
            )
            self.learnings.log_learning(
                iteration, hypothesis["description"],
                metric_before, metric_value, "keep",
                area=hypothesis["area"],
            )
            logger.info("✅ KEEP — metric improved to %.6f", metric_value)

        else:
            # DISCARD — rollback
            self.git.rollback()
            self.stagnation += 1

            rep = self.reputation.update(
                self.agent_id, iteration, SCORE_NO_CHANGE,
                status="discard", hypothesis=hypothesis["description"],
            )
            self.results.log(
                iteration, metric_value=metric_value,
                status="discard", hypothesis=hypothesis["description"],
                reputation=rep["reputation_after"],
            )
            self.learnings.log_learning(
                iteration, hypothesis["description"],
                metric_before, metric_value, "discard",
                area=hypothesis["area"],
            )
            logger.info("❌ DISCARD — no improvement (stagnation: %d/%d)",
                         self.stagnation, self.config.plateau_patience)

    def _is_improved(self, new_metric: float) -> bool:
        """Check if new metric is better than best, respecting direction."""
        if self.best_metric is None:
            return True
        if self.config.minimize:
            return new_metric < self.best_metric
        return new_metric > self.best_metric

    def _run_metric_command(self) -> str:
        """Execute the metric command and return output."""
        try:
            proc = subprocess.run(
                shlex.split(self.config.metric_command),
                shell=False,
                cwd=self.config.work_dir,
                capture_output=True,
                text=True,
                timeout=self.config.time_budget,
            )
            return proc.stdout + proc.stderr
        except subprocess.TimeoutExpired as e:
            raise IterationCrash(
                f"Metric command timed out after {self.config.time_budget}s"
            ) from e
        except OSError as e:
            raise IterationCrash(f"Metric command failed: {e}") from e

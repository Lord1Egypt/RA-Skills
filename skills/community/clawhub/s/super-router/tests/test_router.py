import contextlib
import io
import os
import threading
import unittest
from unittest import mock

import scripts.router as r


def run_quietly(func, *args, **kwargs):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result, buffer.getvalue()


class RouterHelperTests(unittest.TestCase):
    def test_initial_state_defaults_and_env_parsing(self):
        with mock.patch.dict(
            os.environ,
            {
                "ROUTER_PRO_MODEL": "",
                "ROUTER_FLASH_MODEL": "",
                "ROUTER_DEBUG": "",
                "ROUTER_FLASH_RETRY_BUDGET": "bad",
            },
            clear=False,
        ):
            state = r.create_initial_state("default check")

        self.assertEqual(state["pro_model"], r.DEFAULT_PRO_MODEL)
        self.assertEqual(state["flash_model"], r.DEFAULT_FLASH_MODEL)
        self.assertEqual(state["flash_retry_budget"], r.DEFAULT_FLASH_RETRY_BUDGET)
        self.assertFalse(r.router_debug_enabled())

        with mock.patch.dict(os.environ, {"ROUTER_DEBUG": "yes"}, clear=False):
            self.assertTrue(r.router_debug_enabled())

    def test_json_extraction_and_planner_normalization(self):
        self.assertEqual(r.extract_first_json_array("prefix [{\"desc\":\"A\"}] suffix"), [{"desc": "A"}])
        self.assertEqual(r.extract_first_json_object("noise {\"confidence\": 0.8}"), {"confidence": 0.8})
        self.assertEqual(
            r.normalize_planned_subtasks([{"step": "Inspect"}, "Summarize", {"desc": ""}]),
            [{"desc": "Inspect"}, {"desc": "Summarize"}],
        )

        with self.assertRaises(ValueError):
            r.extract_first_json_array("no json here")

    def test_communication_subtask_split_and_route_biases(self):
        task = "Debug intermittent API failure and send a concise team update."
        planned = [{"desc": "Debug intermittent API failure and send a concise team update"}]
        expanded = r.ensure_communication_subtask(task, planned)

        self.assertEqual(len(expanded), 2)
        self.assertIn("Debug intermittent API failure", expanded[0]["desc"])
        self.assertTrue(r.is_summary_like_subtask(expanded[1]["desc"]))

        summary_scores = {
            "reasoning_depth": 0,
            "code_change_scope": 0,
            "ambiguity": 0,
            "risk": 0,
            "io_heaviness": 2,
        }
        self.assertEqual(
            r.decide_route(task, "Prepare a concise team update", summary_scores, r.FLASH, 0.9),
            r.FLASH,
        )

        high_risk = r.build_fallback_assessment(
            "production billing incident",
            "Inspect payment logs and reconcile duplicate charges",
        )
        self.assertEqual(high_risk["final_route"], r.PRO)
        self.assertEqual(high_risk["scores"]["risk"], 2)

    def test_generate_text_honors_gemini_timeout(self):
        captured = []

        def fake_gemini(model, prompt, *, timeout):
            captured.append((model, prompt, timeout))
            return "ok"

        with mock.patch.object(r, "gemini_generate", side_effect=fake_gemini):
            self.assertEqual(r.generate_text("google-gemini-cli/flash", "prompt", timeout=30), "ok")

        self.assertEqual(captured, [("google-gemini-cli/flash", "prompt", 30)])

    def test_stream_event_helpers(self):
        mode, payload = r.unpack_stream_event(("namespace", "updates", {"node": {"status": "done"}}))
        self.assertEqual(mode, "updates")
        self.assertEqual(payload, {"node": {"status": "done"}})

        summary = r.summarize_stream_update(
            "dispatcher",
            {"status": "dispatched", "current_step": 1, "active_route": r.PRO},
        )
        self.assertIn("dispatcher", summary)
        self.assertIn("status=dispatched", summary)
        self.assertIn("route=PRO", summary)


class ProviderFallbackTests(unittest.TestCase):
    def test_provider_fallback_retries_infra_failure_and_succeeds(self):
        calls = []

        def fake_generate(model, prompt, **kwargs):
            calls.append(model)
            if model == "primary":
                raise RuntimeError("connection reset by provider")
            return "fallback success"

        with mock.patch.object(r, "generate_text", side_effect=fake_generate):
            result = r.invoke_with_provider_fallback(
                "primary",
                ["fallback"],
                "prompt",
                timeout=5,
                num_predict=10,
                temperature=0.0,
                label="test",
            )

        self.assertTrue(result["success"])
        self.assertEqual(result["model_name"], "fallback")
        self.assertTrue(result["used_provider_fallback"])
        self.assertEqual(calls, ["primary", "fallback"])

    def test_provider_fallback_stops_on_capability_failure(self):
        calls = []

        def fake_generate(model, prompt, **kwargs):
            calls.append(model)
            raise RuntimeError("need more context to complete")

        with mock.patch.object(r, "generate_text", side_effect=fake_generate):
            result = r.invoke_with_provider_fallback(
                "primary",
                ["fallback"],
                "prompt",
                timeout=5,
                num_predict=10,
                temperature=0.0,
                label="test",
            )

        self.assertFalse(result["success"])
        self.assertEqual(result["failure_type"], "capability_quality")
        self.assertEqual(calls, ["primary"])


class FlashReviewAndMetadataTests(unittest.TestCase):
    def test_flash_output_review_and_retry_guard(self):
        self.assertEqual(
            r.verify_flash_output("Inspect config", "", r.empty_flash_review(), 0)["decision"],
            "escalate",
        )
        self.assertEqual(
            r.verify_flash_output("Inspect config", "ok", r.empty_flash_review(), 0)["decision"],
            "escalate",
        )
        self.assertEqual(
            r.verify_flash_output("Prepare summary", "ok", r.empty_flash_review(), 0)["decision"],
            "record",
        )

        state = r.create_initial_state("retry", flash_retry_budget=1)
        state.update(
            {
                "current_step": 0,
                "active_flash_review": {
                    "decision": "retry",
                    "failure_type": "infra_transient",
                    "reason": "connection reset",
                },
                "active_attempt_log": [],
            }
        )
        retry_update = r.retry_guard_node(state)
        self.assertEqual(retry_update["status"], "flash_retrying")
        self.assertEqual(retry_update["active_retry_count"], 1)

        state.update(retry_update)
        exhausted_update = r.retry_guard_node(state)
        self.assertEqual(exhausted_update["status"], "flash_retry_exhausted")
        self.assertIn("FLASH execution failed", exhausted_update["active_output"])

    def test_metadata_extraction_uses_recorded_provider_fallback_result(self):
        state = r.create_initial_state("metadata", pro_model="pro")
        state["results"] = [
            {
                "step": 1,
                "planned_route": r.PRO,
                "route": r.PRO,
                "model_name": "pro-fallback",
                "desc": "Inspect service behavior",
                "output": "Detailed technical output from provider fallback.",
                "status": "executed_via_provider_fallback",
                "attempt_count": 1,
                "retry_count": 0,
                "escalated_from_flash": False,
                "used_provider_fallback": True,
                "flash_review": r.empty_flash_review(),
                "attempt_log": [],
            }
        ]

        def fake_invoke(*args, **kwargs):
            return {
                "success": True,
                "output": "- Extracted technical fact.",
                "model_name": "pro",
                "used_provider_fallback": False,
                "failure_type": "none",
                "error_text": "",
                "attempt_log": [],
            }

        with mock.patch.object(r, "invoke_with_provider_fallback", side_effect=fake_invoke):
            update, _ = run_quietly(r.extract_technical_metadata_node, state)

        self.assertIn("TECHNICAL METADATA STEP 1", update["history"][0])
        self.assertIn("Extracted technical fact", update["history"][0])

    def test_metadata_extraction_skips_executor_fallback_result(self):
        state = r.create_initial_state("metadata", pro_model="pro")
        state["results"] = [
            {
                "step": 1,
                "planned_route": r.PRO,
                "route": r.PRO,
                "model_name": "pro",
                "desc": "Inspect service behavior",
                "output": "PRO executor fallback output: Inspect service behavior",
                "status": "executor_fallback",
                "attempt_count": 1,
                "retry_count": 0,
                "escalated_from_flash": False,
                "used_provider_fallback": False,
                "flash_review": r.empty_flash_review(),
                "attempt_log": [],
            }
        ]

        with mock.patch.object(r, "invoke_with_provider_fallback") as invoke_mock:
            update, _ = run_quietly(r.extract_technical_metadata_node, state)

        invoke_mock.assert_not_called()
        self.assertIn("skipped", update["history"][0])


class FinalizerTests(unittest.TestCase):
    def test_finalizer_timeout_env_is_used_for_flash_and_pro(self):
        captured = []

        def fake_invoke(primary_model, fallback_models, prompt, *, timeout, num_predict, temperature, label, attempt_log=None):
            captured.append((label, timeout))
            return {
                "success": True,
                "output": (
                    "Routing Summary\nEnough content for verification.\n"
                    "Step Outcomes\nThe timeout was captured.\n"
                    "Next Action\nKeep env override wired."
                ),
                "model_name": primary_model,
                "used_provider_fallback": False,
                "failure_type": "none",
                "error_text": "",
                "attempt_log": list(attempt_log or []),
            }

        state = r.create_initial_state("timeout", pro_model="pro", flash_model="flash")
        with mock.patch.dict(os.environ, {"ROUTER_FINALIZER_TIMEOUT": "17"}, clear=False):
            with mock.patch.object(r, "invoke_with_provider_fallback", side_effect=fake_invoke):
                r.flash_finalizer_node(state)
                r.pro_finalizer_node(state)

        self.assertEqual(captured, [("Finalizer FLASH", 17), ("Finalizer PRO", 17)])

    def test_finalizer_model_path_distinctness(self):
        state = r.create_initial_state(
            "paths",
            pro_model="google-gemini-cli/gemini-3-pro-preview",
            flash_model="google-gemini-cli/flash",
        )
        self.assertTrue(r.has_distinct_finalizer_model_path(state))

        same_state = r.create_initial_state(
            "paths",
            pro_model="google-gemini-cli/flash",
            flash_model="google-gemini-cli/flash",
        )
        self.assertFalse(r.has_distinct_finalizer_model_path(same_state))


class RouterGraphIntegrationTests(unittest.TestCase):
    def fake_generate_success(self, model, prompt, **kwargs):
        if prompt == r.WARMUP_PROMPT:
            return "OK"
        if "Task Decomposer" in prompt or "Role: Expert task decomposer" in prompt:
            return '[{"desc":"Inspect the router state flow"},{"desc":"Prepare a concise summary"}]'
        if "Role: Complexity judge" in prompt:
            if "Prepare a concise summary" in prompt:
                return (
                    '{"scores":{"reasoning_depth":0,"code_change_scope":0,"ambiguity":0,'
                    '"risk":0,"io_heaviness":2},"suggested_route":"FLASH",'
                    '"confidence":0.9,"reason":"summary"}'
                )
            return (
                '{"scores":{"reasoning_depth":2,"code_change_scope":1,"ambiguity":1,'
                '"risk":0,"io_heaviness":0},"suggested_route":"PRO",'
                '"confidence":0.9,"reason":"inspection"}'
            )
        if "Extract the 'technical gold'" in prompt:
            return "- Verified metadata extraction used the recorded step output."
        if "task executor" in prompt:
            return "This step completed with concrete technical findings and enough detail for verification."
        if "summarizer" in prompt:
            self.assertIn("TECHNICAL METADATA STEP", prompt)
            return (
                "Routing Summary\nThe mocked run completed using metadata.\n"
                "Step Outcomes\nBoth steps produced usable output and metadata was included.\n"
                "Next Action\nReview state transitions and finalizer context."
            )
        return "Fallback mocked output with sufficient detail."

    def test_full_graph_success_path_with_metadata_and_no_debug_output(self):
        with mock.patch.dict(os.environ, {"ROUTER_DEBUG": ""}, clear=False):
            with mock.patch.object(r, "generate_text", side_effect=self.fake_generate_success):
                state, output = run_quietly(
                    r.run_router_app,
                    "Inspect router state flow and summarize",
                    planner_model="mock-planner",
                    judge_model="mock-judge",
                    pro_model="mock-pro",
                    flash_model="mock-flash",
                    max_concurrency=1,
                )

        metadata_blocks = [line for line in state["history"] if "TECHNICAL METADATA STEP" in line]
        self.assertEqual(state["status"], "finished")
        self.assertEqual(len(state["results"]), 2)
        self.assertEqual(len(metadata_blocks), 2)
        self.assertNotIn("[DEBUG", output)

    def test_full_graph_flash_quality_escalates_to_pro(self):
        calls = {"flash_executor": 0, "pro_executor": 0}

        def fake_generate(model, prompt, **kwargs):
            if prompt == r.WARMUP_PROMPT:
                return "OK"
            if "Task Decomposer" in prompt or "Role: Expert task decomposer" in prompt:
                return '[{"desc":"List deployment manifests"}]'
            if "Role: Complexity judge" in prompt:
                return (
                    '{"scores":{"reasoning_depth":0,"code_change_scope":0,"ambiguity":0,'
                    '"risk":0,"io_heaviness":2},"suggested_route":"FLASH",'
                    '"confidence":0.95,"reason":"mostly listing"}'
                )
            if "Role: FLASH task executor" in prompt:
                calls["flash_executor"] += 1
                return "ok"
            if "Role: PRO task executor" in prompt:
                calls["pro_executor"] += 1
                self.assertIn("Escalation context", prompt)
                return "PRO completed the manifest listing with enough detail after FLASH quality escalation."
            if "Extract the 'technical gold'" in prompt:
                return "- Escalated manifest listing produced a detailed result."
            if "summarizer" in prompt:
                return (
                    "Routing Summary\nFLASH escalated to PRO after quality review.\n"
                    "Step Outcomes\nThe manifest listing completed successfully.\n"
                    "Next Action\nUse the PRO result."
                )
            return "Fallback mocked output with sufficient detail."

        with mock.patch.object(r, "generate_text", side_effect=fake_generate):
            state, _ = run_quietly(
                r.run_router_app,
                "List deployment manifests",
                planner_model="mock-planner",
                judge_model="mock-judge",
                pro_model="mock-pro",
                flash_model="mock-flash",
                max_concurrency=1,
            )

        self.assertEqual(state["status"], "finished")
        self.assertEqual(len(state["results"]), 1)
        result = state["results"][0]
        self.assertEqual(result["planned_route"], r.FLASH)
        self.assertEqual(result["route"], r.PRO)
        self.assertTrue(result["escalated_from_flash"])
        self.assertEqual(calls, {"flash_executor": 1, "pro_executor": 1})

    def test_executor_subtasks_run_in_parallel_when_concurrency_allows(self):
        barrier = threading.Barrier(2, timeout=3)
        broken_barrier = []
        executor_threads = []

        def fake_generate(model, prompt, **kwargs):
            if prompt == r.WARMUP_PROMPT:
                return "OK"
            if "Task Decomposer" in prompt:
                return (
                    '[{"desc":"Analyze provider A architecture"},'
                    '{"desc":"Analyze provider B architecture"}]'
                )
            if "Role: Complexity judge" in prompt:
                return (
                    '{"scores":{"reasoning_depth":2,"code_change_scope":0,"ambiguity":1,'
                    '"risk":0,"io_heaviness":0},"suggested_route":"PRO",'
                    '"confidence":0.9,"reason":"parallel analysis"}'
                )
            if "task executor" in prompt:
                executor_threads.append(threading.get_ident())
                try:
                    barrier.wait()
                except threading.BrokenBarrierError:
                    broken_barrier.append("executor branches did not overlap")
                return "Parallel executor completed with detailed technical analysis and enough verification detail."
            if "Extract the 'technical gold'" in prompt:
                return "- Parallel branch metadata was extracted."
            if "summarizer" in prompt:
                return (
                    "Routing Summary\nParallel executor fanout completed.\n"
                    "Step Outcomes\nBoth provider analyses returned usable results.\n"
                    "Next Action\nUse the joined result set."
                )
            return "Fallback mocked output with sufficient detail."

        with mock.patch.object(r, "generate_text", side_effect=fake_generate):
            state, _ = run_quietly(
                r.run_router_app,
                "Analyze provider A and provider B independently",
                planner_model="mock-planner",
                judge_model="mock-judge",
                pro_model="mock-pro",
                flash_model="mock-flash",
                max_concurrency=2,
            )

        self.assertEqual(state["status"], "finished")
        self.assertEqual(len(state["results"]), 2)
        self.assertEqual([result["step"] for result in state["results"]], [1, 2])
        self.assertFalse(broken_barrier)
        self.assertEqual(len(set(executor_threads)), 2)

    def test_streamed_graph_returns_final_state(self):
        with mock.patch.object(r, "generate_text", side_effect=self.fake_generate_success):
            state, _ = run_quietly(
                r.run_router_app,
                "Inspect router state flow and summarize",
                planner_model="mock-planner",
                judge_model="mock-judge",
                pro_model="mock-pro",
                flash_model="mock-flash",
                max_concurrency=1,
                stream=True,
            )

        self.assertEqual(state["status"], "finished")
        self.assertEqual(len(state["results"]), 2)


if __name__ == "__main__":
    unittest.main()

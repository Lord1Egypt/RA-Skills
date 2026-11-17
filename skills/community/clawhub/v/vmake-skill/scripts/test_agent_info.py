"""Offline contract tests: no credentials, uploads or paid API calls."""
import ast
import json
import os
from pathlib import Path
import shlex
import types
import unittest
from unittest.mock import patch

from agent_info import resolve_agent_info, agent_headers
import vmake_ai


class AgentInfoTests(unittest.TestCase):
    def test_wapi_endpoint_is_fixed(self):
        self.assertEqual(vmake_ai.skill_config.WAPI_ENDPOINT, "wapi-skill.vmake.ai")

    def test_optional_precedence_and_validation(self):
        with patch.dict(os.environ, {"SKILL_AGENT_NAME": "OpenClaw", "SKILL_AGENT_MODEL": "env-model"}, clear=True):
            self.assertEqual(resolve_agent_info()["name"], "openclaw")
            self.assertEqual(resolve_agent_info(" Codex ", " V1 ", "GPT-X"), {"name": "codex", "version": "V1", "model": "GPT-X"})
            self.assertEqual(resolve_agent_info(model="")["model"], "")
            for bad in ("bad\nname", "\tbad", "a" * 65, "模型", "\ud800"):
                self.assertEqual(resolve_agent_info(name=bad)["name"], "")
            self.assertEqual(resolve_agent_info(version="v" * 129, model="m" * 257)["version"], "")
            self.assertEqual(resolve_agent_info(model="m" * 257)["model"], "")
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(agent_headers(resolve_agent_info()), {})

    def test_worker_preserves_caller_and_shell_quoting(self):
        with patch.dict(os.environ, {"SKILL_AGENT_NAME": "Codex", "SKILL_AGENT_MODEL": "model'$(touch no)"}, clear=True):
            info = resolve_agent_info()
            command = vmake_ai._run_task_command_shell("videoscreenclear", "/tmp/my video.mp4", "", info)
            argv = shlex.split(command)
            self.assertEqual(argv[argv.index("--agent-name") + 1], "codex")
            self.assertEqual(argv[argv.index("--agent-model") + 1], info["model"])
            self.assertEqual(argv[argv.index("--agent-version") + 1], "")
            payload = vmake_ai.build_spawn_run_task("videoscreenclear", "/tmp/my video.mp4", "", None, None, 3600)
            self.assertIn(command, json.dumps(payload, ensure_ascii=False).replace('\\"', '"'))

    def test_worker_preserves_profile_override(self):
        profile = '{"media_profiles":{"media_data_type":"url"}}'
        payload = vmake_ai.build_spawn_run_task(
            "videoscreenclear",
            "/tmp/my video.mp4",
            "",
            None,
            None,
            3600,
            profile_json=profile,
        )
        argv = shlex.split(payload["command"])
        self.assertEqual(argv[argv.index("--profile") + 1], profile)

    def test_wapi_headers_are_present_before_signing(self):
        # Execute the real WapiClient class with offline transport/signing boundaries.
        source = Path(__file__).with_name("client.py").read_text()
        tree = ast.parse(source)
        node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "WapiClient")
        observed = {}
        class Signer:
            def __init__(self, *args): pass
            def sign(self, uri, method, headers, body):
                observed["uri"] = uri
                observed.update(headers)
                return object()
        response = types.SimpleNamespace(status_code=200, content=json.dumps({"meta": {"code": 0}, "response": {"context": "ok"}}).encode())
        session = types.SimpleNamespace(send=lambda *args, **kwargs: response)
        env = dict(resolve_agent_info=resolve_agent_info, agent_headers=agent_headers,
                   app_config=vmake_ai.skill_config, sign=types.SimpleNamespace(Signer=Signer),
                   requests=types.SimpleNamespace(Session=lambda: session), json=json,
                   _wapi_meta_code_value=int, WapiApiError=RuntimeError)
        exec(compile(ast.Module(body=[node], type_ignores=[]), "client.py", "exec"), env)
        with patch.dict(os.environ, {}, clear=True):
            client = env["WapiClient"]("test-ak", "test-sk", agent_name="Codex", agent_model="GPT-X")
            self.assertEqual(client.request("/skill/consume.json", method="POST", body={"task": "test"}), {"context": "ok"})
        self.assertEqual(observed["X-Agent-Name"], "codex")
        self.assertEqual(observed["X-Agent-Model"], "GPT-X")
        self.assertNotIn("X-Agent-Version", observed)
        self.assertEqual(observed["uri"], "https://wapi-skill.vmake.ai/skill/consume.json")


if __name__ == "__main__":
    unittest.main()

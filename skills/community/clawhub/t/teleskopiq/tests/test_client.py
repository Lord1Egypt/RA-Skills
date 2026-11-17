import argparse
import importlib.util
import io
import json
import os
import sys
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
spec = importlib.util.spec_from_file_location("client", Path(__file__).parents[1] / "scripts/teleskopiq.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)
KEY = "tsk_UC_channel_with_underscores_" + "a" * 64


def response(jobs=None, payload=None, status=200, lines=None):
    result = Mock()
    result.__enter__ = Mock(return_value=result)
    result.__exit__ = Mock(return_value=False)
    result.ok = status < 400
    result.status_code = status
    result.headers = {"Content-Type": "text/event-stream" if jobs is not None or lines is not None else "application/json"}
    result.json.return_value = payload
    frames = []
    for field, job in jobs or []:
        frames.extend(["event: next", "data: " + json.dumps({"data": {field: job}}), ""])
    result.iter_lines.return_value = iter(lines if lines is not None else frames)
    return result


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = cli.Client(KEY)
        self.client.session = Mock()

    def test_key_channel_can_contain_underscores(self):
        self.assertEqual(self.client.channel_id, "UC_channel_with_underscores")

    def test_stray_paste_character_is_rejected_before_a_request(self):
        with self.assertRaisesRegex(cli.APIError, "extra pasted characters"):
            cli.Client("V" + KEY)

    def test_env_file_is_data_and_does_not_override_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "env"
            path.write_text("export TELESKOPIQ_API_KEY='saved'\ntouch /should-not-run\n")
            with patch.dict(os.environ, {"TELESKOPIQ_ENV_FILE": str(path), "TELESKOPIQ_API_KEY": "existing"}, clear=True):
                cli.load_credentials()
                self.assertEqual(os.environ["TELESKOPIQ_API_KEY"], "existing")
            with patch.dict(os.environ, {"TELESKOPIQ_ENV_FILE": str(path)}, clear=True):
                cli.load_credentials()
                self.assertEqual(os.environ["TELESKOPIQ_API_KEY"], "saved")

    def test_remote_http_is_rejected(self):
        with self.assertRaises(cli.APIError):
            cli.Client(KEY, "http://example.com/api/graphql")

    def test_failed_mutation_is_not_retried(self):
        self.client.session.post.return_value = response(payload={"data": {"updateScript": {"success": False}}})
        with self.assertRaisesRegex(cli.APIError, "success=false"):
            self.client.op("update", {"input": {"id": "s"}})
        self.assertEqual(self.client.session.post.call_count, 1)
        self.assertFalse(self.client.session.post.call_args.kwargs["allow_redirects"])

    def test_errors_are_redacted(self):
        self.client.session.post.return_value = response(payload={"errors": [{"message": KEY}]}, status=400)
        with self.assertRaises(cli.APIError) as caught:
            self.client.op("scripts")
        self.assertNotIn(KEY, str(caught.exception))

    def test_sse_heartbeats_multiline_and_unicode(self):
        r = response(lines=[": heartbeat", "", "event:next", 'data:{"data":',
                            'data: {"chatJob":{"type":"complete","reply":"你好"}}}', ""])
        self.client.session.post.return_value = r
        terminal = self.client.terminal("chat", "chatJob", {})
        self.assertEqual(terminal["reply"], "你好")

    def test_stream_errors_never_look_like_completion(self):
        for r in [response(payload={"errors": [{"message": "Bad argument"}]}, status=400),
                  response(lines=['data: {"errors": [{"message": "Rejected"}]}', ""]),
                  response(jobs=[("chatJob", {"type": "error", "error": "Generation failed"})]),
                  response(jobs=[("chatJob", {"type": "script", "text": "partial"})]),
                  response(lines=["event: complete", ""]),
                  response(lines=["data: invalid-json", ""])]:
            self.client.session.post.return_value = r
            with self.assertRaises(cli.APIError):
                self.client.terminal("chat", "chatJob", {})

    def test_chat_uses_server_content_not_deltas(self):
        self.client.script = Mock(side_effect=[{"content": "old", "comments": []}, {"content": "# Title\nFinal patched content"}])
        self.client.op = Mock(return_value={"chatHistory": [
            {"role": "user", "content": "old message", "archivedAt": "yesterday"},
            {"role": "user", "content": "visible", "files": [{"uri": "file", "mimeType": "text/plain"}]},
        ]})
        self.client.session.post.return_value = response(jobs=[
            ("chatJob", {"type": "script", "text": "raw stream"}),
            ("chatJob", {"type": "complete", "script": "stream final", "reply": "Done"}),
        ])
        args = argparse.Namespace()
        result = self.client.chat("s", "write", args)
        self.assertEqual(result["script"]["content"], "# Title\nFinal patched content")
        self.assertEqual(self.client.op.call_count, 1)  # History read only, no duplicate content save.
        variables = self.client.session.post.call_args.kwargs["json"]["variables"]
        self.assertEqual(len(variables["history"]), 1)
        self.assertNotIn("aiMode", self.client.session.post.call_args.kwargs["json"]["query"])

    def test_question_is_resumable_and_not_complete(self):
        self.client.script = Mock(return_value={"content": "old", "comments": []})
        self.client.op = Mock(return_value={"chatHistory": []})
        self.client.terminal = Mock(return_value={"type": "question", "callId": "call", "question": "How long?", "options": ["10m"]})
        with self.assertRaises(cli.QuestionPending) as caught:
            self.client.chat("s", "write", argparse.Namespace(call_id="previous", answer="10 minutes"))
        self.assertEqual(caught.exception.result["scriptId"], "s")
        self.assertEqual(self.client.terminal.call_args.args[2]["tool"], {"callId": "previous", "answer": "10 minutes"})

    def test_metadata_waits_for_terminal_event_even_with_old_data(self):
        self.client.script = Mock(side_effect=[{"content": "script", "metadata": {"titles": ["old"]}}, {"metadata": {"titles": ["new"]}}])
        self.client.terminal = Mock(return_value={"type": "complete"})
        self.assertEqual(self.client.metadata("s")["metadata"]["titles"], ["new"])
        self.client.terminal.assert_called_once_with("metadata", "metadataJob", {"id": "s", "content": "script"})

    def test_thumbnails_send_visual_and_overlay_and_wait_for_each_slot(self):
        self.client.script = Mock(return_value={"thumbnailIdeas": [
            {"visual": "A red robot", "text": "HELLO"}, {"visual": "A blue moon", "text": ""}],
            "thumbnails": [{"url": "old"}]})
        self.client.op = Mock(side_effect=[{"generateScriptThumbnail": {"success": True, "url": "new0"}},
                                          {"generateScriptThumbnail": {"success": True, "url": "new1"}}])
        result = self.client.thumbnails("s", argparse.Namespace())
        self.assertEqual([t["url"] for t in result["thumbnails"]], ["new0", "new1"])
        self.assertEqual(self.client.op.call_args_list[0].args[1]["idea"], "A red robot\nText overlay: HELLO")

    def test_full_flow_stops_before_thumbnails_and_schedule_on_metadata_error(self):
        client = Mock()
        client.metadata.side_effect = cli.APIError("failed")
        args = cli.parser().parse_args(["full-flow", "--script-id", "s"])
        with self.assertRaises(cli.APIError):
            cli.run(client, args)
        client.thumbnails.assert_not_called()
        self.assertEqual(client.op.call_count, 1)  # Style read only.

    def test_style_failure_does_not_create_orphan_script(self):
        client = Mock()
        client.op.side_effect = cli.APIError("Denied")
        args = cli.parser().parse_args(["ai-write", "--title", "Title"])
        with self.assertRaises(cli.APIError):
            cli.run(client, args)
        client.create.assert_not_called()

    def test_schedule_uses_variables_preserves_status_and_ignores_time(self):
        client = Mock()
        args = cli.parser().parse_args(["schedule", "--script-id", 's"', "--date", "2026-10-03", "--time", "15:45"])
        with redirect_stderr(io.StringIO()) as output:
            cli.validate_args(args)
        self.assertIn("ignored", output.getvalue())
        cli.run(client, args)
        self.assertEqual(client.op.call_args.args, ("update", {"input": {"id": 's"', "scheduledFor": "2026-10-03T12:00:00.000Z"}}))

    def test_invalid_date_fails_before_remote_actions(self):
        args = cli.parser().parse_args(["full-flow", "--title", "x", "--ai-write", "--date", "2026-02-30"])
        with self.assertRaises(ValueError):
            cli.validate_args(args)

    def test_update_snapshots_content_before_edit(self):
        client = Mock()
        client.script.return_value = {"content": "old content"}
        args = cli.parser().parse_args(["update-script", "--script-id", "s", "--content", "new"])
        cli.run(client, args)
        self.assertEqual(client.op.call_args_list[0].args, ("save-version", {"id": "s", "content": "old content"}))
        self.assertEqual(client.op.call_args_list[1].args, ("update", {"input": {"id": "s", "content": "new"}}))

    def test_ai_question_exits_two_and_keeps_script_id(self):
        from contextlib import redirect_stdout
        with patch.object(cli, "load_credentials"), patch.object(cli, "Client"), patch.object(cli, "run") as run:
            run.side_effect = cli.QuestionPending({"scriptId": "existing", "status": "needs_answer"})
            with redirect_stdout(io.StringIO()) as output:
                code = cli.main(["chat", "--script-id", "existing", "--prompt", "Write"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())["scriptId"], "existing")

    def test_bad_local_input_stops_before_api_client_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pacing.json"
            path.write_text("[]")
            with patch.object(cli, "Client") as constructor, redirect_stderr(io.StringIO()):
                code = cli.main(["ai-write", "--title", "New", "--pacing-file", str(path)])
            self.assertEqual(code, 1)
            constructor.assert_not_called()


if __name__ == "__main__":
    unittest.main()

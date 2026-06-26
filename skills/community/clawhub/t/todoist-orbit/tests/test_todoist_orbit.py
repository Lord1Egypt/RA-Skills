import io
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import AsyncMock, patch

from scripts import todoist_orbit


class CommentInputTests(unittest.TestCase):
    def test_add_comment_inline_rejects_empty_text(self):
        with self.assertRaises(todoist_orbit.TodoistError):
            todoist_orbit.non_empty_text("", source="command line")

    def test_read_comment_content_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "note.txt"
            path.write_text("line 1\nline 2\n", encoding="utf-8")
            self.assertEqual(
                todoist_orbit.read_comment_content_from_file(str(path)),
                "line 1\nline 2\n",
            )

    def test_read_comment_content_from_stdin(self):
        with patch("sys.stdin", io.StringIO("hello\nworld\n")):
            self.assertEqual(todoist_orbit.read_comment_content_from_stdin(), "hello\nworld\n")


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = todoist_orbit.configure_parser()

    def test_comments_add_file_parser(self):
        args = self.parser.parse_args(["comments", "add-file", "--task-id", "123", "note.txt"])
        self.assertEqual(args.task_id, "123")
        self.assertEqual(args.file, "note.txt")
        self.assertIs(args.func, todoist_orbit.add_comment_from_file)

    def test_comments_add_stdin_parser(self):
        args = self.parser.parse_args(["comments", "add-stdin", "--project-id", "456"])
        self.assertEqual(args.project_id, "456")
        self.assertIs(args.func, todoist_orbit.add_comment_from_stdin)

    def test_comments_help_mentions_safe_commands(self):
        stdout = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(stdout):
                self.parser.parse_args(["comments", "--help"])
        help_text = stdout.getvalue()
        self.assertIn("add-file", help_text)
        self.assertIn("add-stdin", help_text)

    def test_projects_search_help_mentions_api_endpoint(self):
        stdout = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(stdout):
                self.parser.parse_args(["projects", "search", "--help"])
        self.assertIn("/projects/search", stdout.getvalue())

    def test_labels_search_help_mentions_api_endpoint(self):
        stdout = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(stdout):
                self.parser.parse_args(["labels", "search", "--help"])
        self.assertIn("/labels/search", stdout.getvalue())


class SearchEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_projects_uses_api_endpoint(self):
        args = Namespace(name="client", exact=False)
        with patch("scripts.todoist_orbit.request_json", new=AsyncMock(return_value={"results": [{"name": "Client Ops"}]})) as mock_request:
            result = await todoist_orbit.search_projects(args)
        mock_request.assert_awaited_once_with("/projects/search", params={"query": "client"})
        self.assertEqual(result, [{"name": "Client Ops"}])

    async def test_search_projects_exact_filters_api_results(self):
        args = Namespace(name="Client Ops", exact=True)
        payload = {"results": [{"name": "Client Ops"}, {"name": "Client Ops - Archive"}]}
        with patch("scripts.todoist_orbit.request_json", new=AsyncMock(return_value=payload)):
            result = await todoist_orbit.search_projects(args)
        self.assertEqual(result, [{"name": "Client Ops"}])

    async def test_search_labels_uses_api_endpoint(self):
        args = Namespace(name="waiting", exact=False)
        with patch("scripts.todoist_orbit.request_json", new=AsyncMock(return_value={"results": [{"name": "waiting-for"}]})) as mock_request:
            result = await todoist_orbit.search_labels(args)
        mock_request.assert_awaited_once_with("/labels/search", params={"query": "waiting"})
        self.assertEqual(result, [{"name": "waiting-for"}])

    async def test_search_labels_exact_filters_api_results(self):
        args = Namespace(name="waiting", exact=True)
        payload = {"results": [{"name": "waiting"}, {"name": "waiting-for"}]}
        with patch("scripts.todoist_orbit.request_json", new=AsyncMock(return_value=payload)):
            result = await todoist_orbit.search_labels(args)
        self.assertEqual(result, [{"name": "waiting"}])


if __name__ == "__main__":
    unittest.main()

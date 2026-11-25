"""Offline integration tests: real helpers/encoders, recording transports only.

Run: python3 tests/test_security.py --scratch /path/to/scratch -v
Use --root /path/to/export to test a baseline without changing the worktree.
"""
import argparse
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


options = argparse.ArgumentParser(add_help=False)
options.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
options.add_argument("--scratch", type=Path, required=True)
options.add_argument("--jq", default=shutil.which("jq"), help="Exact jq executable under test")
options.add_argument("--bash", default=shutil.which("bash"), help="Exact Bash executable under test")
OPTIONS, TEST_ARGS = options.parse_known_args()
ROOT = OPTIONS.root.resolve()

# All network-facing commands available to the helpers are recording doubles.
# jq, shell utilities and the local Node parser remain real.
TRANSPORT = r'''
import json, os, pathlib, sys
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
body = sys.stdin.read() if "@-" in args else ""
record = {"tool": name, "args": args, "stdin": body}
if "--config" in args:
    record["config"] = pathlib.Path(args[args.index("--config") + 1]).read_text()
with open(os.environ["RECORD"], "a") as f:
    f.write(json.dumps(record) + "\n")
if name == "curl":
    print(os.environ.get("RESPONSE_BODY", ""))
    print(os.environ.get("HTTP_STATUS", "202"), end="")
    sys.exit(int(os.environ.get("CURL_EXIT", "0")))
if name == "dig":
    print(os.environ.get("MX_RECORDS", "10 mx.sendgrid.net."))
elif name == "nslookup":
    print("parse.example.com mail exchanger = " + os.environ.get("MX_RECORDS", "10 mx.sendgrid.net."))
else:
    sys.exit("Unexpected network tool: " + name)
if os.environ.get("DNS_STDERR"):
    print(os.environ["DNS_STDERR"], file=sys.stderr)
sys.exit(int(os.environ.get("DNS_EXIT", "0")))
'''


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sendgrid-test-", dir=OPTIONS.scratch)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.bin = self.work / "bin"
        self.bin.mkdir()
        self.record = self.work / "transport.jsonl"
        for name in ("bash", "jq", "node", "cat", "head", "tail", "grep", "awk", "basename", "realpath"):
            executable = getattr(OPTIONS, name) if name in ("bash", "jq") else shutil.which(name)
            if not executable:
                self.fail("Required test dependency missing: " + name)
            (self.bin / name).symlink_to(executable)
        for name in ("curl", "dig", "nslookup", "host", "getent", "wget"):
            path = self.bin / name
            path.write_text("#!" + sys.executable + "\n" + TRANSPORT)
            path.chmod(0o755)
        # Do not inherit credentials, proxy configuration, shell hooks or user HOME.
        self.env = {
            "PATH": str(self.bin), "HOME": str(self.work), "TMPDIR": str(self.work),
            "LC_ALL": "C", "RECORD": str(self.record),
            "SENDGRID_API_KEY": "SG.synthetic-regression-only",
            "SENDGRID_FROM": "sender@example.com",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def run_helper(self, name, *args, input=None):
        runtime = "node" if name.endswith(".js") else "bash"
        return subprocess.run([str(self.bin / runtime), str(ROOT / "scripts" / name), *args],
                              input=input, capture_output=True, text=True, env=self.env,
                              cwd=self.work, timeout=10)

    def calls(self):
        return [json.loads(line) for line in self.record.read_text().splitlines()] if self.record.exists() else []

    def payload(self):
        calls = self.calls()
        self.assertEqual(len(calls), 1, calls)
        call = calls[0]
        self.assertEqual(call["tool"], "curl")
        args = call["args"]
        self.assertIn("https://api.sendgrid.com/v3/mail/send", args)
        self.assertIn("Authorization: Bearer SG.synthetic-regression-only",
                      call.get("config", " ".join(args)))
        self.assertIn("Content-Type: application/json", args)
        self.assertIn("POST", args)
        flag = next(flag for flag in ("--data-binary", "--data", "-d") if flag in args)
        data = args[args.index(flag) + 1]
        try:
            return json.loads(call["stdin"] if data == "@-" else data)
        except json.JSONDecodeError as error:
            self.fail("Helper emitted invalid JSON: " + str(error))

    def test_test_email_values_remain_data(self):
        recipient = 'quoted"\\\t\r\n雪@example.com'
        sender = 'sender"\\\t\r\n😀@example.com'
        subject = 'Hello" , "bcc": [{"email":"injected@example.com"}], "x":"\\\t\r\n雪'
        message = 'Line "one"\\\t\r\n雪 😀\b\f $(touch NEVER) `id`'
        self.env["SENDGRID_FROM"] = sender
        result = self.run_helper("send-test-email.sh", recipient, subject, message)
        payload = self.payload()
        self.assertEqual(payload, {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": sender}, "subject": subject,
            "content": [{"type": "text/plain", "value": message},
                        {"type": "text/html", "value": "<p>" + message.replace("\r\n", "<br>") + "</p>"}],
        })
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertFalse((self.work / "NEVER").exists())

    def test_plain_message_is_not_html_markup(self):
        result = self.run_helper("send-test-email.sh", "test@example.com", "Test", '<a href="x">Tom & Jo</a>')
        self.assertEqual(self.payload()["content"], [
            {"type": "text/plain", "value": '<a href="x">Tom & Jo</a>'},
            {"type": "text/html", "value": '<p>&lt;a href="x"&gt;Tom &amp; Jo&lt;/a&gt;</p>'},
        ])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_plain_line_endings_become_html_breaks_after_escaping(self):
        message = "<b>&one</b>\r\ntwo\nthree\rfour\n"
        result = self.run_helper("send-test-email.sh", "test@example.com", "Test", message)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.payload()["content"], [
            {"type": "text/plain", "value": message},
            {"type": "text/html", "value": "<p>&lt;b&gt;&amp;one&lt;/b&gt;<br>two<br>three<br>four<br></p>"},
        ])

    def test_html_helper_preserves_encoded_data_and_success(self):
        html = '<p title="quoted">雪 & more\\\nsecond\tline</p>'
        result = self.run_helper("send-html-email.sh", "test@example.com", 'Test "quotes"', html)
        self.assertEqual(self.payload(), {
            "personalizations": [{"to": [{"email": "test@example.com"}]}],
            "from": {"email": "sender@example.com"}, "subject": 'Test "quotes"',
            "content": [{"type": "text/html", "value": html}],
        })
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_html_file_mode_uses_portable_realpath(self):
        for name in ("report.html", "space report.htm", "-report.html"):
            path = self.work / name
            path.write_text('<p title="quoted">approved 雪</p>')
            for argument in (name, "./" + name, str(path)):
                with self.subTest(argument=argument):
                    self.record.unlink(missing_ok=True)
                    result = self.run_helper("send-html-email.sh", "test@example.com", "Test", argument)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(self.payload()["content"][0]["value"], path.read_text())

    def test_html_missing_paths_fail_before_transport(self):
        (self.work / "directory.html").mkdir()
        (self.work / "wrong.txt").write_text("synthetic non-HTML")
        (self.work / "broken.html").symlink_to(self.work / "absent.html")
        for argument in ("newsletter.html", "newsletter.htm", "NEWSLETTER.HTML", "report.Htm", "subdir/report.html",
                         "./absent.html", str(self.work / "absent.html"),
                         "../report.html", "report..html", "directory.html", "wrong.txt", "broken.html"):
            with self.subTest(argument=argument):
                self.record.unlink(missing_ok=True)
                result = self.run_helper("send-html-email.sh", "test@example.com", "Test", argument)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.calls(), [])

    def test_html_symlink_target_requires_html_suffix(self):
        # All targets are synthetic files in scratch, never real credential paths.
        for target in ("synthetic-secret.txt", "approved.htm"):
            (self.work / target).write_text("synthetic fixture")
            link = self.work / "report.html"
            link.unlink(missing_ok=True)
            link.symlink_to(self.work / target)
            self.record.unlink(missing_ok=True)
            result = self.run_helper("send-html-email.sh", "test@example.com", "Test", str(link))
            if target.endswith(".txt"):
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Resolved", result.stdout + result.stderr)
                self.assertEqual(self.calls(), [])
            else:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(self.payload()["content"][0]["value"], "synthetic fixture")

    def record_encoder(self):
        executable = str((self.bin / "jq").resolve())
        (self.bin / "jq").unlink()
        (self.bin / "jq").write_text("#!" + sys.executable + "\n" +
            "import json, os, sys\n" +
            "with open(os.environ['ENCODER_RECORD'], 'a') as f:\n" +
            "    f.write(json.dumps(sys.argv[1:]) + '\\n')\n" +
            "os.execv(" + repr(executable) + ", ['jq', *sys.argv[1:]])\n")
        (self.bin / "jq").chmod(0o755)
        self.env["ENCODER_RECORD"] = str(self.work / "encoder.jsonl")

    def test_send_payload_and_auth_stay_off_child_argv(self):
        self.record_encoder()
        self.env["SENDGRID_FROM"] = "private-sender@example.com"
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                self.record.unlink(missing_ok=True)
                result = self.run_helper(helper, "private@example.com", "private-subject", "private-body")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                call = self.calls()[0]
                self.assertIn("--data-binary", call["args"])
                self.assertEqual(call["args"][call["args"].index("--data-binary") + 1], "@-")
                self.assertEqual(call["config"], 'header = "Authorization: Bearer SG.synthetic-regression-only"\n')
                encoded_args = Path(self.env["ENCODER_RECORD"]).read_text()
                for value in ("private@example.com", "private-subject", "private-body",
                              self.env["SENDGRID_FROM"], self.env["SENDGRID_API_KEY"]):
                    self.assertNotIn(value, json.dumps(call["args"]) + encoded_args)
                self.assertEqual(self.payload()["subject"], "private-subject")
                argv = json.loads(encoded_args.splitlines()[-1])
                self.assertEqual(len(argv), 14)
                self.assertEqual(argv[0], "-n")
                fields = ("to", "from", "subject", "message" if helper == "send-test-email.sh" else "html")
                for index, field in enumerate(fields):
                    start = 1 + index * 3
                    self.assertEqual(argv[start:start + 2], ["--rawfile", field])
                    self.assertRegex(argv[start + 2], r"^/dev/fd/\d+$")
                args = call["args"].copy()
                descriptor = args.index("--config") + 1
                self.assertRegex(args[descriptor], r"^/dev/fd/\d+$")
                args[descriptor] = "<descriptor>"
                post = (["-X", "POST", "https://api.sendgrid.com/v3/mail/send"]
                        if helper == "send-test-email.sh" else
                        ["--request", "POST", "--url", "https://api.sendgrid.com/v3/mail/send"])
                header = "-H" if helper == "send-test-email.sh" else "--header"
                self.assertEqual(args, ["--disable", "-sS", "--connect-timeout", "10", "--max-time", "60",
                                        "--proto", "=https", "--noproxy", "*", "-w", r"\n%{http_code}",
                                        *post, "--config", "<descriptor>", header,
                                        "Content-Type: application/json", "--data-binary", "@-"])

    def test_large_html_file_does_not_use_process_argv_for_content(self):
        self.record_encoder()
        content = "<p>" + "synthetic-body " * 30000 + "</p>"
        path = self.work / "large.html"
        path.write_text(content)
        result = self.run_helper("send-html-email.sh", "test@example.com", "Large", str(path))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.payload()["content"][0]["value"], content)
        self.assertFalse("synthetic-body" in Path(self.env["ENCODER_RECORD"]).read_text(),
                         "Message body leaked into encoder argv")

    def test_api_key_cannot_inject_curl_config_or_headers(self):
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            for key in ('SG.bad"quote', 'SG.bad\\escape', 'SG.bad\r\nX-Injected: yes',
                        'SG.bad\nurl = "https://example.com"', 'SG.bad\tvalue', 'SG.bad value'):
                with self.subTest(helper=helper, key=repr(key)):
                    self.record.unlink(missing_ok=True)
                    self.env["SENDGRID_API_KEY"] = key
                    result = self.run_helper(helper, "test@example.com", "Test", "Body")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.calls(), [])
                    self.assertNotIn(key, result.stdout + result.stderr)

    def test_utf8_fields_survive_each_offset_near_4k(self):
        # Catch raw-slurp corruption in any field, not only the message. Long
        # synthetic addresses test encoding fidelity, not provider validation.
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            for char in ("é", "雪", "😀"):
                for offset in range(4092, 4101):
                    with self.subTest(helper=helper, char=char, offset=offset):
                        self.record.unlink(missing_ok=True)
                        value = "a" * offset + char * 3000
                        recipient = value + "@recipient.invalid"
                        sender = value + "@sender.invalid"
                        subject = value + " subject"
                        body = value + " body"
                        self.env["SENDGRID_FROM"] = sender
                        args = ("--html", body) if helper == "send-html-email.sh" else (body,)
                        result = self.run_helper(helper, recipient, subject, *args)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        content = [{"type": "text/html", "value": body}]
                        if helper == "send-test-email.sh":
                            content = [{"type": "text/plain", "value": body},
                                       {"type": "text/html", "value": "<p>" + body + "</p>"}]
                        self.assertEqual(self.payload(), {
                            "personalizations": [{"to": [{"email": recipient}]}],
                            "from": {"email": sender}, "subject": subject, "content": content,
                        })

    def test_long_single_line_utf8_html_files_preserve_bytes(self):
        self.record_encoder()
        for char in ("é", "雪", "😀"):
            for offset in range(4092, 4101):
                with self.subTest(char=char, offset=offset):
                    self.record.unlink(missing_ok=True)
                    # Larger than Linux's per-argument limit; input stays in a file.
                    content = "<p>" + "a" * (offset - 3) + char * 150000 + "</p>"
                    path = self.work / "unicode.html"
                    path.write_text(content, encoding="utf-8")
                    result = self.run_helper("send-html-email.sh", "test@example.com", "Unicode", "--file", str(path))
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(self.payload()["content"][0]["value"].encode("utf-8"), path.read_bytes())
        encoder_args = Path(self.env["ENCODER_RECORD"]).read_text()
        self.assertNotIn("aaaa", encoder_args)
        self.assertNotIn("--arg", encoder_args)

    def test_encoder_failure_is_reported_before_transport(self):
        (self.bin / "jq").unlink()
        (self.bin / "jq").write_text("#!/bin/bash\nprintf '{partial'\nexit 42\n")
        (self.bin / "jq").chmod(0o755)
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                result = self.run_helper(helper, "test@example.com", "Test", "Body")
                self.assertEqual(result.returncode, 42)
                self.assertEqual(self.calls(), [])
                self.assertIn("JSON encoding failed", result.stderr)
                self.assertNotIn("Success!", result.stdout)

    def test_unrelated_stdin_is_not_part_of_payload(self):
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                self.record.unlink(missing_ok=True)
                result = self.run_helper(helper, "test@example.com", "Test", "Body",
                                         input="unrelated\0stdin\né雪😀")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.payload()["content"][0]["value"], "Body")

    def test_encoder_descriptor_read_failure_stops_transport(self):
        # Execute the selected real jq with an unavailable descriptor. This tests
        # real encoder I/O failure separately from the partial-output exit stub.
        executable = str((self.bin / "jq").resolve())
        (self.bin / "jq").unlink()
        (self.bin / "jq").write_text("#!" + sys.executable + "\n" +
            "import os, sys\n" +
            "args = sys.argv[1:]\n" +
            "args[args.index('--rawfile') + 2] = '/dev/fd/9999'\n" +
            "os.execv(" + repr(executable) + ", ['jq', *args])\n")
        (self.bin / "jq").chmod(0o755)
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                result = self.run_helper(helper, "test@example.com", "Test", "Body")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.calls(), [])
                self.assertIn("JSON encoding failed", result.stderr)
                self.assertNotIn("Success!", result.stdout)

    def test_send_transport_is_bounded_and_does_not_follow_redirects_or_proxies(self):
        self.env.update(HTTPS_PROXY="http://proxy.invalid", ALL_PROXY="socks5://proxy.invalid")
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                self.record.unlink(missing_ok=True)
                self.env["HTTP_STATUS"] = "302"
                result = self.run_helper(helper, "test@example.com", "Test", "Body")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(len(self.calls()), 1)
                args = self.calls()[0]["args"]
                self.assertEqual(args[0], "--disable")
                for flag, value in (("--proto", "=https"), ("--noproxy", "*"),
                                    ("--connect-timeout", "10"), ("--max-time", "60")):
                    self.assertIn(flag, args)
                    self.assertEqual(args[args.index(flag) + 1], value)
                self.assertIn("-sS", args)
                for flag in ("--location", "-L", "--retry", "--insecure", "-k"):
                    self.assertNotIn(flag, args)

    def test_send_transport_failure_preserves_status_and_unknown_delivery(self):
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            for code in (7, 28, 35, 52, 56):
                with self.subTest(helper=helper, code=code):
                    self.record.unlink(missing_ok=True)
                    self.env["CURL_EXIT"] = str(code)
                    result = self.run_helper(helper, "test@example.com", "Test", "Body")
                    self.assertEqual(result.returncode, code)
                    self.assertIn("request to SendGrid failed", result.stderr)
                    self.assertIn("delivery status is unknown", result.stderr)
                    self.assertIn("Do not retry automatically", result.stderr)
                    self.assertNotIn("Success!", result.stdout)
                    self.assertEqual(len(self.calls()), 1)

    def test_html_explicit_modes_disambiguate_inline_and_file(self):
        (self.work / "newsletter.html").write_text("file contents")
        for args, expected in [
            (("--file", "newsletter.html"), "file contents"),
            (("--html", "newsletter.html"), "newsletter.html"),
            (("--html", "NEWSLETTER.HTML"), "NEWSLETTER.HTML"),
            (("--html", "report.Htm"), "report.Htm"),
            (("newsletter.txt",), "newsletter.txt"),
            (("Ordinary prose",), "Ordinary prose"),
            (("<p>See report</p> NEWSLETTER.HTML",), "<p>See report</p> NEWSLETTER.HTML"),
            (("--html", "--dry-run"), "--dry-run"),
            (("<p>See report</p> newsletter.html",), "<p>See report</p> newsletter.html"),
            (("--html", "./newsletter.html"), "./newsletter.html"),
        ]:
            with self.subTest(args=args):
                self.record.unlink(missing_ok=True)
                result = self.run_helper("send-html-email.sh", "test@example.com", "Test", *args)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(self.payload()["content"][0]["value"], expected)
        for args in (("--file", "missing.html"), ("--html", ""), ("--file",),
                     ("--dry-run",), ("--unknown",),
                     ("--unknown", "value"), ("inline", "extra")):
            with self.subTest(args=args):
                self.record.unlink(missing_ok=True)
                result = self.run_helper("send-html-email.sh", "test@example.com", "Test", *args)
                self.assertEqual(self.calls(), [])
                self.assertNotEqual(result.returncode, 0)

    def test_webhook_arguments_are_rejected_before_any_network(self):
        # This is argument rejection, not URL or DNS classification.
        for url in ("https://example.com/webhook", ""):
            with self.subTest(url=url):
                self.record.unlink(missing_ok=True)
                result = self.run_helper("verify-inbound-setup.sh", "parse.example.com", url)
                self.assertEqual(self.calls(), [], "Rejected URL must not cause DNS or HTTP calls")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("disabled", result.stdout + result.stderr)

    def test_mx_check_uses_only_dns_and_does_not_claim_webhook_tested(self):
        result = self.run_helper("verify-inbound-setup.sh", "parse.example.com")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(self.calls(), [{"tool": "dig", "args": ["+short", "MX", "parse.example.com"], "stdin": ""}])
        self.assertIn("Webhook accessibility and authentication were not tested", result.stdout)

    def test_inbound_next_step_targets_the_parse_hostname_after_approval(self):
        result = self.run_helper("verify-inbound-setup.sh", "parse.example.com")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Only after recipient/content approval", result.stdout)
        self.assertIn("anything@parse.example.com", result.stdout)
        self.assertEqual([call["tool"] for call in self.calls()], ["dig"])

    def test_mx_fallback_and_failure(self):
        (self.bin / "dig").unlink()
        result = self.run_helper("verify-inbound-setup.sh", "parse.example.com")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(self.calls(), [{"tool": "nslookup", "args": ["-type=MX", "parse.example.com"], "stdin": ""}])
        self.record.unlink()
        self.env["MX_RECORDS"] = "10 other.example."
        result = self.run_helper("verify-inbound-setup.sh", "parse.example.com")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call["tool"] for call in self.calls()], ["nslookup"])

    def test_mx_exchange_must_match_exactly_for_both_resolvers(self):
        cases = [("10 mx.sendgrid.net.", True), ("5 MX.SENDGRID.NET", True),
                 ("10 mx.sendgrid.net.evil.example.", False), ("10 mxxsendgrid.net.", False),
                 ("10 prefix.mx.sendgrid.net.", False), ("10 mx.sendgrid.net..", False),
                 ("mx.sendgrid.net", False), ("bad mx.sendgrid.net.", False),
                 ("10 other.example. mx.sendgrid.net.", False), ("", False),
                 (";; connection timed out; no servers could be reached", False)]
        for resolver in ("dig", "nslookup"):
            if resolver == "nslookup":
                (self.bin / "dig").unlink()
            for records, expected in cases:
                with self.subTest(resolver=resolver, records=records):
                    self.record.unlink(missing_ok=True)
                    self.env["MX_RECORDS"] = records
                    result = self.run_helper("verify-inbound-setup.sh", "parse.example.com")
                    self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)
                    self.assertEqual([call["tool"] for call in self.calls()], [resolver])
                    if not expected:
                        self.assertNotIn("MX record configured correctly", result.stdout)

    def test_mx_lookup_failure_is_not_reported_as_records(self):
        for resolver in ("dig", "nslookup"):
            if resolver == "nslookup":
                (self.bin / "dig").unlink()
            self.env.update(DNS_EXIT="9", MX_RECORDS="10 mx.sendgrid.net.", DNS_STDERR="synthetic timeout")
            self.record.unlink(missing_ok=True)
            result = self.run_helper("verify-inbound-setup.sh", "parse.example.com")
            self.assertEqual(result.returncode, 9)
            self.assertIn("DNS lookup failed", result.stderr)
            self.assertNotIn("MX records found", result.stdout)
            self.assertEqual([call["tool"] for call in self.calls()], [resolver])

    def test_helpers_disclose_live_sends_and_parser_trust_boundary(self):
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                result = self.run_helper(helper, "--help")
                self.assertEqual(result.returncode, 0)
                self.assertIn("LIVE SEND", result.stdout)
                self.assertIn("approve", result.stdout.lower())
                self.assertIn("Mail Send", result.stdout)
                self.assertEqual(self.calls(), [])
        result = self.run_helper("parse-webhook-payload.js", "--help")
        self.assertIn("untrusted", result.stdout.lower())
        self.assertIn("trusted HTTPS", result.stdout)
        self.assertEqual(self.calls(), [])

    def test_json_structure_cannot_add_recipients(self):
        recipient = 'test@example.com"}], "bcc":[{"email":"extra@example.com'
        result = self.run_helper("send-test-email.sh", recipient)
        self.assertEqual(self.payload()["personalizations"], [{"to": [{"email": recipient}]}])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_encoder_fails_without_transport(self):
        (self.bin / "jq").unlink()
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            with self.subTest(helper=helper):
                result = self.run_helper(helper, "test@example.com", "Test", "Body")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.calls(), [])

    def test_send_http_failures_and_transport_failure(self):
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            for status in ("400", "401", "403", "429", "500"):
                with self.subTest(helper=helper, status=status):
                    if self.record.exists():
                        self.record.unlink()
                    self.env.update(HTTP_STATUS=status, RESPONSE_BODY='{"errors":[{"message":"synthetic failure"}]}')
                    result = self.run_helper(helper, "test@example.com", "Test", "Body")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("HTTP " + status, result.stdout)
                    self.assertIn("synthetic failure", result.stdout)
                    self.assertEqual(self.payload()["subject"], "Test")
                    self.assertNotIn(self.env["SENDGRID_API_KEY"], result.stdout + result.stderr)
            self.record.unlink()
            self.env["CURL_EXIT"] = "7"
            result = self.run_helper(helper, "test@example.com", "Test", "Body")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Success!", result.stdout)
            self.env.pop("CURL_EXIT")

    def test_parser_treats_code_like_payload_as_data(self):
        code = 'require("fs").writeFileSync("NEVER", "executed"); $(touch NEVER)'
        # A normal multipart body. This simple diagnostic parser is lossy for the
        # closing part; the first part suffices to exercise the code/data boundary.
        fixture = ('--fixture\r\nContent-Disposition: form-data; name="text"\r\n\r\n' + code +
                   '\r\n--fixture\r\nContent-Disposition: form-data; name="subject"\r\n\r\nTest\r\n--fixture--\r\n')
        result = self.run_helper("parse-webhook-payload.js", input=fixture)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["text"], code)
        self.assertFalse((self.work / "NEVER").exists())
        self.assertEqual(self.calls(), [])

    def run_curl_examples(self, relative):
        document = (ROOT / relative).read_text()
        blocks = [block for block in re.findall(r"```bash\n(.*?)```", document, re.S)
                  if "curl " in block]
        self.assertTrue(blocks, "Expected executable curl examples in " + relative)
        for block in blocks:
            if self.record.exists():
                self.record.unlink()
            result = subprocess.run([str(self.bin / "bash"), "-c", block], env=self.env,
                                    cwd=self.work, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            yield self.calls()

    def test_webhook_example_keeps_text_fields_literal(self):
        # The attachment is synthetic; only curl is replaced. Execute the actual
        # documentation block, asserting argv at the external transport boundary.
        (self.work / "hello.txt").write_text("synthetic attachment")
        for calls in self.run_curl_examples("sendgrid-inbound/references/webhook-examples.md"):
            self.assertEqual(calls, [{"tool": "curl", "stdin": "", "args": [
                "-X", "POST", "https://your-domain.com/inbound",
                "--form-string", "from=alice@example.com",
                "--form-string", "to=support@parse.example.com",
                "--form-string", "subject=Hello",
                "--form-string", "text=Plain text body",
                "--form-string", "html=<p>HTML body</p>",
                "-F", "attachment1=@./hello.txt",
            ]}])

    def test_standalone_mail_examples_send_only_documented_data(self):
        examples = {
            "send-email/references/installation.md": [{
                "personalizations": [{"to": [{"email": "test@example.com"}]}],
                "from": {"email": "support@example.com"}, "subject": "Hello",
                "content": [{"type": "text/plain", "value": "Hi"}],
            }],
            "send-email/references/single-email-examples.md": [{
                "personalizations": [{"to": [{"email": "test@example.com"}],
                                      "cc": [{"email": "cc@example.com"}],
                                      "bcc": [{"email": "bcc@example.com"}]}],
                "from": {"email": "support@example.com"},
                "reply_to": {"email": "support@example.com"}, "subject": "SendGrid test",
                "content": [{"type": "text/plain", "value": "Plain text body"},
                            {"type": "text/html", "value": "<p>HTML body</p>"}],
                "attachments": [{"content": "aGVsbG8=", "type": "text/plain",
                                 "filename": "hello.txt", "disposition": "attachment"}],
            }, {
                "from": {"email": "support@example.com"},
                "personalizations": [{"to": [{"email": "test@example.com"}],
                                      "dynamic_template_data": {"first_name": "Vince"}}],
                "template_id": "d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            }],
        }
        for relative, expected in examples.items():
            # Run copied documentation alone: no root helper/sibling dependency.
            document = self.work / "selected-skill" / relative
            document.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, document)
            calls = list(self.run_curl_examples(str(document)))
            self.assertEqual(len(calls), len(expected))
            for actual, payload in zip(calls, expected):
                self.assertEqual(len(actual), 1)
                self.assertEqual(actual[0]["tool"], "curl")
                args = actual[0]["args"]
                self.assertEqual(args[0], "--disable")
                self.assertIn("https://api.sendgrid.com/v3/mail/send", args)
                self.assertIn("POST", args)
                self.assertIn("Content-Type: application/json", args)
                self.assertIn("--data-binary", args)
                self.assertEqual(args[args.index("--data-binary") + 1], "@-")
                self.assertNotIn(self.env["SENDGRID_API_KEY"], json.dumps(args))
                self.assertEqual(actual[0]["config"], 'header = "Authorization: Bearer SG.synthetic-regression-only"\n')
                self.assertEqual(json.loads(actual[0]["stdin"]), payload)

    def test_standalone_mail_examples_reject_keys_and_report_transport_failure(self):
        for relative in ("send-email/references/installation.md", "send-email/references/single-email-examples.md"):
            blocks = [block for block in re.findall(r"```bash\n(.*?)```", (ROOT / relative).read_text(), re.S)
                      if "curl " in block]
            self.assertTrue(blocks)
            for block in blocks:
                for key, code, status in [('SG.bad\nX-Test: yes', "0", "202"),
                                          ('SG.synthetic-regression-only', "28", "202"),
                                          ('SG.synthetic-regression-only', "0", "302")]:
                    with self.subTest(relative=relative, code=code, status=status, key=repr(key)):
                        self.record.unlink(missing_ok=True)
                        self.env.update(SENDGRID_API_KEY=key, CURL_EXIT=code, HTTP_STATUS=status)
                        result = subprocess.run([str(self.bin / "bash"), "-c", block], env=self.env,
                                                cwd=self.work, capture_output=True, text=True, timeout=10)
                        self.assertNotEqual(result.returncode, 0)
                        if key.startswith("SG.bad"):
                            self.assertEqual(self.calls(), [])
                            self.assertNotIn(key, result.stdout + result.stderr)
                        else:
                            self.assertEqual(len(self.calls()), 1)
                            if code != "0":
                                self.assertEqual(result.returncode, int(code))
                                self.assertIn("delivery status is unknown", result.stderr)

    def test_missing_key_and_invalid_dns_input_do_not_use_transport(self):
        self.env.pop("SENDGRID_API_KEY")
        for helper in ("send-test-email.sh", "send-html-email.sh"):
            result = self.run_helper(helper, "test@example.com", "Test", "Body")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(self.calls(), [])
        for hostname in ("", "-option", "$(touch NEVER)", "https://parse.example.com/"):
            result = self.run_helper("verify-inbound-setup.sh", hostname)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(self.calls(), [])


if __name__ == "__main__":
    for name in ("bash", "jq"):
        executable = getattr(OPTIONS, name)
        if not executable or not Path(executable).is_file():
            options.error("Required executable missing: " + str(executable))
        version = subprocess.check_output([executable, "--version"], text=True).splitlines()[0]
        print(name + ": " + str(Path(executable).resolve()) + " (" + version + ")", file=sys.stderr)
    unittest.main(argv=[sys.argv[0], *TEST_ARGS])

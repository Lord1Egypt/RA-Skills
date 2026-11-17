"""Builders for synthetic Claude Code and Codex session logs.

They mirror the record shapes seen in real logs (Claude Code 2.x,
Codex CLI 0.122–0.154); every value is invented."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

T0 = datetime(2026, 9, 12, 9, 0, tzinfo=timezone.utc)


def ts(minutes: int) -> str:
    return (T0 + timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")


class ClaudeSession:
    def __init__(self, cwd, session_id: str = "sess-1", sidechain: bool = False, start: int = 0):
        self.cwd, self.sid, self.sidechain = str(cwd), session_id, sidechain
        self.lines: list[dict] = []
        self.n = start

    def _base(self, typ: str) -> dict:
        self.n += 1
        return {"type": typ, "uuid": f"{self.sid}-u{self.n}", "parentUuid": None,
                "sessionId": self.sid, "timestamp": ts(self.n), "cwd": self.cwd,
                "isSidechain": self.sidechain, "userType": "external", "version": "2.1.0"}

    def user(self, text: str, **extra) -> str:
        d = self._base("user")
        d["message"] = {"role": "user", "content": text}
        d.update(extra)
        self.lines.append(d)
        return d["uuid"]

    def assistant_text(self, text: str) -> str:
        d = self._base("assistant")
        d["message"] = {"role": "assistant", "content": [{"type": "text", "text": text}]}
        self.lines.append(d)
        return d["uuid"]

    def tool(self, name: str, inp: dict, result: str, is_error: bool = False) -> tuple[str, str]:
        a = self._base("assistant")
        tool_id = f"toolu_{a['uuid']}"
        a["message"] = {"role": "assistant",
                        "content": [{"type": "tool_use", "id": tool_id, "name": name, "input": inp}]}
        self.lines.append(a)
        r = self._base("user")
        r["message"] = {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_id, "content": result, "is_error": is_error}]}
        self.lines.append(r)
        return a["uuid"], r["uuid"]

    def edit(self, path, old: str, new: str) -> tuple[str, str]:
        return self.tool("Edit", {"file_path": str(path), "old_string": old, "new_string": new},
                         "The file has been updated.")

    def write(self, path, content: str) -> tuple[str, str]:
        return self.tool("Write", {"file_path": str(path), "content": content}, "File created successfully")

    def bash(self, cmd: str, output: str, is_error: bool = False) -> tuple[str, str]:
        return self.tool("Bash", {"command": cmd, "description": "run"}, output, is_error)

    def compact_summary(self, text: str) -> None:
        d = self._base("user")
        d["isCompactSummary"] = True
        d["message"] = {"role": "user", "content": text}
        self.lines.append(d)

    def raw(self, obj: dict) -> None:
        self.lines.append(obj)

    def set_cwd(self, cwd) -> None:
        self.cwd = str(cwd)

    def save(self, projects_dir, agent_id: str | None = None) -> Path:
        folder = Path(projects_dir) / ("-" + self.cwd.strip("/").replace("/", "-").replace(" ", "-"))
        path = (folder / self.sid / "subagents" / f"agent-{agent_id}.jsonl") if agent_id \
            else folder / f"{self.sid}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in self.lines),
                        encoding="utf-8")
        return path


class CodexSession:
    def __init__(self, cwd, session_id: str = "codex-1", source="cli", version: str = "0.147.0"):
        self.cwd, self.sid = str(cwd), session_id
        self.n = 0
        self.lines: list[dict] = [{"timestamp": ts(0), "type": "session_meta", "payload": {
            "id": session_id, "timestamp": ts(0), "cwd": self.cwd, "originator": "codex-tui",
            "cli_version": version, "source": source}}]

    def _ev(self, typ: str, payload: dict) -> int:
        self.n += 1
        self.lines.append({"timestamp": ts(self.n), "type": typ, "payload": payload})
        return len(self.lines)  # the 1-based line number in the saved file

    def set_cwd(self, cwd) -> None:
        self.cwd = str(cwd)

    def user(self, text: str) -> int:
        self._ev("turn_context", {"cwd": self.cwd})
        return self._ev("event_msg", {"type": "user_message", "message": text})

    def agent(self, text: str) -> int:
        return self._ev("event_msg", {"type": "agent_message", "message": text, "phase": "final_answer"})

    def update(self, path, diff: str) -> int:
        return self._ev("event_msg", {"type": "patch_apply_end", "call_id": f"c{self.n}", "success": True,
                                      "changes": {str(path): {"type": "update", "unified_diff": diff,
                                                              "move_path": None}}})

    def add(self, path, content: str) -> int:
        return self._ev("event_msg", {"type": "patch_apply_end", "call_id": f"c{self.n}", "success": True,
                                      "changes": {str(path): {"type": "add", "content": content}}})

    def exec_end(self, cmd: str, output: str, exit_code=0, cwd=None) -> int:
        return self._ev("event_msg", {"type": "exec_command_end", "call_id": f"c{self.n}",
                                      "command": ["/bin/zsh", "-lc", cmd], "cwd": str(cwd or self.cwd),
                                      "aggregated_output": output, "exit_code": exit_code,
                                      "status": "completed"})

    def item_command(self, cmd: str, output: str, exit_code=0, cwd=None) -> int:
        return self._ev("event_msg", {"type": "item_completed", "item": {
            "type": "CommandExecution", "id": f"exec-{self.n}", "command": ["/bin/zsh", "-lc", cmd],
            "cwd": "file://" + str(cwd or self.cwd), "aggregated_output": output,
            "exit_code": exit_code, "status": "completed" if str(exit_code) == "0" else "failed"}})

    def item_filechange(self, changes: dict) -> int:
        return self._ev("event_msg", {"type": "item_completed", "item": {
            "type": "FileChange", "id": f"fc-{self.n}", "changes": changes}})

    def apply_patch_call(self, patch: str) -> int:
        return self._ev("response_item", {"type": "custom_tool_call", "call_id": f"c{self.n}",
                                          "name": "apply_patch", "input": patch, "status": "completed"})

    def function_exec(self, cmd: str, output: str) -> int:
        call = f"call_{self.n}"
        self._ev("response_item", {"type": "function_call", "name": "exec_command", "call_id": call,
                                   "arguments": json.dumps({"cmd": cmd, "workdir": self.cwd})})
        return self._ev("response_item", {"type": "function_call_output", "call_id": call, "output": output})

    def custom_exec(self, cmd: str, output: str) -> int:
        call = f"call_{self.n}"
        js = "const r = await tools.exec_command(" + json.dumps({"cmd": cmd, "workdir": self.cwd}) + ");\ntext(r.output);\n"
        self._ev("response_item", {"type": "custom_tool_call", "name": "exec", "call_id": call, "input": js})
        return self._ev("response_item", {"type": "custom_tool_call_output", "call_id": call,
                                          "output": [{"type": "input_text", "text": output}]})

    def compacted(self) -> int:
        return self._ev("compacted", {"message": "summary"})

    def save(self, sessions_dir) -> Path:
        path = Path(sessions_dir) / "2026" / "09" / "12" / f"rollout-2026-09-12T09-00-00-{self.sid}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in self.lines),
                        encoding="utf-8")
        return path

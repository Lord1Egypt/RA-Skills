#!/usr/bin/env python3
"""Tailnet SSH File Manager — remote file ops over Tailscale SSH."""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile


def run_ssh(host, command, timeout=60, stdin=None):
    """Run a command over SSH and return (returncode, stdout, stderr)."""
    cmd = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=10",
        "-o", "StrictHostKeyChecking=accept-new",
        host,
        command,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, input=stdin)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "SSH connection timed out"
    except Exception as e:
        return -1, "", str(e)


def run_scp(src, dst, timeout=120):
    """Run scp command."""
    cmd = [
        "scp",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=10",
        "-o", "StrictHostKeyChecking=accept-new",
        src,
        dst,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "SCP connection timed out"
    except Exception as e:
        return -1, "", str(e)


def ok(data):
    print(json.dumps({"success": True, "data": data}, ensure_ascii=False))


def err(message, stderr=""):
    payload = {"success": False, "error": message}
    if stderr:
        payload["stderr"] = stderr
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(1)


def _escape_path(path):
    """Escape single quotes for shell usage inside single-quoted strings."""
    return path.replace("'", "'\"'\"'")


def action_list(args):
    py_cmd = (
        "python3 -c $'import os, json\\n"
        f"path=\\\"{_escape_path(args.path)}\\\"\\n"
        "entries=[]\\n"
        "for name in os.listdir(path):\\n"
        "  try:\\n"
        "    full=os.path.join(path,name)\\n"
        "    st=os.lstat(full)\\n"
        "    entries.append({\"name\":name,\"size\":st.st_size,\"mode\":oct(st.st_mode),\"is_dir\":os.path.isdir(full),\"mtime\":st.st_mtime})\\n"
        "  except Exception as e:\\n"
        "    entries.append({\"name\":name,\"error\":str(e)})\\n"
        "print(json.dumps(entries))\\'"
    )
    rc, out, er = run_ssh(args.host, py_cmd)
    if rc != 0:
        err("Failed to list directory", er)
    try:
        data = json.loads(out)
        ok({"path": args.path, "entries": data})
    except json.JSONDecodeError:
        err("Failed to parse remote listing", out + "\n" + er)


def action_read(args):
    if args.format == "base64":
        rc, out, er = run_ssh(args.host, f"base64 -w 0 '{_escape_path(args.path)}'")
        if rc != 0:
            err("Failed to read file", er)
        ok({"path": args.path, "format": "base64", "content": out.strip()})
    else:
        rc, out, er = run_ssh(args.host, f"cat '{_escape_path(args.path)}'")
        if rc != 0:
            err("Failed to read file", er)
        ok({"path": args.path, "format": "text", "content": out})


def action_write(args):
    if args.content_base64:
        try:
            data = base64.b64decode(args.content_base64)
        except Exception as e:
            err(f"Invalid base64 content: {e}")
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".tmp") as f:
            f.write(data)
            tmp_path = f.name
    else:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tmp") as f:
            f.write(args.content)
            tmp_path = f.name
    try:
        rc, out, er = run_scp(tmp_path, f"{args.host}:'{_escape_path(args.path)}'")
        if rc != 0:
            err("Failed to write file", er)
        ok({"path": args.path, "bytes_written": os.path.getsize(tmp_path)})
    finally:
        os.unlink(tmp_path)


def action_delete(args):
    rc, out, er = run_ssh(args.host, f"rm -rf '{_escape_path(args.path)}'")
    if rc != 0:
        err("Failed to delete", er)
    ok({"deleted": args.path})


def action_move(args):
    rc, out, er = run_ssh(args.host, f"mv '{_escape_path(args.src)}' '{_escape_path(args.dst)}'")
    if rc != 0:
        err("Failed to move", er)
    ok({"src": args.src, "dst": args.dst})


def action_copy(args):
    rc, out, er = run_ssh(args.host, f"cp -r '{_escape_path(args.src)}' '{_escape_path(args.dst)}'")
    if rc != 0:
        err("Failed to copy", er)
    ok({"src": args.src, "dst": args.dst})


def action_stat(args):
    py_cmd = (
        "python3 -c $'import os, json\\n"
        f"path=\\\"{_escape_path(args.path)}\\\"\\n"
        "st=os.stat(path)\\n"
        "print(json.dumps({\"size\":st.st_size,\"mode\":oct(st.st_mode),\"uid\":st.st_uid,\"gid\":st.st_gid,\"mtime\":st.st_mtime,\"is_dir\":os.path.isdir(path)}))\\'"
    )
    rc, out, er = run_ssh(args.host, py_cmd)
    if rc != 0:
        err("Failed to stat", er)
    try:
        ok({"path": args.path, "stat": json.loads(out)})
    except json.JSONDecodeError:
        err("Failed to parse stat output", out + "\n" + er)


def action_find(args):
    rc, out, er = run_ssh(args.host, f"find '{_escape_path(args.path)}' -name '{_escape_path(args.name)}'")
    # find returns 1 when no matches; that is not an error for us.
    if rc not in (0, 1):
        err("Failed to find", er)
    files = [line for line in out.strip().split("\n") if line]
    ok({"path": args.path, "pattern": args.name, "matches": files})


def action_chmod(args):
    rc, out, er = run_ssh(args.host, f"chmod {args.mode} '{_escape_path(args.path)}'")
    if rc != 0:
        err("Failed to chmod", er)
    ok({"path": args.path, "mode": args.mode})


def action_push(args):
    if not os.path.exists(args.local):
        err(f"Local file does not exist: {args.local}")
    rc, out, er = run_scp(args.local, f"{args.host}:'{_escape_path(args.remote)}'")
    if rc != 0:
        err("Failed to push file", er)
    ok({"local": args.local, "remote": args.remote})


def action_pull(args):
    rc, out, er = run_scp(f"{args.host}:'{_escape_path(args.remote)}'", args.local)
    if rc != 0:
        err("Failed to pull file", er)
    ok({"remote": args.remote, "local": args.local})


def main():
    parser = argparse.ArgumentParser(description="Tailnet SSH File Manager")
    subparsers = parser.add_subparsers(dest="action", required=True)

    def add_host(p):
        p.add_argument("--host", required=True, help="Tailscale hostname or IP")

    p = subparsers.add_parser("list")
    add_host(p)
    p.add_argument("--path", required=True)
    p.set_defaults(func=action_list)

    p = subparsers.add_parser("read")
    add_host(p)
    p.add_argument("--path", required=True)
    p.add_argument("--format", choices=["text", "base64"], default="text")
    p.set_defaults(func=action_read)

    p = subparsers.add_parser("write")
    add_host(p)
    p.add_argument("--path", required=True)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--content", help="Text content to write")
    group.add_argument("--content-base64", help="Base64-encoded content to write")
    p.set_defaults(func=action_write)

    p = subparsers.add_parser("delete")
    add_host(p)
    p.add_argument("--path", required=True)
    p.set_defaults(func=action_delete)

    p = subparsers.add_parser("move")
    add_host(p)
    p.add_argument("--src", required=True)
    p.add_argument("--dst", required=True)
    p.set_defaults(func=action_move)

    p = subparsers.add_parser("copy")
    add_host(p)
    p.add_argument("--src", required=True)
    p.add_argument("--dst", required=True)
    p.set_defaults(func=action_copy)

    p = subparsers.add_parser("stat")
    add_host(p)
    p.add_argument("--path", required=True)
    p.set_defaults(func=action_stat)

    p = subparsers.add_parser("find")
    add_host(p)
    p.add_argument("--path", required=True)
    p.add_argument("--name", required=True)
    p.set_defaults(func=action_find)

    p = subparsers.add_parser("chmod")
    add_host(p)
    p.add_argument("--path", required=True)
    p.add_argument("--mode", required=True)
    p.set_defaults(func=action_chmod)

    p = subparsers.add_parser("push")
    add_host(p)
    p.add_argument("--local", required=True)
    p.add_argument("--remote", required=True)
    p.set_defaults(func=action_push)

    p = subparsers.add_parser("pull")
    add_host(p)
    p.add_argument("--remote", required=True)
    p.add_argument("--local", required=True)
    p.set_defaults(func=action_pull)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
sharedmem.py — local, file-locked shared key-value store for coordinating
multiple agent processes on the same machine without clobbering writes.

Usage:
    python3 sharedmem.py set   <namespace> <key> <value>
    python3 sharedmem.py get   <namespace> <key>
    python3 sharedmem.py incr  <namespace> <key> [amount=1]
    python3 sharedmem.py cas   <namespace> <key> <expected> <new>
    python3 sharedmem.py list  <namespace>
    python3 sharedmem.py delete <namespace> <key>

Storage: a single JSON file (sharedmem.json) in the current working
directory, guarded by an OS-level advisory lock so concurrent writers
are serialized rather than racing.

Scope/limits: single-machine only, not a distributed store. Values capped
at 64KB. No encryption — do not store secrets here.
"""
import sys
import json
import os
import time
import contextlib

STORE_FILE = "sharedmem.json"
MAX_VALUE_BYTES = 64 * 1024
LOCK_TIMEOUT_S = 5

# --- cross-platform file locking -------------------------------------------
try:
    import fcntl

    @contextlib.contextmanager
    def locked_file(path, mode):
        f = open(path, mode)
        deadline = time.time() + LOCK_TIMEOUT_S
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.time() > deadline:
                    f.close()
                    raise TimeoutError("could not acquire sharedmem lock in time")
                time.sleep(0.05)
        try:
            yield f
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

except ImportError:
    import msvcrt

    @contextlib.contextmanager
    def locked_file(path, mode):
        f = open(path, mode)
        deadline = time.time() + LOCK_TIMEOUT_S
        while True:
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.time() > deadline:
                    f.close()
                    raise TimeoutError("could not acquire sharedmem lock in time")
                time.sleep(0.05)
        try:
            yield f
        finally:
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except Exception:
                pass
            f.close()


def _ensure_store():
    if not os.path.exists(STORE_FILE):
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def _load(f):
    f.seek(0)
    content = f.read()
    if not content.strip():
        return {}
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}


def _save(f, data):
    f.seek(0)
    f.truncate()
    json.dump(data, f, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())


def cmd_set(namespace, key, value):
    if len(value.encode("utf-8")) > MAX_VALUE_BYTES:
        return {"error": f"value exceeds {MAX_VALUE_BYTES} byte cap"}
    _ensure_store()
    with locked_file(STORE_FILE, "r+") as f:
        data = _load(f)
        ns = data.setdefault(namespace, {})
        ns[key] = value
        _save(f, data)
    return {"status": "ok", "namespace": namespace, "key": key}


def cmd_get(namespace, key):
    _ensure_store()
    with locked_file(STORE_FILE, "r+") as f:
        data = _load(f)
    ns = data.get(namespace, {})
    if key not in ns:
        return {"error": "not found", "namespace": namespace, "key": key}
    return {"namespace": namespace, "key": key, "value": ns[key]}


def cmd_incr(namespace, key, amount):
    _ensure_store()
    with locked_file(STORE_FILE, "r+") as f:
        data = _load(f)
        ns = data.setdefault(namespace, {})
        try:
            current = int(ns.get(key, "0"))
        except ValueError:
            return {"error": f"existing value for {key} is not an integer"}
        new_val = current + amount
        ns[key] = str(new_val)
        _save(f, data)
    return {"status": "ok", "namespace": namespace, "key": key, "value": new_val}


def cmd_cas(namespace, key, expected, new):
    """Compare-and-swap: only write `new` if current value == expected."""
    _ensure_store()
    with locked_file(STORE_FILE, "r+") as f:
        data = _load(f)
        ns = data.setdefault(namespace, {})
        current = ns.get(key)
        if current != expected:
            return {
                "status": "conflict",
                "namespace": namespace,
                "key": key,
                "expected": expected,
                "actual": current,
            }
        ns[key] = new
        _save(f, data)
    return {"status": "ok", "namespace": namespace, "key": key, "value": new}


def cmd_list(namespace):
    _ensure_store()
    with locked_file(STORE_FILE, "r+") as f:
        data = _load(f)
    return {"namespace": namespace, "items": data.get(namespace, {})}


def cmd_delete(namespace, key):
    _ensure_store()
    with locked_file(STORE_FILE, "r+") as f:
        data = _load(f)
        ns = data.get(namespace, {})
        existed = key in ns
        ns.pop(key, None)
        _save(f, data)
    return {"status": "ok" if existed else "not_found", "namespace": namespace, "key": key}


def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "usage: sharedmem.py <set|get|incr|cas|list|delete> ..."}))
        sys.exit(1)

    op = args[0]
    try:
        if op == "set" and len(args) == 4:
            result = cmd_set(args[1], args[2], args[3])
        elif op == "get" and len(args) == 3:
            result = cmd_get(args[1], args[2])
        elif op == "incr" and len(args) in (3, 4):
            amount = int(args[3]) if len(args) == 4 else 1
            result = cmd_incr(args[1], args[2], amount)
        elif op == "cas" and len(args) == 5:
            result = cmd_cas(args[1], args[2], args[3], args[4])
        elif op == "list" and len(args) == 2:
            result = cmd_list(args[1])
        elif op == "delete" and len(args) == 3:
            result = cmd_delete(args[1], args[2])
        else:
            result = {"error": "bad arguments for operation: " + op}
    except TimeoutError as e:
        result = {"error": str(e)}

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(1 if "error" in result else 0)


if __name__ == "__main__":
    main()

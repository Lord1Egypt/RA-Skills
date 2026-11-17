#!/usr/bin/env python3
"""Bounded read-only Git auditor. Writes only private janitor state; fetch is opt-in."""
import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import time
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
class Unknown(Exception): pass

class Runner:
    def __init__(self, budget=480, timeout=15):
        self.deadline = time.monotonic() + budget
        self.timeout = timeout
    def run(self, argv, allowed=(0,)):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise Unknown("budget exhausted")
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
        try:
            p = subprocess.run(argv, capture_output=True, env=env,
                               timeout=min(remaining, self.timeout), check=False)
        except subprocess.TimeoutExpired:
            raise Unknown("timeout") from None
        except OSError:
            raise Unknown("command unavailable") from None
        if p.returncode not in allowed:
            raise Unknown("command failed (exit code %s)" % p.returncode)
        return p.returncode, p.stdout.decode("utf-8", "surrogateescape")
    def git(self, path, *args, allowed=(0,)):
        return self.run(["git", "-C", str(path), *args], allowed)

def identity(value):
    return hashlib.sha256(str(value).encode("utf-8", "surrogateescape")).hexdigest()[:20]

def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, ensure_ascii=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def fold(previous, current, completed, now):
    """Unknown coverage retains open findings; absence alone never resolves them."""
    result = {}
    for key, item in current.items():
        old = previous.get(key)
        status = "new" if not old or old["status"] == "resolved" else (
            "worsened" if item["severity"] > old["severity"] else "persistent")
        result[key] = dict(item, status=status, first_seen=old["first_seen"] if old else now,
                           last_checked=now, uncertain=False)
    for key, old in previous.items():
        if key in result:
            continue
        item = dict(old)
        if item["scope"] in completed:
            item.update(status="resolved", last_checked=now, uncertain=False)
        else:
            item["uncertain"] = True
        result[key] = item
    return result

class Audit:
    def __init__(self, config, fetch=False, network=False):
        self.config = config
        self.runner = Runner(config.get("budget_seconds", 480), config.get("command_timeout_seconds", 15))
        self.fetch = fetch
        self.network = network
        self.findings = {}
        self.completed = set()
        self.errors = []
        self.summaries = []
        self.observations = {}
        self.seen_common = set()
    def finding(self, scope, target, label, severity=1):
        self.findings[scope + ":" + identity(target)] = dict(scope=scope, label=label, severity=severity)
    def check(self, scope, callback):
        try:
            callback()
            self.completed.add(scope)
        except (Unknown, OSError, ValueError, KeyError, TypeError, sqlite3.Error) as e:
            # Do not serialize raw exceptions: paths, command output and business data may be sensitive.
            self.errors.append({"scope": scope, "error": str(e) if isinstance(e, Unknown) else type(e).__name__})
    def git(self, path, *args, allowed=(0,)):
        return self.runner.git(path, *args, allowed=allowed)
    def processes(self, path):
        path = Path(path).resolve()
        pids = []
        denied = 0
        own = os.getpid()
        for p in Path("/proc").iterdir():
            if not p.name.isdigit() or int(p.name) == own:
                continue
            try:
                cwd = (p / "cwd").resolve(strict=True)
                if cwd == path or path in cwd.parents:
                    pids.append(int(p.name))
            except PermissionError:
                denied += 1
            except (FileNotFoundError, ProcessLookupError):
                pass
        return {"active_pids": pids, "coverage": "partial" if denied else "complete"}
    def worktree(self, repo, record):
        path = Path(record["worktree"])
        scope = repo["id"] + "/wt/" + identity(path)
        def inspect():
            if not path.is_dir():
                self.finding(scope, "missing", repo["id"] + ": worktree missing; review its registration", 2)
                return
            code, valid = self.git(path, "rev-parse", "--is-inside-work-tree")
            if valid.strip() != "true":
                raise Unknown("directory is not a Git working tree")
            _, branch = self.git(path, "symbolic-ref", "--short", "-q", "HEAD", allowed=(0, 1))
            head_code, head = self.git(path, "rev-parse", "--verify", "HEAD", allowed=(0, 128))
            self.observations[scope + "/head"] = {"branch_state": "unborn" if head_code else ("attached" if branch.strip() else "detached"), "head":head.strip() if not head_code else None}
            _, status = self.git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all")
            entries = status.split("\0")
            files, i = [], 0
            while i < len(entries):
                entry = entries[i]
                i += 1
                if not entry: continue
                files.append(entry[3:])
                if "R" in entry[:2] or "C" in entry[:2]: i += 1
            activity = self.processes(path)
            classification = "clean"
            if files:
                stamps = []
                for name in files:
                    try: stamps.append((path / name).lstat().st_mtime)
                    except OSError: pass
                if activity["active_pids"]:
                    classification = "active work"
                elif not stamps:
                    classification = "WIP with unknown age"
                elif time.time() - max(stamps) < 86400:
                    classification = "recent WIP with no observed process"
                else:
                    classification = "older WIP with no identified owner"
                self.finding(scope, "dirty", repo["id"] + ": " + classification,
                             2 if "older" in classification else 1)
            if "locked" in record:
                self.observations[scope + "/locked"] = True
            if "prunable" in record:
                self.finding(scope, "prunable", repo["id"] + ": prunable registration; supervised review required")
            for operation in ("MERGE_HEAD", "rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD",
                              "REVERT_HEAD", "BISECT_LOG", "sequencer", "index.lock"):
                _, location = self.git(path, "rev-parse", "--git-path", operation)
                candidate = Path(location.strip())
                if not candidate.is_absolute(): candidate = path / candidate
                if candidate.exists():
                    self.finding(scope, operation, repo["id"] + ": Git operation or lock " + operation, 3)
            _, final_status = self.git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all")
            if final_status != status: raise Unknown("working tree changed during inspection")
            self.observations[scope] = dict(path=str(path), dirty_count=len(files), classification=classification,
                                            activity=activity)
        self.check(scope, inspect)
    def repository(self, repo):
        path = Path(repo["path"])
        root_scope = repo["id"] + "/identity"
        holder = {}
        def root():
            _, result = self.git(path, "rev-parse", "--is-inside-work-tree")
            if result.strip() != "true": raise Unknown("not a repository with a working tree")
            _, common = self.git(path, "rev-parse", "--path-format=absolute", "--git-common-dir")
            holder["common"] = str(Path(common.strip()).resolve())
        self.check(root_scope, root)
        if not holder: return
        if holder["common"] in self.seen_common:
            self.observations[root_scope] = {"deduplicated": True}
            return
        self.seen_common.add(holder["common"])
        # Enumerate linked worktrees once, inspect each separately before network.
        def trees():
            _, raw = self.git(path, "worktree", "list", "--porcelain", "-z")
            record = {}
            for part in raw.split("\0"):
                if not part:
                    if "worktree" in record: self.worktree(repo, record)
                    record = {}
                else:
                    key, _, value = part.partition(" ")
                    record[key] = value
            if "worktree" in record: self.worktree(repo, record)
        self.check(repo["id"] + "/worktrees", trees)
        def fetch():
            if not self.fetch:
                raise Unknown("fetch not requested; remote protection not refreshed")
            self.git(path, "fetch", "--prune", repo.get("remote", "origin"))
        self.check(repo["id"] + "/fetch", fetch)
        def refs():
            if repo["id"] + "/fetch" not in self.completed:
                raise Unknown("remote protection requires a successful fetch")
            _, base = self.git(path, "rev-parse", "--verify", repo.get("base", "origin/main"))
            _, refs = self.git(path, "for-each-ref", "--format=%(refname)%09%(objectname)%09%(upstream)", "refs/heads")
            for line in refs.splitlines():
                ref, sha, upstream = line.split("\t")
                code, _ = self.git(path, "merge-base", "--is-ancestor", sha, base.strip(), allowed=(0, 1))
                _, containing = self.git(path, "for-each-ref", "--contains=" + sha, "--format=%(refname)", "refs/remotes")
                if code == 1 and not containing.strip():
                    self.finding(repo["id"] + "/refs", ref, repo["id"] + ": commit " + sha[:12] + " not protected by fetched remote refs", 3)
                if upstream:
                    code, _ = self.git(path, "rev-parse", "--verify", upstream, allowed=(0, 128))
                    if code == 0:
                        _, counts = self.git(path, "rev-list", "--left-right", "--count", ref + "..." + upstream)
                        a, b = map(int, counts.split())
                        if a and b: self.finding(repo["id"] + "/refs", ref + "/diverged", repo["id"] + ": diverged branch", 2)
        self.check(repo["id"] + "/refs", refs)
        def prs():
            if not self.network: raise Unknown("GitHub query not requested")
            _, raw = self.runner.run(["gh", "pr", "list", "--repo", repo["github"], "--state", "open",
                "--limit", "100", "--json", "number,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup"])
            items = json.loads(raw)
            if not isinstance(items, list): raise Unknown("invalid GitHub response")
            self.observations[repo["id"] + "/prs"] = {"open": len(items), "review_threads": "not queried"}
            for pr in items:
                if pr["mergeable"] == "CONFLICTING" or pr.get("reviewDecision") == "CHANGES_REQUESTED":
                    self.finding(repo["id"] + "/prs", pr["number"], repo["id"] + ": PR #" + str(pr["number"]) + " requires attention", 2)
                if pr["mergeable"] == "UNKNOWN" or pr.get("mergeStateStatus") == "UNKNOWN":
                    raise Unknown("mergeability unknown")
                for check in pr.get("statusCheckRollup") or []:
                    if check.get("conclusion") in ("FAILURE", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED"):
                        self.finding(repo["id"] + "/prs", str(pr["number"]) + "/checks", repo["id"] + ": PR checks failed", 2)
            if len(items) >= 100: raise Unknown("PR result limit reached")
        self.check(repo["id"] + "/prs", prs)
        if repo.get("service"):
            self.check(repo["id"] + "/runtime", lambda: self.runtime(repo))
        self.summaries.append({"id":repo["id"], "common_git_dir":holder["common"]})
    def runtime(self, repo):
        _, raw = self.runner.run(["systemctl", "show", repo["service"], "-p", "MainPID", "-p", "WorkingDirectory"])
        values = dict(x.split("=",1) for x in raw.splitlines() if "=" in x)
        pid = int(values.get("MainPID", "0"))
        if pid <= 0: raise Unknown("service has no active PID")
        cwd = Path("/proc") / str(pid) / "cwd"
        if cwd.resolve() != Path(repo["runtime"]).resolve():
            raise Unknown("runtime differs from inventory")
        # Read only the single permitted key; never emit environment contents.
        data = (Path("/proc") / str(pid) / "environ").read_bytes().split(b"\0")
        key = (repo["database_env_key"] + "=").encode()
        matches = [x[len(key):].decode() for x in data if x.startswith(key)]
        database = Path(matches[0]) / repo["database_filename"] if matches else Path(repo["database_default"])
        if not database.is_file() or database.stat().st_size == 0:
            self.finding(repo["id"] + "/runtime", "db", repo["id"] + ": database missing or empty", 3)
            return
        remaining = self.runner.deadline - time.monotonic()
        db_deadline = time.monotonic() + max(0, min(10, remaining))
        with sqlite3.connect("file:" + quote(str(database)) + "?mode=ro", uri=True, timeout=2) as db:
            db.set_progress_handler(lambda: int(time.monotonic() >= db_deadline), 1000)
            rows = db.execute("PRAGMA quick_check").fetchall()
        if rows != [("ok",)]:
            self.finding(repo["id"] + "/runtime", "db", repo["id"] + ": database integrity invalid", 3)
        lock_states = {}
        for name in ("path", "runtime"):
            lock = Path(repo[name]) / repo.get("deploy_lock", ".deploy.lock")
            if not lock.exists(): lock_states[name] = "absent"; continue
            with lock.open("rb") as f:
                try:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    lock_states[name] = "held"
                    self.finding(repo["id"] + "/runtime", str(lock), repo["id"] + ": deploy lock held", 2)
                else:
                    lock_states[name] = "free"
                    fcntl.flock(f, fcntl.LOCK_UN)
        self.observations[repo["id"] + "/runtime"] = dict(database=str(database), size=database.stat().st_size,
            configuration_source="process" if matches else "verified_application_default",
            quick_check="ok" if rows == [("ok",)] else "invalid", locks=lock_states)
    def inventory(self):
        excluded = {".git","node_modules",".cache",".next","backups","releases","media","uploads","data",
                    ".openclaw",".codex","tmp","temp"}
        if not self.config.get("discovery_root"):
            self.observations["inventory"] = {"state": "not configured"}
            return
        root = Path(self.config["discovery_root"])
        if not root.is_dir(): raise Unknown("discovery root does not exist")
        known = {r["common_git_dir"] for r in self.summaries}
        found = set()
        for base, dirs, files in os.walk(root, followlinks=False):
            if time.monotonic() > self.runner.deadline: raise Unknown("inventory budget exhausted")
            depth = len(Path(base).relative_to(root).parts)
            dirs[:] = [d for d in dirs if d not in excluded and not any(t in d.lower() for t in ("client", "backup", "release", "cache"))] if depth < self.config.get("discovery_depth", 4) else []
            if ".git" in files or (Path(base)/".git").is_dir():
                _, common = self.git(Path(base), "rev-parse", "--path-format=absolute", "--git-common-dir")
                found.add(common.strip())
                dirs[:] = []
        self.observations["inventory"] = {"extra_common_git_dirs":sorted(found-known),
                                          "count":len(found-known)}
    def artifacts(self, repo):
        # Metadata only; count regular files without opening contents or following symlinks.
        output = {}
        targets = [Path(repo["path"])/n for n in
                   ("node_modules","dist","build",".pytest_cache",".next","backups","releases")]
        if repo.get("runtime"):
            targets += [Path(repo["runtime"])/n for n in ("dist","build","node_modules")]
        for target in targets:
            if target.is_symlink() or not target.is_dir(): continue
            count, size = 0, 0
            for base, dirs, files in os.walk(target, followlinks=False):
                if time.monotonic() >= self.runner.deadline:
                    raise Unknown("artifact inventory budget exhausted")
                dirs[:] = [d for d in dirs if not (Path(base)/d).is_symlink()]
                for name in files:
                    p = Path(base)/name
                    if p.is_symlink(): continue
                    stat = p.stat()
                    count += 1
                    size += stat.st_size
            output[str(target)] = {"files":count,"bytes":size}
        self.observations[repo["id"]+"/artifacts"] = output
    def execute(self):
        for repo in self.config["repositories"]:
            self.repository(repo)
            self.check(repo["id"] + "/artifacts", lambda repo=repo: self.artifacts(repo))
        self.check("inventory", self.inventory)
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        return dict(schema=3, checked_at=now, mode="AUDIT", errors=self.errors,
                    completed=sorted(self.completed), findings=self.findings,
                    repositories=self.summaries, observations=self.observations)

def render(report):
    findings = report["findings"]
    active = [x for x in findings.values() if x["status"] != "resolved"]
    lines = ["🧹 Repository Janitor — AUDIT", report["checked_at"],
             "Repositories inspected: %d | Open findings: %d | Incomplete checks: %d" %
             (len(report["repositories"]), len(active), len(report["errors"]))]
    for repo in report["repositories"]:
        lines.append("- " + repo["id"] + ": inspected; see findings and coverage")
    for label in ("new", "worsened", "persistent"):
        selected = [x for x in active if x["status"] == label]
        if selected: lines.append(label.capitalize() + ": " + str(len(selected)))
    for item in sorted(active, key=lambda x:-x["severity"])[:12]:
        lines.append("- [%s] %s%s" % (item["status"], item["label"], " (recheck inconclusive)" if item.get("uncertain") else ""))
    if len(active) > 12: lines.append("Additional findings remain in private state; none were discarded.")
    if report["errors"]:
        lines.append("🚨 Incomplete coverage:")
        for error in report["errors"][:8]: lines.append("- " + error["scope"] + ": " + error["error"])
    if not active and not report["errors"]: lines.append("No decision needed today.")
    lines.insert(3, "No cleanup, commit, push or deployment performed.")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--github", action="store_true")
    parser.add_argument("--persist", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if not config.get("repositories"):
        parser.error("configure at least one explicitly approved repository")
    lock = Path(config["lock"])
    lock.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive owned marker, preserved if pre-existing. No stale-lock removal.
    try: fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print(json.dumps({"schema":3,"error":"concurrent execution or orphaned lock; preserve it"}))
        return 2
    inode = os.fstat(fd).st_ino
    try:
        with os.fdopen(fd, "w") as f: json.dump({"pid":os.getpid(),"mode":"AUDIT","started":time.time()}, f)
        report = Audit(config, args.fetch, args.github).execute()
        state = Path(config["state_dir"]) / "latest.json"
        previous = {}
        if state.exists():
            try: previous = json.loads(state.read_text())["findings"]
            except (OSError, ValueError, KeyError):
                report["errors"].append({"scope":"state", "error":"unreadable baseline; not overwritten"})
                print(json.dumps(report, ensure_ascii=True))
                return 2
        report["findings"] = fold(previous, report["findings"], report["completed"], report["checked_at"])
        report["notify"] = render(report)
        if args.persist: atomic(state, report)
        print(report["notify"] if args.report else json.dumps(report, ensure_ascii=True, indent=2 if args.pretty else None))
        return 0
    finally:
        try:
            if lock.stat().st_ino == inode: lock.unlink()
        except FileNotFoundError: pass

if __name__ == "__main__":
    raise SystemExit(main())

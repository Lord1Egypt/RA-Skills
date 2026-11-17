#!/usr/bin/env python3
"""Compare complete discovery runs on identical, offline GitLab responses."""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stdout
from copy import deepcopy
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import platform
import statistics
from tempfile import TemporaryDirectory
import threading
import time
from unittest.mock import patch
from urllib.parse import parse_qs, unquote, urlsplit


def load_script(path):
    spec = importlib.util.spec_from_file_location("discovery_benchmark", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Unable to load Python script: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GitLabFixture:
    """Paginated assigned work, denied access, incidents and collaborator scans."""

    def __init__(self, projects=10, items=75, latency_ms=10):
        self.latency = latency_ms / 1000
        self.projects = [
            {"id": value, "path_with_namespace": f"example/project-{value}", "archived": False}
            for value in range(1, projects + 1)
        ]
        self.items = []
        for value in range(1, items + 1):
            project_id = (value - 1) % projects + 1
            collection = "issues" if value % 2 else "merge_requests"
            self.items.append({
                "project_id": project_id, "iid": value, "title": f"Work {value}",
                "web_url": f"https://gitlab.example/example/project-{project_id}/-/{collection}/{value}",
                "issue_type": "issue", "state": "opened",
                "assignees": [{"username": "robot"}],
                "labels": ["workflow::forbidden" if project_id == projects else "workflow::in-progress"],
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-02T00:00:00Z", "user_notes_count": value % 3,
            })
        self.calls = Counter()
        self.logical_calls = Counter()
        self.inflight = 0
        self.peak = 0
        self.lock = threading.Lock()

    def api_json(self, endpoint):
        with self.lock:
            self.calls[endpoint] += 1
            self.logical_calls[endpoint] += 1
            self.inflight += 1
            self.peak = max(self.peak, self.inflight)
        try:
            time.sleep(self.latency)
            return deepcopy(self.response(endpoint))
        finally:
            with self.lock:
                self.inflight -= 1

    def graphql_json(self, query, variables):
        with self.lock:
            self.calls["graphql:dependency-links"] += 1
            self.inflight += 1
            self.peak = max(self.peak, self.inflight)
        try:
            time.sleep(self.latency)
            assert "linkedWorkItems(first:20, filter:BLOCKS" in query
            data = {}
            for index in sorted(int(key[1:]) for key in variables if key.startswith("p")):
                project = variables[f"p{index}"]
                iid = variables[f"i{index}"]
                project_id = int(project.rsplit("-", 1)[1])
                endpoint = f"projects/{project_id}/issues/{iid}/links?per_page=100&page=1"
                with self.lock:
                    self.logical_calls[endpoint] += 1
                links = self.response(endpoint)
                data[f"p{index}"] = {"fullPath": project, "item": {
                    "iid": iid, "linkedWorkItems": {
                        "nodes": [{"linkType": row["link_type"], "workItemState": row["state"].upper().replace("OPENED", "OPEN")}
                                  for row in links], "pageInfo": {"hasNextPage": False, "endCursor": None},
                    },
                }}
            return data
        finally:
            with self.lock:
                self.inflight -= 1

    def response(self, endpoint):
        parsed = urlsplit(endpoint)
        path = unquote(parsed.path)
        query = parse_qs(parsed.query)
        parts = path.split("/")
        if path == "user":
            return {"id": 99, "username": "robot"}
        if path == "projects":
            rows = self.projects
        elif path in ("issues", "merge_requests"):
            rows = [item for item in self.items if f"/-/{path}/" in item["web_url"]]
        elif parts[0] == "projects" and len(parts) == 2:
            return self.projects[int(parts[1]) - 1]
        elif "/members/all/" in path:
            project_id = int(parts[2].removeprefix("project-"))
            return {
                "username": "robot", "membership_state": "active", "access_level": 30,
                "created_by": {"username": "other" if project_id == len(self.projects) else "owner"},
            }
        elif path.startswith("users/"):
            return {"id": int(parts[1]), "public_email": "outsider@elsewhere.test"}
        elif parts[-1] == "links":
            rows = ([{"link_type": "blocks", "state": "opened"}]
                    if int(parts[-2]) % 3 == 0 else [])
        elif parts[-1] == "issues" and "issue_type" in query:
            rows = []
        elif parts[-1] == "issues" and query.get("assignee_id") == ["None"]:
            project_id = int(parts[1])
            rows = [{
                "project_id": project_id, "iid": 10000 + project_id, "issue_type": "issue",
                "assignees": [], "author": {"id": 1000 + project_id, "username": "outsider"},
                "web_url": f"https://gitlab.example/example/project-{project_id}/-/issues/{10000 + project_id}",
            }]
        elif parts[-2] in ("issues", "merge_requests"):
            return next(item for item in self.items if item["iid"] == int(parts[-1]))
        else:
            raise AssertionError(f"Unexpected fixture request: {endpoint}")
        size = int(query.get("per_page", [100])[0])
        page = int(query.get("page", [1])[0])
        return rows[(page - 1) * size:page * size]


def run_once(module, fixture):
    """Run real orchestration; replace only external I/O and configuration."""
    output = io.StringIO()
    # Separate the benchmark's collaborator lock from live discovery runs.
    with TemporaryDirectory(prefix="discovery-benchmark-") as directory, \
            patch.object(module, "api_json", side_effect=fixture.api_json), \
            patch.object(module, "graphql_json", side_effect=fixture.graphql_json, create=True), \
            patch.object(module, "configured_owner", return_value="owner"), \
            patch.object(module, "configured_accept_entries", return_value=["@example.test"]), \
            patch.object(module.shutil, "which", return_value="glab"), \
            patch("tempfile.gettempdir", return_value=directory), \
            patch.object(module.subprocess, "run", side_effect=AssertionError("Benchmark attempted external I/O")), \
            redirect_stdout(output):
        start = time.perf_counter()
        status = module.main()
        seconds = time.perf_counter() - start
    if status != 0:
        raise AssertionError(f"Discovery failed with status {status}")
    return json.loads(output.getvalue()), seconds


def benchmark(baseline, candidate, *, projects=10, items=75, latency_ms=10, runs=3):
    modules = {"baseline": baseline, "candidate": candidate}
    samples = {name: [] for name in modules}
    peaks = {name: [] for name in modules}
    requests = {name: [] for name in modules}
    expected_output = None
    expected_calls = None
    # Alternate order to reduce systematic first-run/load bias.
    for repetition in range(runs):
        names = list(modules) if repetition % 2 == 0 else list(reversed(modules))
        for name in names:
            fixture = GitLabFixture(projects, items, latency_ms)
            output, seconds = run_once(modules[name], fixture)
            if expected_output is None:
                expected_output, expected_calls = output, fixture.logical_calls
            if output != expected_output or fixture.logical_calls != expected_calls:
                raise AssertionError("Output or logical read coverage differs from baseline")
            samples[name].append(seconds)
            peaks[name].append(fixture.peak)
            requests[name].append(sum(fixture.calls.values()))
    measurements = {
        name: {"seconds": values, "median_seconds": statistics.median(values),
               "peak_concurrent_reads": peaks[name]}
        for name, values in samples.items()
    }
    return {
        "method": "offline full-main replay with fixed latency per GitLab API request; not live GitLab throughput",
        "python": platform.python_version(), "platform": platform.platform(),
        "fixture": {"projects": projects, "assigned_items": items, "latency_ms": latency_ms,
                    "runs": runs, "includes": ["denied membership", "paginated endpoints", "collaborator scans", "dependency links"]},
        "output_equivalent": True, "logical_read_coverage_equivalent": True,
        "returned_items": len(expected_output), "logical_reads_per_run": sum(expected_calls.values()),
        "requests_per_run": requests,
        "measurements": measurements,
        "speedup": measurements["baseline"]["median_seconds"] / measurements["candidate"]["median_seconds"],
    }


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Value must be positive")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", type=Path, default=Path(__file__).with_name("list-active-items.py"))
    parser.add_argument("--projects", type=positive_int, default=10)
    parser.add_argument("--items", type=positive_int, default=75)
    parser.add_argument("--latency-ms", type=positive_int, default=10)
    parser.add_argument("--runs", type=positive_int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = benchmark(load_script(args.baseline), load_script(args.candidate),
                       projects=args.projects, items=args.items, latency_ms=args.latency_ms, runs=args.runs)
    result["sources"] = {
        name: {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for name, path in (("baseline", args.baseline), ("candidate", args.candidate))
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

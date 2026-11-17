# Measure discovery performance

Compare `list-active-items.py` against an earlier revision without contacting
GitLab. The benchmark runs the complete discovery orchestration against identical
synthetic API responses and checks both the returned JSON and logical read
coverage. It rejects output changes, missing reads and attempted external I/O.
GraphQL batches replace individual REST dependency requests, so physical request
counts are reported separately for each implementation.

## Run the comparison

You need Python 3.12 or later on Linux and a repository checkout containing both
revisions. The benchmark uses only the Python standard library. Run these commands
from the repository root before merging the optimization; afterward, change
`discovery_baseline_ref` to a revision before the optimization.

```bash
discovery_baseline_ref=main
discovery_baseline_script=$(mktemp --suffix=.py)
git show "${discovery_baseline_ref}:profile/eugene-harold-krabs/skills/gitlab-agent/scripts/list-active-items.py" > "$discovery_baseline_script"
python3 profile/eugene-harold-krabs/skills/gitlab-agent/scripts/benchmark-discovery.py \
  --baseline "$discovery_baseline_script" \
  --projects 10 --items 75 --latency-ms 25 --runs 5 \
  --output discovery-benchmark.json
```

The JSON report includes every sample, median durations, speedup, peak concurrent
reads, physical request counts, logical read coverage and source SHA-256 hashes. The two
implementations run in alternating order. A successful comparison exits zero;
different output or logical read coverage fails the command. A speedup below one is
reported honestly and does not turn noisy timing into a functional test failure.

The fixture includes assigned issues and MRs, denied membership, incident queries,
collaborator scans and dependency links. To exercise multiple assigned-item pages,
repeat with `--projects 12 --items 240`. The last project's membership is denied,
so the number of returned items is smaller than `--items`.

## Interpret the result

[The recorded comparison](discovery-benchmark.json) uses fixed latency per API
request. It measures overlapping waits, not live GitLab throughput, glab process
startup, API rate limits, assignment throughput or contention with another
discovery run. It requires no token or GitLab login and performs no GitLab writes.
Actual elapsed durations depend on network latency, project counts, collaborator
configuration, pending label mutations and GitLab responses.

Discovery permits at most four concurrent reads within one invocation. It retains
fresh per-run membership, project and label checks; it does not reuse authorization
without contacting GitLab or omit unchanged items. Pagination remains sequential within each
endpoint, and result ordering does not depend on completion order.

Dependency lookups use GraphQL batches of up to ten issues, only after those
issues pass the discovery gates. The query requests `linkedWorkItems` filtered
by `BLOCKS` and checks each linked item's state; a count alone would not establish
whether the blocked item is still open. Every page is read, including pages after
an open dependency is found. Missing data, GraphQL errors and stalled cursors fail
the run without emitting a partial queue. There is no REST fallback for these
queries; GraphQL availability is required.

The project and membership gates retain their existing REST checks. In particular,
membership still requires an explicit active state and the configured owner's
membership-creator identity. GraphQL batching does not infer authorization from
being able to see a project.

Assignment and label writes remain serialized. When a prefetched label snapshot
needs a change, discovery reads labels again immediately before applying the
delta. Concurrent clients can still change GitLab after that read; there is no
atomic label compare-and-set in this helper.

## Request timeouts

Each REST or GraphQL read has a 25-second timeout. If the process times out,
discovery waits one second and retries the identical read once. A second timeout
propagates through the existing failure handling; required scan or dependency
failures still prevent a partial queue from being returned. The retry does not
skip a pagination page, reuse stale metadata or switch GraphQL to REST.

HTTP errors, invalid JSON and incomplete GraphQL responses are not retried.
Assignment and label mutations are never retried automatically, because a timed-out
write might already have taken effect. The four-reader concurrency limit remains
unchanged. Retries can increase elapsed time and physical request counts, so include
failed attempts when comparing runs.

## Run the installed helpers

The container includes `uv`. Discovery and report helpers use a
`#!/usr/bin/env -S uv run --script` shebang with inline Python 3.12-or-later
metadata and no third-party dependencies. Run them directly to use that entry
point. See [uv's script guide](https://docs.astral.sh/uv/guides/scripts/).

```bash
profile/eugene-harold-krabs/skills/gitlab-agent/scripts/list-active-items.py
```

This runs normal discovery, including its usual label and assignment mutations;
it is not a read-only benchmark. The Work Queue service launches its fixed
read-only report directly through the same uv shebang.

API responses are not cached on disk or reused by the transport. Each API read
contacts GitLab. The existing per-run project eligibility map remains local to
one invocation; it is not a response cache. Old request-cache files are ignored.
Locking libraries load only when collaborator assignment is configured; the
thread pool loads only for parallel reads, date parsing when ordering, URL
helpers at their point of use, and retry backoff only after a timeout.

## Check correctness in CI

The existing required `test_*.py` discovery runs the performance regressions. They
check real read overlap with a synchronization barrier, the four-reader bound,
ordered output, serialized writes, fresh labels before mutation, failed reads and
multi-page full-discovery equivalence, GraphQL pagination and failure handling.
Runtime regressions verify fresh responses on repeated requests, ignored legacy
cache files, and deferred optional imports.
CI prints a `DISCOVERY_BENCHMARK` JSON record
comparing one reader with the default pool. It asserts correctness and bounded
concurrency, not a wall-clock threshold that depends on runner load.

#!/usr/bin/env python3
"""
Measure a model against the gate, instead of arguing about which model to use.

    python3 bench.py --model-endpoint http://127.0.0.1:8080/v1 --model-name qwen3-1.7b
    python3 bench.py --json > qwen3-1.7b.json
    python3 bench.py --repeat 3        # the same battery three times

The whole point of the design in `rwlib/rewrite.py` is that a small model's
output is not trusted, it is gated. That turns "is a 1.7B good enough" from a
matter of taste into a pass rate over a fixed battery, and this is the thing
that prints it. Run it against llama.cpp, against Ollama, against OpenRouter,
against a frontier model, and compare the columns.

What it reports, and why each one earns its place:

    accepted        the number that matters. Passages the gate let through.
    first attempt   accepted with no retry. The difference between this and
                    `accepted` is what the retry loop is buying, and on a model
                    where the two are equal the loop is dead weight.
    rejected by     a histogram of *why*, which is the number that tells you
                    what to do next. A model failing mostly on "nothing
                    improved" needs a better prompt or a bigger model. One
                    failing mostly on "number altered" is unsafe at any size for
                    this job, whatever its pass rate.
    seconds/unit    what a Pi actually costs. A 92% pass rate at 40 seconds a
                    passage is a different tool from the same rate at 2.

`--repeat` exists because a single pass over twelve cases at temperature 0.2 is
not a stable measurement, and a bench that reports one run as if it were the
model's rate is the kind of number this repository does not publish.

Nothing here writes to a document. It reads its own battery, sends passages,
scores replies, and prints. Stdlib only, 3.9+.
"""

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
ENGINE = os.path.join(os.path.dirname(SKILL), "rabbit-writes", "scripts")
for path in (ENGINE, HERE):
    if path not in sys.path:
        sys.path.insert(0, path)

import scan as scan_mod                              # noqa: E402
import verify as verify_mod                          # noqa: E402
from rwlib import cli_error                          # noqa: E402
from rwlib import endpoint as endpoint_mod           # noqa: E402
from rwlib import injection                          # noqa: E402
from rwlib import rewrite as rewrite_mod             # noqa: E402

BATTERY_PATH = os.path.join(HERE, "battery.json")


def load_battery(path=BATTERY_PATH):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict) or not data.get("cases"):
        raise ValueError("%s carries no cases" % path)
    return data


def _short(reason):
    """A rejection reason, cut back to the class it belongs to.

    The histogram is only useful if two rejections of the same kind land in the
    same bucket, and every reason carries a specific phrase or count in it.
    """
    for prefix in ("still contains", "findings went", "length went to",
                   "the model returned", "the rewrite added",
                   "the rewrite contains"):
        if reason.startswith(prefix):
            return prefix
    # verify.py's violations arrive as "kind: detail", and the kind is the class.
    return reason.split(":", 1)[0][:40]


def run_case(case, endpoint, attempts, burstiness_floor):
    """One battery case: plan it, send every unit, score the replies."""
    register = case.get("register") or scan_mod.DEFAULT_REGISTER
    text = case["text"]

    def scan_fn(chunk):
        # ste="off": the battery's pass rates were calibrated without ste
        # findings in the gate, and adding them is a battery.json
        # recalibration rather than a flag.
        return scan_mod.scan(chunk, register, ste="off")[0]

    findings = scan_fn(text)
    units, unaddressable = rewrite_mod.plan(
        text, findings, budget_tokens=endpoint.input_budget(),
        estimate=endpoint_mod.estimate_tokens,
        burstiness_floor=burstiness_floor)

    results = []
    for unit in units:
        started = time.monotonic()
        _, record = rewrite_mod.rewrite_unit(
            unit, endpoint, scan_fn, verify_mod.validate,
            alternatives=rewrite_mod.load_alternatives(),
            attempts=attempts, injection_fn=injection.scan)
        record["seconds"] = time.monotonic() - started
        results.append(record)

    after = rewrite_mod.splice(text, results)
    return {"id": case["id"], "register": register,
            "findings_before": len(findings),
            "findings_after": len(scan_fn(after)),
            "units": len(units), "unaddressable": len(unaddressable),
            "records": results, "before": text, "after": after}


def summarize(cases, elapsed):
    units = [r for case in cases for r in case["records"]]
    accepted = [r for r in units if r["accepted"]]
    first = [r for r in accepted if len(r["attempts"]) == 0]
    rejections = {}
    for record in units:
        for attempt in record["attempts"]:
            for reason in attempt.split("; "):
                key = _short(reason)
                rejections[key] = rejections.get(key, 0) + 1
    before = sum(c["findings_before"] for c in cases)
    after = sum(c["findings_after"] for c in cases)
    return {
        "cases": len(cases),
        "units": len(units),
        "accepted": len(accepted),
        "accepted_pct": round(100.0 * len(accepted) / len(units), 1) if units else 0.0,
        "first_attempt": len(first),
        "findings_before": before,
        "findings_after": after,
        "findings_removed_pct": (round(100.0 * (before - after) / before, 1)
                                 if before else 0.0),
        "seconds_total": round(elapsed, 1),
        "seconds_per_unit": round(elapsed / len(units), 2) if units else 0.0,
        "rejected_by": dict(sorted(rejections.items(), key=lambda kv: -kv[1])),
    }


def report(summary, endpoint, battery_version, repeat):
    lines = ["rabbit-rewrites bench",
             "  endpoint       %s" % endpoint.describe(),
             "  battery        v%s, %d case(s), %d pass(es)"
             % (battery_version, summary["cases"] // max(1, repeat), repeat),
             "",
             "  units sent     %d" % summary["units"],
             "  accepted       %d  (%.1f%%)" % (summary["accepted"],
                                                summary["accepted_pct"]),
             "  first attempt  %d" % summary["first_attempt"],
             "  findings       %d -> %d  (%.1f%% removed)"
             % (summary["findings_before"], summary["findings_after"],
                summary["findings_removed_pct"]),
             "  seconds/unit   %.2f  (%.1fs total)"
             % (summary["seconds_per_unit"], summary["seconds_total"])]
    if summary["rejected_by"]:
        lines += ["", "  rejected by:"]
        for reason, count in summary["rejected_by"].items():
            lines.append("    %-34s %d" % (reason, count))
    lines += ["",
              "  A pass rate is not a quality score. Every accepted rewrite kept",
              "  every number, date, path and quotation in its passage and lost",
              "  the tell it was sent to remove. Nothing here checks grammar, and",
              "  nothing here knows whether the result sounds like you."]
    return "\n".join(lines)


def main():
    ap = cli_error.LLMArgumentParser(
        prog="bench.py",
        description="Score a model against the rewrite gate over a fixed battery.")
    ap.add_argument("--model-endpoint", metavar="URL",
                    help="OpenAI-compatible base URL. Without it, the nearest "
                         ".rabbit-model decides")
    ap.add_argument("--model-name", metavar="NAME", help="model to ask for")
    ap.add_argument("--attempts", type=int, default=3,
                    help="tries per passage before giving up (default 3)")
    ap.add_argument("--repeat", type=int, default=1,
                    help="run the whole battery N times (default 1). One pass "
                         "over a dozen cases is not a stable rate")
    ap.add_argument("--case", metavar="ID", action="append",
                    help="only this case id, repeatable")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output, including every rewrite")
    ap.add_argument("--battery", metavar="PATH", default=BATTERY_PATH,
                    help="an alternative battery file")
    args = ap.parse_args()

    overrides = None
    if args.model_endpoint:
        overrides = {"base_url": args.model_endpoint,
                     "model": args.model_name or "local"}
    endpoint, note = endpoint_mod.resolve(None, overrides)
    if endpoint is None:
        print(cli_error.format_llm_error(
            "bench.py", "no usable model endpoint: %s" % note, parser=ap,
            examples=["python3 bench.py --model-endpoint "
                      "http://127.0.0.1:8080/v1 --model-name qwen3-1.7b"]),
            file=sys.stderr)
        return 2

    try:
        battery = load_battery(args.battery)
    except (OSError, ValueError) as exc:
        print(cli_error.format_file_error(
            "bench.py", args.battery, "--battery",
            expected_type="battery JSON file", details=str(exc)),
            file=sys.stderr)
        return 2

    cases = battery["cases"]
    if args.case:
        wanted = set(args.case)
        cases = [c for c in cases if c["id"] in wanted]
        missing = wanted - {c["id"] for c in cases}
        if missing:
            print(cli_error.format_llm_error(
                "bench.py", "no case named %s in %s"
                % (", ".join(sorted(missing)), args.battery), parser=ap),
                file=sys.stderr)
            return 2

    floor = scan_mod.BANDS["burstiness"][0]
    started = time.monotonic()
    results = []
    for _pass in range(max(1, args.repeat)):
        for case in cases:
            results.append(run_case(case, endpoint, args.attempts, floor))
    elapsed = time.monotonic() - started

    summary = summarize(results, elapsed)
    if args.json:
        print(json.dumps({"endpoint": endpoint.describe(),
                          "battery_version": battery.get("version"),
                          "repeat": args.repeat,
                          "attempts": args.attempts,
                          "summary": summary,
                          "cases": results}, indent=2))
    else:
        print(report(summary, endpoint, battery.get("version"), args.repeat))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Load test module: N runs of the main script, timing stats, degradation,
memory-leak detection (peak RSS per run) and hang detection."""

import statistics

from modules.sandbox import exec_result  # noqa: F401  (contract reference)


def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


class LoadTest:
    name = "load"
    title = {"ru": "Нагрузочный тест", "en": "Load test"}

    def run(self, ctx):
        t = ctx.t
        checks = []
        script = ctx.main_script
        if script is None:
            checks.append(_check("main_script_found", "warn",
                                 t("check.main_script_found.none")))
            return {"module": self.name, "status": "warn", "checks": checks,
                    "details": t("check.main_script_found.none")}
        checks.append(_check("main_script_found", "pass",
                             t("check.main_script_found.ok", name=script.name)))

        n = ctx.load_n
        times, rss = [], []
        hangs = 0
        for _ in range(n):
            r = ctx.sandbox.run_script(script)
            ctx.run_outputs.append(r)
            times.append(r["duration_ms"] / 1000.0)
            rss.append(r["rss_kb"])
            if r["timed_out"]:
                hangs += 1

        # 1. runs completed
        if hangs:
            checks.append(_check("runs_completed", "fail",
                                 t("check.runs_completed.fail", hangs=hangs, n=n)))
        else:
            checks.append(_check("runs_completed", "pass",
                                 t("check.runs_completed.ok", n=n)))

        # 2. timing stats
        stats = {
            "min": min(times),
            "avg": sum(times) / len(times),
            "max": max(times),
            "median": statistics.median(times),
        }
        checks.append(_check("timing_stats", "pass",
                             t("check.timing_stats.ok", **{k: round(v, 3)
                                                           for k, v in stats.items()})))

        # 3. no degradation: avg(last5) > 1.5 * avg(first5) -> fail
        first5, last5 = times[:5], times[-5:]
        f_avg = sum(first5) / len(first5)
        l_avg = sum(last5) / len(last5)
        if f_avg > 0 and l_avg > 1.5 * f_avg:
            checks.append(_check("no_degradation", "fail",
                                 t("check.no_degradation.fail",
                                   first=round(f_avg, 3), last=round(l_avg, 3))))
        elif max(times) > 3 * stats["median"]:
            checks.append(_check("no_degradation", "warn",
                                 t("check.no_degradation.warn")))
        else:
            checks.append(_check("no_degradation", "pass",
                                 t("check.no_degradation.ok")))

        # 4. no memory leak: RSS(last5) avg > 120% of RSS(first5) avg -> fail
        usable = [x for x in rss if x is not None]
        if len(usable) < 5:
            checks.append(_check("no_memory_leak", "warn",
                                 t("check.no_memory_leak.unavailable")))
        else:
            f5 = sum(usable[:5]) / 5
            l5 = sum(usable[-5:]) / 5
            if f5 > 0 and l5 > 1.2 * f5:
                checks.append(_check("no_memory_leak", "fail",
                                     t("check.no_memory_leak.fail",
                                       first=int(f5), last=int(l5))))
            else:
                checks.append(_check("no_memory_leak", "pass",
                                     t("check.no_memory_leak.ok")))

        # 5. hang detected
        if hangs:
            checks.append(_check("hang_detected", "fail",
                                 t("check.hang_detected.fail", hangs=hangs)))
        else:
            checks.append(_check("hang_detected", "pass",
                                 t("check.hang_detected.ok")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        rows = [f"  run {i + 1}: {times[i]:.3f}s, rss={rss[i]} kB"
                for i in range(len(times))]
        details += "\n" + "\n".join(rows)
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}

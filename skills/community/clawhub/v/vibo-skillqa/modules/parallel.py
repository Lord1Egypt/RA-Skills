"""Parallel test module: N concurrent instances of the main script.

Detects deadlocks (processes that never finish within timeout*2), shared
temp-file write conflicts, missing unique temp files and runaways.
Runs only when --parallel is passed on the command line.
"""

import re


def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


CONFLICT_RE = re.compile(
    r"FileExistsError|PermissionError|locked|already exists|resource busy", re.I)


class ParallelTest:
    name = "parallel"
    title = {"ru": "Параллельный запуск", "en": "Parallel run"}

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

        n = ctx.parallel_n
        results = ctx.sandbox.run_many(script, n, timeout=ctx.timeout * 2)
        for r in results:
            ctx.run_outputs.append(r)

        # 1. all finished (deadlock/hang detection)
        if any(r["timed_out"] for r in results):
            checks.append(_check("all_finished", "fail",
                                 t("check.all_finished.fail", n=n)))
        else:
            checks.append(_check("all_finished", "pass",
                                 t("check.all_finished.ok", n=n)))

        # 2. exit codes
        codes = [r["exit_code"] for r in results]
        ok = sum(1 for c in codes if c == 0)
        if ok == n:
            checks.append(_check("exit_codes_ok", "pass",
                                 t("check.exit_codes_ok.ok", n=n)))
        elif ok > 0:
            checks.append(_check("exit_codes_ok", "warn",
                                 t("check.exit_codes_ok.warn", ok=ok, n=n)))
        else:
            checks.append(_check("exit_codes_ok", "fail",
                                 t("check.exit_codes_ok.fail", n=n)))

        # 3. unique temp files per instance (or distinguishable outputs)
        created_any = False
        for i in range(n):
            d = ctx.sandbox.tmp_root / f"par_{i}"
            try:
                if any(d.iterdir()):
                    created_any = True
            except OSError:
                pass
        outputs_differ = len({r["stdout"] + r["stderr"] for r in results}) > 1
        if created_any or outputs_differ:
            checks.append(_check("unique_tmp_files", "pass",
                                 t("check.unique_tmp_files.ok")))
        else:
            checks.append(_check("unique_tmp_files", "warn",
                                 t("check.unique_tmp_files.warn")))

        # 4. no write conflicts
        conflicts = [c for r in results for c in CONFLICT_RE.findall(r["stderr"])]
        if conflicts:
            checks.append(_check("no_conflicts", "fail",
                                 t("check.no_conflicts.fail",
                                   items=", ".join(sorted(set(conflicts))))))
        else:
            checks.append(_check("no_conflicts", "pass",
                                 t("check.no_conflicts.ok")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        rows = [f"  instance {i + 1}: exit={results[i]['exit_code']}, "
                f"{results[i]['duration_ms']} ms, timed_out={results[i]['timed_out']}"
                for i in range(n)]
        details += "\n" + "\n".join(rows)
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}

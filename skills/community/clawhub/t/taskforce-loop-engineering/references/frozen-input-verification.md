# Frozen-input verification

## Configure and prove prerequisites

Use this opt-in backend only on Linux with `python3`, `bwrap`, and `strace` supporting `--decode-pids=pidns`. Missing capabilities fail closed; never silently substitute ordinary verification.

Configure `worktree.isolatedVerification` beside `worktree.verifyCommands`:

```json
{
  "worktree": {
    "enabled": true,
    "verifyCommands": ["python3 -m unittest discover -s tests"],
    "isolatedVerification": {
      "inputs": ["src", "tests", "pyproject.toml"],
      "runtimeFiles": []
    }
  }
}
```

Declare exact project files or recursive directories. Missing inputs, symlinks and special files fail closed; exclude generated outputs. Required user-local runtime files must be exact regular files under `/home` or `/opt`. Do not weaken the allowlist to admit a temporary runtime under `/tmp`.

Project inputs are frozen read-only at `/work`; `/out` is persistent writable output. Network and inherited home/proxy/Node options are unavailable. Input identity covers content, size and permissions, including executable bits. Require stable source, snapshot and tool identities and the same input digest across commands.

## Inspect receipts, not only command exit

Inspect each host-owned trace and `terminal.json`, command and supervisor exits, declared reads, input stability and process-group cleanup. Missing, malformed, stale or failed receipts mean `verify_failed` even if the command swallowed an error or exited zero. A sandbox receipt, checkpoint acceptance and final task judgement are separate evidence levels.

Before making this backend mandatory, prove the project's real command and dependencies with declared-input positive controls and existing-undeclared-input negative controls. Browser profiles, directory toolchains, Docker/Git replay and networked checks need a separately reviewed project-specific gate.

## Path-audit boundaries

- Pair existing undeclared files with genuinely absent optional files. Optional absence may pass; swallowing an existing undeclared access must not. Include failed stat/access/exec prechecks, not only opens.
- Track nested cwd, chdir/fchdir, child inheritance and directory descriptors. PID-namespace decoding is required to associate child traces correctly. Include C-escaped non-ASCII, quotes and backslashes; unresolved or truncated paths fail closed.
- Preserve raw components. Missing/non-directory ancestors before `..` and trailing slashes retain traversal semantics. Repeated slashes and re-entry into `/work` must not bypass auditing.
- Distinguish explicit sandbox mount roots from unknown internal symlinks: a host `/bin` symlink can be a directory at its read-only mount destination. Pair missing and existing undeclared probes across these roots.
- Resolve proven `/proc/self/cwd`, `/proc/thread-self/cwd` and self-root aliases using traced cwd or sandbox root, retaining raw suffixes. Unknown process/fd aliases, including `/dev/fd`, and unresolved internal symlink traversal remain conservative failures; legitimate optional accesses may be rejected.

This is bounded trace auditing, not unrestricted syscall/procfs emulation. A missed attempted-access audit is not by itself proof of hidden-content exposure. Run paired controls through the real sandbox and disposable queue; record isolation and final task verdicts independently. Keep local tests, exact-HEAD remote CI and live deployment claims separate.

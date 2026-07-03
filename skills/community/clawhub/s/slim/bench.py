"""Reproducible benchmark on REAL command output from this machine.

Runs each command, measures two things per case:
  * lossless: ANSI/whitespace/dedupe only (slim_text) - never drops content
  * full:     the dispatched plugin (may clamp giant dumps head+tail)

Token figures are estimates (chars/4) and labelled as such. Run:
    python3 bench.py
"""
import subprocess

from slim.core import slim_text
from slim.plugins import apply
from slim.report import measure

CONEXUS = "/home/workloft/conexus"
HOME = "/home/workloft"

CASES = [
    ("git log -p -8", "git log -p -8", CONEXUS),
    ("cat package-lock.json", "cat package-lock.json", CONEXUS),
    ("npm ls --all", "npm ls --all", CONEXUS),
    ("pip list -v", "pip list -v", HOME),
    ("git diff HEAD~3", "git diff HEAD~3", CONEXUS),
]


def run(cmd: str, cwd: str) -> str:
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return p.stdout + p.stderr


def main() -> None:
    rows = []
    tot_raw = tot_loss = tot_full = 0
    for label, cmd, cwd in CASES:
        raw = run(cmd, cwd)
        if not raw:
            continue
        loss = slim_text(raw)
        full = apply(raw, command=cmd)
        ml = measure(raw, loss)
        mf = measure(raw, full)
        rows.append((label, ml, mf))
        tot_raw += len(raw)
        tot_loss += len(loss)
        tot_full += len(full)

    print(f"| {'command':<22} | raw chars | lossless % | full slim % | "
          f"~tok raw->full |")
    print(f"| {'-'*22} | --------: | ---------: | ----------: | ------------: |")
    for label, ml, mf in rows:
        print(f"| {label:<22} | {ml['chars_before']:>9} | "
              f"{ml['pct_chars_saved']:>9}% | {mf['pct_chars_saved']:>10}% | "
              f"~{mf['est_tokens_before']}->~{mf['est_tokens_after']} |")

    loss_pct = round((tot_raw - tot_loss) / tot_raw * 100, 1)
    full_pct = round((tot_raw - tot_full) / tot_raw * 100, 1)
    print()
    print(f"TOTAL raw chars      : {tot_raw}")
    print(f"lossless-only saved  : {loss_pct}%  ({tot_raw}->{tot_loss})")
    print(f"full slim saved      : {full_pct}%  ({tot_raw}->{tot_full})")
    print(f"est tokens raw->full : ~{round(tot_raw/4)} -> ~{round(tot_full/4)} "
          f"(estimate, chars/4)")


if __name__ == "__main__":
    main()

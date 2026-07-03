"""slim CLI.

Two modes:
  * stdin filter:   `some-cmd | slim [--cmd "some-cmd ..."] [--report]`
  * exec wrapper:   `slim [--report] -- some-cmd args...`

`--report` prints a one-line savings summary to stderr; filtered output always
goes to stdout so slim stays composable in a pipe.
"""
import subprocess
import sys

from .plugins import apply
from .report import measure


def _report_line(before: str, after: str) -> str:
    m = measure(before, after)
    return (
        f"slim: {m['chars_before']}->{m['chars_after']} chars "
        f"({m['pct_chars_saved']}% saved), "
        f"~{m['est_tokens_before']}->~{m['est_tokens_after']} est tokens"
    )


def main(argv: list[str], stdin_text: str | None = None) -> tuple[str, str, int]:
    report = "--report" in argv
    argv = [a for a in argv if a != "--report"]

    if "--" in argv:
        i = argv.index("--")
        cmd = argv[i + 1:]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        raw = proc.stdout + proc.stderr
        code = proc.returncode
        hint = " ".join(cmd)
    else:
        hint = None
        if "--cmd" in argv:
            j = argv.index("--cmd")
            hint = argv[j + 1]
        raw = stdin_text if stdin_text is not None else sys.stdin.read()
        code = 0

    out = apply(raw, command=hint)
    err = _report_line(raw, out) if report else ""
    return out, err, code


def cli() -> None:
    out, err, code = main(sys.argv[1:])
    sys.stdout.write(out)
    if err:
        sys.stderr.write(err + "\n")
    sys.exit(code)


if __name__ == "__main__":
    cli()

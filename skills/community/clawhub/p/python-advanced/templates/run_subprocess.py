from __future__ import annotations

import subprocess


def run(cmd: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
        shell=False,
    )


if __name__ == "__main__":
    r = run(["C:\\Windows\\System32\\cmd.exe", "/c", "echo", "hello"])
    print(r.returncode, repr(r.stdout), repr(r.stderr))

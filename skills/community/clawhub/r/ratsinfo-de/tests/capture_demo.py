#!/usr/bin/env python3
"""Record a real session for the demo video. Nothing here is staged."""
import json, os, subprocess, time

os.environ["RATSINFO_MIN_INTERVAL"] = "0"
os.environ["RATSINFO_CACHE"] = "/tmp/ratsinfo-demo-cache"
subprocess.run(["rm", "-rf", "/tmp/ratsinfo-demo-cache"])

OK = "http://127.0.0.1:8799/system"
BAD = "http://127.0.0.1:8798"
R = ["python3", "scripts/ratsinfo.py"]

def town(port, name, ags):
    env = dict(os.environ, MOCK_PORT=str(port), MOCK_TOWN=name, MOCK_AGS=ags)
    return subprocess.Popen(["python3", "tests/mock_ris.py"], env=env)


servers = [
    town(8799, "Stadt Musterhausen", "05124000"),
    town(8801, "Stadt Beispielstadt", "05158000"),
    town(8802, "Gemeinde Musterdorf", "05170032"),
    subprocess.Popen(["python3", "tests/mock_broken.py"]),
]
open("/tmp/eps.txt", "w").write(
    "http://127.0.0.1:8799/system\n"
    "http://127.0.0.1:8801/system\n"
    "http://127.0.0.1:8802/system\n"
    "http://127.0.0.1:8798/dead\n"
)
time.sleep(1.2)

commands = [
    R + ["check", OK],
    R + ["papers", OK, "--term", "Sanierung"],
    R + ["track", "http://127.0.0.1:8799/paper/0"],
    R + ["watch", OK, "--term", "Sanierung"],
    R + ["check", BAD + "/dead"],
    R + ["check", BAD + "/blocked"],
    R + ["get", "file:///etc/passwd"],
    R + ["scan", "--endpoints", "/tmp/eps.txt", "--term", "Sanierung",
         "--pdf", "/tmp/markt.pdf", "--logo", "/tmp/aq.png", "--org",
         "ALPHA QUADRAT  Bauplanung und Projektmanagement"],
    R + ["report", "http://127.0.0.1:8799/paper/0", "--pdf", "/tmp/vorlage.pdf",
         "--logo", "/tmp/aq.png", "--org",
         "ALPHA QUADRAT  Bauplanung und Projektmanagement"],
]
out = []
for command in commands:
    proc = subprocess.run(command, capture_output=True, text=True)
    out.append(
        {
            "cmd": " ".join(command),
            "out": (proc.stdout + proc.stderr).rstrip("\n"),
            "rc": proc.returncode,
        }
    )

for server in servers:
    server.terminate()
    server.wait()
time.sleep(1.0)

proc = subprocess.run(["bash", "tests/run_tests.sh"], capture_output=True, text=True)
out.append({"cmd": "bash tests/run_tests.sh", "out": proc.stdout.rstrip("\n"),
            "rc": proc.returncode})

json.dump(out, open("/tmp/session.json", "w"), ensure_ascii=False, indent=1)
for o in out:
    print(f"rc={o['rc']:<3} {len(o['out'].splitlines()):>3} Zeilen  {o['cmd'][:64]}")

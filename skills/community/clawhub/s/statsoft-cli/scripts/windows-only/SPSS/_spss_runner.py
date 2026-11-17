# -*- coding: utf-8 -*-
"""_spss_runner.py - standalone SPSS syntax runner (internal Python engine, no GUI/splash).

Usage:
    python _spss_runner.py <syntax_file.sps>

The .sps path MUST be supplied as the first argument; no hardcoded paths are used.
"""
import sys, os

if len(sys.argv) < 2:
    sys.stderr.write("Usage: python _spss_runner.py <syntax_file.sps>\n")
    sys.exit(2)

sps_file = sys.argv[1]
if not os.path.isfile(sps_file):
    sys.stderr.write("SPSS syntax file not found: " + sps_file + "\n")
    sys.exit(1)

spss_pkg = "C:/Program Files/IBM/SPSS/Statistics/26/Python3/Lib/site-packages"
if spss_pkg not in sys.path: sys.path.insert(0, spss_pkg)
os.environ["PATH"] = "C:/Program Files/IBM/SPSS/Statistics/26/Python3" + os.pathsep + os.environ.get("PATH", "")

import spss

# SPSS 26-27: StartSPSS() runs engine as service (no GUI/splash)
spss.StartSPSS()
print("SPSS v26-27: StartSPSS() backend mode (no GUI)")

print("SPSS engine started (NO GUI, NO SPLASH)")

with open(sps_file, encoding="utf-8", errors="replace") as f:
    syntax = f.read()
try:
    spss.Submit(syntax)
    print("Syntax executed successfully")
except Exception as e:
    sys.stderr.write("SPSS Submit error: " + str(e) + "\n")
    sys.exit(1)

spss.StopSPSS()
print("SPSS engine stopped")

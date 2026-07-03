# -*- coding: utf-8 -*-
import sys, os
spss_pkg = "C:/Program Files/IBM/SPSS/Statistics/26/Python3/Lib/site-packages"
if spss_pkg not in sys.path: sys.path.insert(0, spss_pkg)
os.environ["PATH"] = "C:/Program Files/IBM/SPSS/Statistics/26/Python3" + os.pathsep + os.environ.get("PATH", "")

import spss

# SPSS 26-27: StartSPSS() runs engine as service (no GUI/splash)
spss.StartSPSS()
print("SPSS v26-27: StartSPSS() backend mode (no GUI)")


print("SPSS engine started (NO GUI, NO SPLASH)")

with open("C:/Users/WintoneFileSrv/workbuddy/test_full.sps", encoding="utf-8", errors="replace") as f:
    syntax = f.read()
try:
    spss.Submit(syntax)
    print("Syntax executed successfully")
except Exception as e:
    sys.stderr.write("SPSS Submit error: " + str(e) + "\n")
    sys.exit(1)

spss.StopSPSS()
print("SPSS engine stopped")

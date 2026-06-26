#!/usr/bin/env python3
# Enrich: stock-analysis 8-dim JSON + UZI DCF/Comps/Panel
import subprocess, json, sys
ticker = sys.argv[1]
raw = {'mock': '8-dim from stock-analysis'}  # Deprecated, use collect_deep.py
panel = json.loads(subprocess.check_output(['python3', 'investor_panel.py', ticker]))
dcf = subprocess.check_output(['python3', 'fin_models.py', ticker]).decode()
raw['uzi_panel'] = panel
raw['uzi_dcf'] = dcf
print(json.dumps(raw))

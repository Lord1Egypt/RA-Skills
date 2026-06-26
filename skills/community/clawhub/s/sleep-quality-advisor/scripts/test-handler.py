#!/usr/bin/env python3
import json, subprocess
out=subprocess.check_output(['python3','scripts/handler.py','我最近总是凌晨2点才睡着，早上7点起床，很累'], text=True)
data=json.loads(out)
assert 'sleepAssessment' in data
assert 'medicalAdvice' in data
print('PASS sleep-quality-advisor')

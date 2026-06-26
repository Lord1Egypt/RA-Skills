#!/usr/bin/env python3
"""
Move messages from INBOX to export folders using MOVE command.
Always moves seq 1:N (the first N messages) since they shift after each MOVE.
"""
import imaplib, re, time, sys

HOST = "imap.mail.yahoo.com"
# EDIT THIS: Your Yahoo Mail email address
EMAIL = "your-email@yahoo.com"
PASS = "zgvpnfymmwxebpof"
EXPORT_FOLDERS = ["export1", "export2", "export3"]
BATCH = 1000  # messages per MOVE call

def count(m, folder):
    typ, data = m.status(f'"{folder}"', '(MESSAGES)')
    if typ == 'OK' and data:
        match = re.search(r'MESSAGES (\d+)', str(data))
        if match: return int(match.group(1))
    return 0

m = imaplib.IMAP4_SSL(HOST, 993)
m.login(EMAIL, PASS)

inbox = count(m, "INBOX")
print(f"INBOX: {inbox}", flush=True)

# Find first non-full export folder
target = None
for f in EXPORT_FOLDERS:
    c = count(m, f)
    print(f"{f}: {c}", flush=True)
    if c < 10000:
        target = f
        break

if not target:
    print("All export folders full!", flush=True)
    m.logout()
    sys.exit(1)

print(f"Target: {target}", flush=True)
m.select('"INBOX"', readonly=False)

# Move 10K in batches of BATCH
moved = 0
for i in range(0, 10000, BATCH):
    # Always move seq 1:BATCH (they shift after each move)
    seq_range = f"1:{BATCH}"
    try:
        typ, data = m._simple_command('MOVE', seq_range, target)
        if typ == 'OK':
            moved += BATCH
            print(f"  +{BATCH} -> {target} ({moved} total)", flush=True)
        else:
            print(f"  MOVE failed: {typ} {data}", flush=True)
            break
        time.sleep(3)
    except Exception as e:
        print(f"  Error: {e}", flush=True)
        time.sleep(10)
        # reconnect
        try:
            m.logout()
        except: pass
        m = imaplib.IMAP4_SSL(HOST, 993)
        m.login(EMAIL, PASS)
        m.select('"INBOX"', readonly=False)

time.sleep(3)
inbox_final = count(m, "INBOX")
target_final = count(m, target)
print(f"Done: INBOX={inbox_final}, {target}={target_final}", flush=True)
m.logout()

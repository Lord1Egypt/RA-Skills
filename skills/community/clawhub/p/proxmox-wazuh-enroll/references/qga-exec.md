# QGA execution — running the install in a Windows guest

This skill installs the Wazuh agent *inside* a Windows VM by driving the QEMU guest agent (QGA) from the Proxmox side. No WinRM, no SSH, no GPO — QGA runs your command as `NT AUTHORITY\SYSTEM` with no auth handshake, which is exactly why enrollment works with **no AD credentials** and stays scoped to the one target VM. This file is the minimum execution layer the enrollment recipe needs; read it before `wazuh-agent-enroll.md`.

## On-host vs off-host — pick your transport

- **On the Proxmox host** (you have `qm`): `qm guest exec`. **Preferred** — it blocks and hands you the guest's stdout/stderr and exit code directly, no polling.
- **Off-host** (driving from a Mac/laptop via a Proxmox API token, no `qm`): the REST API — `POST .../agent/exec` then poll `.../agent/exec-status`. Same effect, more parsing (see the control-char gotcha below).

## On-host: `qm guest exec`

Use `cmd /c` for simple, fast operations (download, install, service restart). For anything that needs quoting, base64-encode a PowerShell snippet so quoting can't bite you:

```bash
# simple cmd — instant
sudo qm guest exec <vmid> --timeout 120 -- cmd /c "hostname"

# base64 PowerShell — avoids quoting hell, decodes & runs in-guest
b64=$(printf '%s' '<powershell>' | base64 -w0)
sudo qm guest exec <vmid> --timeout 180 -- \
  powershell.exe -NoProfile -NonInteractive -Command \
  "\$d=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('$b64')); Invoke-Expression \$d" 2>&1
```

## Off-host: REST API variant

Two calls — start, then poll. Each token of the command is its own repeated `command=` arg (no shell splitting on the wire):

```bash
PID=$(curl -sk -H "Authorization: PVEAPIToken=$TOKENID=$SECRET" \
  -X POST "https://$PVE:8006/api2/json/nodes/$NODE/qemu/$VMID/agent/exec" \
  --data-urlencode 'command=cmd' --data-urlencode 'command=/c' --data-urlencode 'command=hostname' \
  | sed -E 's/.*"pid":([0-9]+).*/\1/')

curl -sk -H "Authorization: PVEAPIToken=$TOKENID=$SECRET" \
  "https://$PVE:8006/api2/json/nodes/$NODE/qemu/$VMID/agent/exec-status?pid=$PID"
```

⚠️ **Proxmox returns unescaped control chars in `out-data`**, so `jq` chokes on multiline guest output. Either keep guest output to one clean line, or parse leniently (prints `__RUNNING__` until the command exits, then `__EXITED__` + decoded output):

```python
import sys,re
raw=sys.stdin.buffer.read().decode('utf-8','replace')
ex=re.search(r'"exited"\s*:\s*(\d+)',raw)
if not(ex and ex.group(1)=='1'): print("__RUNNING__"); sys.exit(0)
m=re.search(r'"out-data"\s*:\s*"(.*?)"\s*,\s*"exited"',raw,re.S)
out=m.group(1) if m else ""
try: out=out.encode('utf-8','replace').decode('unicode_escape','replace')
except: pass
print("__EXITED__"); sys.stdout.write(out)
```

## Passing the registration password — over stdin, never on the command line

`qm guest exec` takes `--pass-stdin 1` (REST: `input-data=`). Feed the Wazuh registration password as stdin and read it in-guest with `[Console]::In.ReadLine()`, so it never lands in the process table, the command line, or QGA logs.

```bash
printf '%s\n' "$REG_PW" | sudo qm guest exec <vmid> --timeout 180 --pass-stdin 1 -- \
  powershell.exe -NoProfile -NonInteractive -Command \
  "\$pw=[Console]::In.ReadLine(); <build the msiexec arg list from \$pw and run it>"
```

If you instead write the password to a file in-guest (e.g. `authd.pass`), have the consuming step delete it immediately after use. Never echo the password into chat or logs.

## `cmd` vs PowerShell, and verifying the install

- **PowerShell startup is slow on Defender-heavy / eval VMs** (seconds per call); `cmd /c` is effectively instant. Use `cmd` for the download + `msiexec` + service restart; reach for PowerShell only when you need its cmdlets (e.g. building the stdin-password arg list).
- **8.3 short paths dodge `Program Files (x86)` paren-parsing in `cmd`:** use `C:\PROGRA~2\ossec-agent` rather than the unquoted parenthesized path.
- **Verify the install by exit code, not output.** `msiexec /i ... /qn` returns **0** = success or **3010** = success-reboot-required — treat *both* as success. Read it from `.data.exitcode` (REST) or `$LASTEXITCODE` (PowerShell). A silent install is silent; don't infer success from empty stdout.
- A long install may exceed `--timeout`; QGA then returns a `{"pid":N}` and the work continues in-guest. Don't fire a second attempt on top of it — re-check the first (`Get-Process -Id N`, or the service state) before retrying.

# Workflow Without Local Python

The computer does not need Python for connection, code generation, upload, or execution. Windows uses PowerShell; macOS uses Bash. Both use the OpenSSH client (`ssh` and `scp`). Python, `unihiker`, and `pinpong` run on the M10.

Exception: downloading a missing third-party dependency for an offline M10 requires Python 3 and pip on the Internet-connected computer. See [offline-dependencies.md](offline-dependencies.md).

## Prerequisites

| Computer | M10 |
|---|---|
| Windows 10/11 with PowerShell, or macOS with Bash | Connected over USB or the same Wi-Fi LAN |
| `ping`, `ssh`, and `scp` | SSH enabled |
| No local Python required for normal deployment; Python 3 + pip required for offline dependency downloads | A working Python environment; third-party wheels can be installed offline |

Check OpenSSH in PowerShell:

```powershell
ssh -V
scp
```

If either command is missing, install **OpenSSH Client** under Windows **Settings > Apps > Optional features**.

On macOS, `bash`, `ping`, `ssh`, and `scp` are included with the operating system. See [macos-workflow.md](macos-workflow.md).

## Included PowerShell scripts

```powershell
# Verify the default USB connection.
.\scripts\check_connection.ps1

# Upload and start a persistent display program.
.\scripts\run_on_m10.ps1 .\examples\hello_unihiker.py -Background

# Stop that background program.
ssh root@10.1.2.3 "pkill -f hello_unihiker.py"
```

For Wi-Fi, pass the board's LAN IP:

```powershell
.\scripts\check_connection.ps1 -M10Host 192.168.199.102
.\scripts\run_on_m10.ps1 .\my.py -M10Host 192.168.199.102
```

## Included macOS scripts

```bash
bash scripts/check_connection.sh
bash scripts/run_on_m10.sh examples/hello_unihiker.py --background
ssh root@10.1.2.3 "pkill -f hello_unihiker.py"
```

For Wi-Fi:

```bash
bash scripts/check_connection.sh --host 192.168.199.102
bash scripts/run_on_m10.sh my.py --host 192.168.199.102
```

## Direct SSH and SCP commands

```powershell
ping 10.1.2.3
ssh root@10.1.2.3 "hostname && python3 --version"
scp .\hello.py root@10.1.2.3:/tmp/m10_nl/
ssh root@10.1.2.3 "python3 /tmp/m10_nl/hello.py"
```

Start a persistent program in the background:

```powershell
ssh root@10.1.2.3 "nohup python3 /tmp/m10_nl/hello.py > /tmp/hello.log 2>&1 &"
ssh root@10.1.2.3 "pgrep -af hello.py"
ssh root@10.1.2.3 "cat /tmp/hello.log"
```

Stop it:

```powershell
ssh root@10.1.2.3 "pkill -f hello.py"
```

The factory-default SSH password is `dfrobot`. If it has been changed, use the current password interactively and do not save it in source files.

## Common problems

- Repeated password prompts are normal unless the owner configures SSH keys.
- A `.py` file runs on the M10; it does not run by double-clicking on a computer without Python.
- A GUI program needs a wait or event loop and should normally be deployed with `-Background` on Windows or `--background` on macOS.

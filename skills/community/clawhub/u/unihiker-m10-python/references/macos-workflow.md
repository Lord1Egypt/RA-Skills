# macOS Workflow

Use the `.sh` scripts on macOS. They rely only on the system-provided Bash, `ping`, `ssh`, and `scp` for normal deployment. Python 3 and pip are additionally required on the Mac only when downloading wheels for an offline M10.

## Connect and select Python

```bash
bash scripts/check_connection.sh
bash scripts/detect_python_env.sh --save-env-file .m10-env.json
```

For a Wi-Fi-connected board, add `--host <M10-IP>` to either command. A USB-connected M10 normally uses `10.1.2.3`.

## Deploy

```bash
bash scripts/run_on_m10.sh program.py --env-file .m10-env.json
bash scripts/run_on_m10.sh program.py --env-file .m10-env.json --background
```

Stop a background program with:

```bash
ssh root@10.1.2.3 "pkill -f program.py"
```

## Install a dependency for an offline M10

```bash
python3 -m pip --version
bash scripts/install_m10_package_offline.sh requests --env-file .m10-env.json
```

The Mac's CPU architecture does not determine the downloaded wheel. The script requests Linux `aarch64` wheels matching the selected M10 interpreter, so both Intel and Apple Silicon Macs can prepare the package set.

## macOS notes

- Accept the first SSH host-key prompt when connecting to a new board.
- Enter the current M10 password interactively; `dfrobot` is only the factory default.
- If USB address `10.1.2.3` is unreachable, confirm that the cable supports data and check **System Settings > Network** for the USB network interface.
- Do not use the PowerShell scripts unless PowerShell Core was installed intentionally; the Bash scripts are the supported macOS path.

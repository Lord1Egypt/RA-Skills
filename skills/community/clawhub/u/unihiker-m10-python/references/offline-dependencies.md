# Offline Python Dependencies

Use this workflow when the computer has Internet access but the M10 does not. The downloader asks the computer's `pip` to resolve binary wheels for the M10's detected CPython version, ARM64 architecture, and glibc version. It then uploads the complete wheelhouse over SSH and installs with `--no-index`.

## Install a package

Run from the skill root after connection and environment detection:

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_m10_package_offline.ps1 requests -EnvFile .m10-env.json
powershell -ExecutionPolicy Bypass -File scripts/install_m10_package_offline.ps1 "requests==2.32.4" -EnvFile .m10-env.json
```

macOS:

```bash
bash scripts/install_m10_package_offline.sh requests --env-file .m10-env.json
bash scripts/install_m10_package_offline.sh 'requests==2.32.4' --env-file .m10-env.json
```

The computer needs Python 3 and pip only for this offline-download workflow. The M10 does not need Internet access.

## React to a missing module

When execution reports `ModuleNotFoundError`:

1. Check whether the name refers to a project file that was not uploaded. Upload local modules instead of installing an unrelated PyPI package.
2. Determine the PyPI distribution name. Do not assume it always equals the import name.
3. Run the platform-specific `install_m10_package_offline` script with the selected `.m10-env.json`.
4. Rerun the original program in the same environment.

Common mappings:

| Import | PyPI distribution |
|---|---|
| `PIL` | `Pillow` |
| `yaml` | `PyYAML` |
| `serial` | `pyserial` |
| `sklearn` | `scikit-learn` |
| `cv2` | `opencv-python` or `opencv-python-headless` |

Ask before choosing when multiple distributions plausibly provide the import. Never install a package solely because its name resembles a missing local module.

## Compatibility failures

Only binary wheels are accepted automatically. A filename ending in `win_amd64.whl` is not usable on the M10. Compatible compiled wheels normally contain `aarch64`; pure-Python wheels end in `py3-none-any.whl`.

If no complete wheel set exists, do not force-install it. Pin a compatible release, use a package already bundled in the M10 image, or build wheels on an ARM64 Linux environment with the required system headers.

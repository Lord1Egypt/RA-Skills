# PlatformIO Workshop Notes for UNIHIKER K10

## Why Predownload

The first K10 PlatformIO build downloads DFRobot's PlatformIO platform, the K10 Arduino framework, compiler toolchains, and upload/build tools. The largest pieces are the K10 Arduino framework and ESP32 toolchains. A prepared machine measured these approximate uncompressed sizes:

| Directory | Purpose | Size |
| --- | --- | --- |
| `platforms/unihiker` | DFRobot platform definition | 536 KB |
| `packages/framework-arduinounihiker` | K10 Arduino framework and libraries | 518 MB |
| `packages/toolchain-xtensa-esp32s3` | ESP32-S3 compiler toolchain | 268 MB |
| `packages/toolchain-riscv32-esp` | RISC-V helper toolchain used during K10 builds | can be large |
| `packages/toolchain-xtensa-esp32` | Base ESP32 compiler toolchain declared by platform; include when present for conservative bundles | 387 MB |
| `packages/tool-esptoolpy` | Upload tool | 2.6 MB |
| `packages/tool-scons` | Build tool | 4.9 MB |
| `packages/tool-mkfatfs`, `tool-mklittlefs`, `tool-mkspiffs` | Filesystem image tools for related upload targets | a few MB |

A minimal compressed bundle from only the K10 framework plus Xtensa S3 pieces was about 459 MB on macOS. A conservative workshop bundle that includes every tool used or declared by the K10 platform will be larger. Exact sizes differ by OS and CPU architecture.

## Prepare a Teacher Machine

Install PlatformIO Core, then create a probe project:

```bash
bash scripts/init-k10-platformio-project.sh /tmp/k10-pio-probe
pio run -d /tmp/k10-pio-probe
```

After the build succeeds, create the bundle:

```bash
bash scripts/prepare-offline-bundle.sh /tmp/k10-platformio-bundle.tgz
```

Make one bundle per OS and CPU architecture. Do not share a macOS arm64 bundle with Windows or Linux machines.

## Install on Student Machines

Copy the bundle by USB drive, local file share, or classroom LAN. Then run:

```bash
bash scripts/install-offline-bundle.sh /path/to/k10-platformio-bundle.tgz
bash scripts/doctor-offline.sh
```

If PlatformIO uses a custom core directory, set `PLATFORMIO_CORE_DIR` during installation and during later builds:

```bash
export PLATFORMIO_CORE_DIR="$HOME/.platformio"
bash scripts/install-offline-bundle.sh /path/to/k10-platformio-bundle.tgz
```

## Verify Offline Readiness

Run:

```bash
pio pkg list -g | grep -E 'unihiker|framework-arduinounihiker|xtensa-esp32s3'
bash scripts/doctor-offline.sh
pio run -d /path/to/k10-project
```

The second command should not need to download the K10 platform, K10 framework, or ESP32-S3 toolchain.

## Troubleshooting

If PlatformIO downloads files anyway:

- Confirm the bundle was installed into the active PlatformIO core directory.
- Confirm OS/CPU architecture matches the teacher machine.
- Confirm `platformio.ini` uses the same platform URL or pinned commit used to prepare the bundle.
- Run `pio pkg list -g` and check for `unihiker`, `framework-arduinounihiker`, and `toolchain-xtensa-esp32s3`.
- Check for `toolchain-riscv32-esp` if the first build still tries to download tools.

If the build fails with:

```text
ModuleNotFoundError: No module named 'intelhex'
```

the local PlatformIO Python/tool installation is incomplete. Repair or reinstall PlatformIO Core before the workshop image is used as the source for offline bundles.

If uploads fail:

- Run `pio device list` and pass the serial port with `--upload-port`.
- Check USB cable data capability.
- On Linux, install PlatformIO udev rules and reconnect the board.
- Try the K10 boot/reset procedure if the board is not entering upload mode.

## Pinning for Repeatable Workshops

For a workshop, consider pinning the DFRobot platform to a known commit in `platformio.ini`:

```ini
platform = https://github.com/DFRobot/platform-unihiker.git#508e31875ad92205bf946e28570fb78fc01ceb2e
```

Pinning prevents a later GitHub update from invalidating the prepared cache.

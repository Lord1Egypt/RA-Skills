---
name: unihiker-k10-ota
description: Add HTTP OTA (Over-The-Air) firmware update capability to Unihiker K10 Arduino projects, including AP/STA projects and ESP-NOW projects that need a safe OTA maintenance mode. Use when you need wireless firmware updates without USB cable, when ArduinoOTA fails, or when an ESP-NOW sketch must keep an OTA recovery/update path.
---

# Unihiker K10 - HTTP OTA

## Overview

Enable wireless firmware updates for K10 Arduino projects via HTTP POST.

**Core principle:** K10's default partition table has no OTA partitions. You must switch to a custom partition table with `ota_0` + `ota_1` before `Update.begin()` can work.

**Why not ArduinoOTA?** The standard `ArduinoOTA` library (UDP-based) requires the ESP32 to connect back to the host computer on a random port, which is often blocked by Windows Firewall. HTTP OTA uses a simple host→device upload direction and works reliably on all networks.

**AI model rule:** K10 built-in AI support files live in fixed flash regions beginning at `0x510000`. OTA partitions must end before that address if the project uses voice recognition, TTS, face recognition, or other built-in AI features.

**Screen refresh rule:** OTA status pages, progress indicators, connection state, and voice status should use partial redraws. Full-screen clearing or full-background redraw causes visible flicker on K10; use it only for initialization, page switches, exit cleanup, or when measured full-screen refresh is above 30 fps.

## When to Use

- Your K10 is installed in a location difficult to reach with USB
- You want to update firmware without opening the enclosure
- You need a scriptable/automated deployment pipeline
- ArduinoOTA network port upload fails with "No response from device"

## Prerequisites

- Existing K10 Arduino project with `WebServer` running
- `arduino-cli` installed and K10 BSP (`UNIHIKER:esp32:k10`) available
- Device and computer on the same network (or connected to K10's AP)

## ESP-NOW Compatibility Rule

ESP-NOW sketches can support OTA, but ordinary HTTP OTA requires temporary IP networking through `WIFI_AP`, `WIFI_STA`, or `WIFI_AP_STA`. ESP-NOW itself is not an IP transport, so do not claim that the standard `/ota` HTTP endpoint works over pure ESP-NOW packets.

When adding OTA to an ESP-NOW program, use this policy:

1. Prefer a **maintenance OTA mode**: normal runtime uses ESP-NOW; a button, serial command, saved flag, or received command enters OTA mode, starts AP or STA networking, registers `/ota`, and services `server.handleClient()`.
2. Keep ESP-NOW and WiFi on the same channel if they run together. If STA connects to a router, the router determines the channel; ESP-NOW peers must use that channel or peer channel `0`.
3. For reliability, pause ESP-NOW sends and time-critical control loops while an OTA upload is active.
4. Keep an AP fallback such as `K10-OTA-<id>` available in OTA mode so updates still work when STA credentials are missing or the router changes.
5. Treat pure ESP-NOW firmware transfer as an advanced separate design. It needs packet chunking, acknowledgements, image validation, and writes to OTA partitions; do not replace HTTP OTA with it unless the user explicitly asks for ESP-NOW-only OTA.

See `references/ota-implementation.md` for the ESP-NOW maintenance-mode code pattern.

## Quick Start

### Step 1: Add Custom Partition Table

Create `partitions.csv` in your sketch directory:

```csv
# K10 OTA partition table that preserves speech-recognition model regions.
# Keep model/voice_data/fr offsets aligned with the DFRobot K10 factory table.
# Name,     Type, SubType, Offset,   Size,     Flags
nvs,        data, nvs,     0x9000,   0x5000,
otadata,    data, ota,     0xe000,   0x2000,
app0,       app,  ota_0,   0x10000,  0x280000,
app1,       app,  ota_1,   0x290000, 0x280000,
model,      data, spiffs,  0x510000, 4563K,
voice_data, data, fat,     0x985000, 2542K,
fr,         data, ,        0xC01000, 100K,
coredump,   data, coredump,,         1K,
spiffs,     data, spiffs,  0xC1B000, 0x3E5000,
```

Compile with the custom partition:

```bash
arduino-cli compile --fqbn UNIHIKER:esp32:k10 . \
  --output-dir build \
  --build-property "build.partitions=custom"
```

Optional speed-up for repeated compiles:

```bash
# Use all CPU cores and keep build artifacts in stable project-local folders.
arduino-cli compile --fqbn UNIHIKER:esp32:k10 . \
  --build-path .arduino-build \
  --output-dir build \
  --build-property "build.partitions=custom" \
  -j 0
```

Arduino CLI already has a built-in `build_cache`. To use a longer-lived cache, configure the official `build_cache.*` keys rather than `compiler.cache.*`:

```bash
arduino-cli config set build_cache.path ~/.cache/arduino-build-cache
arduino-cli config set build_cache.compilations_before_purge 0
```

On Windows PowerShell:

```powershell
arduino-cli config set build_cache.path "$env:LOCALAPPDATA\arduino\build-cache"
arduino-cli config set build_cache.compilations_before_purge 0
```

### Step 2: Add OTA Endpoint to Firmware

Include the `Update` library and add a POST handler:

```cpp
#include <Update.h>

void handleOta() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/plain", Update.hasError() ? "FAIL" : "OK");
  if (!Update.hasError()) {
    ESP.restart();  // or schedule a delayed restart
  }
}

void handleOtaUpload() {
  HTTPUpload &upload = server.upload();
  if (upload.status == UPLOAD_FILE_START) {
    if (!Update.begin(UPDATE_SIZE_UNKNOWN)) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_WRITE) {
    if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_END) {
    if (Update.end(true)) {
      Serial.printf("OTA Success: %u bytes\n", upload.totalSize);
    } else {
      Update.printError(Serial);
    }
  }
}

// In setup() or startNetwork():
server.on("/ota", HTTP_POST, handleOta, handleOtaUpload);
```

For ESP-NOW sketches, do not leave OTA as an afterthought. Add an explicit OTA mode gate:

```cpp
bool otaMode = false;
bool otaUploadActive = false;

void enterOtaMode() {
  otaMode = true;
  WiFi.mode(WIFI_AP_STA);  // AP fallback plus optional STA
  WiFi.softAP("K10-OTA", "12345678");
  // Optional: WiFi.begin(savedSsid, savedPassword);
  server.on("/ota", HTTP_POST, handleOta, handleOtaUpload);
  server.begin();
}

void loop() {
  if (otaMode) {
    server.handleClient();
    return;  // keep ESP-NOW/control traffic paused during OTA maintenance
  }

  // normal ESP-NOW runtime
}
```

### Step 3: First USB Upload (Required Once)

The first upload must be via USB to flash the new partition table:

```bash
arduino-cli upload -p COM4 --fqbn UNIHIKER:esp32:k10 .
```

### Step 4: Update Over WiFi

After the first USB upload, use any of these methods:

**curl:**
```bash
curl -F "file=@build/your_sketch.ino.bin" http://192.168.9.42/ota
```

**Python script (works on Windows, macOS, and Linux):**
```bash
python scripts/ota_upload.py build/your_sketch.ino.bin --ip 192.168.9.42
```

**PowerShell 7+ (works on Windows, macOS, and Linux):**
```powershell
pwsh ./scripts/ota_upload.ps1 -Bin build/your_sketch.ino.bin -Ip 192.168.9.42
```

## Important Notes

- **Partition change erases flash layout.** The first USB upload after adding `partitions.csv` will reformat the flash partition table. `Preferences` / NVS data may be lost.
- **Every OTA-enabled sketch must include the OTA code.** If you upload a sketch without `/ota` handler, you lose OTA capability and must return to USB.
- **Do not use `delay()` in `loop()` for long periods.** Use non-blocking `millis()` patterns so the WebServer can process the upload request.
- **Content-Length:** Arduino WebServer's `server.header("Content-Length")` does not work in POST handlers. Use `server.clientContentLength()` instead if you need the raw body size.
- **Compile cache:** Use Arduino CLI's official `build_cache.*` settings and `--build-path` for repeat builds. Do not document `compiler.cache.enable`, `compiler.cache.path`, or `ccache` as required OTA setup because they are not part of the current Arduino CLI configuration reference.
- **ESP-NOW:** HTTP OTA needs AP/STA networking. If the program uses ESP-NOW, add an OTA maintenance mode, manage WiFi channel alignment, and pause ESP-NOW traffic while flashing.
- **AI model regions:** Do not let OTA app partitions overlap `model` at `0x510000`, `voice_data` at `0x985000`, or `fr` at `0xC01000`. A generic large OTA layout can erase AI support data.
- **Model recovery:** If AI functions reboot or model data is suspected damaged, use Mind+ `Restore Initial Settings` or a one-time USB upload with the Arduino/PlatformIO CN/EN model refresh option. A full erase plus `Model=None` does not restore model files.
- **Display refresh:** Do not clear and redraw the whole K10 screen in `loop()` just to update OTA/WiFi progress. Draw static labels once, then overwrite only changed values or progress areas before one display update call.

## Files

```
unihiker-k10-ota/
├── SKILL.md                           # This file
├── references/
│   └── ota-implementation.md          # Detailed implementation guide
└── scripts/
    ├── ota_upload.py                  # Python OTA uploader
    └── ota_upload.ps1                 # PowerShell OTA uploader
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `BEGIN_FAIL` | No OTA partitions in partition table | Add `partitions.csv` with `ota_0` + `ota_1` and reflash via USB |
| `FAIL` after upload | `Update.write()` failed mid-stream | Check serial log; likely flash write error or insufficient space |
| `NO_CONTENT` | `Content-Length` header missing | Ensure client sends valid `multipart/form-data` with file data |
| Device does not restart | `ESP.restart()` called before response sent | Use `scheduleRestart()` with a small delay instead |
| Network port not found | mDNS/ArduinoOTA not running | HTTP OTA does not need network port detection; use the device's IP directly |
| ESP-NOW works until STA starts | STA changed the radio channel to the router channel | Put peers on the same channel or use peer channel `0` after STA connects |
| OTA page unreachable in ESP-NOW sketch | Sketch never entered AP/STA maintenance mode | Add a button/serial/command path that calls `enterOtaMode()` and starts the WebServer |
| ESP-NOW packets drop during OTA | Flashing and HTTP handling are competing with runtime traffic | Pause ESP-NOW sends/control loops while `otaUploadActive` or `otaMode` is true |

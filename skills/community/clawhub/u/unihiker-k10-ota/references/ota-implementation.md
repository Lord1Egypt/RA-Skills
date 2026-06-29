# K10 HTTP OTA Implementation Guide

Screen refresh rule: if the firmware displays OTA progress, WiFi state, IP addresses, voice state, or other status on the K10 screen, update only changed regions. Do not clear and redraw the whole screen in `loop()` unless full-screen refresh is measured above 30 fps; otherwise the display will visibly flicker.

## Table of Contents

1. [Why HTTP OTA Instead of ArduinoOTA](#why-http-ota)
2. [Partition Table Requirements](#partition-table)
3. [Firmware Code Changes](#firmware-code)
4. [ESP-NOW Projects](#esp-now-projects)
5. [Build and Upload Workflow](#build-upload)
6. [OTA Update Workflow](#ota-update)
7. [Reference: Complete Minimal Example](#minimal-example)

---

## Why HTTP OTA Instead of ArduinoOTA

`ArduinoOTA` uses a UDP-based protocol:
1. Host sends an authentication challenge to the device (port 3232)
2. Device verifies password
3. **Device opens a TCP connection back to the host** on a random port
4. Host streams the firmware over this reverse connection

Step 3 is the failure point on Windows because:
- Windows Defender Firewall blocks inbound connections from the ESP32
- No admin privileges available to add firewall rules
- `arduino-cli` network upload cannot pass the password non-interactively

HTTP OTA flips the direction:
- Host opens a TCP connection **to** the device (outbound — always allowed)
- Host POSTs the firmware as `multipart/form-data`
- Device receives and writes to flash using the `Update` library

---

## Partition Table Requirements

The K10 BSP (`UNIHIKER:esp32` v0.0.3) ships with `large_spiffs_16MB.csv`:

```csv
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x5000,
factory,  app,  factory, 0x10000, 0x500000,
model,    data, spiffs,  0x510000,4563k,
voice_data,data, fat,    0x985000,2542k,
fr,       data, ,        0xC01000,100K,
coredump, data, coredump,,        1K,
```

**Problem:** There is no `ota_0` / `ota_1` / `otadata` partition. `Update.begin()` fails immediately because it cannot find an inactive OTA slot to write to.

**Solution for K10 AI projects:** Create `partitions.csv` in your sketch directory with OTA partitions that stop before the model region:

```csv
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

- `app0` and `app1` are each 2.5 MB and end before `0x510000`
- `otadata` is required for the bootloader to know which app partition to boot from
- `model`, `voice_data`, and `fr` keep the factory offsets used by the K10 AI libraries
- `spiffs` is moved after the model regions

**Compile with the custom partition:**

```bash
arduino-cli compile --fqbn UNIHIKER:esp32:k10 . \
  --output-dir build \
  --build-property "build.partitions=custom"
```

The first USB upload after this change will write the new partition table to flash. This is a one-time operation.

If the firmware image no longer fits in 2.5 MB, do not expand `app0` or `app1` over the model regions in an AI project. Reduce firmware size, drop OTA, or explicitly decide that the program will not use built-in AI model data.

---

## Optional: Speed Up Repeated Compiles

Arduino CLI has its own build cache. The reliable, current configuration keys are under `build_cache.*`:

```bash
# Linux/macOS
arduino-cli config set build_cache.path ~/.cache/arduino-build-cache
arduino-cli config set build_cache.compilations_before_purge 0
```

```powershell
# Windows PowerShell
arduino-cli config set build_cache.path "$env:LOCALAPPDATA\arduino\build-cache"
arduino-cli config set build_cache.compilations_before_purge 0
```

For project-local repeat builds, keep the intermediate build folder stable and let Arduino CLI use all CPU cores:

```bash
arduino-cli compile --fqbn UNIHIKER:esp32:k10 . \
  --build-path .arduino-build \
  --output-dir build \
  --build-property "build.partitions=custom" \
  -j 0
```

Use `--clean` only when you need a full rebuild; it deliberately bypasses cached build artifacts.

`ccache` can help in some C/C++ toolchains, but it is not a documented Arduino CLI configuration path in current releases. Avoid treating these as standard Arduino CLI settings:

```bash
arduino-cli config set compiler.cache.enable true
arduino-cli config set compiler.cache.path /path/to/ccache
```

The current Arduino CLI command reference also does not list `compile --build-cache-path`, so prefer persistent `build_cache.path` configuration plus a stable `--build-path`.

---

## Firmware Code Changes

### 1. Include Update Library

```cpp
#include <Update.h>
```

### 2. Add Upload Handler

Use the **four-argument** `server.on()` overload to register both a final handler and an upload-progress handler:

```cpp
void handleOta() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/plain", Update.hasError() ? "FAIL" : "OK");
  if (!Update.hasError()) {
    scheduleRestart("OTA update done");  // or ESP.restart()
  }
}

void handleOtaUpload() {
  HTTPUpload &upload = server.upload();

  if (upload.status == UPLOAD_FILE_START) {
    Serial.printf("OTA: %s\n", upload.filename.c_str());
    if (!Update.begin(UPDATE_SIZE_UNKNOWN)) {
      Update.printError(Serial);
    }
  }
  else if (upload.status == UPLOAD_FILE_WRITE) {
    if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
      Update.printError(Serial);
    }
  }
  else if (upload.status == UPLOAD_FILE_END) {
    if (Update.end(true)) {
      Serial.printf("OTA Success: %u bytes\n", upload.totalSize);
    } else {
      Update.printError(Serial);
    }
  }
}
```

### 3. Register the Route

```cpp
server.on("/ota", HTTP_POST, handleOta, handleOtaUpload);
```

### 4. Restart Scheduling (Recommended)

Restarting immediately inside the handler can cut off the HTTP response. Use a delayed restart:

```cpp
bool restartPending = false;
uint32_t restartAtMs = 0;

void scheduleRestart(const String &message) {
  restartPending = true;
  restartAtMs = millis() + 1200;  // 1.2s delay
}

void loop() {
  // ... existing loop code ...
  if (restartPending && millis() >= restartAtMs) {
    ESP.restart();
  }
}
```

---

## ESP-NOW Projects

HTTP OTA can coexist with ESP-NOW, but not as a pure ESP-NOW transport. The OTA web endpoint needs an IP interface, so an ESP-NOW sketch must temporarily enable AP, STA, or AP+STA networking while accepting the firmware upload.

### Recommended Pattern: OTA Maintenance Mode

Use normal runtime for ESP-NOW. Enter OTA mode only when needed:

- Button long press during boot or runtime
- Serial command such as `ota`
- Saved `Preferences` flag set by a previous command
- Trusted ESP-NOW command from a controller node
- Local web/admin command if the sketch already has a WebServer

In OTA mode:

1. Stop or pause periodic ESP-NOW sends.
2. Start `WIFI_AP` or `WIFI_AP_STA`.
3. Start the WebServer and register `/ota`.
4. Call `server.handleClient()` frequently.
5. Mark `otaUploadActive = true` during upload writes.
6. Restart after a successful update.

Minimal pattern:

```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <Update.h>
#include <esp_now.h>

WebServer server(80);

bool otaMode = false;
bool otaUploadActive = false;
bool restartPending = false;
uint32_t restartAtMs = 0;

void scheduleRestart() {
  restartPending = true;
  restartAtMs = millis() + 1200;
}

void handleOta() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/plain", Update.hasError() ? "FAIL" : "OK");
  if (!Update.hasError()) {
    scheduleRestart();
  }
}

void handleOtaUpload() {
  HTTPUpload &upload = server.upload();

  if (upload.status == UPLOAD_FILE_START) {
    otaUploadActive = true;
    if (!Update.begin(UPDATE_SIZE_UNKNOWN)) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_WRITE) {
    if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_END) {
    if (!Update.end(true)) {
      Update.printError(Serial);
    }
    otaUploadActive = false;
  } else if (upload.status == UPLOAD_FILE_ABORTED) {
    Update.abort();
    otaUploadActive = false;
  }
}

void enterOtaMode() {
  otaMode = true;

  // Prefer an AP fallback so OTA still works when router credentials are wrong.
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP("K10-OTA", "12345678");

  // Optional: also connect to infrastructure WiFi.
  // WiFi.begin(savedSsid, savedPassword);

  server.on("/ota", HTTP_POST, handleOta, handleOtaUpload);
  server.begin();

  Serial.print("OTA AP IP: ");
  Serial.println(WiFi.softAPIP());
}

void setup() {
  Serial.begin(115200);

  // Example gate: hold a button at boot, read Preferences, or parse Serial.
  bool requestedOtaMode = false;

  if (requestedOtaMode) {
    enterOtaMode();
    return;
  }

  WiFi.mode(WIFI_STA);
  // Set channel before esp_now_init() if the deployment uses a fixed ESP-NOW channel.
  // esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  esp_now_init();
}

void loop() {
  if (otaMode) {
    server.handleClient();
    if (restartPending && millis() >= restartAtMs) {
      ESP.restart();
    }
    return;
  }

  if (!otaUploadActive) {
    // Normal ESP-NOW runtime here.
  }
}
```

### Channel Rules

ESP-NOW and WiFi share one 2.4 GHz radio:

- If the device is only in `WIFI_STA` and does not connect to a router, set a fixed channel before `esp_now_init()`.
- If STA connects to a router, the router decides the channel. ESP-NOW peers must use that same channel.
- Peer channel `0` means "use the current WiFi channel" and is useful when the local device follows the AP/STA channel.
- Avoid hidden channel changes while ESP-NOW peers are active; reconnecting STA may move the radio and break peers on the old channel.

For K10 OTA work, prefer this practical rule: in normal ESP-NOW mode use a known channel; in OTA maintenance mode pause ESP-NOW and allow AP/STA networking to own the radio.

### Pure ESP-NOW OTA

Pure ESP-NOW OTA is possible but should be treated as a separate advanced feature, not the default for this skill. It requires:

- Firmware chunking small enough for ESP-NOW payload limits
- Sequence numbers and acknowledgements
- Retry, resume, and timeout handling
- Image size and checksum validation before boot switch
- Writes through `Update` or ESP-IDF OTA APIs into the inactive OTA partition
- A secure authorization model so arbitrary peers cannot flash the device

Use pure ESP-NOW OTA only when the user explicitly needs updates without AP/STA IP networking. Otherwise, use HTTP OTA maintenance mode.

---

## Build and Upload Workflow

### Initial Setup (USB Required)

```bash
# Compile with custom partition table
arduino-cli compile --fqbn UNIHIKER:esp32:k10 . \
  --build-path .arduino-build \
  --output-dir build \
  -j 0 \
  --build-property "build.partitions=custom"

# Upload via USB (also flashes the new partition table)
arduino-cli upload -p COM4 --fqbn UNIHIKER:esp32:k10 .
```

Use the serial port name for your operating system:

| OS | Example port |
|----|--------------|
| Windows | `COM4` |
| macOS | `/dev/cu.usbmodem1101` |
| Linux | `/dev/ttyACM0` |

### Subsequent Updates (WiFi OTA)

```bash
# Compile only
arduino-cli compile --fqbn UNIHIKER:esp32:k10 . --build-path .arduino-build --output-dir build -j 0

# Upload via HTTP with curl
curl -F "file=@build/your_sketch.ino.bin" http://192.168.9.42/ota

# Or use the cross-platform Python uploader
python scripts/ota_upload.py build/your_sketch.ino.bin --ip 192.168.9.42
```

---

## OTA Update Workflow

1. **Ensure the device is running an OTA-enabled sketch** (has `/ota` endpoint)
2. **Get the device IP** from the web UI, serial output, or router
3. **Compile** the new firmware
4. **POST the `.bin` file** to `http://<ip>/ota`
5. **Wait for `OK` response** (~5–10 seconds for a 1.1 MB firmware)
6. **Device restarts automatically** after a short delay
7. **Verify** by checking the web UI or JSON status endpoint

---

## Reference: Complete Minimal Example

```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <Update.h>

WebServer server(80);

void handleOta() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/plain", Update.hasError() ? "FAIL" : "OK");
  if (!Update.hasError()) {
    delay(100);
    ESP.restart();
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
    if (!Update.end(true)) {
      Update.printError(Serial);
    }
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.softAP("K10-OTA-Test", "12345678");

  server.on("/ota", HTTP_POST, handleOta, handleOtaUpload);
  server.begin();

  Serial.print("IP: ");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  server.handleClient();
}
```

---

## Common Pitfalls

| Pitfall | Why It Happens |
|---------|---------------|
| `Update.begin(size)` with exact size fails | ESP32 flash requires 4 KB alignment. Use `UPDATE_SIZE_UNKNOWN` instead. |
| `Update.writeStream(server.client())` hangs | `writeStream()` waits for the client to close the connection, but the client waits for the HTTP response. Deadlock. Use chunked `client.read()` with a known `Content-Length` instead. |
| `server.header("Content-Length")` returns empty | Arduino WebServer stores `Content-Length` in `_clientContentLength`, not the headers map. Use `server.clientContentLength()` (public in ESP32 core). |
| `FAIL` after full upload | `Update.end(true)` failed. Most common cause: firmware size exceeds OTA partition size. Ensure partition is large enough. |

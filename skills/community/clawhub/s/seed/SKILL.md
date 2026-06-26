---
name: seed
description: Grow firmware on any hardware through HTTP — upload C, compile on device, apply with watchdog rollback
homepage: https://github.com/Awis13/seed
user-invocable: true
metadata: {"openclaw":{"emoji":"🌱","os":["darwin","linux"],"requires":{"bins":["curl","gcc"]}}}
---

# seed.c — Self-Growing Firmware

**Source:** https://github.com/Awis13/seed

You have access to a seed node — a minimal C firmware with an HTTP API
that you can grow by writing and compiling new firmware on the device.

## First steps

If the user hasn't given you a node address and token, ask them:
- Do they already have a seed node running? If so, get the IP and token.
- If not, offer to deploy one. All they need is a Linux machine with gcc:

```bash
# On the target machine (Pi, VPS, any Linux box):
curl -fsSL https://raw.githubusercontent.com/Awis13/seed/main/seeds/linux/seed.c -o seed.c
gcc -O2 -o seed seed.c
./seed 8080
# Token will be printed — give it to the agent
```

The seed binary is ~70KB, zero dependencies beyond libc.

## Connecting

The node prints its address and token on startup. If you don't know them:
```bash
# The user will provide the address, or:
curl http://<ip>:8080/health          # no auth needed
curl http://<ip>:8080/skill           # full connection details + token
```

All requests except `/health` need: `Authorization: Bearer <token>`

## What you can do

### 1. Discover the hardware
```bash
curl -H "Authorization: Bearer $TOKEN" http://$HOST/capabilities
```
Returns: arch, CPU, RAM, disk, temperature, GPIO, I2C, serial ports,
USB devices, WiFi, Bluetooth, WireGuard — everything the node has.

### 2. Read the running firmware
```bash
curl -H "Authorization: Bearer $TOKEN" http://$HOST/firmware/source
```
Returns the C source code currently running on the node.

### 3. Write new firmware
```bash
curl -H "Authorization: Bearer $TOKEN" \
  -X POST --data-binary @new_firmware.c \
  http://$HOST/firmware/source
```
Upload C source code. The node saves it for compilation.

### 4. Compile on the device
```bash
curl -H "Authorization: Bearer $TOKEN" -X POST http://$HOST/firmware/build
```
The node runs `gcc -O2` on itself. Check errors with `GET /firmware/build/logs`.

### 5. Apply (hot-swap)
```bash
curl -H "Authorization: Bearer $TOKEN" -X POST http://$HOST/firmware/apply
```
Atomic binary swap. 10-second watchdog — if the new firmware fails
the health check, the old version is restored automatically.

## API reference

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Alive check (no auth) |
| GET | /capabilities | Hardware fingerprint |
| GET | /config.md | Node config (markdown) |
| POST | /config.md | Update config |
| GET | /events | Event log (?since=unix_ts) |
| GET | /firmware/version | Version, build date, uptime |
| GET | /firmware/source | Read source code |
| POST | /firmware/source | Upload new source |
| POST | /firmware/build | Compile (gcc -O2) |
| GET | /firmware/build/logs | Compiler output |
| POST | /firmware/apply | Apply + watchdog rollback |
| GET | /skill | Generate this file with live connection details |

## Writing firmware

**Constraints:**
- C only, libc only — no external libraries
- `gcc -O2 -o seed seed.c` must compile with no extra flags
- Single-threaded, one request at a time
- Max request body: 64KB
- 3 failed applies -> /firmware/apply locks (POST /firmware/apply/reset to unlock)

**Handler pattern:**
```c
if (strcmp(req.path, "/myendpoint") == 0
    && strcmp(req.method, "GET") == 0) {
    char resp[4096];
    snprintf(resp, sizeof(resp), "{\"key\":\"value\"}");
    json_resp(fd, 200, "OK", resp);
    goto done;
}
```

**Available functions:**
- `json_resp(fd, code, status, json)` — send JSON response
- `text_resp(fd, code, status, text)` — send plain text
- `respond(fd, code, status, content_type, body, len)` — send anything
- `file_read(path, &len)` — read file, returns malloc'd buffer
- `file_write(path, data, len)` — write file
- `cmd_out(shell_cmd, buf, bufsize)` — run command, capture output
- `event_add(fmt, ...)` — log event

**Request struct:** `req.method`, `req.path`, `req.body` (malloc'd, may be NULL),
`req.body_len`, `req.content_length`. Path includes query string.

Auth is already checked before your handler. `/health` is always public.

## Capabilities example

```json
{
  "type": "seed", "version": "0.1.0", "seed": true,
  "hostname": "raspberrypi", "arch": "armv6l",
  "cpus": 1, "mem_mb": 512, "disk_mb": 14000,
  "temp_c": 42.3, "board_model": "Raspberry Pi Zero W Rev 1.1",
  "has_gcc": true,
  "net_interfaces": ["eth0", "wlan0", "usb0"],
  "serial_ports": ["/dev/ttyAMA0"],
  "i2c_buses": ["/dev/i2c-1"],
  "gpio_chips": ["/dev/gpiochip0"],
  "has_wifi": true, "has_bluetooth": true,
  "endpoints": ["/health", "/capabilities", "/config.md", ...]
}
```

Use this to decide what the node can do and what firmware to write.

## Typical workflow

1. `GET /health` — is it alive?
2. `GET /capabilities` — what hardware does it have?
3. `GET /firmware/source` — read the current code
4. Write new firmware that adds the endpoints you need
5. `POST /firmware/source` — upload it
6. `POST /firmware/build` — compile
7. `GET /firmware/build/logs` — check for errors
8. `POST /firmware/apply` — deploy (auto-rollback on failure)
9. Test the new endpoints
10. Repeat — the grown firmware still has `/firmware/*`, so you can grow it again

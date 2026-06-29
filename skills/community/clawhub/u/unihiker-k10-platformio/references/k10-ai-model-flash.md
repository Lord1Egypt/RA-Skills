# K10 AI Model Flashing and Recovery

Use this reference when a PlatformIO project combines K10 built-in AI features, voice recognition, TTS, face recognition, OTA partitions, or factory recovery.

## Fixed AI Flash Regions

Keep these offsets unchanged unless DFRobot publishes a new partition table.

| Region | Offset | Size in factory table | Purpose |
| --- | --- | --- | --- |
| `model` | `0x510000` | `4563K` | Speech recognition model image |
| `voice_data` | `0x985000` | `2542K` | TTS voice data |
| `fr` | `0xC01000` | `100K` | Face-recognition related data |

In DFRobot's current K10 PlatformIO framework package:

- `srmodels.bin` is about 3.1 MB and is used by `-DModel=CN`.
- `srmodels4.bin` is about 4.2 MB and is used by `-DModel=EN`.
- `srmodels5.bin` is about 4.5 MB but is not selected by the current PlatformIO upload builder.
- `esp_tts_voice_data_xiaoxin.dat` is about 2.5 MB and is flashed with both CN and EN.

## PlatformIO Environments

Use a normal environment for day-to-day builds and separate initialization environments for model recovery.

```ini
[k10_base]
platform = https://github.com/DFRobot/platform-unihiker.git
board = unihiker_k10
framework = arduino
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1

[env:unihiker]
extends = k10_base
build_flags =
    ${k10_base.build_flags}
    -DModel=None

[env:unihiker-init-cn]
extends = k10_base
build_flags =
    ${k10_base.build_flags}
    -DModel=CN

[env:unihiker-init-en]
extends = k10_base
build_flags =
    ${k10_base.build_flags}
    -DModel=EN
```

Use `unihiker-init-cn` or `unihiker-init-en` once over USB when the model partitions may be blank or damaged. Use `unihiker` for normal uploads and OTA app images.

## OTA Partition Rule

Do not use a generic two-slot OTA table whose app partitions grow past `0x510000`; it can overwrite the model region.

Use a model-preserving OTA table:

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

Each OTA app slot is 2.5 MB. If the firmware no longer fits, reduce firmware size, drop OTA, or explicitly decide that the project will not use built-in AI model data.

## Recovery Paths

Official UNIHIKER documentation provides Mind+ recovery:

1. Hold BOOT while connecting USB.
2. Release BOOT after the port appears.
3. Click `Restore Initial Settings`.
4. Press RST when restoration completes.

The hardware download page also provides a factory programme zip for restoring the factory demo after Mind+ initial settings are restored.

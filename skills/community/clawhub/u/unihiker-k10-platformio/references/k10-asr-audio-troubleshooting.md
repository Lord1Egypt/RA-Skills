# K10 ASR Audio Troubleshooting

Use this procedure when K10 voice models load and ASR commands register, but the wake indicator never changes or spoken commands appear ignored.

Before changing code, identify whether the application uses the official `UNIHIKER_K10::begin()` audio path or installs/configures I2S itself. Keep those paths separate during diagnosis; a minimal official-path probe is the baseline for judging custom I2S code.

## Separate the Layers

Treat these as independent checks:

1. Model partition: `MODEL_LOADER`, WakeNet, and MultiNet load successfully.
2. Command graph: command registration reaches a clear `ASR commands ready` marker.
3. Codec control: ES7243E responds on I2C and accepts initialization.
4. Audio transport: I2S produces changing, nonzero samples.
5. Recognition: a real wake word and command produce application events.

Model and command logs do not prove that microphone audio reaches the recognizer.

## Prefer the Official Audio Path

Use `UNIHIKER_K10::begin()` to initialize board IO and I2S unless there is a verified reason to reproduce the audio setup manually:

```cpp
#include <unihiker_k10.h>

UNIHIKER_K10 board;

void prepareAudio() {
  board.begin();
}
```

`board.begin()` does not call `initScreen()`. A custom TFT_eSPI/LVGL port can remain the only active display driver as long as the application never calls the SDK screen initializer. Initialize display/UI before starting the ASR worker, or keep all work after `asrInit()` short; long blocking setup after ASR starts can produce `rb_out slow` warnings.

If a strict build cannot link `unihiker_k10` because even an unused file-static TFT instance is unacceptable, first prove the microphone with a minimal official-path program. Then reproduce the K10 `initI2S()` configuration exactly and compare each initialization step rather than guessing pins or formats.

## Do Not Trust the First DMA Block

I2S DMA buffers may contain silence captured while MCLK and ES7243E were still settling. An immediate probe can report every sample as zero even though later audio is valid.

After codec initialization:

1. Wait about 500 ms.
2. Read and discard more data than the configured DMA capacity.
3. Measure subsequent samples.
4. Do not call `i2s_zero_dma_buffer()` immediately before ASR starts.

For the K10 SDK default of three 300-frame stereo, 16-bit buffers, draining about 6 KiB is sufficient:

```cpp
void probeMicrophone() {
  int16_t samples[256];

  delay(500);
  for (int block = 0; block < 12; ++block) {
    size_t bytesRead = 0;
    i2s_read(I2S_NUM_0, samples, sizeof(samples), &bytesRead,
             pdMS_TO_TICKS(250));
  }

  uint32_t nonzero = 0;
  uint16_t peak = 0;
  size_t bytesRead = 0;
  i2s_read(I2S_NUM_0, samples, sizeof(samples), &bytesRead,
           pdMS_TO_TICKS(250));
  for (size_t i = 0; i < bytesRead / sizeof(samples[0]); ++i) {
    const int32_t value = samples[i];
    const uint16_t magnitude = value < 0 ? -value : value;
    if (value != 0) ++nonzero;
    if (magnitude > peak) peak = magnitude;
  }
  Serial.printf("MIC probe: bytes=%u nonzero=%u peak=%u\n",
                static_cast<unsigned>(bytesRead),
                static_cast<unsigned>(nonzero), peak);
}
```

A healthy quiet-room probe should normally contain nonzero noise samples. Judge it by repeated post-drain reads, not one startup block.

## ES7243E Checks

The codec is normally visible at 7-bit I2C address `0x11` on K10. Early boot messages such as `Es7243e STOP failed`, `initialize failed`, or `START failed` can occur before I2S supplies MCLK. Do not ignore them, but distinguish the early attempt from a retry after I2S starts.

If official board initialization still leaves repeated post-drain reads at zero:

1. Scan I2C0 and confirm `0x11` responds.
2. Confirm the official I2S pins: MCLK 3, BCLK 0, LRCK 38, data-in 39, data-out 45.
3. Run a minimal program containing only `board.begin()` and repeated `i2s_read()` calls.
4. Compare that result with the full application before changing codec registers.
5. Only then consider a board-revision-specific post-MCLK codec retry.

Some framework builds expose `es7243e_adc_init()` and `es7243e_adc_ctrl_state()` only as internal C symbols. Treat calls to them as a compatibility fallback, verify against the installed framework, and never copy an arbitrary register table from another ES7243E board without testing.

## Recognition Verification

After audio is nonzero, verify the whole path rather than stopping at startup logs:

1. Wait for the explicit command-ready marker.
2. Confirm the actual wake phrase from the loaded WakeNet model name, startup log, or project configuration; one common Chinese K10 model uses `你好小鑫`.
3. Speak the command within the configured wake timeout.
4. Log the command source, for example `Light ON; cat eyes OPEN (VOICE)`.
5. Test both commands at least once.

`isWakeUp()` represents a transient recognition state. Poll it frequently and update the UI only when its value changes.

## Failure Interpretation

| Evidence | Likely layer |
| --- | --- |
| Model partition cannot map | Model flash or partition layout |
| Models load, command-ready marker absent | ASR initialization or command registration |
| Codec absent at `0x11` | Board bus, power, or hardware |
| Immediate probe is zero, post-drain probe is nonzero | Stale startup DMA silence; audio is healthy |
| Repeated post-drain probes stay zero in minimal official program | Hardware, clock, codec, or I2S path |
| Audio is nonzero but wake fails | Wake model, phrase, noise level, or recognizer configuration |
| Commands work but wake indicator appears stuck | UI polling/state-transition logic |

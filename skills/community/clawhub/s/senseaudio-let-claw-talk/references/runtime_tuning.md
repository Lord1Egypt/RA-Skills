# Runtime Tuning

## Common adjustments

- More false triggers:
  - raise `--speech-threshold-db`
  - increase `--silence-seconds`
  - increase `--vad-mode`
- Misses quiet speech:
  - lower `--speech-threshold-db`
  - lower `--vad-mode`
- Cuts off too early:
  - increase `--silence-seconds`
- Replies too slowly:
  - use `--tts-mode say` for quick local playback during debugging
  - or raise `--tts-speed` a bit, for example `1.25`
  - 这个导出包默认先走整段播报；如果你想打开流式 TTS，可手动加 `--senseaudio-streaming-tts`
  - 如果想让流式模式尽量少卡顿，可选安装 `miniaudio`，再用 `--senseaudio-streaming-backend miniaudio`
- Wants a wake word:
  - add `--wake-phrase`
  - add `--sleep-phrase` if the user wants an explicit way to return to sleep
  - increase `--wake-sticky-seconds` if follow-up turns too容易失效
  - current default wake model is `sense-asr-deepthink`
  - if the user wants a lighter wake detector, add `--wake-asr-model sense-asr-lite`
- Wants no wake word:
  - add `--no-wake-phrase`
- Wants no sleep word:
  - add `--no-sleep-phrase`
- Wants to interrupt playback:
  - add `--interrupt-playback`
  - if playback self-interrupts too often, raise `--interrupt-speech-threshold-db`
  - or increase `--interrupt-grace-seconds`
- Wants to disable interruption:
  - add `--no-interrupt-playback`
  - or increase `--interrupt-grace-seconds`
- Wants more spoken answers:
  - adjust `--spoken-style-prompt`
- Wants remembered preferences:
  - say `记住当前偏好`
  - say `记住不要打断我`
  - say `记住语速 1.1`
  - say `记住多等一下再截断`
  - say `记住以后更简短一点`
  - say `记住以后展开一点`
  - say `记住默认音色是 温柔御姐`
  - say `清除偏好`
- Wants voice switching:
  - say `列出音色`
  - say `换成温柔御姐`
  - say `切到温柔御姐`
  - say `换个女声`
  - say `切换到 male_0018_a`
  - say `以后都用 male_0004_a`
  - say `注册克隆音色 vc-123456 叫 我的声音`
- Wants a runtime summary:
  - say `当前设置`
- Wants optional voiceprint filtering with WeSpeaker:
  - say `开启 WeSpeaker 声纹验证`
  - say `录入我的声音`
  - say `重录我的声音`
  - say `查看 WeSpeaker 状态`
  - say `关闭 WeSpeaker 声纹验证`
  - say `启动后台声纹`
  - say `停止后台声纹`
  - or add `--speaker-verification-backend wespeaker`
  - if the user environment is not ready, set `VOICECLAW_WESPEAKER_PYTHON` first
  - if filtering is too loose, raise `--wespeaker-threshold`

## Example commands

Noisy room:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --tts-speed 1.25 \
  --interrupt-grace-seconds 1.2 \
  --interrupt-min-speech-seconds 0.35 \
  --interrupt-speech-threshold-db -16 \
  --speech-threshold-db -18 \
  --silence-seconds 1.6 \
  --vad-mode 3
```

Quick single-turn check:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --once \
  --capture-backend swift \
  --tts-mode say
```

One-click launcher with extra defaults:

```bash
export VOICECLAW_EXTRA_ARGS='--wake-phrase 贾维斯 --sleep-phrase 贾维斯休息 --interrupt-playback'
bash "{baseDir}/scripts/start_senseaudio_let_claw_talk.sh"
```

Disable SenseAudio streaming TTS temporarily:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --no-senseaudio-streaming-tts
```

Use the optional `miniaudio` streaming backend:

```bash
/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --user miniaudio
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --capture-backend swift \
  --senseaudio-streaming-tts \
  --senseaudio-streaming-backend miniaudio
```

If you need to bypass startup checks temporarily:

```bash
bash "{baseDir}/scripts/start_senseaudio_let_claw_talk.sh" --skip-self-check
```

Wake phrase mode:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --wake-phrase "贾维斯" \
  --sleep-phrase "贾维斯休息" \
  --wake-sticky-seconds 90
```

WeSpeaker enabled:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --speaker-verification-backend wespeaker \
  --wespeaker-python "$HOME/.audioclaw/workspace/tools/wespeaker/.venv/bin/python" \
  --wespeaker-threshold 0.72
```

No wake phrase mode:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --no-wake-phrase
```

Interrupt playback mode:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --interrupt-playback \
  --speech-threshold-db -18
```

Disable interruption:

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --no-interrupt-playback
```

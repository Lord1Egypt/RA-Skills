# WeSpeaker User Environment Guide

这个 skill 默认不会把 WeSpeaker 的虚拟环境或模型权重放在 skill 目录里。

推荐的用户级目录约定：

- 虚拟环境：`~/.audioclaw/workspace/tools/wespeaker/.venv`
- 模型缓存和运行状态：`~/.audioclaw/workspace/state/wespeaker`

## 1. 创建用户级环境

建议优先用 Python 3.11。Windows 端尽量不要直接拿 3.14 做 WeSpeaker 环境。

```bash
mkdir -p ~/.audioclaw/workspace/tools/wespeaker
python3 -m venv ~/.audioclaw/workspace/tools/wespeaker/.venv
~/.audioclaw/workspace/tools/wespeaker/.venv/bin/pip install --upgrade pip setuptools wheel
```

## 2. 安装 WeSpeaker 及运行依赖

下面这组是当前 skill 推荐的用户级安装组合。Windows 用户把 `bin/python` 和 `bin/pip` 对应替换成 `Scripts\\python.exe`、`Scripts\\pip.exe` 即可。

如果你在 Windows 上遇到：

- `AttributeError: module 'torchaudio' has no attribute 'set_audio_backend'`

说明当前 `torchaudio` 太新，而 WeSpeaker 依赖链里某些组件还在调用旧接口。优先建议按 WeSpeaker README 里偏旧、更稳的组合来装。

```bash
~/.audioclaw/workspace/tools/wespeaker/.venv/bin/pip install torch==1.12.1 torchaudio==0.12.1
~/.audioclaw/workspace/tools/wespeaker/.venv/bin/pip install soundfile PyYAML requests onnxruntime s3prl openai-whisper peft
~/.audioclaw/workspace/tools/wespeaker/.venv/bin/pip install git+https://github.com/wenet-e2e/wespeaker.git
```

## 3. 验证环境

```bash
~/.audioclaw/workspace/tools/wespeaker/.venv/bin/python - <<'PY'
import wespeaker
print("wespeaker ok")
PY
```

如果这里能输出 `wespeaker ok`，说明环境已经准备好。

## 4. 告诉 SenseAudio-Let-Claw-Talk-Universal 去哪里找环境

默认启动脚本会优先读取：

- `VOICECLAW_WESPEAKER_PYTHON`

如果你按上面的推荐目录安装，一般不用再改。

如果你把环境装在别的位置，可以手动指定：

```bash
export VOICECLAW_WESPEAKER_PYTHON=/你的路径/bin/python
```

## 5. 在当前 skill 中启用

直接启动：

```bash
bash "{baseDir}/scripts/start_senseaudio_let_claw_talk_universal.sh" \
  --speaker-verification-backend wespeaker
```

或者先设环境变量：

```bash
export VOICECLAW_SPEAKER_BACKEND=wespeaker
bash "{baseDir}/scripts/start_senseaudio_let_claw_talk_universal.sh"
```

启动后可以直接说：

- `开启 WeSpeaker 声纹验证`
- `录入我的声音`
- `查看 WeSpeaker 状态`

## 6. 权重放在哪里

第一次真正启动 WeSpeaker 后台时，模型会自动下载到：

- `~/.audioclaw/workspace/state/wespeaker/models`

这部分不在 skill 目录里。

## 7. 常见问题

- 如果提示 `WeSpeaker Python 不存在`
  - 说明用户级环境还没装好，或者 `VOICECLAW_WESPEAKER_PYTHON` 指到了错误路径
- 如果第一次启动比较慢
  - 这是正常的，通常是首次下载模型和预热
- 如果后面想让它更快
  - 直接开启 WeSpeaker 后台服务一次，后续再用会更快
- 如果 Windows 上报 `torchaudio.set_audio_backend` 相关错误
  - 优先把 WeSpeaker 用户环境里的 `torch / torchaudio` 降到 README 推荐组合
- 如果报 `No module named 'peft'`
  - 说明 WeSpeaker 依赖链缺了 `peft`
  - 直接把 `peft` 补进当前 WeSpeaker 用户环境即可

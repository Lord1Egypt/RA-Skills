---
name: qwen3-tts-feishu
description: 使用 Qwen3-TTS 本地语音合成，将文字转为语音文件，并可通过飞书发送语音消息（语音气泡格式）。支持 Apple Silicon (MPS) 和 CUDA GPU，无需 API Key 即可本地合成。
metadata:
  openclaw:
    requires:
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
      bins:
        - ffmpeg
        - sox
        - python3
    primaryEnv: FEISHU_APP_ID
    emoji: "🎙️"
    os:
      - macos
      - linux
---

# Qwen3-TTS 本地语音合成 + 飞书语音消息

完全本地运行，无需 API Key。支持中文、英文、日文等多语言，9 种音色可选。

---

## 第一步：环境准备

### 安装依赖

```bash
# 创建项目目录（可自定义）
mkdir -p ~/qwen-tts && cd ~/qwen-tts

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 安装 Python 依赖
pip install qwen-tts soundfile modelscope

# 安装系统工具（发送飞书语音需要）
# macOS:
brew install ffmpeg sox
# Ubuntu/Debian:
# apt install ffmpeg sox
```

---

## 第二步：下载模型

模型大小约 **4.2GB**，需要下载两个组件：

### 国内（ModelScope，推荐）

```python
from modelscope.hub.snapshot_download import snapshot_download

# 下载主模型（3.57GB）
snapshot_download(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    local_dir="./Qwen3-TTS-12Hz-1.7B-CustomVoice"
)
```

> **注意**：`modelscope` CLI 在 Python 3.12+ 下有 bug，请用上面的 Python API 方式。

### 海外（HuggingFace）

```bash
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice \
    --local-dir ./Qwen3-TTS-12Hz-1.7B-CustomVoice
```

> **提示**：模型目录自带 `speech_tokenizer` 子目录，不需要单独下载 tokenizer。

---

## 第三步：合成语音

```python
import soundfile as sf
from qwen_tts.inference.qwen3_tts_model import Qwen3TTSModel

# 根据硬件选择设备
# Apple Silicon: device_map="mps"
# NVIDIA GPU:    device_map="cuda"
# CPU（慢）:     device_map="cpu"
MODEL_PATH = "./Qwen3-TTS-12Hz-1.7B-CustomVoice"

model = Qwen3TTSModel.from_pretrained(MODEL_PATH, device_map="mps")

wavs, sample_rate = model.generate_custom_voice(
    text="你好，我是本地语音合成助手。",
    speaker="aiden",      # 见下方音色列表
    language="Chinese"    # Chinese / English / Japanese
)

sf.write("output.wav", wavs[0], sample_rate)
print(f"已生成: output.wav ({sample_rate}Hz)")
```

也可直接用脚本（见 `scripts/synthesize.py`）：

```bash
python scripts/synthesize.py "要合成的文字" output.wav aiden Chinese
```

### 可用音色

| speaker   | 性别 | 风格         |
|-----------|------|--------------|
| aiden     | 男   | 标准普通话   |
| bella     | 女   | 标准普通话   |
| chelsie   | 女   | 年轻活泼     |
| ethan     | 男   | 成熟稳重     |
| freya     | 女   | 温柔知性     |
| george    | 男   | 低沉磁性     |
| holly     | 女   | 清新自然     |
| iris      | 女   | 活力充沛     |
| james     | 男   | 专业正式     |

---

## 第四步：通过飞书发送语音消息

> **重要**：飞书 `msg_type: audio` 要求 **opus 格式**，必须直接调飞书 API 上传文件。OpenClaw `message` 工具的 `filePath` 参数只发送路径文本，不是真正上传。

### 前置条件

- 飞书自建应用的 `app_id` 和 `app_secret`
- 收件人的 `open_id`
- 应用已开通权限：`im:message:send_as_bot`、`im:resource`

### 发送流程（4步）

```bash
# 1. WAV → opus
ffmpeg -i output.wav -c:a libopus -b:a 24k output.opus -y

# 2. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"YOUR_APP_ID","app_secret":"YOUR_APP_SECRET"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# 3. 上传 opus 文件
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=audio.opus" \
  -F "file=@output.opus" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")

# 4. 发送语音气泡
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"TARGET_OPEN_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

完整自动化脚本见 `scripts/send_voice_feishu.sh`（需配置环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`）。

---

## 常见问题

| 问题 | 原因 / 解决方案 |
|------|----------------|
| `flash-attn` 警告 | 可忽略，不影响功能 |
| 模型加载慢（10~20s） | 首次加载正常，之后复用同一实例 |
| MPS 报错 | 确认 PyTorch >= 2.0，macOS >= 12.3 |
| 飞书收到的是文件而不是语音气泡 | 格式必须是 opus，不能是 mp3/wav |
| `pkg_resources` 报错 | modelscope CLI bug，改用 Python API 下载 |

---

## 性能参考（Apple M4）

- 模型加载：约 15 秒
- 短句合成（< 50字）：约 2~3 秒
- 长句合成（100~200字）：约 5~10 秒

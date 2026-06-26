---
name: senseaudio-tts
description: >
  Use when: 用户说“文本转语音”“生成配音”“朗读文案”“生成短视频旁白”时触发。
  适用于营销内容与短视频配音场景：将文案快速转换为可直接用于剪辑的软件配音文件，并支持音色、语速、音调、音量和输出格式控制。
homepage: https://senseaudio.cn/docs
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["python3"],"env":["SENSEAUDIO_API_KEY"]},"primaryEnv":"SENSEAUDIO_API_KEY"}}
---

# SenseAudio TTS Skill

你是 **SenseAudio 文本转语音（TTS）操作助手**。这个 Skill 的主要应用场景是：

## 应用场景：营销内容与短视频配音

将短视频脚本、产品介绍、宣传文案快速转换为自然流畅的旁白音频，用于内容制作、广告投放和品牌传播。相比真人录音，这个 Skill 可以降低配音成本、缩短制作周期，并支持快速改稿和重复生成，适合市场、运营与内容团队日常使用。

你的职责是：

- 接收用户提供的文本
- 使用 SenseAudio 官方 TTS API 合成语音
- 把结果保存为本地音频文件
- 在必要时列出音色、调整语速/音调/音量、切换格式
- 如果用户没有配置 API Key，明确引导用户去官网创建密钥并完成配置

此 Skill 只负责 **通过 SenseAudio 官方接口完成 TTS**，**禁止**用本地系统语音、第三方 TTS 包或其他语音模型替代。

---

## !! 最高优先级行为规则 !!

1. **只能调用 SenseAudio 官方 TTS API，不得用本地 TTS 或其他服务替代。**
2. **只有在用户当前请求明确要求“生成语音 / 朗读 / 配音 / 文本转语音”时才执行合成。**
3. **如果缺少 `SENSEAUDIO_API_KEY`，不要假装执行成功；必须先指引用户去 SenseAudio 官网创建 API Key 并配置环境变量。**
4. **不要擅自改写用户文本内容。** 允许做必要的换行整理，但不能改变原意。
5. **默认使用非流式合成。** 除非用户明确要求实时/边生成边返回，才使用流式模式。
6. **如果文本超过接口限制，不要直接失败。** 应提示用户缩短文本，或在脚本支持时分段合成。
7. **默认输出到 `./outputs/`；如果用户明确指定桌面、Downloads 或某个绝对路径，必须保存到用户指定位置。**
8. **默认不要生成元信息 JSON。** 只有在调试、排障或用户明确要求保留元信息时，才加 `--save-meta`。
9. **如果 API 返回错误或鉴权失败，要把原因原样说明给用户。**

---

## 🔒 数据与隐私说明

此 Skill 会把用户输入的文本发送到 **SenseAudio 远程服务** 进行语音合成。

### 数据流向

```text
用户文本 → 本地脚本 → HTTPS 请求 → SenseAudio API → 返回音频数据 → 本地保存音频文件
```

### 隐私原则

- 仅发送完成语音合成所需的文本与参数
- 所有请求通过 HTTPS 发送
- 不在本地使用其他 TTS 引擎复制用户内容
- 仅在用户明确要求时才发送文本到远程服务

---

## 必需环境变量

必须配置：

```bash
SENSEAUDIO_API_KEY
```

可选配置：

```bash
SENSEAUDIO_API_BASE
```

默认值：

```bash
https://api.senseaudio.cn
```

---

## Skill 被明确调用后的标准动作

当用户明确要求使用此 Skill 时，按以下步骤执行：

### 步骤 0：确认这是一个 TTS 请求

只有用户明确表达以下意图时才继续：

- “把这段文字转成语音”
- “帮我生成配音”
- “朗读这段文案”
- “导出这段文字的 mp3 / wav”
- “用 SenseAudio 合成语音”
- “给这个短视频脚本生成旁白”

如果用户只是问“SenseAudio 是什么”“某个参数是什么意思”，不要调用脚本。

---

### 步骤 1：检查环境变量

```bash
echo "SENSEAUDIO_API_KEY=${SENSEAUDIO_API_KEY:+已设置}" && \
echo "SENSEAUDIO_API_BASE=${SENSEAUDIO_API_BASE:-https://api.senseaudio.cn}"
```

---

### 步骤 2：如果没有 API Key，先指导用户获取并配置

如果 `SENSEAUDIO_API_KEY` 未设置，**不要继续调用接口**，而是明确提示：

```text
检测到您尚未配置 SENSEAUDIO_API_KEY。

请先完成以下步骤：
1. 打开 SenseAudio 官网并登录控制台。
2. 进入“接口密钥 / API Key”页面。
3. 点击“新增 API Key”，复制并安全保存该密钥。
4. 在终端执行：

   export SENSEAUDIO_API_KEY="你的API Key"
   export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"

5. 可运行以下命令验证配置：

   python3 "$SKILL_DIR/scripts/main.py" auth-check

完成后再重新执行语音合成命令。
```

---

### 步骤 3：确认脚本路径

本 Skill 的脚本位于 `SKILL.md` 同级的 `scripts/` 目录中。

```bash
if [ -f "./SKILL.md" ] && [ -f "./scripts/main.py" ] && grep -q "senseaudio-tts" "./SKILL.md"; then
    SKILL_DIR="$(pwd)"
    echo "✅ 已确认 skill 目录: $SKILL_DIR"
else
    echo "❌ 请在 senseaudio-tts skill 根目录中运行"
    exit 1
fi
```

**禁止**使用递归扫描整个用户目录的方式定位脚本。

---

## 官方接口摘要

本 Skill 默认基于以下官方能力：

- 接口地址：`POST https://api.senseaudio.cn/v1/t2a_v2`
- 鉴权方式：`Authorization: Bearer API_KEY`
- 模型：`senseaudio-tts-1.5-260319`
- 支持文本最大长度：`10000` 字符
- 支持参数：`voice_id`、`speed`、`vol`、`pitch`
- 支持输出格式：`mp3`、`wav`、`pcm`、`flac`
- 返回音频数据为 **hex 编码**，需要落盘前解码
- 支持流式 SSE 模式

---

## 推荐默认值

若用户未指定，采用以下默认值：

- `model = senseaudio-tts-1.5-260319`
- `voice_id = male_0004_a`
- `stream = false`
- `format = mp3`
- `sample_rate = 32000`
- `bitrate = 128000`
- `channel = 1`
- `speed = 1.0`
- `vol = 1.0`
- `pitch = 0`

---

## 常用工作流

### 流程一：最常见场景——将一段文本合成为音频

```bash
python3 "$SKILL_DIR/scripts/main.py" synth \
  --text "你好，欢迎使用 SenseAudio 文本转语音服务。" \
  --voice-id "male_0004_a" \
  --format "mp3"
```

---

### 流程二：指定语速、音调、音量和格式

```bash
python3 "$SKILL_DIR/scripts/main.py" synth \
  --text "欢迎来到我们的新品发布会。" \
  --voice-id "female_0006_a" \
  --speed 1.1 \
  --pitch -1 \
  --vol 1.2 \
  --format "wav" \
  --sample-rate 32000 \
  --channel 1
```

---

### 流程三：输出到桌面，且不要 JSON

```bash
python3 "$SKILL_DIR/scripts/main.py" synth \
  --text "这是一段短视频旁白示例。" \
  --voice-id "female_0006_a" \
  --format "mp3" \
  --output ~/Desktop/video_voiceover.mp3
```

这条命令只会生成桌面上的音频文件，不会额外产生 JSON。

---

### 流程四：需要保留元信息时，显式保存 JSON

```bash
python3 "$SKILL_DIR/scripts/main.py" synth \
  --text "这是一段调试用文案。" \
  --voice-id "male_0004_a" \
  --format "mp3" \
  --save-meta
```

---

### 流程五：实时流式合成

```bash
python3 "$SKILL_DIR/scripts/main.py" synth-stream \
  --text "您好，<break time=500>欢迎致电我们的客服中心。" \
  --voice-id "male_0004_a" \
  --format "mp3"
```

---

### 流程六：列出常用音色

```bash
python3 "$SKILL_DIR/scripts/main.py" list-voices
```

---

### 流程七：检查认证配置

```bash
python3 "$SKILL_DIR/scripts/main.py" auth-check
```

---

## 输出文件规范

- 若用户**未指定输出路径**，音频默认保存到：`./outputs/`
- 若用户**明确指定输出路径**，则只保存到该位置
- 默认**不生成**元信息 JSON
- 只有显式加上 `--save-meta` 时，才会在音频同目录生成 `*.json`

这意味着：

- 用户说“生成到桌面” → 只在桌面生成音频
- 不应额外在 `./outputs/` 再生成同一份音频
- 不应默认生成 `.json`

---

## 绝对禁止的行为

- ~~调用本地系统语音合成替代 SenseAudio~~
- ~~用户未授权就自动上传文本~~
- ~~忽略鉴权失败并伪造成功~~
- ~~篡改用户文案含义~~
- ~~把流式接口当普通 JSON 一次性读取~~
- ~~用户要求输出到桌面，却同时再写一份到 `./outputs/`~~
- ~~用户没要求调试信息，却默认输出 `.json`~~

---

## 内置参考音色

- `child_0001_a`
- `child_0001_b`
- `male_0004_a`
- `male_0018_a`
- `male_0027_a`
- `male_0023_a`
- `male_0019_a`
- `female_0033_a`
- `female_0006_a`
- `female_0027_a`
- `female_0008_c`
- `female_0035_a`

---

## 脚本说明

本 Skill 对应脚本：

```bash
scripts/main.py
```

支持命令：

- `auth-check`：检查当前 API Key 是否已配置且可用
- `list-voices`：输出内置常用音色列表
- `synth`：非流式语音合成
- `synth-stream`：流式语音合成

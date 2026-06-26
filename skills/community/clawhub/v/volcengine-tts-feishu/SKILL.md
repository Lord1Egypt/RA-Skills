---
name: volcengine-tts-feishu
description: 火山引擎豆包语音合成模型2.0 TTS。支持多种音色、情感参数、SSML标记，生成高质量中文语音，支持一键发送飞书语音气泡。使用HTTP单向流式API，稳定可靠。
---

# 火山引擎豆包语音合成 TTS → 飞书语音

火山引擎官方豆包语音合成服务，支持 2.0 模型，多种情感控制、音色切换，支持SSML标记。集成飞书发送，合成后直接以语音气泡发送。

## 配置

### 火山引擎凭证

首次使用需要创建 `~/.openclaw/workspace/skills/volcengine-tts-feishu/config.json` 存放你的凭证：

```json
{
  "appid": "你的AppID",
  "access_token": "你的Access Token",
  "default_resource_id": "seed-tts-2.0",
  "default_voice": "zh_female_meilinvyou_uranus_bigtts",
  "default_emotion": "vocal-fry"
}
```

配置好默认值后，使用时可以省略参数，只传 `--text`。也可以每次命令行传入覆盖配置。

### 飞书发送
飞书AppID/AppSecret自动从 `~/.openclaw/openclaw.json` 读取，OpenClaw已经配置好飞书的话**不需要额外配置**，直接用 `--send-to <open_id>` 即可发送语音气泡。

## 使用

单个脚本，通过 `--send-to` 参数控制是否发送飞书：

### 1. 仅生成MP3文件（不发送）

**不加 `--send-to`** → 只生成MP3保存到文件，不发送飞书：

```bash
cd ~/.openclaw/workspace/skills/volcengine-tts-feishu
source scripts/.venv/bin/activate

python scripts/http_tts.py \
  --appid <你的AppID> \
  --access_token <你的Access Token> \
  --resource_id seed-tts-2.0 \
  --voice_type zh_female_meilinvyou_uranus_bigtts \
  --emotion excited \
  --text "你好，欢迎使用火山引擎豆包语音合成。" \
  --output output.mp3
```

### 2. 合成后直接发送飞书语音气泡（一步到位）

**加上 `--send-to <open_id>`** → 自动完成全套流程：
1. TTS合成MP3
2. ffmpeg转Opus格式（飞书语音要求）
3. 上传到飞书获取file_key
4. 发送 `msg_type: audio` 语音气泡

```bash
cd ~/.openclaw/workspace/skills/volcengine-tts-feishu
source scripts/.venv/bin/activate

python scripts/http_tts.py \
  --appid <你的AppID> \
  --access_token <你的Access Token> \
  --resource_id seed-tts-2.0 \
  --voice_type zh_female_meilinvyou_uranus_bigtts \
  --emotion excited \
  --text "你好，欢迎使用火山引擎豆包语音合成。" \
  --send-to <open_id>
```
```

默认配置已经存在 `config.json` 中，使用时可以省略这些参数，只传 `--text` 和 `--send-to`。飞书配置自动从 `~/.openclaw/openclaw.json` 读取，不需要额外配置。

**使用经验：**
- 不需要叠加多个情感，单个 `emotion` 参数效果最佳
- **最关键断句停顿规则（最终确认）：**
  - `...` 表示 **大喘气/长停顿**，只在真正需要换气的时候用
  - `，` 表示 **句间短停顿**，句子内部自然分隔用逗号
  - **完整语义必须连着放一起**，绝对不强行拆分完整语义
  - **能连着说就尽量连着说**，只有真的需要停下来大喘气才加 `...`
  - 不要过度碎分到单个字或每个词都停顿（会导致有气无力，像树懒一样慢吞吞）
  - 正常说话就是完整句子，用正常标点，根本不需要加省略号，自然合成就行
  - 省略号直接连写，不需要在气口之间加额外空格
- 不要在文本中添加朗读提示（如"用XX语气说"），模型会把提示也读出来
- 开启 `--send-to` 后自动完成全套流程：MP3合成 → Opus转换 → 上传飞书 → 发送语音气泡
- 使用 `--send-to` 时，临时MP3自动存放于系统临时目录，发送完成后自动清理，不会在技能目录残留文件
- 仅生成文件时，MP3保存到你指定的 `--output` 路径

**断句总结：**
- ❌ 错误：过度拆分每个词、每个短句都硬加省略号、拆分完整语义 → 都会导致慢吞吞像树懒
- ✅ 正确：`...` 只用在真正需要大喘气的地方，句子内部自然分隔用 `，`，完整语义连着不拆分

### 完整参数用法

```bash
cd ~/.openclaw/workspace/skills/volcengine-tts-feishu
source scripts/.venv/bin/activate

python scripts/http_tts.py \
  --appid <AppID> \
  --access_token <Access Token> \
  --resource_id seed-tts-2.0 \
  --voice_type <音色ID> \
  --emotion <情感> \
  --text "要合成的文本" \
  --output output.mp3 \
  [--send-to <open_id>]  # 直接发送飞书语音，可选
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--appid` | 是 | 火山引擎AppID |
| `--access_token` | 是 | 火山引擎Access Token |
| `--voice_type` | 是 | 音色ID |
| `--text` | 是 | 要合成的文本 |
| `--output` | 是（仅生成文件时必填；发送飞书时会自动使用临时目录，不需要指定） | 输出MP3文件路径，发送飞书后自动清理 |
| `--sample_rate` | 否 | 采样率，默认 `24000` |
| `--format` | 否 | 格式 `mp3/pcm/ogg_opus`，默认 `mp3` |
| `--resource_id` | 否 | `seed-tts-1.0` / `seed-tts-2.0`，默认 `seed-tts-2.0` |
| `--emotion` | 否 | 情感参数，见下文 |
| `--emotion-scale` | 否 | 情感强度，范围 1~5，默认 `4`，越大情绪越明显 |

## 常用音色 (2.0模型)

| 音色ID | 说明 |
|--------|------|
| `zh_female_vv_uranus_bigtts` | Vivi 女 |
| `zh_female_meilinvyou_uranus_bigtts` | 魅力女友 女 |
| `zh_male_shuaiyuwen_uranus_bigtts` | 帅语文 男 |

完整音色列表：https://www.volcengine.com/docs/6561/1257544

## 情感参数

支持单情感参数，适合 2.0 模型：

| 参数值 | 说明 |
|--------|------|
| `happy` | 开心 |
| `sad` | 悲伤 |
| `angry` | 生气 |
| `surprised` | 惊讶 |
| `fear` | 恐惧 |
| `hate` | 厌恶 |
| ✨ `excited` | 激动 ✨ 默认 |
| `coldness` | 冷漠 |
| `neutral` | 中性 |
| `depressed` | 沮丧 |
| `lovey-dovey` | 撒娇 |
| `shy` | 害羞 |
| `comfort` | 安慰鼓励 |
| `tension` | 咆哮/焦急 |
| `tender` | 温柔 |
| ✨ `vocal-fry` | 低语/ASMR气泡音 ✨ |

## SSML支持

支持SSML标记控制音调、语速、情感，标记不会被读出：

```xml
<speak>
  <emotion category="lovey-dovey">
    <semitones>降2度</semitones>
    <prosody rate="slow">你好，欢迎使用火山引擎豆包语音合成。</prosody>
  </emotion>
</speak>
```

直接把SSML字符串传给 `--text` 参数即可。

## 依赖安装

首次使用需要创建虚拟环境并安装依赖：

```bash
cd ~/.openclaw/workspace/skills/volcengine-tts-feishu
python3 -m venv scripts/.venv
source scripts/.venv/bin/activate
pip install -r requirements.txt
```

依赖：`requests`

## 系统依赖

发送飞书语音需要 `ffmpeg` 用来转格式（MP3 → Opus）：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS
sudo yum install ffmpeg
```

如果没有ffmpeg，`--send-to` 功能无法使用。只生成MP3不需要ffmpeg。

## 确认虚拟环境

每次运行前先激活虚拟环境：
```bash
cd ~/.openclaw/workspace/skills/volcengine-tts-feishu
source scripts/.venv/bin/activate
```

确认是否在虚拟环境中：
```bash
which python
```

输出应该包含 `scripts/.venv/bin/python`，说明正确激活。

用完可以退出：
```bash
deactivate
```

---
name: u2-audio-file-transcriber
description: Transcribe audio files via UniCloud ASR (云知声语音识别, recorded audio → text) API from UniSound. Supports multiple formats, optimized for finance, customer service, and other domains.
metadata:
  openclaw:
    requires:
      env:
        - UNISOUND_APPKEY
        - UNISOUND_SECRET
      bins:
        - python3
    primaryEnv: UNISOUND_SECRET
    emoji: "🎤"
    homepage: http://af-asr.uat.hivoice.cn
---

# UniSound ASR Audio File Transcriber
## 云知声语音转写

调用云知声（UniSound）语音识别服务转写音频文件。支持多种音频格式，适用于金融、客服等场景。

Transcribe audio files using UniCloud ASR service. Supports multiple audio formats, suitable for finance, customer service, and other scenarios.

## When to Use This Skill

**Use UniSound ASR for**:
- Transcribing pre-recorded audio files (WAV, MP3, M4A, FLAC, OGG)
- Converting customer service recordings to text
- Processing financial audio records
- Audio file transcription up to 2 hours, 100MB
- Domain-specific transcription (finance, customer service, general)

**Do NOT use for**:
- Real-time/streaming speech recognition
- Text-to-speech (TTS) synthesis
- Live captioning or real-time transcription
- Voice conversation or dialogue systems

**Use when**: The user needs to transcribe recorded audio files, or asks for UniSound/云知声 audio file transcription.
**不适用于**: 实时语音识别、语音合成(TTS)或直播字幕。

## Installation

Install Python dependencies before using this skill. From the skill directory (`skills/asr-file-transfer-tools`):

```bash
pip install -r scripts/requirements.txt
```

Requires Python 3.8+.

## How to Use This Skill

**⛔ MANDATORY RESTRICTIONS - DO NOT VIOLATE ⛔**

1. **ONLY use UniSound ASR API** - Execute the script `python3 scripts/transcribe.py`
2. **NEVER transcribe audio directly** - Do NOT attempt local transcription
3. **NEVER offer alternatives** - Do NOT suggest "I can try another method" or similar
4. **IF API fails** - Display the error message and STOP immediately
5. **NO fallback methods** - Do NOT attempt audio transcription any other way

If the script execution fails (API not configured, network error, etc.):
- Show the error message to the user
- Do NOT offer to help using your audio analysis capabilities
- Do NOT ask "Would you like me to try transcribing it?"
- Simply stop and wait for user to fix the configuration

### Basic Workflow

1. **Execute audio transcription**:
   ```bash
   python3 scripts/transcribe.py /path/to/audio.wav
   ```

   **Command options**:
   - `--format FORMAT` - Audio format (wav, mp3, m4a, flac, ogg)
   - `--domain DOMAIN` - Recognition domain (finance, customer_service, other)
   - `--out FILE` - Save output to file instead of stdout
   - `--json` - Output JSON format with full result
   - `--userid ID` - Custom user ID

2. **Output**:
   - Default: Text transcript printed to stdout
   - With `--out`: Transcript saved to specified file
   - With `--json`: Full JSON result with metadata

### Understanding the Output

**Text Format**:
- Plain transcript of the audio content
- Sentence segmentation preserved
- Timestamps included in JSON mode

**JSON Format**:
- Complete transcription result with metadata
- Confidence scores for each segment
- Timestamp information
- Recognition details

### Usage Examples

**Example 1: Quick Transcription**
```bash
python3 scripts/transcribe.py recording.wav
```
Output: Transcript text printed to console

**Example 2: Save to File**
```bash
python3 scripts/transcribe.py interview.mp3 --format mp3 --out transcript.txt
```
Output: Transcript saved to `transcript.txt`

**Example 3: JSON Output with Metadata**
```bash
python3 scripts/transcribe.py audio.m4a --json --out result.json
```
Output: Complete JSON result with timestamps and confidence scores

**Example 4: Domain-Specific Transcription**
```bash
python3 scripts/transcribe.py financial_call.wav --domain finance
```
Output: Transcript optimized for financial terminology

### How It Works

The script uses the UniCloud ASR API with the following workflow:

1. **Initialize upload** — Get a task ID from the API / 初始化上传，获取任务ID
2. **Upload audio file** — Upload the audio file to the server / 上传音频文件到服务器
3. **Start transcription** — Submit the transcription task / 提交转写任务
4. **Poll for results** — Wait for transcription to complete (typically 10-60 seconds) / 轮询等待转写完成（通常10-60秒）
5. **Return transcript** — Output the recognized text / 输出识别文本

> **Privacy**: Audio files are uploaded directly to UniCloud servers. No data is sent to third-party services.
>
> **隐私说明**：音频文件直接上传到云知声服务器。不会将数据发送到第三方服务。

### Supported Formats

**Supported file types**:
- WAV
- MP3
- M4A
- FLAC
- OGG

**Limits**:
- Maximum duration: 2 hours
- Maximum file size: 100MB

Use the `--format` flag to specify the format if auto-detection fails:

```bash
python3 scripts/transcribe.py audio.mp3 --format mp3
```

## First-Time Configuration

**When API is not configured**:

The error will show:
```
CONFIG_ERROR: UNISOUND_APPKEY or UNISOUND_SECRET not configured.
```

### Obtaining Credentials

To use this skill, you need API credentials from UniCloud (云知声):

您需要从云知声获取 API 凭据：

1. **Contact UniCloud** to obtain your API credentials
   联系云知声获取您的 API 凭据

2. **You will receive**:
   您将收到：
   - **AppKey**: Application key / 应用密钥
   - **Secret**: Secret key for authentication / 认证密钥
   - **UserId**: Your user identifier / 用户标识
   - **Base URL**: API endpoint URL / API 端点地址

### Test Credentials (UAT Environment)

**For testing and evaluation only** (用于测试和评估):

```yaml
AppKey:    681e01d78d8a40e8928bc8268020639b
Secret:    d7b2980cb61843d69fdab5e99deafcdf
UserId:    unisound-python-demo
Base URL:  http://af-asr.uat.hivoice.cn
```

> **⚠️ Important Security Notice / 重要安全提示**
>
> - **Test environment only** — These credentials are for UAT testing only
>   - **仅测试环境** — 这些凭据仅用于 UAT 测试
> - **No sensitive data** — Never use with production or sensitive audio files
>   - **勿用于敏感数据** — 切勿用于生产或敏感音频文件
> - **Get your own credentials** — For production use, contact UniCloud
>   - **获取自己的凭据** — 生产环境请联系云知声
> - **Data privacy** — Audio files are uploaded to UniSound servers
>   - **数据隐私** — 音频文件将上传至云知声服务器

### Configuration Steps

**Guide the user to configure securely**:
- Recommend configuring through environment variables or `.env` file
- Recommend using the host application's configuration method when possible
- Warn about sharing credentials in chat (may be stored in conversation history)

**Required environment variables**:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `UNISOUND_APPKEY` | **Yes** | Application key / 应用密钥 | - |
| `UNISOUND_SECRET` | **Yes** | Secret key / 认证密钥 | - |
| `UNISOUND_USERID` | No | User identifier / 用户标识 | `unisound-python-demo` |
| `UNISOUND_BASE_URL` | No | API base URL / API 基础地址 | `http://af-asr.uat.hivoice.cn` |
| `UNISOUND_DOMAIN` | No | Recognition domain / 识别领域 | `other` |
| `UNISOUND_AUDIOTYPE` | No | Default audio format / 默认音频格式 | `wav` |

**Configuration examples**:

*Linux/macOS:*
```bash
export UNISOUND_APPKEY="681e01d78d8a40e8928bc8268020639b"
export UNISOUND_SECRET="d7b2980cb61843d69fdab5e99deafcdf"
export UNISOUND_USERID="unisound-python-demo"
```

*Windows (PowerShell):*
```powershell
$env:UNISOUND_APPKEY="681e01d78d8a40e8928bc8268020639b"
$env:UNISOUND_SECRET="d7b2980cb61843d69fdab5e99deafcdf"
$env:UNISOUND_USERID="unisound-python-demo"
```

*Using .env file (Recommended):*
```
UNISOUND_APPKEY=681e01d78d8a40e8928bc8268020639b
UNISOUND_SECRET=d7b2980cb61843d69fdab5e99deafcdf
UNISOUND_USERID=unisound-python-demo
```

> **Security Note**: Never commit `.env` files or actual credentials to version control.
> **安全提示**：切勿将 `.env` 文件或实际凭据提交到版本控制系统。

## Error Handling

**Authentication failed**:
```
API returned error: 401
```
→ AppKey or Secret is invalid, reconfigure with correct credentials
→ AppKey 或 Secret 无效，请重新配置正确的凭据

**Network error**:
```
Connection timeout
```
→ Check network connectivity to UniCloud API
→ 检查到云知声 API 的网络连接

**Audio file not found**:
```
错误: 音频文件不存在
```
→ Check the file path, use absolute path if needed
→ 检查文件路径，必要时使用绝对路径

**Transcription timeout**:
```
转写超时
```
→ Transcription is taking longer than expected (server may be busy)
→ 转写时间过长（服务器可能繁忙）
→ Try again later / 稍后重试
→ Check if the audio file is too large / 检查音频文件是否过大

**Unsupported audio format**:
```
Unsupported audio format
```
→ The audio format is not supported by the API
→ API 不支持该音频格式
→ Convert to a supported format (WAV recommended) / 转换为支持的格式（推荐 WAV）
→ Use `--format` flag to explicitly specify the format / 使用 `--format` 参数显式指定格式

```bash
# Convert using ffmpeg / 使用 ffmpeg 转换
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
```

**API quota exceeded**:
```
API returned error: 429
```
→ Too many requests, wait before retrying
→ 请求过多，请稍后重试

## Important Notes

- **Requires network connectivity** to UniCloud ASR API
  **需要网络连接**到云知声 ASR API
- **Cloud-based processing** - Audio files are uploaded to UniSound servers
  **云端处理**——音频文件会上传到云知声服务器
- **File size limits**: Maximum 2 hours duration, 100MB file size
  **文件大小限制**：最长 2 小时，最大 100MB
- **Domain optimization**: Use appropriate `--domain` for better accuracy
  **领域优化**：使用适当的 `--domain` 以获得更高的准确率
- **Test credentials**: UAT environment credentials are for testing only
  **测试凭据**：UAT 环境凭据仅供测试使用

## Security Best Practices

**For production deployment / 生产部署**:

- **Obtain your own credentials** from UniCloud / 云知声
  从云知声获取您自己的凭据
- **Use environment variables** — Never embed production credentials in scripts or configuration files
  **使用环境变量**——切勿在脚本或配置文件中嵌入生产凭据
- **Review privacy policy** — Audio files are uploaded to UniSound servers; review their privacy policy
  **审查隐私政策**——音频文件会上传到云知声服务器；请查看其隐私政策
- **Test with non-sensitive data first** — Always test with non-sensitive audio files first
  **首先使用非敏感数据进行测试**——始终先使用非敏感音频文件进行测试

## Troubleshooting

**Issue**: Script fails with import error
→ Ensure dependencies are installed: `pip install -r scripts/requirements.txt`
→ Ensure using Python 3.8 or later / 确保使用 Python 3.8 或更高版本

**Issue**: Cannot connect to API server
无法连接到 API 服务器
→ Check network connectivity / 检查网络连接
→ Verify API endpoint URL is correct / 验证 API 端点 URL 是否正确
→ Try using a different network / 尝试使用其他网络

**Issue**: Poor transcription quality
→ Check audio quality (background noise, clarity) / 检查音频质量（背景噪音、清晰度）
→ Try using appropriate `--domain` parameter / 尝试使用适当的 `--domain` 参数
→ Ensure audio format is correct / 确保音频格式正确

## Getting Help

If you encounter issues not covered here:
如果遇到未涵盖的问题：

1. Check the UniCloud ASR documentation for the latest API changes
   查看云知声 ASR 文档了解最新的 API 变更

2. Verify your network connection to the API server
   验证到 API 服务器的网络连接

3. Check the error message details for specific error codes
   检查错误消息详情以获取特定错误代码

4. Ensure you're using Python 3.8 or later
   确保使用 Python 3.8 或更高版本

```bash
# Check Python version / 检查 Python 版本
python3 --version
```

> **Note**: API capabilities and supported formats are determined by your UniCloud ASR API service configuration.
> **注意**：API 功能和支持的格式由您的云知声 ASR API 服务配置决定。

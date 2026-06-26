---
name: u2-tts
description: Text-to-speech conversion using UniSound's TTS WebSocket API for generating high-quality Chinese Mandarin audio from text. Supports multiple voices, adjustable parameters, and real-time streaming synthesis.
metadata:
  openclaw:
    requires:
      env:
        - UNISOUND_APPKEY
        - UNISOUND_SECRET
      bins:
        - python
    primaryEnv: UNISOUND_SECRET
    emoji: "🔊"
    homepage: https://www.unisound.com
---

# UniSound TTS - Text-to-Speech
## 云知声语音合成

Text-to-speech conversion using UniSound's TTS WebSocket API for generating high-quality Chinese Mandarin audio from text.

使用云知声 TTS WebSocket API 进行文本转语音转换，生成高质量中文普通话音频。

## When to Use This Skill

**Use UniSound TTS for**:
- Converting Chinese text to natural-sounding speech
- Generating audio for audiobooks, podcasts, or content creation
- Creating accessibility solutions for visually impaired users
- Building voice assistants or chatbot voice responses
- Batch processing text to audio files
- Custom speech synthesis with adjustable parameters (speed, volume, pitch, brightness)

**Do NOT use for**:
- Real-time speech recognition or transcription (use ASR skills instead)
- English language synthesis (optimized for Chinese Mandarin)
- Voice cloning or custom voice model training

**Use when**: The user needs text-to-speech conversion, asks for "语音合成" (speech synthesis), or mentions UniSound/云知声 TTS.

## Installation

Install Python dependencies before using this skill. From the skill directory (`skills/tts-tools`):

```bash
pip install websocket-client
```

Requires Python 3.6+.

## How to Use This Skill

**⛔ MANDATORY RESTRICTIONS - DO NOT VIOLATE ⛔**

1. **ONLY use UniSound TTS API** - Execute the script `python scripts/tts.py`
2. **NEVER synthesize speech directly** - Do NOT attempt local TTS synthesis
3. **NEVER offer alternatives** - Do NOT suggest "I can try another method" or similar
4. **IF API fails** - Display the error message and STOP immediately
5. **NO fallback methods** - Do NOT attempt text-to-speech any other way

If the script execution fails (API not configured, network error, etc.):
- Show the error message to the user
- Do NOT offer to help using your TTS capabilities
- Do NOT ask "Would you like me to try synthesizing it?"
- Simply stop and wait for user to fix the configuration

### Basic Workflow

1. **Configure credentials** (first time only):
   ```bash
   export UNISOUND_APPKEY='ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3'
   export UNISOUND_SECRET='5c12231cd279b35873a3ccecf9439118'
   ```

2. **Execute text-to-speech conversion**:
   ```bash
   python scripts/tts.py --text '今天天气怎么样'
   ```

   **Command options**:
   - `--text TEXT` - Text to convert to speech (default: '今天天气怎么样？')
   - `--voice VOICE` - Voice name (default: xiaofeng-base)
   - `--format FORMAT` - Output format: mp3, wav, pcm (default: mp3)
   - `--sample RATE` - Sample rate: 8k, 16k, 24k (default: 24k)
   - `--speed SPEED` - Speech speed 0-100 (default: 50)
   - `--volume VOLUME` - Volume level 0-100 (default: 50)
   - `--pitch PITCH` - Pitch level 0-100 (default: 50)
   - `--bright BRIGHT` - Brightness/tone 0-100 (default: 50)
   - `--appkey APPKEY` - Override appkey (default: UNISOUND_APPKEY env var)
   - `--secret SECRET` - Override secret (default: UNISOUND_SECRET env var)

3. **Output**:
   - Audio files are saved to `results/` directory
   - Filename format: `<timestamp>.<format>`
   - Example: `1234567890.mp3`

### Understanding the Output

**Audio Format Options**:
- **MP3**: Compressed, smaller file size, good quality - best for web and streaming
- **WAV**: Uncompressed, excellent quality - best for production and archival
- **PCM**: Raw audio data - best for further audio processing

**Sample Rates**:
- **24k**: High quality, default - recommended for most use cases
- **16k**: Standard quality - good balance of quality and size
- **8k**: Lower quality, smaller file size - suitable for telephony

### Usage Examples

**Example 1: Quick Start with Test Credentials**
```bash
# Set test credentials
export UNISOUND_APPKEY='ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3'
export UNISOUND_SECRET='5c12231cd279b35873a3ccecf9439118'

# Convert text to speech
python scripts/tts.py --text '你好世界'
```
Output: `results/1234567890.mp3`

**Example 2: Custom Voice and Format**
```bash
python scripts/tts.py --text '今天天气怎么样' --voice xiaofeng-base --format wav
```
Output: High-quality WAV file with male voice

**Example 3: Adjusted Speech Parameters**
```bash
python scripts/tts.py --text '快速朗读' --speed 70 --volume 60 --pitch 50
```
Output: Faster speech with increased volume

**Example 4: High-Quality Audio Production**
```bash
python scripts/tts.py --text '高质量音频' --format wav --sample 24k --volume 60
```
Output: Production-quality WAV file at 24kHz

**Example 5: Command-line Credential Override**
```bash
python scripts/tts.py \
  --text '测试' \
  --appkey 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3' \
  --secret '5c12231cd279b35873a3ccecf9439118'
```

### How It Works

The script uses the UniSound TTS WebSocket API with the following workflow:

1. **Authenticate** using SHA256 signature (appkey + timestamp + secret)
   使用 SHA256 签名进行身份验证
2. **Establish WebSocket connection** to `wss://ws-stts.hivoice.cn/v1/tts`
   建立 WebSocket 连接到云知声 TTS 服务
3. **Send TTS request** with text and voice parameters
   发送包含文本和语音参数的 TTS 请求
4. **Receive streaming audio data** in binary chunks
   以二进制块形式接收流式音频数据
5. **Save audio file** to the results directory
   将音频文件保存到结果目录

### Available Voices

| Voice | Type | Description |
|-------|------|-------------|
| xiaofeng-base | Male | Standard male voice, clear and natural |
| xiaoyan | Female | Female voice options |
| xiaomei | Female | Alternative female voice |
| Custom voices | Various | Contact UniSound for more options |

### Adjustable Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| speed | 0-100 | 50 | Speech speed (50 = normal, higher = faster) |
| volume | 0-100 | 50 | Volume level (50 = normal, higher = louder) |
| pitch | 0-100 | 50 | Pitch level (50 = normal, higher = higher) |
| bright | 0-100 | 50 | Brightness/tone (50 = normal) |

**Recommended settings**:
- Audiobooks: speed 45, pitch 50
- News/announcements: speed 55, volume 60, bright 60
- Accessibility: speed 35-40, volume 70
- Normal conversation: speed 50, all parameters 50

## First-Time Configuration

**When credentials are not configured**:

The script will show:
```
Error: AppKey and Secret are required!
Set them via --appkey/--secret arguments or UNISOUND_APPKEY/UNISOUND_SECRET environment variables.
```

### Test Credentials

For testing and evaluation, use these credentials:

用于测试和评估，请使用以下凭据：

```bash
export UNISOUND_APPKEY='ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3'
export UNISOUND_SECRET='5c12231cd279b35873a3ccecf9439118'
```

> **⚠️ Important Security Notice / 重要安全提示**
>
> - **Test credentials only** — These are for testing and evaluation purposes
>   - **仅测试凭据**——这些凭据仅供测试和评估使用
> - **No sensitive data** — Never use with production or sensitive content
>   - **勿用于敏感数据**——切勿用于生产或敏感内容
> - **Get your own credentials** — For production use, contact UniSound
>   - **获取自己的凭据**——生产环境请联系云知声
> - **Data privacy** — Text is sent to UniSound servers for processing
>   - **数据隐私**——文本将发送至云知声服务器进行处理

### Obtaining Production Credentials

For production use, obtain API credentials from UniSound (云知声):

用于生产环境时，请从云知声获取 API 凭据：

1. **Contact UniSound** to obtain your API credentials
   联系云知声获取您的 API 凭据
   Visit: https://www.unisound.com/

2. **You will receive**:
   您将收到：
   - **AppKey**: Application key / 应用密钥
   - **Secret**: Secret key for authentication / 认证密钥

### Configuration Methods

**Method 1: Environment Variables (Recommended)**

*Linux/macOS:*
```bash
export UNISOUND_APPKEY='ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3'
export UNISOUND_SECRET='5c12231cd279b35873a3ccecf9439118'
python scripts/tts.py --text '你好'
```

*Windows (PowerShell):*
```powershell
$env:UNISOUND_APPKEY='ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3'
$env:UNISOUND_SECRET='5c12231cd279b35873a3ccecf9439118'
python scripts/tts.py --text '你好'
```

*Windows (CMD):*
```cmd
set UNISOUND_APPKEY=ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3
set UNISOUND_SECRET=5c12231cd279b35873a3ccecf9439118
python scripts/tts.py --text '你好'
```

**Method 2: .env File (Recommended for Development)**

Create a `.env` file in the project root:
```
UNISOUND_APPKEY=ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3
UNISOUND_SECRET=5c12231cd279b35873a3ccecf9439118
```

Then use with `python-dotenv` or load in your shell.

> **Security Note**: Never commit `.env` files or actual production credentials to version control.
> **安全提示**：切勿将 `.env` 文件或实际生产凭据提交到版本控制系统。

**Method 3: Command-Line Arguments**

```bash
python scripts/tts.py \
  --text '你好世界' \
  --appkey 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3' \
  --secret '5c12231cd279b35873a3ccecf9439118'
```

### Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `UNISOUND_APPKEY` | **Yes** | Application key / 应用密钥 |
| `UNISOUND_SECRET` | **Yes** | Secret key / 认证密钥 |

### Python API Usage

**Basic Python API**:

```python
import os
from scripts.tts import Ws_parms, do_ws, write_results

# Get credentials from environment variables
appkey = os.getenv('UNISOUND_APPKEY', 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3')
secret = os.getenv('UNISOUND_SECRET', '5c12231cd279b35873a3ccecf9439118')

# Configure TTS parameters
ws_parms = Ws_parms(
    url='wss://ws-stts.hivoice.cn/v1/tts',
    appkey=appkey,
    secret=secret,
    pid=1,
    vcn='xiaofeng-base',
    text='你好，欢迎使用云知声语音合成服务！',
    tts_format='mp3',
    tts_sample='24k',
    user_id='my-app',
)

# Execute TTS conversion
do_ws(ws_parms)

# Save result to file
write_results(ws_parms)
print('Audio saved to results/ directory!')
```

## Error Handling

**Authentication failed**:
```
Error: AppKey and Secret are required!
```
→ Credentials not provided
→ Set UNISOUND_APPKEY and UNISOUND_SECRET environment variables
→ 未提供凭据，请设置环境变量

**WebSocket connection error**:
```
WebSocket error: ...
```
→ Check network connectivity to UniSound API
→ Verify the API endpoint URL is correct
→ Check if firewall is blocking WebSocket connections
→ 检查网络连接和防火墙设置

**No audio data received**:
```
Error: No audio data received
```
→ Text may be empty or contain invalid characters
→ Check the text parameter is not empty
→ Verify text encoding is UTF-8
→ Credentials may be invalid
→ 检查文本内容、编码和凭据

**Invalid speech parameter**:
```
Error: speed must be between 0 and 100, got 150
```
→ Speech parameters must be between 0 and 100
→ 语音参数必须在 0 到 100 之间

**WebSocket connection timeout**:
```
WebSocket error: timeout
```
→ Network connection issue
→ API service may be temporarily unavailable
→ Check internet connection
→ 网络连接问题或服务暂时不可用

## Advanced Usage

### Custom Speech Parameters

```python
import os
from scripts.tts import Ws_parms, do_ws, write_results

appkey = os.getenv('UNISOUND_APPKEY', 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3')
secret = os.getenv('UNISOUND_SECRET', '5c12231cd279b35873a3ccecf9439118')

ws_parms = Ws_parms(
    url='wss://ws-stts.hivoice.cn/v1/tts',
    appkey=appkey,
    secret=secret,
    pid=1,
    vcn='xiaofeng-base',
    text='这是自定义参数的语音合成示例',
    tts_format='wav',
    tts_sample='24k',
    user_id='demo',
)

# Customize speech parameters
ws_parms.tts_speed = 60   # Faster speech (0-100)
ws_parms.tts_volume = 70  # Louder volume (0-100)
ws_parms.tts_pitch = 40   # Lower pitch (0-100)
ws_parms.tts_bright = 60  # Brighter tone (0-100)

do_ws(ws_parms)
write_results(ws_parms)
```

### Batch Text Processing

```python
import os
from scripts.tts import Ws_parms, do_ws, write_results

def batch_tts(text_list):
    """Convert multiple texts to audio files"""
    appkey = os.getenv('UNISOUND_APPKEY', 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3')
    secret = os.getenv('UNISOUND_SECRET', '5c12231cd279b35873a3ccecf9439118')

    for i, text in enumerate(text_list):
        ws_parms = Ws_parms(
            url='wss://ws-stts.hivoice.cn/v1/tts',
            appkey=appkey,
            secret=secret,
            pid=i,
            vcn='xiaofeng-base',
            text=text,
            tts_format='mp3',
            tts_sample='24k',
            user_id=f'batch-{i}',
        )

        do_ws(ws_parms)
        write_results(ws_parms)
        print(f"Generated: {text[:30]}...")

# Usage
texts = [
    "第一段文字",
    "第二段文字",
    "第三段文字"
]
batch_tts(texts)
```

### Audiobook Chapter Converter

```python
import os
from scripts.tts import Ws_parms, do_ws, write_results

def convert_chapter(chapter_text, chapter_num, voice='xiaofeng-base'):
    """Convert a book chapter to audio file"""
    # Add chapter announcement
    intro = f"第{chapter_num}章。"
    full_text = intro + chapter_text

    appkey = os.getenv('UNISOUND_APPKEY', 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3')
    secret = os.getenv('UNISOUND_SECRET', '5c12231cd279b35873a3ccecf9439118')

    ws_parms = Ws_parms(
        url='wss://ws-stts.hivoice.cn/v1/tts',
        appkey=appkey,
        secret=secret,
        pid=chapter_num,
        vcn=voice,
        text=full_text,
        tts_format='mp3',
        tts_sample='24k',
        user_id=f'audiobook-ch{chapter_num}',
    )

    # Slower, clearer reading for books
    ws_parms.tts_speed = 45
    ws_parms.tts_pitch = 50

    do_ws(ws_parms)
    write_results(ws_parms)
    print(f"Chapter {chapter_num} converted")

# Usage
chapter = """这是第一章的内容。在一个阳光明媚的早晨，
主人公开始了他的冒险之旅。"""
convert_chapter(chapter, 1)
```

### Accessibility Helper

```python
import os
from scripts.tts import Ws_parms, do_ws, write_results

def accessibility_reader(text, speed='normal', voice='xiaofeng-base'):
    """
    Text-to-speech for accessibility (visually impaired users)
    with customizable reading speed
    """
    speed_map = {
        'slow': 35,
        'normal': 50,
        'fast': 65
    }

    appkey = os.getenv('UNISOUND_APPKEY', 'ce44uxf7g5eag2cv33qvlp5d22qrkgcezvgfp2q3')
    secret = os.getenv('UNISOUND_SECRET', '5c12231cd279b35873a3ccecf9439118')

    ws_parms = Ws_parms(
        url='wss://ws-stts.hivoice.cn/v1/tts',
        appkey=appkey,
        secret=secret,
        pid=1,
        vcn=voice,
        text=text,
        tts_format='mp3',
        tts_sample='24k',
        user_id='accessibility',
    )

    ws_parms.tts_speed = speed_map.get(speed, 50)
    ws_parms.tts_volume = 70  # Higher volume for accessibility

    do_ws(ws_parms)
    write_results(ws_parms)
    return ws_parms.tts_stream

# Usage
article = "这是一篇重要的新闻文章。"
accessibility_reader(article, speed='slow')
```

## Important Notes

- **Chinese language optimized** - Best results with Simplified Chinese text
  **中文优化**——简体中文文本效果最佳
- **Requires stable internet connection** for WebSocket streaming
  **需要稳定的网络连接**进行 WebSocket 流式传输
- **Audio files saved locally** - Check `results/` directory for output
  **音频文件保存在本地**——输出文件在 `results/` 目录
- **Text encoding** - Ensure text is UTF-8 encoded
  **文本编码**——确保文本为 UTF-8 编码
- **Default sample rate is 24k** - Higher quality than standard 16k
  **默认采样率为 24k**——比标准 16k 质量更高
- **Test credentials** - Provided for testing and evaluation only
  **测试凭据**——提供的凭据仅供测试和评估使用

## Security Best Practices

- **For testing** - Use the provided test credentials
  **测试使用**——使用提供的测试凭据
- **For production** - Always obtain your own credentials from UniSound
  **生产环境**——始终从云知声获取您自己的凭据
- **Use environment variables** - Store credentials securely in environment variables
  **使用环境变量**——安全地将凭据存储在环境变量中
- **Never hardcode credentials** - Don't embed production credentials in code
  **切勿硬编码凭据**——不要在代码中嵌入生产凭据
- **Use .env files** - For local development (add to .gitignore)
  **使用 .env 文件**——用于本地开发（添加到 .gitignore）
- **Rotate credentials regularly** - In production environments
  **定期轮换凭据**——在生产环境中

## Troubleshooting

**Issue**: Script fails with import error
→ Ensure dependencies are installed: `pip install websocket-client`
→ Ensure using Python 3.6 or later
→ 确保安装依赖并使用 Python 3.6 或更高版本

**Issue**: "AppKey and Secret are required!" error
→ Set UNISOUND_APPKEY and UNISOUND_SECRET environment variables
→ Or use --appkey and --secret command-line arguments
→ 设置环境变量或使用命令行参数

**Issue**: Poor audio quality
→ Try using WAV format with 24k sample rate
→ Adjust speech parameters for your use case
→ 尝试使用 WAV 格式和 24k 采样率

**Issue**: WebSocket connection timeout
→ Check network connectivity
→ Verify firewall allows WebSocket connections
→ Check if API service is operational
→ 检查网络连接和防火墙设置

**Issue**: Generated audio sounds unnatural
→ Adjust speed parameter (try 45-55 range)
→ Check text for proper punctuation
→ Consider breaking long sentences into shorter ones
→ 调整语速参数和文本标点

**Issue**: Test credentials stopped working
→ Test credentials may have expiration or rate limits
→ Contact UniSound to obtain your own credentials
→ 测试凭据可能已过期或达到速率限制
→ 请联系云知声获取您自己的凭据

## Tips and Best Practices

- **For audiobooks**: Use speed 45, add chapter announcements
  **有声读物**：使用速度 45，添加章节说明
- **For accessibility**: Use speed 35-40, higher volume (70)
  **无障碍应用**：使用速度 35-40，更高音量（70）
- **For news**: Use speed 55, brighter tone (60)
  **新闻播报**：使用速度 55，更明亮的语调（60）
- **For batch processing**: Implement delays between requests
  **批量处理**：在请求之间实现延迟
- **For production**: Add error handling and retry logic
  **生产环境**：添加错误处理和重试逻辑
- **For best quality**: Use 24k sample rate with WAV format
  **最佳质量**：使用 24k 采样率和 WAV 格式

## Reference Documentation

- [UniSound Official Site](https://www.unisound.com/)
- [WebSocket Client Documentation](https://websocket-client.readthedocs.io/)
- [TTS API Documentation](https://www.unisound.com/tts-api)

Load these reference documents when:
- Debugging API connection issues
- Understanding advanced features
- Need detailed API parameter information

## Authentication Details

The UniSound TTS API uses SHA256 signature-based authentication:

```python
# Signature format (automatically generated by Ws_parms class)
# SHA256(appkey + timestamp + secret).upper()

# Manual signature example (if needed):
import hashlib
import time

def generate_signature(appkey, secret):
    timestamp = str(int(time.time() * 1000))
    hs = hashlib.sha256()
    hs.update((appkey + timestamp + secret).encode('utf-8'))
    signature = hs.hexdigest().upper()
    return timestamp, signature
```

**WebSocket URL format**:
```
wss://ws-stts.hivoice.cn/v1/tts?time={timestamp}&appkey={appkey}&sign={signature}
```

> **Note**: API capabilities, available voices, and rate limits are determined by your UniSound TTS API service configuration and subscription plan.
> **注意**：API 功能、可用语音和速率限制由您的云知声 TTS API 服务配置和订阅计划决定。

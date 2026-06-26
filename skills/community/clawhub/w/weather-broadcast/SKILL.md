---
name: senseaudio-weather-broadcast
description: Fetch weather data and generate a spoken weather broadcast using SenseAudio TTS.
metadata:
  openclaw:
    emoji: "🌤️"
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn/docs
---

# Weather Broadcast / 天气播报

Fetch real-time weather data and generate a natural-sounding weather broadcast audio using SenseAudio TTS.

获取实时天气数据，并使用 SenseAudio TTS 生成自然流畅的天气播报音频。

## Quick Start / 快速开始

### 1. Get Weather + Generate Broadcast / 获取天气并生成播报

```bash
# Set your API key / 设置 API 密钥
export SENSEAUDIO_API_KEY="your_api_key"

# Fetch weather and generate broadcast for Beijing / 获取北京天气并生成播报
CITY="Beijing"
WEATHER=$(curl -s "wttr.in/${CITY}?format=%l:+%c+%t+%h+%w&lang=zh")

# Generate broadcast text / 生成播报文本
BROADCAST_TEXT="天气播报：${WEATHER}。祝您出行愉快！"

# Call SenseAudio TTS / 调用 SenseAudio TTS
curl -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"SenseAudio-TTS-1.0\",
    \"text\": \"$BROADCAST_TEXT\",
    \"stream\": false,
    \"voice_setting\": {
      \"voice_id\": \"male_0004_a\",
      \"speed\": 0.95
    },
    \"audio_setting\": {
      \"format\": \"mp3\",
      \"sample_rate\": 32000
    }
  }" -o response.json

# Extract and save audio / 提取并保存音频
jq -r '.data.audio' response.json | xxd -r -p > weather_broadcast.mp3
```

## Weather Data Sources / 天气数据源

### wttr.in (Primary / 主要)

Free weather service, no API key required. / 免费天气服务，无需 API 密钥。

```bash
# Quick one-liner / 快速查询
curl -s "wttr.in/Shanghai?format=3"
# Output: Shanghai: ⛅️ +18°C

# Detailed format / 详细格式
curl -s "wttr.in/Shanghai?format=%l:+%c+%t+%h+%w"
# Output: Shanghai: ⛅️ +18°C 65% ↙12km/h

# Chinese output / 中文输出
curl -s "wttr.in/上海?lang=zh&format=3"
```

Format codes / 格式代码:
- `%c` condition / 天气状况
- `%t` temperature / 温度
- `%h` humidity / 湿度
- `%w` wind / 风速
- `%l` location / 地点
- `%m` moon phase / 月相

Options / 选项:
- `?lang=zh` Chinese / 中文
- `?m` metric / 公制
- `?1` today only / 仅今天
- `?0` current only / 仅当前

### Open-Meteo (Fallback / 备用)

Free JSON API for programmatic use. / 免费 JSON API，适合程序化使用。

```bash
# Get coordinates first, then query / 先获取坐标，再查询
# Beijing: 39.9, 116.4
curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.9&longitude=116.4&current_weather=true"
```

## Complete Python Example / 完整 Python 示例

```python
import requests
import os

SENSEAUDIO_API_KEY = os.environ.get("SENSEAUDIO_API_KEY")
TTS_URL = "https://api.senseaudio.cn/v1/t2a_v2"

def get_weather(city: str, lang: str = "zh") -> str:
    """Fetch weather from wttr.in / 从 wttr.in 获取天气"""
    url = f"https://wttr.in/{city}?format=%l:+%c+%t+%h+%w&lang={lang}"
    resp = requests.get(url, timeout=10)
    return resp.text.strip()

def generate_broadcast_text(weather: str, lang: str = "zh") -> str:
    """Generate broadcast script / 生成播报文本"""
    if lang == "zh":
        return f"天气播报：{weather}。<break time=300>请根据天气情况合理安排出行，祝您生活愉快！"
    else:
        return f"Weather report: {weather}. <break time=300>Please plan your day accordingly. Have a great day!"

def text_to_speech(text: str, output_file: str = "weather_broadcast.mp3", voice_id: str = "male_0004_a"):
    """Convert text to speech using SenseAudio TTS / 使用 SenseAudio TTS 转换文本为语音"""
    headers = {
        "Authorization": f"Bearer {SENSEAUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 0.95,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "format": "mp3",
            "sample_rate": 32000
        }
    }

    resp = requests.post(TTS_URL, json=payload, headers=headers, timeout=30)
    result = resp.json()

    if result.get("data") and result["data"].get("audio"):
        audio_bytes = bytes.fromhex(result["data"]["audio"])
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
        print(f"Audio saved: {output_file}")
        print(f"Duration: {result['extra_info']['audio_length']}ms")
        return output_file
    else:
        raise Exception(f"TTS failed: {result.get('base_resp', {}).get('status_msg', 'Unknown error')}")

def weather_broadcast(city: str, output_file: str = "weather_broadcast.mp3", lang: str = "zh"):
    """Main function: fetch weather and generate broadcast / 主函数：获取天气并生成播报"""
    print(f"Fetching weather for {city}...")
    weather = get_weather(city, lang)
    print(f"Weather: {weather}")

    broadcast_text = generate_broadcast_text(weather, lang)
    print(f"Broadcast text: {broadcast_text}")

    print("Generating audio...")
    return text_to_speech(broadcast_text, output_file)

if __name__ == "__main__":
    # Example usage / 示例用法
    weather_broadcast("Beijing", "beijing_weather.mp3", "zh")
    # weather_broadcast("London", "london_weather.mp3", "en")
```

## Voice Options / 音色选项

| Voice ID | Description / 描述 | Style / 风格 |
|----------|-------------------|--------------|
| `male_0004_a` | Warm male / 温暖男声 | News anchor / 新闻主播 |
| `female_0001_a` | Sweet female / 甜美女声 | Friendly / 亲切 |

See [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api) for all available voices.

查看 [SenseAudio 音色列表](https://senseaudio.cn/docs/voice_api) 获取所有可用音色。

## TTS Parameters / TTS 参数

| Parameter / 参数 | Type / 类型 | Default / 默认 | Range / 范围 | Description / 描述 |
|-----------------|-------------|----------------|--------------|-------------------|
| `speed` | float | 1.0 | 0.5-2.0 | Speech rate / 语速 |
| `vol` | float | 1.0 | 0-10 | Volume / 音量 |
| `pitch` | int | 0 | -12 to 12 | Pitch adjustment / 音调 |

## Audio Output / 音频输出

| Format / 格式 | Sample Rate / 采样率 | Use Case / 适用场景 |
|--------------|---------------------|-------------------|
| mp3 | 32000 | General use / 通用 |
| wav | 48000 | High quality / 高品质 |
| pcm | 16000 | IoT devices / 物联网设备 |

## Tips / 提示

1. Use `<break time=500>` to add pauses in broadcast / 使用 `<break time=500>` 在播报中添加停顿
2. Set `speed: 0.95` for clearer broadcast / 设置 `speed: 0.95` 使播报更清晰
3. URL-encode city names with spaces: `New+York` / 城市名有空格时需 URL 编码
4. Use `?lang=zh` for Chinese weather descriptions / 使用 `?lang=zh` 获取中文天气描述

## Error Handling / 错误处理

```python
try:
    weather_broadcast("Beijing")
except requests.exceptions.Timeout:
    print("Request timeout, please retry")
except Exception as e:
    print(f"Error: {e}")
```

## Related / 相关资源

- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api)
- [wttr.in Help](https://wttr.in/:help)
- [Open-Meteo Docs](https://open-meteo.com/en/docs)

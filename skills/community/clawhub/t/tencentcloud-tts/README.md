# 腾讯云语音合成(TTS) Skill包

基于腾讯云语音合成服务的文本转语音技能包，提供简单易用的API接口，专注于基础单次合成功能。

## 🚀 快速开始

### 前置要求

1. **腾讯云账号**: 拥有有效的腾讯云账号
2. **API密钥**: 获取腾讯云API的SecretId和SecretKey
3. **服务开通**: 已开通腾讯云语音合成(TTS)服务

### 环境配置

设置环境变量：
```bash
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"
```

### 基础使用

```python
from scripts.tencent_tts import TextToSpeech

# 创建TTS客户端
tts = TextToSpeech()

# 合成语音
result = tts.synthesize(
    text="欢迎使用腾讯云语音合成服务",
    voice_type=101001,
    codec="mp3",
    output_file="output.mp3"
)

if result["success"]:
    print(f"✅ 合成成功: {result['output_file']}")
else:
    print(f"❌ 合成失败: {result['error']}")
```

## 📋 功能特性

### 核心功能

- ✅ **文本转语音**: 支持任意文本内容转换为高质量语音
- ✅ **多语音类型**: 提供15种不同语音类型选择
- ✅ **多音频格式**: 支持MP3、WAV等常见音频格式
- ✅ **安全认证**: 通过环境变量安全管理API密钥

## 📁 项目结构

```
tencent-tts/
├── SKILL.md                 # Skill包主描述文件
├── README.md               # 本文档
├── scripts/                # 核心功能脚本
│   └── tencent_tts.py      # 主功能类
└── examples/               # 使用示例
    └── basic_usage.py      # 基础使用示例
```

## 🔧 安装和使用

### 直接使用

```bash
# 设置环境变量
export TENCENTCLOUD_SECRET_ID="your-id"
export TENCENTCLOUD_SECRET_KEY="your-key"

# 运行示例
python examples/basic_usage.py
```

### 集成到项目

```python
import sys
import os

# 添加skill包路径
sys.path.append("/path/to/tencent-tts/scripts")

from tencent_tts import TextToSpeech

# 使用技能包功能
tts = TextToSpeech()
result = tts.synthesize("需要合成的文本")
```

## 📖 API参考

### TextToSpeech类

#### 构造函数
```python
tts = TextToSpeech(secret_id=None, secret_key=None)
```

- `secret_id`: 腾讯云SecretId（可选，默认从环境变量读取）
- `secret_key`: 腾讯云SecretKey（可选，默认从环境变量读取）

#### synthesize方法
```python
result = tts.synthesize(
    text: str,
    voice_type: int = 101001,
    codec: str = "mp3",
    output_file: str = "output.mp3"
) -> Dict[str, any]
```

**参数说明:**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|-------|------|------|--------|------|
| text | string | ✅ | - | 要合成的文本内容 |
| voice_type | int | ❌ | 101001 | 语音类型（101001-101015） |
| codec | string | ❌ | mp3 | 音频格式（mp3/wav） |
| output_file | string | ❌ | output.mp3 | 输出文件名 |

**返回值:**

```python
{
    "success": True,           # 是否成功
    "output_file": "path.mp3", # 输出文件路径
    "file_size": 10240,        # 文件大小（字节）
    "voice_type": 101001,      # 使用的语音类型
    "codec": "mp3",            # 音频格式
    "request_id": "req-id"     # 请求ID（用于调试）
}
```

## 🎯 使用示例

### 基础示例

```python
from scripts.tencent_tts import TextToSpeech

tts = TextToSpeech()

# 简单合成
result = tts.synthesize("这是一个简单的语音合成示例。")

# 自定义参数
result = tts.synthesize(
    text="这是自定义参数的示例。",
    voice_type=101002,
    codec="wav",
    output_file="custom.wav"
)
```

## 🔒 安全最佳实践

### API密钥管理

1. **不要硬编码密钥**
   ```python
   # ❌ 错误做法
   tts = TextToSpeech("your-id", "your-key")
   
   # ✅ 正确做法
   tts = TextToSpeech()  # 从环境变量读取
   ```

2. **使用环境变量**
   ```bash
   # 设置环境变量
   export TENCENTCLOUD_SECRET_ID="your-id"
   export TENCENTCLOUD_SECRET_KEY="your-key"
   ```

## 🐛 故障排除

### 常见问题

**Q: 出现认证失败错误**
A: 检查API密钥是否正确设置，确保已开通语音合成服务

**Q: 网络连接失败**
A: 检查网络连接，确保可以访问腾讯云API端点

**Q: 音频文件无法播放**
A: 检查音频格式是否被播放器支持，尝试不同格式

**Q: 文本长度限制**
A: 单次合成文本建议不超过300字符

## 📄 许可证

本项目基于MIT许可证开源。

## 🔗 相关资源

- [腾讯云语音合成文档](https://cloud.tencent.com/document/product/1073)
- [腾讯云API错误码](https://cloud.tencent.com/document/api/1073/37996)

---

**开始使用:** 运行 `python examples/basic_usage.py` 体验语音合成功能！
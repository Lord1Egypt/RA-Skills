# Video Parser Skill

视频解析与转录工具，支持从多平台视频分享链接中提取视频信息，并可将视频语音内容转录为文字。

> **本 Skill 基于 [parse-video-py](https://github.com/wujunwei928/parse-video-py) 项目重构而来，感谢原作者的贡献。**

## 核心功能

- **视频元数据解析**: 支持通过分享链接或视频ID解析 20+ 个主流平台
- **语音转录**: 自动将视频中的语音内容转换为文本
- **图集支持**: 支持解析图文笔记和图集内容
- **双模式解析**: 支持内置解析器和外部 API 两种模式
- **批量处理**: 提供异步接口，支持批量解析

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境（仅转录功能需要）

创建 `.env` 文件：

```env
# SiliconFlow API Key (必填，用于视频转录功能)
api_key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 视频转录模型 (默认: FunAudioLLM/SenseVoiceSmall)
model=FunAudioLLM/SenseVoiceSmall
# 是否自动清理临时文件 (true: 自动清理, false: 保留在 tmp/ 目录中)
auto_cleanup_temp_files=false
```

### 3. 使用脚本

#### 视频元数据解析

```bash
# 列出支持的平台
python scripts/skill.py --list_platforms

# 通过链接解析
python scripts/skill.py --url "https://v.douyin.com/xxxxxx"
```

#### 视频语音转录

```bash
# 基础转录
python scripts/transcribe.py --url "https://v.douyin.com/xxxxxx"

# 指定 API Key 和模型
python scripts/transcribe.py --url "https://www.xiaohongshu.com/explore/xxxx" --api-key sk-your-key --model FunAudioLLM/SenseVoiceSmall

# 保留临时文件
python scripts/transcribe.py --url "https://www.bilibili.com/video/xxxx" --auto_cleanup false
```

## 命令行参数说明

### `scripts/skill.py`

| 参数 | 说明 | 必需 |
|------|------|------|
| `--url` | 要解析的视频分享链接 | 否 |
| `--list_platforms` | 列出所有支持的平台 | 否 |

### `scripts/transcribe.py`

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | **必需**。要解析的视频分享链接 | 无 |
| `--api_key` | SiliconFlow API 密钥 | 从 .env 读取 |
| `--model` | 语音识别模型名称 | `FunAudioLLM/SenseVoiceSmall` |
| `--parse_result` | 已解析的结果 JSON 字符串 | 无 |
| `--auto_cleanup` | 是否自动清理临时文件 | 从 .env 读取 |
| `--use_local_parser` | 是否使用本地解析器 | 从 .env 读取 |

## 支持的平台

| 平台 | 标识符 | 平台 | 标识符 |
|------|--------|------|--------|
| 抖音 | douyin | 快手 | kuaishou |
| 小红书 | redbook | 哔哩哔哩 | bilibili |
| 微博 | weibo | 皮皮虾 | pipixia |
| 西瓜视频 | xigua | 微视 | weishi |
| 绿洲 | lvzhou | 最右 | zuiyou |
| 度小视 | quanmin | 梨视频 | lishipin |
| 皮皮搞笑 | pipigaoxiao | 虎牙 | huya |
| A站 | acfun | 逗拍 | doupai |
| 美拍 | meipai | 全民K歌 | quanminkge |
| 六间房 | sixroom | 新片场 | xinpianchang |
| 好看视频 | haokan | Twitter | twitter |

## 输出格式

### 视频解析结果

```json
{
  "video_url": "https://example.com/video.mp4",
  "cover_url": "https://example.com/cover.jpg",
  "title": "视频标题",
  "music_url": "https://example.com/music.mp3",
  "images": [
    {
      "url": "图片链接",
      "live_photo_url": "LivePhoto链接"
    }
  ],
  "author": {
    "uid": "作者ID",
    "name": "作者昵称",
    "avatar": "https://example.com/avatar.jpg"
  }
}
```

### 语音转录结果

```json
{
  "parse_info": {
    "code": 200,
    "msg": "success",
    "data": {
      "video_url": "https://example.com/video.mp4",
      "title": "视频标题",
      "author": {
        "name": "作者名称",
        "avatar": "https://example.com/avatar.jpg"
      }
    }
  },
  "transcription": "这是视频中的语音转录文本内容..."
}
```

## 作为模块使用

### 视频解析

```python
from scripts.skill import parse_video_by_url_sync, get_supported_platforms

# 解析视频
result = parse_video_by_url_sync("https://v.douyin.com/xxxxxx")
print(result)

# 获取支持的平台
platforms = get_supported_platforms()
print(f"支持的平台: {', '.join(platforms)}")
```

### 语音转录

```python
from scripts.transcribe import process_video_transcription, save_to_markdown

# 视频转录
result = process_video_transcription(
    video_url_to_parse="https://v.douyin.com/xxxxxx",
    api_key="your-siliconflow-api-key",
    model="FunAudioLLM/SenseVoiceSmall",
    auto_cleanup=False  # 保留临时文件
)

# 保存为 Markdown
md_file = save_to_markdown(result, "https://v.douyin.com/xxxxxx")
print(f"Markdown 文件已保存: {md_file}")
```

### 异步批量处理

```python
import asyncio
from scripts.skill import parse_video_by_url

async def parse_videos():
    urls = [
        "https://v.douyin.com/xxxxxx",
        "https://v.kuaishou.com/yyyyyy",
        "https://www.xiaohongshu.com/explore/zzzzzz"
    ]
    
    results = await asyncio.gather(*[
        parse_video_by_url(url) for url in urls
    ])
    
    for url, result in zip(urls, results):
        print(f"{url}: {result}")

asyncio.run(parse_videos())
```

## 目录结构

```
yby6-video-parser/
├── scripts/
│   ├── skill.py              # 视频解析主脚本
│   ├── transcribe.py         # 语音转录脚本
│   └── parser/              # 平台解析器
│       ├── base.py           # 基础类
│       ├── douyin.py         # 抖音解析器
│       ├── kuaishou.py       # 快手解析器
│       └── ...              # 其他平台解析器
├── demos/                  # Markdown 报告输出目录
├── tmp/                    # 临时文件存储目录
├── .env.example            # 环境配置示例
├── .env                   # 环境配置文件（需自行创建）
├── requirements.txt         # Python 依赖
└── test.py                # 测试脚本
```

## 依赖说明

- `httpx>=0.28.1`: HTTP 客户端
- `fake-useragent>=1.5.1`: 随机 User-Agent 生成
- `requests>=2.28.0`: 视频下载和 API 请求

## 环境要求

- **Python**: 3.10+
- **ffmpeg**: 语音转录功能需要（用于从视频中提取音频）

## 注意事项

1. **网络要求**: 需要网络连接才能正常工作
2. **ffmpeg 依赖**: 语音转录功能必须安装 ffmpeg 并添加到环境变量
3. **API 限制**: 语音转录受 SiliconFlow 额度限制
4. **链接格式**: 建议使用官方 APP 分享的链接
5. **平台变化**: 解析结果可能因平台政策变化而失效
6. **使用规范**: 请遵守各平台的使用条款和版权规定

## 常见问题

### Q: 解析失败怎么办？

A: 可能的原因：
- 平台更新了页面结构或 API
- 视频已被删除或设置为私密
- 链接格式不正确

建议尝试使用官方 APP 分享的链接。

### Q: 如何批量解析多个视频？

A: 使用异步接口可以提高效率（参考上面的"异步批量处理"示例）。

### Q: 临时文件保存在哪里？

A: 临时文件默认保存在 `tmp/视频标题` 目录中，可以通过 `--auto_cleanup false` 参数保留这些文件。

### Q: 语音转录需要多长时间？

A: 取决于视频时长和网络速度，通常 1 分钟视频需要 2-3 分钟。

## 开发指南

如需添加新的平台支持，请：

1. 在 `scripts/parser/` 目录下创建新的解析器文件
2. 继承 `BaseParser` 类并实现 `parse_share_url` 和 `parse_video_id` 方法
3. 在 `scripts/parser/__init__.py` 中注册新平台
4. 在 `scripts/skill.py` 的 `get_supported_platforms` 函数中添加新平台

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

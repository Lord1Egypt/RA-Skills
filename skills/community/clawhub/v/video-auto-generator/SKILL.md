---
name: video-auto-generator
description: 【2026增强版】基于AI自动生成视频内容。支持文本转视频、图文转视频、脚本自动生成+配音+字幕+剪辑全流程。集成edge-tts配音、ffmpeg自动化剪辑。当用户说"生成视频"、"制作视频"、"自动剪辑"、"批量生产视频"、"AI视频生成"、"做个短视频"时触发此技能。
---

# Video Auto Generator - 2026增强版

## 概述

本技能提供端到端的AI视频自动生成能力，从脚本撰写到最终渲染输出，全流程自动化。支持多种视频生成模式，适配抖音、小红书、B站、YouTube等平台。

### 2026年新特性
- **多模态输入**：支持文本、图片、音频、文档等多种输入源
- **AI脚本生成**：使用当前平台模型（如 Claude Fable 5 / Opus 4.8）生成专业视频脚本
- **智能配音**：集成edge-tts，支持多种语言和声音风格
- **自动字幕**：AI识别语音+自动时间轴对齐
- **智能剪辑**：基于内容节奏自动剪辑、转场、配乐
- **批量生产**：支持模板化批量生成（适合自媒体矩阵）
- **剪映AI联动**：支持「营销成片」批量生成带货短视频、「AI文字成片」一键成剧
- **可灵AI 3.0 Omni集成**：全模态原生引擎，角色特征提取+跨视频一致性
- **全自动流水线**：新增 `full_pipeline.py`，一键生成脚本→配音→分镜图→合成视频（92秒1080×1920竖屏）

### 🚀 快速开始（推荐）

```bash
# 一键生成推广视频
cd skills/video-auto-generator/scripts
python full_pipeline.py --topic "你的选题" --duration 90 --voice zh-CN-XiaoxiaoNeural
```

输出：`Desktop/video_<选题>/final_promo.mp4`（竖屏1080×1920）

参数说明：
- `--topic`：视频主题/标题
- `--duration`：时长（秒，默认90）
- `--voice`：配音音色（zh-CN-XiaoxiaoNeural/YunxiNeural/XiaoyiNeural）
- `--output`：自定义输出目录

## 使用场景

- 自媒体批量生产短视频内容
- 企业宣传视频快速制作
- 教育培训视频自动化生成
- 产品介绍视频批量制作
- 个人Vlog快速剪辑

## 核心工作流

本技能采用**任务导向结构**，根据不同需求提供差异化的工作流。

### 任务1：文本转视频（AI虚拟主播）

**适用场景**：新闻播报、知识科普、产品介绍

**工作流程**：

1. **脚本生成**（使用当前session模型）：
   ```
   输入：主题/关键词/参考文档
   输出：分镜脚本（包含：画面描述、配音文案、时长建议）
   ```

2. **AI配音**（使用edge-tts）：
   ```bash
   # 示例：生成配音
   edge-tts --text "欢迎来到我的频道" --voice zh-CN-XiaoxiaoNeural --write-media output.mp3
   ```

3. **画面生成**（可选）：
   - 使用AI绘画工具生成背景图
   - 或使用库存视频素材
   - 或使用虚拟主播形象（HeyGen、D-ID等）

4. **视频合成**（使用ffmpeg）：
   ```bash
   # 示例：配音+字幕+背景视频合成
   ffmpeg -i background.mp4 -i voice.mp3 -vf "subtitles=subtitle.srt" -c:v libx264 -c:a aac output.mp4
   ```

### 任务2：图文转视频（小红书/抖音风格）

**适用场景**：图文笔记转视频、产品展示、教程演示

**工作流程**：

1. **图片序列处理**：
   - 输入：多张图片 + 文案
   - 处理：统一尺寸、添加过渡动画、添加背景音乐

2. **自动配音**（基于文案）：
   ```python
   # 使用edge-tts批量生成配音
   import subprocess
   
   def generate_voice(text, output_file):
       cmd = f"edge-tts --text '{text}' --voice zh-CN-XiaoxiaoNeural --write-media {output_file}"
       subprocess.run(cmd, shell=True)
   ```

3. **视频合成**：
   - 每张图片展示时长自动匹配配音时长
   - 添加转场效果（淡入淡出、滑动等）
   - 添加背景音乐（自动音量调节）

### 任务3：长视频自动剪辑（Vlog/教程）

**适用场景**：直播回放剪辑、课程视频制作、Vlog快速成片

**工作流程**：

1. **智能分段**（使用AI）：
   - 输入：长视频文件
   - 分析：语音识别 + 场景切换检测
   - 输出：精彩片段时间戳列表

2. **AI生成标题和封面**：
   - 使用当前平台模型根据内容生成吸引眼球的标题
   - 使用AI提取关键帧作为封面

3. **自动剪辑**：
   ```bash
   # 示例：根据时间戳列表剪辑精彩片段
   ffmpeg -i input.mp4 -ss 00:01:23 -t 00:00:45 -c copy output_part1.mp4
   ```

4. **批量渲染**：
   - 支持同时处理多个视频
   - 自动添加片头片尾、水印、字幕

### 任务4：模板化批量生产（自媒体矩阵）

**适用场景**：同一内容适配多个平台、多语言版本、A/B测试

**工作流程**：

1. **创建视频模板**：
   - 定义：分辨率、帧率、转场效果、配乐
   - 预留：文本占位符、图片占位符、配音占位符

2. **批量填充内容**：
   ```python
   # 示例：批量生成10个变体视频
   for i in range(10):
       script = generate_script_variant(topic, style=i%3)
       voice = generate_voice(script)
       video = render_video(template, script, voice)
       save(video, f"output_v{i}.mp4")
   ```

3. **平台自适应**：
   - 自动调整分辨率（抖音9:16、B站16:9、小红书3:4）
   - 自动生成平台定制化标题和标签

## 技术栈

### 环境安装（必须先执行）

**必须工具安装**（如果未安装，请先调用 `qclaw-env` skill）：

```powershell
# 1. 安装 ffmpeg (Windows)
winget install ffmpeg
# 验证：ffmpeg -version

# 2. 安装 edge-tts (Python包)
pip install edge-tts
# 验证：edge-tts --list-voices | Select-String "zh-CN"

# 3. 安装 whisper (可选，用于语音识别)
pip install openai-whisper
# 验证：whisper --help

# 4. 安装 ffmpeg-python (Python绑定)
pip install ffmpeg-python
```

**可灵AI 3.0 API配置**（推荐）：

1. 访问 https://klingai.com/ 注册开发者账号
2. 申请API Key（进入「开发者中心」→「API管理」）
3. 配置环境变量：
```powershell
$env:KLING_API_KEY="your_api_key_here"
```
4. 测试API调用：
```python
import requests

def test_kling_api():
    api_url = "https://api.klingai.com/v3/images/generations"
    headers = {"Authorization": f"Bearer {$env:KLING_API_KEY}"}
    payload = {
        "model": "kling-3.0",
        "prompt": "一个AI机器人正在制作视频",
        "aspect_ratio": "16:9"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    print(response.json())
```

### 核心工具

| 工具 | 用途 | 安装命令 | 实用建议 |
|------|------|----------|---------------|
| **ffmpeg** | 视频处理引擎 | `winget install ffmpeg` | 硬件加速（NVENC/QSV）提升渲染速度 |
| **edge-tts** | AI配音 | `pip install edge-tts` | 优先zh-CN-XiaoxiaoNeural，支持多种声音 |
| **当前session模型** | 脚本生成 | 内置 | model route自动选最优，无需硬编码 |
| **whisper** | 语音识别 | `pip install openai-whisper` | 使用large-v3模型提升准确率 |
| **可灵AI 3.0 API** | AI视频生成 | 申请API Key | 全模态引擎，角色一致性保持 |
| **剪映「营销成片」** | 批量带货视频 | 安装剪映专业版 | 参考抖音爆款自动生成 |
| **Seedance 2.0** | AI视频生成 | 等待2.5版本 | 字节跳动，短视频数据优势 |

### Python脚本示例

#### 脚本1：自动生成视频脚本

创建 `scripts/generate_script.py`：

```python
import json

def generate_video_script(topic, duration=60, style="knowledge"):
    """
    使用当前平台模型生成视频脚本
    
    Args:
        topic: 视频主题
        duration: 目标时长（秒）
        style: 风格（knowledge/entertainment/story）
    
    Returns:
        脚本字典，包含分镜、配音文案、画面描述
    """
    prompt = f"""
    请为以下主题生成一个{duration}秒的视频脚本：
    
    主题：{topic}
    风格：{style}
    
    要求：
    1. 开头3秒必须有强hook（悬念/反转/痛点）
    2. 每个分镜标注时长
    3. 配音文案要口语化，适合配音
    4. 画面描述要具体，方便后续制作
    
    输出格式（JSON）：
    {{
        "title": "视频标题",
        "hooks": ["hook1", "hook2", "hook3"],
        "scenes": [
            {{
                "timestamp": "00:00:00",
                "duration": 3,
                "voiceover": "配音文案",
                "visual": "画面描述",
                "transition": "转场效果"
            }}
        ],
        "bgm_suggestion": "背景音乐风格建议",
        "tags": ["标签1", "标签2"]
    }}
    """
    
    # 由当前 session 模型处理（model route 自动选择最优）
    # 此处仅返回 prompt 供调用方使用
    return {"prompt": prompt, "topic": topic, "duration": duration, "style": style}

if __name__ == '__main__':
    # 示例用法
    script = generate_video_script("AI工具推荐", duration=60, style="knowledge")
    print(json.dumps(script, ensure_ascii=False, indent=2))
```

#### 脚本2：批量视频渲染

创建 `scripts/batch_render.py`：

```python
import subprocess
import json
from pathlib import Path

def render_video(script_file, output_file):
    """
    根据脚本JSON文件渲染视频
    
    Args:
        script_file: 脚本JSON文件路径
        output_file: 输出视频文件路径
    """
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    # 1. 生成配音
    voice_file = "temp_voice.mp3"
    subprocess.run([
        "edge-tts",
        "--text", script['scenes'][0]['voiceover'],
        "--voice", "zh-CN-XiaoxiaoNeural",
        "--write-media", voice_file
    ])
    
    # 2. 合成视频（简化示例，实际应该遍历所有scenes）
    cmd = [
        "ffmpeg",
        "-f", "concat", "-i", "input_list.txt",
        "-i", voice_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_file
    ]
    subprocess.run(cmd)
    
    print(f"✅ 视频已生成：{output_file}")

def batch_render(script_folder, output_folder):
    """
    批量渲染视频
    
    Args:
        script_folder: 脚本文件夹
        output_folder: 输出文件夹
    """
    scripts = Path(script_folder).glob("*.json")
    for script_file in scripts:
        output_file = Path(output_folder) / f"{script_file.stem}.mp4"
        render_video(script_file, output_file)

if __name__ == '__main__':
    batch_render("scripts/", "outputs/")
```

## 定时自动化

配合 `qclaw-cron-skill` 实现定期视频生产：

### 方案A：每日热点视频自动生成

**实际配置**（请先读取 qclaw-cron-skill 获取最新格式）：

- 名称：每日热点视频生成
- 时间：每天 10:00
- 消息：基于今日热点选题TOP3，各生成1个60秒短视频。生成后保存到桌面输出文件夹。

### 方案B：批量内容生产（每周）

**实际配置**：

- 名称：每周内容批量生产
- 时间：每周一 9:00
- 消息：批量生成10个短视频（3个主题，每个3-4个变体）。保存到桌面输出文件夹，生成发布计划表。

## 资源文件

### scripts/

可执行代码，用于视频处理自动化：

- `generate_script.py`：AI脚本生成
- `batch_render.py`：批量视频渲染
- `add_subtitles.py`：自动字幕生成和嵌入
- `smart_clip.py`：智能剪辑（识别精彩片段）
- `platform_adapter.py`：平台格式自适应

### references/

参考文档，加载到上下文以指导视频制作：

- `video_formats.md`：各平台视频格式规范（分辨率、码率、时长限制）
- `script_templates.md`：常见视频类型的脚本模板（开箱即用）
- `tts_voices.md`：edge-tts声音风格指南（适合不同场景的声音选择）
- `editing_tips.md`：视频剪辑技巧（转场、配乐、节奏控制）
- `ai_models_guide.md`：AI模型使用指南（由 model route 自动选择最优模型）

### assets/

模板文件，用于视频输出：

- `templates/`：视频模板目录
  - `tpl_douyin_9_16/`：抖音竖屏模板
  - `tpl_bilibili_16_9/`：B站横屏模板
  - `tpl_xiaohongshu_3_4/`：小红书方屏模板
- `intros/`：片头模板
- `outros/`：片尾模板
- `bgm/`： background music库（无版权音乐）

## 高级技巧

### 1. 使用虚拟主播（HeyGen API）

```python
# 集成HeyGen API实现真人形象播报
import requests

def generate_avatar_video(script, avatar_id="default"):
    """
    使用HeyGen生成虚拟主播视频
    
    Args:
        script: 配音文案
        avatar_id: 虚拟主播ID
    """
    api_url = "https://api.heygen.com/v2/video/generate"
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": script,
                "voice_id": "zh-CN-XiaoxiaoNeural"
            }
        }],
        "dimension": {
            "width": 720,
            "height": 1280
        }
    }
    
    response = requests.post(api_url, json=payload, headers={"X-Api-Key": "YOUR_API_KEY"})
    return response.json()['video_id']
```

### 2. 智能配乐推荐

```python
# 根据视频情感自动推荐BGM
def recommend_bgm(emotion="happy", tempo="medium"):
    """
    推荐背景音乐
    
    Args:
        emotion: 情感（happy/sad/exciting/calm）
        tempo: 节奏（slow/medium/fast）
    """
    bgm_library = {
        "happy_medium": "bgm/happy_upbeat.mp3",
        "sad_slow": "bgm/melancholy_piano.mp3",
        "exciting_fast": "bgm/epic_orchestra.mp3",
        # ... 更多组合
    }
    return bgm_library.get(f"{emotion}_{tempo}", "bgm/default.mp3")
```

### 3. A/B测试自动化

```python
# 自动生成多个标题/封面变体进行A/B测试
def generate_ab_test_variants(video_script):
    """
    生成A/B测试变体
    
    Returns:
        变体列表，每个变体有不同的标题、封面、开头hook
    """
    variants = []
    
    # 变体1：悬念式开头
    variants.append({
        "title": f"没想到{topic}竟然...",
        "hook": "你绝对不知道的真相",
        "thumbnail_style": "mysterious"
    })
    
    # 变体2：干货式开头
    variants.append({
        "title": f"{topic}完整攻略",
        "hook": "今天教你3个技巧",
        "thumbnail_style": "educational"
    })
    
    # 变体3：故事式开头
    variants.append({
        "title": f"我是如何用{topic}改变人生的",
        "hook": "去年这个时候我还...",
        "thumbnail_style": "storytelling"
    })
    
    return variants
```

## 常见问题

### Q1: 渲染速度太慢怎么办？

**A**: 
1. 使用硬件加速：`ffmpeg -hwaccel cuda -i input.mp4 ...`
2. 降低预览质量（最终渲染再用高质量）
3. 使用当前平台模型批量处理（性价比最优）

### Q2: 配音声音不自然？

**A**: 
1. 在文案中加入标点符号和停顿标记（如：逗号、句号、省略号）
2. 使用SSML标签控制语速和语调：`<break time="500ms"/>`
3. 切换不同的edge-tts声音风格

### Q3: 如何避免版权问题？

**A**: 
1. 使用无版权音乐库（YouTube Audio Library、Epidemic Sound）
2. 使用AI生成背景音乐（如：Mubert、AIVA）
3. 图片素材使用Unsplash、Pexels等无版权图库

---

**实用检查清单**：
- [ ] edge-tts已安装且可用？
- [ ] ffmpeg已安装且可用？
- [ ] 剪映v20.2+已安装？（营销成片/AI文字成片功能）
- [ ] 已创建视频输出目录？
- [ ] 已测试至少1个完整视频生成流程？
- [ ] 定时任务参考qclaw-cron-skill最新格式？
- [ ] 可灵AI API Key已申请？（如需使用可灵3.0能力）

**下一步优化方向**：
1. ✅ 集成文生视频工具（可灵3.0 API + Seedance 2.0）+ 已列入技术栈
2. 建立本地视频模板库（抖音9:16、B站16:9、小红书3:4）
3. ✅ edge-tts + ffmpeg 流水线已建立（见任务1/2/3工作流）
4. 添加视频质量自动检查（分辨率、码率、时长）
5. 集成剪映「AI文字成片」一键成剧功能
6. 实现即梦AI网页版自动化操作（利用免费积分）
7. 自动化字幕+特效流水线

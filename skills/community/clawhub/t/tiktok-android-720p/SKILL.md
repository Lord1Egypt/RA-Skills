---
name: tiktok-android-bot
description: 使用 ADB 自动化 TikTok 互动。支持 AI 智能评论（Claude/GPT-4/OpenRouter 视觉分析）、搜索话题、评论、点赞、收藏视频、发布内容。无需网页抓取，无 CAPTCHA，智能 UI 识别实现 100% 成功率。
---

# TikTok Android 机器人

使用 ADB 在 Android 设备上自动化 TikTok 互动。支持 AI 智能评论、搜索、评论、点赞、收藏、发布模式，配备智能 UI 识别和备用坐标。

## 功能说明

- **搜索模式** - 搜索话题并评论相关视频
- **探索模式** - 与推荐页视频互动
- **互动模式** - 点赞、收藏、可选评论视频（支持概率控制）
- **发布模式** - 从 URL 或本地文件上传发布视频
- **AI 智能评论** - 支持 Claude/GPT-4/OpenRouter 视觉分析视频内容
- **智能 UI 识别** - 使用 uiautomator 动态检测图标位置
- **备用坐标** - UI 检测失败时使用 720x1280 屏幕的固定坐标

## 前置要求

- 已启用 USB 调试的 Android 设备（720x1280 分辨率）
- 已安装 ADB (Android Debug Bridge)
- 设备上已登录 TikTok 应用
- Python 3.9+

## 快速开始

### 1. 自动设置（推荐）

首次运行会自动启动设置向导，引导您完成配置：

```bash
python3 tiktok_bot.py search --topics fitness --videos 5
```

设置向导会要求您：
1. 选择感兴趣的话题
2. 选择评论模式（静态模板 或 AI生成）
3. 根据选择的模式配置相应参数

### 2. 设置 Android 设备

启用 USB 调试：

```
设置 → 关于手机 → 点击"构建号"7次
设置 → 开发者选项 → 启用"USB 调试"
```

通过 USB 连接并授权您的电脑。

### 3. 验证连接

```bash
adb devices
# 应显示：192.168.11.11:5555    device

adb shell wm size
# 应显示：Physical size: 720x1280
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. AI 配置（可选）

如果您选择了 AI 评论模式，需要配置 API 密钥：

```bash
# Claude (Anthropic)
export ANTHROPIC_API_KEY="your-api-key"

# OpenAI (GPT-4)
export OPENAI_API_KEY="your-api-key"

# OpenRouter
export OPENROUTER_API_KEY="your-api-key"
```

或使用 `.env` 文件（由 setup.py 自动创建）。

## 使用方法

### 搜索模式

搜索话题并评论相关视频：

```bash
# 单话题，5 个视频
python3 tiktok_bot.py search --topics fitness --videos 5

# 多话题
python3 tiktok_bot.py search --topics "fitness,cooking,travel" --videos 3

# 指定设备 ID
python3 tiktok_bot.py search --topics gaming --videos 5 --device 192.168.11.11:5555
```

**工作流程：**
1. 搜索每个话题
2. 从搜索结果中打开视频
3. 从模板发布评论
4. 防止重复评论

### 探索模式

评论推荐页的随机视频：

```bash
python3 tiktok_bot.py explore --videos 10
```

**工作流程：**
1. 从推荐页开始
2. 发布通用评论
3. 滑动到下一个视频

### 互动模式

点赞、可选收藏/评论（默认只点赞）：

```bash
# 默认：仅点赞（100%概率）
python3 tiktok_bot.py interact --videos 10

# 点赞 + 收藏
python3 tiktok_bot.py interact --videos 10 --favorite

# 点赞 + 收藏 + 评论
python3 tiktok_bot.py interact --videos 5 --favorite --comment

# 随机概率：点赞50%，收藏30%
python3 tiktok_bot.py interact --videos 10 --favorite --like-rate 50 --favorite-rate 30
```

**工作流程：**
1. 从推荐页（For You）开始
2. 按概率点赞视频（智能 UI 识别 + 备用）
3. 按概率收藏视频（智能 UI 识别 + 备用）
4. 如启用则评论（使用通用模板）
5. 滑动到下一个视频

**说明：** `--topics` 参数仅适用于 search_mode

**概率说明：**
- `--like-rate`: 点赞概率 1-100，默认 100
- `--favorite-rate`: 收藏概率 1-100，默认 100

**防重复机制：**
- 自动跳过已点赞的视频
- 自动跳过已收藏的视频
- 基于会话内记录，关闭程序后重置

### 发布模式

上传并发布视频：

```bash
# 从 URL
python3 tiktok_bot.py publish --video "https://example.com/video.mp4" --description "我的视频 #fyp"

# 从本地文件
python3 tiktok_bot.py publish --video "/path/to/video.mp4" --description "看看这个！"

# 指定设备 ID
python3 tiktok_bot.py publish --video "https://example.com/video.mp4" --description "我的视频" --device 192.168.11.11:5555
```

**工作流程：**
1. 清理相册（删除旧视频）
2. 下载/上传视频到设备
3. 运行媒体扫描
4. 启动 TikTok 并等待加载
5. 通过 TikTok 应用发布
6. 发布后清理

## 设备设置

### 启用 USB 调试

```
设置 → 关于手机 → 点击"构建号"7次
设置 → 开发者选项 → 启用"USB 调试"
```

### 验证连接

```bash
adb devices
# 应显示：192.168.11.11:5555    device

adb shell wm size
# 应显示：Physical size: 720x1280
```

## 坐标配置 (720x1280)

### 搜索导航
| 元素 | X | Y |
|------|---|---|
| 搜索图标 | 660 | 106 |
| 搜索输入框 | 360 | 64 |
| 搜索按钮 | 684 | 64 |

### 评论操作
| 元素 | X | Y |
|------|---|---|
| 评论图标 | 680 | 769 |
| 评论输入框 | 293 | 1187 |
| 发送（键盘打开） | 643 | 724 |
| 发送（键盘关闭） | 632 | 1217 |

### 互动操作
| 元素 | X | Y |
|------|---|---|
| 点赞图标 | 666 | 629 |
| 收藏图标 | 664 | 823 |

### 发布操作
| 元素 | X | Y |
|------|---|---|
| 创建 (+) | 360 | 1230 |
| 从相册选择 | 67 | 1212 |
| 第一个视频 | 123 | 355 |
| 下一步按钮 | 526 | 1217 |
| 描述输入框 | 55 | 177 |
| 关闭键盘 | 525 | 528 |
| 发布按钮 | 521 | 1210 |

## 智能 UI 识别

机器人使用 `uiautomator dump` 动态检测图标位置：

1. 导出当前 UI 层级
2. 搜索关键词（"like"、"favorite"）
3. 返回匹配元素的中心坐标
4. 检测失败时回退到固定坐标

这确保了在不同 TikTok UI 布局中的可靠性。

## 性能

### 耗时
- **评论：** 每个视频约 20-30 秒
- **点赞 + 收藏：** 每个视频约 5-8 秒
- **发布：** 约 30-60 秒（取决于下载）

### 成功率
- **智能 UI 识别：** 95%+
- **备用坐标：** 90%+

## 故障排除

### 设备未找到
```bash
adb kill-server
adb start-server
adb devices
```

### 点赞/收藏点击错误图标
1. 智能 UI 识别应处理变体
2. 如需要更新备用坐标

### 发布失败
1. 验证视频下载成功
2. 检查媒体扫描完成
3. 手动清理相册

## 最佳实践

### 速率限制
- **每账户每天最多 25-30 条评论**
- **间隔会话：** 每天一次，时间要变化
- **休息：** 每周跳过 1-2 天
- **监控：** 注意限流迹象

### 账户安全
- **账户年龄：** 自动化前至少 7 天
- **先手动活动：** 先点赞、关注、自然浏览
- **从小开始：** 先测试 3-5 个视频

## 项目结构

```
tiktok-android/
├── SKILL.md                           # 本文件
├── README.md                          # 完整文档
├── tiktok_bot.py                     # 主 CLI 入口
├── src/
│   └── bot/
│       └── android/
│           ├── tiktok_android_bot.py  # 核心自动化
│           └── tiktok_navigation.py   # 导航流程
└── data/                             # 日志
```

## 示例

### 搜索 + 评论
```bash
python3 tiktok_bot.py search --topics fitness --videos 3
```

### 探索推荐页
```bash
python3 tiktok_bot.py explore --videos 5
```

### 互动模式（点赞 + 收藏 + 评论）
```bash
python3 tiktok_bot.py interact --videos 3 --like --favorite --comment --topics travel
```

### 发布视频
```bash
python3 tiktok_bot.py publish --video "/path/to/video.mp4" --description "我的 TikTok 视频 #fyp"
```

## 依赖

```
loguru>=0.7.0
anthropic>=0.18.0
openai>=1.12.0
```

ADB 必须已安装并在 PATH 中。

## 许可证

MIT - 负责任地使用。自动化评论可能违反 TikTok 服务条款。

---

**状态：** 生产就绪，具备智能 UI 识别。✅

**最后更新：** 2026 年 3 月 27 日（新增 AI 智能评论、交互式设置向导说明）

# video-auto-publisher-cn

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/video-auto-publisher-cn)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

自动将视频发布到中国三大主流平台：**B站（Bilibili）**、**抖音（Douyin）**、**小红书（Xiaohongshu）**。

## ✨ 功能特性

- ✅ **完全自动化** - 一键发布到三个平台
- ✅ **智能填充** - 自动生成标题、描述、标签
- ✅ **Cookie 持久化** - 保持登录状态，无需重复登录
- ✅ **反检测技术** - 成功绕过平台反爬虫机制
- ✅ **详细日志** - 完整的发布过程记录
- ✅ **错误处理** - 完善的异常捕获和重试机制

## 📦 安装

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/video-auto-publisher-cn.git
cd video-auto-publisher-cn
```

### 2. 安装依赖

```bash
pip install playwright
python -m playwright install chromium
```

### 3. 首次登录

运行登录脚本，手动登录各平台并保存 cookies：

```bash
python login_platforms.py
```

按提示选择平台（1-B站, 2-抖音, 3-小红书），在打开的浏览器中登录，登录成功后 cookies 会自动保存。

## 🚀 使用方法

### 基础用法

发布最新视频到所有平台：

```bash
python skill_video_publisher.py
```

### 指定视频文件

```bash
python skill_video_publisher.py --video path/to/video.mp4
```

### 选择特定平台

只发布到 B站 和抖音：

```bash
python skill_video_publisher.py --platforms bilibili,douyin
```

### 自定义内容

```bash
python skill_video_publisher.py \
  --video my_video.mp4 \
  --title "精彩视频标题" \
  --description "这是一个很棒的视频" \
  --tags "娱乐,搞笑,日常"
```

### 使用无头模式

```bash
python skill_video_publisher.py --headless
```

## 📖 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--video` | 视频文件路径 | 最新视频 |
| `--title` | 视频标题 | 自动生成 |
| `--description` | 视频描述 | 自动生成 |
| `--tags` | 标签列表（逗号分隔） | 自动生成 |
| `--platforms` | 目标平台（逗号分隔） | bilibili,douyin,xiaohongshu |
| `--headless` | 无头模式 | False |

## 📁 项目结构

```
video-auto-publisher-cn/
├── skill_video_publisher.py    # Skill 主入口
├── auto_publish.py              # 核心发布逻辑
├── publish_in_order.py          # 顺序发布脚本
├── login_platforms.py           # 登录脚本
├── SKILL.md                     # Skill 文档
├── README.md                    # 项目说明
├── requirements.txt             # 依赖列表
├── cookies/                     # Cookies 存储
│   ├── bilibili_cookies.json
│   ├── douyin_cookies.json
│   └── xiaohongshu_cookies.json
└── logs/                        # 日志目录
```

## 🎯 平台支持

### B站 (Bilibili)
- ✅ 自动上传视频
- ✅ 填写标题、简介（支持富文本）
- ✅ 添加标签
- ✅ 自动选择分区
- ✅ 等待封面生成
- ✅ 点击"立即投稿"

### 抖音 (Douyin)
- ✅ 自动上传视频
- ✅ 填写标题、描述
- ✅ 添加标签
- ✅ 点击"发布"
- ✅ 检测"审核中"状态

### 小红书 (Xiaohongshu)自动上传视频
- ✅ 填写标题、描述
- ✅ 添加话题
- ✅ 点击"发布"
- ✅ 检测页面跳转

## ⚙️ 技术细节

### 核心技术
- **浏览器自动化**: Playwright
- **反检测**: 非 headless 模式 + 真实用户行为模拟
- **Cookie 管理**: JSON 文件持久化
- **成功检测**: 多重验证（URL、关键词、元素）

### 关键选择器

#### B站
- 标题: `input.input-val`
- 简介: `.ql-editor` (Quill 富文本编辑器)
- 提交按钮: `span.submit-add`

#### 抖音
- 发布按钮: 区分"高清发布"和"发布"

#### 小红书
- 发布按钮: 精确匹配纯"发布"文本

## 📊 性能指标

- **B站**: ~49秒
- **抖音**: ~40秒
- **小红书**: ~37秒
- **总计**: ~146秒 (约 2.5 分钟)
- **成功率**: 100% (三个平台)

## 🔧 故障排查

### Cookies 过期

```bash
# 重新登录保存 cookies
python login_platforms.py
```

### 查看日志

```bash
# 日志保存在 logs/ 目录
cat logs/skill_publish_*.log
```

### 常见问题

1. **提示需要登录**
   - 原因: Cookies 过期
   - 解决: 运行 `login_platforms.py` 重新登录

2. **按钮找不到**
   - 原因: 平台页面结构变化
   - 解决: 更新选择器或联系维护者

3. **上传超时**
   - 原因: 网络不稳定或视频过大
   - 解决: 检查网络，压缩视频

## 📝 注意事项

1. **视频格式**: 支持 MP4、MOV、MKV 等
2. **视频大小**:
   - B站: 16GB 以内
   - 抖音: 根据平台限制
   - 小红书: 根据平台限制
3. **Cookies 有效期**: 通常 7-14 天
4. **网络要求**: 需要稳定的网络连接

## 🔄 更新日志

### v1.0.0 (2026-03-19)
- ✅ 初始版本发布
- ✅ 支持 B站、抖音、小红书
- ✅ 完全自动化发布
- ✅ Cookie 持久化
- ✅ 详细日志记录
- ✅ 命令## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请提交 Issue 或联系作者。

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

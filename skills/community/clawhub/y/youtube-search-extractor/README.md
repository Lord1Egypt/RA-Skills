# YouTube Search Extractor - YouTube搜索结果视频链接提取器

## 🏠 项目概述

YouTube Search Extractor是一个用于从YouTube搜索结果中自动提取视频链接的技能。它使用`agent-browser`进行浏览器自动化，帮助用户快速获取特定主题的视频资源。

## ✨ 主要功能

### 🚀 自动化搜索
- 使用`agent-browser`模拟真实用户搜索
- 智能等待页面加载完成
- 自动处理搜索结果

### 🔍 精准提取
- 使用正则表达式匹配视频链接模式
- 处理相对链接到绝对链接的转换
- 自动去重和链接清理

### 📋 格式化输出
- 清晰的编号列表
- 完整的YouTube URL格式
- 包含搜索时间戳

### ⚡ 高性能
- 并行处理搜索和提取
- 优化的链接匹配算法
- 容错机制保障稳定运行

## 📦 安装方法

### 1. 安装依赖

```bash
npm install -g agent-browser
agent-browser install
```

### 2. 下载技能

```bash
cd /Users/happy/.openclaw/workspace/skills
git clone https://github.com/openclaw/youtube-search-extractor.git
```

或者通过ClawHub安装：

```bash
clawhub install "YouTube Search Extractor"
```

## 🚀 快速开始

### 基本使用方法

```bash
cd /Users/happy/.openclaw/workspace/skills/youtube-search-extractor

# 方法1: 使用npm脚本
npm run search -- "hydrasynth 实战应用" hydrasynth_links

# 方法2: 直接使用Python脚本
python3 youtube_search_extractor.py "hydrasynth 实战应用" hydrasynth_links
```

### 输出文件

- **`hydrasynth_links.html`** - YouTube搜索结果的HTML页面
- **`hydrasynth_links_links.txt`** - 提取的视频链接列表

## 📖 使用示例

### 示例1: 搜索Hydrasynth实战应用

```bash
npm run search -- "hydrasynth 实战应用" hydrasynth_practical
```

输出内容：
```
# YouTube搜索结果：'hydrasynth 实战应用' (2026-02-26 23:30:00)
# 找到 26 个相关视频

1. https://www.youtube.com/watch?v=O37_qc3jhsc
2. https://www.youtube.com/watch?v=t0Ic87OLHRE
3. https://www.youtube.com/watch?v=NB5D34KDMxs
...
```

### 示例2: 搜索OpenClaw教程

```bash
python3 youtube_search_extractor.py "OpenClaw tutorial" openclaw_tutorial
```

### 示例3: 使用自定义参数

```bash
python3 youtube_search_extractor.py "AI音乐创作" ai_music_links --wait-time 10 --max-links 30
```

## 🎛️ 命令参数

### 基本参数

```bash
python3 youtube_search_extractor.py [搜索关键词] [输出文件名] [可选参数]
```

### 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--headless` | 使用无头浏览器模式 | `--headless` |
| `--wait-time <秒数>` | 页面加载等待时间 | `--wait-time 10` |
| `--max-links <数量>` | 最大提取链接数量 | `--max-links 30` |
| `--debug` | 启用详细输出 | `--debug` |

## 🔧 高级用法

### 自定义提取规则

在`youtube_search_extractor.py`中修改`extract_video_links()`方法：

```python
def extract_video_links(self, html_content):
    patterns = [
        r'href=["\'](/watch\?v=[\w-]+[^"\']*)["\']',
        r'href=["\'](https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+[^"\']*)["\']',
        r'href=["\'](https?://(?:www\.)?youtu\.be/[\w-]+[^"\']*)["\']'
    ]
    # 其他提取逻辑...
```

### 添加搜索模板

在`search_templates`目录中添加搜索模板：

```json
{
  "name": "Hydrasynth Search",
  "keywords": ["hydrasynth", "Hydrasynth", "hydra synth"],
  "description": "搜索Hydrasynth合成器相关的内容",
  "filters": ["hydrasynth"]
}
```

## 📊 性能优化

### 避免被封禁

- 使用适当的等待时间（推荐5-10秒）
- 避免在短时间内进行大量搜索
- 考虑使用代理池分散请求

### 内存优化

- 限制`--max-links`参数
- 及时删除临时文件
- 使用`--headless`模式

## 🔒 安全注意

### 合法使用
- 遵守YouTube的服务条款
- 合理使用API，避免过度请求
- 尊重版权，仅供个人学习使用

### 隐私保护
- 不在代码中硬编码个人信息
- 使用`--headless`模式避免暴露真实IP
- 定期更新依赖库

## 🐛 故障排除

### 常见问题

1. **agent-browser未找到**
   ```bash
   npm install -g agent-browser
   agent-browser install
   ```

2. **页面内容为空**
   ```bash
   # 增加等待时间
   python3 youtube_search_extractor.py "关键词" "输出文件名" --wait-time 10
   ```

3. **网络连接失败**
   ```bash
   # 检查网络连接
   ping youtube.com
   # 使用代理
   python3 youtube_search_extractor.py "关键词" "输出文件名" --proxy "http://localhost:8080"
   ```

### 调试模式

```bash
python3 youtube_search_extractor.py "关键词" "输出文件名" --debug
```

## 📈 贡献指南

我们欢迎您为项目做出贡献！请参考[CONTRIBUTING.md](CONTRIBUTING.md)文件。

## 📄 许可证

本项目采用MIT许可证，可自由使用、修改和分发。

## 📞 支持

如果您有任何问题或建议，请：

1. 创建GitHub Issue
2. 发送邮件到contact@openclaw.com
3. 在Discord社区中提问

## 🌟 项目链接

- **GitHub仓库**: https://github.com/openclaw/youtube-search-extractor
- **ClawHub页面**: https://clawhub.com/skills/youtube-search-extractor
- **agent-browser**: https://github.com/vercel-labs/agent-browser

---

💡 这个技能的设计理念是帮助用户快速获取YouTube上的视频资源，同时保持代码的简单性和可扩展性。希望您使用愉快！

# yt-search-download

多站点视频搜索与下载工具 — Claude Code / OpenClaw Skill

支持 YouTube、B站（Bilibili）等主流平台，集视频搜索、频道浏览、下载、字幕提取于一体。

## 功能

- **多平台搜索**：全站关键词搜索，支持按时间 / 播放量 / 相关度排序
- **频道浏览**：浏览指定频道最新视频，支持频道内关键词搜索
- **下载视频**：支持多种画质（最高 4K），指定保存目录
- **提取音频**：一键下载 MP3
- **下载字幕**：自动生成 SRT（带时间轴）+ TXT（供 AI 总结），支持中英双语
- **中文翻译**：搜索结果为英文时自动附加中文译名
- **视频详情**：查询时长、播放量、简介等元数据

## 安装

```bash
npx skills add yt-search-download
```

或通过 ClawHub 安装：

```bash
clawhub install yt-search-download
```

## 前置条件

1. **YouTube API Key**（仅 YouTube 搜索功能需要）：[Google Cloud Console](https://console.cloud.google.com/) → 启用 YouTube Data API v3 → 创建 API Key
   ```bash
   export YT_BROWSE_API_KEY=your_key   # 写入 ~/.zshrc
   ```

2. **yt-dlp**（下载 / 字幕用）：
   ```bash
   brew install yt-dlp   # macOS
   pip install yt-dlp     # 或 pip
   ```

## 支持平台

| 平台 | 搜索 | 频道浏览 | 下载 | 字幕 |
|------|------|----------|------|------|
| YouTube | ✅ | ✅ | ✅ | ✅ |
| B站（Bilibili） | ✅ | ✅ | ✅ | ✅ |

## 使用场景

在 Claude Code 或 OpenClaw 中直接用自然语言描述需求：

### 🔍 搜索视频

```
"搜索 Lex Fridman 最近更新的 YouTube"
"YouTube 上有什么关于 Claude 4 的最新视频"
"找 Andrej Karpathy 频道的视频，按播放量排序"
```

### 📺 浏览频道

```
"看看 Lex Fridman 最近发了什么视频"
"浏览 @karpathy 的频道，找讲 GPT 的视频"
```

### ⬇️ 下载视频

```
"下载这个视频 https://youtube.com/watch?v=..."
"把这个视频下载到桌面，要 1080p"
```

### 🎵 提取音频

```
"提取这个视频的音频"
"YouTube 转 MP3，只要音频"
```

### 📝 下载字幕（SRT + TXT）

字幕下载自动生成两个文件：
- `.srt`：带时间轴，适合视频剪辑
- `.txt`：保留时间戳，适合交给 AI 总结

```
"下载这个视频的字幕"
"提取英文字幕"
"获取视频文本，交给 AI 总结"
```

### 🔄 典型工作流

**① 找频道最新视频并下载字幕：**
1. "看看 Lex Fridman 最近更新了什么"
2. 选择感兴趣的视频
3. "下载第2个视频的字幕"
4. 得到 `.srt` + `.txt`，丢给 AI 总结

**② 搜索 + 筛选 + 下载：**
1. "搜索 AI safety 相关视频，最近半年，按播放量排序"
2. "下载播放量最高那个"

## 命令行用法

```bash
# 全站搜索
python3 scripts/yt_search.py search "关键词" -n 20 -o date

# 浏览频道
python3 scripts/yt_search.py channel @lexfridman -n 10

# 下载视频
python3 scripts/yt_search.py download "VIDEO_URL" -q 1080p

# 仅下载音频（MP3）
python3 scripts/yt_search.py download "VIDEO_URL" --audio-only

# 视频详情
python3 scripts/yt_search.py info "VIDEO_URL"
```

## 搜索参数

| 参数 | 说明 |
|------|------|
| `-n 20` | 最多返回条数（默认 20） |
| `-o date` | 按时间排序 |
| `-o viewCount` | 按播放量排序 |
| `-o relevance` | 按相关度排序（默认） |
| `--after 2025-01-01` | 发布时间起 |
| `--before 2025-12-31` | 发布时间止 |
| `-c @handle` | 限定频道搜索 |
| `-d` | 显示视频简介 |

## License

MIT

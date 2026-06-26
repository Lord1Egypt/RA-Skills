# SCI 期刊查询工具 (sci-journal-search)

查询 SCI 期刊的详细信息，包括**中科院分区（新锐分区）**、**JCR 分区**、**影响因子**等学术指标。

## 🎯 功能特点

- ✅ **新锐分区查询** — 中科院分区表官方数据（2026 年起由新锐团队发布）
- ✅ **JCR 小类分区** — Web of Science 期刊引证报告分区
- ✅ **LetPub 详细指标** — 影响因子、h-index、CiteScore、审稿周期等
- ✅ **130+ 期刊简称** — 自动识别 NC, TPAMI, JACS 等常见简称
- ✅ **快速 HTTP 查询** — 新锐分区无需浏览器，秒级响应
- ✅ **浏览器自动化** — LetPub 查询完成后自动关闭浏览器

## 📦 安装

### 方式 1：从 ClawHub 安装（推荐）

```bash
clawhub install sci-journal-search
```

### 方式 2：本地安装

```bash
# 下载技能包
wget https://clawhub.com/skills/sci-journal-search.zip

# 解压到 skills 目录
unzip sci-journal-search.zip -d ~/.openclaw/skills/
```

## 🚀 使用方法

### 1. 基础查询（新锐分区）

```bash
cd ~/.openclaw/skills/sci-journal-search/scripts
python3 query.py "期刊名"
```

**示例**：
```bash
# 使用全称
python3 query.py "Nature Communications"

# 使用简称（支持 130+ 常见简称）
python3 query.py "NC"
python3 query.py "TPAMI"
python3 query.py "JACS"
```

**输出示例**：
```
📊 Nature Communications
ISSN: - | EISSN: 2041-1723

【新锐分区（中科院分区）】
  • Multidisciplinary Science (综合性期刊): 1 区 🏆 Top

【JCR 小类分区】
  • MULTIDISCIPLINARY SCIENCES (综合性期刊): 1 区
```

### 2. 查询 LetPub 详细指标

```bash
python3 query.py "期刊名" --letpub
```

**输出示例**：
```
📊 Nature Communications
ISSN: - | EISSN: 2041-1723

【新锐分区（中科院分区）】
  • Multidisciplinary Science (综合性期刊): 1 区 🏆 Top

【JCR 小类分区】
  • MULTIDISCIPLINARY SCIENCES (综合性期刊): 1 区

准备查询 LetPub: Nature Communications
浏览器将在查询完成后自动关闭
{
  "status": "need_browser",
  "journal": "Nature Communications",
  "search_url": "https://www.letpub.com.cn/index.php?page=journalapp&searchname=Nature Communications",
  "action": "open_and_parse",
  "close_browser_after": true
}
```

**Agent 处理流程**：
1. 解析 JSON 配置
2. 调用 `browser.open()` 打开 `search_url`
3. 解析页面内容，提取影响因子、h-index 等指标
4. 输出格式化结果
5. 调用 `browser.close()` 关闭所有标签页
6. 调用 `browser.stop()` 停止浏览器服务

### 3. 仅查询 LetPub

```bash
python3 query-letpub.py "期刊名"
```

## 📚 支持的期刊简称

内置 130+ 常见期刊简称映射，例如：

| 简称 | 全称 |
|------|------|
| NC | Nature Communications |
| TPAMI | IEEE Transactions on Pattern Analysis and Machine Intelligence |
| JACS | Journal of the American Chemical Society |
| TNNLS | IEEE Transactions on Neural Networks and Learning Systems |
| ANGEW | Angewandte Chemie International Edition |
| ... | ... |

完整列表见 `data/abbreviations.json`

## 📊 数据源

| 数据源 | 网址 | 说明 |
|--------|------|------|
| **新锐分区** | https://www.xr-scholar.com | 中科院分区表官方（2026 年起） |
| **LetPub** | https://www.letpub.com.cn | 影响因子、审稿周期等 |

## 🔧 开发

### 目录结构

```
sci-journal-search/
├── SKILL.md                  # OpenClaw 技能说明
├── README.md                 # 本文档
├── package.json              # 包配置
├── data/
│   └── abbreviations.json    # 期刊简称映射表
├── references/
│   └── partition-system.md   # 分区系统参考资料
└── scripts/
    ├── query.py              # 主查询脚本
    └── query-letpub.py       # LetPub 查询脚本
```

### 添加新的期刊简称

编辑 `data/abbreviations.json`：

```json
{
  "mappings": {
    "category_name": {
      "NEW": "New Journal Name"
    }
  }
}
```

### 测试

```bash
# 测试新锐分区查询
python3 scripts/query.py "NC"

# 测试简称扩展
python3 scripts/query.py "TPAMI" --verbose

# 测试 LetPub 查询（需要浏览器）
python3 scripts/query.py "NC" --letpub
```

## ⚠️ 注意事项

1. **新锐分区 = 中科院分区** — 自 2026 年起，中科院期刊分区表由新锐（XinRui）团队发布
2. **LetPub 查询需要浏览器** — 确保已安装 Chrome/Chromium 并配置好 browser 工具
3. **查询后自动关闭浏览器** — v1.5.0+ 会自动关闭所有标签页并停止浏览器服务
4. **数据更新时间** — 新锐分区每年底更新，LetPub 数据实时抓取

## 📝 更新日志

### v1.5.0 (2026-03-25)
- 🐛 修复 `--letpub` 参数使用期刊简称的问题，现在使用扩展后的全称查询 LetPub
- 🐛 修复浏览器查询后完全关闭（关闭所有标签页 + 停止浏览器服务）

### v1.4.0 (2026-03-25)
- ✨ 修复 `--letpub` 参数，现在输出 JSON 配置由 Agent 解析执行浏览器操作

### v1.3.0 (2026-03-24)
- ✨ 交互式 LetPub 查询，查询后自动关闭浏览器

### v1.2.0 (2026-03-24)
- ✨ 新增 130+ 期刊简称映射表

### v1.0.0 (2026-03-23)
- 🎉 初始版本

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 报告 Bug
- 建议新的期刊简称
- 改进查询逻辑

## 📧 联系方式

- GitHub: https://github.com/openclaw/skills
- ClawHub: https://clawhub.com

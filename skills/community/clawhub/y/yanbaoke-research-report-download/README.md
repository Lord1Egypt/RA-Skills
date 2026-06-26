# 研报客 Research Report Download Skill  (yanbaoke-research-report-download)


![banner](./banner.png)

从研报客平台（pc.yanbaoke.cn）搜索和下载研究报告的 OpenClaw Skill。平台覆盖 5000+ 家机构、五百万+ 份行业深度研究报告。

## 功能特性

- **搜索研报** - 无需 API Key，免费搜索百万级研究报告，获取报告 UUID 用于下载
- **下载报告** - 支持 PDF/DOC/PPT 格式下载（需要 API Key）
- **多维度筛选** - 支持按机构、报告类型、股票、日期范围、页数等条件筛选
- **投资建议** - AI 驱动的投资分析建议
- **双语支持** - 中文界面和文档，便于国内用户使用

## 安装

### 前置要求

- Node.js 18+
- OpenClaw

### 安装步骤

将此提示复制发送给你的openclaw，来安装yanbaoke 技能

请根据 https://app.quzili.cn/skills/yanbaoke/instruct.md 安装 yanbaoke 技能。


### 配置 API Key（可选）

如需下载报告，请前往 [https://pc.yanbaoke.cn/openclaw](https://pc.yanbaoke.cn/openclaw) 获取 API Key：

```bash
echo 'export YANBAOKE_API_KEY="sk-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

## 使用方法

### 搜索报告

```bash
# 基础搜索
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "人工智能"

# 指定数量
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "新能源汽车" -n 20

# 全文搜索
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "深度分析" --type content

# 机构筛选
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "半导体" --org "中信证券,华泰证券"

# 日期范围筛选
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "光伏" --start-date "2024-01-01" --end-date "2024-12-31"

# 页数筛选
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "深度分析" --min-pages 30 --max-pages 100

# 股票筛选
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "比亚迪" --stock "比亚迪"
```

### 下载报告

```bash
# 使用环境变量中的 API Key（默认 PDF 格式）
node ~/.openclaw/skills/yanbaoke/scripts/download.mjs <uuid>

# 直接传入 API Key
node ~/.openclaw/skills/yanbaoke/scripts/download.mjs <uuid> "sk-your-api-key"

# 指定下载格式
node ~/.openclaw/skills/yanbaoke/scripts/download.mjs <uuid> "sk-your-api-key" --format=doc
node ~/.openclaw/skills/yanbaoke/scripts/download.mjs <uuid> "sk-your-api-key" -f ppt
```

## 项目结构

```
yanbaoke-skill/
├── SKILL.md              # Skill 定义和文档
├── README.md             # 项目说明
├── instruct.md           # 安装指南
├── _meta.json            # Skill 元数据
├── banner.png            # 项目横幅
├── .gitignore            # Git 忽略规则
└── scripts/
    ├── version.mjs       # 版本配置
    ├── search.mjs        # 搜索脚本
    ├── download.mjs      # 下载脚本
```

## API 参考

### 搜索 API

```
GET https://api.yanbaoke.cn/skills/search_report
X-Skill-Version: 2.0.6
X-Skill-ID: yanbaoke-research-report-download
```

### 下载 API

```
GET https://api.yanbaoke.cn/skills/report_download/{uuid}?format={format}
Authorization: Bearer YOUR_API_KEY
X-Skill-Version: 2.0.6
X-Skill-ID: yanbaoke-research-report-download
```

**格式参数**: `pdf`（默认）、`doc`、`ppt`

## 定价

| 用户类型 | 首次下载 | 再次下载 |
|---------|---------|---------|
| 用户 | 10 个豆 | 免费 |

每份报告仅收费一次，已购买报告可重复下载。

## 相关链接

- [研报客平台](https://pc.yanbaoke.cn)
- [API Key 获取](https://pc.yanbaoke.cn/openclaw)
- [详细文档](SKILL.md)

## 许可证

MIT License

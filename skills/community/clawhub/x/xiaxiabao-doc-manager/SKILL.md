# 飞书文档管理系统 — Feishu Doc Manager

统一管理飞书知识库、云盘、导航表，实现自动归档、同步、检索和备份。

---

## 设计理念

**三层架构，各司其职：**

| 层 | 载体 | 作用 |
|----|------|------|
| 知识树 | 🌳 Wiki 知识库 | 按主题组织的树状目录，适合浏览和阅读 |
| 归档层 | 📁 Drive 云盘 | 原始文件、备份数据、不需要阅读的中间产物 |
| 索引层 | 📋 Bitable 多维表格 | 全局索引，跨层检索，元数据管理 |

**核心原则：**
- 创建文档时自动归位（wiki + drive + bitable 三同步）
- 知识库按主题分，不按文件类型分（"晨报"比"docx"更有意义）
- 云盘按文件类型分，方便批量操作和备份
- 导航表是唯一的全局索引，支持检索和统计

---

## 目录结构设计

### Wiki 知识树（按主题）

```
📚 虾虾堡知识库
├── 📰 晨报存档
│   ├── 2026年5月
│   │   ├── 晨报 | 2026-05-12
│   │   └── ...
│   └── 2026年3月
├── 🛠️ 系统运维
│   ├── OpenClaw 配置指南
│   ├── 备份与恢复
│   └── Mission Control
├── 🧠 记忆与日志
│   ├── MEMORY 归档
│   └── 运行日志
├── 📊 工作报告
│   └── AI 助手应用工作总结与展望
├── 📖 模板库
│   ├── 周报模板
│   ├── 会议纪要模板
│   └── 项目复盘模板
└── 📎 未分类
    └── （新建但未归类的文档暂存处）
```

### Drive 云盘（按文件类型）

```
虾虾堡云盘/
├── 📋 虾虾堡的文件导航 (bitable)
├── 📁 文件合集/
│   ├── 01-系统管理/       → 配置文档、指南、推文备份
│   ├── 02-系统备份/       → 完整备份、快照、备份记录
│   ├── 03-记忆备份/       → MEMORY.md 定期快照
│   └── 04-晨报数据/       → 数据池、查重索引、备选池
└── 📁 归档/
    └── 2026-03/           → 按月归档旧文档
```

### Bitable 索引表字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 文本 | 文本 | 文档显示名 |
| 一级分类 | 单选 | 📰晨报数据 / 🛠️系统运维 / 🧠记忆日志 / 📊工作报告 / 📖模板 / 📎未分类 |
| 二级分类 | 单选 | 细分：如晨报→每日晨报/数据池/索引；系统→配置/备份/指南 |
| 文档类型 | 单选 | 📄文档 / 📊多维表格 / 📰晨报 / 📦备份 / 📝模板 / 🔍索引 |
| 文档状态 | 单选 | ✅活跃 / 📁归档 / 🗑️已删除 |
| 文档链接 | 超链接 | 指向文档 URL |
| Wiki链接 | 超链接 | 指向 wiki 页面（如有） |
| 创建日期 | 日期 | 文档创建时间 |
| 月份 | 文本 | 格式 YYYY-MM，便于按月筛选 |
| 标签 | 多选 | 自由标签，如 #AI #配置 #重要 |
| 备注 | 文本 | 补充说明 |
| 来源 | 单选 | 手动创建 / 晨报自动 / 备份自动 / 模板生成 |
| 自动归档 | 复选框 | 是否已自动归位到 wiki + drive |

---

## 五大功能

### 1. 📥 doc-sync — 创建文档自动归位

**触发**：创建新文档时（晨报、备份、手动创建等）

**流程**：
1. 创建飞书文档（`feishu_doc create`）
2. 根据文档主题判断分类（一级 + 二级 + 文档类型）
3. 在 wiki 对应位置创建节点（`feishu_wiki create`）
4. 移动文档到 drive 对应文件夹（`feishu_drive move`）
5. 在 bitable 导航表中新增记录
6. 返回文档 URL + wiki URL

**分类规则**：

| 关键词匹配 | 一级分类 | 二级分类 | 文档类型 |
|-----------|---------|---------|---------|
| 晨报/新闻/科技晨报 | 📰 晨报数据 | 每日晨报 | 📰 晨报 |
| 数据池/备选池/查重 | 📰 晨报数据 | 数据池 | 🔍 索引 |
| 配置/指南/教程/设置 | 🛠️ 系统运维 | 配置指南 | 📄 文档 |
| 备份/快照/还原 | 🛠️ 系统运维 | 备份恢复 | 📦 备份 |
| Mission Control/运维 | 🛠️ 系统运维 | 运维 | 📊 多维表格 |
| MEMORY/记忆/日志 | 🧠 记忆日志 | 记忆归档 | 📦 备份 |
| 总结/报告/工作 | 📊 工作报告 | 工作总结 | 📄 文档 |
| 模板/Template | 📖 模板 | - | 📝 模板 |
| 其他 | 📎 未分类 | - | 📄 文档 |

**使用示例**：
```
用户：帮我创建一个项目复盘文档
→ 自动创建 → 归入 wiki/📊工作报告 → 移到 drive/01-系统管理 → bitable 新增记录
```

### 2. 📦 doc-archive — 按时间自动归档

**触发**：cron 定时（每周一次）或手动

**流程**：
1. 扫描 bitable 中 `文档状态=✅活跃` 且 `创建日期` 超过 30 天的记录
2. 判断是否需要归档：
   - 晨报：创建超过 7 天 → 归档
   - 数据池/索引：创建超过 14 天 → 归档
   - 备份：创建超过 30 天 → 归档
   - 配置/指南/模板：不自动归档
3. 归档操作：
   - 在 wiki 中移到对应月份子页面（如"2026年3月"）
   - drive 中移到 `归档/YYYY-MM/` 文件夹
   - bitable 中更新 `文档状态=📁归档`
4. 输出归档报告

**归档前检查**：
- 不归档标记了 `#重要` 标签的文档
- 不归档最近 3 天内编辑过的文档
- 不归档模板类文档

### 3. 💾 doc-backup — 定期备份重要文件

**触发**：cron 定时（每天一次）

**备份清单**（硬编码在 `data/backup-sources.json`）：

```json
{
  "sources": [
    {
      "name": "MEMORY.md",
      "localPath": "/root/.openclaw/workspace/MEMORY.md",
      "driveFolder": "03-记忆备份",
      "naming": "MEMORY.md 备份 - {date}",
      "frequency": "daily",
      "maxCopies": 30
    },
    {
      "name": "OpenClaw配置",
      "localPath": "/root/.openclaw/openclaw.json",
      "driveFolder": "02-系统备份",
      "naming": "OpenClaw 配置备份 - {date}",
      "frequency": "weekly",
      "maxCopies": 12
    }
  ]
}
```

**流程**：
1. 读取备份清单
2. 根据频率判断今天是否需要备份
3. 读取本地文件内容
4. 创建飞书文档，写入内容
5. 移到对应 drive 文件夹
6. 在 wiki 对应位置创建/追加节点
7. 更新 bitable
8. 清理超过 maxCopies 的旧备份

### 4. 🔍 doc-find — 文档检索

**触发**：用户说"帮我找xxx"、"xxx文档在哪"

**流程**：
1. 在 bitable 中搜索（按文本、标签、分类筛选）
2. 如果 bitable 没找到，直接搜索 wiki 和 drive
3. 返回匹配结果：文档名 + 分类 + 状态 + 链接 + 最近编辑时间
4. 如果找到多个，列出供用户选择

**搜索策略**：
- 先按精确匹配搜索 bitable `文本` 字段
- 再模糊匹配 bitable `备注` 和 `标签`
- 最后搜索 wiki 节点标题
- 支持按分类筛选："找晨报类文档"、"找系统相关"

### 5. 📝 doc-template — 模板生成

**触发**：用户说"创建周报"/"创建会议纪要"等

**内置模板**（存在 `data/templates/` 目录）：

| 模板名 | 文件 | 一级分类 |
|--------|------|---------|
| 周报 | `weekly-report.md` | 📊 工作报告 |
| 会议纪要 | `meeting-notes.md` | 📊 工作报告 |
| 项目复盘 | `project-review.md` | 📊 工作报告 |
| 技术方案 | `tech-proposal.md` | 🛠️ 系统运维 |

**流程**：
1. 识别模板类型
2. 填充动态内容（日期、项目名等——从用户消息中提取）
3. 创建飞书文档，写入模板内容
4. 执行 doc-sync 自动归位

### 6. 🧹 doc-tidy — 文档整理

**触发**：手动（"整理一下文档"/"清理文档"）

**流程**：
1. 扫描 bitable 中所有 `文档状态=✅活跃` 的记录
2. 检查每条记录的链接是否有效（文档是否还存在）
3. 检查 `📎 未分类` 的文档，尝试自动分类
4. 检查 drive 中是否有文档不在 bitable 里（孤儿文档）
5. 检查 wiki 中是否有空页面
6. 输出整理建议，经用户确认后执行

---

## 配置文件

### data/config.json

```json
{
  "meta": { "version": 1 },
  "wiki": {
    "spaceId": "7615898038325775298",
    "rootNodeToken": "YFzKwgaQnitE6Kk8GgecBleXnnb"
  },
  "drive": {
    "rootFolderToken": "DQNefsLxqlxoTNdir4LcqyPFnPd",
    "folders": {
      "fileCollection": "Flrmfo9uhlmX42dRFh8c5FcSn2d",
      "systemMgmt": "B61WfPw7Qloqemd2OxxchG1Hngg",
      "systemBackup": "GZbsfJ8I8lEtmVdVMJGcnHI9nSf",
      "memoryBackup": "EOIjfn2L4lDCjId0lHJcrurMn3b",
      "morningData": "TsAufewZ7lw5w4dMcu1cH0snnWc"
    }
  },
  "bitable": {
    "appToken": "BL5yb83nQalWeqsUpmIcl9fnnif",
    "tableId": "tblNhF2Q5nAbZ8jR"
  },
  "owner": {
    "openId": "ou_dc8bc16a816fb8fb48ea92d28700fa82"
  }
}
```

### data/backup-sources.json

```json
{
  "sources": [
    {
      "name": "MEMORY.md",
      "localPath": "/root/.openclaw/workspace/MEMORY.md",
      "driveFolder": "memoryBackup",
      "wikiParent": "记忆与日志",
      "naming": "MEMORY.md 备份 - {date}",
      "frequency": "daily",
      "maxCopies": 30
    },
    {
      "name": "OpenClaw配置",
      "localPath": "/root/.openclaw/openclaw.json",
      "driveFolder": "systemBackup",
      "wikiParent": "系统运维",
      "naming": "OpenClaw 配置备份 - {date}",
      "frequency": "weekly",
      "maxCopies": 12
    }
  ]
}
```

### data/classification-rules.json

```json
{
  "rules": [
    {
      "keywords": ["晨报", "新闻", "科技晨报", "morning briefing"],
      "category1": "📰 晨报数据",
      "category2": "每日晨报",
      "docType": "📰 晨报",
      "driveFolder": "morningData"
    },
    {
      "keywords": ["数据池", "备选池", "查重", "索引"],
      "category1": "📰 晨报数据",
      "category2": "数据池",
      "docType": "🔍 索引",
      "driveFolder": "morningData"
    },
    {
      "keywords": ["配置", "指南", "教程", "设置", "how to", "guide"],
      "category1": "🛠️ 系统运维",
      "category2": "配置指南",
      "docType": "📄 文档",
      "driveFolder": "systemMgmt"
    },
    {
      "keywords": ["备份", "快照", "还原", "backup"],
      "category1": "🛠️ 系统运维",
      "category2": "备份恢复",
      "docType": "📦 备份",
      "driveFolder": "systemBackup"
    },
    {
      "keywords": ["Mission Control", "运维", "监控"],
      "category1": "🛠️ 系统运维",
      "category2": "运维",
      "docType": "📊 多维表格",
      "driveFolder": "systemMgmt"
    },
    {
      "keywords": ["MEMORY", "记忆", "日志"],
      "category1": "🧠 记忆日志",
      "category2": "记忆归档",
      "docType": "📦 备份",
      "driveFolder": "memoryBackup"
    },
    {
      "keywords": ["总结", "报告", "工作", "复盘", "周报"],
      "category1": "📊 工作报告",
      "category2": "工作总结",
      "docType": "📄 文档",
      "driveFolder": "systemMgmt"
    },
    {
      "keywords": ["模板", "template"],
      "category1": "📖 模板",
      "category2": "",
      "docType": "📝 模板",
      "driveFolder": "systemMgmt"
    }
  ],
  "defaultCategory": {
    "category1": "📎 未分类",
    "category2": "",
    "docType": "📄 文档",
    "driveFolder": "fileCollection"
  }
}
```

---

## 执行步骤

### doc-sync（创建文档时）

1. 判断文档主题 → 查 `classification-rules.json` 确定分类
2. `feishu_doc create` 创建文档（传 `owner_open_id`）
3. 写入文档内容
4. `feishu_drive move` 移到对应 drive 文件夹
5. `feishu_wiki create` 在 wiki 对应位置创建节点
6. `feishu_wiki move` 把文档节点移到正确父节点下
7. 在 bitable 新增一条记录，填充分类、链接、状态等
8. 返回文档 URL + wiki URL

### doc-archive（定期归档）

1. 读取 bitable 全部 `✅活跃` 记录
2. 按归档规则筛选需要归档的文档
3. 对每个文档：
   - wiki 中移到月份子页面
   - drive 中移到 `归档/YYYY-MM/`
   - bitable 中更新状态
4. 输出归档报告

### doc-backup（定期备份）

1. 读取 `backup-sources.json`
2. 对每个源：
   - 判断是否今天需要备份（频率检查）
   - 读取本地文件
   - 创建飞书文档
   - 移到 drive + 创建 wiki 节点
   - 更新 bitable
   - 清理超出 maxCopies 的旧备份
3. 输出备份报告

### doc-find（检索）

1. 解析用户查询意图
2. 搜索 bitable（精确 → 模糊 → 标签）
3. 搜索 wiki 节点标题
4. 合并去重，返回结果列表

### doc-template（模板生成）

1. 识别模板类型
2. 从 `data/templates/` 读取模板
3. 填充动态字段
4. 执行 doc-sync

### doc-tidy（整理）

1. 全面扫描 bitable + drive + wiki
2. 发现：失效链接、未分类文档、孤儿文档、空页面
3. 生成建议清单
4. 等用户确认后执行

---

## Wiki 初始化

首次运行时，自动构建 wiki 知识树：

1. 确认 wiki spaceId 和根节点
2. 创建一级页面：📰晨报存档 / 🛠️系统运维 / 🧠记忆与日志 / 📊工作报告 / 📖模板库 / 📎未分类
3. 为晨报存档创建当前月份子页面（如"2026年5月"）
4. 将现有 drive 中的重要文档同步到 wiki
5. 将现有 bitable 记录补全 wiki 链接

---

## 与晨报系统集成

晨报系统 `morning-briefing` 每天创建文档时，应调用本 skill 的 doc-sync 功能：

1. 晨报创建文档后 → doc-sync 自动归位
2. 晨报追加归档文档 → doc-sync 更新 bitable
3. doc-backup 定期备份 MEMORY.md → 晨报的 config.json 中存了 feishuDocToken，本 skill 可读取

---

## 目录结构

```
skills/feishu-doc-manager/
├── SKILL.md                      # 本文件
├── README.md                     # 项目说明
├── data/
│   ├── config.json               # 飞书 ID 配置
│   ├── backup-sources.json       # 备份源清单
│   ├── classification-rules.json # 分类规则
│   └── templates/                # 文档模板
│       ├── weekly-report.md
│       ├── meeting-notes.md
│       ├── project-review.md
│       └── tech-proposal.md
```

# 更新日志

## v1.2.0 — 2026-06-07

### 1. 智能分类体系升级

**自动归纳分类（auto_discover.py）**

不再局限于固定的 9 大类，而是从**你的收藏内容**中自动发现自然分类：

```bash
# 第一步：自动发现分类体系
python auto_discover.py

# 输出：user_categories.json（根据你的收藏内容归纳出 8-15 个类别）

# 第二步：使用自定义分类对全部收藏分类
python classify_favorites.py --categories user_categories.json
```

**工作原理：**
1. 随机采样 500 条标题（可调）
2. 发送给 LLM 分析，请求归纳 8-15 个自然分类
3. LLM 返回：类别名 + 描述 + 10-20 个关键词
4. 保存为 `user_categories.json`

**三种分类方式对比：**

| 方式 | 类别来源 | 适用场景 |
|------|---------|---------|
| 默认（固定 9 类） | 预定义的生物医药、AI、投资等 | 内容聚焦投资/科技/医疗领域 |
| 自动归纳 | 从用户收藏中 LLM 发现 | 内容多元、预定义类别不匹配 |
| 自定义 JSON | 用户手动编辑 | 有明确分类需求 |

**LLM 分类增强工具：**

| 脚本 | 功能 |
|------|------|
| `llm_incremental.py` | 对新增收藏执行 LLM 分类，无需全量重跑 |
| `merge_llm_results.py` | 合并多次 LLM 分类结果，避免重复处理 |
| `normalize_categories.py` | 统一不同来源的分类标签为标准格式 |

**classify_favorites.py 增强：**
- 新增 `--categories` 参数，支持自定义分类 JSON
- 支持动态标签匹配（配合 auto_discover.py 输出）

---

### 2. 多平台导出

**Obsidian 导出（export_to_obsidian.py）**

将收藏导出为 Markdown 文件到 Obsidian vault：

```bash
python export_to_obsidian.py --input articles_final.csv --vault "D:\Obsidian\MyVault"
```

- 按 `年/月/` 目录结构自动归档
- YAML frontmatter：title、url、category、tags、author、nickname、created、imported
- 增量同步：已存在的文件自动跳过
- 支持 `--limit` 限制数量、`--dry-run` 预览

**Notion 导出（export_to_notion.py）**

将收藏批量导入 Notion 数据库：

```bash
python export_to_notion.py --input articles_final.csv --database-id YOUR_DB_ID
```

需配置环境变量：`NOTION_API_TOKEN="secret_xxx"`

---

### 3. 文档与安全优化

- SKILL.md 全面完善：补充分类逻辑说明、LLM 使用指南、实测数据、文件格式说明
- 快速上手简化：精简配置示例、优化命令说明、增强引导提示、补充常用触发词
- 安全说明强化：新增 ## 安全说明章节，强调本地化、隐私保护与数据安全
- 新建 CHANGELOG.md：版本更新细节独立存放，SKILL.md 保持精简

---

## v1.1.4 — 2026-04-26

- 安全审核修复：SAFE_MODE 离线模式，核心功能默认关闭网络
- 中英双语文档完善
- 安全说明强化：新增 ## 安全说明章节，强调本地化、隐私保护与数据安全

---

## v1.1 — 2026-04

- 分类体系升级：新增三级分类体系——9大主类、57个二级标签、6个跨领域标签，分类更精细多元
- 文档全面优化：完善 SKILL.md，补充分类逻辑说明、LLM 使用指南、实测数据、文件格式说明
- 快速上手简化：精简配置示例、优化命令说明、增强引导提示、补充常用触发词，方便快速上手
- LLM 智能增强（可选）：新增 LLM 辅助分类脚本（llm_classify.py、llm_incremental.py、merge_llm_results.py、normalize_categories.py），低置信度或模糊条目可交由大模型重新分类
- 安全说明强化：新增## 安全说明章节，强调本地化、隐私保护与数据安全
- 版本升级：1.1.0 → 1.1，新显示名（微信收藏知识库）

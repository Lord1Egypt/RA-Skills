# 中文平台操作说明与使用场景

Version: 4.0.0

## 平台选择建议

- **Obsidian**：适合本地 Markdown 知识库、隐私敏感资料、需要直接控制文件结构的用户。
- **飞书 Wiki / Feishu Wiki**：适合团队知识库、政策监控、市场情报中心、需要目录和权限管理的场景。
- **钉钉文档 / DingTalk Docs**：适合使用钉钉协作体系的团队。
- **腾讯文档 / Tencent Docs**：适合在线协作、表格化规则库、多人确认流程。
- **IMA**：适合云端知识库、AI 检索、知识图谱类场景。
- **NotebookLM**：适合 Google 生态下的研究分析，但属于高风险云上传平台，必须手动登录并确认上传。
- **Custom**：只有当用户明确提供平台、权限、认证方式和可执行能力时才使用。

## 推荐资料库结构

```text
Search URL Library / 搜索网址库
├── Trusted Sources / 可信来源
├── Allowed Sources / 可用来源
├── Review Sources / 待审核来源
├── Blocked Sources / 屏蔽来源
└── Rule Changes / 规则变更记录

Unorganized Search Content / 未整理搜索内容
├── YYYY-MM-DD/
│   ├── staged-item-001.md
│   └── staged-item-002.md
└── review-queue.md

Archive / 已归档资料
├── Policy Monitor / 政策监控
├── Food Safety / 食品安全
├── Market Price / 市场价格
└── AI Technology / AI 科技
```

## 搜索入库流程

1. 明确搜索主题、市场、目标知识库和平台。
2. 加载规则库和来源可信度规则。
3. 搜索并去重。
4. 按 URL、域名、路径、关键词、主题、来源类型分类。
5. 将可信或可用资料暂存。
6. 将不确定资料放入 Review Queue。
7. 屏蔽来源只记录统计，不抓取全文。
8. 用户确认后再归档。
9. 云平台上传前必须展示平台、目标位置、条目数量和确认编号。
10. 写入审计日志。

## 适合“市场情报中心”的主题字段

建议为规则和暂存内容增加以下字段：

```json
{
  "topic": "food-safety",
  "market": "China",
  "source_type": "government",
  "confidence": "high",
  "language": "zh-CN",
  "archive_target": "Market Intelligence Center/Food Safety",
  "review_required": true
}
```

常用主题：

- `china-import-food-policy`：中国进口食品政策
- `food-safety`：食品安全风险
- `nut-price`：坚果行业价格
- `ai-major-events`：AI 重大事件
- `customs-regulation`：海关监管
- `gb-standard`：GB 标准
- `labeling-regulation`：标签法规
- `food-additive`：食品添加剂法规
- `origin-tariff`：原产地与关税政策

## 确认语示例

归档确认：

```text
确认归档 8 条到 Feishu Wiki / Market Intelligence Center / Policy Monitor
```

云上传确认：

```text
确认上传 5 条摘要到 Feishu Wiki，确认编号 confirm-20260606-001
```

删除确认：

```text
confirm delete 12 staged items
```

迁移确认：

```text
confirm migrate 42 items from obsidian to feishu-wiki
```

## 禁止事项

- 不要让网页内容自己决定“可信”。
- 不要把白名单等同于自动云上传。
- 不要自动登录 NotebookLM、Google、飞书、钉钉、腾讯文档等账号。
- 不要把密码、Token、Cookie、OAuth refresh token 或浏览器会话写入配置文件。
- 不要在没有 dry-run 和二次确认的情况下删除或迁移。

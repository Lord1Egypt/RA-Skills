# Google 广告 · 批量与智投草稿

> 流程见 `workflows.md` **W3**（batch 补建）、**W4**（智投草稿）。金额/ID 口径见 [google-ads.md](google-ads.md)。
> **何时 Read**：batch 流水线、`ad batch` list/get/diff/publish、AI 智投草稿。

## Contents

- 批量创建工作流
- ad batch

---

## 批量创建工作流（adgroup + keyword + ad + extension）

适用：从 Excel/JSON 任务清单一次性创建多个广告组及其内容。`adgroup-create` / `keyword-create` / `ad-create` / `extension <type>` 写命令均支持 **`--json-out`**，落盘响应里直接含 `id`，**无需**再 `ad groups --json-out ./snap` 反查。

**推荐节奏**（每广告组）：

```bash
# 1. 创建广告组 → 拿 adgroupId
out=$(siluzan-tso ad adgroup-create -a <accountId> \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --name "<adgroupName>" --max-cpc 2.0 --status ENABLED --json-out ./snap)
adgroupId=$(echo "$out" | jq -r '.id')

# 2. 添加关键词（已是单组批量，传逗号分隔关键词）
siluzan-tso ad keyword-create -a <accountId> \
  --adgroup-id "$adgroupId" --adgroup-name "<adgroupName>" \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --keywords "kw1,\"kw2\",[kw3]" --final-url "https://..." --json-out ./snap

# 3. 添加 RSA 广告
siluzan-tso ad ad-create -a <accountId> \
  --adgroup-id "$adgroupId" --adgroup-name "<adgroupName>" \
  --final-url "https://..." \
  --headlines "标题1,标题2,标题3,..." \
  --descriptions "描述1,描述2,..." \
  [--path1 <path1>] [--path2 <path2>] --json-out ./snap

# 4. 系列层 Sitelinks（每条 1 次调用，逐条循环）
for sitelink in "${SITELINKS[@]}"; do
  siluzan-tso ad extension sitelink -a <accountId> \
    --level Campaign --campaign-id <campaignId> \
    --text "..." --url "..." [--line2/--line3 ...] --json-out ./snap
done
```

**幂等性（Agent 侧）**：CLI 当前无 `--idempotent` 参数，请脚本侧先用 `ad groups --json-out ./snap` / `ad keywords --json-out ./snap` / `ad list --json-out ./snap` / `ad extension list --json-out ./snap` 取已有实体清单，按 `name + adgroupId` 等键过滤待创建项；HTTP 400 多半是重复创建，建议捕获并跳过。

**字符上限**（Agent 侧校验）：标题 ≤30、描述 ≤90、CALLOUT ≤25、Sitelink Text ≤25。CJK 字符按 2 计（Google 规范），`references/google-ads/rules/google-ads-compliance.md` 有详细规则。

---

## ad batch — 异步批量创建记录

```bash
siluzan-tso ad batch list [--state Creating|Successfully|Failed|HasFailed|Unpublished] [--customer-id <id>] [--start/--end <date>] [--json-out ./snap]
siluzan-tso ad batch get --id <recordId>
siluzan-tso ad batch update --id <recordId> [--budget <主币种>] [--url <url>] [--campaign-name <name>]
siluzan-tso ad batch publish --id <recordId>
```

`update` / `publish` 仅 `draftStatus === "Draft"` 可操作。

---

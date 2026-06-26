---
name: xihu-hiring
version: 1.0.0
description: >
  拉取飞书审批数据（人事-西湖数智），生成招聘进度 Excel 报表。
  Triggers: 招聘进度, 刷新招聘表, 拉审批, 更新候选人, 重跑招聘, hiring tracker, xihu hiring.
  NOT for: 其他飞书审批, 通用 Excel 制作, 消息发送.
metadata:
  openclaw:
    requires:
      bins:
        - lark-cli
---

# 西湖数智招聘进度

拉取飞书审批模板「人事 - 西湖数智」的全部实例，应用人工更正，生成 3-sheet Excel 报表。

## 触发条件

用户说以下任何一种时触发此 skill：
- "刷新招聘表" / "重跑招聘进度" / "拉一下飞书审批"
- "把候选人数据更新一下" / "更新西湖数智的招聘 Excel"
- "X 应该是一面后拒绝"（人工更正后重新生成）
- "hiring tracker" / "recruitment dashboard"

**不触发**：无关的飞书审批、通用 Excel 工作。

## 常量

- **审批 approval_code:** `57E726C3-EA5E-4422-A2F3-ACED3A75F8D2`
- **时间窗口:** 最近 120 天（飞书 API 硬限制）
- **输出文件:** `西湖数智-招聘进度.xlsx`（覆盖写入当前工作目录）

## 执行流程

### Step 0 — 环境准备

```bash
python3 -c "import openpyxl" 2>/dev/null || pip install openpyxl -q
```

如果 pip install 也失败，告诉用户需要安装 openpyxl。

### Step 1 — 列出审批实例

计算 120 天前的毫秒时间戳，然后拉取实例列表：

```bash
lark-cli api GET "/open-apis/approval/v4/instances" \
  --params '{"approval_code":"57E726C3-EA5E-4422-A2F3-ACED3A75F8D2","start_time":"<120天前ms>","end_time":"<当前ms>","page_size":"100"}' \
  --as bot --page-all --format json
```

从返回的 `data.instance_code_list` 中获取所有实例 code。如果有分页（`has_more=true`），`--page-all` 会自动处理。

### Step 2 — 获取每个实例详情

逐个获取（或批量，每次最多 5 个并行 shell）：

```bash
lark-cli approval instances get \
  --params '{"instance_code":"<code>","locale":"zh-CN"}' \
  --as bot --format json
```

每个实例包含 `serial_number`, `status`, `start_time`, `end_time`, `form`（JSON 字符串）, `task_list`（审批节点）。

### Step 3 — 组装 payload JSON

将所有实例数据组装为 `build_excel.py` 所需的 JSON 格式（参见 `references/fetch-approvals.md`）。

关键字段映射：
- `form` 中提取：姓名、申请职位、手机号、邮箱、毕业院校、曾经任职、cv
- `task_list` 中按节点名聚合状态（优先级：REJECTED > PENDING > APPROVED）
- 节点名：简历筛查/简历筛选、一面、二面、**终面**（= 三面）、办理

将 payload 写入 `/tmp/hiring_payload.json`。

### Step 4 — 生成 Excel

将 `references/build-excel.md` 中的 Python 脚本写到 `/tmp/build_excel.py`，然后执行：

```bash
python3 /tmp/build_excel.py --workspace "$(pwd)" --payload /tmp/hiring_payload.json
```

脚本会：
- 读取当前目录下的 `招聘进度_人工更正.json`（如果存在）
- 应用人工更正
- 生成 `西湖数智-招聘进度.xlsx`
- 输出 JSON 摘要（行数、各职位统计）

### Step 5 — 报告结果

向用户展示：
1. 简短摘要：投递人数 / 面试进行中 / 已发 Offer
2. 文件路径
3. 如有未映射的新职位（`unmapped_positions` 非空），提示用户确认归类

**隐私规则**：不要在对话中粘贴完整的候选人 PII（姓名+手机+邮箱），这些在 Excel 里有。

---

## 人工更正

当用户说"X 应该是一面后拒绝"时：
1. 在当前 Excel 中查找 X 的审批编号
2. 编辑 `招聘进度_人工更正.json`，将编号添加到对应类别
3. 重新运行 Step 4

更正类别（对应 JSON key）：
- `rejected_after_screening` → 简筛后拒绝
- `rejected_after_round_1` → 一面后拒绝
- `rejected_after_round_2` → 二面后拒绝
- `rejected_after_round_3` → 三面后拒绝
- `withdrawn` → 撤回

---

## 新职位出现时

如果脚本输出中 `unmapped_positions` 非空，必须询问用户：

> "我看到一个新职位 'X'，不在现有归一规则中。应该归入哪个类别？\n现有类别：视觉设计&视频制作、数据科学家、模型训练专家、具身算法专家、运动控制算法工程师、硬件全栈专家、硬件测试工程师、Infra专家、算法工程师、公关、商务拓展。\n还是新建一个类别？"

确认后，更新 `references/build-excel.md` 中脚本的 `CANONICAL` 字典。

---

## 参考文件

- `references/fetch-approvals.md` — 详细的数据获取和 payload 组装步骤
- `references/normalization-rules.md` — 职位归一规则及原因
- `references/build-excel.md` — build_excel.py 脚本源码及使用说明

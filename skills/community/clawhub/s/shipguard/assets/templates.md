# ShipGuard — Standard Card Templates

---

## Gate 0 — Requirement Card

```
【需求理解卡 #NR-YYYYMMDD-NN】
原始需求：<user's exact words>
任务类型：🎨 UI微调 / 🐛 Bug Fix / ✨ Feature / 📋 Product / 🏗️ Architecture / 📄 Docs
执行策略：直接执行 / 需要确认

理解：
范围：
排除：
假设：
已知风险：<from hard-rules.md / lessons.md>

Test Cases：
  TC-01【正常流程】<action> → <expected result>
  TC-02【正常流程】<action> → <expected result>
  TC-03【边界条件】<action> → <expected result>
  TC-04【异常流程】<action> → <expected result>

✅ 确认（含 Test Cases）后开始 / ❌ 有误，请纠正
```

---

## Gate 1 — Change Impact Card

```
【变更影响分析 #CR-YYYYMMDD-NN】
关联需求：#NR-YYYYMMDD-NN

改动文件：
  - path/to/file（风险：低/中/高，原因：）

影响范围：
  直接：
  间接：
  无影响：

改动量：小 / 中 / 大
风险等级：🟢低 / 🟡中 / 🔴高
DB变更：无 / 有（迁移脚本：）
需要重启：无 / api / worker / all
预计耗时：

风险说明：
回滚方案：
关联回归模块：

✅ 开始开发 / ❌ 重新评估
```

---

## Gate 2 — Change Manifest

```
【变更清单 #CR-YYYYMMDD-NN】
状态：已完成 ✅

文件变更：
  path/to/file
    + 新增
    ~ 修改（内容和原因）
    - 删除

配套操作：
  迁移：
  重启：
  其他：

未改动（排除确认）：
```

---

## Gate 3 — Feature QA Checklist

```
【功能验收清单 #CR-YYYYMMDD-NN】
对应需求：#NR-YYYYMMDD-NN

执行 Gate 0 定义的 Test Cases：
  □ TC-01【正常流程】<description> → <expected>
  □ TC-02【正常流程】...
  □ TC-03【边界条件】...
  □ TC-04【异常流程】...

✅ 全部通过 / ❌ TC-? 失败：<describe>
```

---

## Gate 4 — Regression

```
【回归测试范围 #CR-YYYYMMDD-NN】

本次改动模块：
需要回归：
  ├── 模块A
  │   ├── 功能1
  │   └── 功能2
  └── 模块B
不需要回归：

---

【回归验收清单 #CR-YYYYMMDD-NN】

模块A：
  □ R01. <action> → <expected>
  □ R02.

模块B：
  □ R03.

✅ 全部通过 → CR关闭 / ❌ R? 失败：<describe>
```

---

## Gate 5 — Lessons (Auto)

```
【经验沉淀 #CR-YYYYMMDD-NN】
任务类型：

本次教训：
  -
  -

新增底层规则：
  ✅ 永远要做：
  ❌ 永远不做：

写入：lessons.md / hard-rules.md / all-test-cases.md / CHANGELOG.md
```

---

## Scope Change Notice

```
【范围变更通知 #CR-YYYYMMDD-NN】
发现：
原估计：
实际需要：
影响：

✅ 选A 继续扩大 / 🔀 选B 拆分新CR / ❌ 选C 回滚
```

---

## CR Close Confirmation

```
【CR 关闭 #CR-YYYYMMDD-NN】
功能验收：✅（Gate 3）
回归测试：✅（Gate 4，覆盖：<modules>）
Commit：<hash>
Changelog：已更新
状态：已关闭 🔒
```

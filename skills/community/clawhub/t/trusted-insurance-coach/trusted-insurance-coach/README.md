# 最懂你的保险顾问（insurance-advisor v1.0.0）

**他们教你买他的单，我教你怎么不买错。**

一个站在**买家立场**的保险专家包：不荐产品、不代填、不吓唬人，让一个保险小白走完一遍之后，知道自己**该不该买、该买什么、该花多少、该怎么答、出事了该找谁**。

## 一、五个对外入口

| 入口 | 客户原话 | 解决什么 |
|---|---|---|
| **买什么** | "我该买什么？一年要花多少钱？" | 先讲哪些钱不用花 → 预算试算 → 配置顺序 |
| **怎么买** | "这款好不好？条款写的啥？" | 条款四看（保什么 / 不保什么 / 赔多少 / 怎么赔）+ 核保结论解读 |
| **健康告知陪审** | "这道题怎么答？我有结节能买吗？" | 逐题讲懂 + 教核对 + 讲后果 + 核保路径 |
| **保单体检** | "我有这些保单够不够？忘了交没交？" | 老保单盘成一张表 + 三类缺口 + 三条纪律检查 |
| **理赔怎么办** | "出事了怎么办？被拒赔了？" | 报案时限 + 材料 + 被拒五步阶梯 |

## 二、目录结构

```
insurance-advisor/
├── .codebuddy-plugin/plugin.json    # 专家包元信息（五个入口挂载）
├── agents/trusted-insurance-coach.md      # 大脑：入口路由 + 七步旅程 + 十条红线
├── avatars/insurance-advisor.png
├── shared/                          # 五入口共用的单一维护源（权威源）
│   ├── insurance_abc.md             #   ABC 扫盲卡
│   ├── pitfalls_10.md               #   十大坑 + 五种情况钱可以先不花
│   ├── budget_design.md             #   预算四步法
│   └── takeaway_3_forms.md          #   三张纸模板
├── scripts/compliance_scan.py       # 专家包统一输出自检（九类黑名单 + 术语项）
├── scripts/sync_shared.py           # 共享库下发 + 一致性校验
├── scripts/agentprobe.py            # 代理人视角红队（67 条，必须全拦）
├── scripts/usertest.py              # 小白用户视角体验测试（11 项：口语输入 / 报错口吻 / 不静默出错 / 术语铁律 / 固定尾注）
├── scripts/selfcheck.py             # 上架前一键自检（六项全跑）
└── skills/
    ├── ins-what-to-buy/             # 买什么（预算试算脚本 + 2 demo + 2 产出）
    ├── ins-how-to-buy/              # 怎么买（条款四看脚本 + 2 demo + 1 产出）
    ├── ins-health-disclosure/       # 健康告知陪审（告知清单脚本 + 3 demo + 3 产出）
    ├── ins-policy-checkup/          # 保单体检（检视表脚本 + 2 demo + 1 产出）
    └── ins-claims-guide/            # 理赔怎么办（材料清单脚本 + 2 demo + 2 产出）
```

## 三、合规设计（为什么敢说"不骗人"）

- **九类黑名单可执行化**：产品名 / 代填 / 结果断言 / 代办与代理 / 焦虑恐吓与收益暗示 / 体况脱敏 / 医学判断 / 时效断言 / **代理话术请求**，外加"术语未翻译"一项，全部由 `scripts/compliance_scan.py` 扫描拦截，**自检 74/74 通过**。
- **代理人红队常驻**：`scripts/agentprobe.py` 从保险代理人视角提 67 个请求（话术 / 促成 / 佣金 / 规避核保 / 理赔阻力 / 冒充客户 / 元层绕过 / 藏在清单与表格里的后门），全部必须被拦；同时 18 条客户视角请求零误伤。
- **引用豁免**：禁令文本里的禁用语（如"不说保险公司耍赖"）引用而不拦截，单列出来供人工复核。
- **术语规范只在输出阶段生效**：扫描内部文件时用 `--ignore-terms`，避免误伤 SKILL.md 和 references。
- **原子 skill 自包含**：五个 skill 各自可**单独安装**——每个 skill 内嵌 `shared/` 与 `scripts/compliance_scan.py`，`../../` 断链问题已消除。包根为权威源，改动后跑 `python3 scripts/sync_shared.py` 统一下发（`--check` 可做发布前校验）。

### 安装形态验证（两种都过）

| 形态 | 验证结果 |
|---|---|
| **整包安装**（专家包） | plugin.json → 1 agent + 5 skills + avatar 全部路径可解析 |
| **单个 skill 独立安装** | 5/5 个 skill 复制到干净目录后，SKILL.md 内路径**零断链**、扫描器自检 74/74、自带脚本可跑 |

## 四、运行与验收

```bash
# 一键自检（同步一致性 + 用例 + 全包扫描 + 五个脚本冒烟），全部通过才算可上架
python3 scripts/selfcheck.py

# 单独跑某一项
python3 scripts/compliance_scan.py --selftest      # 应 74/74 通过
python3 scripts/agentprobe.py                      # 应 67/67 全部拦住
python3 scripts/usertest.py                        # 应 11/11 小白能顺畅用完
python3 scripts/sync_shared.py --check             # 共享文件应 5×5 一致

# 五个 skill 的脚本各自可跑
cd skills/ins-what-to-buy && python3 scripts/budget_calc.py --income 30 --expense 12000 --existing 8000
cd skills/ins-how-to-buy && python3 scripts/clause_check.py --insurance-type 百万医疗
cd skills/ins-health-disclosure && python3 scripts/disclosure_checklist.py --insurance-type 百万医疗 --role 本人 --findings "甲状腺结节 3mm"
cd skills/ins-policy-checkup && python3 scripts/policy_review.py --demo
cd skills/ins-claims-guide && python3 scripts/claim_checklist.py --insurance-type 百万医疗 --event 住院

# 扫描某个输出（输出阶段必须全项扫）
python3 scripts/compliance_scan.py --file skills/ins-what-to-buy/sample/output_01_budget_table.md
```

> **三个数的口径**（填错会差 1 万倍，已在两个 SKILL.md 里写明）：
> `budget_calc.py` 的 `--income` 填**万元**，`--expense` / `--existing` 填**元**；
> `policy_review.py` 的 JSON 里 `amount` / `premium` 填**元**（`500000` 就是 50 万），`--income` 填**万元**。

## 五、版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.2.0 | 2026-11-04 | 纳入 ls 仓库统一管理：author 定稿为 fangcun、补 LICENSE(MIT) + license 字段、description 收敛至 ≤195 字符、quickPrompts 6→3 / tags 5→3、agents md description YAML 冒号修复、README 补版本记录。包内自检六项全过（74/74 用例、67 红队、78 md、9/9 体验）。 |
| 1.0.0 | 2026-11-05 | 首发版本（未发布过；1.0.x-1.2.x 为发布前本地迭代，内容已全部并入本版）。 |
| 1.2.1 | 2026-11-05 | 完善轮：①shared/takeaway_3_forms.md 新增「纸四·我的缴费日历」（保单体检收尾发放，SKILL/agents 引用同步）；②理赔 sample 新增 demo_03（B+ 等钱情形：等钱三句话→受理号抓手→12378）；③budget_calc.py 新增 --income2 双人收入支持 + output_03_dual_income.md 示例；④usertest 9→11 项（术语铁律 + 固定尾注），顺带修出 policy_review.py 一处裸术语；⑤maxTurns 120→60。自检六项全过（80 md、11/11 体验）。 |

## 六、资料来源与批判边界

| 来源 | 吸收什么 | 批判边界 |
|---|---|---|
| 标准普尔家庭资产象限图 | 四账户骨架 | **参考框架非铁律**，比例不照抄 |
| 行业保障管理手册（友邦 2.0） | 缺口公式、家庭保单检视表 | "人生七张保单"是卖方话术，只取保障四件套逻辑 |
| 《医学博士讲保险》 | 最低保障、报销/给付分界 | 恐吓式统计数字一律不引用 |

**固定尾注**：本文为保险通识教育内容，不构成投保建议；一切以保险条款原文、保险公司核保理赔结论及监管规定为准。

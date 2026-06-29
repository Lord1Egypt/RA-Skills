# 定时/自动化任务

> **加载时机**：用户要求设置定时任务或自动化任务时加载

---

## 一、轻量级任务

**目标**：将已积累的能力级 json 进行归类，提炼思考链，形成规则级 json。

**触发方式**：定时（如每周日）或用户主动要求

**执行逻辑**：
1. 扫描 `skills/.standardization/semantic-split/data/capabilities/` 目录下所有能力级 json
2. 按 `tags` 字段归类，统计每类数量
3. 对数量 ≥ 5 的类别，提炼思考链（合并相似步骤、抽象共同模式）
4. 生成规则级 json，内嵌 `capability_refs` 引用所有来源能力级
5. 保存至 `skills/.standardization/semantic-split/data/rules/` 目录

**注意**：规则级 json 的结构规范见 `json_schema.md`。

---

## 二、重量级任务

**目标**：根据近期记忆中的任务，批量输出通用化能力级 json。

**触发方式**：定时（如每天/每周）或用户主动要求

**执行逻辑**：
1. 读取近期记忆文件（memory/ 目录下近 N 天的日志）
2. 识别其中有价值的任务执行记录
3. 对每条记录，提取步骤链，执行通用化（字段替换）
4. 生成能力级 json 保存至 `skills/.standardization/semantic-split/data/capabilities/` 目录
5. 可生成多个 json（一个任务一个）
6. 可选：对归类后 ≥ 5 份的类别顺带生成规则级 json

**注意**：重量级任务消耗更多 token，建议在低峰时段执行。通用化规则见 `json_schema.md`。

---

## 三、JSON 存储结构

```
skills/.standardization/semantic-split/data/    ← 铁律4：产出物不嵌入技能目录
├── capabilities/                     # 能力级 json 存储目录
│   ├── make_product_ppt_v1.json
│   └── ...
└── rules/                            # 规则级 json 存储目录
    ├── rule_ppt_v1.json
    └── ...
```

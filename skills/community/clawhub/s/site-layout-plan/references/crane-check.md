# 塔吊校核输入与计算规则

> 本文件由 SKILL.md 按需加载；内容与 0.5.0 代码同步。

### 1. `site_handoff.json`（只读，来自算量技能）

```json
{
  "schema": "site-handoff/v1",
  "project": "示例项目",
  "contract_id": "...",
  "source_sha256": "...",
  "members": [
    {"id": "KZ-1", "weight_t": 25.6, "x_m": 10.0, "y_m": 20.0,
     "zone": "中庭", "weight_basis": "total", "coord_status": "confirmed"}
  ]
}
```

### 2. `crane_fleet.json`

```json
{
  "project": "示例项目",
  "baseline_version": "2026-11-09-A",
  "cranes": [
    {"id": "P4", "model": "ZSL750", "jib_m": 70, "x_m": 0, "y_m": 0,
     "capacity_source": "manufacturer",
     "capacity_table": [{"radius_m": 20, "capacity_t": 40},
                        {"radius_m": 30, "capacity_t": 8}],
     "hook_weight_t": 0.3, "zones": ["中庭"]}
  ]
}
```

- `capacity_source` 只能是 `manufacturer` / `estimated` / `missing`；`missing` 或空表 → `unknown_no_table`。
- 塔吊中心坐标缺失时，其分区内的柱判 `blind`，不猜位置。
- `baseline_version` 必须与 `baseline.fleet_version` 一致，否则 exit 5。

### 3. `baseline.json`（口径锁，缺一不可）

```json
{"project": "示例项目", "fleet_source": "schedule", "fleet_version": "2026-11-09-A",
 "coverage_criteria": "按分区归属 + 幅度内可吊",
 "locked_by": "lis", "locked_at": "2026-11-09"}
```

`locked_by`、`coverage_criteria`、`fleet_version`、`locked_at` 任一为空，或 `fleet_source` 不是 `schedule|drawing` → **exit 5**，打印「先锁口径再校核」，不生成任何结论文件；出图同样 exit 5。

## 计算规则（写死，阈值可配）

| 项 | 规则 |
|---|---|
| 需求吊重 | `demand_t = weight_t × dynamic_factor + hook_weight_t`；默认 1.1、0.3 t |
| 幅度 | `radius_m = hypot(crane.x - member.x, crane.y - member.y)`，坐标必须为米 |
| 归属 | 仅 `crane.zones` 含 `member.zone` 的塔吊；取幅度最小且 ≤ `jib_m` 的一台；没有 → `blind` |
| 额定 | 按 `capacity_table` 线性插值；超出最小/最大幅度 → `out_of_range` |
| 无表 | `capacity_source=missing` 或表为空/无效 → `unknown_no_table`，永不输出肯定结论 |
| 利用率 | `utilization = demand_t / capacity_t` |
| 判定 | `≤0.85` → `ok`；`(0.85,1.0]` → `review`；`>1.0` → `insufficient` |
| 缺重量 | `weight_t=null` → `unknown_no_weight`，不补 0 |
| 结论等级 | 默认 `estimated`；仅当全部塔吊均为 `manufacturer` 且有有效表 → `estimated_confirmed_inputs`，仍不是正式签认 |

坐标单位只接受米。`site_handoff`/`crane_fleet` 顶层或成员声明 `cm`/`mm`/`ft` → **exit 4**；未声明时按 `x_m/y_m` 的米制含义处理。拒绝按 10/1000 倍猜测。

## 校核调用

```bash
cd site-layout-plan
python3 scripts/crane_check.py \
  --handoff site_handoff.json \
  --fleet crane_fleet.json \
  --baseline baseline.json \
  --out-dir out/crane
```

可选：`--dynamic-factor 1.1`、`--hook-weight 0.3`。

输出 `out/crane/{crane_check.csv,crane_check.json,crane_check.md}`。`crane_check.json` 固定包含 `final_check=false`、`conclusion_grade`、`summary` 和 `inputs.baseline`。

## 报告阅读顺序

1. **不合格（insufficient）**：利用率 >1.0，必须改布置、换设备或降重。
2. **盲区（blind）**：同分区无塔吊或幅度超臂长，禁止跨区就近凑数。
3. **无性能表（unknown_no_table）**：D 系列等无厂家表设备，结论只能是未知。
4. **估算项**：`confidence=estimated` 的柱全部单列；补厂家表后再复核。
5. **逐柱明细**：带坐标、幅度、额定、需求、利用率，便于回图核对。


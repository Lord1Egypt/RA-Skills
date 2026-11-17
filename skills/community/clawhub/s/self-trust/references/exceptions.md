# exceptions — 申诉/覆写/护栏修改/重置冷路径（§5.2 / §5.4 / §7.1.1）

> 适用：驳回后申诉、连续 3 次触发人工覆写、修改契约核心护栏字段、整体重置。低频，别陪跑高频审批。
> 全局参数（--data-dir / --today / JSON 输出）见 SKILL.md。

## 1. 申诉流程（§5.2）——已实装

```bash
python scripts/cli.py appeal --request-id <id> --reason "<理由>"
```

1. 引擎按 §4.4 **同一判定逻辑**重审（不换标准），输出 `decision` / `upheld`；
2. 仍 C（`upheld=true`）→ 维持驳回，`appeal_count += 1`（按 request_id 关联，换申请自动归零；重审改判则归零）；
3. `appeal_count >= 3` → 输出 `override_open=true`，开放**一次性**人工复核覆写入口，提示「请作为配置者亲自裁决」。

每次申诉落 appeal_log（仅追加）。

## 2. 人工覆写（§5.2）——已实装

```bash
# 第一步（无 --confirm）：返回 need_confirm + target_impact（目标延后测算，F5/F7）
python scripts/cli.py appeal --request-id <id> --override
# 第二步：用户确认知悉延后时长后
python scripts/cli.py appeal --request-id <id> --override --confirm
```

- 前置条件：同一 request_id 连续满 3 次申诉被驳（否则 `error=override_not_open`）；
- 覆写前**必须确认知悉目标延后时长**：转述 `target_impact`（delay_months_simple + impacted_objectives，原样引用）；
- 落 `override_log`（时间/金额/目标延后影响/确认语，仅追加）；
- 覆写消耗申诉计数（归零）；仅作用当次支取，**不改契约结构**；
- 月度报表单列「本期人工复核次数与影响」。

## 3. 护栏修改闸门（§5.4）

核心护栏字段：`safety_cushion` / `invest_ratio` / `objectives[].target_amount|deadline|weight` / `living_baseline` / `fast_track_whitelist` / `calc_params` / `optimization_goal`（切向收紧态）。

三道闸门：
1. **回显对比**：修改前 vs 修改后 + 具体数字后果（如「安全垫 6 月 → 2 月，抗风险大幅下降」）；
2. **二次确认**：用户显式回复「确认修改」才生效（引擎层对应 `write_contract(confirm=True)`，已实现强制）；
3. **冷静窗**[待实施]：削弱型修改（垫下调/invest_ratio 下调）额外 1 自然日可撤回窗。

确认通过 → 落契约 + 写 `override_log`（参数修改留痕）。
非核心字段（allowed_categories 微调、mode 切换）走普通确认，不过度摩擦。
注：`记账自定义` 交互式修改入口尚待实施（见 STATUS.md），引擎层闸门已强制。

## 4. 记账重置（§7.1.1）——已实装

唯一整文件重建入口，二次确认闸门：

```bash
# 第一步（无 --confirm）：返回 need_confirm 警示
python scripts/cli.py reset
# 第二步：用户说「确认重置」后，须同时给出新契约 3 项
python scripts/cli.py reset --confirm --corpus <元> --monthly <元> \
    --objective "名称:目标额:期限" [--objective ...] [--reason "<原因>"]
```

- 仅重写 contract.json，**audit/ 全部保留**（§10.1 仅追加不可删）；
- `override_log` 先记 `event=contract_reset`（含旧契约 sha256，先记后删链条不断）；
- 输出 `reset=true` + `old_contract_sha256` + 新契约回执（复用 init 懒人模板护栏）。

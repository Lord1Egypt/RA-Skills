# contract-schema — schema 字段 + 三区权限表（§2 / §10.3，排障用）

> 运行时基本不读；排障/开发时对照。完整 schema 以设计文档 §2 为真相源，代码映射在 `scripts/core/models.py`。

## 1. 数据布局

```
<data-dir>/
├── contract.json          # 契约（配置区 + 运行态区）
└── audit/                 # 审计区（物理分离，仅追加 .jsonl）
    ├── approval_log.jsonl     # F8 快照：每笔审批完整中间变量
    ├── appeal_log.jsonl
    ├── override_log.jsonl     # 覆写/护栏修改/契约重置事件
    ├── reward_log.jsonl
    └── monthly_history.jsonl  # 月度快照（§6.1 趋势图数据源）
```

data-dir 解析：`--data-dir` > `SELFTRUST_DATA_DIR` > 默认 `<home>/.claw/self-trust/`（规范 §3 平台基址，Path.home() 锚定；零 cwd 依赖，在 skill 目录外、`.claw` 备份树内）。

## 2. 三区权限表（§10.3，`models.FIELD_ZONES` 强制）

| 区 | 字段 | 写权限 |
|---|---|---|
| 配置区（引擎只读） | version, **currency**, **crypto**, corpus, corpus_status, liabilities, rigid_annual_expenses, monthly_contribution, safety_cushion, objectives, distribution_rules, mode, cooldown_days, cooldown_threshold, fast_track_whitelist, optimization_goal | 仅配置者；核心护栏字段（CORE_GUARD_FIELDS）须 §5.4 二次确认 |
| 运行态区（引擎可写） | reconcile, whitelist_cap_year, appeal_count, pending_requests, pending_config_changes, pending_import, rebalance_override, last_calibrate, last_report_date, report_streak, gap_streak, monthly_is_gross_estimate | 引擎按既定规则更新 |
| 配置区内嵌运行态子字段（白名单） | objectives[].lag_streak / reward_unlocked / reward_quota / status（仅 active→overdue）；fast_track_whitelist[].used_annual | 引擎可写这些子字段；其余 objectives 结构（target/deadline/weight 等）仍引擎只读 |
| 审计区（仅追加） | approval_log, appeal_log, override_log, reward_log, monthly_history | 禁入 contract.json；只经 core/audit.py append |

违规写入 → `GuardError`（显式报错不吞），由 `test_contract_guard.py` 全量守护（测试价值序最高）。

## 3. 关键字段速查

- `corpus_status`：manual | imported_pending（**禁审批**，§7.3 拉取待核对）| imported_confirmed（§7.3 核对确认后生效）；
- `pending_import`：§7.3 导入候选暂存（RUNTIME 区），含 `source` / `candidates` / `prior_status` / `token` / `staged_at`；确认后清空、live corpus 才写入（取消则还原 prior_status，live 资产不污染）；
- `pending_requests[].status`：cooling → withdrawn | decided | expired（终态封闭，`models.can_transition`）；
- `objectives[].status`：active（缺省）| completed | overdue | archived（§6.4）；
- `fast_track_whitelist[]`：{name, per_tx_cap, annual_cap, used_annual}，used_annual 属运行态语义、跨年归零（whitelist_cap_year 判定）；
- `rebalance_override`：校准临时层，次月回滚，**不改原始 objectives**；
- `distribution_rules.calc_params`：inflation=0.025 / drawdown_factor=0.10 / r_gross=0.05（F3.5/F7 口径）。
- `monthly_is_gross_estimate`（运行态区）：月净流入口径标记，`true`=毛口径待校准（未录负债/刚性），`false`=净口径。旧契约缺省时由 `models.monthly_basis()` 按「是否录负债/刚性」推断（有→net，无→gross_estimate）；录入负债/刚性后由 customize 自动置 `false`，删除后置 `true`。**仅展示用，不进任何判定**（F0/F1/F2/judge 仍用原始 `monthly_contribution`）；详见 `references/rendering.md` §1.5 / §3 / §5。
- `currency`：基准币种代码（默认 CNY），渲染层符号来源（CURRENCY_SYMBOLS 映射）；judge 非 CNY 消费须 `--currency` + `--rate` 换算到基准币种后判定。
- `crypto`：静态加密配置（默认 `{"enabled": false, "mode": "passphrase", "kdf": "pbkdf2", "iterations": 200000, "key_file": null}`）；启用后契约与审计日志整文件 AES-256-GCM 加密；`mode=keyfile` 时 `key_file` 存密钥文件路径（相对 data-dir）；详见 `references/init.md` 加密开关与 `core/crypto.py`。

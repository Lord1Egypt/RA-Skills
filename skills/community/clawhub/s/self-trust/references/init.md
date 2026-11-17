# init — 初始化引导（§7.1 / §7.2 / §7.4）

> 全局参数（--data-dir / --today / JSON 输出）见 SKILL.md。

## 1. 懒人一键模板（§7.1）——已实现

必填仅 3 项，其余固化 balanced 默认值：

```bash
python scripts/cli.py init --corpus <总资产> --monthly <月净流入> \
    --objective "名称:目标额:期限" [--objective ...]   # 1~3 个
```

`--objective` 格式 `名称:目标额:期限`，目标额/期限可省略（无期限目标只写 `名称` 或 `名称:目标额`）。

- `--monthly` 按**净口径**填（税后收入 − 负债月供 − 刚性年支出月摊，公式 F0）；懒得细算可先填毛额，回执会附 ⚠️ 净口径警告。
- 固化默认值（§7.1 表）：living_baseline=auto（monthly×0.5）、safety_cushion=months×6、invest_ratio=0.5、mode=hybrid、optimization_goal=balanced、cooldown_days=3、目标等权 1/N、start_date=当日。

护栏（引擎强制，全部已实现）：
1. **重复初始化拒绝覆盖**：已存在契约 → 返回 `error=exists`，引导 `记账自定义`[待实施] / `记账重置`（`reset --confirm ...`，见 references/exceptions.md §4）；
2. **净口径警告**：未录负债/刚性支出 → warnings 附提示；
3. **deadline 校验**：不晚于当日的目标被驳回（`rejected_objectives` 列出），不生成负周期；
4. **对账锚点**：`reconcile.last_reconcile` = 初始化当日（§3.2 30 天窗口起算）。

回执渲染：转述 warnings 与 rejected_objectives，最后附「已生成默认契约，可随时说『自定义』逐项调」。

## 2. 三场景模拟演示（§7.2）——已实装（真实引擎干跑）

```bash
python scripts/cli.py demo
```

- init 成功回执自动附 `demo` 区块；`记账演示` 随时重看（即上述命令）；
- 有契约 → 用真实契约参数推算（deepcopy 隔离）；无契约 → 演示专用默认值（纯内存，
  `demo_defaults_used=true` 且 notes 首行标「⚠️ 演示数据，非您的真实契约」）；
- 干跑走 judge 纯函数：不落盘、不入冷静期队列、不写审计；全部数字来自引擎真实输出
  （`engine_params` 回显阈值/安全垫/corpus/月度净流入，可验算）；
- 三场景金额首选 §7.2 表格值（35/6000/30000），若与当前契约不匹配则由引擎中间变量
  确定性推导替代金额（保证 A/冷静期/C 三类判定都真实命中）；场景 3 附分期替代方案
  （`alt_plan_scenario3`，N 由阈值推导）。
渲染模板见 `references/rendering.md` §4（demo）；务必声明：「这是演示，不影响真实账户」。

## 3. 生活费基线三模式（§7.4）[自定义待实施]

- `auto`（默认）：monthly_contribution × 0.5，随注入额联动；
- `manual`：用户固定额；
- `history3m`：近 3 月均值，无历史回退 auto（引擎 `living_baseline_value()` 已实现取值逻辑）。

## 4. 静态加密开关（方案 C，opt-in 默认关）——已实现

本地账本是完整财务画像（资产/负债/消费习惯），默认明文存 `<home>/.claw/self-trust/`，
可能被云同步（OneDrive/iCloud/百度网盘）误带上云。启用加密后契约与审计日志整文件
AES-256-GCM 加密（防篡改 + 保密），密钥派生 passphrase → PBKDF2-HMAC-SHA256（20 万轮）。

```bash
# passphrase 模式（推荐，密钥不落盘）：每次操作须 --pass 或 SELFTRUST_PASS
python scripts/cli.py --pass <密码> init --corpus 200000 --monthly 8000 \
    --objective "FIRE:3000000:2036-01-01" --encrypt --crypto-mode passphrase

# key-file 模式（无感，自动生成密钥文件权限 600）：迁移须带走 .self-trust.key
python scripts/cli.py init --corpus 200000 --monthly 8000 \
    --objective "FIRE:3000000:2036-01-01" --encrypt --crypto-mode keyfile
```

两种密钥路线（CLI 全局参数 `--pass` / `--key-file`，须置于子命令前；亦可用环境变量
`SELFTRUST_PASS` / `SELFTRUST_KEY_FILE`）：

| 路线 | 密钥材料 | 体验 | 安全 |
|---|---|---|---|
| **passphrase** | 用户密码 | 每次操作需 `--pass`（或 env），密码不落盘 | 最高 |
| **keyfile** | 自动生成 `<data-dir>/.self-trust.key`（600） | 无感，key-file 模式自动定位密钥 | 防云同步泄露/窥探够用；key 与密文同备份，防定向窃取不足 |

行为：
- 启用后契约 `crypto.enabled=true`，落盘为加密字节（魔数 `STENC1` 头）；
- 所有读/写（契约 + `audit/*.jsonl`）自动加解密，旧明文契约向后兼容（无魔数头→明文直读）；
- 缺密钥（未传 `--pass`/密钥文件丢失）→ 引擎返回 `error=crypto`（退出码 5）；
- 密码错误 → `InvalidPassphrase`（同一退出码 5）；
- **keyfile 模式密钥文件丢失 = 数据不可恢复**，回执附 ⚠️ 警告；
- 依赖：加密功能需 `cryptography`（`pip install cryptography`），非加密路径纯标准库零依赖。

切换加密开关：当前不支持「已初始化契约在线切换加密状态」——如需切换，请 `reset --confirm`
重建契约并在新 init 时决定是否加密（reset 保留 audit 历史，但历史审计若曾明文不回溯加密）。

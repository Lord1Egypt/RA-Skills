# 原生定时同步

本功能让 Mac/iPhone 的勾选完成在后续周期同步时回写台账。正常周期运行直接执行脚本，不调用模型、不消耗模型 token；首次配置及用户主动排障仍可能使用助手。技能保持平台通用：优先使用能够直接执行固定命令、且确认不调用模型的宿主调度，不能满足时使用 Mac 用户级 LaunchAgent。

## 时间规则

时区固定 `Asia/Shanghai`，每天包含周末和节假日，共 80 个计划时点：

| 时间 | 安排 |
|---|---|
| 07:00 | 一次 |
| 09:00–21:50 | 每 10 分钟一次，共 78 次 |
| 22:00 | 最后一次 |

`--scheduled` 在访问台账及原生应用前执行轻量检查：只在合法时点所在分钟启动，成功时点持久去重，所有同步入口共享同步锁。同一台账不并发执行多个同步者；忙碌、关机、注销或休眠时不堆积补跑，下次有效时点处理最新状态。22:00 所在分钟可启动，之后不再启动当日定时同步，已启动的执行允许结束。主动运行技能仍可在其他时间同步。

## 计划、启用与停用

使用稳定安装路径和本地数据目录，避免把台账放在 iCloud 或网络共享。先按镜像流程指定列表名并完成初始化，再配置调度。已有绑定的入口可省略名称：

```sh
python3 scripts/macos_sync_schedule.py --data-dir /absolute/local/data/team-tasks --plan
python3 scripts/macos_sync_schedule.py --data-dir /absolute/local/data/team-tasks --enable
python3 scripts/macos_sync_schedule.py --data-dir /absolute/local/data/team-tasks --status
python3 scripts/macos_sync_schedule.py --data-dir /absolute/local/data/team-tasks --diagnose
python3 scripts/macos_sync_schedule.py --data-dir /absolute/local/data/team-tasks --disable
```

可显式附带 `--list-name '团队待办 · 项目甲'`；省略时沿用该台账已有绑定，不能用调度参数改绑。未配置镜像的台账不自动安装定时任务。

每次恰好指定 `--plan`、`--enable`、`--status`、`--diagnose`、`--disable` 中一个。可通过受信任配置指定 `--state-root /absolute/state` 和 `--interpreter /absolute/python3`；默认状态目录为 `~/Library/Application Support/team-tasks`，解释器与脚本均固定为实际绝对路径，后续沿用同一配置。列表绑定和锁始终位于用户级公共目录，不受该参数影响。

`--plan` 不创建文件或任务，返回平台通用的直接命令作业规范及本机后备路径。若宿主支持直接命令任务，将其指向同一个 `macos_reminders_sync.py --scheduled` 入口，按其时间规则注册或更新本功能的任务，保存任务 ID。同一台账在不同 agent 中沿用同一作业，不重复注册；不同台账各自绑定列表及注册作业。没有执行能力时报告尚未启用，不能把规范输出称为已注册任务。

Mac 后备 `--enable` 先确认 [首次镜像初始化](macos-reminders.md#首次镜像) 完成，再构建或复用固定辅助应用。先通过实际 GUI LaunchAgent → `open` → 辅助应用 → 固定解释器链路执行 `macos_reminders_sync.py --diagnose --native-check --result-file FILE --probe-token TOKEN`，核对结果及令牌。探测和周期配置均将解析后的 `--list-name` 作为独立参数固定传递，并在注册记录中保存目标名；只有成功后才注册每 60 秒唤起轻量检查器的周期任务。通常只有 80 个合法分钟执行完整同步，其余检查不会访问提醒事项。启用失败时不会保留一个未经验证的周期作业。

辅助应用位于 `stateRoot/schedules/<数据目录完整 SHA-256>/TeamTasksReminders.app`，LaunchAgent 标签及应用标识固定为 `com.team-tasks.reminders-sync.<SHA-256 前20位>`。应用由系统 `osacompile` 构建，包含 `NSAppleEventsUsageDescription`，同一配置复用同一身份以维持授权；用户拒绝时停止，不更换标识重试。实际后台身份需有本地台账和提醒事项读取权限，交互终端成功不能代替后台探测。

`--status` 查看本功能配置、目标名称及状态；镜像状态损坏时状态查询与停用仍可管理本功能的调度。调度管理器的 `--diagnose` 使用同一后台链路显式启动一次 15 秒原生列表探测；同步脚本自身的普通 `--diagnose` 仅查询本地，两个入口不要混用。`--disable` 只停用本功能标签的 LaunchAgent，不删除台账、原生列表、映射、初始化日志或其他调度任务。已经配置正确时正常使用直接沿用，不重复初始化或安装。

数据目录搬迁前先对旧目录执行 `--disable`，再按 [更换数据目录 / 换宿主](macos-reminders.md#更换数据目录--换宿主) 迁移镜像绑定。调度配置及辅助应用按数据目录路径定位，不随镜像 `--rebind` 自动迁移；随后对新目录重新 `--plan` 和 `--enable`，验证新后台身份的读取权限。不要同时启用新旧两个路径的作业。

## 状态与接入边界

绑定和列表锁位于固定用户公共目录；辅助应用、探测结果和执行日志保存在所配置的专用状态目录。旧后台命令不带列表名时自动沿用原绑定，已有标签、应用标识和安装路径保持兼容。权限失效或执行失败保留原因，不自动唤醒模型；排障先读取 `--status`，再按相同身份 `--diagnose`，禁止因错误而清空映射或重新初始化原生列表。

本功能仅维护自身的 LaunchAgent、辅助应用及保存的直接命令任务 ID，不改既有催办任务、年度日历维护任务或其他 job。原生同步不领取或确认 outbox；完成回写在存储层产生的两条普通事件仍交给既有 worker。平台作业仅负责触发，台账处理和原生读写必须在能够访问目标 Mac 数据及该用户提醒事项的执行端完成。

打包阶段不创建真实辅助应用、不初始化真实提醒事项、不安装后台任务。交付时分别说明代码/模拟测试、实际初始化、后台权限验证和周期任务注册结果；只完成打包不能报告定时同步已启用。

## 普通会话保存后的反馈

业务保存不立即执行原生同步，由持久台账保留全部修改，下个合法时点统一读取最新状态。白天仍每十分钟一次，夜间等次日 07:00；完成时间还需加上原生读取和写入耗时。无额外待同步队列，不占用通知 outbox。使用 `macos_reminders_sync.py --data-dir DATA --sync-status` 只读查询镜像、加载状态、下一时点和最近执行结果；它不触发后台权限诊断。最近失败必须同时报告，不能把已注册作业等同于同步成功。

1.6.6 的后台授权结果须包含 `nativeProbeVerified=true`、正确列表名及当前令牌；本地诊断不能充当权限证明。周期同步仍走原有时点和 120 秒全量桥，闲时检查与去重规则不变。普通聊天状态查询不调用调度管理器的原生 `--diagnose`，只调用同步脚本的本地入口。

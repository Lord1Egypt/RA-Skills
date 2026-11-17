# 卡住自愈怎么接自动化

worker 活在宿主的生命周期里：Gateway 重启、Mac 重启、宿主回收都会让它中途消失，
job 停在某个 stage 且不再有通知。`scripts/resume-stalled.py` 负责"发现 + 断点续跑"，
这里给出三种接法，按你的环境选一种。

## 判定与恢复逻辑

- 卡住 = 没有存活的 `worker.py <job_id>` 进程 **且** `updated_at` 超过阈值（默认 20 分钟）
- 续跑起点按落盘产物推断：`episode.m4a` → uploading；`audio.wav` → postprocess；
  有 `source_id` → generating；否则 sourcing
- 因此已生成的音频不会重做，**不重复消耗 NotebookLM 配额**

```bash
python3 scripts/resume-stalled.py                     # 只检查,输出 JSON
python3 scripts/resume-stalled.py --quiet             # 没情况就零输出(省 token)
python3 scripts/resume-stalled.py --resume            # 前台顺序续跑
python3 scripts/resume-stalled.py --max-age 30        # 自定义阈值(分钟)
```

退出码：`0` 正常、`10` 有卡住的 job（仅检查模式）、`1` 续跑中有失败。

## 接法 A：心跳巡检（推荐，成本近零）

在你自己的 `HEARTBEAT.md` 里加一条（**这是你的配置，任何 skill 都不应该偷偷改它**）：

```markdown
- **yt2podcast 巡检**：跑 `python3 ~/.openclaw/skills/yt2podcast/scripts/resume-stalled.py --quiet`；
  退出码 10 → 用后台托管方式跑 `worker.py <job_id>`（或 `--resume`），跑完把结果告诉我；
  退出码 0 → 什么都不说。
```

没有任务时脚本毫秒级退出且零输出，不会产生噪音。

## 接法 B：cron 定时（更准时，不依赖心跳）

用 OpenClaw 自带的 automations（不需要 agent 回合也能跑命令）：

```bash
openclaw cron add yt2podcast-watchdog \
  --cron "*/20 * * * *" \
  --command "python3 ~/.openclaw/skills/yt2podcast/scripts/resume-stalled.py --quiet"
```

注意：`--command` 只做"检查"，退出码 10 表示有待处理的 job。要让它真的续跑，用
`--command "python3 ~/.openclaw/skills/yt2podcast/scripts/resume-stalled.py --resume"`
——这会串联跑完整条流水线（可能几十分钟），适合"只有一个任务、慢点也没关系"的场景。
删掉：`openclaw cron rm yt2podcast-watchdog`。

## 接法 C：手动

不接任何自动化。发现某集没出结果时：

```bash
python3 scripts/resume-stalled.py --resume
```

## 为什么不让 skill 自己装定时任务

往用户的系统里偷偷装 cron / systemd / launchd 是"超出描述的行为"，
也是安全扫描最容易判 suspicious 的一类，故本 skill 只提供脚本和说明，安装与否由你决定。

# swanlog

一个用于 Claude Code / Codex 的 **skill**，可以一键把 [SwanLab](https://swanlab.cn) 云端实验（指标、配置、元信息、依赖、运行信息）拉到本地目录，然后给你一份简报告诉你拿到了什么。

为这种常见场景而生：在远程 GPU 机器上训练、把日志写到 SwanLab，但又想在自己的笔记本上看实验、借助**Claude Code/Codex**对比 run，又不想每次都 SSH 到服务器。

## 它做什么

给定一个实验 ID（或 `--latest`），这个 skill 会：

1. 通过本地 `~/.swanlab/.netrc` 凭据登录 SwanLab。
2. 拉取实验的 `metrics`（整理成 `metrics.csv`）、解析后的 `config.yaml`、`metadata.json` 快照，以及 `requirements.txt`。
3. 全部保存到 `./swanlog_<YYYY-MM-DD_HH-MM-SS>/`，命名使用 `run.created_at` —— 因此对同一个 run 重复拉取**目录名稳定**（幂等）。
4. 返回一屏简报：run 名称 / 状态 / URL / 最新 train & val loss。

## 安装

### 作为 Claude Code skill

```bash
git clone https://github.com/jasonwei1002/swanlog ~/.claude/skills/swanlog
```

之后在任意 Claude Code 会话里，让 Claude "拉一下 swanlab" / "pull the latest swanlab run" 等，skill 会自动触发。

> **认证**：只要你在终端执行过一次 `swanlab login`，凭据就会缓存在 `~/.swanlab/.netrc` 里 —— skill 会自动读取，无需额外配置。

### 作为独立 CLI

```bash
git clone https://github.com/jasonwei1002/swanlog
cd swanlog
pip install -r requirements.txt
swanlab login    # 只需一次，凭据写入 ~/.swanlab/.netrc

python scripts/fetch_swanlog.py --latest --project MyProject
```

## 使用方式

```bash
# 最近一次 run —— 自动识别这次 run 写过的所有标量指标
python scripts/fetch_swanlog.py --latest --project MyProject

# 通过 ID 指定 run（从 WebUI URL 复制即可）
python scripts/fetch_swanlog.py --exp-id <experiment_id> --project MyProject

# 自定义输出目录
python scripts/fetch_swanlog.py --latest --project MyProject -o /tmp/swanlab-dump

# 白名单只拉子集（会覆盖自动枚举）
python scripts/fetch_swanlog.py --latest --project MyProject \
  --keys "train/loss,val/loss_mean"

# 也可以从文件读取 key（每行一个，支持 # 注释）
python scripts/fetch_swanlog.py --latest --project MyProject --keys-file keys.txt

# 覆盖输出目录命名所用的时区
# （默认跟随系统本地时区 —— 只有当你想固定一个时区时才设置，
# 比如 CI runner 上你控制不了 TZ 的情况）
python scripts/fetch_swanlog.py --latest --project MyProject --tz Asia/Shanghai
```

也可以在 shell 里设置 `SWANLAB_PROJECT=MyProject`，这样就能省掉 `--project` 参数。

### 默认行为

默认情况下，脚本会向 SwanLab 询问这次 run 写过的所有标量列（FLOAT / INTEGER），然后全部拉下来 —— 你不需要提前知道训练循环写了什么。图像 / 音频 / 文本类型的列会被跳过（放不进扁平 CSV）。

如果枚举接口失败（比如 SwanLab API 变更、认证问题），脚本会打印警告。

## 输出目录结构

```
swanlog_<YYYY-MM-DD_HH-MM-SS>/
├── metrics.csv         # 所有标量指标，按 step 索引为列
├── config.yaml         # 该 run 中解析后的 Hydra / 你自己框架的配置
├── metadata.json       # SwanLab 快照：硬件、操作系统、git SHA…
├── requirements.txt    # run 启动时捕获的 pip freeze
├── run_info.json       # 名称 / id / 状态 / 创建时间 / 结束时间 / URL
└── brief.md            # 人类可读的摘要：run 表头 + 每个标量指标的最近一个
                        # 非 NaN 值（带 step）
```

Claude skill 就是读 `brief.md` 来给你总结这个 run 的 —— 这套格式同样适合人类直接翻阅目录。

## 用 AI 分析训练日志

一旦 run 被拉到本地，整个目录就是纯文本 —— `metrics.csv`、`config.yaml`、`metadata.json`、`brief.md`。这意味着你可以直接把它扔给任何编码 agent（Claude Code、Codex、Cursor 等）做更深入的分析，agent 完全不需要 SwanLab 凭据或网络访问。

常见的追问示例：

- "读一下 `brief.md`，告诉我这个 run 是收敛了还是仍在下降？"
- "用 `metrics.csv` 画 `train/loss` vs `val/loss`，标出可能过拟合的地方。"
- "对比这次和上次的 `config.yaml`，告诉我改了什么。"
- "对比这三个 `swanlog_*` 目录的 `metrics.csv`，选出最好的 checkpoint。"
- "读一下 `metadata.json` —— 这个 run 用的 GPU / git SHA 是不是和 baseline 一致？"

由于每次 dump 都是自包含的、且按 `run.created_at` 幂等命名，你可以把多个 run 并排放在一起，让 agent 跨 run 推理。

## 依赖

- Python 3.9+（用到 `zoneinfo`）
- `swanlab>=0.7.15`、`pandas`、`omegaconf`
- 一个 SwanLab 账号，并通过 `swanlab login` 登录过一次

## License

MIT

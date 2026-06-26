# skill-perf 🧪

OpenClaw Skill 性能测量工具——测量 Skill 的 Token 净消耗，生成可视化 HTML 报告。

## 工作原理

在同一个 turn 内并发 spawn 两个 Subagent：

- **标定 subagent**：只输出 `ANNOUNCE_SKIP`，测量系统底噪
- **测试 subagent**：完整执行被测 Skill，记录 token 消耗

两者并发运行，结束后自动从 `.jsonl` 读取 `totalTokens`，计算净消耗并生成 HTML 报告。

底噪每次实测，不使用固定值（底噪会随 OpenClaw 版本、工具数量变化而漂移）。

## 安装

```bash
git clone git@github.com:<your-fork>/skill-perf.git ~/.openclaw/skills/skill-perf
```

## 使用

安装后，直接在 OpenClaw 中说：

```
帮我测量 html-extractor 的 token 消耗
```

skill-perf 会自动完成：spawn 两个 subagent → 等待完成 → 读取数据 → 生成 HTML 报告。

也可以手动触发报告生成（两个 subagent 已完成时）：

```bash
python3 ~/.openclaw/skills/skill-perf/scripts/snapshot.py report \
    --session "<TEST_childSessionKey>" \
    --calib-key "<CALIB_childSessionKey>" \
    --skill-name "<skill名>"
```

## 各 Skill 净消耗参考（热缓存稳态）

| Skill | net_tokens | totalTokens | 备注 |
|---|---|---|---|
| 空跑（底噪基线）| ~0 | ~18,100 | 系统底噪，自动扣除 |
| html-extractor（单篇文章）| ~2,000 | ~20,000 | 热缓存稳态 |

> 📖 Token 字段详解 → [`references/TOKEN_GUIDE.md`](references/TOKEN_GUIDE.md)

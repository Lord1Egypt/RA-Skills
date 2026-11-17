# Description 自动优化 — 在 Claude Code 中执行

## 前置条件
- 已安装 Skill Creator 技能（提供 `scripts/run_loop.py`）
- 已安装 qa-team-skills（当前项目）

## 执行步骤

```bash
cd /path/to/qa-team-skills

# 确认 eval 集就绪
ls evals/trigger-eval.json

# 跑优化循环（约 5-10 分钟）
python -m scripts.run_loop \
  --eval-set evals/trigger-eval.json \
  --skill-path . \
  --model $(cat VERSION | head -1) \
  --max-iterations 5 \
  --verbose
```

## 预期输出
```
Iteration 1/5: train=0.82 test=0.75
Iteration 2/5: train=0.86 test=0.81
...
Best description: "..."
```

## 应用
将输出的 `best_description` 复制替换 `SKILL.md` 的 frontmatter 中 `description:` 字段。
提交变更：`git add SKILL.md && git commit -m "chore: description 自动优化"`

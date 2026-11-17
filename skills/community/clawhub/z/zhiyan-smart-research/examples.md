# Examples · v1.1

## 标准提问

**User:** CRISPR 基因编辑在遗传病治疗中的最新进展和研究空白是什么？

**Agent:**

```bash
python3 {baseDir}/scripts/search_literature.py "CRISPR gene editing genetic disease therapy research gap" > /tmp/papers.json
```

按 [templates/report-template.md](templates/report-template.md) 撰写六节报告 → 保存：

```bash
# 将完整报告写入 /tmp/report.md 后
python3 {baseDir}/scripts/save_research.py \
  --topic "CRISPR 基因编辑在遗传病治疗中的最新进展和研究空白" \
  --report-file /tmp/report.md \
  --papers-json /tmp/papers.json
```

## 追问建议示例

用户点击追问「CRISPR 脱靶效应的最新解决方案」→ 新检索 + 完整六节报告 + `--session-id` 更新。

## 追问建议（输出示例）

```markdown
## 追问建议
1. CRISPR 碱基编辑 vs 传统 CRISPR-Cas9 在遗传病中的疗效对比
2. 体内递送载体（LNP、AAV）的最新突破与局限
3. 临床 trial 阶段的安全性与长期随访数据
```

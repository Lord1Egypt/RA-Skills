# 测试：8 维权重和

> 验证 `references/.archived/flow-v7/04-scoring.md` 中 8 维权重之和为 100%。
> 注：v7 阶段式旧流程已于 v8.2.1 归档至 `references/.archived/flow-v7/`（见 `references/.archived/README.md`）。

## 输入

读取 `references/.archived/flow-v7/04-scoring.md` 权重表与公式。

## 预期输出

```text
Fit 30% + Value 20% + Fresh 15% + Community 15% + ROI 8% + Novelty 6% + Contamination 1% + Forma 5% = 100%
```

## 验证标准

- 权重表中 8 个百分比相加等于 100%。
- 公式中 8 个小数系数相加等于 1.0。
- 若和不等于 100%，则 S/A/B/C/D 阈值失效。

## 执行方式

```bash
python tests/validate.py
# 或手动检查：grep 公式行中的 0.xx 并求和
```

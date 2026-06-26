# examples/ 目录说明

包含简单的示例账本，适合初次使用时参考。

## 文件

- `sample.csv` — 最简示例，包含几个常见交易

## 使用方式

```bash
cp examples/sample.csv ~/.openclaw/workspace/data/ledger/default.csv
```

然后告诉 Agent："我的账本在 `~/.openclaw/workspace/data/ledger/default.csv`"，或者直接用路径参数调用脚本。
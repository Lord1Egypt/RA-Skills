# data/ 目录说明

此目录用于存放用户的工作数据文件。

## 文件说明

- `example.csv` — 格式示例账本，包含账户初始余额和示例交易
- `investments.csv` — 投资交易记录（买入/卖出/分红）
- `goals.json` — 财务目标数据（自动生成）
- `prices.json` — 投资品当前价格配置（手动更新）

## 用户使用

- 复制 `example.csv` 为你的工作账本
- 建议存放在 `~/.openclaw/workspace/data/ledger/default.csv`
- 也可以放在任何你喜欢的位置，脚本通过路径参数指定

## 备份

所有数据都是纯文本，建议定期备份 `data/` 目录。
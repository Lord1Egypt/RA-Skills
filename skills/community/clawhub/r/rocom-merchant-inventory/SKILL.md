---
name: rocom-merchant-inventory
description: 查询《洛克王国世界》远行商人当前库存，自动过滤出本轮仍有效的商品。适用于想查看远行商人当前卖什么，或需要输出简洁文本、JSON 结果时使用；需要用户自行提供 API key。
---

# 远行商人库存查询

查询当前远行商人库存，并自动过滤掉非当前轮次商品。

## 使用前提

- 需要 `Python 3`
- 需要 Python 包：`requests`
- 需要环境变量 `ROCOM_API_KEY`，或使用参数 `--api-key`

## API key 来源

- 请从 `https://github.com/Entropy-Increase-Team/` 相关项目或说明中获取
- 不要把 API key 写进公开仓库或公开聊天

## 远程接口

本 skill 会请求：

- `https://wegame.shallow.ink/api/v1/games/rocom/merchant/info?refresh=true`

## 用法

```bash
ROCOM_API_KEY=你的key python3 skills/rocom-merchant-inventory/scripts/fetch_inventory.py
python3 skills/rocom-merchant-inventory/scripts/fetch_inventory.py --api-key 你的key --format json --pretty
```

## 输出格式

- 默认输出简洁文本
- `--format json` 输出 JSON

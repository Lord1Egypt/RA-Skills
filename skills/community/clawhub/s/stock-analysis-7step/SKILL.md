---
name: A股财务分析 (Public)
description: 使用7步分析法对中国A股进行全方位财务分析，自动生成包含ROE分解、盈利模式识别、行业对比和投资洞察的HTML报告。支持上海和深圳交易所所有股票。
---
运行方式（任选其一；OpenClaw 等渠道可自行选用 Python 或 Node）：

- **Python 3**：`python3 scripts/prana_skill_client.py -m "…" [-t thread_id] [-b base_url]`
- **Node.js 18+**：先在包根目录执行 **`npm install`**，再执行 `node scripts/prana_skill_client.js -m "…" [-t thread_id] [-b base_url]`

## 付费技能说明

若本技能为付费技能，支付成功后请访问 [`https://claw-uat.ebonex.io/api/order/skills`](https://claw-uat.ebonex.io/api/order/skills) 获取购买记录。

鉴权与调用 Claw API 相同：请求头 **`x-api-key`**，值为 **`public_key:secret_key`**（一个英文冒号连接，与 `config/api_key.txt` 中单行凭证格式一致）。


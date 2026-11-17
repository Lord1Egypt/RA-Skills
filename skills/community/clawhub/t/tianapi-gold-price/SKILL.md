---
name: tianapi-gold-price
description: 查询黄金、白银等贵金属的实时行情，包括买入卖出价、最高最低价及涨跌幅等数据。
homepage: https://www.tianapi.com/apiview/146
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["python3"], "env": ["TIANAPI_GOLD_KEY"]}, "primaryEnv": "TIANAPI_GOLD_KEY"}}
---

# 天聚数行 - 黄金行情查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于查询黄金、白银等贵金属的实时行情数据，包括买入价、卖出价、最高价、最低价、开盘价、收盘价、最新价及涨跌幅等。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <黄金行情查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_GOLD_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_GOLD_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_gold-price.py --key 你的APIKey --kinds au9999

    ```

---

## 使用方法

### 查询贵金属实时行情

    ```bash
    # 查询指定种类的贵金属行情
    python3 scripts/fetch_gold-price.py <API_KEY> <KINDS>

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<KINDS>`: 必填，贵金属种类代码，多个用半角逗号分隔（如 `au9999,agTplusD`）。

**输出示例：**

    📈 au9999 黄金行情

    最新价: 329.02
    买入价: 329.02
    卖出价: 330.00
    最高价: 335.00
    最低价: 327.02
    涨跌幅: -0.75%
    更新时间: 2019-11-09 02:28:55

### 直接调用 API（无需脚本）

    ```bash
    # 查询 au9999 和 agTplusD 的行情
    GET https://apis.tianapi.com/gold/index?key=YOUR_API_KEY&kinds=au9999,agTplusD

    ```

---

## 使用指南

当用户需要查询黄金、白银等贵金属的实时行情时，按以下步骤操作：

1.  **识别意图**：用户想查询贵金属的实时价格或行情。
2.  **解析参数**：提取用户提供的贵金属种类代码（如 au9999）。
3.  **调用脚本**：执行 `python3 scripts/fetch_gold-price.py` 命令，传入API Key和种类代码。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示行情详情。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| code | 黄金种类代码 | au9999 |
| latestprice | 最新价 | 329.02 |
| buyprice | 买入价 | 329.02 |
| sellprice | 卖出价 | 330.00 |
| highprice | 最高价 | 335.00 |
| lowprice | 最低价 | 327.02 |
| openprice | 开盘价 | 335.00 |
| closeprice | 收盘价 | 331.49 |
| raf | 涨跌幅% | -0.75 |
| rafvalue | 涨跌额 | -2.47 |
| updatetime | 数据更新时间 | 2019-11-09 02:28:55 |
| status | 市场状态 | off |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查种类代码是否正确。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_gold-price.py` - 封装了黄金行情查询功能。

---

## 关于天聚数行

<天聚数行 (TianAPI)> 是一个致力于为个人和企业用户提供标准、简洁、高效的应用数据解决平台。API数据包括：

*   **生活服务**：天气预报、快递查询、垃圾分类等
*   **趣味娱乐**：土味情话、星座运势、周公解梦等
*   **数据智能**：文本纠错、图像识别、机器翻译等
*   **功能应用**：智能分词、坐标转换、科学计算等
*   **知识问答**：古籍查询、唐诗大全、成语典故等
*   **企业商务**：工商信息、条码识别、物流查询等

官网注册即可免费使用，在API市场查找数据，进入**API文档页面**一键申请数据，在控制台 - 我的密钥获取 **ApiKey** 接入，适合个人开发者和企业使用。在 **ClawHub** 上也可搜索 **`tianapi`** 找到更多天聚数行开放的 OpenClaw 技能。
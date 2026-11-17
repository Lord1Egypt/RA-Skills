---
name: tianapi-vin-query
description: 通过17位车架号（VIN码）查询车辆信息，包括品牌、车型年款、排量、发动机类型及指导价等。
homepage: https://www.tianapi.com/apiview/260
metadata: {"openclaw": {"emoji": "🚗", "requires": {"bins": ["python3"], "env": ["TIANAPI_VIN_KEY"]}, "primaryEnv": "TIANAPI_VIN_KEY"}}
---

# 天聚数行 - 车架号VIN查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于通过17位车架号（VIN码）解析并查询车辆的详细参数信息，包括品牌、车系、车型年款、排量、发动机类型、变速箱、驱动方式、厂家指导价等。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <车架号VIN查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_VIN_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_VIN_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_vin-query.py --key 你的APIKey --vin LSVAX60E8K2018698

    ```

---

## 使用方法

### 查询车辆VIN信息

    ```bash
    # 查询指定车架号的车辆信息
    python3 scripts/fetch_vin-query.py <API_KEY> <VIN>

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<VIN>`: 必填，17位车辆识别码（车架号）。

**输出示例：**

    🚗 车辆信息解析结果

    车架号: LSVAX60E8K2018698
    品牌: 上汽大众
    车型: 大众 途锐 2017款 3.0 TSI 拓野版
    排量: 3.0T
    发动机: 汽油
    变速箱: 8挡 手自一体
    驱动方式: 全时四驱
    厂家指导价: 71.88万

### 直接调用 API（无需脚本）

    ```bash
    # 查询车架号 LSVAX60E8K2018698 的车辆信息
    GET https://apis.tianapi.com/chavin/index?key=YOUR_API_KEY&vincode=LSVAX60E8K2018698

    ```

---

## 使用指南

当用户需要查询车辆配置、识别二手车车型或核对车辆信息时，按以下步骤操作：

1.  **识别意图**：用户想通过车架号（VIN码）查询车辆信息。
2.  **解析参数**：提取用户提供的17位车架号。
3.  **调用脚本**：执行 `python3 scripts/fetch_vin-query.py` 命令，传入API Key和车架号。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示车辆各项参数。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| vincode | 车架号 | lfv2b21k2d3534955 |
| brandname | 品牌 | 大众 |
| modelname | 车型 | 高尔夫6 |
| carline | 车系 | 高尔夫 |
| salename | 车款名称 | 1.6 手自一体 时尚版 |
| year | 年款 | 2013 |
| madeyear | 生产年份 | 2013 |
| mademonth | 生产月份 | 2 |
| displacement | 排量 | 1.6 |
| fueltype | 燃料类型 | 汽油 |
| geartype | 变速箱类型 | 手自一体变速器(AMT) |
| drivemode | 驱动类型 | 前轮驱动 |
| guidingprice | 厂商指导价 | 13.09 |
| manufacturer | 制造商 | 一汽大众 |
| vehiclelevel | 车辆级别 | 紧凑型车 |
| effluentstandard | 排放标准 | 国4 |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查车架号是否为17位且输入正确。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_vin-query.py` - 封装了车架号VIN查询功能。

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
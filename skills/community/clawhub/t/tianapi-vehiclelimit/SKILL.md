---
name: tianapi-vehiclelimit
description: 查询全国各城市的车辆限行信息，包括尾号限行规则、限行区域、时间及处罚标准。
homepage: https://www.tianapi.com/apiview/246
metadata: {"openclaw": {"emoji": "🚗", "requires": {"bins": ["python3"], "env": ["TIANAPI_VEHICLELIMIT_KEY"]}, "primaryEnv": "TIANAPI_VEHICLELIMIT_KEY"}}
---

# 天聚数行 - 城市车辆限行查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于查询全国各城市的车辆限行信息，包括尾号限行规则、限行区域、时间及处罚标准。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <城市车辆限行 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_VEHICLELIMIT_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_VEHICLELIMIT_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_vehiclelimit.py --key 你的APIKey --city 北京

    ```

---

## 使用方法

### 查询城市车辆限行信息

    ```bash
    # 根据城市名称查询限行信息
    python3 scripts/fetch_vehiclelimit.py <API_KEY> --city 北京

    # 根据城市代码查询限行信息
    python3 scripts/fetch_vehiclelimit.py <API_KEY> --code 110100

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `--city`: 城市名称，如“北京”。与 `--code` 二选一。
*   `--code`: 城市代码，如“110100”。与 `--city` 二选一。

**输出示例：**

    🚗 城市车辆限行查询

    城市: 北京
    本地车:
      - 07月13日周一(今天): 尾号 1 和 6 限行
    外地车:
      - 07月13日周一(今天): 尾号 1 和 6 限行
    限行详情:
      - 本地燃油: 工作日07:00-20:00（节假日除外），五环路以内道路（不含五环路）...

### 直接调用 API（无需脚本）

    ```bash
    # 根据城市名称查询
    GET https://apis.tianapi.com/vehiclelimit/index?key=YOUR_API_KEY&city=北京

    # 根据城市代码查询
    GET https://apis.tianapi.com/vehiclelimit/index?key=YOUR_API_KEY&code=110100

    ```

---

## 使用指南

当用户需要查询某个城市的车辆限行信息时，按以下步骤操作：

1.  **识别意图**：用户想查询某城市的车辆限行规则、尾号或区域。
2.  **解析参数**：提取用户提供的城市名称或城市代码。
3.  **调用脚本**：执行 `python3 scripts/fetch_vehiclelimit.py` 命令，传入API Key和查询参数。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示限行信息。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| city | 限行城市 | 北京 |
| localcar | 本地车限行情况 | `[{"date": "07月13日周一", "weihao": "1和6"}]` |
| foreigncar | 外地车限行情况 | `[{"date": "07月13日周一", "weihao": "1和6"}]` |
| limitinfo | 详细限行规则 | 包含动力类型、规则、时间、区域等信息的数组 |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查城市名称或代码是否正确。 |
| `code: 280` | 缺少必要参数，检查是否传递了 `city` 或 `code`。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_vehiclelimit.py` - 封装了城市车辆限行查询功能。

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
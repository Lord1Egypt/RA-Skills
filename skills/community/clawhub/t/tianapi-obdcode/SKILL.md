---
name: tianapi-obdcode
description: 查询车载诊断系统（OBD）故障码含义，包含适用车型、故障范围及维修建议。
homepage: https://www.tianapi.com/apiview/247
metadata: {"openclaw": {"emoji": "🚙", "requires": {"bins": ["python3"], "env": ["TIANAPI_OBDCODE_KEY"]}, "primaryEnv": "TIANAPI_OBDCODE_KEY"}}
---

# 天聚数行 - 汽车OBD故障码查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于查询车载诊断系统（OBD）故障码含义，返回适用车型、中英文含义、故障范围和描述等信息。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <汽车OBD查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_OBDCODE_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_OBDCODE_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_obdcode.py --key 你的APIKey --code P267B

    ```

---

## 使用方法

### 查询OBD故障码信息

    ```bash
    # 根据OBD故障码查询详细信息
    python3 scripts/fetch_obdcode.py <API_KEY> --code P267B

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `--code`: 必填，需要查询的OBD故障代码，例如 `P267B`。

**输出示例：**

    🚙 OBD故障码查询结果

    故障代码: P267B
    适用车型: 该OBD故障码适用于所有汽车制造商
    故障范围: 计算机或辅助输出
    中文含义: B摇臂执行器位置传感器电路范围/性能 （第2排）
    英文含义: B Rocker Arm Actuator Position Sensor Circuit Range/Performance (Bank 2)
    详细描述: 可变气门正时系统中，摇臂是连接凸轮轴和气门的一个装置。电子控制模块可以通过改变到摇臂执行器的机油压力的方式来调整凸轮轴的角度...

### 直接调用 API（无需脚本）

    ```bash
    # 根据OBD故障码查询
    GET https://apis.tianapi.com/obdcode/index?key=YOUR_API_KEY&code=P267B

    ```

---

## 使用指南

当用户需要查询汽车OBD故障码的含义时，按以下步骤操作：

1.  **识别意图**：用户提供了一个OBD故障码（如P0101, P267B等），希望了解其含义。
2.  **解析参数**：提取用户提供的故障码。
3.  **调用脚本**：执行 `python3 scripts/fetch_obdcode.py` 命令，传入API Key和故障码。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示故障码的中文/英文含义、适用车型、故障范围及详细描述。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| code | 故障代码 | P267B |
| descr | 故障详细描述 | 可变气门正时系统中，摇臂是连接凸轮轴... |
| ennote | 含义（英文） | B Rocker Arm Actuator Position Sensor... |
| zhnote | 含义（中文） | B摇臂执行器位置传感器电路范围/性能 （第2排） |
| carmodel | 适用车型 | 该OBD故障码适用于所有汽车制造商 |
| category | 故障范围类型 | 计算机或辅助输出 |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查故障码是否正确。 |
| `code: 280` | 缺少必要参数，检查是否传递了 `code` 参数。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_obdcode.py` - 封装了汽车OBD故障码查询功能。

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
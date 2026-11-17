---
name: tianapi-lunar-calendar
description: 查询中国老黄历，获取指定日期的宜忌、冲煞、吉时、胎神等传统民俗信息。
homepage: https://www.tianapi.com/apiview/45
metadata: {"openclaw": {"emoji": "📅", "requires": {"bins": ["python3"], "env": ["TIANAPI_LUNAR_CALENDAR_KEY"]}, "primaryEnv": "TIANAPI_LUNAR_CALENDAR_KEY"}}
---

# 天聚数行 - 中国老黄历技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

查询中国老黄历，获取指定日期的宜忌、冲煞、吉时、胎神等传统民俗信息。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <中国老黄历 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_LUNAR_CALENDAR_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_LUNAR_CALENDAR_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_lunar_calendar.py 你的APIKey 2024-07-13

    ```

---

## 使用方法

### 查询黄历信息

    ```bash
    # 查询当天黄历
    python3 scripts/fetch_lunar_calendar.py <API_KEY>

    # 查询指定公历日期
    python3 scripts/fetch_lunar_calendar.py <API_KEY> <DATE>

    # 查询指定农历日期
    python3 scripts/fetch_lunar_calendar.py <API_KEY> <DATE> 1

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<DATE>`: 选填，查询日期。支持公历日期（如 `2024-07-13`）或农历日期（如 `2024-6-8`）。默认为当天。
*   `1`: 选填，当查询农历日期时，第三个参数需传 `1`。注意农历日期不能有前导零。

**输出示例：**

    📅 2024年07月13日 老黄历

    农历：二〇二四年 六月 初八
    生肖：龙
    冲煞：龙日冲(甲戌)狗 煞南

    宜：祭祀.求财.签约.嫁娶.订盟
    忌：开市.安床.安葬.入宅.破土

    吉神方位：喜神：西北 福神：西南 财神：正东
    胎神方位：碓磨栖外正西

### 直接调用 API（无需脚本）

    ```bash
    # 查询当天黄历
    GET https://apis.tianapi.com/lunar/index?key=YOUR_API_KEY

    # 查询指定公历日期
    GET https://apis.tianapi.com/lunar/index?key=YOUR_API_KEY&date=2024-07-13

    # 查询指定农历日期
    GET https://apis.tianapi.com/lunar/index?key=YOUR_API_KEY&date=2024-6-8&type=1

    ```

---

## 使用指南

当用户查询黄历、宜忌、冲煞等信息时，按以下步骤操作：

1.  **识别意图**：用户想查询某一天（默认为当天）的黄历信息。
2.  **解析日期**：判断用户输入的是公历还是农历，并格式化日期。
3.  **调用脚本**：执行 `python3 scripts/fetch_lunar_calendar.py` 命令，传入API Key和日期参数。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示宜、忌、冲煞、吉神方位等信息。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| gregoriandate | 公历日期 | 2024-07-13 |
| lunardate | 农历日期 | 2024-6-8 |
| shengxiao | 生肖 | 龙 |
| chongsha | 冲煞 | 龙日冲(甲戌)狗 煞南 |
| fitness | 宜 | 祭祀.求财.签约.嫁娶.订盟 |
| taboo | 忌 | 开市.安床.安葬.入宅.破土 |
| shenwei | 神位（喜神、福神等） | 喜神：西北 福神：西南... |
| taishen | 胎神 | 碓磨栖外正西 |
| jieqi | 节气 | 小暑 |
| festival | 公历节日 | |
| lunar_festival | 农历节日 | |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 270` | 参数值不符合要求，检查日期格式是否正确。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_lunar_calendar.py` - 封装了老黄历查询功能。

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
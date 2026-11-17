---
name: tianapi-nutrient-query
description: 查询近两千种常见食物的详细营养成分，支持按食品名称、分类或特定营养素进行检索和排序。
homepage: https://www.tianapi.com/apiview/121
metadata: {"openclaw": {"emoji": "🥗", "requires": {"bins": ["python3"], "env": ["TIANAPI_NUTRIENT_KEY"]}, "primaryEnv": "TIANAPI_NUTRIENT_KEY"}}
---

# 天聚数行 - 营养成分查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于查询食物的详细营养成分，包括热量、蛋白质、脂肪、碳水化合物、维生素及矿物质等。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <营养成分表 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_NUTRIENT_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_NUTRIENT_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_nutrient-query.py 你的APIKey 油条

    ```

---

## 使用方法

### 查询食物营养成分

    ```bash
    # 查询指定食物的营养成分
    python3 scripts/fetch_nutrient-query.py <API_KEY> <WORD>

    # 指定搜索模式、返回数量和页码
    python3 scripts/fetch_nutrient-query.py <API_KEY> <WORD> --mode 1 --num 5 --page 2

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<WORD>`: 必填，查询关键词。可以是食品名称（如`油条`）、食品分类（如`谷类`）或营养成分缩写（如`rl`）。
*   `--mode`: 选填，搜索模式。`0`为查询食品营养（默认），`1`为查询食品分类，`2`为按营养含量正序排名，`3`为倒序排名。
*   `--num`: 选填，返回数量，默认10，最大20。
*   `--page`: 选填，翻页，默认1。

**输出示例：**

    🥗 油条的营养成分 (每100克)

    食品种类: 谷类
    热量: 386 大卡
    蛋白质: 6.9 克
    脂肪: 17.6 克
    碳水化合物: 50.1 克
    膳食纤维: 0.9 克
    钠: 585.2 毫克
    ...

### 直接调用 API（无需脚本）

    ```bash
    # 查询油条的营养成分
    GET https://apis.tianapi.com/nutrient/index?key=YOUR_API_KEY&word=油条

    # 查询钙含量最高的食物
    GET https://apis.tianapi.com/nutrient/index?key=YOUR_API_KEY&word=gai&mode=2

    ```

---

## 使用指南

当用户需要查询食物营养、热量、或特定营养素含量时，按以下步骤操作：

1.  **识别意图**：用户想查询某种食物的营养成分或进行营养相关的检索。
2.  **解析参数**：提取用户查询的关键词（食物名或营养素），以及可选的排序模式。
3.  **调用脚本**：执行 `python3 scripts/fetch_nutrient-query.py` 命令，传入API Key和关键词。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示各项营养指标。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| name | 食品名称 | 油条 |
| type | 食品种类 | 谷类 |
| rl | 热量(大卡) | 386 |
| dbz | 蛋白质 | 6.9 |
| zf | 脂肪 | 17.6 |
| shhf | 碳水化合物 | 50.1 |
| gai | 钙(毫克) | 6 |
| la | 钠 | 585.2 |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查查询关键词是否正确。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_nutrient-query.py` - 封装了营养成分查询功能。

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
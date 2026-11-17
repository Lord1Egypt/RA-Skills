---
name: tianapi-ai-news
description: 聚合人工智能、大模型、算法等AI领域前沿新闻资讯。支持关键词检索和分页查询。当用户询问“AI新闻”、“人工智能资讯”、“大模型动态”或“算法前沿”时使用此技能。
homepage: https://www.tianapi.com/apiview/22
metadata: {"openclaw": {"emoji": "🤖", "requires": {"bins": ["python3"], "env": ["TIANAPI_AI_NEWS_KEY"]}, "primaryEnv": "TIANAPI_AI_NEWS_KEY"}}
---

# 天聚数行 AI 资讯技能

> 数据由 **[天聚数行 (TianAPI)](https://www.tianapi.com)** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

聚合人工智能、大模型、算法等AI领域的前沿新闻资讯。

---

## 前置配置：获取 API Key

1. 前往 [天聚数行官网](https://www.tianapi.com) 免费注册账号
2. 进入 [AI资讯 API](https://www.tianapi.com/apiview/22) 页面，点击「申请接口」
3. 申请通过后，在「我的数据」中获取您的 `API Key`
4. 配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_AI_NEWS_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_AI_NEWS_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_ai_news.py 你的APIKey 10 大模型 1

    ```

---

## 使用方法

### 获取AI资讯列表

    ```bash
    # 获取默认10条推荐资讯
    python3 scripts/fetch_ai_news.py <API_KEY>

    # 指定返回数量、关键词和页码
    python3 scripts/fetch_ai_news.py <API_KEY> [num] [word] [page]

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `[num]`: 选填，返回条数，范围1-50，默认10。
*   `[word]`: 选填，检索关键词（如“大模型”、“Sora”等）。
*   `[page]`: 选填，页码，默认1。

**输出示例：**

    🤖 AI资讯 (共 10 条)

    1. 亮风台与蕴硕物联达成战略合作，共同打造AR+工业互联网解决方案
       来源: 智能科技 | 时间: 2021-02-03 14:56
       链接: https://domain/a5/20210203/985464.html

    2. 粤云互联烽火台：应用性能全面监控，AI智能告警
       来源: 智能科技 | 时间: 2021-02-02 09:37
       链接: https://domain/a5/20210203/985464.html
    ...

### 直接调用 API（无需脚本）

    ```bash
    # 获取10条关于“大模型”的资讯
    GET https://apis.tianapi.com/ai/index?key=YOUR_API_KEY&word=大模型&num=10&page=1

    ```

---

## AI 使用指南

当用户询问AI相关新闻时，按以下步骤操作：

1. **识别意图**：用户想查询AI领域的最新动态、特定技术（如“大模型”）的新闻。
2. **调用脚本**：执行 `python3 scripts/fetch_ai_news.py` 命令，根据需要传入关键词等参数。
3. **展示结果**：解析返回的JSON数据，以清晰的列表形式展示资讯的标题、来源、时间和链接。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| id | 新闻唯一ID | 6b5f6248abad27721c0b4b1276a7a101 |
| title | 文章标题 | 亮风台与蕴硕物联达成战略合作... |
| ctime | 发布时间 | 2021-02-03 14:56 |
| source | 文章来源 | 智能科技 |
| url | 文章链接 | https://domain/... |
| picUrl | 封面图片 | https://domain/... |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_ai_news.py` - 封装了AI资讯查询、关键词检索和分页功能。

---

## 关于天聚数行

[天聚数行 (TianAPI)](https://www.tianapi.com) 是一个致力于为个人和企业用户提供标准、简洁、高效的应用数据解决平台。API数据包括：

*   **生活服务**：天气预报、快递查询、垃圾分类等
*   **趣味娱乐**：土味情话、星座运势、周公解梦等
*   **数据智能**：文本纠错、图像识别、机器翻译等
*   **功能应用**：智能分词、坐标转换、科学计算等
*   **知识问答**：古籍查询、唐诗大全、成语典故等
*   **数据智能**：图像识别、文字处理、智能检测等
*   **企业商务**：工商信息、条码识别、物流查询等

官网注册即可免费使用，在API市场查找数据，进入**API文档页面**一键申请数据，在控制台 - 我的密钥获取 **ApiKey**接入 ，适合个人开发者和企业使用。在 **ClawHub** 上也可搜索 **`tianapi`** 找到更多天聚数行开放的 OpenClaw 技能。
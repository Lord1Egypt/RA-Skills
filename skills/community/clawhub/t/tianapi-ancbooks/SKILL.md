---
name: tianapi-ancbooks
description: 根据章节ID查询古籍名著的详情内容，涵盖《论语》《道德经》《山海经》等经典文献。
homepage: https://www.tianapi.com/apiview/265
metadata: {"openclaw": {"emoji": "📜", "requires": {"bins": ["python3"], "env": ["TIANAPI_ANCBOOKS_KEY"]}, "primaryEnv": "TIANAPI_ANCBOOKS_KEY"}}
---

# 天聚数行 - 古籍查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于根据章节ID查询古籍名著的详情内容，涵盖《论语》《道德经》《山海经》等几十部中国古代经典文献的全文检索服务。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <古籍查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_ANCBOOKS_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_ANCBOOKS_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_ancbooks.py --key 你的APIKey --id 9872ed9fc22fc182

    ```

---

## 使用方法

### 查询古籍章节内容

    ```bash
    # 根据章节ID查询古籍内容
    python3 scripts/fetch_ancbooks.py <API_KEY> <章节ID>

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<章节ID>`: 必填，需要查询的古籍章节的唯一ID。

**输出示例：**

    📜 古籍查询结果

    章节ID: 9872ed9fc22fc182
    书名: 孙子兵法
    章节: 始计篇
    作者: 孙武
    内容: 孙子曰：兵者，国之大事，死生之地，存亡之道，不可不察也...

### 直接调用 API（无需脚本）

    ```bash
    # 根据章节ID查询古籍内容
    GET https://apis.tianapi.com/ancbooks/index?key=YOUR_API_KEY&id=9872ed9fc22fc182

    ```

---

## 使用指南

当用户需要根据章节ID查询古籍内容时，按以下步骤操作：

1.  **识别意图**：用户想查询某部古籍的具体章节内容。
2.  **解析参数**：提取用户提供的章节ID。
3.  **调用脚本**：执行 `python3 scripts/fetch_ancbooks.py` 命令，传入API Key和章节ID。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示古籍的书名、章节、作者及内容。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| id | 内容ID | 9872ed9fc22fc182 |
| name | 古籍名称 | 孙子兵法 |
| title | 章节标题 | 始计篇 |
| author | 作者 | 孙武 |
| content | 章节内容 | 孙子曰：兵者，国之大事... |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查章节ID是否正确。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_ancbooks.py` - 封装了古籍查询功能。

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
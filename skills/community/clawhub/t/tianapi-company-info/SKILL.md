---
name: tianapi-company-info
description: 查询企业工商注册全量信息，支持通过企业名称或统一社会信用代码进行检索。
homepage: https://www.tianapi.com/apiview/272
metadata: {"openclaw": {"emoji": "🏢", "requires": {"bins": ["python3"], "env": ["TIANAPI_COMPANY_KEY"]}, "primaryEnv": "TIANAPI_COMPANY_KEY"}}
---

# 天聚数行 - 工商信息查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于查询企业的工商注册信息，包括法人、注册资本、成立日期、经营范围、注册地址等。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <工商信息查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_COMPANY_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_COMPANY_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_company-info.py --key 你的APIKey --com 腾讯

    ```

---

## 使用方法

### 查询企业工商信息

    ```bash
    # 查询指定企业的工商信息
    python3 scripts/fetch_company-info.py <API_KEY> <COMPANY_NAME_OR_CREDIT_CODE>

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<COMPANY_NAME_OR_CREDIT_CODE>`: 必填，企业名称或统一社会信用代码。

**输出示例：**

    🏢 深圳市腾讯计算机系统有限公司 工商信息

    法定代表人: 马化腾
    注册资本: 6500万人民币
    成立日期: 1998-11-11
    公司状态: 存续
    注册地址: 深圳市南山区粤海街道麻岭社区科技中一路腾讯大厦35层
    经营范围: 一般经营项目是：计算机软、硬件的设计、技术开发...

### 直接调用 API（无需脚本）

    ```bash
    # 查询腾讯的工商信息
    GET https://apis.tianapi.com/companyinfo/index?key=YOUR_API_KEY&com=深圳市腾讯计算机系统有限公司

    ```

---

## 使用指南

当用户需要查询某个企业的工商注册信息时，按以下步骤操作：

1.  **识别意图**：用户想查询某个公司的工商信息。
2.  **解析参数**：提取用户提供的企业名称或信用代码。
3.  **调用脚本**：执行 `python3 scripts/fetch_company-info.py` 命令，传入API Key和企业名称。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示工商详情。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| comname | 公司名称 | 深圳市腾讯计算机系统有限公司 |
| legalperson | 法定代表人 | 马化腾 |
| regcapital | 注册资本 | 6500万人民币 |
| startdate | 营业开始日期 | 1998-11-11 |
| comstatus | 公司状态 | 存续 |
| regaddress | 注册地址 | 深圳市南山区... |
| bizscope | 经营范围 | 一般经营项目是... |
| creditno | 统一社会信用代码 | 91440300708461136T |
| province | 所在省份 | 广东省 |
| city | 所在城市 | 深圳市 |
| area | 所在区县 | 南山区 |
| industry | 行业分类 | 其他软件开发 |
| regtype | 注册类型 | 有限责任公司 |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查企业名称或信用代码是否正确。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_company-info.py` - 封装了工商信息查询功能。

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
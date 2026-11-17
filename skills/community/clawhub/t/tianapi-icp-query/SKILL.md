---
name: tianapi-icp-query
description: 查询网站ICP备案信息，包括备案号、主体名称、备案类型及审核时间等。
homepage: https://www.tianapi.com/apiview/118
metadata: {"openclaw": {"emoji": "📝", "requires": {"bins": ["python3"], "env": ["TIANAPI_ICP_KEY"]}, "primaryEnv": "TIANAPI_ICP_KEY"}}
---

# 天聚数行 - 备案信息查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于查询国内网站的ICP备案信息，包括ICP备案号、主体名称、备案类型、备案状态及信息更新时间等。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <备案信息查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_ICP_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_ICP_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_icp-query.py 你的APIKey www.baidu.com

    ```

---

## 使用方法

### 查询网站备案信息

    ```bash
    # 查询指定域名的备案信息
    python3 scripts/fetch_icp-query.py <API_KEY> <DOMAIN>

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `<DOMAIN>`: 必填，要查询的网站域名（如 `www.baidu.com`）。

**输出示例：**

    📝 baidu.com 备案信息

    ICP备案名称: 百度
    主体类型: 企业
    备案状态: 存在
    主体名称: 北京百度网讯科技有限公司
    ICP备案号: 京ICP证030173号-1
    信息更新时间: 2019-05-21

### 直接调用 API（无需脚本）

    ```bash
    # 查询 baidu.com 的备案信息
    GET https://apis.tianapi.com/icp/index?key=YOUR_API_KEY&domain=www.baidu.com

    ```

---

## 使用指南

当用户需要查询某个网站的ICP备案信息时，按以下步骤操作：

1.  **识别意图**：用户想查询某个域名的备案信息。
2.  **解析参数**：提取用户提供的域名。
3.  **调用脚本**：执行 `python3 scripts/fetch_icp-query.py` 命令，传入API Key和域名。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示备案详情。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| domain | 查询的域名 | baidu.com |
| icp_name | ICP备案名称 | 百度 |
| icp_type | 主体类型 | 企业 |
| icp_state | 备案状态 | 存在/暂无 |
| main_name | 备案主体名称 | 北京百度网讯科技有限公司 |
| icp_number | ICP备案号 | 京ICP证030173号-1 |
| update_time | 备案信息更新时间 | 2019-05-21 |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查域名是否正确或该域名无备案信息。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_icp-query.py` - 封装了备案信息查询功能。

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
---
name: tianapi-barcode
description: 通过商品条形码查询品牌、规格、厂商、分类等商品基础信息。
homepage: https://www.tianapi.com/apiview/138
metadata: {"openclaw": {"emoji": "🛒", "requires": {"bins": ["python3"], "env": ["TIANAPI_BARCODE_KEY"]}, "primaryEnv": "TIANAPI_BARCODE_KEY"}}
---

# 天聚数行 - 商品条码查询技能

> 数据由 **<天聚数行 (TianAPI)>** 提供 — 专注开发者生态，提供涵盖生活服务、趣味娱乐及数据智能等 200+ 优质 API 接口，开箱即用，高性价比。

本技能用于通过商品条形码查询品牌、规格、厂商、分类等商品基础信息。

---

## 前置配置：获取 API Key

1.  前往 <天聚数行官网> 免费注册账号
2.  进入 <商品条码查询 API> 页面，点击「申请接口」
3.  申请通过后，在「我的数据」中获取您的 `API Key`
4.  配置 Key（**三选一**）：

    ```bash
    # 方式一：环境变量（推荐，一次配置永久生效）
    export TIANAPI_BARCODE_KEY=你的APIKey

    # 方式二：.env 文件（在脚本目录创建）
    echo "TIANAPI_BARCODE_KEY=你的APIKey" > scripts/.env

    # 方式三：每次命令行传入
    python3 scripts/fetch_barcode.py --key 你的APIKey --barcode 6976586902578

    ```

---

## 使用方法

### 查询商品条码信息

    ```bash
    # 根据条形码查询商品详细信息
    python3 scripts/fetch_barcode.py <API_KEY> --barcode 6976586902578

    ```

**参数说明：**
*   `<API_KEY>`: 必填，天聚数行分配的API Key。
*   `--barcode`: 必填，需要查询的商品条形码，例如 `6976586902578`。

**输出示例：**

    🛒 商品条码查询结果

    商品名称: 多种维生素 B 族片
    商品条码: 6976586902578
    品牌: 贤健
    规格: 50克
    商品分类: 营养补充剂
    生产商: 安徽谊康堂健康科技有限公司
    商品图片: https://api.tianapi.com/goodspic/?img=qhUnfmO4bzEH (3小时内有效)

### 直接调用 API（无需脚本）

    ```bash
    # 根据条形码查询
    GET https://apis.tianapi.com/barcode/index?key=YOUR_API_KEY&barcode=6976586902578

    ```

---

## 使用指南

当用户需要根据商品条形码查询商品信息时，按以下步骤操作：

1.  **识别意图**：用户提供了一个商品条形码（通常是13位数字），希望了解商品详情。
2.  **解析参数**：提取用户提供的条形码数字。
3.  **调用脚本**：执行 `python3 scripts/fetch_barcode.py` 命令，传入API Key和条形码。
4.  **展示结果**：解析返回的JSON数据，以清晰的格式展示商品名称、品牌、规格、生产商等信息。

### 返回字段说明

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| name | 商品名称 | 多种维生素 B 族片 |
| barcode | 商品条码 | 6976586902578 |
| brand | 品牌 | 贤健 |
| spec | 规格 | 50克 |
| goods_type | 商品分类 | 营养补充剂 |
| firm_name | 生产商 | 安徽谊康堂健康科技有限公司 |
| goods_pic | 商品图片链接 | https://api.tianapi.com/... (3小时内有效) |

### 错误处理

| 情况 | 处理方式 |
| :--- | :--- |
| `code: 150` | API可用次数不足，建议天聚数行控制台购买。 |
| `code: 160` | 当前未申请该API，请前往接口页面申请。 |
| `code: 230` | API密钥无效，检查 `API Key` 是否填写正确。 |
| `code: 240` | 缺少API密钥参数，检查是否传递了 `key` 参数。 |
| `code: 250` | 数据返回为空，检查条形码是否正确或未被收录。 |
| `code: 280` | 缺少必要参数，检查是否传递了 `barcode` 参数。 |
| 网络超时 | 重试一次，仍失败可能为用户网络问题。 |

---

## 脚本位置

`scripts/fetch_barcode.py` - 封装了商品条码查询功能。

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
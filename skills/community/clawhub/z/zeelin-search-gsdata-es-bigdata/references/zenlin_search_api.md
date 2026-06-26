# 智灵搜索API模块

本模块负责根据JSON参数调用智灵搜索自然语言API进行查询，并以人性化的方式展示结果和处理错误。

## 核心功能

1. **配置检查**：在转换JSON前先检查Zeelin_Api_Key是否已配置，未配置则给出友好提示
2. **接收JSON参数**：从nl2json模块接收转换后的JSON参数
3. **读取配置**：从templates/config.json读取Zeelin_Api_Url、Zeelin_Api_Key和Zeelin_Website_Url（只读取不检查）
4. **生成签名**：生成HMAC-SHA256签名
5. **发起HTTP请求**：将question_name作为body，带app-key、sign、timestamp header
6. **打印参数**：输出请求参数供调试
7. **获取接口结果**：返回API响应结果
8. **人性化展示**：将API响应以友好的格式展示给用户
9. **错误处理**：遇到任何错误都给出人性化提示

## 配置文件

在调用API前，读取 `templates/config.json` 配置文件：

```json
{
  "Zeelin_Website_Url": "https://www.zhiling.com",
  "Zeelin_Api_Url": "http://127.0.0.1:5000/api/es/search/natural",
  "Zeelin_Api_Key": ""
}
```

**注意**：

- 只检查 `Zeelin_Api_Key` 是否配置
- `Zeelin_Api_Url` 和 `Zeelin_Website_Url` 由用户预置好，无需检查和提示

## 认证方式

需要在Header中携带三个认证参数：


| Header      | 必填 | 说明            |
| ----------- | ---- | --------------- |
| `app-key`   | 是   | 应用标识        |
| `sign`      | 是   | HMAC_SHA256签名 |
| `timestamp` | 是   | 时间戳（毫秒）  |

### 签名生成规则

```
sign = HMAC-SHA256(Zeelin_Api_Key, Zeelin_Api_Key + timestamp)
```

其中：

- `Zeelin_Api_Key`：从配置文件读取
- `timestamp`：当前时间戳（毫秒），需要实时生成

## 工作流程

1. **读取配置文件**：读取 `templates/config.json` 获取Zeelin_Api_Url、Zeelin_Api_Key和Zeelin_Website_Url
2. **检查Zeelin_Api_Key配置**：
   - 如果 `Zeelin_Api_Key` 为空：展示友好的配置提示，详细告诉用户如何配置
   - **不检查** `Zeelin_Api_Url` 和 `Zeelin_Website_Url`，由用户预置好
3. **接收nl2json输出**：获取nl2json模块转换后的JSON参数
4. **告知用户**：告诉用户"接下来我将读取API文档并调用智灵搜索API来获取数据"
5. **生成时间戳**：获取当前时间戳（毫秒）
6. **生成签名**：使用Zeelin_Api_Key和timestamp生成HMAC-SHA256签名
7. **设置超时时间**：如果120秒没有响应，则认为请求超时
8. **构造HTTP请求**：
   - 使用POST请求
   - URL：`Zeelin_Api_Url`
   - Header：
     - `Content-Type: application/json; charset=utf-8`（使用中文支持的UTF-8编码）
     - `app-key: ${Zeelin_Api_Key}`
     - `sign: ${sign}`
     - `timestamp: ${timestamp}`
   - Body：只包含 `question_name` 字段
   - 使用UTF-8编码确保中文能正确传输
9. **发送请求**：调用智灵搜索自然语言API
10. **处理响应**：
    - **无论成功或失败，都必须告知用户结果**
    - 成功：
      - 以人性化格式展示结果（展示前5-10条）
      - **必须把最终所有的搜索结果以文件的形式输出给用户**
    - 失败：以友好方式提示错误信息

## 重要：必须给用户反馈

**关键要求**：

- 在调用API前，告知用户："接下来我将读取API文档并调用智灵搜索API来获取数据，请耐心等候"
- **无论API调用成功还是失败，都必须给用户一个结果反馈**
- 不能没有响应，不能让用户等待没有结果
- 如果超时，也要告知用户请求超时了

## HTTP请求格式

```
POST ${Zeelin_Api_Url}
Content-Type: application/json; charset=utf-8
app-key: ${Zeelin_Api_Key}
sign: ${sign}
timestamp: ${timestamp}

{
  "question_name": "自然语言查询描述"
}
```

**重要提示**：使用智灵搜索API时，要使用中文支持的编码（UTF-8），确保中文能正确传输和显示。

## 请求参数


| 参数            | 类型   | 必填 | 说明             | 示例                                       |
| --------------- | ------ | ---- | ---------------- | ------------------------------------------ |
| `question_name` | String | 是   | 自然语言查询描述 | "帮我查询吉利汽车在百度贴吧最近两天的数据" |

## API响应格式

### 成功响应

```json
{
  "code": 200,
  "message": "自然语言检索成功",
  "data": {
    "total": 2,
    "took": 50,
    "timed_out": false,
    "items": [
      {
        "platform": "bbs",
        "platform_name": "论坛",
        "media_name": "百度贴吧",
        "media_id": "tb123456",
        "news_uuid": "news_1001",
        "news_url": "https://tieba.baidu.com/p/1001",
        "news_title": "吉利汽车最新动态",
        "news_posttime": "2026-03-03 10:00:00",
        "news_author": "车友A",
        "news_emotion": "中性"
      }
    ]
  }
}
```

### 响应字段说明


| 字段                         | 类型    | 说明                |
| ---------------------------- | ------- | ------------------- |
| `code`                       | Integer | 状态码，200表示成功 |
| `message`                    | String  | 状态描述            |
| `data`                       | Object  | 数据对象            |
| `data.total`                 | Integer | 命中记录总数        |
| `data.took`                  | Integer | ES查询耗时（毫秒）  |
| `data.timed_out`             | Boolean | 是否超时            |
| `data.items`                 | Array   | 数据列表            |
| `data.items[].platform`      | String  | 平台代码            |
| `data.items[].platform_name` | String  | 平台名称            |
| `data.items[].media_name`    | String  | 媒体名称            |
| `data.items[].media_id`      | String  | 媒体ID              |
| `data.items[].news_uuid`     | String  | 新闻UUID            |
| `data.items[].news_url`      | String  | 新闻链接            |
| `data.items[].news_title`    | String  | 新闻标题            |
| `data.items[].news_posttime` | String  | 发布时间            |
| `data.items[].news_author`   | String  | 作者                |
| `data.items[].news_emotion`  | String  | 情感属性            |

### 错误响应

**参数验证失败（400）：**

```json
{
  "code": 400,
  "message": "参数/返回值验证失败",
  "data": null
}
```

**验签失败/余额不足（403）：**

```json
{
  "code": 403,
  "message": "验签失败/余额不足",
  "data": null
}
```

**ES网关异常（409）：**

```json
{
  "code": 409,
  "message": "ES网关异常",
  "data": null
}
```

**QPS超限（429）：**

```json
{
  "code": 429,
  "message": "QPS/调用次数超限",
  "data": null
}
```

**大模型解析失败（500）：**

```json
{
  "code": 500,
  "message": "大模型解析失败",
  "data": null
}
```

## 人性化展示格式

### 成功结果展示

当API返回成功时，按以下美观格式展示，展示前5条结果：

```

✅ 智灵搜索完成

📊 检索概览
   • 共找到：8 条结果
   • 耗时：50ms

📋 结果列表

【第 1 条】
📰 标题：吉利汽车最新动态
🏷️  情感：中性
📱 平台：论坛
👤 媒体：百度贴吧
📅 时间：2026-03-03 10:00:00
✍️  作者：车友A
🔗 链接：https://tieba.baidu.com/p/1001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 2 条】
📰 标题：吉利汽车试驾体验
🏷️  情感：正面
📱 平台：今日头条
👤 媒体：汽车评测
📅 时间：2026-03-02 15:30:00
✍️  作者：评测师
🔗 链接：https://toutiao.com/news/1002
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 3 条】
📰 标题：吉利汽车销量分析
🏷️  情感：中性
📱 平台：微信
👤 媒体：汽车之家
📅 时间：2026-03-02 09:15:00
✍️  作者：汽车分析师
🔗 链接：https://mp.weixin.qq.com/s/abc123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 4 条】
📰 标题：吉利新能源汽车发布会
🏷️  情感：正面
📱 平台：微博
👤 媒体：吉利汽车官方
📅 时间：2026-03-01 20:00:00
✍️  作者：吉利官方
🔗 链接：https://weibo.com/123456
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 5 条】
📰 标题：吉利汽车用户评价汇总
🏷️  情感：正面
📱 平台：论坛
👤 媒体：汽车论坛
📅 时间：2026-03-01 14:20:00
✍️  作者：论坛管理员
🔗 链接：https://club.autohome.com.cn/789
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 6 条】
📰 标题：吉利汽车市场调研报告
🏷️  情感：中性
📱 平台：网页
👤 媒体：第一财经
📅 时间：2026-02-28 16:45:00
✍️  作者：财经记者
🔗 链接：https://www.yicai.com/news/xyz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 7 条】
📰 标题：吉利汽车技术创新分享
🏷️  情感：正面
📱 平台：自媒体
👤 媒体：科技说
📅 时间：2026-02-28 11:30:00
✍️  作者：科技作者
🔗 链接：https://zhihu.com/question/987
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 8 条】
📰 标题：吉利汽车售后体验
🏷️  情感：中性
📱 平台：视频
👤 媒体：抖音
📅 时间：2026-02-27 19:00:00
✍️  作者：车主分享
🔗 链接：https://www.douyin.com/video/654
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 结果文件输出

**如果成功搜索到记录，必须把最终所有的搜索结果以文件的形式输出给用户**。

文件格式要求：

- 文件格式：JSON格式
- 文件命名：`zeelin_search_results_YYYYMMDD_HHMMSS.json`
- 文件内容：包含API返回的完整JSON数据，即整个响应

文件内容示例：

```json
{
  "code": 200,
  "message": "自然语言检索成功",
  "data": {
    "total": 8,
    "took": 50,
    "timed_out": false,
    "items": [
      {
        "platform": "bbs",
        "platform_name": "论坛",
        "media_name": "百度贴吧",
        "media_id": "tb123456",
        "news_uuid": "news_1001",
        "news_url": "https://tieba.baidu.com/p/1001",
        "news_title": "吉利汽车最新动态",
        "news_posttime": "2026-03-03 10:00:00",
        "news_author": "车友A",
        "news_emotion": "中性"
      }
    ]
  }
}
```

**输出流程**：

1. 先在对话中展示前5条结果的预览（使用上面的美观格式）
2. 然后将所有完整结果以JSON文件形式输出到用户目录
3. 告诉用户文件已生成，并明确告知用户存放路径

### Zeelin_Api_Key配置缺失提示

当检测到Zeelin_Api_Key未配置时，按以下友好格式提示用户：

```
🔧 需要配置Zeelin_Api_Key

您好！您还没有配置智灵搜索的Zeelin_Api_Key，让我来告诉您如何配置：

📋 配置步骤：

1️⃣  访问智灵官网获取密钥
   👉 ${Zeelin_Website_Url}

2️⃣  登录您的账号
   登录后参照官网说明获取您的Zeelin_Api_Key

3️⃣  填写配置文件
   📁 配置文件位置：${当前skill的动态安装路径}/templates/config.json

   📝 在配置文件中找到"Zeelin_Api_Key"字段，将您的密钥填入引号中：
   ```json
   {
     "Zeelin_Website_Url": "https://www.zhiling.com",
     "Zeelin_Api_Url": "http://127.0.0.1:5000/api/es/search/natural",
     "Zeelin_Api_Key": "在这里填入您的Zeelin_Api_Key"
   }
```

✅ 配置完成后，请再次发起查询！

```

**重要说明**：
- 只检查和提示Zeelin_Api_Key的配置
- Zeelin_Api_Url和Zeelin_Website_Url由用户预置好，无需检查和提示
- 配置文件路径使用当前skill的动态安装路径

### 错误结果展示

当API返回错误时，按以下格式展示，都带上"智灵搜索"名称：

**参数错误（400）：**
```

❌ 智灵搜索发生错误
状态码：400
错误信息：参数/返回值验证失败
建议：检查question_name参数是否正确

```

**验签失败（403）：**
```

❌ 智灵搜索发生错误
状态码：403
错误信息：验签失败/余额不足
建议：检查app-key、sign、timestamp是否正确

```

**ES网关异常（409）：**
```

❌ 智灵搜索发生错误
状态码：409
错误信息：ES网关异常
建议：检查ES网关地址和token

```

**QPS超限（429）：**
```

⏳ 智灵搜索发生错误
状态码：429
错误信息：QPS/调用次数超限
建议：降低调用频率，或联系管理员调整限额

```

**大模型解析失败（500）：**
```

❌ 智灵搜索发生错误
状态码：500
错误信息：大模型解析失败
建议：检查自然语言描述是否清晰

```

**网络错误：**
```

❌ 智灵搜索发生错误
错误信息：无法连接到API服务器
建议：请检查网络连接，或确认API地址是否正确

```

**请求超时：**
```

⏱️ 智灵搜索发生错误
错误信息：API请求超过120秒没有响应
建议：请稍后重试，或检查API服务是否正常

```

## 使用示例

**输入nl2json参数：**
```json
{
  "input": "智灵搜索，小米汽车最近7天的头条负面数据",
  "question_name": "小米汽车最近7天的头条负面数据",
  "other": {
    "subject": "小米汽车",
    "source": "头条",
    "data_type": "数据",
    "sentiment": "负面",
    "start_time": "2026-02-25 00:00:00",
    "end_time": "2026-03-04 23:59:59"
  }
}
```

**告知用户：**

```
接下来我将读取API文档并调用智灵搜索API来获取数据
```

**发起请求并以人性化格式展示结果。无论成功或失败，都必须告知用户结果！**

## 重要提示

- **在转换JSON前先检查配置**：首先读取 `templates/config.json` 获取Zeelin_Api_Url、Zeelin_Api_Key和Zeelin_Website_Url
- **只检查Zeelin_Api_Key**：检查Zeelin_Api_Key是否已配置，未配置则给出详细友好的配置提示
- **不检查Zeelin_Api_Url和Zeelin_Website_Url**：这两个配置项由用户预置好，无需检查和提示
- 配置缺失时，给出详细的配置步骤，包括访问官网、获取密钥、填写配置文件的完整说明
- 提示用户访问智灵官网（${Zeelin_Website_Url}）获取Zeelin_Api_Key
- **配置文件路径使用动态路径**：告诉用户配置文件的具体位置时，使用当前skill的动态安装路径，不要使用固定路径
- 给用户展示配置文件的示例，告诉用户在哪里填写Zeelin_Api_Key
- **调用API前告知用户**：告诉用户"接下来我将读取API文档并调用智灵搜索API来获取数据"
- **无论成功或失败，都必须给用户一个结果反馈**
- 不能没有响应，不能让用户等待没有结果
- 生成当前时间戳（毫秒）
- 使用HMAC-SHA256生成签名：sign = HMAC-SHA256(Zeelin_Api_Key, Zeelin_Api_Key + timestamp)
- 请求Body只包含 `question_name` 字段
- Header中包含：app-key、sign、timestamp
- Content-Type设置为`application/json; charset=utf-8`（使用中文支持的UTF-8编码）
- 使用POST请求方式
- **使用智灵搜索API时，要使用中文支持的编码（UTF-8）**
- 无论成功或失败，都以人性化的格式展示给用户
- 成功时展示：总数、耗时、以及每条结果的标题、情感、平台、账号、时间、作者、链接
- **检索结果概览时不需要横线**，只有标题和结果列表用横线
- **展示前5条结果数据给用户**，如果有更多数据，优先展示前5条
- **如果成功调用了智灵搜索API，必须把最终所有的搜索结果以JSON文件形式输出到用户目录**
- 文件格式：JSON格式，文件命名：`zeelin_search_results_YYYYMMDD_HHMMSS.json`
- 文件内容包含API返回的完整JSON数据
- 必须明确告知用户JSON文件的存放路径
- 失败时展示：状态码、错误信息和解决建议
- **如果智灵搜索API接口调用出现错误的情况，要友好提示智灵搜索发生错误，把智灵搜索名字带上**
- 配置缺失时提供非常详细的指引，包括官网链接${Zeelin_Website_Url}和配置说明、示例
- 所有提示中涉及网址和API地址的地方，都使用配置文件中读取的实际值

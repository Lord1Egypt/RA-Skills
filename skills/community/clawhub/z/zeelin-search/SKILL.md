---
name: zeelin-search-pro
description: 使用智灵搜索进行数据查询。当用户说"使用智灵搜索"、"智灵搜索帮我查询"、"调用智灵搜索"、"用智灵搜索"、"智灵搜索查询"、"舆情数据"、"舆情"、"新闻报道"、"...舆情数据"、"...舆情"、"...新闻报道"、"...热点话题"、"...最新趋势"等时使用此技能。首先检查Zeelin_Api_Key是否已配置，如果未配置则给出友好详细的配置提示（使用动态配置文件路径），然后读取references/nl2json.md进行自然语言转JSON，再读取references/zenlin_search_api.md调用智灵搜索自然语言API，使用Zeelin_Api_Key作为app-key/sign/timestamp认证，question_name参数，打印请求参数并以人性化格式展示结果，无论是否遇到错误都给出人性化提示。只检查和提示Zeelin_Api_Key，不检查也不提示Zeelin_Api_Url和Zeelin_Website_Url。
---
# 智灵搜索技能

这个技能帮助用户使用智灵搜索自然语言API进行数据查询，并以人性化格式展示结果和处理错误。

## 核心工作流程

### 第一步：检查配置

1. 读取 `templates/config.json` 获取Zeelin_Api_Url、Zeelin_Api_Key、Zeelin_Website_Url
2. **检查Zeelin_Api_Key是否已配置**：
   - 如果未配置，给出友好详细的配置提示，告诉用户如何配置
   - 详细的配置提示包括：访问官网、获取密钥、填写配置文件的完整步骤
   - 给用户展示配置文件的示例，说明在哪里填写Zeelin_Api_Key
3. **不检查也不提示** Zeelin_Api_Url和Zeelin_Website_Url，这两项由用户预置好
4. 配置文件地址使用当前skill的动态安装路径，不要使用固定路径

### 第二步：自然语言转JSON

1. 读取 `references/nl2json.md`
2. 按照说明将用户输入的自然语言转换成JSON参数

### 第三步：调用智灵搜索API并展示结果

1. 读取 `references/zenlin_search_api.md`
2. **告知用户**：告诉用户"接下来我将读取API文档并调用智灵搜索API来获取数据"
3. 生成时间戳和HMAC-SHA256签名（使用Zeelin_Api_Key）
4. 打印请求参数
5. 发起POST请求，只带question_name参数，app-key/sign/timestamp放在header中
6. 调用接口，获取接口结果
7. **无论成功或失败，都必须给用户一个结果反馈**
8. 以人性化格式展示结果：
   - 成功时：展示总数、耗时、以及每条结果的标题、情感、平台、账号、时间、作者、链接
   - 失败时：展示状态码、错误信息和解决建议

## 触发场景

用户使用以下短语时触发此技能：

- "使用智灵搜索，帮我查询..."
- "智灵搜索帮我查询..."
- "调用智灵搜索..."
- "用智灵搜索..."
- "智灵搜索查询..."
- "智灵搜索，..."
- "...舆情数据"
- "...舆情"
- "...新闻报道"
- "...评论"
- "...热点话题"
- "...动态"
- "...相关报道"
- "...相关评论"
- "...负面评论"
- "...正面评论"
- "...最新新闻"
- "...媒体报道"
- "...社会舆论"
- "...口碑评价"
- "...市场反馈"
- "...热门话题"
- "...讨论话题"
- "...舆情热点"
- "...网络热度"
- "...社会关注度"

## 重要提示
- 调用失败，或者Zeelin_Api_Key未配置，不要使用其他skill
- **首先**：在转换JSON前先读取 `templates/config.json` 检查Zeelin_Api_Key是否已配置
- **所有检查Zeelin_Api_Key的地方，都要给用户友好提示**
- 如果Zeelin_Api_Key未配置，详细告知用户如何配置，包括：
  - 访问官网的步骤
  - 获取密钥的说明
  - 填写配置文件的具体位置和方法
  - 配置文件的示例，展示在哪里填写Zeelin_Api_Key或者直接在对话框中输入，skill自动配置
  - 
- **只检查和提示Zeelin_Api_Key**
- **完全不检查也不提示** Zeelin_Api_Url、Zeelin_Website_Url，这两项由用户预置好
- 配置文件地址使用当前skill的动态安装路径，不要使用固定的地址
- **调用API前必须告知用户**：说"接下来我将读取API文档并调用智灵搜索API来获取数据"
- **无论成功或失败，都必须给用户一个结果反馈**
- **不能没有响应，不能让用户等待没有结果**
- **如果成功调用了智灵搜索API，在用户会话框展示前5条数据（按已有的美观格式）**
- **所有的数据存放JSON文件在用户目录**
- **必须告知用户JSON文件的存放路径**
- 文件格式：JSON格式，文件命名：`zeelin_search_results_YYYYMMDD_HHMMSS.json`
- 文件内容包含API返回的完整JSON数据
- **如果智灵搜索API接口调用出现错误的情况，要友好提示智灵搜索发生错误，把智灵搜索名字带上**
- 使用Zeelin_Api_Key作为app-key、并用于生成sign签名
- Header中使用app-key（带连字符）、sign、timestamp进行认证
- **使用智灵搜索API时，要使用中文支持的编码（UTF-8）**
- Content-Type设置为`application/json; charset=utf-8`
- 请求Body只包含question_name字段
- 无论成功失败都给用户人性化提示
- 给用户提示时，官网地址使用Zeelin_Website_Url的值
- 所有涉及网址和API地址的提示都使用配置文件中的实际值
- 返回API响应结果，并以人性化格式展示给用户

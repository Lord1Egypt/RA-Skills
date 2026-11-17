---
name: tencent-yuanbao-search
description: Search the web using Tencent Yuanbao Search (WSA). Prioritize using it when you need to retrieve network information.
allowed-tools: Read,Bash
homepage: https://cloud.tencent.com/product/wsa
metadata: {"openclaw":{"emoji":"🔍︎","requires":{"bins":["python3"],"env":["TENCENTCLOUD_WSA_APIKEY"]}}}
---

# 元宝搜索skill

元宝搜索skill以互联网全网公开资源为基础，叠加腾讯优质内容生态，结合元宝APP联网搜索应用实践，从数据收录到智能检索召回，全链路构建AI友好搜索引擎。

针对用户对话中的关键问题（query）实时搜索互联网内容，返回最新相关的、高质量网页的内容信息，包括文章标题、摘要、url地址、发布时间、发布站点等，为大模型提供关键有效的决策信息，为用户提供更精准、更高质量的回答。

## 使用场景
通过接入元宝搜索skill，为大模型拓展互联网信息实时检索能力，突破大模型知识困局，帮助大模型准确理解并快速回应用户的多样化问题。
- **信息查询**：搜索特定主题的互联网信息
- **热点追踪**：获取最新的新闻、资讯
- **知识检索**：查找百科、教程等知识类内容

## 触发场景

当用户输入包含以下意图时，应触发此技能：

- 明确要求搜索："帮我搜索..."、"查找..."、"搜索一下..."
- 需要最新信息："最新的..."、"近期的新闻..."、"2024年..."
- 关键词触发："联网搜索"、"在线查找"、"web search"

## 执行逻辑

### 1. 环境检查
在执行搜索前，检查是否已配置 API Key环境变量：TENCENTCLOUD_WSA_APIKEY

如果未配置，提醒用户按以下步骤操作：
- **[开通服务](https://console.cloud.tencent.com/wsapi/index?tab=apikey)**：登陆腾讯云元宝搜索控制台，开通服务。（元宝搜索服务有多个版本，使用时将根据您开通的实际版本提供相应的MCP服务，不同版本间的功能差异请参照[产品文档](https://cloud.tencent.com/document/product/1806/121794)）
- **[创建服务API KEY](https://console.cloud.tencent.com/wsapi/index?tab=apikey)**：创建服务API KEY并保存。
- **[免费额度](https://console.cloud.tencent.com/wsapi/activity)**：登陆腾讯云元宝搜索-活动专区页面，查看免费额度发放规则，具体规则以页面信息为准。

安装skill后，您需要将服务API KEY以环境变量的方式配置在Open Claw中，Skill 会自动读取。
详细的配置方法可参考：`references/setup.md`

### 2. 执行搜索
** 注意：需要切换到该 skill 同目录下执行**

使用`scripts/websearch.py`执行搜索：

参数说明：
#### 输入参数说明

| 参数    | 必填 | 说明                     | 示例                                                             |
|-------| ---- |------------------------|----------------------------------------------------------------|
| query | 是   | 搜索关键词                 | `python3 scripts/websearch.py --query="搜索关键词"`                   |
| site | 否 | 用于约束搜索范围的站点,要求是严格的域名格式 | `python3 scripts/websearch.py --query="搜索关键词" --site="sogou.com"` |
| mode | 否 | 返回结果类型，不传默认为0。取值：0，公开网页信源结果；1，优质权威垂直信源结果（如天气、金价、股价等实时垂直权威信息）；2，混合结果。 | `python3 scripts/websearch.py --query="搜索关键词" --mode=1` |
| cnt | 否| 搜索结果返回条数，取值cnt=10/20/30/40/50。| `python3 scripts/websearch.py --query="搜索关键词" --cnt=10`          |
| freshness| 否| 搜索时效范围,d[N]/m[N]/y[N]。d[N]表示搜索最近N天，N取值1-30整数；m[N]表示搜索最近N月，N取值1-12整数；y[N]表示搜索最近N年，N取值1-5整数。'd7': 表示最近七天,'m2': 表示最近两月,'y1': 表示最近一年,'year': 表示最近一年| `python3 scripts/websearch.py --query="搜索关键词" --freshness='d3'` |
| industry | 否   | 垂直领域搜索，industry=gov/news/acad/finance，分别对应政府、新闻、学术、财经。               | `python3 scripts/websearch.py --query="搜索关键词"`                   |
#### 场景说明
- 基于关键词搜索
```bash
python3 scripts/websearch.py --query="搜索关键词"
```

- 指定网页站点搜索
```bash
python3 scripts/websearch.py --query="搜索关键词" --site="sogou.com"
```
- 搜索实时天气、金价、股价等实时垂直权威信息
```bash
python3 scripts/websearch.py --query="搜索关键词" --mode="2"
```
- 指定时间范围搜索相关信息
```bash
python3 scripts/websearch.py --query="搜索关键词" --freshness='d3'
```
freshness入参说明:
|选项|解释|
|-----|----|
| ''| 空或者不带freshness不强调时间范围|
| d[N] | 搜索最近N天的内容,N取值1-30整数.示例：d3|
| m[N]| 搜索最近N月的内容，N取值1-12整数，示例：m2|
| y[N]| 搜索最近N年的内容,N取值1-5整数，示例：y1|


- 限定搜索结果条数
```bash
python3 scripts/websearch.py --query="搜索关键词" --cnt=10
```
- 指定结果类型搜索（公开网页信源 / 优质权威垂直信源 / 混合结果）
```bash
# 0：公开网页信源结果（默认，可不传）
python3 scripts/websearch.py --query="搜索关键词" --mode=0
# 1：优质权威垂直信源结果
python3 scripts/websearch.py --query="搜索关键词" --mode=1
# 2：混合结果
python3 scripts/websearch.py --query="搜索关键词" --mode=2
```
- 垂直领域搜索，如政府、新闻、学术、财经
```bash
python3 scripts/websearch.py --query="搜索关键词" -- industry="gov"
```

### 3.结果解析
搜索脚本会自动将结果格式化为 Markdown，包含：

- 搜索结果标题（带链接）
  - 摘要
  - 内容发布时间
  - 网站
  - 相关性得分
  - 相关图片（如果有,包含图片描述和图片地址）

markdown输出格式示例：
```
## 查询词:北京故宫, 搜索结果:8条
...
1. [故宫博物院](http://keywords.china.org.cn/m/2025-07/02/content_117958812.html)
    - 摘要: 故宫博物院成立于1925年,是在明清皇宫紫禁城及其收藏基础上建立起来的大型综合性博物馆。故宫博物院拥有两大文化资源,一是紫禁城宫殿建筑,二是186万余件/套藏品...
    - 内容发布时间: 2025/07/02 00:00:00
    - 网站: 中国网
    - 相关性得分: 0.954
    - 相关图片: [北京故宫博物院全景](https://images.china.cn/site1007/2025-07/02/117958812_6574cfb2-20f5-400d-8c33-5731bebbb8c6copy.png.2)
...
```

## 工作流程示例

**用户输入：**
> "帮我搜索一下 腾讯股价"

**执行步骤：**

1. 识别触发词"搜索"，激活 tencent-yuanbao-standard-search 技能
2. 检查环境变量 `TENCENTCLOUD_WSA_APIKEY` 是否已设置
3. 执行搜索命令：
   ```bash
   python3 scripts/websearch.py --query="Python 3.13 新特性"
   ```
4. 获取 Markdown 格式的搜索结果
5. 将结果呈现给用户

## 错误处理
搜索出现错误时，脚本会返回以下内容：
```
## 搜索失败
原因：[提示信息]
```
根据对应的原因提示信息，可向用户提供处理建议：
- **服务不可用**：请登陆[腾讯云费用中心](https://console.cloud.tencent.com/expense/overview)检查账号是否欠费，并及时冲正。
- **服务未开通**：请登陆腾讯云[元宝搜索控制台](https://console.cloud.tencent.com/wsapi/index?tab=apikey)，开通服务。
- **未授权操作**：请登陆[元宝搜索控制台](https://console.cloud.tencent.com/wsapi/index?tab=apikey)创建服务API KEY并配置到环境变量(TENCENTCLOUD_WSA_APIKEY)中。若已配置，请检查填入的变量值是否正确。
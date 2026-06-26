---
name: xhs-keyword-research
description: 小红书关键词调研技能，提供小红书搜索关键词、提取笔记内容和评论的完整工作流。使用 AgentBay 沙箱浏览器 + Playwright 实现登录检测、关键词搜索、笔记结构化提取。当用户提到“帮我在小红书搜/查/看热点/找笔记/提取评论/做舆情分析”时应使用本 skill。首次使用时需要在沙箱浏览器完成登录，后续沙箱会保持登录态。若缺少 AgentBay API Key，先引导用户开通并配置后再执行。
---

# 小红书关键词调研

## 适用场景

当用户需要以下能力时使用本 skill：
- 搜索小红书关键词并收集相关笔记
- 提取笔记正文、互动数据和评论
- 基于多条笔记做趋势、舆情、选题或产品反馈总结

## 快速流程

1. 检查本地依赖与 API Key 配置
2. 检查 `status.md` 和登录状态
3. 先扩展关键词，再向用户确认配置
4. 根据确认后的关键词执行搜索
5. 提取笔记内容与评论
6. 汇总结果并向用户汇报
7. 删除 `status.md`，重置 `config.json`

## 目录结构

```text
xhs-search-skill/
├── SKILL.md
├── config.json
├── status.md
├── requirements.txt
├── logs/
├── output/
│   ├── searchUrls/search_urls_*.json
│   └── notes/xhs_note_*.json
└── scripts/
    ├── common.py
    ├── check_env.py
    ├── env_setup.py
    ├── search_notes.py
    └── extract_note.py
```

## 运行约定

以下命令默认在 skill 根目录 `xhs-search-skill/` 下执行。

### config.json 关键字段

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `session_id` | `""` | AgentBay session ID，留空则新建 |
| `context_name` | `"xiaohongshu"` | Browser Context 名称，用于持久化 Cookie |
| `agentbay_api_key` | `""` | AgentBay API Key，与环境变量 `AGENTBAY_API_KEY` 同名（小写），[开通入口](https://www.aliyun.com/product/agentbay) |
| `agentbay_region_id` | `""` | 对应环境变量 `AGENTBAY_REGION_ID` |
| `agentbay_endpoint` | `""` | 对应环境变量 `AGENTBAY_ENDPOINT` |
| `agentbay_timeout_ms` | `"30000"` | 对应环境变量 `AGENTBAY_TIMEOUT_MS` |
| `proxy` | `{}` | 代理配置；为空对象时不使用代理 |
| `keywords` | `[]` | 关键词字符串数组，每个元素只能有 1 个关键词 |
| `max_notes_per_keyword` | `3` | 每个关键词最多采集条数 |
| `scroll_rounds` | `10` | 评论区滚动轮数 |

proxy 示例：

```json
{
  "proxy": {
    "server": "http://127.0.0.1:7890",
    "username": "",
    "password": ""
  }
}
```

> 小红书反爬策略较强，建议配置高质量代理。

### 状态驱动规则

每次开始任务前先检查 `status.md`：

| 状态 | 含义 | 下一步 |
|------|------|--------|
| `error` | 本地依赖或 AgentBay 基础配置检查失败 | 修复配置后重试 |
| `login_required` | 需要登录 | 引导用户通过 `resource_url` 登录，再重跑 `env_setup.py` |
| `running` | 环境就绪 | 展示当前配置并开始搜索 |
| `search_done` | 搜索完成 | 运行 `extract_note.py` |
| `extract_done` | 提取完成 | 读取 `output/notes/` 做总结 |
| 不存在或为空 | 没有进行中的任务 | 从 Step 1 开始 |

补充规则：
- `status.md` 不存在或为空，说明上次任务已结束
- `status.md` 仍有状态，优先按当前状态续跑，不要重复从头执行
- 任务完成后删除 `status.md`

## 操作步骤

### Step 1：检查本地依赖与 API Key 配置

先安装依赖并运行检查脚本：

```bash
cd xhs-search-skill
pip install -r requirements.txt
python scripts/check_env.py
```

`check_env.py` 主要检查：
- `agentbay`、`playwright` 等关键依赖是否已安装
- `agentbay_api_key` 是否已在 `config.json` 或环境变量中配置
- AgentBay 基础连接配置是否可用（API Key 必填，其他配置按需校验）
- 会创建或复用一个可继续用于后续步骤的 AgentBay session，并写回 `config.json` 的 `session_id`，用于校验 key、region、endpoint 等配置是否可正常工作

API Key 二选一配置：

```json
{
  "agentbay_api_key": "akm-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

或：

```bash
export AGENTBAY_API_KEY=akm-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

结果判断：
- 脚本执行成功，说明依赖、API Key 和 AgentBay 基础连接校验通过，可进入 Step 2，并清理旧的 `error` 状态
- 如创建或复用了可用 session，会把 `session_id` 写回 `config.json`，供后续步骤继续使用
- 如果脚本写入 `status.md = error` 或提示缺少 API Key，不要进入下一步

如果没有配置 API Key：
- 先让用户补齐 `config.json` 中的 `agentbay_api_key`
- 或让用户设置环境变量 `AGENTBAY_API_KEY`
- 配置完成后，重新运行 `python scripts/check_env.py`

缺少 API Key 时的固定处理：
- 必须明确告知“当前无法执行小红书 skill，需要先配置 AgentBay API Key”
- 必须给出开通入口：https://www.aliyun.com/product/agentbay
- 不要在缺 key 时改用其他数据源、搜索引擎或网页抓取作为兜底
- 用户补齐 key 后，再继续 Step 2

### Step 2：检查登录状态

只有在 `python scripts/check_env.py` 已通过后，才运行：

```bash
python scripts/env_setup.py
```

读取 `status.md`：
- 如果是 `running`，直接进入 Step 3
- 如果是 `login_required`，按下面流程处理
- 如果是 `error`，返回 Step 1 重新检查本地配置

登录流程，最多重试 3 次：

```text
1. 读取 status.md 中的 session_id 和 resource_url
2. 将 session_id 写回 config.json；如果没有则置为空
3. 通知用户打开 resource_url，在沙箱浏览器中完成登录
4. 等待用户回复“已登录”
5. 重新运行 python scripts/env_setup.py
6. 如果仍是 login_required，继续重试；满 3 次后终止
```

说明：
- `env_setup.py` 现在流程上只承担登录态检查步骤
- `session_id` 会自动更新，可复用
- 登录失败重试超过 3 次时，应明确终止任务

### Step 3：先扩展关键词，再向用户确认配置

登录成功后、搜索前，先根据用户原始需求扩展关键词，再把扩展结果和其它配置一起展示给用户确认。

关键词扩展规则：
- 用户只给 1 个关键词时，扩展到 3 个
- 用户给 2 个关键词时，可保持不变或补到 3 个
- 用户给 3 个及以上时，直接使用

关键词格式要求：
- `keywords` 必须是字符串数组
- 每个数组元素只放 1 个关键词
- 多个关键词必须拆成多个元素，不能拼进同一个字符串
- 写 JSON 时建议一行一个关键词元素

正确示例：

```json
{
  "keywords": [
    "阿里云无影 评测",
    "阿里云无影 使用体验",
    "阿里云无影 最新动态"
  ]
}
```

错误示例：

```json
{
  "keywords": [
    "阿里云无影 评测，阿里云无影 使用体验，阿里云无影 最新动态"
  ]
}
```

推荐格式：

```text
环境已就绪，当前配置如下：
- 关键词：
  - 关键词 1
  - 关键词 2
  - 关键词 3
- 每个关键词采集上限：N 条
- 代理：未配置 / 自定义代理 xxx

如需调整以上配置，请告诉我。
没问题的话我将开始搜索。
```

要求：
- 必须先展示扩展后的关键词，再等待用户确认
- 如果用户要求增删改关键词，应先更新关键词列表，再继续后续步骤
- 关键词优先逐行展示，不要挤成一长串
- 如未配置代理，可提醒用户小红书风控较强

### Step 4：根据确认后的关键词执行搜索

运行：

```bash
python scripts/search_notes.py
# 或
python scripts/search_notes.py --keywords "关键词1,关键词2,关键词3"
```

数量规则：
- 默认 `max_notes_per_keyword = 3`
- “多找一些”可调到 `5-10`
- “简单看看”可调到 `2-3`

搜索前必须说明：

```text
即将搜索以下已确认关键词：
- xxx
- xxx
- xxx

每个关键词最多采集 N 条，预计共采集约 M 条笔记链接。
开始搜索...
```

内部结果会写入 `output/searchUrls/search_urls_{timestamp}.json` 和 `status.md`，仅供后续步骤使用，不要展示给用户。

### Step 5：提取笔记内容与评论

运行：

```bash
python scripts/extract_note.py
python scripts/extract_note.py --url "https://..."
python scripts/extract_note.py --urls-file output/searchUrls/search_urls_20260309_120000.json
```

提取前必须说明耗时：

```text
共 N 条笔记待提取，每条约需 50 秒，预计总耗时约 X 分钟。
请稍等，我开始提取。
```

调用建议：
- 同步调用：`timeout >= N * 50 秒 + 30 秒`
- 异步轮询：首次轮询延迟约 `N * 50 秒 * 0.8`

内部结果会写入 `output/notes/xhs_note_{timestamp}.json` 和 `status.md`，不要展示给用户。

### Step 6：整理结果并汇报用户

当 `status.md` 为 `extract_done` 时，读取 `output/notes/` 下本次提取生成的笔记 JSON，输出结构化总结。

汇报原则：
- 不要输出原始 JSON
- 以整体观察为主，不要逐条笔记平铺
- 可引用少量代表性案例，但只用于支撑结论
- 评论只在能支撑判断时展示

推荐格式：

```text
共采集 N 条笔记，关键词：xxx、xxx、xxx

整体观察：
- 这批内容主要集中在 xxx、xxx、xxx
- 用户最关注的问题是 xxx
- xxx 类型内容更容易获得互动
- 整体情绪偏 xxx

代表性内容：
- 笔记 A：核心观点 + 为什么有代表性
- 笔记 B：核心观点 + 为什么有代表性

结论建议：
- 舆情：总结讨论焦点和情绪走向
- 选题：提炼值得延展的方向
- 产品反馈：归纳好评、槽点和待验证问题

本次共分析 N 条笔记。
```

严格禁止：
- 不要展示 `status.md`、`search_urls_*.json`、`xhs_note_*.json`
- 不要展示任何 JSON 路径、目录路径或本地存储位置
- 不要添加“数据源”“文件位置”“保存位置”“本地目录”等区块
- 即使知道最终文件位置，也不要告诉用户

### Step 7：任务完成后收尾

全部完成后：

1. 删除 `status.md`
2. 重置 `config.json`
   - `session_id = ""`
   - `keywords = []`

## 数据结构参考

以下结构仅供读取 JSON 时参考，不要原样展示给用户：

```json
{
  "url": "https://www.xiaohongshu.com/explore/...",
  "title": "笔记标题",
  "content_text": "正文内容",
  "author": "作者昵称",
  "like_count": 1234,
  "collect_count": 567,
  "comment_count": 89,
  "comments": [
    {"level": "一级评论", "text": "评论内容", "like_count": 10},
    {"level": "二级评论", "text": "回复内容", "like_count": 2}
  ]
}
```

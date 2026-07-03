---
name: weibo-hot-with-your-taste
description: 抓取微博热榜，根据用户偏好定制化推送热点话题，视情进行信息补全。特性：用户偏好交互式访谈，推送质量即时反馈，特征规则自优化。关键词：微博热榜 / 态势快报 / 私人定制 / grill taste / self-adaptive taste feature
url: https://github.com/zify9000/weibo-hot-with-your-taste
license: MIT
---

# 微博热榜追踪

## 使用指南（以hermes agent为例）
1. 加载skill。下达指令，“安装skill，https://github.com/zify9000/weibo-hot-with-your-taste”；
2. 配置凭证。下达指令，"配置微博热点skill", 交互式完成初始化配置（提供LLM和飞书凭据，扫码登陆微博，访谈用户偏好形成特征规则）；
3. 设置定时任务，下达指令，“每小时执行一次微博热点爬取，12点05，18点05各执行一次推送，每周执行一次偏好特征优化（编写sh脚本，使用no_agent模式执行）”；
4. 触发式调用，下达指令，“抓取并推送微博热点”，“对话题1/3不感兴趣”，“展开说说话题2和话题3”，“进行一轮微博热点偏好调研”。

## 目录结构

```
weibo-hot-with-your-taste/
├── SKILL.md                  # Skill 说明文档
├── scripts/
│   ├── common.py             # 公共工具：配置加载、日志、格式化
│   ├── fetch.py              # 抓取热点：抓取 → 规则过滤 → LLM核校 → 缓存
│   ├── push.py               # 推送热点：读缓存 → 去重 → LLM二次过滤 → 推送飞书卡片
│   ├── survey.py             # 调研用户偏好：LLM 从未推送话题中召回候选，记录用户对候选话题的意见
│   ├── feedback.py           # 反馈推送质量：将用户对推送质量的反馈写入 tasted_topics.jsonl，收到"信息不全"反馈时触发二次搜索
│   ├── fit_taste.py          # 偏好特征自适应优化：根据反馈和分类变化，LLM 全面优化 taste.yaml 全部七项配置
│   ├── init/
│   │   ├── taste.py        # 偏好初始化：配置领域关键词→配置喜欢/不喜欢的话题类型→配置召回关键词→偏好访谈→生成特征规则
│   │   ├── llm_feishu.py      # LLM/飞书凭据配置：写入 .llm.env / .feishu.env
│   │   ├── weibo_get_qr.py     # 微博登录步骤1：获取二维码，浏览器保持运行
│   │   └── weibo_wait_login.py  # 微博登录步骤2：等待扫码，保存 Cookie
│   ├── env/
│   │   ├── .llm.env          # LLM 配置（llm_model / llm_base_url / llm_api_key）
│   │   ├── .llm.env.example
│   │   ├── .feishu.env       # 飞书应用凭据
│   │   ├── .feishu.env.example
│   │   ├── .weibo.env        # 微博 Cookie（weibo_sub + weibo_cookies_json）
│   │   └── .weibo.env.example
│   ├── config/
│   │   ├── base.yaml         # 基础配置（LLM参数、飞书重试策略、摘要补充模式）
│   │   ├── taste.yaml         # 偏好特征（关注领域、感兴趣/不感兴趣的话题类型、召回关键词、yes/no综合评判标准）
│   │   └── prompt.yaml       # LLM prompt 模板
│   ├── data/
│   │   ├── topic_category.json     # 话题类型词库（自动维护，记录微博API返回的category）
│   │   ├── all_topics.jsonl  # 原始全量抓取数据（每次fetch追加）
│   │   ├── ruleFiltered_topics.jsonl # 规则过滤后候选（每次fetch追加，LLM核校前）
│   │   ├── pushed_topics.jsonl # 已推送热点话题
│   │   ├── tasted_topics.jsonl # 用户品味档案（反馈+调研结果合并）
│   ├── tmp/                  # 步骤间临时文件：fetch → push 缓存、init/taste 缓存
│   ├── log/                  # fetch、push等各模块运行日志（按日滚动，保留7天）+ init.log 初始化记录
│   └── cli/
│       └── clear.sh          # 清理工具：一键重置所有数据和配置到初始状态
└── references/               # 参考文档
    ├── weibo-api-header.md   # 微博公开 API 的 Header 要求
    └── weibo-auth.md         # 微博登录态与 API 认证机制
```

## 业务流

### 0. 初始化

#### 1. **凭据配置**

凭据文件统一在 `scripts/env/`：

| 文件 | 内容 |
|------|------|
| `.llm.env` | `llm_model` / `llm_base_url` / `llm_api_key` |
| `.feishu.env` | `feishu_app_id` / `feishu_app_secret` / `feishu_chat_id` |
| `.weibo.env` | 微博 Cookie（由 `init/weibo_get_qr.py` + `init/weibo_wait_login.py` 生成，含 SUB + cookies_json） |

agent 首次使用时应检查这 3 个文件是否存在，对缺失的逐一询问配置。

> **⚠️ agent 注意**：
1. `.llm.env`、`.feishu.env`、`.weibo.env` 是以 `.` 开头的隐藏文件。部分工具的 glob 匹配（如 `search_files(pattern='.llm.env')`）对隐藏文件支持有缺陷，可能返回假阴性。**用 `ls -la scripts/env/` 或直接 `Read` 目标路径确认**，不要单独依赖 glob 搜索结果。
2. Hermes 等agent框架会拦截终端中出现的 key 明文。**不要直接在终端 echo/cat/粘贴 key**，应写 Python 脚本从 Hermes 配置（`config.yaml`、环境变量）读取实际值后调用 `write_file` 写入 `.llm.env` / `.feishu.env`，避免 key 泄露到终端历史。


**LLM / 飞书配置**：

```
python3 scripts/init/llm_feishu.py \
  --llm-model <模型名> --llm-base-url <API地址> --llm-api-key <API密钥> \
  --feishu-app-id <app_id> --feishu-app-secret <secret> --feishu-chat-id <chat_id>
```
可只传 LLM 参数、只传飞书参数，或同时传入两者。

**微博 Cookie 配置**：

```
# 步骤1：获取二维码
python3 scripts/init/weibo_get_qr.py

# agent 读取 /tmp/weibo_login_qr.png 展示给用户扫码

# 步骤2：等待扫码并保存 Cookie
python3 scripts/init/weibo_wait_login.py
```

**直接执行上述命令，不要自己重写登录逻辑。** 步骤1以 headless 模式启动 Chromium，QR 图片保存至 `/tmp/weibo_login_qr.png`，浏览器进程保持运行。步骤2连接已有浏览器等待扫码完成，登录后保存 Cookie 至 `.weibo.env` 并关闭浏览器。

Cookie 过期后 fetch 阶段日志会输出警告，重新执行上述命令即可。

#### 2. **筛选特征配置（4步流水线）**：

**Step 1 — 领域关键词 → LLM 匹配 → 审查分类 + 召回：**
1. 检查 `scripts/config/taste.yaml` 中 `yes_criteria` 是否存在且非空
2. 不存在 → 提示用户："首次使用，需要设置你的偏好。请提供2-5个你最关注的领域关键词，如：科技、经济、国际时政"
3. 用户提供 → 执行：
   ```
   python3 scripts/init/taste.py mention-taste --domain-kw "关键词1" "关键词2" ...
   ```
4. 获取 JSON，展示 `liked`/`disliked` LLM 建议，询问用户是否调整。同时询问召回关键词：
   > "当话题属于不感兴趣的类别但包含召回关键词时会被救回。例如：'AI'、'芯片'。多个用逗号分隔，回复'不需要'跳过。"

5. 用户调整后，带 `--liked`/`--disliked`/`--recall` 重新执行同一条命令：
   ```
   python3 scripts/init/taste.py mention-taste --domain-kw "关键词1" "关键词2" ... --liked "..." --disliked "..." --recall "..."
   ```
   > 传入 `--liked`/`--disliked` 后跳过 LLM 匹配，直接使用用户指定的分类。

**Step 2 — 深度偏好访谈（推荐，可跳过）：**
6. 询问用户是否进行深度访谈。若同意，Agent 逐轮编排：
   ```
   # 第1轮：生成问题
   python3 scripts/init/taste.py grill-taste
   → {"round": 1, "max_rounds": 4, "question": "..."}

   # Agent 展示问题给用户，收集回答后：
   python3 scripts/init/taste.py grill-taste --answer "用户的回答"

   # 重复直到输出最终 JSON（含 qa_rounds），或用户回答 "done" 提前结束
   ```
   最多 4 轮，无需 stdin 交互。

**Step 3 — 生成判断标准：**
7. 执行：
   ```
   python3 scripts/init/taste.py build-criteria
   ```
   > 若跳过了 Step 2，传入 Step 1 确认模式输出 JSON。

8. 获取 JSON（`status: "pending_confirm"`），将 `yes_criteria` 和 `no_criteria` 展示给用户确认：
   ```
   **判断标准已生成，请确认：**

   **重要（yes）：**
   {yes_criteria 内容}

   **不重要（no）：**
   {no_criteria 内容}

   确认无误？你可以直接确认，或提出修改意见（如"yes里加上'涉及AI监管'，no里删掉'娱乐八卦'"）。
   ```

**Step 4 — 确认写入：**
9. 用户确认或提出修改 → 将最终版本保存为 JSON 文件（与 build-criteria 输出结构一致），执行：
    ```
    python3 scripts/init/taste.py confirm-criteria
    ```
10. 初始化完成（yes_criteria 写入 taste.yaml，初始化记录写入 log/init.log）

**重新初始化：** 清空 `scripts/config/taste.yaml` 中的 `yes_criteria` 和 `no_criteria` 后再次使用即可

### 1. 抓取与推送

**抓取和推送解耦为两个独立脚本**，一天中可多次抓取，一次性推送：

```
fetch.py:  抓取微博热榜 → 规则过滤 → 写入 ruleFiltered_topics.jsonl → 信息量核校+摘要补充 → LLM核校
                ↓              ↓                                       │
           all_topics.jsonl  topic_category.json                       │
                                                                       │ LLM成功 → important → fetch_topics.jsonl
                                                                       │ LLM失败 → candidates 存 meta，push 补跑 judge
                                                                       ▼
push.py:   读 meta + topics → 按 word 去重 → (多次抓取/有failed) LLM 二次精选 → 飞书卡片 → 清空缓存
                                                                                     ↓
                                                                              pushed_topics.jsonl
                                                                 (仅一次且全部ok) 跳过二次过滤
```

**跨周期去重**：推送时会识别近N天（默认3天，由 `base.yaml` 中 `push.dedup_days` 配置）已推送过的热点，将其平铺展示在「📌 近N天已推送热点」区域，并标注热度变化（上涨红色↑，下跌绿色↓，变化阈值10%）。

**全重复处理**：如果本次推送候选全部为近期已推送热点，则发送文本消息「当前时段无新增微博热点」。

**信息量核校与摘要补充**：规则过滤后，对信息量不足的话题补充摘要。由 `base.yaml` 中 `规则过滤后自动补充` 控制：
- `llm` 模式（默认）：短话题（≤5字）直接走搜索快速路径；长话题由 LLM 批量判断信息量，不足的再搜索补充摘要
- `heuristic` 模式：仅按字数阈值判断（向后兼容）

**⚠️ 推送必须通过 `push.py` 完成，禁止使用 `send_message` 等工具替代。** `push.py` 发送的是飞书卡片消息（带红色标题栏、分类标签、序号），不是纯文本。

### 2. 反馈

**触发词**：`推送反馈` / `反馈` / 直接给序号评价如 `1,3感兴趣` / `1和4不错，2不关心` / `3信息不全`

**工作流**：

1. 用户说"推送反馈"或直接给序号评价
2. 读取 `scripts/data/pushed_topics.jsonl`，取最后一条记录
3. 如果用户只说了"推送反馈"而未给评价 → 提示："本次推送共N条，请告诉我序号偏好，如'1,3感兴趣，2不感兴趣，4信息不全'"
4. 如果用户已给序号评价 → 解析自然语言，映射序号到话题：
   - `1,3感兴趣` → 话题1和3 feedback=liked
   - `2和5不感兴趣` → 话题2和5 feedback=disliked
   - `4信息不全` → 话题4 feedback=info_insufficient（即时触发二次搜索补充摘要并推送飞书）
   - `1和2不错，其他一般` → 话题1和2 feedback=liked，其余 feedback=disliked
5. 逐条调用 `python3 scripts/feedback.py --word "话题名" --feedback liked/disliked/info_insufficient --ts "推送时间戳" --comment "用户原话"`
6. 回复："已记录：👍 x2, 👎 x3"

**反馈类型**：

| --feedback | 语义 | 触发动作 |
|---|---|---|
| `liked` | 感兴趣 | 仅记录 |
| `disliked` | 不感兴趣 | 仅记录 |
| `info_insufficient` | 信息不全 / 要求二次检索 | 记录 + 即时二次搜索补充摘要 + 推送飞书补充卡片 |

**注意**：如果用户未明确表态的序号（如只说"1和3感兴趣"但共有8条），不要猜测，不记录未提及的条目。

### 3. 调研

**触发词**：`偏好调研` / `调研` / `有什么我可能错过的新闻`

**工作流**：

1. 执行 `python3 scripts/survey.py`，获取 JSON：
   - `ready=false` → 告诉用户数据不足（如"未推送新闻不足5条，无法调研"）
   - `ready=true` → 得到 `{candidates, total_unpushed, pushed_count}`
2. 按以下格式展示候选话题（LLM 推荐项用 🔹 标记）：

```
今天有 45 条未推送新闻，LLM 筛选出以下可能与你相关的：

1. #话题1#  `科技`
2. 🔹 #话题2#  `国内时政`
3. #话题3#  `财经`
4. 🔹 #话题4#  `互联网`
...

你对哪些感兴趣？例如："1和2感兴趣"
```

3. 用户回复后，解析自然语言，调用 `feedback.py` 逐条写入。未提及的条目不写入。

### 4. 偏好特征自适应优化

**触发词**：`优化偏好` / `fit taste`

**定时任务**：`python3 scripts/fit_taste.py`（建议每周执行一次）

**工作流**：

1. 执行 `python3 scripts/fit_taste.py`
2. 脚本自动完成以下步骤：
   - 检查是否有足够的新反馈数据（距上次优化后 ≥ 5 条）或新分类
   - 收集 tasted_topics.jsonl 中的用户反馈 + topic_category.json 中的新分类
   - LLM 全面审视 taste.yaml 全部七项配置，输出优化后的完整配置
   - 备份旧 taste.yaml → taste.yaml.bak，写入新配置
3. 优化完成后，日志中会输出变更摘要

**优化范围**：
- `domain_keywords`：关注领域关键词
- `liked_categories`：感兴趣的话题分类
- `disliked_categories`：不感兴趣的话题分类
- `recall_keywords`：召回关键词
- `yes_criteria`：判断为重要的标准
- `no_criteria`：判断为不重要的标准
- `info_check_criteria`：信息量核校标准（由 info_insufficient 反馈驱动优化）

**手动触发**：agent 执行 `python3 scripts/fit_taste.py`，完成后读取日志中的变更摘要告知用户。

### 5. Cookie 过期重新配置

**症状**：
- 推送卡片中所有话题都没有摘要（扩展信息），日志中大量 `未获取到话题详情` 或 `疑似 Cookie 已过期`
- 标记文件 `/tmp/weibo_cookie_status.json` 内容为 `{"status": "expired"}`
- `fetch_topic_detail` 报错：`获取话题详情失败（疑似 Cookie 已过期，API 返回登录页面）`

**根因**：`.weibo.env` 中的 Cookie（`SUB` 字段）已失效，m.weibo.cn 将请求重定向到登录页面，`resp.json()` 解析 HTML 时报错。

**恢复流程（agent 必须按此执行）**：

```
# 步骤1：获取二维码
python3 scripts/init/weibo_get_qr.py

# agent 读取 /tmp/weibo_login_qr.png 展示给用户扫码

# 步骤2：等待扫码并保存 Cookie
python3 scripts/init/weibo_wait_login.py
```

> ⚠️ **禁止告诉用户手动从浏览器复制 Cookie。** 必须使用上述 QR 码登录流程——headless Chromium 打开微博登录页获取二维码 → 用户 App 扫码 → nodriver 自动提取 Cookie 写入 `.weibo.env`。

**主动检测**（agent 排查用）：
1. 读取最近一次 fetch 日志：`tail -50 scripts/log/fetch_*.log | grep -E "Cookie|过期|详情获取"`
2. 检查标记文件：`cat /tmp/weibo_cookie_status.json`（存在且 `status=expired` 即确认过期）
3. 确认后主动提醒用户并执行上述恢复流程




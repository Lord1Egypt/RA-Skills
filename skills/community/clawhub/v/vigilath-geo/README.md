# Vigilath GEO 优化 Skill

把你的 AI agent(小龙虾)链接到 **Vigilath**,让它具备"检测·审计·优化·监控品牌在 AI 搜索引擎中的可见性"的能力。

**装完不授权也能用一半**:任何网站的 GEO + SEO 体检(`check`)免登录、免费、不限次;
要看某个账号的真实投放数据、跑一键全面诊断、查舆情产稿,才需要授权。

底层 = 一个 1 年期账号 token + Vigilath 的 `/api/agent/v1/*` 接口;本 skill 是 drop-in 封装,纯标准库、零依赖。

## 最省事:把地址发给你的 AI 助手

    https://vigilath.cn/skill

agent 抓这个地址拿到的是**可直接执行的纯文本安装指令**(人用浏览器打开则跳到安装页 `/install`)。
跟它说一句「照这个地址装一下」即可,它会自己跑下面这条命令、把配对码转达给你。

## 安装(手动跑,免 token,一条通用命令)

在**要装 skill 的那台机器**上跑:

```bash
curl -fsSL https://vigilath.cn/skill/install.sh | bash
```

终端会显示一个 8 位配对码。用浏览器打开它给出的链接(`https://vigilath.cn/link`),登录 Vigilath 账号、输入配对码点「批准」,安装就自动继续完成。

这条命令对所有人都一样,可以直接印在文档、官网、聊天里 —— token 由脚本自己去换,**不经过剪贴板、不进 shell 历史**。配对码 10 分钟内有效、只能用一次。

- 装到哪:自动装进**所有**已存在的 skills 目录 —— OpenClaw `~/.openclaw/skills`、Claude `~/.claude/skills`、`~/.agents/skills`、当前项目 `./skills`;都没有则兜底 `~/.vigilath/skills`。也可 `--dir <路径>` 只装一处。
- 凭证:token 与 API 基址写进 `~/.vigilath/config`(权限 600,**无需设环境变量**)。
- 换账号 / token 过期:重跑 `python3 <skill目录>/scripts/geo_client.py login` 再授权一次即可,不必重装。

### 备选:已有 token 的装法

无人值守的机器、CI、或不方便交互时,用控制台「对接集成」页生成的带 token 命令:

```bash
curl -fsSL https://vigilath.cn/skill/install.sh | bash -s -- <你的token> --base https://vigilath.cn
```

> `--base` 请**照控制台给的那条命令原样用**。脚本被 `curl | bash` 管道执行时拿不到自己的下载地址,基址只能靠它传入;不传会退到默认的 `https://vigilath.cn`。

### OpenClaw 用户

上面那条免 token 命令直接可用(会装进 `~/.openclaw/skills`)。也可以走 OpenClaw 自己的安装器:

```bash
openclaw skills install <本目录路径> --global      # 本地目录
openclaw skills                                    # 确认已识别
```

装完仍需授权一次:`python3 ~/.openclaw/skills/vigilath-geo/scripts/geo_client.py login`。

## 手动安装(可选)

把 `vigilath-geo/` 目录放进你 agent 的 skills 目录,token 二选一:
- 写进 `~/.vigilath/config`:`VIGILATH_AGENT_TOKEN=...`(一行 KEY=VALUE)
- 或设环境变量:`export VIGILATH_AGENT_TOKEN="..."`

> token 是机密(等同 API key):**不要硬编码、不要打印、不要提交**。一个 token = 一个账号,只能访问该账号自己的数据。

## 自测

```bash
python3 <skill目录>/vigilath-geo/scripts/geo_client.py check https://example.com   # 免登录
python3 <skill目录>/vigilath-geo/scripts/geo_client.py capabilities
python3 <skill目录>/vigilath-geo/scripts/geo_client.py data today
python3 <skill目录>/vigilath-geo/scripts/geo_client.py chat "我的品牌累计被搜到几个问题?"
```

- `check <网址>` **不需要任何凭证**:GEO 25 类 + SEO 12 类全跑,返回两个 0–100 分与等级。
  分数真实,但免费档只给 5(GEO)+3(SEO)类明细,其余只列类目名、无修复建议、不写历史。
  加 `--no-seo` 只跑 GEO。
- `chat` 输出 = 自然语言回答 + 结构化卡片 JSON(命中数字、竞品等)。
- `data <name>` 直接取数(`overview` / `period` / `periods` / `coverage` / `publish` / `diagnosis` / `run`),不走大模型,更快更省。旧名 `today` / `growth` / `batch` / `report` 仍兼容。

## 能力边界

- 引擎、调度、频率由 Vigilath 平台固定,只看结果。
- **真实对外发布不在本 skill 范围**(受平台内部护栏控制);本 skill 只做查询 / 诊断 / 归因 / 优化建议。
- `401` = token 无效/过期,联系 Vigilath 重发。

## 需要 Python 之外的语言?

`/api/agent/v1/*` 是普通 HTTP(`chat` 为 SSE,`data/*`、`meta/*` 为 JSON),带 `Authorization: Bearer <token>` 即可,用任意语言重写客户端都行。协议见 Vigilath《对外开放-契约》(docs/agent/)§11 / §13。

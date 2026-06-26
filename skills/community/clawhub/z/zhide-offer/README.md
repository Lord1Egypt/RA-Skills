# 职得Offer校园求职助手

一个面向校招和实习场景的 OpenClaw Skill。

它把职得Offer的 MCP 接口封装成一组本地可直接调用的查询脚本，适合用来：

- 搜校招/实习岗位
- 查看岗位详情和 JD
- 搜真实面经
- 查看完整面经轮次、题目和回答

适用人群：

- 正在找校招、实习、秋招机会的同学
- 想快速收集岗位信息、公司方向、城市分布的人
- 想做面试准备、看真实面经和常见题的人

## 能力概览

- `jobs.search`：搜索岗位列表
- `jobs.get`：查看岗位详情
- `interviews.search`：搜索面经列表
- `interviews.get`：查看面经详情

## 为什么值得装

- 信息集中：岗位和面经放在一套查询入口里
- 上手直接：安装后就能用 Node 脚本查，不用自己拼 MCP 请求
- 支持筛选：公司、城市、招聘类型都能带上
- 面试准备友好：可直接拉完整轮次、题目和回答

## 安装后怎么配

二选一即可。

### 方式 1：环境变量（推荐）

```bash
export ZHIDE_OFFER_KEY='ofk_your_key_here'
```

### 方式 2：本地配置文件

```bash
cp ~/.openclaw/skills/zhide-offer/scripts/config.json.template ~/.openclaw/skills/zhide-offer/scripts/config.json
```

然后把 `scripts/config.json` 里的 `zhideOfferKey` 改成你的真实 key。

## 快速开始

### 查岗位

```bash
node ~/.openclaw/skills/zhide-offer/scripts/jobs_search.js 数据产品经理
node ~/.openclaw/skills/zhide-offer/scripts/jobs_search.js 产品经理 --company 字节跳动 --city 北京 --size 5
```

### 看岗位详情

```bash
node ~/.openclaw/skills/zhide-offer/scripts/jobs_get.js <岗位ID>
```

### 查面经

```bash
node ~/.openclaw/skills/zhide-offer/scripts/interviews_search.js 产品经理 --company 字节跳动 --tag 校招 --limit 5
```

### 看完整面经

```bash
node ~/.openclaw/skills/zhide-offer/scripts/interviews_get.js <面经ID>
```

## 更顺手的统一入口

如果你不想记多个脚本名，也可以直接用这个包装命令：

```bash
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh jobs-search 产品经理 --size 3
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh job-get <岗位ID>
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh interviews-search 产品经理 --limit 2
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh interview-get <面经ID>
```

## 使用建议

- 搜面经时，`position_query` 最好用单一精准词组，比如 `产品经理`、`数据产品经理`
- 不要把很多词硬堆在一起，不然容易空结果
- `interviews.search` 响应通常比岗位搜索慢一些，约 8 秒，属于正常现象
- 每日接口调用有限额，建议先缩小关键词再查

## 目录说明

- `SKILL.md`：Skill 描述和触发说明
- `README.md`：市场展示和使用说明
- `references/api.md`：接口字段说明
- `scripts/`：实际可执行脚本

## 当前形态说明

这个 Skill 当前是“技能说明 + 可直接运行的本地脚本”形态。

优点是简单、透明、好改；缺点是它还不是 OpenClaw 原生一等工具扩展。如果后续要做成更原生的交互形式，可以继续封装成 tool schema 或 MCP bridge 版本。

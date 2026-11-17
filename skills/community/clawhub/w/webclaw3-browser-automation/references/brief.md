# 环节③：提炼（brief）

> 什么时候读这个文件：探索成功后，用户说"提炼成 skill""帮我提炼""以后每天自动跑"。

## 前提：必须先本地探索

**只接受"本次对话里真实探索成功过"的提炼请求。** 判断标准：本次对话中用浏览器真实执行过任务，拿到了结果，且用户确认过满意。

不满足就拒绝并说明：请先描述任务、我们一起探索，拿到满意结果后再提炼。不要凭用户的文字描述直接提炼——纯文字提炼的质量没有保障，这是产品设计红线。

## 四步流程

### 第 1 步：对齐最终版需求

和用户确认两件事：

- **需求描述**：探索中目标常会变（条件放宽、范围调整），以最终确认的版本为准
- **验收标准**：必须可量化、可代码验证。"数据完整""结果正确"不行；">= 10 条，每条含 title、url 且非空"可以

### 第 2 步：写两份文档

凭本次对话记忆写，不需要翻记录、不需要补数据。

**requirement.md** —— 回答"要什么、怎么算成了"：

```markdown
# <skill 英文名，小写/连字符，如 xhs-blogger-posts；同时作为落盘目录名>

## 需求描述
一段话说清任务目标。

## 入参定义
- 参数名（类型，必填/默认值）：说明
> 探索测试值：{ ... }（不要硬编码进 skill）

## Accept
输出格式模板 + 验收底线（数量下限、必含字段；不足时标 partial 并说明）
```

**primer.md** —— 回答"怎么走过去、哪里有坑"：

```markdown
## 入口
目标站点、有效入口、是否需要登录态/浏览器模式

## 走通的路径
1. 按探索实际走通的顺序写步骤（自然语言）

## 筛选逻辑
抓取过程中怎么筛数据：筛选条件在页面上怎么实现、字段怎么换算后比较（如"1.2万"→ 12000）、缺字段时的替代判法
注意：这是执行期的筛数据方法（怎么做），不是验收标准；产出怎么算合格只写在 requirement 的 Accept 里，两边不要重复

## 必避陷阱
- 试过不行的路、反爬现象、页面行为坑
- 目标修正记录：探索中放弃/放宽了什么，别再试
```

三条提炼规则：

1. **入参参数化**：探索用的具体值（搜索词、数量）是测试值，抽成参数写进入参定义，不进正文
2. **requirement 只写最终版**：条件变更的过程作为陷阱写进 primer（"原要求近一周实测仅 3 条，已放宽为参数"），requirement 里不留历史
3. **收稳定技巧，不收精确选择器**：URL 模式、ID 解码规则、"筛选必须走 UI"这类收；CSS 选择器具体值不收，写成"要先 inspect 再定位"的提示

### 第 3 步：落盘，交用户检查

写入当前工作目录 `wc3-brief/<skill名>/`（skill 名即 requirement.md 标题定义的英文名）：

```
wc3-brief/<skill名>/
├── requirement.md
└── primer.md
```

告知用户两个文件路径，请用户检查。**用户确认后才进入第 4 步，不要自行提交。**

### 第 4 步：提交本地生成器，轮询到安装

**前置**：生成器（wc3-pipeline）必须已安装且运行中。装完跑一次 `webclaw3 doctor`，`ready.generate:true` 即可。

**配置**（`~/.webclaw3/config.json`，由 `webclaw3 config ak` 写入）：

- `ak`：wc3-app 登录后获取的 Access Key（`wc3_` 前缀）。缺失时引导用户去 wc3-app 网页登录后复制，跑 `webclaw3 config ak <key>`。
- `appBase`：wc3-app 地址，默认 `https://webclaw3.com`；本地开发可设 `http://127.0.0.1:3003`。

**提交**（本地 http，无鉴权——信任边界在本地）：

```
POST http://127.0.0.1:3460/api/generate
Content-Type: application/json
{ "requirement": "<requirement.md 全文>", "primer": "<primer.md 全文>" }
→ 201 { "id": "skill名", "status": "processing", "skillName": "...", "workDir": "..." }
→ 400/502 把 error 转告用户（H1 不合法 / AK 未配置 / 次数不足）
```

**轮询**（生成通常需要几十分钟，每 60s 一次）：

```
GET http://127.0.0.1:3460/api/skills/{id}
```

- `status=processing`：响应含 `stage`（explore/distill/validate/review）与 `round`，可转述给用户当进度
- `status=done`：响应附 `install`（安装指引 markdown），照指引用 `ln -s` 装到当前 Agent 的 skills 目录，装完提醒用户唤起 skill 实际跑一次验证
- `status=failed`：同 skill 重跑不重复扣次数，把 `error` 转告用户，和用户对齐修订两文档后可重新提交
- `status=interrupted`：服务重启或进程被杀，用 `node cli.mjs --resume -w <workDir>` 恢复

**安装后**：用户验证不通过 → 本地修，走 `references/repair.md`，**不要再打服务端**。

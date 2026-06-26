---
name: raccoon-ppt
description: >
  Raccoon (小浣熊) PPT generation skill powered by the PPT OpenAPI. Create PPT
  decks from a natural-language topic. Primarily use this skill when the user
  wants to create a brand-new full PPT deck; secondarily use it to continue a
  PPT generation task or check the result of an existing PPT task. Keywords:
  raccoon, ppt, slides, presentation, deck, 生成PPT, 做一份PPT, 新建PPT,
  演示文稿, 汇报材料, 培训课件, 路演PPT.
homepage: https://xiaohuanxiong.com
metadata:
  {
    "clawdbot":
      {
        "emoji": "🦝",
        "requires":
          {
            "bins": ["python3"],
            "env": ["RACCOON_API_HOST", "RACCOON_API_TOKEN"],
          },
        "primaryEnv": "RACCOON_API_TOKEN",
      },
  }
---

# Raccoon PPT OpenAPI Skill

你是 PPT 生成任务助手。当用户明确要求"生成/创建/做一份 PPT"时,使用本 skill 调用小浣熊 API 创建完整演示文稿。

## 快速判断:何时使用本 Skill

**立即使用(第一优先):**
- 用户说"帮我做一份XX的PPT"、"生成一个XX演示文稿"
- 用户已给出主题,明确要求产出完整 PPT 成品
- 用户明确提到"用小浣熊生成PPT"

**次要使用:**
- 继续回答之前 PPT 任务的补充问题
- 查询已创建 PPT 任务的进度或下载链接

**不要使用:**
- 用户只是咨询如何制作 PPT(给建议即可)
- 用户要编辑已有 PPT 文件(本 skill 只能新建)
- 用户只是讨论 PPT 话题,没有明确生成意图



## 核心规则（必读）

**交互原则：**
1. 用自然语言交互，不暴露技术细节（如 job_id）
2. 必须使用 skill 自带脚本，不要自己写 curl 或 Python 代码
3. `waiting_user_input` 是正常状态，把 API 返回的 question 转成自然语言问用户

**参数处理：**
4. 自动推断 role/scene/audience，无法确定时用一句话问用户（给出选项）
5. 优先使用枚举值，用户表达不在枚举内时直接用原始输入

**时间预期（重要）：**
6. 创建任务接口响应需要 **2-3 分钟**（正常特性，不是超时）
7. 接口可能需要最多 **120 秒**才返回，设置足够的超时时间
8. 任务提交后告知用户："任务已创建，预计 10-120 分钟完成"

**状态管理：**
9. 任务状态自动保存到本地，用 `find-recent-job` 查找最近任务
10. 定期用 `check-job` 检查进度，状态变为 `succeeded` 时通知用户并提供下载链接
11. 任务失败时，展示用户友好的失败原因

## 环境变量检查

**每次执行前必须检查：**
```bash
source ~/.zshrc && echo "RACCOON_API_HOST=${RACCOON_API_HOST:-未设置}" && echo "RACCOON_API_TOKEN=${RACCOON_API_TOKEN:+已设置}"
```

**必需变量：**
- `RACCOON_API_TOKEN`（必需）
- `RACCOON_API_HOST`（可选，默认 https://xiaohuanxiong.com）

**未设置时提示用户：**
```bash
export RACCOON_API_HOST="https://xiaohuanxiong.com"
export RACCOON_API_TOKEN="your-token-here"
```

**重要：Token 清理**
环境变量可能包含换行符，执行脚本时必须清理：
```bash
CLEAN_TOKEN=$(echo "$RACCOON_API_TOKEN" | tr -d '\n\r')
RACCOON_API_TOKEN="$CLEAN_TOKEN" python3 scripts/main.py ...
```
- 第一优先或第二优先都可:用户明确提到"小浣熊 PPT"或要求用小浣熊来生成演示文稿。

在下面场景不要使用本 skill:

- 用户只是想优化一页文案、润色标题、改写摘要、补几条 bullet,但并没有要求直接生成整套 PPT。
- 用户已经有现成 PPT,只是想局部改稿、扩写单页、压缩页数、调整措辞,而不是重新生成一整份。
- 用户只是想讨论汇报思路、页面结构、演讲提纲、配色建议,而不是立刻创建 PPT 任务。
- 用户要处理的对象不是 PPT 成品生成任务,例如单纯写文章、写邮件、写方案、做表格。
- 用户表达仍然停留在泛化讨论,尚未表现出"现在就帮我做一份 PPT"或"继续/查询已有 PPT 任务"的意图。

典型触发话术:

- "帮我生成一份面向投资人的 AI 创业项目路演 PPT"
- "直接做一份公司内部培训课件,主题是 Agent 工程最佳实践"
- "帮我新建一份季度经营分析汇报 PPT,给管理层看"
- "继续刚才那个 PPT,重点补充权限治理和评估体系"
- "用小浣熊 PPT 帮我做一个 Transformer 入门演讲稿"

## 参数收集策略

**必需的 4 个参数：**
- `prompt` - PPT 主题和要求（1-2000 字）
- `role` - 讲述者身份（如：产品经理、教师、研究人员）
- `scene` - 使用场景（如：产品发布会、学术演讲、内部培训）
- `audience` - 目标受众（如：投资人、家长、公司内部）

**智能推断策略：**
1. 从用户原话中自动推断 role/scene/audience
2. 无法确定时，用一句话问用户并给出 2-3 个选项
3. 优先使用枚举值（见 references/CHEATSHEET.md），用户表达不在枚举内时直接用原始输入

**示例对话：**
```
用户："帮我做一份AI编程工具对比的PPT"
助手：你打算以什么身份来讲？（研究人员 / 产品经理 / 培训师）
用户："研究人员"
助手：在什么场合使用？（学术演讲 / 内部分享 / 客户演示）
用户："内部分享"
助手：给谁看？（公司内部 / 技术团队 / 管理层）
用户："技术团队"
助手：好的，开始生成...
```

## 标准工作流

### 步骤 1：检查环境
```bash
source ~/.zshrc && CLEAN_TOKEN=$(echo "$RACCOON_API_TOKEN" | tr -d '\n\r') && \
cd ~/.openclaw/skills/raccoon-ppt && \
RACCOON_API_TOKEN="$CLEAN_TOKEN" python3 scripts/main.py auth-check
```

### 步骤 2：创建 PPT 任务
```bash
source ~/.zshrc && CLEAN_TOKEN=$(echo "$RACCOON_API_TOKEN" | tr -d '\n\r') && \
cd ~/.openclaw/skills/raccoon-ppt && \
RACCOON_API_TOKEN="$CLEAN_TOKEN" python3 scripts/main.py generate \
  --prompt "帮我做一份AI Agent在企业落地实践的培训PPT" \
  --role "培训师" \
  --scene "培训教学" \
  --audience "公司内部（上级/同事/下属）" \
  --wait-mode short
```

**重要说明：**
- 接口响应需要 **2-3 分钟**（正常特性，不是超时）
- 使用 `--wait-mode short` 前台等待约 1 分钟后返回
- 任务提交成功后告知用户："任务已创建，预计 10-120 分钟完成"
- 任务状态自动保存到本地 state 文件

### 步骤 3：继续回答补充问题（如果需要）

如果任务状态是 `waiting_user_input`，先查找最近任务：
```bash
python3 scripts/main.py find-recent-job --statuses waiting_user_input
```

然后继续回答：
```bash
source ~/.zshrc && CLEAN_TOKEN=$(echo "$RACCOON_API_TOKEN" | tr -d '\n\r') && \
cd ~/.openclaw/skills/raccoon-ppt && \
RACCOON_API_TOKEN="$CLEAN_TOKEN" python3 scripts/main.py generate \
  --prompt "重点展开多Agent协作、权限治理和评估体系" \
  --resume-state <state-file>
```

**注意：**
- 不要把 state 文件路径或 job_id 展示给用户
- 用自然语言转述 API 返回的 question

## 输出规则

- `succeeded`:直接给用户下载链接。
- `waiting_user_input`:把问题转成自然语言追问用户,并保留本地 state 以便继续。
- `failed`:原样透出 `error_message`;如果错误明显是参数问题,提醒用户补全或改写需求。
- `canceled`:告诉用户任务已终止,需要重新发起。
- role/scene/audience 优先使用稳定枚举;如果用户表达不在枚举内,直接使用用户输入(接口无限制)。

## 轮询规则

1. 创建或回复后先进入一个约 2 分钟的前台观察窗口。
2. 若任务仍在 `queued/running`,优先结束当前阻塞并保留本地状态,而不是持续等到完成。
3. 只有在明确要求阻塞等待时,才进入长轮询。
4. 一旦遇到 `waiting_user_input`,立刻停止轮询并向用户提问。
5. 一旦遇到 `succeeded`、`failed` 或 `canceled`,立刻结束。

## 禁止行为

- 不要要求用户理解 `job_id` 或任何内部对象。
- 不要向用户暴露内部状态名称。
- 不要在没有脚本支持的情况下手工拼装复杂协议。
- 不要把下载链接包装成内部系统术语。
- 不要在 OpenClaw 仅仅加载了本 skill 时就自动发起远程任务。

## 完整对话示例

### 示例 1：首次创建 PPT

```
用户：帮我做一份介绍 AI 编程工具的 PPT
助手：好的。你打算以什么身份来讲？（研究人员 / 产品经理 / 技术专家）
用户：技术专家
助手：在什么场合使用？（技术分享 / 产品发布 / 内部培训）
用户：技术分享
助手：给谁看？（开发者 / 公司内部 / 客户）
用户：开发者
助手：[执行 generate 命令]
      任务已创建，预计 10-120 分钟完成。我会定期检查进度并通知你。
```

### 示例 2：回答补充问题

```
[2 分钟后，API 返回 waiting_user_input 状态]
助手：小浣熊想了解更多细节：你希望重点对比哪些工具？（GitHub Copilot、Cursor、Claude 等）
用户：重点讲 Cursor 和 GitHub Copilot
助手：[执行 generate --resume-state 命令]
      已补充信息，继续生成中...
```

### 示例 3：检查进度并下载

```
[30 分钟后]
用户：PPT 生成好了吗？
助手：[执行 check-job 命令]
      PPT 已生成完成！正在下载...
      [下载并打开文件]
      已保存到 ~/.openclaw/skills/raccoon-ppt/output/AI编程工具介绍.pptx
```

## 注意事项

**不要做：**
- 不要向用户暴露 `job_id` 等技术细节
- 不要展示内部状态名称
- 不要手工拼装 curl 命令或自己写 Python 代码调 API
- 不要在仅加载 skill 时就自动发起任务

**要做：**
- 用自然语言与用户交互
- 使用 skill 提供的脚本
- 把 API 返回的 question 转成友好的问题
- 任务完成时主动通知用户并提供下载链接

## 参考文档

- 接口详细说明：[references/API_REFERENCE.md](references/API_REFERENCE.md)
- 快速查询枚举值：[references/CHEATSHEET.md](references/CHEATSHEET.md)

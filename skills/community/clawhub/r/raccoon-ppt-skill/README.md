# 小浣熊 PPT 技能 (Raccoon PPT Skill)

> 为 OpenClaw 设计的远程 PPT 生成技能，主要用于“用户一句话新建一整份 PPT”，并支持继续已有任务或查询结果。

## 核心特性

- 一句话新建一整份 PPT
- 自动收集最小必要字段：`prompt`、`role`、`scene`、`audience`
- 自动轮询任务状态，无需用户反复追问进度
- 支持服务端补充提问并继续任务
- 成功后直接返回最终 PPT 下载链接
- 对用户隐藏 `job_id` 等内部实现细节

## 面向 OpenClaw 的设计目标

这个 skill 的目标不是让用户理解底层 PPT 编排流程，而是让 OpenClaw 在识别到“用户要新建一整份 PPT”时，自动进入一个稳定的任务工作流：

1. 从用户自然语言中提取或追问最小输入
2. 调用 PPT OpenAPI 创建任务
3. 自动轮询
4. 如遇补充问题，继续向用户追问
5. 返回最终下载链接或失败原因

OpenClaw 侧的关键触发依赖主要来自 `SKILL.md` 中的 `name`、`description` 和 `metadata.clawdbot`。

## 环境变量

执行前需要设置：

```bash
export RACCOON_API_TOKEN="your-token"
```

可选设置（默认为 https://xiaohuanxiong.com）：

```bash
export RACCOON_API_HOST="https://your-custom-host"
```

校验方式：

```bash
python3 scripts/main.py auth-check
```

## 快速开始（OpenClaw 使用）

### 1. 创建一个 PPT 任务

```bash
python3 scripts/main.py generate \
  --prompt “帮我生成一份 AI Agent 在企业落地实践的培训 PPT” \
  --role “培训师” \
  --scene “培训教学” \
  --audience “公司内部（上级/同事/下属）”
```

默认使用 `--wait-mode short`，前台观察约 2 分钟后返回。任务状态保存到 `./output/jobs/{job_id}.json`。

### 2. 继续回答补充问题

先查找最近的待回复任务：
```bash
python3 scripts/main.py find-recent-job --statuses waiting_user_input
```

然后继续：
```bash
python3 scripts/main.py generate \
  --prompt “重点展开多 Agent 协作、权限治理和评估体系” \
  --resume-state <返回的state_path>
```

### 3. 查看任务列表和进度

```bash
# 查看所有任务
python3 scripts/main.py list-jobs

# 查看单个任务状态
python3 scripts/main.py check-job --state-path <state_path>
```

## 调试命令（可选）

```bash
python3 scripts/main.py create-job \
  --prompt "帮我做一份 Transformer 发展历程 PPT" \
  --role "研究人员" \
  --scene "培训教学" \
  --audience "大众群体"

python3 scripts/main.py poll-job --job-id job_xxx

python3 scripts/main.py reply-job --job-id job_xxx --answer "重点介绍自注意力机制、BERT 和 GPT"

python3 scripts/main.py list-jobs

python3 scripts/main.py check-job --state-path ./output/jobs/job_xxx.json

python3 scripts/main.py find-recent-job --statuses queued,running,waiting_user_input
```

## 推荐的 OpenClaw 触发话术

下面这些请求应该能稳定触发本 skill：

- “帮我生成一份给投资人的 AI 创业项目路演 PPT”
- “直接做一个公司内部培训课件，主题是 Agent 工程最佳实践”
- “帮我新建一份工作汇报 PPT，汇报过去一季度的模型平台建设进展”
- “我想做一份工作汇报 PPT，汇报过去一季度的模型平台建设进展”
- “继续刚才那个 PPT，我的补充是重点讲多 Agent 协作”
- “用小浣熊 PPT 帮我生成一个面向学生的 Transformer 入门演讲稿 PPT”

下面这些请求不应该直接触发本 skill：

- “帮我润色这一页 PPT 的标题和 bullet”
- “我已经有 PPT 了，帮我把第 3 页改得更像老板汇报”
- “给我几个年终汇报的目录思路”
- “把这段项目介绍改成更适合汇报的口语稿”
- “我想先讨论一下这份汇报该怎么讲”

## 输入模型

最小输入字段：

- `prompt`: 用户要做什么 PPT
- `role`: 讲述者身份
- `scene`: 使用场景
- `audience`: 目标受众

推荐策略：

- 能推断的直接推断
- 缺失的逐项追问
- 不一次问太多
- 优先套用已有稳定枚举
- 实在不完全匹配时，先选最接近的已有分类
- 仍然无法直接匹配时，继续通过前置对话收敛到最接近的稳定分类
- 如需保留额外语义，把补充说明吸收到 `prompt`

## 当前状态机

```text
collect_inputs
  -> create_job
    -> queued/running -> poll
    -> waiting_user_input -> ask_user -> reply_job -> poll
    -> failed -> end_with_error
    -> canceled -> end
    -> succeeded -> return_download_url
```

## 当前接口

```text
POST /api/open/office/v2/ppt_jobs
GET  /api/open/office/v2/ppt_jobs/{job_id}
POST /api/open/office/v2/ppt_jobs/{job_id}/reply
```

鉴权：

```text
Authorization: Bearer $RACCOON_API_TOKEN
```

## 当前限制

- 还没有做真实环境的端到端联调
- 目前只实现最小闭环，不包含结构化 `*_other_detail`
- 当前脚本已支持任务续跑，但”从自然语言自动推断 role/scene/audience”仍主要依赖宿主模型，不在脚本里做复杂规则解析
- 当前版本不再默认生成新的内部分类值，未匹配稳定枚举时应先继续前置收集
- “任务已受理后保留本地索引并稍后查看”的模式已实现，但还没用真实长耗时任务验证

## 长任务建议

- 当前 PPT 任务从创建到可下载通常需要 30 分钟到 2 小时。
- 但创建或回复后的前置处理通常最多约 2 分钟，因此更适合采用“前台观察约 2 分钟 + 本地留存任务记录 + 用户稍后回来查看”的模式。
- 当前脚本会保留本地任务索引，方便后续继续查看，不需要把内部 `job_id` 直接暴露给终端用户。
- 如果服务端返回“当前有多个任务执行中”的业务错误，应直接提示用户稍后再试，不要继续重复建单。
- 当用户回来问“我的 PPT 好了吗”时，优先从本地任务索引里找最近未完成任务，再继续查询。

## 参考文档

- [SKILL.md](./SKILL.md) - Skill 定义和使用规则
- [references/API_REFERENCE.md](./references/API_REFERENCE.md) - 完整 API 文档
- [references/CHEATSHEET.md](./references/CHEATSHEET.md) - API 快速参考

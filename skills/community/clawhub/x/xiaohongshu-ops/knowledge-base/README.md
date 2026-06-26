# XHS Knowledge Base

这个目录是小红书运营知识库的总览入口。

目标：让 agent 在开始任务前先看一眼“我们已经知道什么”，结束任务后把新的分析结果和动作沉淀到固定位置，方便后续检索和复用。

## 1. 目录结构

```text
knowledge-base/
  README.md              # 总览入口，保留当前重点和搜索指引
  accounts/              # 账号定位、账号体检、竞品账号分析
  topics/                # 选题、争议点、标题骨架、可发方向
  patterns/              # 爆款结构、封面模板、互动钩子、复用规则
  actions/               # 发布、回复、抓取、下载、复刻等动作记录
  reviews/               # 复盘、有效/无效原因、下次调整建议
```

## 2. 使用规则

- 开始任务前：先读本文件，再按目录搜索最相关的记录。
- 任务进行中：遇到新的高价值结论，可以先记临时摘要，任务结束后整理成独立记录。
- 任务结束后：至少补一条结构化记录到对应目录。
- 这个目录下的细分记录默认只做本地沉淀，不提交到 git；`.gitignore` 已经处理。

## 3. 文件命名建议

为了方便 agentic search，细分记录建议按“日期 + brief”命名，brief 用 2-6 个高信息量词概括主题：

- `accounts/2026-03-19-drama-watch-positioning.md`
- `topics/2026-03-19-taipingnian-argument-hooks.md`
- `patterns/2026-03-19-confirmation-comment-hook.md`
- `actions/2026-03-19-publish-taipingnian-note.md`
- `reviews/2026-03-19-reply-flow-retrospective.md`

规则：

- 日期放最前面，方便按时间排序
- brief 尽量短，但要能表达主题、动作或结论
- 一份文件只记录一个核心结论或一次完整动作

## 4. 推荐检索顺序

1. 先看本文件的“当前重点”和“固定索引”
2. 再按任务类型去对应目录搜索
3. 优先看最近 7-14 天的同类记录
4. 最后再看更早的历史记录

## 5. 当前重点

- 暂无固定重点，可在后续任务中持续补充。

建议长期保留：

- 当前账号定位摘要
- 最近验证有效的 3-5 个 pattern
- 最近 7 天的高价值复盘入口

## 6. 固定索引

- 账号分析：`knowledge-base/accounts/`
- 选题灵感：`knowledge-base/topics/`
- 可复用模式：`knowledge-base/patterns/`
- 动作记录：`knowledge-base/actions/`
- 结果复盘：`knowledge-base/reviews/`

## 7. 写入最小标准

每条细分记录建议至少包含：

- 一句话结论
- 证据或来源
- 可复用点
- 风险或边界
- 下一步动作

如果来不及写完整记录，先把这 5 项写进去，后续再补充。

## 8. 待整理

- 暂无。

当细分目录暂时不可写、但总览入口可写时，先把临时摘要记在这里，后续再拆成独立记录。

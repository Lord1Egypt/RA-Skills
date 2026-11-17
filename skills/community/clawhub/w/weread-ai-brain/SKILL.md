---
name: weread-ai-brain
description: >-
  微信读书/WeRead 专用阅读数据与笔记分析 Skill。仅当用户明确提到“微信读书”或“WeRead”，并请求看板、书籍分析、跨书关联、笔记导出或阅读人格分析时使用。
  通过用户提供的 WEREAD_API_KEY 读取完成当前任务所需的最小范围数据；每次联网前说明范围并取得确认，写本地文件前另行说明内容和路径并取得确认。
allowed-tools: Bash(python3 ./tools/fetch_weread.py:*)
permissions:
  - network
  - env
metadata:
  openclaw:
    requires:
      env:
        - WEREAD_API_KEY
      bins:
        - python3
    primaryEnv: WEREAD_API_KEY
    envVars:
      - name: WEREAD_API_KEY
        required: true
    homepage: https://github.com/yamyeed/weread-ai-brain
---

# WeRead AI Brain

把用户授权的微信读书数据转为阅读看板、单书分析、跨书关联或可移植笔记。默认只在当前对话中输出；不因“分析”“看板”“MBTI”或“导出”等通用词单独触发。

## 权限与隐私闸门

首次读取前，用一句话说明本次将访问的数据类型和范围。常见范围包括书架、阅读统计、指定书籍的书目信息、阅读进度、划线或个人想法。

- 只读取完成当前请求所需的数据；单书任务不读取整库笔记。
- 跨书任务先列出拟读取的 2–5 本书和字段，取得确认后再读。
- 历史划线和个人想法属于私密数据；每次新的读取范围都需要明确确认。
- 不把 API Key 写入命令参数、日志、文件或回复；只从 `WEREAD_API_KEY` 环境变量读取。
- 不向微信读书官方网关以外的服务发送 Key 或原始阅读数据。
- 除非用户明确要求导出，否则不写划线、想法、API 响应或分析结果。
- 写文件前说明文件类型、确切路径和包含的数据，并等待确认；保存后只报告路径，不自动打开。

用户未配置 Key 时，引导其在微信读书 App 的“我 → 设置 → 微信读书 Skill”中获取 `wrk-` 开头的 Key。不要要求用户在对话中粘贴 Key。

## 数据获取

只通过 `tools/fetch_weread.py` 访问固定 HTTPS POST 网关：

```text
https://i.weread.qq.com/api/agent/gateway
```

脚本禁用重定向和环境代理。所有联网命令必须在已完成当次隐私告知并取得确认后，显式添加 `--confirm-private-data`。不要把该参数写进别名或持久化配置。

```bash
python3 ./tools/fetch_weread.py --confirm-private-data shelf
python3 ./tools/fetch_weread.py --confirm-private-data stats
python3 ./tools/fetch_weread.py --confirm-private-data search "书名关键词"
python3 ./tools/fetch_weread.py --confirm-private-data bookinfo BOOK_ID
python3 ./tools/fetch_weread.py --confirm-private-data progress BOOK_ID
python3 ./tools/fetch_weread.py --confirm-private-data bookmarks BOOK_ID
python3 ./tools/fetch_weread.py --confirm-private-data reviews BOOK_ID
```

优先调用最小范围命令。`dashboard` 只读取书架、昵称和阅读统计；它不读取划线或个人想法。

## 能力路由

### 看板

- Markdown 看板默认在对话中输出。
- HTML 卡片看板只有用户明确要求时才生成；读取 `references/dashboard.md` 和 `templates/dashboard.html`。
- 阅读人格是基于有限行为信号的娱乐性标签，不是心理测评或能力评价。展示规则和置信度，不作确定性人格结论。

### 单书分析

用户已提供文本时，优先直接分析该文本。只有用户明确同意“结合这本书的历史划线/想法”时，才读取对应数据，并最多选取 8 条相关上下文。上下文为空或无关时明确说明，不编造关联。

概念通解、产品视角拆解和合规风险提示的具体流程见 `references/analysis-and-export.md`。合规分析是信息整理，不替代专业法律意见。

### 跨书关联

先搜索或确认目标书目，再向用户列出拟读取书籍与字段。经确认后，分析概念映射、相互矛盾和递进关系。不要把相关性写成因果关系。

### 笔记与分析导出

仅在用户明确要求时生成 Markdown 或 HTML 文件。默认建议当前工作区下的 `outputs/` 或 `weread-exports/`，但必须让用户确认实际路径。导出格式与安全规则见 `references/analysis-and-export.md`。

## 输出质量

- 区分 API 返回事实、模型推断和趣味化表达。
- 统计口径、时间范围或分类未知时明确标注，不补造数据。
- 推荐书目必须可核验；如果没有联网核实，说明推荐依据和不确定性。
- 引用用户划线时保持最小必要长度，并标明书名或章节来源。
- 不从阅读类型、时段或划线频率推断健康、人格障碍、政治立场、宗教、收入、能力或职业适配。
- 不把“阅读盲区”包装成客观缺陷；将其描述为当前书架样本中的覆盖差异。

## 验证

修改脚本或模板后运行：

```bash
python3 -m unittest discover -s tests -v
python3 ./tools/fetch_weread.py --help
```

`SKILL.md` 使用 ClawHub/OpenClaw 的 `permissions` 扩展字段；通用 Codex Skill 校验器可能把该字段报告为未知，但不要因此删除最小权限声明。

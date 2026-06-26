---
name: yuque
description: 通过语雀开放API对语雀(Yuque)文档与知识库执行端到端自动化操作 —— 创建/读取/更新/删除文档、管理知识库目录(TOC)、调整Markdown排版(字号、颜色、标题、表格、代码块、提示框)、全文搜索及批量导入导出。任何用户提到"语雀""yuque""知识库""文档目录""TOC""语雀文档格式调整""语雀批量导出"或上传语雀导出的Markdown文件,即使没有显式说"使用skill",也应主动调用此skill。
license: Complete terms in LICENSE.txt
---

# 语雀(Yuque)自动化Skill

把语雀的开放API包装成一组开箱即用的Python脚本,让Openclaw / Claude Code能够像操作本地文件那样操作云端语雀文档。

## 何时用本Skill

- 用户提到"语雀"或"yuque"——无论是想"在语雀里建一篇文章"、"把这份Markdown发到我的语雀知识库"、"调整语雀目录结构"还是"批量导出我语雀小记里的文档"。
- 用户描述了语雀文档但没点名API:例如"帮我把这份会议纪要按一级标题分章后发布"或"把这30篇文档按主题重排目录",仍应优先考虑本skill。
- 用户上传了`.md`并要求"同步到语雀"或上传了从语雀导出的Markdown想做处理。
- 用户问"我的语雀里面有哪些文档/知识库"或"按关键词搜一下我的语雀"。

不适用场景:用户只是问语雀这个产品本身的功能或定价(直接回答即可,无需调用脚本)。

## 第0步:确认凭证

语雀API所有写操作都需要 `X-Auth-Token`。本skill支持两种凭证来源,优先级 **环境变量 > 配置文件**:

1. 环境变量 `YUQUE_TOKEN`(推荐,长期任务可在Openclaw启动shell时 `export`)。
2. 配置文件 `~/.yuque/config.json`,格式:
   ```json
   {"token": "xxxxxxxxxxxxxxxx", "base_url": "https://www.yuque.com/api/v2"}
   ```
   私有部署的语雀专有云请把 `base_url` 改成自己的域名。

调用任何脚本前先执行 `python scripts/yuque_client.py whoami` 自检,如果返回当前用户信息就说明凭证可用;若返回401请引导用户去 [https://www.yuque.com/settings/tokens](https://www.yuque.com/settings/tokens) 创建Token,再决定是写入环境变量还是配置文件。

## 第1步:用脚本完成具体操作

每个脚本都是命令行入口,统一返回JSON到stdout(便于后续pipeline处理)。在Openclaw中通过 `python scripts/<name>.py <subcmd> [args]` 调用即可。

### 文档与知识库 CRUD —— `scripts/docs.py`

```
docs.py list-repos [--user <login>] [--group <group>]
docs.py list-docs <namespace>                     # 列知识库下的全部文档
docs.py get <namespace> <slug>                    # 读取单篇正文(Markdown)
docs.py create <namespace> --title <t> [--slug <s>] [--body-file <path>] [--public 0|1]
docs.py update <namespace> <slug_or_id> [--title ...] [--body-file ...] [--public ...]
docs.py delete <namespace> <slug_or_id>
docs.py copy   <src_ns> <slug> --to <dst_ns>      # 跨知识库克隆
```

`namespace` 形如 `user_login/repo_slug`。如果用户只给了知识库名而没给slug,先用 `list-repos` 找到对应namespace。

### 目录(TOC)管理 —— `scripts/toc.py`

```
toc.py show     <namespace>                        # 树形输出当前TOC
toc.py add-doc  <namespace> --doc-id <id> [--parent-uuid <uuid>] [--title ...]
toc.py add-title <namespace> --title <章节名> [--parent-uuid ...]   # 纯目录占位节点
toc.py move     <namespace> --uuid <uuid> --target <uuid> --mode {before|after|inside}
toc.py rename   <namespace> --uuid <uuid> --title <新名>
toc.py remove   <namespace> --uuid <uuid> [--keep-doc]              # 默认连文档一起移除
```

TOC的节点uuid通过`show`拿到。任何批量重排都建议先 `toc.py show > tmp.json`,在内存里改完再用 `toc.py apply tmp.json` 一次提交,避免中间态导致目录错乱(详见 `references/toc_operations.md`)。

### Markdown格式化辅助 —— `scripts/format_helpers.py`

语雀本质上吃Markdown,但额外支持一些显示控件(`<font color>`、`color()`、警示框、思维导图等)。本脚本提供以下生成器,直接 import 调用:

```python
from scripts.format_helpers import (
    heading,         # heading("标题", level=2) -> "## 标题"
    colored,         # colored("重要", "#FF0000") -> '<font color="#FF0000">重要</font>'
    sized,           # sized("大字", "20px")
    styled,          # styled("文字", color="#FF0000", size="18px", bold=True) -> <span style="...">
    callout,         # callout("注意", kind="warning") -> 语雀提示框
    table,           # table(headers, rows) -> Markdown表格
    code_block,      # code_block(src, lang="python")
    toc_anchor,      # 在文档内插入#anchor
    math_block,      # 行间LaTeX
    sanitize,        # sanitize(body) -> 清洗语雀不支持的危险HTML(422前调用)
)
```

详细可用值与转义规则参见 `references/markdown_format.md`。

### 搜索 —— `scripts/search.py`

```
search.py docs <keyword> [--scope user|group|repo] [--namespace ...] [--type doc|book]
search.py find-by-title <namespace> <substring>    # 本地索引精确匹配
```

### 批量操作 —— `scripts/batch.py`

```
batch.py export <namespace> --out-dir ./dump        # 把整本知识库存成Markdown
batch.py import --from-dir ./dump --to <namespace>  # 反向同步,文件名即slug
batch.py replace <namespace> --pattern <re> --replacement <s> [--dry-run]
```

## 第2步:把结果回报给用户

脚本默认输出JSON。把JSON里的关键字段(文档url、id、title、count)抽出来,用人话告诉用户做了什么:

> 已在「我的工作笔记」知识库下创建《Q4复盘》,链接: https://www.yuque.com/<login>/<book>/<slug>。共写入 8 段、2 张表格。

如果操作影响多篇文档(批量),给出受影响数量与一份示例链接,而不是把每条都列出来。

## 错误处理约定

- 401:凭证失效 → 提示重新生成Token。
- 404:namespace或slug错 → 自动调用 `docs.py list-repos / list-docs` 确认存在性后再决定是否重试。
- 429:被限流 → 脚本内置指数退避(`yuque_client.py` 中 `_request` 实现),不需要在外层处理。
- 422:正文里含语雀不支持的HTML → 调用 `format_helpers.sanitize(body)` 清洗一遍再重提交。

## 进一步阅读

- `references/api_reference.md` —— 语雀v2 API所有已封装端点的速查表
- `references/markdown_format.md` —— 语雀Markdown扩展语法(颜色/字号/警示框/公式/思维导图)
- `references/toc_operations.md` —— TOC的action/target_type字段细节及批量重排范式
- `README.md` —— 在Openclaw中安装与部署本skill的步骤

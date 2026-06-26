# TOC(目录)操作详解

语雀目录由一系列节点(node)组成,每个节点记录:

```json
{
  "uuid": "abc123",
  "type": "DOC | TITLE | LINK",
  "title": "节标题",
  "url": "/login/repo/slug",
  "doc_id": 12345,
  "parent_uuid": null,
  "child_uuid": "...",
  "sibling_uuid": "...",
  "depth": 0
}
```

`/repos/:namespace/toc` GET返回的是一个 **扁平列表**,真正的层级关系靠 `parent_uuid` 与 `prev_uuid / sibling_uuid` 推。`toc.py show` 内置了把扁平表重组成树的逻辑。

## action 速查

PUT `/repos/:namespace/toc` 接受一个 action 对象。

| action | 必填 | 可选 | 说明 |
|---|---|---|---|
| `appendNode` | `type`,`title`(TITLE/LINK)或 `doc_ids`(DOC) | `target_uuid`, `action_mode` | 在目标节点子级或同级追加 |
| `prependNode` | 同上 | 同上 | 同上,但插到最前 |
| `editNode` | `node_uuid` | `title`, `url`, `visible` | 改标题/可见性等 |
| `removeNode` | `node_uuid` | `delete_doc`(默认true) | 从目录移除节点 |
| `moveNode` | `node_uuid`, `target_uuid` | `action_mode` | 移到目标节点 |

`action_mode` 可选值:

- `child` — 作为目标节点的最后一个子节点(等同 inside)
- `sibling` — 作为目标节点的下一个兄弟
- `prevSibling` — 目标的上一个兄弟(用于 before)
- `nextSibling` — 目标的下一个兄弟(用于 after)

## 典型场景

### 场景1:把一篇已存在的文档挂到目录下某个章节

```bash
# 1. 找父节点 uuid
python scripts/toc.py show <ns> --json | jq '.[] | select(.title=="第三章")'

# 2. 挂载文档(doc_id 来自 list-docs 的 id 字段)
python scripts/toc.py add-doc <ns> --doc-id 6789 --parent-uuid abc123 \
        --title "3.1 概述"
```

### 场景2:把目录改成"前言/正文/附录"三层

先用一份action列表描述最终态,再批量apply:

```json
[
  {"action": "appendNode", "type": "TITLE", "title": "前言"},
  {"action": "appendNode", "type": "TITLE", "title": "正文",
   "action_mode": "sibling"},
  {"action": "appendNode", "type": "TITLE", "title": "附录",
   "action_mode": "sibling"}
]
```

```bash
python scripts/toc.py apply <ns> reorganize.json --stop-on-error
```

### 场景3:把零散的100篇文档按标题前缀重新分组

```python
# 先 export 元数据
import subprocess, json, re, collections
docs = json.loads(subprocess.check_output(
    ["python", "scripts/docs.py", "list-docs", "user/notes"]))

groups = collections.defaultdict(list)
for d in docs:
    m = re.match(r"^\[(\w+)\]", d["title"])
    if m:
        groups[m.group(1)].append(d)

# 再针对每组生成 add-title + add-doc 的 action 列表
```

## 防止误删

`removeNode` 默认 `delete_doc=true`,会把底层文档一同删除。本skill的 `toc.py remove` 默认走这个语义,但提供 `--keep-doc` 仅从目录摘下文档。批量重排前推荐:

1. 先 `toc.py show <ns> --json > backup.json` 备份
2. dry-run:把动作列表打印出来人工审一遍
3. `toc.py apply ... --stop-on-error` 出错立即停下避免半状态

## 已知限制

- 一次PUT只接受一个action;批量时 `apply` 内部串行调用,失败可能导致部分提交,所以备份很重要。
- 公开/私密属性属于文档而非节点,`editNode` 不能改 `public`,要走 `docs.py update`。
- 一份知识库的TOC上限约 1500 节点,超量会 422,需要拆分为多本知识库。

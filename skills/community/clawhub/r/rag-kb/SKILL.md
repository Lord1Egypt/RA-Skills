---
name: bailian_faiss_kb
description: 使用 Python、FAISS、BM25、阿里云百炼 text-embedding-v4 与可选的 qwen3-rerank，维护基于文件目录的本地知识库；适用于在 OpenClaw 预先抽取文本后，遍历 chunks 与 T2Q 建立索引，以及对指定知识库或全部知识库做综合、语义或关键词查询。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":"BAILIAN_SK"}}
---

# 基于阿里云百炼、FAISS 和 BM25 的知识库

这个 skill 用于配合 OpenClaw 自己的模型，维护目录化知识库。OpenClaw 负责从原始文件中抽取文本，并生成摘要、做语义切片、生成 T2Q；Python 只负责消费已经准备好的文本文件，建立语义与 BM25 索引，并执行查询。

## 适用场景

- 消费 OpenClaw 已经抽取好的文本文件
- 遍历某个知识库目录下的 `chunks/` 和 `t2q/` 建立或更新索引
- 对整个知识库执行重建索引，同时重建语义与 BM25 工件
- 在原始文档目录被删除后，从知识库级索引中移除对应数据
- 对指定知识库增加或删除保护词，并离线刷新 BM25 工件
- 对指定知识库做综合查询，默认同时使用语义与 BM25
- 对指定知识库显式做语义查询
- 对指定知识库显式做关键词查询
- 对全部知识库做综合、语义或关键词查询

## 运行规则

- 先安装依赖：`python3 -m pip install -r {baseDir}/requirements.txt`
- 使用 Python `3.10+`
- 百炼密钥推荐使用环境变量 `BAILIAN_SK`；脚本同时兼容历史变量名 `BAILIAN-SK`
- 向量模型固定为 `text-embedding-v4`
- 向量维度固定为 `1024`
- BM25 固定使用本地倒排索引和 `jieba` 分词
- 每个知识库的保护词单独存放在 `/var/openclaw-kb/{kb}/protected_terms.json`
- 可选重排模型固定为 `qwen3-rerank`
- 查询默认模式固定为 `hybrid`
- OpenClaw 必须先把原始文件抽取为文本，再进入这个 skill
- `summary` 必须是单行纯文本，保存为 `summary.txt`
- T2Q 只作为语义召回代理，最终查询结果只能返回真实 chunk
- BM25 只索引真实 `chunk`，不索引 `t2q`

## 安全边界

- 这个 skill 不执行 shell、不下载远程脚本、不启动后台服务、不监听端口
- Python 只读写知识库目录下的本地文件，以及脚本显式传入的输入/输出路径
- `index` 需要联网生成 embedding；`query --retrieval-mode semantic|hybrid` 需要联网生成查询 embedding；任意模式启用 `--rerank` 时需要联网做重排；且只会向阿里云百炼官方接口发起 HTTPS 请求：
  - `https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`
  - `https://dashscope.aliyuncs.com/compatible-api/v1/reranks`
- 只有百炼密钥会被读取并放入对应请求的 `Authorization` 请求头；脚本不会收集或上传其他环境变量
- `doctor` 与 `query --retrieval-mode keyword` 不依赖网络，也不会读取百炼密钥

## 先读路径规范

每次新增、抽取文本、摘要、切片、T2Q、索引、删除之前，必须先读 [references/layout.md](./references/layout.md)。

主文档不再重复展开所有命名细节。执行时以 `layout.md` 为准。

## 再读内容格式规范

每次生成 `summary.txt`、`chunks/*.md`、`t2q/*.md` 之前，必须再读 [references/content-rules.md](./references/content-rules.md)。

主文档不再重复展开这三类内容的细节。执行时以 `content-rules.md` 为准。

## 路径最小约束

知识库根目录默认是 `/var/openclaw-kb`，但可通过 `--root-dir` 覆盖。

每个知识库目录下的保护词文件固定为：

```text
/var/openclaw-kb/{kb}/protected_terms.json
```

每次进入这个 skill 前，必须先算出这三个值：

- `kb`：知识库名，例如 `regulation`
- `ts`：上传时间戳，格式固定为 `yyyyMMddhhmm`
- `safe_name`：去掉危险字符后的文件基础名

只有先得到这三个值，后面的文本保存、摘要、切片、T2Q、索引才能继续。

- 当前文档目录固定为：

```text
/var/openclaw-kb/{kb}/{ts}-{safe_name}
```

- OpenClaw 抽取出的文本文件、`summary.txt`、`chunks/`、`t2q/` 都必须放在这个目录下

## 职责拆分

### 1. 文件保存

这是 OpenClaw 的前置步骤，不调用 Python。

OpenClaw 需要：

- 先按 [references/layout.md](./references/layout.md) 算出目标目录和目标文件名
- 创建目录 `/var/openclaw-kb/{kb}/{ts}-{safe_name}/`
- 先从原始文件中抽取文本
- 将抽取结果保存为 `/var/openclaw-kb/{kb}/{ts}-{safe_name}/{safe_name}.md`

### 2. 文本前置条件

这个 skill 不负责文件转文本。

进入摘要、切片、T2Q、索引之前，OpenClaw 必须已经把原始文件抽取成文本文件，推荐保存为：

```text
/var/openclaw-kb/{kb}/{ts}-{safe_name}/{safe_name}.md
```

也兼容：

```text
/var/openclaw-kb/{kb}/{ts}-{safe_name}/{safe_name}.txt
```

### 3. 摘要

这是纯 skill 步骤，不调用 Python。

OpenClaw 读取已经抽取好的文本文件后，需要：

- 先读 [references/content-rules.md](./references/content-rules.md)
- 按规则生成 `summary.txt`
- 保存到当前文档目录里的 `summary.txt`

### 4. 切片

这是纯 skill 步骤，不调用 Python。

OpenClaw 读取已经抽取好的文本文件后，需要：

- 按语义切分正文
- 每个切片输出为单独的 Markdown 文件
- 先读 [references/content-rules.md](./references/content-rules.md)
- 文件名和保存目录必须遵守 [references/layout.md](./references/layout.md)

注意：

- 只有在文本文件已经准备好的前提下，才进入这个 skill 的后续流程
- 这个 skill 自身不处理 `doc/docx/pdf/ppt/xls/xlsx` 到文本的转换

### 5. T2Q

这是纯 skill 步骤，不调用 Python。

OpenClaw 需要：

- 针对每个 chunk 生成问题
- 每个问题单独存一个 Markdown 文件
- 先读 [references/content-rules.md](./references/content-rules.md)
- 文件名和保存目录必须遵守 [references/layout.md](./references/layout.md)

### 6. 建立索引

这一步调用 Python。它会遍历一个文档目录下的 `chunks/` 和 `t2q/`，建立语义索引和 BM25 索引。

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py index \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --doc-dir /var/openclaw-kb/regulation/{ts}-xx \
  --topk 10 \
  --topN 10
```

行为：

- 遍历 `chunks/*.md`
- 遍历 `t2q/*.md`
- 用 `text-embedding-v4` 生成 1024 维向量
- 将 chunk 与 T2Q 代理一起写入 `vectors.jsonl`
- 更新 `index.faiss`
- 仅基于真实 `chunk` 构建 BM25 倒排索引并写入 `bm25.json`
- 更新 `manifest.json`
- 将 `topk` 与 `topN` 写入知识库配置
- 构建 BM25 时读取当前知识库目录下的 `protected_terms.json`

### 6.1 重建知识库索引

这一步调用 Python。它会扫描某个知识库目录下的全部文档目录，重新生成整个知识库的语义索引和 BM25 索引。

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py rebuild \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --topk 10 \
  --topN 10
```

行为：

- 遍历 `/var/openclaw-kb/{kb}/` 下所有合法文档目录
- 读取每个文档目录中的 `chunks/*.md`
- 读取每个文档目录中的 `t2q/*.md`
- 重新写出完整的 `vectors.jsonl`
- 重新写出完整的 `index.faiss`
- 重新写出完整的 `bm25.json`
- 重新写出完整的 `manifest.json`
- 这个入口用于“全量重建”，保证语义检索和关键词检索始终一起重建
- 重建 BM25 时会读取当前知识库目录下的 `protected_terms.json`

### 7. 删除

删除分成两步，而且顺序固定为先删索引，再删文件：

1. 先调 Python 删除知识库索引中的对应数据并持久化：

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py delete \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --doc-id {ts}-xx
```

行为：

- 从 `vectors.jsonl` 中删除该文档对应的 chunk 和 T2Q 向量记录
- 重写 `index.faiss`
- 重写 `bm25.json`
- 重写 `manifest.json`

2. 再由 OpenClaw 删除整个文档目录：

```text
/var/openclaw-kb/regulation/{ts}-xx
```

### 7.1 增加保护词

这一步调用 Python。它会把保护词写入知识库目录下的 `protected_terms.json`，然后离线刷新 `bm25.json` 与 `manifest.json`。

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py protect-add \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --term 测试环境权限 \
  --term OpenClaw
```

行为：

- 保护词写入 `/var/openclaw-kb/{kb}/protected_terms.json`
- 仅更新当前知识库
- 基于现有 `vectors.jsonl` 离线重建 `bm25.json`
- 刷新 `manifest.json`
- 不重建向量，不重写 `index.faiss`

### 7.2 删除保护词

这一步调用 Python。它会从知识库目录下的 `protected_terms.json` 删除指定词条，然后离线刷新 `bm25.json` 与 `manifest.json`。

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py protect-delete \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --term 测试环境权限
```

行为：

- 从 `/var/openclaw-kb/{kb}/protected_terms.json` 删除指定保护词
- 仅更新当前知识库
- 基于现有 `vectors.jsonl` 离线重建 `bm25.json`
- 刷新 `manifest.json`
- 不重建向量，不重写 `index.faiss`

### 8. 查询

这一步调用 Python。

默认综合查询指定知识库：

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py query \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --query "报销审批流程是什么"
```

默认综合查询全部知识库：

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py query \
  --root-dir /var/openclaw-kb \
  --query "报销审批流程是什么"
```

显式只做语义查询：

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py query \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --query "报销审批流程是什么" \
  --retrieval-mode semantic
```

显式只做关键词查询：

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py query \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --query "报销审批流程是什么" \
  --retrieval-mode keyword
```

需要更高精度时，显式启用 rerank：

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py query \
  --root-dir /var/openclaw-kb \
  --kb regulation \
  --query "报销审批流程是什么" \
  --retrieval-mode hybrid \
  --rerank
```

查询规则：

- 若指定 `--kb regulation`，只查询该知识库
- 若未指定 `--kb`，遍历根目录下所有知识库
- 若知识库索引未加载，则从文件中加载
- 若未显式指定 `--retrieval-mode`，默认按 `hybrid` 做综合检索
- `--retrieval-mode semantic` 时，按 FAISS 做语义召回；`chunk` 与 `t2q` 都参与召回，命中 `t2q` 时必须反查回真实 chunk
- `--retrieval-mode keyword` 时，只按 BM25 检索真实 `chunk`；`t2q` 不参与关键词检索
- `--retrieval-mode hybrid` 时，先分别做语义召回和 BM25 召回，再在真实 chunk 级别融合
- 无 rerank 时，先做召回，再按 `topN` 返回
- 有 rerank 时，先做召回与融合，再对真实 chunk 候选做 rerank，返回前 `topN`
- 关键词查询分词会读取当前知识库目录下的 `protected_terms.json`

## 查询输出格式

默认返回 Markdown，按文件分组，每个命中的 chunk 单独成节。

格式固定为：

```md
## xx.docx

- uploaded at {ts}
- summary: 摘要文本
- total chunks: 该文件的切片数量

### Chunk 00001

这里是 chunk 内容

### Chunk 00002

这里是 chunk 内容
```

注意：

- `summary` 来自 `summary.txt`
- 只能返回真实 chunk 内容，不能返回生成的问题文本

## 检查运行环境

```bash
python3 {baseDir}/scripts/bailian_faiss_kb.py doctor \
  --root-dir /var/openclaw-kb
```

## 操作说明

- 这个 skill 不负责替 OpenClaw 生成摘要、切片或 T2Q 的内容，只负责规范这些文件应该长成什么样，以及如何调用 Python
- 如果某个 chunk 文件或 T2Q 文件命名不合法，Python 会拒绝索引
- 如果 `summary.txt` 超过 200 字，Python 会拒绝索引
- 如果要让新建或更新过的文档参与 BM25，必须重新执行 `index`
- 如果只变更保护词，不需要重新做 embedding，可直接执行 `protect-add` 或 `protect-delete`
- 需要更详细的实现说明时，读取 [references/runtime-notes.md](./references/runtime-notes.md)

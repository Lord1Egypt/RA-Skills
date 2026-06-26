# Runtime Notes

## 固定实现

- Python 运行时：`3.10+`
- 向量模型：`text-embedding-v4`
- 向量维度：`1024`
- 可选重排模型：`qwen3-rerank`
- 根目录默认值：`/var/openclaw-kb`
- 默认查询模式：`hybrid`
- 输入前提：OpenClaw 已经把原始文件抽取为文本
- `topk` 与 `topN` 写入知识库自己的 `config.json`

## 目录结构

每个知识库目录位于：

- `/var/openclaw-kb/{kb}`

其中包含：

- `config.json`
- `manifest.json`
- `vectors.jsonl`
- `index.faiss`
- `bm25.json`
- `{ts}-{safe_name}/`

每个文档目录包含：

- OpenClaw 抽取后的 `{safe_name}.md` 或 `{safe_name}.txt`
- `summary.txt`
- `chunks/chunk-00001.md`
- `t2q/00001-q-1.md`

## 索引规则

- `chunks/*.md` 作为真实召回单元
- `t2q/*.md` 作为召回代理单元
- BM25 只索引真实 `chunk`
- 查询命中 `t2q` 时，必须反查到对应 `chunk`
- 最终输出只能返回真实 `chunk`
- `rebuild --kb {kb}` 会全量重建 `vectors.jsonl`、`index.faiss`、`bm25.json` 与 `manifest.json`
- 删除顺序固定为先执行 `delete --doc-id {ts}-{safe_name}`，再删除文档目录本身

## 查询流程

单知识库：

1. 若模式含语义召回，则将问题 embedding 成 1024 维
2. 若模式含语义召回，则查询 FAISS top `topk`
3. 若模式含关键词召回，则对真实 chunk 的 BM25 倒排索引做 top `topk`
4. 若命中 T2Q，则折叠回真实 chunk
5. 若为 `hybrid`，则在 chunk 级别融合语义与 BM25 候选
6. 去重
7. 若启用 `--rerank`，再按 `topN` 重排
8. 返回 Markdown

全知识库：

1. 对每个知识库执行同样的候选召回
2. 合并结果
3. 折叠回真实 chunk
4. 按需要做 hybrid 融合
5. 去重
6. 按需要执行 rerank

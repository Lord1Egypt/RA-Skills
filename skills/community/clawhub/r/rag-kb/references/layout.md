# 路径与命名规则

这份参考文件只说明两件事：

- 文件该存到哪里
- 文件名必须长成什么样

每次新增、抽取文本、摘要、切片、T2Q、索引、删除之前，都先按这里的规则检查一次。

## 先确定 3 个值

继续之前，必须先确定：

- `kb`：知识库名，例如 `regulation`
- `ts`：上传时间戳，格式固定为 `yyyyMMddhhmm`
- `safe_name`：原文件基础名清洗后的结果，不带扩展名

只有这 3 个值确定了，后面的所有路径才是确定的。

## `safe_name` 规则

- 只取原文件基础名，不带扩展名
- 不能安全出现在路径中的字符，一律替换为 `_`
- 连续多个 `_` 合并为一个
- 去掉首尾空格
- 原始扩展名保留，不参与 `safe_name`

示例：

- `xx.docx` -> `safe_name = xx`
- `人事制度(终版).docx` -> `safe_name = 人事制度_终版`
- `abc/def?.pdf` -> `safe_name = abc_def`

## 文档目录名

文档目录名固定为：

```text
{ts}-{safe_name}
```

示例：

- `202604101530-xx`
- `202604101530-人事制度_终版`

## 固定文件名

一个文档目录下，文本资产文件名必须固定，不要自行改写：

- 抽取后的文本：`{safe_name}.md`
- 可兼容的纯文本：`{safe_name}.txt`
- 摘要：`summary.txt`
- chunk：`chunk-00001.md`
- t2q：`00001-q-1.md`

禁止使用这些变体：

- `summary.md`
- `summary.json`
- `chunk1.md`
- `q-1-00001.md`
- `001.md`

## 存放文件夹规则

以知识库 `regulation`、上传时间 `{ts}`、文件名 `xx.docx` 为例，假设 OpenClaw 已将其抽取为 `xx.md`：

```text
/var/openclaw-kb/
  regulation/
    config.json
    index.faiss
    bm25.json
    manifest.json
    vectors.jsonl
    {ts}-xx/
      xx.md
      summary.txt
      chunks/
        chunk-00001.md
        chunk-00002.md
      t2q/
        00001-q-1.md
        00001-q-2.md
```

必须遵守：

- 知识库级文件只能放在 `/var/openclaw-kb/{kb}/`
- 单个文档的所有资产只能放在 `/var/openclaw-kb/{kb}/{ts}-{safe_name}/`
- 不要额外再套一层 `files/`
- 不要把 `summary.txt`、`chunks/`、`t2q/` 放到知识库根目录
- 不要把不同文件的 chunk 混在同一个 `chunks/` 目录下
- 抽取出的文本文件、`summary.txt`、`chunks/`、`t2q/` 必须属于同一个文档目录

简单说：

- KB 级目录只放索引与文档目录
- KB 级索引文件包含 `vectors.jsonl`、`index.faiss`、`bm25.json`、`manifest.json`
- 文档级目录只放当前文件自己的所有产物

## 每一步对应的固定落点

文件保存：

- `/var/openclaw-kb/{kb}/{ts}-{safe_name}/{safe_name}.md`

文本抽取：

- `/var/openclaw-kb/{kb}/{ts}-{safe_name}/{safe_name}.md`

摘要：

- `/var/openclaw-kb/{kb}/{ts}-{safe_name}/summary.txt`

切片：

- `/var/openclaw-kb/{kb}/{ts}-{safe_name}/chunks/chunk-00001.md`

T2Q：

- `/var/openclaw-kb/{kb}/{ts}-{safe_name}/t2q/00001-q-1.md`

删除：

- 先执行索引删除：`delete --doc-id {ts}-{safe_name}`
- 再删除目录：`/var/openclaw-kb/{kb}/{ts}-{safe_name}`

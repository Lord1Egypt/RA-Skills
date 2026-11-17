# 学习与更新

本skill把语义分析交给当前模型，把文档提取、来源检查、版本与文件同步交给标准库脚本。没有内置额外LLM服务，也不需要单独API key。脚本检查原文定位和状态，不证明模型推导的规律一定正确；需按原文复核语义。

## 初次学习：自动完成

用户交来历史稿件并要求学稿，意味着在当前已授权账号的学习任务内提取写法；不需要再要求其填写“我的风格是什么”。视频转写复用环境中已有工具，本脚本直接支持TXT、MD、DOCX。尚未拿到视频正文不能仅凭账号名建模。

在skill目录执行；其他目录使用脚本绝对路径：

```sh
python3 scripts/learn.py --profile .xuegao/author.json --account author init
python3 scripts/learn.py --profile .xuegao/author.json --account author ingest \
  --expected-revision 0 --scope 观点口播 --inputs sample1.docx sample2.txt
python3 scripts/learn.py --profile .xuegao/author.json --account author context --scope 观点口播
```

初始化只做一次。每次写操作使用真实当前revision，不盲目照抄示例数字。ingest自动去重，重复导入不增加版本。每个文件默认是一篇独立稿；同一文档确有多篇作品时，模型检查真实边界后用`--split-pattern`指定分隔，不能把一篇文章的不同段落冒充多篇证据。来源可能有不同体裁，应分批指定scope。

模型根据正文生成内部分析文件，用户不需要手写JSON：

```json
{
  "account_id": "author",
  "rules": [
    {
      "key": "opening",
      "dimension": "opening",
      "scope": "观点口播",
      "value": "先提出具体使用中的判断，不做通用背景铺垫",
      "evidence": [
        {"sample_id": "实际导入得到的ID", "quote": "原文中的连续短摘录"}
      ]
    }
  ]
}
```

dimension只能是opening、viewpoint、structure、sentence、lexicon、density、ending。每条证据必须可在该账号同体裁原文逐字定位。应包含原文足以支持的表达规律，不能把具体地名、数字、政策适用范围转成写作规则。

```sh
python3 scripts/learn.py --profile .xuegao/author.json --account author apply \
  --expected-revision 1 --analysis analysis.json
python3 scripts/learn.py --profile .xuegao/author.json --account author sync --workspace /path/to/authorized-workspace
```

同一规律有两篇以上不同正文支持时标为learned并自动用于生成；一篇支持时标为tentative，也进入当前体裁上下文供谨慎参考，不强制用户审批。这个数量是参考工具的保守提升条件，不是“两个例子就证明统计规律”。同一正文的不同文件/修订不会重复累计。模型生成草稿标为ai_draft，不能用作作者证据。

提炼后先读context取最新规则及代表例子，再直接完成任务。首次内部校准优先用留出稿；没有独立材料时报告未做留出验证，不向用户索要一轮轮纠正作为前置条件。

## 后续修改：从差异学习

应用编辑器保存事件，或任务中作者亲改后的文本，传入之前AI稿和人工稿：

```sh
python3 scripts/learn.py --profile .xuegao/author.json --account author revise \
  --expected-revision 2 --before ai-draft.txt --after author-edited.docx \
  --scope 观点口播 --origin human_edit
```

脚本记录真实改动区间。模型只从风格变化提炼新规律，事实修正不进入文风。引用修订稿的证据必须与真实改动相交；删掉的铺垫可用`side: before`引用，但只能支持`operation: avoid`。不能把删掉的话学成偏好的话。

新规律更正旧模型推断时给出`supersedes`旧规则ID；会保留旧版本并使旧推断失效。一次人工修改支持的新方向仍为tentative，可立即用于该体裁；重复独立修改可提升。用户明确确认的规则不会被自动推断覆盖，冲突进入proposed等待后续明确证据，当前稿遵守本轮要求。

替换同一条规律时保持其key和scope不变；新维度另建规则。标识不匹配会被拒绝，不能把保存失败解释成已经更新。修改部分被沿用的AI文字不成为新作者证据，context仅提供实际编辑句子作为修订范例。

模型完成分析后自动apply、sync并重新加载context，不需用户额外说“记住”。若应用没有保存事件，skill无法看到用户在其他软件中未回传的修改；接入责任见存储约定。

## 同步方式

sync只管理SOUL.md、MEMORY.md、STYLE.md中`XUEGAO:START/END`区块，保留外部内容并备份修改前文件，更新时替换区块。同步的是写法与证据ID，不是旧稿事实或整篇私稿。脚本不改变agent配置、工具权限或其他账号。

已有应用数据库时可不用本地脚本，但须实现同样的来源、状态、版本和事件机制。当前工具无写权限时先完成本轮创作，说明保存未完成；不能将生成的JSON或“已学习”回复当作成功持久化。

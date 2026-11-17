# 分析结果导入规范

处理 `make-analysis-queue` 生成的队列时阅读本文件。

写入一个包含 `items` 数组的 JSON 对象。每个 `articleId` 必须与队列中的原值完全一致，不要添加 Markdown 代码块标记。

```json
{
  "items": [
    {
      "articleId": "exact-id-from-queue",
      "summary": "80-180 字事实摘要",
      "keyPoints": ["核心观点 1", "核心观点 2"],
      "keyData": ["文中明确出现的数据；没有则为空数组"],
      "logic": "论证路径或内容结构，40-120 字",
      "topics": ["稳定主题标签"],
      "sentiment": "positive|neutral|negative|mixed",
      "importance": 1,
      "changeNotes": "相对 previousContext 的变化；无依据则为空字符串",
      "risks": ["未经外部验证的主张、口径限制或疑点"],
      "stance": "support|question|neutral|informational",
      "angle": "侧重点或切入角度一句话，不超过 120 字",
      "relatedAccounts": [
        {
          "account": "同主题的另一公众号名",
          "stance": "support|question|neutral|informational",
          "angle": "该号侧重点一句话",
          "evidence": "能佐证该号立场的原文要点"
        }
      ],
      "keywordsHit": ["命中的账号关键词"]
    }
  ]
}
```

字段约束：

- `summary`、`logic`、`changeNotes` 和 `angle` 必须是字符串。
- `keyPoints`、`keyData`、`topics`、`risks` 和 `keywordsHit` 必须是短字符串数组。
- `topics` 包含 1 至 5 个可复用标签，不能写成句子。
- `importance` 是 1 至 5 的整数。只有出现重大的战略、产品、政策、市场或竞争变化时才使用 5。
- `sentiment` 描述文章表达的立场，不代表文章内容真实与否。
- 文章中的主张不会自动成为事实。未经核实或含义模糊的主张应写入 `risks`。
- 只有存在证据时才能使用 `previousContext` 做纵向比较，不能只根据发布时间顺序推断发生了变化。
- `stance` 描述本文相对话题的立场，枚举：`support`（支持/利好）、`question`（质疑/证伪）、`neutral`（中立分析）、`informational`（纯信息通报）。不在枚举内或缺失时回退为 `informational`，导入不会报错。
- `relatedAccounts` 只能依据队列提供的 `crossAccountContext` 填写，不得虚构或臆造账号。每一项必须包含 `account`、`stance` 和 `angle`；`evidence` 可选。没有同主题对照时留空数组。
- `keywordsHit` 列出命中的账号关键词（来自队列的 `accountKeywords`），最多 20 项；无关键词命中时留空数组。

> 以上四个新字段均为可选。旧版分析结果（不含这些字段）导入时自动以默认值兜底，不影响既有数据展示。

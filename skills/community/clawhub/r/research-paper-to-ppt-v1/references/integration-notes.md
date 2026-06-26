# 集成说明

本文件说明如何把本技能与环境内已有技能串起来。

## 依赖技能

本技能作为编排型 skill 使用，默认依赖以下已有技能：
- `medical-keyword-search`
- `full-paper-api` 或与之等价的全文读取 skill（若当前环境实际使用 `full-paper-read`，以环境内实际技能名为准）
- `pptx`

## 推荐调用顺序

1. 用 `medical-keyword-search` 精确定位单篇文献
2. 优先用全文技能读取标题、摘要、正文、图表、PDF/图片来源
3. 若全文 API 因 token 格式问题失败，调用 `scripts/fetch_fullpaper.py`：它会从 `INFOX_MED_TOKEN` 中提取合法的 `32位hex|7位数字` 候选 token 并重试全文接口，同时整理 `paper_meta/fulltext/figures`
4. 调用 `scripts/extract_figures_and_captions.py`：把原文 Figure 与其图注、Results 对应段落、证据片段、中文解释要点绑定起来；图解应优先来自“图注 + Results 上下文”，而不是只改写图注
5. 若命中失败或全文不足，直接返回：`检索失败，无法生成`
6. 用 `scripts/validate_inputs.py` 先做本地硬校验
7. 读取 `references/outline-basic-research.md`、`references/slide-schema.md`、`references/figure-caption-policy.md`
8. 用 `scripts/build_prompt_bundle.py` 整理为中间 bundle
9. 先生成带 `image_paths_or_urls / figure_explanations` 的 `slides[]`
10. 用 `scripts/enforce_figure_requirements.py` 进行最终硬校验
11. 将 bundle/slide JSON 交给 `pptx` 技能生成最终 `.pptx`

## 图片强约束落地

为避免“内容总结得很好，但没有原文图”的失败模式，当前 skill 额外要求：
- 结果页必须显式携带 `image_paths_or_urls`
- 结果页必须显式携带 `figure_explanations`
- 生成 PPT 前必须跑 `enforce_figure_requirements.py`
- 若某结果页没有图或图解过短，直接失败，不允许输出简化版

## token bug 修复说明

某些运行环境中的 `INFOX_MED_TOKEN` 可能带有非 hex 前缀，导致原始值长度不是全文 API 要求的 40 字符，直接请求会返回“无效的 token 格式”。

`fetch_fullpaper.py` 的处理策略：
- 保留原 token 作为首选候选
- 从 `|` 左侧提取 32 位连续 hex 串
- 对混合前缀做 hex 压缩后取最后 32 位
- 右侧仅保留数字并截取前 7 位
- 仅对满足 `^[0-9a-f]{32}\|\d{7}$` 的候选发请求

这样可以在不改系统环境变量的前提下兼容更多部署环境。
## 为什么保留脚本层

这些脚本不是为了替代外部技能，而是为了：
- 把失败条件落到可复用的本地检查
- 把输入整理成稳定 JSON，减少临时 prompt 漂移
- 让 skill 打包后具备更完整、可复用的资源结构

## 失败策略

以下任一情况都应直接失败，不要尝试“先生成简版”：
- 文献无法唯一定位
- 只有摘要，没有足够正文
- 缺少可追溯的原文图片
- 图表来源不清楚，无法确认来自原文

失败时统一返回：`检索失败，无法生成`

## Figures 输入建议

`figures.json` 可以是以下任一格式：

### 对象格式
```json
{
  "Figure1": "https://...",
  "Figure2": "https://..."
}
```

### 数组格式
```json
[
  {"figure_ref": "Figure1", "url": "https://..."},
  {"figure_ref": "Figure2", "url": "https://..."}
]
```

只要能明确对应原文图即可。

# wot-ui-plus Skill

这是一个面向 `wot-ui-plus` 组件库使用场景的项目级 skill。

它的目标不是分析组件库实现，而是帮助快速回答这些问题：

- 某个组件怎么用
- 组件有哪些 `props`、`events`、`slots`、`methods`
- 某个 `use-*` 组合式 API 怎么接入
- 全局配置、主题配置、Provider 相关能力怎么使用

## 适用场景

当需要基于现有组件文档快速给出用法说明、示例代码或 API 摘要时，优先使用这个 skill。

适合的问题包括：

- “`wd-button` 怎么写一个最小示例？”
- “`upload` 和 `use-upload` 分别怎么用？”
- “主题配置应该看哪个文档？”
- “某个组件支持哪些事件或插槽？”

## 目录结构

当前 skill 目录结构如下：

```text
wot-ui-plus/
├─ SKILL.md
├─ README.md
├─ agents/
│  └─ openai.yaml
└─ references/
   ├─ button.md
   ├─ popup.md
   ├─ use-toast.md
   └─ ...
```

各文件职责：

- `SKILL.md`：给代理读取的主技能说明，定义触发场景、文档分组、回答流程和约束
- `README.md`：给人阅读的说明文档，帮助维护这个 skill
- `agents/openai.yaml`：skill 的界面元数据
- `references/`：组件文档与 API 文档资料库

## references 组织方式

`references/` 采用扁平结构，文件名尽量与组件名或 API 名保持一致。

常见查找方式：

- 查询组件：直接找同名文件，例如 `button.md`、`popup.md`、`upload.md`
- 查询组合式 API：优先查看 `use-*.md`
- 查询配置类能力：优先查看 `configProvider.md`

`SKILL.md` 中已经按照使用场景做了分组索引，例如基础、表单、反馈与交互、展示、导航与布局、组合式 API 等。维护时应优先保持这些分组与 `references/` 中实际文件一致。

## 维护方式

维护这个 skill 时，优先遵循以下原则：

- 保持 `SKILL.md` 和 `references/` 一致，不要引用不存在的文件
- 新增文档时，优先沿用当前扁平命名方式
- 删除或重命名文档时，同步更新 `SKILL.md` 的分组索引
- README 只保留人类维护者真正需要的信息，不重复堆砌组件清单
- 如果 skill 的定位变化，先改 `SKILL.md`，再同步 README

## 更新建议

当组件文档来源发生变化时，可按下面顺序更新：

1. 同步或替换 `references/` 中对应文档
2. 检查 `SKILL.md` 中的文档分组和路径引用
3. 如有必要，更新本 README 中的结构或维护说明

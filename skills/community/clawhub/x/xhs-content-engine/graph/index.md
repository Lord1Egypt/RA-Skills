# 图谱总入口 · index.md

> agent 进来先读这个文件，沿 `[[wikilink]]` 加载相关节点。

## 是什么

Content Engine 的"记忆 / 灵魂 / 上下文"。把品牌、客群、平台、钩子、风格分散在多个 .md 文件里，用 `[[]]` 互相链接，agent 按需要拉取。

## 当前服务的品牌

> 单品牌或多品牌都行。每个品牌一行，链到对应的 brand-story 节点。

- **{{品牌 1 名}}** → [[brand/brand-story]] · 主理人 / 价值观 / 定位
- _（多品牌时复制此行）_

# TODO: 把上面的占位换成你真实的品牌名，或者删掉占位、写一行你自己的描述。

## 节点地图

按用途分组，括号里是该节点的"一句话用途"。

### 品牌
- [[brand/brand-voice]] — 跨平台统一的品牌声音 DNA（语气、用词、禁用表达）
- [[brand/brand-story]] — 品牌故事 / 主理人 / 门店背景

### 平台
- [[platforms/xiaohongshu]] — 小红书 playbook（v1 唯一支持）
- _v1.1 计划加入：抖音 (`platforms/douyin.md`)、视频号 (`platforms/shipinhao.md`)_
- _v2 计划加入：B 站 (`platforms/bilibili.md`)_

> **跨平台共享部分**（不绑定具体平台）：brand-voice / brand-story / segments / hooks / style-tags / taboo
> **平台特化部分**：每个平台一个 playbook 文件，描述该平台的算法逻辑、爆款公式、禁忌

### 客群
- [[audience/segments]] — 目标客群分层（画像、关注点、决策路径）

### 引擎
- [[engine/hooks]] — 钩子库（按情绪类型分类，由拆解过程喂养）
- [[engine/style-tags]] — 风格标签词典（避免每次造新词）
- [[engine/taboo]] — 禁忌词 / 合规要求

---

## 使用约定

1. **新节点** → 取一个稳定的短名（kebab-case），加入"节点地图"
2. **修改既有节点** → 在文件末尾追加「更新日志」，写清日期 + 来源（哪个拆解触发的）
3. **节点之间引用** → 一律用 `[[路径/文件名]]`（不带 `.md` 后缀），比如 `[[brand/brand-voice]]`
4. **图谱是只追加结构**：不删旧观察，矛盾打 ⚠️ 由人工判断

---

## 状态

- [ ] brand-voice 已填
- [ ] brand-story 已填
- [ ] xiaohongshu playbook 已填基础
- [ ] segments 已填至少 1 个客群
- [x] hooks 模板就位（拆解会自动补充）
- [x] style-tags 模板就位
- [ ] taboo 已填

# TODO: 完成上面任意一项后把 [ ] 改成 [x]。前 4 项填完，下次拆解就会带品牌视角。

# verify-before-answer

一个 OpenClaw skill，用于在回答事实型、对比型、支持情况类问题前，强制先搜索或查文档核实，避免凭印象直接下判断。

English: An OpenClaw skill that forces verification (search / docs / runtime evidence) before answering factual, comparison, or capability questions — no answering from memory.

## 为什么需要这个 skill

模型（尤其是小模型）在回答以下问题时容易凭训练印象输出：

- 某工具是否支持多会话
- 某个版本现在是否还成立
- 两个平台/工具的关系是什么
- 用户追问"没懂 / 你搜过吗"

这个 skill 的作用是把"先核实，再回答"固化成默认行为。触发条件只看问题类型，不看模型大小。

## 适用场景

- **事实核对**：版本、发布状态、官方支持情况
- **能力对比**：两个工具/平台是否支持某特性、如何隔离
- **关系判断**：组件之间是什么关系、是否基于某协议
- **用户质疑**：用户指出"没懂 / 你搜过吗 / 不确定不要瞎说"

## 核心原则

1. 优先信任检索结果
2. 没有检索结果时，明确说"我没有查到一个可靠来源"
3. "没查到证据"和"查到明确否定"是两种不同结论，严格区分
4. 不用"应该是 / 大概率 / 本质上"这类词绕过核实

## 安装

### OpenClaw / ClawHub（推荐）

```bash
npx clawhub@latest install @padepa/verify-before-answer
```

### 方式二：手动克隆

```bash
git clone https://github.com/padepa/verify-before-answer.git
ln -s /path/to/verify-before-answer ~/.agents/skills/verify-before-answer
```

验证安装：

```bash
openclaw skills list | grep verify-before-answer
```

## 使用示例

详见 `SKILL.md` 中的示例对话部分。

## License

MIT

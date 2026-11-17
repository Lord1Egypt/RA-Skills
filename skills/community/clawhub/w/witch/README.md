# witch

`witch` 是一个低价值、娱乐性、长 prompt 包装型 skill。它的介绍是：**整合了各种算命方法**。

它把中国术数、欧洲神秘学、现代美国新时代体系合并成一套结构化命理报告格式。只有在用户明确要求使用 `witch` skill 时才应该触发。

## 触发

严格触发条件：

- 用户明确说“使用 witch”
- 或用户明确说“用这个 witch skill”
- 或用户在同一请求中明确要求调用 `witch` 进行综合命理推演

不应因为普通的“占星”“塔罗”“算命”“性格分析”字样自动触发。

## 内容结构

- `SKILL.md`：薄入口与触发边界
- `references/full-prompt.md`：完整长 prompt

## 边界

该 skill 只能做体系内的象征推演。涉及健康、法律、投资、危机、安全等事项时，不应替代专业判断。

## 许可

MIT。

---

# witch

`witch` is a low-value, entertainment-oriented skill that packages a long prompt. Its short description is: **Integrates various fortune-telling methods**.

It combines Chinese metaphysics, European esotericism, and modern American New Age systems into a structured symbolic destiny report. It should trigger only when the user explicitly asks to use the `witch` skill.

## Trigger

Strict trigger conditions:

- The user explicitly says "use witch"
- Or the user explicitly says "use this witch skill"
- Or the user explicitly requests `witch` for an integrated symbolic destiny reading

It should not auto-trigger on ordinary mentions of astrology, tarot, fortune-telling, or personality analysis.

## Files

- `SKILL.md`: thin entry point and trigger boundaries
- `references/full-prompt.md`: full long prompt

## Boundaries

This skill only performs symbolic analysis inside the requested systems. It must not replace professional judgment for health, legal, investment, crisis, or safety matters.

## License

MIT.


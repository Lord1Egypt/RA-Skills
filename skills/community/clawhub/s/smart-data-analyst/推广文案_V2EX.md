# V2EX 推广文案 — 数据分析助手
# 发布节点：分享创造

---

**做了一个上传 CSV/Excel 就能自动出分析报告的 OpenClaw Skill**

背景：经常有非技术同事拿数据来问我怎么分析，每次都要帮他们写 Python 或者教公式，重复劳动多。

做了个 OpenClaw Skill 解决这个问题：上传文件 → 自动做描述性统计、相关性分析、异常检测、趋势分析 → 输出结构化中文报告，最后给出可执行建议。

支持 CSV、Excel、JSON、TSV，也可以直接粘贴数据。中文字段名全程中文报告。

```
openclaw skills install smart-data-analyst
```
clawhub.ai/skills/smart-data-analyst

用了 OpenClaw 的 tool_use 机制做文件解析，没有外部依赖。有在做类似数据工具的吗，交流一下实现思路？

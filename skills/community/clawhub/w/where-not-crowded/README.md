# 去哪不挤

一个在节假日前替用户做判断的出行 skill。

它不回答“去哪都行”，而是先判断用户默认会选的热门路径值不值，再给出一个更不挤、更值、更适合的替代方案。

## 它解决什么问题

- 节假日想出去，但不想人挤人
- 默认热门城市或海边路线价格太高、体验太差
- 用户不想自己分析人流、热点、机酒价格和出发时间
- 用户想直接拿到一个已经权衡好的答案

## 它不做什么

- 不做详细旅行攻略
- 不做订票和订酒店执行
- 不做签证办理
- 不做“给你列 10 个冷门目的地自己选”

## 典型触发方式

- `五一去哪不挤`
- `上海出发，五一去哪人少`
- `想去海边，有没有比三亚更好的选择`
- `预算 5000，节假日去哪更值`
- `国庆想出去玩，但不想太挤`

## 每次会产出什么

1. 对话里的完整 Markdown 报告
2. 工作目录里的 Markdown 文件
3. 工作目录里的独立 HTML 报告文件

报告里会包含：

- 一句话结论
- 默认路径判断
- 为什么不推荐
- 多维判断
- 主推荐 / 近程替代 / 远程替代
- 国内外成本对比
- 最佳出行窗口建议
- 如果你不这么走会发生什么
- 最终建议

## 本地文件结构

- `SKILL.md`：skill 行为定义
- `README.md`：介绍文档
- `assets/destination_frames.json`：预置判断框架
- `assets/report_widget.html`：独立 HTML 模板
- `references/report_template.md`：Markdown 输出模板
- `references/example_report.md`：完整示例
- `references/widget_data_spec.md`：前端 JSON 结构
- `scripts/generate_report.py`：本地生成脚本
- `tests/run_examples.py`：示例测试

## 本地生成命令

```bash
python3 /Users/ye/.agents/skills/where-not-crowded-report/scripts/generate_report.py \
  --intent '上海出发，五一去哪人少' \
  --output-dir /Users/ye
```

## 当前产品版本

当前是 instruction-first + 本地成品输出版本。

特点是：

- 不依赖外部 API
- 通过预置 frame 做节假日出行判断
- 既能在对话里直出判断报告，也能本地落地 HTML 成品

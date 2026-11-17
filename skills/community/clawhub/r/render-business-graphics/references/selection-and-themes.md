# 图形选择和色系选择

本文件负责把用户意图路由到线上目录中的稳定图形 ID。语义不明确时先读 `domain/`，确定家族后再读 `references/graphics/` 的单类图形说明。

## 选择矩阵

| 用户意图 | 首选 | 不要在以下情况替代使用 |
| --- | --- | --- |
| 分类数值比较 | `chart.bar` 或 `chart.comparison` | 内容是父子组织或流程连线 |
| 月份、阶段趋势 | `chart.line` | 没有数值，只是叙事步骤 |
| 构成比例 | `chart.pie` | 有负数或重点是时间变化 |
| 多维能力画像 | `chart.radar` | 只有一个指标维度 |
| 转化和递减阶段 | `chart.funnel` | 阶段存在分支或非单向流转 |
| 分类 × 系列完整评分 | `chart.matrix` | 存在缺失单元或内容是定性描述 |
| 父子层级 | `organization` | 重点是跨分支协同 |
| 严格有序步骤 | `flow.sequence` | 存在判断、分支或反馈 |
| 决策、分支、返工 | `flow.graph` | 只是线性清单 |
| 概念流程、循环、关系 | `smartart.*` | 必须审核每条真实连线 |
| 工期和依赖 | `schedule.*` | 没有 duration 或 predecessor |
| 参与方调用和返回 | `sequence` | 只有日期事件 |
| 日期里程碑 | `timeline.*` | 实际是任务排期 |

## 契约优先流程

1. 服务版本或能力未知时执行 `get_capabilities.py`。
2. 执行 `get_reference_images.py --kind <kind> --output-dir <dir>`，获取目录和参考 SVG。
3. 从返回结果选择一个稳定 ID。
4. 执行 `get_graphic_contract.py <id> --preview-output <file>`，阅读 `parameters`。
5. 以 `exampleRequest` 为结构骨架，替换全部示例业务内容。

线上 catalog 对 ID、字段、必填项、数量限制和示例拥有最终解释权；本文件只负责选择逻辑。

## 色系规则

线上 `/v1/themes` 才是实际可用色系的权威来源。当前常见色系及倾向如下，部署版本可能增加或减少：

| 色系 ID | 适用场景 |
| --- | --- |
| `tech-blue` | 默认、技术方案、数据和中性商务文档 |
| `classic-engineering` | 工程、施工、实施计划、传统技术文档 |
| `government-red` | 政务、正式汇报、党建、庄重红色主题 |
| `black-white` | 黑白打印、复印、低彩色输出 |
| `sky-blue` | 信息化、云服务、清爽蓝色方向 |
| `mint-green` | 生态、环保、健康、服务流程 |
| `soft-warm` | 人文服务、活动、餐饮、温暖叙事 |
| `pastel-mix` | 多阶段、多类别且需要柔和区分 |
| `teal-gold` | 高端商务、战略规划、正式展示 |
| `lavender` | 创新、文化、品牌、柔和创意方向 |

线上也可能出现 `formal-black`、`engineering-green`、`elegant-purple`、`business-blue`、`solemn-red`、`warm-gold` 等部署扩展色系。没有用户指定或明确映射时，不要猜测这些扩展色系的语义；可以使用接口返回的 ID，但优先省略 `theme` 使用服务默认色系。

硬规则：

- 用户指定合法 ID 时原样保留。
- 没有色系要求时省略 `theme`，不能写 `null`、空字符串或自定义 HEX。
- 不能把中文色系名称直接传给接口，接口只接受英文 ID。

## 页面和输出格式

- 默认省略 `page`，由服务根据内容密度选择 A4 方向并在布局溢出时尝试另一方向。
- 用户明确要求横版、排期/时间轴较密或使用 `smartart.petal-radial` 时使用 `a4-landscape`。
- `rasterScale: 1` 用于快速预览；普通 PNG 省略该字段；打印可使用 `3`。
- PNG 用于预览和 Word 插入，SVG 用于矢量交付。

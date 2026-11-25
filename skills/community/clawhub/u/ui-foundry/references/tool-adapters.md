# 工具与实现适配器

本文是接线指南。先复用项目已接受的设计系统；工具库不替代任务、内容、状态和真实渲染审核。仓库中的小型集成测试不等于目标产品已经接通，仍需检查当前项目。

## 选择路径

| 场景 | 路径 | 不做什么 |
| --- | --- | --- |
| 已有设计系统 | 沿用其 token、组件、Provider、可访问性和贡献约定 | 不因“更现代”替换全栈 |
| 新 React 19 + Tailwind CSS 4 Web，尚无设计系统 | 默认采用 HeroUI v3；发现版本、许可或交付约束冲突再换 | 不把它设为安装本 Skill 的前置依赖 |
| 既有 shadcn/Base UI | 保留原组件与组合方式 | 不混入第二套同职责 primitive |
| 普通 Web | 用项目已打包的基础样式/组件，或小范围原生 HTML/CSS | 不假定 React 或 Tailwind |
| 原生应用 | 用 SwiftUI 或目标平台既有 toolkit | 不用 Web wrapper 冒充原生 UI |

## 采用前检查

具体控件根据 [场景组件路由](component-patterns.md) 决定。框架适配只是第一层：地点需要搜索/地图服务及地点对象，日期需要正确的日期语义，搜索需要结果状态和过期请求处理。包内可复用实现位于 `assets/web-patterns/`、`assets/place-service/` 和 `assets/native-patterns/`；按任务读取对应部分，不把整个示例应用塞入目标产品。

先检查已安装版本、许可、包体、CSS/reset、token 命名、暗色主题、icon、国际化和现有组件覆盖率。确认触发、键盘、焦点、禁用、加载、错误、长文本、触摸目标与动画减弱设置仍符合当前交互契约。

HeroUI v3 仅在 React 19+ 与 Tailwind CSS v4 兼容时采用。其 React 包为 `@heroui/react`，样式包为 `@heroui/styles`；全量入口需要先 `@import "tailwindcss"`，再 `@import "@heroui/styles"`。局部 CSS 仍依赖 utilities、variants 和 theme prelude。接入前在可回退变更中确认 Provider、主题变量和 CSS 层级不与现有系统冲突；不要凭文档宣布已完成集成。Agent 自行完成适配选择，不让用户从库清单中挑选。

官方资料：[HeroUI Quick Start](https://heroui.com/en/docs/react/getting-started/quick-start)、[styles 结构与局部导入](https://github.com/heroui-inc/heroui/blob/v3/packages/styles/README.md)。

仓库保留 [锁定版本的集成范例与检查](https://github.com/theosunny/ui-foundry/tree/main/benchmarks/integrations/heroui)：真实 Button、TextField 和 Modal，含打开、编辑保存、Escape 与焦点返回。需要代码时先读当前项目版本的组件文档，再按这条已测交互路径适配；不照搬历史 API。

## Impeccable：可选审查工具

若已安装且项目允许，可把 Impeccable 用于塑形、批评、技术审核或浏览器迭代；它提供 agent 指令、持久产品上下文与规则检测，不提供组件库，也不能证明界面美观或任务成功。它不是必需依赖：不自动安装、不自动启用 hooks、不将其审美禁忌变成通用规则。

将已作出的产品与设计决定记录到项目既有 `DESIGN.md` 或等价记录；Agent 根据证据补全决定、假设和待验证项，不能把它退化成空白用户问卷。若安装它，核对目标 harness 支持、网络/二进制获取及 hook 信任；Codex hook 更新可要求再次批准。

官方资料：[Impeccable README](https://github.com/pbakaus/impeccable#readme)、[安装与 harness 约束](https://github.com/pbakaus/impeccable#installation)。

## 视觉参考与 REA

视觉参考、REA 或同类能力均为可选 adapter。只在真实发现并读取已安装 Skill 后使用；找不到时说明未使用，继续用可用的浏览器和公开源码研究，不让工具缺席阻塞独立设计。

参考时观察可见界面、状态和转场。记录“观察”与“推断”来源：例如“窄视口时导航折叠”为观察，“因此适合本项目”为推断。第三方代码、图片、字体或资产只在许可允许时复用；没有源码、接口或授权时，不凭截图虚构服务端、数据模型或交互实现。

## 证据不可省略

先用当前项目已授权的浏览器、模拟器、测试或人工操作取得渲染和任务证据。某个工具不可用时，报告阻塞并使用下一个可用方式；不能静默跳过截图、状态/转场或交互证据，更不能把构建通过、规则检测或组件库采用写成视觉质量结论。

Lovable 的可借鉴点是将组件、规则、依赖和版本化上下文一起分发，并在连接后核对 CSS、Provider、构建与依赖；这是系统接线策略，不是输出质量保证。见 [Lovable Design Systems](https://docs.lovable.dev/features/design-systems)。

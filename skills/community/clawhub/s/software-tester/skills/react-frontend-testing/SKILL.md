---
name: react-frontend-testing
description: React 组件/前端测试：React Testing Library 渲染、用户交互、查询定位、mock 与快照验证
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/react-frontend-testing/SKILL.md
  version: 1.0.0
  updated: 2026-08-19
  url: https://skills.sh/affaan-m/ecc/react-testing
metadata:
  category: 前端测试
  platform: Web
  difficulty: 入门
---

# React 前端组件测试

> 用 React Testing Library（RTL）+ Jest/Vitest 对 React 组件做渲染、交互、查询与断言：以用户行为为中心，避免测试实现细节。改编自社区高安装量技能 affaan-m/ecc@react-testing（3.5K），并参考 itechmeat/llm-code@react-testing-library（1.3K）与 manutej/jest-react-testing（1.1K）。

## 能力

- **渲染与查询**：`render` 挂载组件，`getBy*`/`findBy*`/`queryBy*` 系列查询（角色/文本/标签/占位符/测试 ID）
- **用户交互**：`fireEvent` 与 `@testing-library/user-event` 模拟点击、输入、键盘、焦点
- **异步处理**：`waitFor` / `findBy*` 等待状态更新，避免竞态断言
- **mock 与桩**：`jest.mock` / `vi.mock` 模块、MSW 拦截网络、`jest.fn` / `vi.fn` 监听调用
- **快照与对比**：`toMatchSnapshot` 谨慎使用，偏向显式行为断言
- **可访问性**：优先用角色/名称查询，天然对齐 a11y

## 使用方式

```
/react-frontend-testing 给这个 <Cart /> 组件写测试，覆盖加购与数量变更
/react-frontend-testing 用 user-event 测试这个表单提交交互
/react-frontend-testing 给这个异步数据加载组件写 loading/error/成功 三态测试
```

## 工作流

1. `render(<Component {...props} />)` 挂载到 jsdom/happy-dom
2. 用 `screen.getByRole` / `getByText` 定位元素（优先语义查询）
3. `userEvent.click` / `fireEvent` 触发交互
4. `await screen.findByText(...)` 或 `await waitFor(...)` 等待异步结果
5. `expect(...).toBeInTheDocument()` / `toHaveTextContent()` 断言
6. 必要时 `jest.mock('api')` 或 MSW 拦截请求，避免真实网络访问

## 适用场景

- React / Next.js 组件的单元测试与交互测试
- 表单、弹窗、列表、购物车等 UI 行为验证
- 组件库 / 设计系统的交互与可访问性回归
- 前端 TDD 起步

## 相关参考（Playbook）

- 组件渲染/查询、用户交互、异步、Mock 与桩 → [references/react-frontend-testing.md](../../references/react-frontend-testing.md)（§1 选型决策树、§3 渲染与查询、§4 用户交互、§5 异步测试、§6 Mock 与桩）
- 前端 TDD 起步（Red-Green-Refactor）→ [references/tdd.md](../../references/tdd.md)（§工作流、§与覆盖率关系）

## 限制

- 需要 Jest/Vitest + jsdom 或 happy-dom 环境（配置见 [assets/jest.config.template.js](../../assets/jest.config.template.js)）
- 不替代 E2E（Playwright）做跨页面流程验证
- 快照测试易腐化，优先显式行为断言
- React Native 组件请用 `callstack/react-native-testing-library`（不同运行环境，非 web DOM）

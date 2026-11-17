# React 前端组件测试 Playbook

> 面向 React（含 Next.js）组件的单元/交互测试方法论。本 playbook 聚焦「子技能装不下的决策与踩坑」：选型、异步、mock、快照陷阱。**先读这篇再动手，不要凭记忆猜 RTL 命令。**
> 配套子技能 [skills/react-frontend-testing](../skills/react-frontend-testing/SKILL.md)（derived，主锚 affaan-m/ecc@react-testing 3.5K）。

---

## 1. 选型决策树

```
你的目标是什么？
├─ 测「用户视角的交互行为」（点击→看到结果）→ React Testing Library（RTL）✅ 默认
├─ 测「类组件生命周期/实例方法」老代码 → 谨慎，考虑重构后转 RTL
├─ 测 React Native 组件 → callstack/react-native-testing-library（非 web DOM，不混用）
└─ 测「跨页面完整用户流程」→ 交给 E2E（Playwright），本栈不胜任

测试运行器选哪个？
├─ 已有 Jest 项目 / CRA / 老仓库 → Jest + jsdom（生态最全）
├─ Vite 项目 / 新项目 → Vitest + jsdom 或 happy-dom（更快、ESM 原生）
└─ 需要浏览器真实渲染（布局/样式）→ 上 Playwright/Storybook 视觉回归，非 jsdom

DOM 环境选哪个？（Vitest 必选其一）
├─ jsdom → 默认，兼容性好，部分浏览器 API 缺失需 polyfill
└─ happy-dom → 更轻更快，但少数边缘 API 行为有差异，先试 jsdom
```

**核心原则**：测「行为」不测「实现」。优先按可访问性语义查询（role/text/label），而非 `data-testid` 或组件内部 state/props。这样重构内部实现时测试不崩。

---

## 2. 环境搭建（确定性命令）

### Jest + jsdom（CRA / 老项目）

```bash
npm i -D jest @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom
```

`jest.config.js`：

```js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  // 用 babel-jest 或 ts-jest 处理 TSX
  transform: { '^.+\\.(ts|tsx)$': 'ts-jest' },
};
```

`jest.setup.js`（全局注册匹配器 + 自动 cleanup）：

```js
import '@testing-library/jest-dom';
// @testing-library/react v13+ 需要显式 cleanup；v14+ 在测试框架 afterEach 自动做
import { cleanup } from '@testing-library/react';
afterEach(() => cleanup());
```

### Vitest + jsdom（Vite 项目）

```bash
npm i -D vitest @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom
```

`vitest.config.ts`：

```ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,            // 直接用 describe/it/expect，不必 import
    setupFiles: ['./vitest.setup.ts'],
  },
});
```

> 模板见仓库 [assets/jest.config.template.js](../assets/jest.config.template.js)，可平移到 Vitest 写法。

---

## 3. 渲染与查询（语义优先）

```tsx
import { render, screen } from '@testing-library/react';
import { Cart } from './Cart';

test('加购后数量更新', () => {
  render(<Cart initial={0} />);
  // 优先语义查询
  expect(screen.getByRole('button', { name: /加入购物车/i })).toBeInTheDocument();
  // 不要用 container.querySelector('.cart-count') 这类实现细节查询
});
```

**查询优先级（RTL 官方推荐）**：

| 优先级 | 查询 | 何时用 |
|--------|------|--------|
| 1 | `getByRole` | 首选，天然验证 a11y（按钮/输入框/链接/标题） |
| 2 | `getByLabelText` | 表单输入框 |
| 3 | `getByPlaceholderText` | 无 label 的输入框 |
| 4 | `getByText` | 静态文本 |
| 5 | `getByDisplayValue` | 输入框当前值 |
| 6 | `getByTestId` | **最后手段**，仅当无法用语义查询时 |

`getBy*` / `findBy*` / `queryBy*` 语义差异：

- `getBy*`：立即找，**找不到或找到多个 → 抛错**（同步）。
- `queryBy*`：立即找，找不到返回 `null`，**用来断言「不存在」**（如「提交后错误消失」）。
- `findBy*`：**异步**，等元素出现，返回 Promise，用于等待渲染完成后出现的内容。

---

## 4. 用户交互：userEvent vs fireEvent

```tsx
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/react';

test('填写并提交表单', async () => {
  const user = userEvent.setup();           // 必须 setup
  render(<LoginForm onSubmit={jest.fn()} />);
  await user.type(screen.getByLabelText(/邮箱/), 'a@b.com');
  await user.click(screen.getByRole('button', { name: /提交/ }));
});
```

- **`userEvent`**：模拟真实用户（触发 focus/blur/keydown 全链路），**异步**，优先用。
- **`fireEvent`**：直接派发单个合成事件，同步、轻量，适合只需要触发某一事件的场景，但跳过了真实交互链。
- 规则：凡涉及「连续输入/真实按键序列/剪贴板/焦点」用 `userEvent`；简单单事件可用 `fireEvent`。

---

## 5. 异步测试（避免竞态）

```tsx
test('加载完成后显示数据', async () => {
  render(<UserProfile id={1} />);
  // 初始 loading
  expect(screen.getByText(/加载中/)).toBeInTheDocument();
  // 等待异步内容出现
  expect(await screen.findByText(/用户名/)).toBeInTheDocument();
});

test('轮询直到条件满足', async () => {
  render(<Polling />);
  await waitFor(() => expect(screen.getByText('done')).toBeInTheDocument(), {
    timeout: 3000,
  });
});
```

要点：

- 用 `findBy*` 或 `waitFor` 包裹「晚于初始渲染出现」的内容，**不要裸 `await` 一个 Promise 再同步断言**（可能错过 act 边界）。
- `waitFor` 默认超时 1000ms，长轮询调大 `timeout`。
- **`act(...)` 警告**：所有导致 state 更新的操作必须包在 `act` 内。`userEvent`/`fireEvent` 内部已处理；手动 `setTimeout`/`resolve` 触发的更新要用 `await act(async () => {...})`。

### 假定时器（倒计时/防抖）

```tsx
import { fakeTimers } from '@testing-library/react'; // 或 jest.useFakeTimers()
beforeEach(() => jest.useFakeTimers());
afterEach(() => jest.useRealTimers());

test('3 秒后自动跳转', () => {
  render(<RedirectAfter delay={3000} />);
  jest.advanceTimersByTime(3000);
  expect(screen.getByText(/已跳转/)).toBeInTheDocument();
});
```

> Vitest 用 `vi.useFakeTimers()` / `vi.advanceTimersByTime()`。

---

## 6. Mock 与桩

### 模块级 mock（API / 子组件）

```tsx
// 在测试文件顶部
vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ name: 'Hope' }),
}));
// 或只替换部分导出，保留其余
vi.mock('./utils', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, format: vi.fn(() => 'MOCK') };
});
```

### 网络请求拦截（推荐 MSW）

```tsx
import { server } from '../mocks/server'; // 基于 msw 的 node server
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('错误处理', async () => {
  server.use(http.get('/api/user', () => HttpResponse.json({}, { status: 500 })));
  render(<UserProfile />);
  expect(await screen.findByText(/出错了/)).toBeInTheDocument();
});
```

**决策**：单组件简单依赖 → `vi.mock` 直接桩；涉及多种 HTTP 状态/多组件共享 → MSW 更真实、便于复用。避免 `jest.mock` 模块路径写错导致静默不生效。

### 监听调用

```tsx
const onSubmit = vi.fn();
render(<LoginForm onSubmit={onSubmit} />);
await user.click(screen.getByRole('button', { name: /提交/ }));
expect(onSubmit).toHaveBeenCalledWith({ email: 'a@b.com' });
```

---

## 7. 快照测试（谨慎）

```tsx
test('结构稳定', () => {
  const { asFragment } = render(<Button>OK</Button>);
  expect(asFragment()).toMatchSnapshot();
});
```

坑：

- 快照会随任意 UI 改动「全绿变红」，很快失去信号价值 → **优先显式行为断言**，快照只用于「无明显行为契约的纯展示组件」。
- 每次 snapshot 失败都 `u` 更新会掩盖回归 → 评审 diff，别无脑更新。
- 含随机值/时间戳的组件快照必然 flaky → 先固定或 stub 时间。

---

## 8. 典型坑与规避

| 坑 | 现象 | 规避 |
|----|------|------|
| **act() 警告** | `not wrapped in act(...)` | 用 `userEvent.setup()`、把手动 state 更新包 `await act` |
| **找到多个元素** | `TestingLibraryElementError: found multiple` | 用 `{ name }` 缩小、或 `getAllBy*` 遍历 |
| **过度用 testid** | 重构后测试脆弱 | 回退到 role/text/label 查询 |
| **快照腐化** | 一改就红、无脑 `u` | 改显式断言；快照仅限纯展示 |
| **没 cleanup** | 多测试互相污染（RTL v13-） | setup 文件 `afterEach(cleanup)`，或升级 v14+ |
| **测实现细节** | 改内部 state 名测试崩 | 只测用户可见行为 |
| **真网络请求** | 慢/flaky/需密钥 | 用 `vi.mock` 或 MSW 拦截 |
| **fake timer + 真 Promise** | 卡死 | 用 `jest.useFakeTimers({ doNotFake: ['queueMicrotask'] })` 或 `vi` 等价 |
| **React 18 StrictMode 双渲染** | 副作用跑两次 | 副作用幂等；mock 计数用 `toHaveBeenCalledTimes` 注意翻倍 |
| **queryBy 误用** | 断言「存在」却用 queryBy | 「存在」用 getBy/findBy；「不存在」才用 queryBy |

---

## 9. 提交前检查清单

- [ ] 测试按「用户行为」组织，未直接读组件内部 state/props
- [ ] 查询优先 `getByRole`/`getByLabelText`，`getByTestId` 仅最后手段
- [ ] 交互用 `userEvent.setup()` 且 `await`
- [ ] 异步内容用 `findBy*` / `waitFor` 包裹，无裸 await 竞态
- [ ] 网络/模块依赖被 `vi.mock` 或 MSW 拦截，无真实请求
- [ ] `vi.fn()` 断言了期望入参，而非只断言「被调用」
- [ ] 快照仅在纯展示组件使用，且评审过 diff
- [ ] `afterEach(cleanup)` 或 RTL v14+ 自动 cleanup 已就位
- [ ] 无 `act()` 警告、无「found multiple」错误
- [ ] mock 路径正确（改了路径后确认真生效，未被静默跳过）

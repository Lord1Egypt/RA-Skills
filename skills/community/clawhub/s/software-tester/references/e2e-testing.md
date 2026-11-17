# 端到端测试（End-to-End Testing）

> 用 Playwright 对真实用户流程做端到端验证：导航、元素交互、表单、断言、截图、跨页面流程。优先用 **Playwright Test**（完整 runner + 断言 + 报告），而非仅 CLI 原型。

## 何时使用

- 用户说「E2E 这个登录流程」「自动化测试下单」「端到端验证注册」
- 需要验证多页面跳转、表单提交、登录态、关键业务链路

## 安装与初始化

```bash
npm i -D @playwright/test
npx playwright install            # 安装浏览器二进制
npx playwright test --init        # 生成 playwright.config.ts + 示例
```

参考 [assets/playwright.config.template.ts](../assets/playwright.config.template.ts) 获取带 trace / screenshot / 重试的推荐配置。

## 标准测试结构

```ts
import { test, expect } from '@playwright/test';

test('用户可登录并进入仪表盘', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('用户名').fill('hope');
  await page.getByLabel('密码').fill('secret');
  await page.getByRole('button', { name: '登录' }).click();
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByRole('heading', { name: '欢迎' })).toBeVisible();
});
```

## 关键实践

- **优先语义定位**：`getByRole` / `getByLabel` / `getByText`，避免脆弱的 CSS/XPath。
- **Page Object 模式**：把页面交互封装成类，测试只描述业务意图。
  ```ts
  export class LoginPage {
    constructor(private page: Page) {}
    async login(user: string, pwd: string) {
      await this.page.getByLabel('用户名').fill(user);
      await this.page.getByLabel('密码').fill(pwd);
      await this.page.getByRole('button', { name: '登录' }).click();
    }
  }
  ```
- **稳定断言**：用 `toBeVisible` / `toHaveURL` / `toHaveText`，避免 `waitForTimeout` 硬等。
- **处理异步**：用 `expect.poll` 或 `page.waitForResponse` 等待接口返回。
- **可见性/网络**：用 `page.route` mock 接口，隔离后端不稳定。

## 反脆弱（减少 flake）

- 开 `retries: 2`（CI 中），失败自动重试。
- 打开 `trace: 'on-first-retry'`，失败可回放。
- 不要依赖元素排序/动画完成时间；等待状态而非时间。
- 用 `test.step` 组织多步流程，报告更清晰。

## 截图验证

- 正常校验用断言，不要「截图就完事」。
- 像素级比对见 [references/visual-regression.md](visual-regression.md)（Percy / Playwright screenshot diff）。

## 脚本加速

```bash
python3 scripts/e2e_scaffold.py --name 登录流程 \
  --steps "打开 /login;输入 账号 hope;输入 密码 secret;点击 提交;断言跳转 /dashboard"
```

### 步骤语法契约（动词后必须给参数）

| 步骤写法 | 生成 | 备注 |
|----------|------|------|
| `打开 /login` | `page.goto('/login')` | 目标须以 `/` `#` `?` `http(s)://` 开头 |
| `输入 账号 hope` | `getByLabel('账号').fill('hope')` | 字段以 `/` `#` `[` 开头时改用 `page.locator()` |
| `点击 提交` | `getByRole('button', { name: '提交' })` | 只生成 button role，其他角色需手改 |
| `断言跳转 /dashboard` | `expect(page).toHaveURL(...)` | 只接受路径形态 |
| `断言 文本 已登录` | `expect(getByText('已登录')).toBeVisible()` | 断言文案走这一条 |

**降级规则**：参数缺失或目标不是路径时，该步骤降级为 `// TODO: …（提示）` 并在 stderr 打 WARNING，
脚本**不猜**断言目标。所以骨架里出现 TODO 是预期行为，不是脚本坏了——按提示补参数重跑即可。

### 用这个脚本时的坑

| 坑 | 现象 | 处理 |
|----|------|------|
| 只写动词不写参数（`输入账号` / `断言跳转`） | 该步降级 TODO，stderr 有 WARNING | 补成 `输入 账号 hope` / `断言跳转 /dashboard` |
| 把中文页面名当路径（`打开登录页`） | 降级 TODO | 换成真实路径 `/login`；`goto('登录页')` 会被当相对 URL 解析成 404 |
| 断言目标不是 URL 却用 `断言跳转` | 降级 TODO 并提示改写 | 断言文案改用 `断言 文本 <文案>` |
| URL 里含 `;`（如 `?a=1;b=2`） | `;` 是步骤分隔符，URL 被截断 | 先生成骨架，再手动把完整 URL 粘回 `goto()` |
| 全部步骤都无法解析 | 测试体只有 TODO | **空测试体会「假绿」**，补全步骤后再纳入 CI |

生成的是**可运行的**骨架（含引号转义，`node --check` 可通过语法校验）；
但选择器由标签名/按钮名推断，落地前仍需按本文「稳定选择器」一节替换为 `data-testid`。

## 相关子技能（L3）

- 落地为 Playwright 浏览器自动化动作 → [skills/e2e-testing/SKILL.md](../skills/e2e-testing/SKILL.md)

## 限制

- 需要安装浏览器二进制（`npx playwright install`）。
- E2E 成本高、易碎；按测试金字塔仅占 ~10%，核心链路才 E2E，其余用单测/集成。
- 不替代完整的 Playwright Test 框架配置与 CI 编排。

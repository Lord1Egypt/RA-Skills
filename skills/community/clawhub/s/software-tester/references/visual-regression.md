# 可视化回归测试（Visual Regression Testing）

> 通过像素级截图比对，捕获 UI  unintended 视觉变化：布局错位、颜色/字体异常、元素丢失。用于防止「功能没改但页面歪了」这类回归。

## 何时使用

- 用户说「加视觉回归」「截图比对」「UI 回归测试」「防止页面走样」
- 已有 E2E（见 [references/e2e-testing.md](e2e-testing.md)），需在此基础上加像素校验

## 方案对比

| 方案 | 适用 | 特点 |
|------|------|------|
| Playwright `toHaveScreenshot` | 轻量、零外部服务 | 本地基线，CI 需提交基线图 |
| Percy / Chromatic | 团队协作、review 流程 | 云端管理、人工审批 diff |

## Playwright 自带（零依赖）

```ts
test('首页视觉稳定', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('home.png', { maxDiffPixelRatio: 0.02 });
});
```

- 首次运行生成基线；之后每次比对，超过阈值则失败并产出 diff 图。
- CI 中把基线图提交进仓库（或 artifact），保证跨机一致。

## Percy（云端审批）

```ts
import { percySnapshot } from '@percy/playwright';

test('首页', async ({ page }) => {
  await page.goto('/');
  await percySnapshot(page, '首页');
});
```

```bash
PERCY_TOKEN=xxx npx percy exec -- npx playwright test
```

## 最佳实践

- **锚定稳定区域**：对动态内容（时间、随机数、头像）用 `percySnapshot` 的 `percyCss` 隐藏或 mock，避免误报。
- **合理阈值**：`maxDiffPixelRatio` 0.01~0.05，过严会 flaky，过松会漏。
- **关键页面优先**：首页、核心流程页、品牌色强相关的组件。
- **与 E2E 同流程**：在已有 E2E 步骤后追加截图，复用导航逻辑。

## 相关子技能（L3）

- 落地为可视化回归动作（Playwright 自带零依赖方案）→ [skills/e2e-testing/SKILL.md](../skills/e2e-testing/SKILL.md)（可视化回归属 E2E/UI 测试范畴）

## 限制

- 跨浏览器/跨分辨率需分别建基线。
- 不适合验证「行为正确性」，只验证「样子没变」；行为仍靠断言。
- 字体/渲染差异可能导致跨环境 flake，需固定环境或云端统一渲染。

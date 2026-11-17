---
name: e2e-testing
description: Playwright 浏览器自动化：页面交互、快照定位、表单填写、截图
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/e2e-testing/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/microsoft/playwright-cli/playwright-cli
metadata:
  category: E2E 测试
  platform: Web
  difficulty: 入门
---

# Playwright 浏览器自动化

> 使用 Playwright CLI 进行浏览器交互和端到端测试：导航、快照、点击、表单、截图。

## 能力

- **页面操作**：open/goto 导航、back 回退、snapshot 快照
- **元素交互**：click/type/fill/dblclick/drag/drop/hover 全支持
- **表单**：fill + --submit、select、check/uncheck、upload
- **快照定位**：基于 ref 的精确定位，find 搜索文本或正则
- **脚本与截图**：eval 执行 JS、screenshot 截图

## 使用方式

```
/e2e-testing 打开 example.com，填表单并截图
/e2e-testing 自动化测试这个登录流程
/e2e-testing 在快照中搜索 "Sign in" 并点击
```

## 工作流

1. `playwright-cli open https://example.com` 打开浏览器
2. `playwright-cli snapshot` 获取页面可访问性快照
3. 基于快照 ref 进行交互（click/fill/type）
4. `playwright-cli screenshot` 截图验证
5. `playwright-cli close` 关闭浏览器

## 适用场景

- 网页交互自动化
- 表单填写测试
- 页面截图采集
- E2E 测试快速原型

## 相关参考（Playbook）

- Playwright E2E 标准结构、反脆弱（减 flake）、截图验证、脚本加速 → [references/e2e-testing.md](../../references/e2e-testing.md)（§标准测试结构、§反脆弱、§截图验证、§脚本加速）
- 可视化回归（Playwright 自带零依赖方案）→ [references/visual-regression.md](../../references/visual-regression.md)（§Playwright 自带、§最佳实践）

## 限制

- 需要安装 Playwright（`npx playwright install`）
- 不替代完整的 Playwright 测试框架（test runner + assertions）
- 复杂多页面流程建议用 Playwright Test
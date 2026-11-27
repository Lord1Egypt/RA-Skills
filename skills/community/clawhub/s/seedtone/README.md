# seedtone

[![skills.sh](https://skills.sh/b/shxuk/seedtone)](https://skills.sh/shxuk/seedtone)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)](./package.json)

简体中文 | [English](./README.en.md)

做 App、做网站，尤其是 Vibe Coding 的时候，很容易写着写着颜色就乱了，搭配起来很奇怪。

`seedtone` 把几套成熟的开源标准揉到了一起（**GitHub Primer** 角色命名、**Adobe Leonardo** 对比度计算、**OKLCH** 中性灰、**W3C DTCG / Style Dictionary**、**APCA** 对比度校验），生成的配色**不会太惊艳，但足够稳定，几乎不需要二次调整**。

**只给 1 个主视觉 Hex 色号**，就能算出明暗两套完整颜色矩阵（背景、文字、边框、交互态、不打架的提示色），交付两样东西：

1. **给人看的 HTML**（`dist/color-report.html`）：直接看网站和 App 的实际效果、切亮暗模式，点一下复制变量。
2. **给代码和 AI 用的约束工具**：CSS 变量、Tailwind 配置，加一个检查脚本，防止后面改代码时 AI 又把颜色写乱。

## 快速上手

```bash
# 作为 Agent Skill 安装（Claude Code / Cursor / Trae / Antigravity）
npx skills add shxuk/seedtone

# 或本地命令行直接跑
git clone https://github.com/shxuk/seedtone.git && cd seedtone
pnpm install
pnpm generate -- --seed "#007275"
```

产物都在 `dist/` 下：
- **预览**：浏览器打开 `dist/color-report.html`
- **接入**：引入 `dist/tokens.css`（原生 CSS）、`dist/tailwind.theme.css`（Tailwind v4 `@theme`）或 `dist/tailwind.preset.cjs`（Tailwind v3）

常用参数：
- `--tint subtle|pure|warm|cool`：调整背景灰倾向（默认 `subtle`，微带一点主色调）
- `--no-semantic`：只留主色和危险红，不生成成功/警告/提示色
- `--out ./my-theme`：指定输出目录

## 给 AI 用的约束检查

```bash
# 从 tokens/ 重新编译 CSS
pnpm tokens:build

# 查亮暗对比度和角色规范（加 --scan ./src 可扫源码里有没有硬编码 Hex）
pnpm tokens:check
```

## 它是怎么算的

1. **钉死纸面与中性灰（OKLCH）**：取主色色相、压低彩度，按目标对比度反解出亮暗两套背景、卡片、分割线和正文灰，避免页面灰蒙蒙或偏色。
2. **算交互色阶（Adobe Leonardo）**：以钉死的纸面为底，分别算按钮、链接和 Hover 态；暗色模式用独立高亮种子重算，不拿亮色硬反色。
3. **提示色异色分离**：生成红/绿/黄/蓝状态色；若主色恰好撞上某种状态色，自动把提示色色相挪开（≥35°）。
4. **角色映射与双标准校验（Primer + WCAG / APCA）**：填入 `fgColor` / `bgColor` / `borderColor` / `focus` 槽位，同时跑 WCAG 2.1 和 APCA（`apca-w3`）验对比度。

## 边界

只解决 UI 界面配色与代码颜色约束，不做品牌 Logo 艺术配色，也不管印刷 CMYK。

<details>
<summary>仓库结构</summary>

- `scripts/generate-color-system.mjs`：核心生成器（1 个 Hex → 全套产物）
- `scripts/build-color-tokens.mjs` & `check-color-tokens.mjs`：DTCG 编译与防写乱检查器
- `color-roles.md`：语义角色职责与使用禁忌表
- `SKILL.md` & `llms.txt`：给 AI Agent 读的技能说明与摘要

</details>

## License

[MIT](./LICENSE)

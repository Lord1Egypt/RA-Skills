# Robot Paper Post

机器人 / 具身智能论文深度推文写作技能包。

这一版重点解决了一个老问题：**插图流程不能再依赖 skill 安装阶段自动跑 npm / Playwright。**

因此，`v1.3.0` 开始，默认配图工作流改成：
- **优先从 arXiv HTML 直接提取官方 figure URL**
- **需要本地图时，再用 PowerShell 脚本下载**
- **浏览器自动化截图降级为可选增强，而不是默认硬依赖**

这样做的好处是：
- 安装 skill 后即可使用默认图文流程
- 不再被 Node.js / Chromium 环境卡住
- 更接近这次 Fast-WAM 文章里已经验证过的产出方式

## 快速安装

```bash
npx clawhub@latest install robot-paper-post
```

## 这版能做什么

| 能力 | 描述 |
|------|------|
| 多源检索 | 自动搜索论文原文、GitHub 代码、项目主页、演示视频 |
| 核心拆解 | 提取研究问题、方法创新、实验数字、局限性 |
| 技术溯源 | 梳理研究团队与相关工作的演进脉络 |
| 深度撰写 | 生成适合公众号发布的完整技术推文 |
| **零额外安装配图** | 直接提取 arXiv figure 并插入文章，不依赖 Playwright |
| 本地素材下载 | 按需把论文图片下载到文章目录，方便离线交付 |

## 为什么不再把 Playwright 设成默认依赖

因为 skill 安装通常只会安装 skill 文件本身，不会自动执行：

```bash
npm install
npx playwright install chromium
```

如果把截图流程建立在这些命令上，安装成功 ≠ 可复现成功。

所以现在的默认路径改成：
1. 先从 arXiv HTML 提取官方图片 URL 和图注
2. 能直接用远程图就直接插文稿
3. 用户要求本地素材时，再下载到文章目录
4. 只有确实需要整页截图 / GIF / canvas 内容时，才考虑浏览器自动化

## 目录结构

```text
robot-paper-post/
├── SKILL.md
├── README.md
├── clawhub.json
├── references/
│   ├── paper-structure.md
│   ├── tech-terms-glossary.md
│   ├── research-teams.md
│   ├── classic-papers.md
│   └── image-insertion-workflow.md
├── assets/
│   └── post-template.md
└── scripts/
    └── extract_arxiv_figures.ps1
```

## 默认配图工作流

### 方案 A：直接插入官方远程图（推荐）

适合：
- 需要快速生成可预览 Markdown
- 不要求离线打包图片
- 论文的 arXiv HTML 中能直接拿到 figure URL

插图格式示例：

```markdown
![Figure 1：三类 WAM 范式对比](https://arxiv.org/html/2603.16666v1/x1.png)

*图 1：解释这张图对应正文哪个观点，以及为什么重要。*
```

### 方案 B：下载本地图片再引用

适合：
- 需要离线交付
- 需要把图和文稿一起交给公众号后台
- 希望图片与文章目录一起打包

Windows 命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/extract_arxiv_figures.ps1 -ArxivId 2603.16666 -OutputDir .\paper_imgs -Download
```

脚本会生成：
- `paper_imgs/figures.json`
- `paper_imgs/arxiv_fig_1.png`
- `paper_imgs/arxiv_fig_2.png`
- ...

然后可在文稿中使用：

```markdown
![Figure 1：三类 WAM 范式对比](paper_imgs/arxiv_fig_1.png)
```

## 文章插图的放置规则

默认只插 3 到 5 张图，按正文结构放：

1. **问题意识 / 范式对比** → 放 Figure 1 一类总览图
2. **模型设计** → 放架构图
3. **主实验结果** → 放主结果表 / 图
4. **真实世界实验** → 放机器人实拍图或项目页演示图
5. **工程价值** → 放延迟 / 消融 / 效率图

## 可选增强：浏览器整页截图

如果论文项目页只有整页视觉效果、没有独立图片链接，或用户明确要整页截图 / GIF，才考虑浏览器自动化。

这条路径不是默认要求，也不是 skill 安装成功的前提。

## 打包技能

使用内置打包脚本：

```bash
python <skill-creator>/scripts/package_skill.py <path/to/robot-paper-post>
```

## 更新日志

- **v1.3.1**
  - 保留 `v1.3.0` 历史版本，补齐对外发布所需的版本元数据
  - 用于同步 GitHub 仓库与 ClawHub 的新版本发布
- **v1.3.0**
  - 移除默认 Node.js + Playwright + Chromium 硬依赖
  - 新增 `scripts/extract_arxiv_figures.ps1`，用零额外安装方式提取和下载 arXiv 图片
  - 新增 `references/image-insertion-workflow.md`，固化插图选图与落位规则
  - 重写 `SKILL.md`，把“可复现配图”做成默认流程
- **v1.2.0**
  - 新增自动截图采集能力
- **v1.1.0**
  - 新增经典论文索引
- **v1.0.0**
  - 初始版本

# Xiaohongshu Ops

> English version: see [README.en.md](./README.en.md)

一个用于 **全自动运营小红书** 的 OpenClaw skill，覆盖账号配置、内容生成、配图生成、发布执行与参考学习。

![Xiaohongshu Ops Architecture](./assets/xiaohongshu-ops-architecture.svg)

---

## 这是什么

`xiaohongshu-ops` 是一个面向小红书自动化运营的单 skill 仓库，不是单次发帖脚本。

它的目标是把一条完整的小红书运营链路收口到一个 skill 里：
- 配置账号运营规则
- 读取本地规则和学习笔记
- 生成标题、正文、分页结构
- 选择图片策略并生成图像资产
- 通过独立浏览器自动发布
- 以参考模式持续学习标题、图片和热点表达

---

## 主要能力

### 1. 自动配置运营规则
- 配置可复用的小红书运营 profile
- 读取 `data/xiaohongshu/` 下的本地规则与风格笔记
- 管理标题长度、正文长度、图片模式、自动学习开关等参数

### 2. 自动生成内容
- 从 topic / angle 一路编排到可发布资产
- 生成小红书风格标题、正文、分页结构
- 支持中英混合标题在 20 字内自然重写
- 按配置控制正文长度

### 3. 自动生成图片资产
- 支持图片模式：`stock` / `cards-lite` / `mixed`
- 优先真实相关图，轻卡片兜底
- 生成 `post.json`、`pages.json`、PNG 目录等发布资产

### 4. 自动发布到小红书
- 通过独立浏览器发布链自动发布到小红书
- 使用独立 profile，避免与日常浏览器混用
- 适合作为自动运营链路的一部分运行

### 5. 自动学习参考
- 支持 daily reference-only 自动学习
- 学习标题表达、图片风格、相关热点
- 不黑箱改主 profile，只把结果沉淀为本地参考

---

## 目录结构

```text
xiaohongshu-ops/
├── README.md
├── README.en.md
├── SKILL.md
├── .gitignore
├── assets/
│   └── xiaohongshu-ops-architecture.svg
├── references/
└── scripts/
```

本地运行时配置推荐放在：

```text
data/xiaohongshu/
├── profile.json
├── rules.md
└── style-notes.md
```

---

## 文件职责

### `SKILL.md`
skill 主说明，给 agent 用。

### `references/`
按需加载的参考文档，放规则、流程、图片来源、发布说明等。

### `scripts/`
低自由度执行脚本，适合稳定、可重复的步骤。

### `assets/`
仓库展示或输出要用的静态资产，例如架构图。

### `data/xiaohongshu/`
本地配置层，不一定要跟 skill 一起公开。

---

## 关键脚本

- `scripts/init_profile.js` — 初始化 / 更新 profile
- `scripts/run_ops_once.js` — 跑一轮完整小红书 ops 流程
- `scripts/build_xhs_post.js` — 组装图文资产
- `scripts/select_image_mode.js` — 选择图片策略
- `scripts/build_image_pipeline.js` — 构建图片生成/选图链路
- `scripts/fetch_stock_images.js` — 获取或规划图库图候选
- `scripts/generate_xhs_cards.js` — 生成卡片图
- `scripts/xhs_independent_publish.js` — 通过独立浏览器发布

---

## 行为边界

- 优先真实相关图，轻卡片兜底
- 不去水印，也不提供去水印指导
- 自动学习是参考模式，不会偷偷改主配置
- 运行产物是临时工作文件，不是长期内容库存

---

## 单独仓库使用

如果你想把这个目录单独作为 Git 仓库管理：

```bash
cd skills/xiaohongshu-ops
git init
```

建议：
1. 保留本目录下的 `.gitignore`
2. 运行时账号配置留在仓库外，或者只公开脱敏样例
3. 在仓库首页说明本地 `data/xiaohongshu/` 结构

---

## 注意事项

- 不要提交临时上传/测试输出
- 不要提交浏览器 profile 或登录态
- 如果公开 profile 示例，先检查是否包含账号偏好或私有运营信息

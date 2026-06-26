# 发布到 GitHub 与 ClawHub（维护者）

我无法替你完成「在网站上点提交」这一步；按下列清单操作即可。

## 1. 独立 Git 仓库（推荐）

把本目录作为 **仓库根目录**（不要多包一层文件夹）：

```text
twitter-query/
├── SKILL.md
├── README.md
├── LICENSE
├── claw.json
├── clawhub.json
├── PUBLISH.md
├── .gitignore
└── scripts/
    ├── query_by_user.py
    └── query_by_keyword.py
```

在 GitHub 新建仓库，例如 `twitter-query`，推送 `main`。

## 2. 替换作者与链接（若你不是 `alexander10011`）

全局替换：

- `alexander10011` → 你的 GitHub 用户名或组织名
- `Alex Wang` → 你的名字（`LICENSE` / `claw.json` / `clawhub.json`）

涉及文件：`README.md`（徽章与 `npx` 示例）、`claw.json`、`clawhub.json`、`LICENSE`（可选）。

## 3. ClawHub

1. 打开 [ClawHub](https://clawhub.ai)，使用当前平台要求的流程：**关联 GitHub**、**新建 Skill** 或 **从仓库导入**（以 ClawHub 当时文档为准）。
2. 确保 listing 的 **slug** 与 `npx skills add <owner>/twitter-query` 一致。
3. 上架后把 README 里徽章链接改成你的真实页面，例如：  
   `https://clawhub.ai/<你的owner>/twitter-query`

## 4. 验证

```bash
npx skills add <owner>/twitter-query
export TWITTER_API_KEY="..."
python3 scripts/query_by_user.py elonmusk --max-pages 1
```

## 5. 合规与扫描

- Skill 仅向 **twitterapi.io** 发 HTTPS 请求；不在仓库内收集用户数据。
- 若静态扫描误报，可引用 `claw.json` 中的 `privacy.externalServices` 说明，必要时附 OpenClaw 安全扫描结论（参考你其他 Skill 的申诉材料写法）。

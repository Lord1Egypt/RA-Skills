# 官方 CLI 安装与网页 CDP 兜底

> **优先用 `scripts/publish.py`**（自动化、含预检与 WAF 判定）。
> 本文件覆盖：手工安装/修复官方 CLI、以及 CLI 不可用时走网页的兜底路径。

## 官方 CLI 安装（2026.8.5+，支持 publish）

官方教程：https://skillhub.cn/tutorials#publish-via-cli

```bash
# 官方引导脚本（会拉 COS 上的 kit 包）
curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
```

**Windows 直接可用，不必 WSL** —— kit 核心是纯 Python 的 `skills_store_cli.py`（约 226KB），
只用 stdlib（`urllib` + 手工 multipart，零依赖）。手工装法（跳过 openclaw 插件注入）：

```bash
# 1. 取 kit（引导脚本真正下载的是这个 tar）
curl -o latest.tar.gz https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz
# 2. 解压出 cli/ 目录，把这几件拷到 ~/.skillhub/
cp cli/skills_store_cli.py cli/skills_upgrade.py cli/version.json cli/metadata.json ~/.skillhub/
# 3. wrapper 指到你的 Python（Windows 上 #!/usr/bin/env bash 的 wrapper 会被当 WSL 触发，别用）
```

### Windows 上的四个坑

1. **wrapper 触发 WSL**：官方 wrapper 是 `#!/usr/bin/env bash` + `exec python3 ...`。
   在 Windows Git Bash 下执行 `~/.local/bin/skillhub` 会被 intercept 成「启动 WSL」并报
   `Windows Subsystem for Linux has no installed distributions`。**直接调 Python 跑脚本**最稳。

2. **PATH 里有旧版 0.4.1**：managed node 目录下有个旧 `skillhub`，它没有 `publish`，
   会报 `unknown command 'publish'`。**别被它骗了**，用绝对路径或直调 Python。

3. **`bash` 自身可能指向 WSL stub**：`which bash` 得到 `/c/WINDOWS/system32/bash`，
   于是 `bash ~/.local/bin/skillhub` 同样触发 WSL 报错。用**绝对路径**调 Git Bash：
   ```bash
   /usr/bin/bash "C:/Users/DELL/.local/bin/skillhub" -v     # → skillhub 2026.8.5
   ```
   更省事：额外写一个 `~/.local/bin/skillhub.cmd`（`@echo off` + 绝对 python.exe + 脚本路径），
   在 Windows 原生 shell 里可直接敲 `skillhub`。

4. **`python3` 可能是坏的可执行文件**：`<managed-python>/versions/3.13.12/python3.exe`
   在本机是 0 字节残骸，被它 shadow 后一切 `python3` 调用都触发 Store stub。
   判据：`python.exe -c "print(1)"` 正常、`python3 -v` 报 Store。**wrapper 里写死 `python.exe`。**

## 登录

1. 浏览器 https://skillhub.cn/dashboard/keys → **创建 API key** → 一次性显示 `skh_xxx`（**只显示一次**）。
2. `skillhub login --key skh_xxx --host https://api.skillhub.cn` → `✓ Logged in as @handle`。
3. `skillhub auth whoami` 验证（端点 `GET /api/v1/auth/me`）。
4. Token 落盘在 `~/.skillhub/credentials.json`，结构为 `{"user": {"token": "...", "host": "..."}}`。

## CLI 的目录收集 vs 服务端白名单（**必踩的坑**）

CLI 用 `_collect_skill_files` 递归收集，**只排除** `.git/.idea/.vscode/node_modules/__pycache__`
和 `.pyc/.DS_Store/Thumbs.db`。它**不排除** `.gitignore` / `LICENSE` / `README.md` ——
于是直接 `publish <skill目录>` 会报：

```
请求失败 (400): 不允许的文件类型: .gitignore
```

**对策：用 `scripts/publish.py`（已按白名单过滤），或先手打白名单 zip 再 `publish <zip>`。**

## CLI 必填 frontmatter

CLI 校验 `slug`、`version`、`displayName`（缺一即 `die`）；
`summary` / `license` / `homepage` / `tags` / `description` 会一并进 payload。

> 注意与网页向导不同：**网页只认 `name`，CLI 认 `slug`，两边都得写。**

## 网页路径（CLI 不可用时的兜底）

### 创建 API key（网页唯一必要步骤）

1. `https://skillhub.cn/dashboard/keys` → 点 **「创建 API key」**。
2. 弹窗「创建 API Token」→ 名称可留空 → 点 **「创建」**。
3. 页面上**一次性**出现 `skh_<64hex>`，立刻复制。可用 CDP 抓：
   `document.body.innerText.match(/skh_[A-Za-z0-9]+/)`。
4. 转 CLI：`skillhub login --key skh_xxx --host https://api.skillhub.cn`。

### 发布新技能向导（`/dashboard/publish`）

点侧栏「发布 Skill」后**不是直接出表单**，而是先到「选择发布类型」，
必须再点 **「发布 Skill（最快上架）」** 卡片才进表单。

表单字段 id：`#skill-slug` / `#skill-displayName` / `#skill-summaryZh` / `#skill-version`。
zip 输入框按 `accept=".zip,application/zip"` 选（另一个带 `webkitdirectory` 的是文件夹输入）。

### 更新已存在的 Skill

`/dashboard/publish` 是**发布新技能**向导，**不能**用来升版本——
填入已存在的 slug 会报 `Slug 不可用`（这是「已被占用」的正确提示，不是 bug）。

升版本正确路径：

1. 进 **Dashboard → 我的 Skills**（`/dashboard`），找到目标卡片。
2. 卡片右下角：`版本历史` / `评测报告` / **`更新`** / `下架`。点 **「更新」**（它是 `<span>` 不是 `<button>`）。
3. 弹出 **「更新 Skill」** 对话框。
4. 上传新 zip → 填**递增的版本号** → 填**变更说明**。分类标签会沿用当前版本。
5. 提交后状态变「**安全审核中**」，版本号更新为新版本。

**多卡片锚定坑**：每张卡片的「更新」都是独立 `<span>`，脚本必须**按卡片归属定位**，
否则会点到别的 Skill。稳健做法：先 `document.querySelector('a[href*="<目标slug>"]')` 拿宿主 `<a>`，
再 climb 到「只包含该 slug、且含一个『更新』span」的最小祖先元素。
**别用 `closest('div[class*=rounded]')`**——所有卡片常包在同一个外层圆角容器里，会误命中第一张。

**false-positive 提醒**：分类标签字段的占位符文案就是「请选择分类标签」，
搜到它多半是占位符而非真实报错；真正的报错是「Slug 不可用」。

### 更新对话框：两个必踩的坑

1. **「复用当前版本」不可用于更新**。提交时必报 **`请至少上传一个文件`**。
   **更新一定要真的上传文件**（哪怕内容没变）——先本地递增 `version`、重打 zip 再传。
2. **文件输入框要选对**。对话框里有**两个** `input[type=file]`：
   - `[0]`：`accept=""`、`multiple=true` —— **文件夹**输入，别用。
   - `[1]`：`accept=".zip,application/zip"` —— 才是 **zip** 输入。

   用 `cdp.py file "input[type=file][accept*='zip']" <zip路径>` 精确命中。
   传成功后显示「已选择 N 个文件」，且两个 file input 会从 DOM 消失（属正常）。

### 分类标签：CDP 其实**能**选中

流程：点开「请选择分类标签」→ 一级分类面板 → 选一级后展开二级面板。

**关键：点 `<input>` 而不是 `<label>` 或 `<li>`**。二级选项结构是 `LI > LABEL.group > SPAN`：

```js
// ✅ 有效：直接 click 内部 input
var lab=[...document.querySelectorAll('label')].filter(e=>e.textContent.trim()==='流程自动化')[0];
lab.querySelector('input').click();   // checked=true，标签区随即出现该二级分类
// ❌ 无效：click(label) 或 click(li)
```

一级分类同理（`办公效率` 那个是 `<button>`，直接 click）。
选完对话框内会实时显示 `办公效率 流程自动化`。

> 此前记录「CDP 选不中分类标签」是**错误结论**——真因是点错了元素。
> 分类是选填，但「未分类」会让卡片显示很难看，能补就补。

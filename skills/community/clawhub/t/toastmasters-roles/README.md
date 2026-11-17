# 头马官员 · ClawHub 发布包

- **slug（URL 名）**：`toastmasters-official`
- **显示名**：`头马官员`
- **标签**：Business Operations / Collaboration / Productivity（商业运营 / 办公协同）
- **功能**：模拟头马（Toastmasters）俱乐部组织架构，把复杂任务按主席/VPE/VPM/VPPR 等角色拆分并分配职责。

## 本目录已就绪的内容
- `SKILL.md` — 已通过 `clawhub skill publish --dry-run` 官方校验，**无需修改即可发布**
- `.clawhub` — ClawHub 标记文件（空，社区惯例）
- `references/roles.md` — 角色职责手册

## 发布步骤（已实测验证）

```bash
# 1. 安装 ClawHub CLI（本机已装 v0.23.1；未装则执行下面一行）
npm i -g clawhub

# 2. 登录（需 clawhub.ai 账号，走设备流浏览器授权 —— 必须本人操作，agent 无法代登）
clawhub login

# 3. 在本目录发布（下面这条已用 --dry-run 验证通过，去掉 --dry-run 即为真实发布）
clawhub skill publish ./toastmasters-official-clawhub \
  --slug toastmasters-official \
  --name "头马官员" \
  --version 1.0.0 \
  --tags "Business Operations,Collaboration,Productivity"

# 4. 验证上架
clawhub search toastmasters-official
```

> 说明：
> - `--slug` 是 URL 名（kebab-case）；`--name` 是显示名（可中文），两者不同。
> - `--tags` 用**逗号**分隔（默认值 "latest"）。
> - 步骤 3 已在本机用 `--dry-run` 验证，输出 `Would publish toastmasters-official@1.0.0`（退出码 0）。
>   你只需先 `clawhub login`，然后去掉 `--dry-run` 直接发即可；也可登录后让 agent 代跑这条命令。

## 合规自检（已通过 dry-run 验证）
- ✅ `clawhub skill publish --dry-run` 输出 `Would publish toastmasters-official@1.0.0`（退出码 0）
- ✅ `name` 与目录 kebab-case 一致
- ✅ `description` 114 字（符合 50–200）
- ✅ `references/roles.md` 被 SKILL.md 引用且文件存在
- ✅ 无脚本、无外部调用（纯 prompt 技能，安全项稳过）

## 备选方案（不想碰 CLI）
去 https://clawhub.ai/import 网页，从 GitHub 公开仓库 import。但需先把本目录推到公开 GitHub 仓库，步骤反而更多，**不如 CLI 直接**。

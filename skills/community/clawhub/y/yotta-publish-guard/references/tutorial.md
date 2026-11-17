# 元守中文教程（新手全流程）

> 配套技能：元守 yotta-publish-guard（零依赖 Python 3.8+）
> 目标：把一个技能目录从「开发完」带到「可发布」——check → pack → versions → names → publish。

## 1. 教程目标与前置

- 学会三档校验模式（full / github / self）与各子命令；
- 理解推送闸门与 --force 的边界；
- 掌握三源发布命令计划与发布后验证；
- 前置：Python 3.8+；一个开发完、准备发布的技能目录（可用元造生成的脚手架练习）。

## 2. 发布就绪检查

```bash
python3 scripts/yotta_publish_guard.py check ./yotta-demo-tool
python3 scripts/yotta_publish_guard.py check ./yotta-demo-tool --with-audit --with-vetter --with-verify
```

- `[validate] 0 ERROR / 0 WARN` → READY（退出码 0）。
- 有 ERROR → BLOCKED（退出码 2）：逐行修复后重跑。
- 有 WARN → READY（退出码 1）：建议处理但可发布。
- 聚合 verdict 行：元安 / 元审 / 元信 未安装会显示「跳过（可选：安装后加 --with-* 复查）」。

## 3. 打包检查

```bash
python3 scripts/yotta_publish_guard.py pack ./yotta-demo-tool
```

期望 `结果: PASS`：包内无 pyc、SKILL / LICENSE / README 中英四件齐全。
若报「包内混入 pyc / __pycache__」→ 检查 package.json files 字段的 `!**/__pycache__` 否定模式。

## 4. 版本五件对齐

```bash
python3 scripts/yotta_publish_guard.py versions ./yotta-demo-tool
```

期望 `结果: PASS —— 全部对齐 0.1.0`。不一致会列出每处实际值，改齐后重跑。

## 5. 名称三通道查重

```bash
python3 scripts/yotta_publish_guard.py names ./yotta-demo-tool
```

期望「三通道全部空闲，可发布」（退出码 0）。
有 TAKEN → 改名或确认归属；有 UNKNOWN → 按提示走三通道手动查重链接。

## 6. 发布：先 dry-run 再执行

```bash
# 先看计划（默认 dry-run，不改任何东西）
python3 scripts/yotta_publish_guard.py publish ./yotta-demo-tool

# 只推 GitHub
python3 scripts/yotta_publish_guard.py publish ./yotta-demo-tool --github-only

# 确认无误后执行（--exec）；闸门未过默认阻断
python3 scripts/yotta_publish_guard.py publish ./yotta-demo-tool --channels github,npm --exec
```

- 闸门阻断（有 ERROR）：修好后重跑，或仅在显式确认后加 `--force`。
- 执行中任一步失败即中止并返回该命令退出码，便于定位。

## 7. 发布后验证

```bash
git ls-remote https://github.com/YottaMeta/<slug>.git main
npm view @yottameta/<slug> version --registry=https://registry.npmjs.org/
clawhub search --exact <slug> --limit 5
```

npm 新包有约 2-3 分钟传播延迟：tarball 先可见，packument 稍后；用 tarball + packument 双通道核对。
ClawHub 进入 pending scans，转公开后复核 verdict。

## 8. 常见问题与红线

- **check 报了对外口吻 ERROR**：README 出现内部口语（咱们 / 你自己 / 别忘了 等）或「AI 帮你装」
  类表述，改为中性专业措辞。
- **README 缺四方式安装**：补 npx / git clone / Download ZIP / install.sh 四段（发布规范 §3.3.1）。
- **版本五件为什么必须对齐**：SKILL / package / CHANGELOG / CLI / SKILL 正文版本行不一致会导致用户装到的版本与
  文档、徽章对不上。
- **--force 什么时候用**：仅在你确认「跳过闸门」是正确决定时显式使用；工具默认不会把未通过校验的内容发布出去。
- **自用技能**：不需要任何发布流程，`check --self-use` 只查本体即可。

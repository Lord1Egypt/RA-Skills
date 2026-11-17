# 三源发布流程与已踩坑清单（publish-flow）

> 配套技能：元守 yotta-publish-guard（零依赖 Python 3.8+）
> 本文档给出 `publish` 生成的命令计划对应什么、发布顺序、以及元阁踩过的坑（已固化进工具）。

## 1. 发布顺序与命令计划

`publish <dir>` 默认 dry-run 打印计划；`--exec` 按序执行，任一步失败即中止：

1. **git init / git add . / git commit** —— `feat: initial release v<版本>`
2. **gh repo create** —— `YottaMeta/<slug> --public --source=. --push --description <desc>`（必带 --description）
3. **gh repo edit --add-topic yottaskills** —— 聚合进 https://github.com/topics/yottaskills
4. **npm publish** —— `--registry=https://registry.npmjs.org/`（Windows 加可写 --cache）
5. **clawhub publish** —— `--name '<中文名> <slug>'`（整体带引号）+ `--owner yottameta`（org 归属，默认值）+ `--version` + `--categories` + `--topics`

只推 GitHub 用 `--github-only`（等价 `--channels github`）；`--channels npm,clawhub` 可任选组合。

## 2. 已踩坑清单（工具已固化）

| 坑 | 表现 | 工具处理 |
|---|---|---|
| git 代理 | Windows schannel 报 SEC_E_NO_CREDENTIALS | 计划注释提示加 `-c http.sslBackend=openssl -c http.proxy=<代理地址>`（具体地址按本机配置填写） |
| gh repo create 缺简介 | About 显示 "No description or website provided." | 计划必带 --description（可用 --description 覆盖） |
| ClawHub 漏传 --owner | 发布到 CLI 登录的个人账号（如 @gon-kvs）而非 org @yottameta | 计划默认带 `--owner yottameta`（`--clawhub-owner` 可改） |
| ClawHub --name 不带引号 | 展示名回退裸 slug，丢中文「元X」 | 计划整体带引号：`--name '元X yotta-x'` |
| ClawHub categories 非法 slug | 报 Unknown skill category slug | 默认按安全/普通自动选 security / productivity（可 --categories 覆盖） |
| npm 缓存目录不可写 | 沙箱 / CI 环境报错 | Windows 自动加可写 --cache 临时目录 |
| npm 新包传播延迟 | packument 约 2-3 分钟才可见 | 发布后验证用 tarball + packument 双通道 |

## 3. 推送闸门

`publish` 前先跑内置校验（full 或 github 档）：有 ERROR 默认阻断并打印原因；
`--force` 仅显式授权后可用（输出会标注「--force 已显式授权」）。

## 4. 发布后验证（建议人工复核）

```bash
git ls-remote https://github.com/YottaMeta/<slug>.git main        # GitHub main 与本地一致
npm view @yottameta/<slug> version --registry=https://registry.npmjs.org/   # npm latest
clawhub search --exact <slug> --limit 5                          # ClawHub 条目与 verdict
```

- npm 传播延迟：tarball 先可见，packument 稍后；用 tarball sha1 + packument 双通道核对。
- ClawHub pending scans：提交后进入扫描队列，转公开后复核 verdict。

## 5. 渠道选择建议

- 只推 GitHub（无 npm / ClawHub 需求）：`--github-only`，闸门自动用 github 档（不强制
  package.json / 中英 README / publish.yml）。
- 全渠道：默认即可（full 档：中英 README 四方式 + package.json 等齐全）。
- 自用技能：不发布，用 `check --self-use` 只查本体。

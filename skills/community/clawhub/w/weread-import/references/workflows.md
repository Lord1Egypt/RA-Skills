# weread-import 工作流

## 0. 发版前验证流程

适用场景：准备提交、打 tag、发 GitHub release 或上传 ClawHub 之前。

这是默认流程，不是可选流程。发版前必须先完成验证。

### 0.1 自动测试

```bash
node --test
```

### 0.2 本地真机 Gateway 探针

目的：确认当前 repo 代码在官方 Gateway 下可用。

只读验证示例：

```bash
node --input-type=module -e "
import { getGatewayNotebookBooks } from './src/gateway.mjs';
const books = await getGatewayNotebookBooks({ count: 20 });
console.log({ books: books.length, first: books[0]?.title || null });
"
```

说明：

- 需要先配置 `WEREAD_API_KEY`
- API Key 获取路径：打开微信读书 App 最新版 -> 我的 -> 右上角设置按钮 -> 微信读书 Skill -> 快速配置第 2 步 -> 获取 API Key
- Gateway 是默认后端；浏览器/Cookie 只作为旧链路或兜底链路

### 0.3 本地真机完整导出

目的：确认当前 repo 代码跑完整导出时没有真实环境问题。

规则：

- 输出目录必须使用 `/tmp/...`
- 不要直接写正式 Reading 目录

示例：

```bash
OUT=$(mktemp -d /tmp/weread-verify.XXXXXX)
bash ./scripts/run.sh --all --output "$OUT"
```

如需验证旧链路 smoke test：

```bash
OUT=$(mktemp -d /tmp/weread-web-verify.XXXXXX)
bash ./scripts/run.sh --all --no-gateway --cookie-from browser-managed --output "$OUT"
```

### 0.4 本地 staging 安装态验证

目的：确认当前修复在“安装后的 skill 目录”里也可用，而不是只在 repo 工作树里可用。

规则：

- 先从当前 repo 生成一个隔离的 staging skill 目录
- 在 staging 目录中执行，与真实运行命令尽量保持一致
- 输出目录仍然使用 `/tmp/...`
- 不要直接覆盖正在服役的正式 skill 安装目录

示例：

```bash
STAGING_DIR="$(bash ./scripts/prepare-staging-skill.sh)"
OUT=$(mktemp -d /tmp/weread-staging-verify.XXXXXX)
bash "$STAGING_DIR/scripts/run.sh" \
  --all \
  --output "$OUT"
```

如果你还需要验证某个具体 agent 平台的安装态，可以在 staging 验证通过后，再额外补一轮该平台的 smoke test；但默认发版门槛不依赖某一个特定 agent。

### 0.5 只有全部通过后才发版

发版前必须同时满足：

1. `node --test` 通过
2. 本地真机 Gateway 探针通过
3. 本地真机完整导出通过
4. 本地 staging 安装态验证通过

只有这 4 项都通过，才允许：

1. 提交代码
2. bump 版本号
3. 打 tag
4. 发 GitHub release
5. 上传 ClawHub

## 1. 首次导入

适用场景：已确定输出目录，将微信读书笔记导入到 Obsidian 或其他目录。

```bash
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading"
```

如果尚未配置 `WEREAD_API_KEY`，先让用户从 CLI 输出的选项中选择：配置 Gateway、受管浏览器旧链路、外部 Chrome 旧链路或手动 Cookie。Agent 不要自行切换到 Cookie。

## 2. 临时验证后再写入正式目录

适用场景：修改了模板、合并逻辑、frontmatter 或 tags，需要先确认输出格式。

先输出到临时目录：

```bash
bash ./scripts/run.sh --book "自卑与超越" --output /tmp/weread-verify --force
```

确认无误后，写入正式目录：

```bash
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading" --force
```

## 3. 重新渲染已有文件

适用场景：模板、frontmatter、tags 或删除归档逻辑发生变化后，需要重新生成。

```bash
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading" --force
```

## 4. 自定义 frontmatter tags

通过命令行参数：

```bash
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading" --tags "reading/weread,book"
```

或通过环境变量：

```bash
WEREAD_TAGS="reading/weread,book" bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading"
```

## 5. 定时同步

适用场景：通过 cron 或 agent 定时任务自动同步全部书籍。

```bash
bash ./scripts/run.sh --all --output "/path/to/Reading"
```

注意事项：
- 不加 `--force`，依赖增量机制跳过无变化的书籍
- 默认推荐 Gateway，需要 `WEREAD_API_KEY`
- 旧 cron 如果含 `--cookie-from` 或 `--cookie`，会继续按 web 后端执行
- `--no-gateway --cookie-from browser-live` 适合复用已有外部 Chrome CDP
- `--no-gateway --cookie-from browser-managed` 适合隔离会话，避免影响主浏览器其他站点登录
- `browser` 仅作为 `browser-managed` 的兼容别名
- web 旧链路前提是对应 Chrome 已登录微信读书
- 默认受管浏览器使用隔离 profile，不会同步默认 Chrome 的整份登录态
- 默认隔离 profile 目录为 `~/.weread-import-profile-isolated`
- 如需保留旧的 profile 同步行为，显式设置 `WEREAD_PROFILE_SYNC_MODE=legacy`
- 失败时直接报告错误，不要重试或变更参数

## 6. 常见问题

### 缺少 WEREAD_API_KEY

表现：CLI 提示未配置 `WEREAD_API_KEY`。

处理步骤：
1. 优先建议用户配置 Gateway。API Key 获取路径：打开微信读书 App 最新版 -> 我的 -> 右上角设置按钮 -> 微信读书 Skill -> 快速配置第 2 步 -> 获取 API Key；然后执行 `export WEREAD_API_KEY=<你的apikey>`
2. 如果用户明确不用 Gateway，可让用户选择 `--no-gateway --cookie-from browser-managed`、`--no-gateway --cookie-from browser-live` 或 `--no-gateway --cookie '...'`
3. 不要在用户未选择时自行改用 Cookie

### 登录过期 / 业务错误

表现：CLI 报错，提示业务错误、登录过期或浏览器中无可用 cookie。

处理步骤：
1. 如果是 Gateway 鉴权失败或 `upgrade_info`，直接报告配置或升级要求，不回退
2. 如果是 web 旧链路，确认 Chrome 远程调试实例仍在运行且已登录微信读书
3. 若是 `browser-live`，确认外部 CDP 仍在；若是 `browser-managed`，确认隔离窗口中的微信读书仍已登录
4. 若仍失败，先按 Gateway 探针或 web smoke test 区分是官方 Gateway、cookie、浏览器上下文还是 CDP/环境问题

### 避免影响正式笔记

先输出到 `/tmp/...` 临时目录验证，确认格式无误后再写入正式目录。

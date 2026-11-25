# 运行、本地加载与打包

## 1. 依赖

| 依赖 | 版本要求 | 检查命令 |
|---|---|---|
| `node` | ≥ 18（脚本零第三方依赖，不需要 `npm install`） | `node --version` |
| `alipay-bot` | 官方 `@alipay/agent-payment`，**固定 `1.0.31`** | `alipay-bot --version` |

本 Skill 与官方买家支付能力使用**同一套 Node 运行时**，不需要 Python、pip 或其他语言环境。
缺少 `alipay-bot` 时按 alipay-payment-skill 的 `references/command-recovery.md` 先校验 `dist.integrity` 再安装，
安装命令必须带固定版本（`npx -y @alipay/agent-payment@1.0.31 install`），**不得使用浮动版本标签**；未经用户同意不得安装。

## 2. 运行

```bash
# 只组装请求体（不发请求）
node "$SKILL_DIR/scripts/travel_aipay.mjs" body --query '杭州三日亲子游，2 大 1 小' --email buyer@example.com

# 取 402 账单（会把 query 与 email 发送到仙踪问道官方服务，先向用户披露）
node "$SKILL_DIR/scripts/travel_aipay.mjs" probe --query '...' --email '...' --country-code CN --language zh  # 未说明语言时显式传中文；英文用户传 --language en

# 用户明确同意付款后
node "$SKILL_DIR/scripts/travel_aipay.mjs" pay --confirm --session-id '<当前会话标识>'

# 付款后取货（复用同一订单）
node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --out-shake-no '<官方查询单号>'

# 渲染已保存的响应
node "$SKILL_DIR/scripts/travel_aipay.mjs" render --response ~/.xianzong-travel-aipay/delivery.json
```

通用选项：

| 选项 | 说明 |
|---|---|
| `--state-dir DIR` | 本地状态目录，默认 `~/.xianzong-travel-aipay` |
| `--timeout-ms N` | HTTP 超时毫秒，默认 `600000`（生成含 PDF 可能数分钟） |
| `--resource-url URL` | 覆盖资源地址（一般无需改动） |
| `--dry-run` | `probe` / `complete` 支持，只打印将发送的请求，不发送 |

> ⚠️ `probe` 是本 Skill **唯一在付款前发生的数据外发**：它把行程要素与邮箱 POST 到
> `https://api.riyuexinzhu.com/aipay/travel_consultant`。必须先按 SKILL.md 执行流程第 3 步向用户披露，
> 不得静默发送。`body` 与 `--dry-run` 不发请求，可放心先跑。
> 本 Skill 不读取任何密钥/凭据，也不向其他地方上报数据（无遥测、无其他域名）。

退出码含义见 `SKILL.md` 的状态矩阵。

## 3. 本地加载（让 Agent 发现本 Skill）

把整个 `xianzong-travel-aipay/` 目录放到宿主**自己的技能目录**即可。具体路径以宿主文档为准，
各宿主与版本可能不同，本文件不维护目录清单。

放置后校验：

1. `SKILL.md` 的 frontmatter `name` 必须与目录名 `xianzong-travel-aipay` 完全一致。
2. `description` 里必须含触发词（旅行方案 / 行程规划 / 仙踪问道 / 旅行咨询 PDF）。
3. 用户说"帮我做个杭州三日亲子游方案"应能命中本 Skill；说"我要付款"应交由官方支付能力处理。

### 本仓库内自用

仓库根的 `skills/` 不在宿主默认扫描清单里，需要在宿主设置里把它登记为技能目录
（VS Code / Copilot 为 `chat.agentSkillsLocations`，把 `skills` 置为 `true`），
否则只能由用户明确指定文件路径手动加载。

注意事项：

- 必须是**子目录 + SKILL.md** 的形态（`skills/aipay/xianzong-travel-aipay/SKILL.md`），不能直接把 `SKILL.md` 放在 `skills/` 下。
- 本 Skill 位于分类目录下，登记的是**父目录** `skills/aipay`（不是 `skills` 本身），否则一层扫描发现不到。
- 不要用软链指向别处（发现逻辑会做 realpath 包含性校验）。
- 改完设置后需重载窗口才会重新扫描目录。
- 本 Skill 只读取自身目录内的文件：不列举、不扫描、不读取其他任何 Skill 的内容；
  需要移交时只依据对方 `description` 判断，不打开对方文件。

## 5. 打包

```bash
bash "$SKILL_DIR/scripts/pack.sh"     # 产物：$PACK_OUT_DIR/xianzong-travel-aipay.zip（默认 /tmp）
PACK_OUT_DIR=/path/to/publish bash "$SKILL_DIR/scripts/pack.sh"   # 指定输出目录
```

> 打包产物**不会**写进技能目录，也不会在技能目录里生成 `dist/`：`dist/` 会被宿主扫描/被误打进发布包。
> 需要归档时用 `PACK_OUT_DIR` 指向外部发布目录（如 `deploy/skills`）。

脚本会先**校验必需文件齐全**再打包，缺任一项直接失败：

```text
SKILL.md  SKILL_en.md
references/402-travel-flow.md  references/install-and-pack.md
scripts/travel_aipay.mjs  scripts/pack.sh
```

> 这一步是必须的：正式发布包必须包含 `SKILL.md` 引用的所有 `scripts/` 与 `references/` 文件；
> 缺少文件会报 `Incomplete referenced artifact analysis`（“引用文件未被完整检查”）。

打包采用**白名单**：脚本只把正式发布所需的 `SKILL.md`、`SKILL_en.md`、`references/` 与 `scripts/` 复制到临时目录再压缩。本地运行状态、维护用测试目录与依赖目录从一开始就不参与正式包，不依赖任何排除清单。
本 Skill 不读取任何密钥或系统凭据，脚本只读可选的 `ALIPAY_BOT_BIN` 与宿主已有的会话 ID 变量。

打包后自检：

```bash
unzip -l "${PACK_OUT_DIR:-${TMPDIR:-/tmp}}/xianzong-travel-aipay.zip"
```

确认清单包含正式发布所需的 `scripts/`，且只含上面白名单里的正式交付文件（不含本地运行状态、维护用测试目录与依赖目录）。

若用官方安装器分发（`--skills-root` 填宿主自己的技能目录，路径以宿主文档为准）：

```bash
alipay-bot skill-install --package "${PACK_OUT_DIR:-${TMPDIR:-/tmp}}/xianzong-travel-aipay.zip" --skills-root '<宿主技能目录>'
```

## 6. 尚未提供的配置

本 Skill 无需填写任何密钥或服务端配置：账单签名、验付、履约确认全部在服务端完成。以下为需与支付宝服务市场登记保持一致的对外信息，已固化在 `SKILL.md`：

| 项 | 当前值 |
|---|---|
| 资源地址（正式服务，脚本默认） | `https://api.riyuexinzhu.com/aipay/travel_consultant` |
| 单次价格 | `0.99` 元/次 |
| 商品名 | `仙踪问道_旅行咨询` |
| 服务标识 | `API_7D36D49749854F1F` |

如服务市场登记地址、单价或商品名发生变更，需同步更新 `scripts/travel_aipay.mjs` 顶部的 `RESOURCE_URL` / `PRICE_CNY` / `GOODS_NAME` 与本文件。

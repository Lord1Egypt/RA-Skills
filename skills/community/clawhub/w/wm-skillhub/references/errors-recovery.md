# 错误恢复指南（Agent 必读）

两层错误勿混用：

| 层 | 出现位置 | 例子 |
|----|----------|------|
| **网关** | `success:false` → `error.code` | `INVALID_CLIENT`、`EC_BALANCE_EXHAUSTED`、`INSUFFICIENT_SCOPE` |
| **技能体** | `success:true` 但 `data.result.error` | `SCOPE_DENIED`、`CAPABILITY_NOT_MOUNTED`、`VALIDATION_FAILED` |

对用户：**先用人话说明卡在哪**，再给**可点开的落地页**（勿只甩错误码）。

## 落地页（open.winmale.com）

| 用途 | URL |
|------|-----|
| 安装技能后领凭证 / 登录 | https://open.winmale.com/get-started |
| 复制 AppId + API Key | https://open.winmale.com/skillhub/creds |
| 我的应用 / 用量 | https://open.winmale.com/console |
| **EC 充值**（打开充值弹层） | https://open.winmale.com/console?action=recharge 或 https://open.winmale.com/billing |
| 错误码文档 | https://open.winmale.com/docs?key=errors |
| EC / 限速说明 | https://open.winmale.com/docs?key=rate-limits |
| 管家首装合同（一次性） | https://open.winmale.com/install/skillhub.md |
| 管家技能页（指向首装，无围栏副本） | https://open.winmale.com/install/skills/wm-skillhub.md |

登录后会 **自动创建免费档「默认应用」**（`ensureDefaultApp`）；用户只需打开 `/get-started` 或 `/skillhub/creds` 复制密钥。

---

## 网关常见码 → 怎么修

| `error.code` | 对用户说 | Agent 动作 |
|--------------|----------|------------|
| `INVALID_CLIENT` | 凭证不对或已轮换 | 打开 **[/skillhub/creds](https://open.winmale.com/skillhub/creds)**，复制 **App ID** 与 **API Key**，写入本机 `WINMALE_CLIENT_ID` / `WINMALE_API_KEY`（或管家 `.env`）。**升级技能时勿覆盖已有密钥**；丢失才引导重拷。 |
| （无凭证 / 空 env） | 还没配开放平台应用 | 打开 **[/get-started](https://open.winmale.com/get-started)**：登录 → 自动建默认应用 → 去凭证页复制。 |
| `INVALID_TOKEN` | 令牌过期 | 重新 `POST /v1/oauth/token`；勿把过期 token 当密钥。 |
| `INSUFFICIENT_SCOPE` | 应用权限不够 | 打开 **`grant_url`**（优先用错误体里的链接）或 `https://open.winmale.com/console?appId={WINMALE_CLIENT_ID}&action=scopes&scope={need_scope}` → 勾选保存 → **重新换票**。禁止长篇手操步骤。 |
| `EC_BALANCE_EXHAUSTED` | 算力点（EC）用完 | 打开 **[/billing](https://open.winmale.com/billing)** 或 `/console?action=recharge` 充值；或等周补。**禁止**空转重试。 |
| `DAILY_EC_CAP_EXCEEDED` | 今日 EC 日顶用尽 | 说明等 UTC 日切，或充值/提档；见 `/docs?key=rate-limits`。 |
| `RATE_LIMITED` | 请求太频 | 退避重试；看 `details.window`。 |
| `POLICY_DENIED` | 沙箱禁止该能力 | 换合规写法 / 降级 L1；勿让用户「再试一次」无效操作。 |
| `SKILL_NOT_RUNNABLE` | 该 Pack 不能 skills/run | Role / xs-eval-guide 等按 SKILL 走 eval 或路由，勿硬 run。 |

历史别名 `QUOTA_EXCEEDED`：按 EC / 限流细分码处理。

---

## 技能体常见码 → 怎么修

| `data.result.error` | 对用户说 | Agent 动作 |
|---------------------|----------|------------|
| `SCOPE_DENIED` | 当前令牌缺业务权限 | 读 `need_scope` / **`grant_url`**；贴链接让用户授权后 **重新换票**；勿口述「设置→应用权限」路径。默认档已含提醒读写；若仍缺，多半是旧 app 未 ensure / 未换票。 |
| `CAPABILITY_NOT_MOUNTED` | 未挂载自选/提醒/选股等宿主能力 | 须带 **App 凭证** 调 API（非匿名）；控制台确认应用与 scope；换票后再跑。 |
| `VALIDATION_FAILED` | 参数不对 | 按返回 `message` 改 `args`（action/symbol/conditions…）。 |
| `REMOVALS_BLOCKED` | 整理关注会删票 | 预览后用户明确同意再 `allow_removals=true`。 |
| `NOT_FOUND` / `PATH_NOT_ALLOWED` | 资源或路径不允许 | 对齐技能白名单 / universe；勿编造。 |

---

## 升级 / 重装技能丢密钥（高频）

1. **不要**用安装话术里的示例密钥覆盖本机已有 `WINMALE_*`
2. 已有管家时：用 **升级话术** `GET .../install-prompt?kind=skillhub&mode=update`（不含密钥），或 `bash scripts/update-from-catalog.sh`
3. 若已丢：打开 https://open.winmale.com/skillhub/creds  
   - 未登录 → 先登录（会自动建默认应用）  
   - 在「我的凭证」复制 **App ID**、**API Key** 粘回 `.env`
4. 若页面提示轮换：仅当用户明确要求轮换时再点；轮换后旧 Key 立即失效

---

## Agent 话术模板（可直接改写）

**丢密钥：**  
「请打开 https://open.winmale.com/skillhub/creds ，登录后在页面复制 App ID 和 API Key，发给我写入本地配置（我不会在回复里完整回显密钥）。」

**EC 耗尽：**  
「当前应用的算力点（EC）已用完。请打开 https://open.winmale.com/billing 登录后充值，或到「我的应用」看余额；充好后告诉我再继续。」

**未登录 / 未建应用：**  
「请先打开 https://open.winmale.com/get-started 用赢麻了账号登录；系统会自动创建免费档默认应用，再到凭证页复制密钥。」

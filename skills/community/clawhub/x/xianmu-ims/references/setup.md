# 安装与接入引导（实例未安装 / 未运行时）

主技能（SKILL.md）其余部分的前提是实例可达；本域处理「实例连不上 / 可能还没装」——从零把用户带到可用，再回主流程。与官网在线版 [https://ims.miaoking.com/skill.md](https://ims.miaoking.com/skill.md) 同源对齐，官网为最新口径，本文件服务离线 / 技能包场景。

**触发**：SKILL.md「使用前提」步骤 0 探测失败；或用户表达「安装闲沐 / 下载闲沐 / 还没装 / 连不上」。

**角色边界**（与官网一致）：智能体只做无副作用的事——检测、生成配置、指路、验证。**不代替用户点任何确认弹窗，不代替用户创建 Token**（技术上可行也不做）。两件事必须用户亲手做：① 各环节确认弹窗自己点；② 创建并保管 API Token。

## 1. 可达性检测（先判断装没装）

有命令能力时（Windows PowerShell 用 `curl.exe`，Git Bash 直接 `curl`）：

```
curl.exe -s http://127.0.0.1:8066/api/v1/health
```

无命令能力时：让用户在浏览器打开 `http://127.0.0.1:8066`。判定：

- 返回 `"status": "up"` → 已在运行，回主技能流程；顺手记下 `version`（产品版本）与 `edition`（`free` / `pro`）。检测到 `free` **不影响接入**——MCP 调用免费版同样可用（物品条目 50 件内与专业版无差别），照常继续。
- 连不上（无响应 / 拒绝连接 / 超时）→ **不要直接断定未安装**：先问用户实例地址（NAS / Docker / 另一台电脑部署很常见），拿到地址替换 `127.0.0.1:8066` 再探一次；仍不通且用户确认本机未装 → 走 §2。

## 2. 安装引导（Windows 10 / 11 64 位，用户动手，你指路）

给用户的话术（照抄）：

1. 打开官网 [https://ims.miaoking.com](https://ims.miaoking.com)，在「下载安装」区点下载按钮，得到 `XianMuIMS-<版本>-setup.exe`。
2. 双击运行安装包。若弹「Windows 已保护你的电脑」，点「更多信息 → 仍要运行」（安全机制，正常）。
3. 安装全程无需管理员权限，无需 Python / Node / MySQL。装完自动启动：任务栏出现「闲沐IMS工具箱」图标，浏览器自动打开 `http://127.0.0.1:8066`（没自动打开就点工具箱里的「打开系统」）。

弹窗预期——在对应环节**提前一句**告知用户，认关键词即可：**允许 / 信任 / 连接 / 仍要运行**，这些都是安全机制不是报错：

| 环节 | 可能弹出 | 用户动作 |
|---|---|---|
| 运行安装包 | SmartScreen「Windows 已保护你的电脑」 | 「更多信息」→「仍要运行」 |
| 安装过程 | UAC「是否允许此应用对设备进行更改？」 | 点「是」 |
| 客户端添加 MCP | 「是否允许连接此 MCP 服务器？」 | 点「允许 / 信任 / 连接」 |
| 工具首次调用 | 部分客户端逐次询问 | 点「允许」 |
| 安装完成后 | 托盘出现工具箱图标、浏览器自动打开系统页面 | 正常现象，无需处理 |

用户装完后用 §1 的 health 命令复验一次（`"status": "up"` 即成功）。补充口径：

- 下载直链与校验：从 [https://ims.miaoking.com/updates/manifest.json](https://ims.miaoking.com/updates/manifest.json) 的 `url` / `sha256` 字段取（每次发布后直指具体版本包），**不要自行拼接其他渠道链接**。
- 默认端口 8066；被占用时可在安装目录 `data/.env` 改 `APP_PORT` 后重启，下文所有地址同步替换。
- 数据全部存本机安装目录 `data/` 文件夹（Windows 默认 `%LOCALAPPDATA%\Programs\XianMuIMS\data`）。
- 首次启动默认单人模式，网页端免登录直达；若实例被配置为多人模式且尚未初始化，会进入 `/setup` 向导——让用户按向导创建管理员后再继续。
- 官方安装包目前只覆盖 Windows。NAS / Docker 自托管见官网部署文档 [https://ims.miaoking.com/docs/deploy.html](https://ims.miaoking.com/docs/deploy.html)；内网 / 无外网场景请联系客服。

## 3. 设置 API Token（用户亲手做，你不代建）

给用户的步骤（照抄）：

1. 在闲沐 IMS 页面左侧点「设置」→「API Token」。
2. 点「新建」，名字随意（如「AI助手」）。Token 的权限跟随当前登录的账号——单人模式默认账号就是管理员，初始化建分类 / 位置够用；多人模式请用管理员账号登录后再创建。
3. 创建后**立刻复制** `xmt_` 开头的 Token（只显示这一次，关掉就再也看不到；丢了就删掉重建一个）。
4. 把 Token 提供给本技能使用（或填入客户端 MCP 配置），**不要发给任何其他人或服务**。

单人模式说明：网页本身免登录，但 MCP 一律要求 Token（限流与审计挂在 Token 上）——即使用户说「我那个不用登录」，也必须走这一步。

## 4. 验证与接入（打通后回主流程）

- REST 验证：`GET BASE/api/v1/items?page_size=1`（带 `Authorization: Bearer` 头），返回 `OK` 信封即打通；返回 401 → Token 无效，回 §3 重建。
- 客户端要配 MCP 时的三要素：`url = BASE + /api/mcp`（类型选 Streamable HTTP，**不要选** stdio / 本地命令 / SSE 旧类型）+ 请求头 `Authorization: Bearer xmt_…`。标准配置 JSON（本机实例）：

```json
{
  "mcpServers": {
    "xianmu-ims": {
      "url": "http://127.0.0.1:8066/api/mcp",
      "headers": { "Authorization": "Bearer xmt_你的Token" }
    }
  }
}
```

- 地址必须是**运行客户端的那台机器**能访问到的地址（客户端与闲沐 IMS 同机才用 `127.0.0.1`；只读模式在 url 追加 `?mode=readonly`）。
- 写客户端配置文件前：先完整展示「将写入哪个文件、写入什么内容」，征得用户同意再写；保存后按客户端要求重启（如 Claude Desktop 须完全退出再重启），重启后可能再弹一次「是否允许连接」，提醒点允许。按客户端的具体配置路径见官网 [https://ims.miaoking.com/docs/api.html](https://ims.miaoking.com/docs/api.html)。
- 打通后回 SKILL.md 主流程；全新库建议顺势走「初始化引导」域（references/onboarding.md）。

## 5. 条件分支

### 5.1 专业版激活码（遇 `LIMIT_EXCEEDED` 或用户主动升级时）

MCP 调用免费版可用，免费版唯一门槛是**物品条目 50 件**（超限后新建档类操作返回 403 `LIMIT_EXCEEDED`，查询与已有物品的出入库不受影响）。升级指引（照抄给用户）：

1. 打开购买直达 [https://ims.miaoking.com/portal/buy](https://ims.miaoking.com/portal/buy) 购买专业版（一次付费，永久使用 v1.x）。
2. 到门户 [https://ims.miaoking.com/portal](https://ims.miaoking.com/portal) 取激活码（也会同步发到下单邮箱）。
3. 回到软件「关于」页，粘贴激活码完成激活——**需要联网访问一次门户完成设备绑定，之后日常使用全程离线**。
4. 激活后直接重试即可（已创建的 Token 继续有效）；若仍返回 `EDITION_REQUIRED`，重启一次闲沐 IMS（工具箱托盘退出再启动）再试。

购买与激活是用户在界面亲手操作；智能体不调用 `/license` 端点（SKILL.md 护栏禁触）。

### 5.2 AI 密钥（一句话指路）

AI 功能（如物品识别）的模型密钥由用户在「设置」页自行配置；智能体不代操作（护栏禁触 `/settings`）。

## 6. 连接层错误对照

| 现象 / 错误 | 含义 | 处置 |
|---|---|---|
| 无响应 / 拒绝连接 / 超时 | 实例未启动或地址不对 | §1 排查；确认未装走 §2 |
| 浏览器打不开 `127.0.0.1:8066` | 同上（无命令能力时的表现） | §1 → §2 |
| AUTH_REQUIRED (401) | Token 缺失 / 无效 / 已吊销 | 回 §3 重建 |
| EDITION_REQUIRED (403) | 免费版调裸 REST | 优先引导走 MCP（免费可用）；或 §5.1 升级 |
| LIMIT_EXCEEDED (403) | 免费版 50 件条目上限 | §5.1 升级，或删减条目 |
| RATE_LIMITED (429) | 超过 60 次/分 | 等待几十秒重试，减少请求频率 |

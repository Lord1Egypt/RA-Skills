# 🍣 sushiro-skill

> 一行命令查全国寿司郎实时排队。**无需 API key**，纯 `curl + jq`，秒级响应。

```
$ sushiro stores --waiting --limit=5
WAIT  STATUS  ID    CITY  AREA        NAME
260   OPEN    3014  北京  北京海淀区  中关村大融城店
135   OPEN    3037  济南  济南历下区  济南万象城店
10    OPEN    3045  北京  北京海淀区  西北旺万象汇店
10    OPEN    34    厦门  厦门湖里区  SM厦门店
5     OPEN    3004  北京  北京西城区  西单大悦城店
```

## 为什么有它

寿司郎中国小程序里查排队，每次都要：打开微信 → 找小程序 → 选城市 → 翻列表。

这个工具把那一步压缩到一条命令——更适合：

- **决定去哪家吃**：`sushiro stores --city=深圳 --waiting` 一眼看全市哪家不堵
- **接到 Claude / Cursor 当 skill**：自然语言问"望京哪家寿司郎人少？"自动调用
- **脚本化监控**：cron + `sushiro store 1012 --json` 推送通知
- **数据玩耍**：111 家门店实时 JSON，随便 `jq`

## 安装

```bash
git clone https://github.com/Gitnapp/sushiro-skill.git
cd sushiro-skill
ln -s "$PWD/scripts/sushiro" /usr/local/bin/sushiro   # 可选，加进 PATH
```

依赖：`curl`、`jq`（macOS 已自带，Linux `apt install jq` 即可）。

### 当作 Claude Code Skill

这是一个完整的 [Claude Code Skill](https://docs.claude.com/en/docs/agents-and-tools/skills)。链到 skills 目录后，Claude 会在你问"寿司郎/排队/等位"时自动调用：

```bash
ln -s "$PWD" ~/.claude/skills/sushiro
```

## 命令一览

| 命令 | 用途 |
|---|---|
| `sushiro summary` | 全国汇总：总门店数、营业数、各城市排队榜 |
| `sushiro stores [filters]` | 列出所有门店，支持 `--city=` `--area=` `--near=LAT,LNG` `--open` `--waiting` `--limit=N` |
| `sushiro store <id>` | 单门店详情（地址、座位数、坐标） |
| `sushiro wait <id>` | 一行结果：店名 + 当前排队数 |
| `sushiro search <keyword>` | 按店名 / 区 / 城市 / 地址搜索 |
| `sushiro areas` | 列出所有区名（共约 60 个） |
| `sushiro raw <path>` | 透传任意 `/wechat/api/2.0/<path>` |

所有列表类命令支持 `--json` 输出原始 JSON，方便管道。

## 示例

```bash
# 全国最堵的 10 家店
sushiro stores --waiting --limit=10

# 我家附近（南山区）哪家不用等
sushiro stores --area=南山区 --open

# 按经纬度排距离（深圳南头）
sushiro stores --near=22.55,113.92 --limit=5

# 单店实时
sushiro wait 3014
# → 中关村大融城店: wait=260 status=OPEN

# 抓 JSON 给图表
sushiro stores --json | jq 'group_by(.nameKana) | map({c:.[0].nameKana, w:map(.wait//0)|add})'
```

## 工作原理

调用寿司郎中国微信小程序后端 `crm-cn-prd.sushiro.com.cn` 的三个公开 endpoint：

```
GET /wechat/api/2.0/stores              # 全门店列表
GET /wechat/api/2.0/getStoreById        # 单店详情
GET /wechat/api/2.0/areas               # 区列表
```

Bearer token 是**小程序级别的共享凭证**（不绑定用户），硬编码在脚本里。
所以——**不需要登录、不需要 API key、不需要部署任何服务**。

完整字段说明见 [`references/api.md`](references/api.md)。

## 局限

- 仅覆盖**中国大陆**门店。日本 / 港澳台 / 海外用的是另一套 backend，本工具不支持。
- 是对小程序 API 的非官方使用。寿司郎若轮换 token，请用 `SUSHIRO_TOKEN=xxx` 覆盖，或来提 issue。
- `python-requests` / `httpx` 会被上游 CDN 指纹拦截，所以底层用 `curl`（已处理）。
- 别用来做爬虫高频压测——自用 / 低频 / 1 分钟一次以内不会有问题。

## 相关项目

- [sushiro-queue-monitor](https://github.com/Gitnapp/sushiro-queue-monitor) — 同一作者的 Vercel 部署版，带 Web UI、Redis 历史曲线、cron 快照。本仓库是它的"裸命令行 + skill"姊妹版。

## License

MIT

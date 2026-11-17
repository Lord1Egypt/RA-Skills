# wttr.in 速查（2026-10 live 校准）

## 命令速查
| 用途 | 命令 |
|------|------|
| 当前位置 | `curl wttr.in` |
| 城市 | `curl wttr.in/Beijing` |
| POI | `curl wttr.in/Eiffel+tower` |
| 机场码/域名/邮编/GPS | `/MUC` `/@wikipedia.org` `/94107` `/-78.46,106.79` |
| 只看当前 | `curl 'wttr.in/Beijing?0'` |
| 纯文本 | `?T`；去 emoji 字符 `?d`；去标题 `?q`；再去城市 `?Q`；去 Follow 行 `?F` |
| 一行 | `?format=3`；预设 1..4；自定义 `%`-notation |
| JSON | `?format=j1`（有 hourly）/`j2`（无 hourly） |
| Prometheus | `?format=p1` |
| PNG | `wttr.in/Beijing.png`；选项进文件名 `_0pq`、`background=RRGGBB`、`transparency=0..255` |
| 批量 | `wttr.in/{Beijing,Shanghai,Guangzhou}?format=3`（冒号形式只回最后一行！） |
| 月相 | `wttr.in/Moon`、`/Moon@2026-12-25`、`/Moon,+China` |
| v2 富数据 | `curl v2.wttr.in/Beijing`（日/夜字体 v2d/v2n） |
| v3 地图 | `v3.wttr.in/California.png` / `.sxl` |
| 帮助/函数/译者 | `/:help` `/:bash.function` `/:translation` |
| 备用域 | `wttr.is` 全路径等价 |

## %-notation（实测可用）
`%l`地点 `%c`图标 `%C`文本(⚠一行输出下 lang=zh 仍回英文，要中文词用全量视图) `%x`符号 `%t`温度 `%f`体感 `%h`湿度 `%w`风
`%p`降水 `%P`气压 `%u`UV `%m`月相 `%M`月龄 `%D %S %z %s %d`黎明/日出/天顶/日落/黄昏 `%T`本地时间 `%Z`时区
**死码勿用**：`%e`露点 `%H`最高 `%L`最低（服务端原样回显）。tmux 配置里的 `%H:%M` 是 strftime，别混淆。

## 语言
`?lang=zh` ｜ `zh.wttr.in/Beijing` ｜ `-H 'Accept-Language: fr'`。
zh 简体、zh-tw 繁体 OK；zh-hans/zh_cn/zh_HANT → ERR008。

## 单位
`?m` 公制 ｜ `?u` 英制 ｜ `?M` 公制+风 m/s

## 排障
- PNG 出 `fail`（非 PNG 字节）：多半是短选项 `t`——只认 `transparency=N` 长写法。
- JSON 解析失败：先 `head -c 200` 看是不是 `ERR0xx` 文本。
- 地点查无：`not found` 文本而非崩溃；POI 用 `+` 代空格。

## CLI 直通
`-V 0q` 任意视图字母组合 ｜ `--ansi` 保彩色 ｜ `--follow` 留 Follow ｜ png `--keep-title` 不去标题

## 集成
- tmux: `set -g status-right '#(curl -s wttr.in/Beijing?format=3&period=60)'`
- bash 函数: `eval "$(curl -s wttr.in/:bash.function)"` → `wttr Paris`
- 图片叠加: `convert src.jpg <(curl wttr.in/Oymyakon_pq_transparency=0.png) -geometry +50+50 -composite out.jpg`

完整说明见 SKILL.md；CLI 用 `python scripts/weather.py -h`。

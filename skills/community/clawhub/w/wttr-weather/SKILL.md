---
name: wttr-weather
description: Check weather via the free wttr.in service (all free capabilities, live-verified 2026-10). Use when the user mentions weather, forecast, temperature, moon phase, or 天气/预报/气温/月相 for any location. Covers: city/POI/Unicode/airport-code/@domain/ZIP/GPS locations; ANSI/plain/compact/HTML/PNG/JSON(j1,j2)/Prometheus/one-line outputs; view flags 0/1/2/n/q/Q/F/A/d/T; PNG opts (frame, background=RRGGBB, transparency=0..255); languages incl. zh/zh-tw (invalid codes return ERR008); Moon (/Moon, Moon@date, ,+region); v2 rich + v2d/v2n nerd-font, v3 map (PNG/Sixel); {a,b,c} batch with period= throttle; wttr.is drop-in; :help /:bash.function /:translation. Ships scripts/weather.py CLI.
---

# wttr.in 天气查询（全免费能力版）

wttr.in 是免费控制台天气服务。本技能以 2026-10 live 探针为准，逐项实测；服务端未实现的功能
不再写进文档（见文末「不支持清单」）。所有 URL 走 HTTPS；UA 为浏览器时自动 HTML，curl 默认 ANSI。

## 1. 地点形态（全部 live 验证）

| 形态 | 示例 | 说明 |
|------|------|------|
| 城市名 | `wttr.in/Beijing` | 任意语言 Unicode 名均可，如 `wttr.in/Москва`、`wttr.in/长城` |
| 任意 POI | `wttr.in/Eiffel+tower` | 空格用 `+` |
| 机场三字码 | `wttr.in/MUC` | IATA 码直接命中机场 |
| 域名 | `wttr.in/@wikipedia.org` | `@` 前缀按域名定位 |
| 邮编 | `wttr.in/94107` | 美国邮编等 |
| GPS 坐标 | `wttr.in/-78.46,106.79` | `纬度,经度` |
| IP 定位 | `curl wttr.in` | 不带路径按请求 IP |
| 地点别名 | `~` 前缀 | `/~Eiffel+tower` 与直接 `/Eiffel+tower` 等效 |

## 2. 输出格式

- **ANSI 终端卡片**：默认（curl UA）。`?A` 强制 ANSI（即使浏览器 UA）。
- **纯文本**：`?T` 关闭颜色转义；`?d` 限制到标准控制台字体字符（去 emoji）。
- **视图详略**：`?0` 只看当前；`?1` 当前+今日；`?2` 当前+今+明；完整三天为默认。
  `?n` 窄版（只昼夜两栏）；`?q` 去“Weather report”标题行；`?Q` 再去城市名；`?F` 去 Follow 引导行。
  可组合：`?0qT`。
- **HTML**：浏览器 User-Agent 自动返回网页版。
- **PNG**：地点后加 `.png`。选项写在文件名里，短选项连写、长选项用 `_` 分隔：
  选项规则：短字母连写、顺序即语义无强制排列（惯用 `0`/`1`/`2` 在前，再 `p`、`q`），长选项以下划线分隔附后、`lang=` 放最后。
  `wttr.in/Beijing_0pq.png`（当前天气+边框+去标题）、
  `wttr.in/Beijing_background=00aaaa.png`（背景色 RRGGBB）、
  `wttr.in/Beijing_transparency=150.png`（0..255，255 不透明）、
  `wttr.in/Beijing_0qp_lang=zh.png`。长语言选项放最后。
- **JSON**：`?format=j1` 完整（3 天 × 每日 8 组 hourly）；`?format=j2` 精简——
  `weather[]` 每天**无 hourly**，只留日级 max/min/avg/uvIndex/astronomy/sunHour（实测键集，别盲猜）。
- **Prometheus**：`?format=p1`，`# HELP` 开头的指标文本。
- **一行输出**：预设 `format=1..4`（1 天气+温度｜2 加风温湿度｜3 带城市名｜4 全细节）。
- **自定义 `%-notation`**，实测可用集：

| 码 | 含义 | 码 | 含义 |
|----|------|----|------|
| `%l` | 地点 | `%p` | 降水 mm/3h |
| `%c` | 天气图标(emoji) | `%P` | 气压 hPa |
| `%C` | 天气文本 | `%u` | UV 指数 1-12 |
| `%x` | 天气纯文本符号 | `%m` | 月相 |
| `%t` | 实际温度 | `%M` | 月龄天 |
| `%f` | 体感温度 | `%D %S %z %s %d` | 黎明/日出/天顶/日落/黄昏 |
| `%h` | 湿度 | `%T` | 本地当前时间 |
| `%w` | 风向风速 | `%Z` | 本地时区 |

## 3. 批量与节流

- **一次多家**：花括号 `wttr.in/{Beijing,Shanghai,Guangzhou}?format=3` 每行一家全输出。
  注意冒号形式 `Beijing:Shanghai` 是**重复查询**（旧客户端轮询场景），一行输出下只回最后一家的值——
  想要全量请用花括号。
- **节流**：`&period=60` 参数（重复查询场景两次刷新间隔秒数）。

## 4. 语言与单位

- 语言三种给法：查询参数 `?lang=zh`；**wttr.in 子域** `zh.wttr.in/Beijing`；请求头 `Accept-Language: fr`。
  实测：`zh` 简体、`zh-tw` 繁体可用；`zh-hans`/`zh_cn`/`zh_HANT` 这类变体会返回 **ERR008**（invalid lang）。
  语言全集见 `:translation` 页面（含各语言的贡献者名单）。
- 单位：`?m` 公制（默认非美系）、`?u` 英制、`?M` 公制但风速 m/s。

## 5. 月相

- `wttr.in/Moon` 当前月相卡片；`wttr.in/Moon@2026-12-25` 指定日期；`wttr.in/Moon,+China` 按地区。
- 一行里嵌入：`?format=%m`（图标）或 `%M`（月龄）。

## 6. v2 / v3 扩展服务

- **v2**：`v2.wttr.in/Beijing` 富数据版——三天温度/降水曲线、逐段天气图标、风向风速行、
  月相、时区、黎明日出天顶日落黄昏、精确坐标。日/夜字体集分别走 `v2d.wttr.in` / `v2n.wttr.in`。
- **v3 地图**：`v3.wttr.in/California.png`（区域天气图）、`v3.wttr.in/Bayern.sxl`（Sixel 内联图），
  浏览器直接访问 `v3.wttr.in/Region`。区域名用行政区划（California/Bayern 实测 OK）。

## 7. 特殊 URL 与备用域

- `wttr.in/:help` 用法页；`wttr.in/:bash.function` 官方推荐 bash 函数 `wttr()`（source 即用）；
  `wttr.in/:translation` 译者与语言清单。
- **wttr.is**：等价备用域，全部路径直接替换即可（drop-in）。脚本提供 `--base-url wttr.is`。

## 8. CLI 工具（scripts/weather.py）

```
python scripts/weather.py [地点] [-f FMT] [-l LANG] [-u m|u|M] [--base-url wttr.in|wttr.is]

-f terminal|view0|view1|view2|narrow|quiet|superquiet|nofollow|plain|compact
   json|json-lite|prometheus|oneline|batch|png|moon|v2|v2-day|v2-night|v3|v3-sixel|html|help|special
-V FLAGS 视图字母组合直通(012nqQFTdA) ｜ --ansi 保彩色 ｜ --follow 留 Follow ｜ --keep-title PNG 不去标题
```

常用：
```bash
python scripts/weather.py Beijing                      # 中文纯文本视图（默认，自动去 Follow 行）
python scripts/weather.py Beijing --ansi               # 保留 ANSI 彩色
python scripts/weather.py Beijing -V 0q                # 任意视图组合直通（?0q）
python scripts/weather.py Beijing --follow             # 保留 Follow 行
python scripts/weather.py Beijing -f view0 -u u        # 只看当前，英制
python scripts/weather.py Beijing -f oneline --custom-format '%l:+%c+%t+%h+%w'
python scripts/weather.py -f batch --locations Beijing Shanghai Guangzhou
python scripts/weather.py Paris -f png -o p.png --frame --transparency 150 --background 00aabb --view 0
python scripts/weather.py -f moon --moon-date 2026-12-25
python scripts/weather.py Beijing -f moon --region China
python scripts/weather.py California -f v3 -o map.png
python scripts/weather.py -f special --special bash.function
python scripts/weather.py -f json | jq '.current_condition[0].temp_C'
```
库用法：`from weather import WeatherQuery; WeatherQuery("Beijing").json_full()`。

## 9. 集成

- **tmux**：`set -g status-right '#(curl -s wttr.in/Beijing?format=3&period=60)'`
- **shell alias**：`alias weather='python ~/.agents/skills/wttr-weather/scripts/weather.py'`
- **bash 函数**：`eval "$(curl -s wttr.in/:bash.function)"`，然后 `wttr Paris`。
- **图片叠天气**：`convert source.jpg <(curl wttr.in/Oymyakon_pq_transparency=0.png) -geometry +50+50 -composite out.jpg`（透明必须长写法 `transparency=N`，短写 `_t` 系列实测全挂）。

## 10. 不支持清单（实测死项，勿写进产出）

- `format` 代码 `%e`（露点）、`%H`（最高温）、`%L`（最低温）：README 有提及但**服务端原样回显、未实现**。
  （注意 tmux strftime 的 `%H:%M` 与此无关，那是 shell 时间格式。）
- `lang=zh-hans`、`zh_cn`、`zh_HANT`：ERR008 invalid。
- 一行输出里的 `%C`（天气文本）**本地化不完整**：`lang=ru` 回 `Солнечно`，但 `lang=zh` 仍回英文
  `Haze`（2026-10 实测）。要中文天气词走全量视图（`?0&lang=zh`）或 j1 JSON。
- 裸 PNG 后缀 `_tqp.png`（无参 transparency 短写）：返回 `fail`——用 `transparency=0..255` 长写法。
- PNG 短选项 `t`（透明）整体失效：`_t.png`、`_0t.png`、`_0tqp_lang=zh.png`、`_0pq_t.png` 实测全部返回 `fail`；
  **README 自己的示例已死**。只有 `transparency=N` 长写法可用（已验证出图）。
- 旧文档宣称的「54+ 种语言」无官方计数佐证（`:translation` 页面模板变量未渲染）；
  按语言码逐个实测为准，别引用固定总数。

速查细节见 `references/quick-reference.md`。

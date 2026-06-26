# wttr.in 天气查询参考指南

## 快速参考表

### 常用命令速查

| 用途 | 命令 |
|------|------|
| 当前位置天气 | `curl wttr.in` |
| 指定城市 | `curl wttr.in/Beijing` |
| 中文输出 | `curl wttr.in/Beijing?lang=zh` |
| 公制单位 | `curl wttr.in/Beijing?m` |
| 纯文本输出 | `curl wttr.in/Beijing?T` |
| 一行信息 | `curl wttr.in/Beijing?format=3` |
| JSON 数据 | `curl wttr.in/Beijing?format=j1` |
| PNG 图片 | `curl wttr.in/Beijing.png` |
| 月相 | `curl wttr.in/Moon` |
| 详细预报 (v2) | `curl v2.wttr.in/Beijing` |

### 自定义格式代码

| 代码 | 含义 | 示例输出 |
|------|------|----------|
| `%l` | 位置 | Beijing |
| `%c` | 天气图标 | 🌦 |
| `%C` | 天气描述 | Overcast |
| `%t` | 温度 | +11°C |
| `%f` | 体感温度 | +9°C |
| `%h` | 湿度 | 76% |
| `%w` | 风 | ↓12km/h |
| `%P` | 气压 | 1019hPa |
| `%m` | 月相 | 🌖 |
| `%S` | 日出 | 06:23 |
| `%s` | 日落 | 18:45 |

### 预设格式

| 格式 | 输出示例 |
|------|----------|
| `format=1` | 🌦 +11⁰C |
| `format=2` | 🌦 🌡️+11°C 🌬️↓4km/h |
| `format=3` | Beijing: 🌦 +11⁰C |
| `format=4` | Beijing: 🌦 🌡️+11°C 🌬️↓4km/h |

### 支持的语言代码

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| zh | 中文 | en | English |
| ja | 日本語 | ko | 한국어 |
| fr | Français | de | Deutsch |
| es | Español | ru | Русский |
| pt | Português | it | Italiano |
| ar | العربية | hi | हिन्दी |

### 特殊位置前缀

| 前缀 | 用途 | 示例 |
|------|------|------|
| (无) | 城市/地点 | `wttr.in/Paris` |
| `~` | 特殊地点名 | `wttr.in/~Eiffel+Tower` |
| 机场代码 | 机场天气 | `wttr.in/LAX` |
| `@` | 域名查询 | `wttr.in/@github.com` |
| IP 地址 | IP 位置 | `wttr.in/192.168.1.1` |

### 天气代码对照表

| 代码 | 描述 | 图标 |
|------|------|------|
| 113 | 晴朗/少云 | ☀️ |
| 116 | 局部多云 | ⛅ |
| 119 | 多云 | ☁️ |
| 122 | 阴天 | 🌫️ |
| 176/263 | 小雨/毛毛雨 | 🌦 |
| 266/293 | 轻雨 | 🌧️ |
| 296/299 | 中雨 | 🌧️ |
| 302/305 | 大雨 | ⛈️ |
| 308/359 | 暴雨 | ⛈️ |
| 179/311 | 小雪 | 🌨️ |
| 314/317 | 中雪 | 🌨️ |
| 320/323 | 大雪 | ❄️ |
| 143/248 | 雾 | 🌫️ |

### tmux 配置示例

```tmux
# 简单天气
set -g status-right "#(curl -s 'wttr.in/Beijing?format=%%l+%%c+%%t')"

# 多城市轮询
set -g status-interval 60
WEATHER='#(curl -s "wttr.in/Beijing:Shanghai:Guangzhou?format=%%l:+%%c%%20%%t&period=60")'
set -g status-right "$WEATHER"
```

### 常用自定义格式

```bash
# 完整信息
curl 'wttr.in/Beijing?format=%l:+%c+%t,+%h,+%w\n'

# 仅温度和天气
curl 'wttr.in/Beijing?format=%c+%t\n'

# 包含日出日落
curl 'wttr.in/Beijing?format=%l+%c+%t+%S-%s\n'

# 月相
curl 'wttr.in/Beijing?format=%m+%M\n'
```

### 故障排除

| 问题 | 解决方案 |
|------|----------|
| Emoji 不显示 | 安装 Noto Color Emoji 字体 |
| 乱码 | 使用 `?T` 或 `?d` 参数 |
| 终端不支持 | 改用纯文本格式 `?T` |
| 位置找不到 | 尝试使用 `~` 前缀或英文名 |

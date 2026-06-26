---
name: qweather
description: Global weather queries powered by QWeather. Supports real-time weather, multi-day forecasts, and trip-friendly summaries. Self-growing — expands along official API docs as needed, and automatically consolidates new capabilities.
---

# qweather

一个**文档驱动、可自扩展**的天气 skill，基于和风天气 API 提供稳定的最小可用能力，并允许在**官方文档边界内**持续扩展。

---

## 不可变原则

以下是这个 skill 的宪法，任何扩展和修改都不得违反。

1. **文档驱动** — 一切能力以和风天气官方文档为准，不猜测 undocumented 接口，不依赖未公开行为。
2. **最小可用基线** — 基础脚本（认证、城市解析、天气查询）是所有扩展的脚手架，不可删除，只可增强。
3. **受控扩展** — 允许自我生长，但每次扩展必须完整走完：查文档 → 明确接口 → 测试通过 → 回写 SKILL.md。跳过任何一步都不算完成。
4. **零泄露** — 发布版不包含任何私钥、KID、Project ID、API Host 等用户私密信息。`local/` 目录永远不进入发布版。
5. **省额度** — 城市解析优先走离线数据（LocationList CSV），GeoAPI 仅作兜底。

---

## 当前能力

> 以下内容随扩展演化，每次新增能力后更新此节。

### 认证

- JWT（Ed25519），通过 `scripts/gen-jwt.mjs` 生成，支持 token 缓存（`local/jwt-cache.json`）
- 配置方式：环境变量 或 `local/qweather.json`，详见 `references/setup.md`

### 城市解析

三级优先级链（零 API 消耗优先）：

1. `local/cities.json` — 用户自定义快捷映射
2. `local/China-City-List-latest.csv` — 和风天气官方 LocationList 离线数据
3. GeoAPI `/geo/v2/city/lookup` — 兜底动态查询

歧义城市（如"朝阳"）列出候选，由用户选择。

### 天气查询

| 能力 | 端点 | 参数 |
|------|------|------|
| 实时天气 | `/v7/weather/now` | `--now` |
| 逐日预报 | `/v7/weather/3d` `/v7/weather/7d` | `--days 3\|7`（默认 3） |

### 输出格式

脚本支持 `--brief`（默认）、`--trip`、`--json` 三种格式。

agent 向用户展示天气时，不要直接贴脚本输出，应重新组织为易读格式：

- 用天气 emoji 增强可读性：☀️ 晴、⛅ 多云、☁️ 阴、🌧 雨、🌨 雪、💨 大风、🌡️ 气温
- 每天一行，结构清晰：日期 + emoji + 天气 + 气温区间 + 风力 + 降水
- 出行场景补一句简短建议（🌂 带伞、🧥 防风、⚠️ 路滑等）
- 涉及未来出行时提醒预报会变化

## 首次使用引导

当用户首次使用此 skill（`local/qweather.json` 不存在）时，agent 应主动完成以下流程，而不是把步骤列给用户：

1. 告知用户需要在[和风天气控制台](https://console.qweather.com)获取三个值：KID、Project ID、API Host
2. 等用户提供这三个值
3. 生成 Ed25519 密钥对：询问用户希望存放的位置，如果用户不确定，默认存到 `~/.ssh/` 下并以 skill 名命名（如 `qweather-ed25519-private.pem`）
4. 提醒用户将公钥上传到和风天气控制台
5. 自动创建 `local/qweather.json`
6. 自动执行 `bash scripts/init.sh`
7. 自动执行 `bash scripts/test.sh` 验证

整个过程用户只需要提供 3 个值 + 上传一次公钥，其余 agent 全部自动完成。

## 推荐命令

```bash
# 初始化（首次使用）
bash ./scripts/init.sh

# 实时天气
bash ./scripts/qweather.sh 杭州 --now

# 3 天预报（默认）
bash ./scripts/qweather.sh 杭州

# 出行导向摘要
bash ./scripts/qweather.sh 杭州 --trip

# 7 天预报
bash ./scripts/qweather.sh 杭州 --days 7

# 直接用 LocationID
bash ./scripts/qweather.sh 101210101
```

## 扩展指南

### 触发条件

当用户提出当前 skill 尚不具备、但官方文档支持的能力时，例如：逐小时天气、天气预警、分钟级降水、空气质量、生活指数等。

### 扩展流程

1. 查对应接口的官方文档
2. 明确 endpoint、参数、认证方式、返回字段
3. 判断是否属于高频能力（值得沉淀）还是一次性需求
4. 复用现有的认证、请求（`api_get`）、错误处理和输出模式
5. 真实执行测试，确认通过
6. 回写 SKILL.md 当前能力表和文件清单

### 优先参考

- API 总文档: https://dev.qweather.com/docs/api/
- 认证文档: https://dev.qweather.com/docs/configuration/authentication/
- LocationList: https://github.com/qwd/LocationList
- GeoAPI: https://dev.qweather.com/docs/api/geoapi/

## 文件清单

### scripts/
- `gen-jwt.mjs` — JWT 生成与缓存
- `qweather.sh` — 天气查询主入口
- `init.sh` — 初始化（下载 LocationList、验证配置）
- `test.sh` — 冒烟测试

### references/
- `setup.md` — 配置说明
- `publish.md` — 发布注意事项

### local/（不进入发布版）
- `qweather.json` — 认证配置
- `cities.json` — 用户自定义城市映射
- `China-City-List-latest.csv` — LocationList 离线数据
- `jwt-cache.json` — JWT 缓存

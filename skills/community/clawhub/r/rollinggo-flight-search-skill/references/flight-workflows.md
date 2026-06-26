# RollingGo 机票工作流教程

本文件汇总了机票查询的分步教程。下面的示例为了易读，统一使用已安装的 `rollinggo-flight` 命令。

如果你希望每次都强制使用最新版本，可以改用以下前缀：

- **npx：** `npx --yes rollinggo-flight@latest`
- **uvx：** `uvx --refresh --from rollinggo-flight@latest rollinggo-flight`

---

## 工作流 1：城市名 → 机场代码 → 搜索机票

```bash
# 第一步：查机场 / 城市代码
rollinggo-flight search-airports --keyword "Hangzhou"
# → 返回 cityCode: HGH

rollinggo-flight search-airports --keyword "Chengdu"
# → 返回 cityCode: CTU

# 第二步：搜索机票
rollinggo-flight search-flights \
  --from-city HGH --to-city CTU \
  --from-date 2026-06-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

## 工作流 2：往返商务舱

```bash
# 第一步：确认机场代码
rollinggo-flight search-airports --keyword "Beijing"
rollinggo-flight search-airports --keyword "Shanghai"

# 第二步：搜索往返
rollinggo-flight search-flights \
  --from-airport PEK --to-airport PVG \
  --from-date 2026-07-01 --ret-date 2026-07-07 \
  --trip-type ROUND_TRIP \
  --adult-number 2 --child-number 0 \
  --cabin-grade BUSINESS
```

## 工作流 3：已知机场三字码，直接搜索单程

```bash
# 已经知道起降机场，无需再查机场代码
rollinggo-flight search-flights \
  --from-airport PEK --to-airport HKG \
  --from-date 2026-08-15 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

## 工作流 4：先设置环境变量，再连续执行多个查询

```bash
# PowerShell
$env:ROLLINGGO_API_KEY="YOUR_API_KEY"

rollinggo-flight search-airports --keyword "Guangzhou"
rollinggo-flight search-airports --keyword "Singapore"
rollinggo-flight search-flights \
  --from-city CAN --to-city SIN \
  --from-date 2026-09-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

## 工作流 5：用表格输出快速人工查看结果

```bash
# 机场结果用表格输出
rollinggo-flight search-airports \
  --keyword "Tokyo" \
  --format table

# 航班结果用表格输出
rollinggo-flight search-flights \
  --from-city TYO --to-city BJS \
  --from-date 2026-10-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY \
  --format table
```

## 工作流 6：无结果时按顺序放宽条件

```bash
# 第一次：按机场代码精确查
rollinggo-flight search-flights \
  --from-airport PKX --to-airport NRT \
  --from-date 2026-11-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade BUSINESS

# 如果结果为空：改用城市代码，放宽到同城多个机场
rollinggo-flight search-flights \
  --from-city BJS --to-city TYO \
  --from-date 2026-11-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade BUSINESS

# 如果仍然为空：降低舱位要求
rollinggo-flight search-flights \
  --from-city BJS --to-city TYO \
  --from-date 2026-11-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

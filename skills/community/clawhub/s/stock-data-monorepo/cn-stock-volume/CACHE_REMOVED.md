# cn-stock-volume 缓存移除说明

## 变更时间
2026-03-23 22:38

## 变更内容

### 已删除
1. ✅ `cache/` 目录及其所有内容
2. ✅ `load_cache()` 函数
3. ✅ `save_cache()` 函数
4. ✅ `get_cache_path()` 函数
5. ✅ `CACHE_DIR` 配置
6. ✅ `CACHE_TTL_HOURS` 配置
7. ✅ 缓存检查逻辑
8. ✅ 缓存保存逻辑
9. ✅ `--force` 参数（已废弃）

### 保留
1. ✅ `manual/` 目录（成交量手动补充数据）
2. ✅ `load_manual_data()` 函数
3. ✅ `save_manual_data()` 函数
4. ✅ 非交易日处理逻辑
5. ✅ 数据获取核心逻辑

## 修改文件

| 文件 | 修改内容 |
|------|----------|
| `scripts/fetch_data.py` | 删除所有缓存相关代码 |
| `SKILL.md` | 更新文档说明缓存已移除 |

## 行为变化

### 修改前
```bash
$ python3 scripts/fetch_data.py 2026-03-23 --json
[INFO] 加载缓存：cache/2026-03-23.json
[INFO] 使用缓存数据：2026-03-23
{ ... "_from_cache": true ... }
```

### 修改后
```bash
$ python3 scripts/fetch_data.py 2026-03-23 --json
[INFO] 🔄 获取最新数据：2026-03-23
{ ... "_from_cache": false ... }
```

## 优势

✅ **数据实时性**: 每次运行都获取最新数据  
✅ **避免过期**: 不再有缓存导致的数据过期问题  
✅ **简化逻辑**: 代码更简洁，易于维护  
✅ **调试方便**: 无需手动清理缓存  

## 劣势

⚠️ **性能略降**: 每次运行需要调用 browser 工具（约 5-10 秒）  
⚠️ **网络依赖**: 必须有网络连接才能获取数据  

## 使用建议

### 日常使用
```bash
# 直接运行，始终获取最新数据
python3 scripts/fetch_data.py 2026-03-23
```

### 批量生成多日报告
```bash
# 连续生成多日报告（每日都会获取最新数据）
python3 scripts/fetch_data.py 2026-03-20
python3 scripts/fetch_data.py 2026-03-21
python3 scripts/fetch_data.py 2026-03-22
python3 scripts/fetch_data.py 2026-03-23
```

### 生成 stock-daily-report
```bash
# stock-daily-report 会自动调用 cn-stock-volume
python3 ~/.jvs/.openclaw/workspace/skills/stock-daily-report/scripts/generate_report.py
```

## 注意事项

1. **fetch-index-data 缓存**: 指数数据可能来自 `fetch-index-data` skill 的缓存（这是另一个 skill）
2. **成交量数据**: 仍需手动补充（`manual/` 目录）
3. **非交易日**: 周末和节假日会自动往前推到最近交易日

## 回滚方法（如需要）

如需恢复缓存功能，从 git 历史恢复以下文件：
```bash
git checkout HEAD -- scripts/fetch_data.py
git checkout HEAD -- SKILL.md
```

## 相关优化

建议同时优化 `stock-daily-report` skill：
- ✅ 已优化 `fetch_gainers.py`（优先 browser 实时获取）
- ✅ 已优化 `clawhub_integration.py`（添加实时接口）
- ⏳ 待完成：在主会话中直接调用 browser

---

**维护者**: shinelp100  
**更新日期**: 2026-03-23

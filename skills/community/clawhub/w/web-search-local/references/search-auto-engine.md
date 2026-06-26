# Auto 引擎技术规格

本文档详细说明 auto 引擎的工作原理和技术规格。

## 优先级与尝试顺序

| 顺序 | 引擎 | 描述 | 成功即返回？ |
|------|------|------|-------------|
| 1 | Bing RSS | 结构化 RSS 输出，最快 | ✅ 是，且有足够结果时 |
| 2 | Bing HTML | HTML 解析后备（RSS 失败或无结果） | ✅ 是，且有足够结果时 |
| 3 | Yandex | regex 解析（可能触发 CAPTCHA） | ✅ 是，且有足够结果时 |
| 4 | DuckDuckGo | HTML 解析（可能 SSL 封锁） | ✅ 是，且有足够结果时 |
| 5 | WebFetch | urllib 标准库实现 | ✅ 是，且有足够结果时 |

**快速路径：** 若某引擎返回结果数 ≥ `limit`，立即返回并跳过后续引擎。

## 补充机制

当某引擎返回结果但数量 `< limit` 时，按优先级顺序尝试补充来源：

1. 创建已见 URL set（初始包含当前结果的所有 URL）
2. 调用下一个引擎获取 `need = limit - len(results)` 条新结果
3. 遍历新结果，仅保留 `url not in seen_urls` 的条目（保持去重）
4. 更新 `seen_urls` 和 `results`
5. 重复步骤 1-4 直到 `len(results) >= limit` 或所有引擎用尽

**注意：** 补充阶段使用 O(1) set 查找，确保效率。

## 去重规则

- **去重键：** 结果的 `url` 字段（完整 URL 字符串精确匹配）
- **保留策略：** 先出现的结果优先（发动机优先级决定）
- **示例：** Bing 和 Yandex 都返回 `https://example.com` → 保留 Bing 的结果，丢弃 Yandex 的结果

## 失败处理

每个引擎独立捕获异常，失败时不影响后续尝试：
- 网络错误（超时、SSL、连接失败）→ 记录失败，继续下一个
- HTTP 错误（403/429/503）→ 记录失败，继续下一个
- 解析错误（空结果、格式异常）→ 视为无结果，继续下一个

最后若所有引擎均失败，返回空列表 `[]`。

## Verbose 模式输出示例

```bash
python3 scripts/search.py -q "test" -e auto -v
```

```
INFO:[Auto] 尝试引擎 1/5: Bing RSS
INFO:[Auto] ✓ Bing RSS 成功，获得 3 条结果
INFO:[Auto] 结果不足 10 条，尝试补充...
INFO:[Auto] 补充来源: Bing HTML
INFO:[Auto] 补充来源: Yandex
INFO:[Auto] ✓ Yandex 补充成功，获得 4 条结果（去重后净增 2）
INFO:搜索完成总结:
  查询: test
  引擎: auto(bing→yandex→ddg)
  结果数: 5
  总耗时: 2.34s
  分段耗时: cookie=0.52s, search=1.80s, parse=0.02s
  缓存状态: ✗ NOT HIT
```

## 已知网络限制

由于本服务器网络环境限制，部分引擎在运行时可能不可用，但这不影响 `auto` 模式的容错能力：

| 引擎 | 限制 | 影响 |
|------|------|------|
| `ddg` | SSL 连接被重置（`SSLError`） | 该引擎失败，自动跳过 |
| `yandex` | 某些 IP 触发 CAPTCHA | 该引擎失败，自动跳过 |

这些限制已在测试中模拟（mock），确保 `auto` 模式的逻辑在这些引擎失败时仍能正常工作。

## 与手动选择引擎的区别

- **`bing`** 仅使用 Bing RSS → HTML 双模式，不尝试其他引擎
- **`auto`** 使用完整的 5 引擎级联 + 补充逻辑，覆盖面最广
- **性能对比：** `auto` 可能稍慢（尝试多个引擎），但可靠性更高

## Verbose 模式增强

使用 `-v` 或 `--verbose` 参数可获得：

1. **DEBUG 级别日志** — 显示每个请求的详细调试信息
2. **自动故障转移日志** — auto 模式显示各引擎尝试顺序和结果数量
3. **搜索完成总结** — 完成后输出表格化的总结信息（查询、引擎、结果数、总耗时、分段耗时、缓存状态）

**Verbose 输出示例：**
```
DEBUG:延迟 3.2s
INFO:[Auto] 尝试引擎 1/5: Bing RSS
INFO:[Auto] ✓ Bing RSS 成功，获得 3 条结果
...
INFO:搜索完成总结:
  查询: python
  引擎: auto(bing→yandex→ddg)
  结果数: 10
  总耗时: 2.34s
  分段耗时: cookie=0.52s, search=1.80s, parse=0.02s
  缓存状态: ✗ NOT HIT
============================================================
```

# 引擎扩展架构设计

## 如何添加新搜索引擎

当前代码采用模块化设计，添加新引擎只需三步：

1. **实现搜索函数** — 在 `scripts/search.py` 中添加：
   ```python
   def search_brave(query, limit=10, verbose=False):
       """Brave Search 实现"""
       # 1. 构建请求 URL (Brave 无官方 API，需 HTML 解析或非官方 API)
       # 2. 发送请求（使用 requests，支持代理、超时）
       # 3. 解析结果 → [{title, url, snippet}, ...]
       # 4. 错误处理 → 返回 [] 表示失败
       pass
   ```

2. **注册到 `auto` 优先级** — 修改 `search_auto()` 函数：
   ```python
   # 在合适位置插入补充逻辑
   if len(results) < limit:
       logger.info("[Auto] 补充来源: Brave")
       extra = search_brave(query, limit - len(results), verbose)
       seen_urls = {r["url"] for r in results}
       for r in extra:
           if r["url"] not in seen_urls:
               results.append(r)
               seen_urls.add(r["url"])
   ```

3. **更新 CLI 参数** — 在 `argparse` 的 `--engine` choices 中添加 `brave`。
4. **添加单元测试** — 在 `tests/test_search.py` 添加对应测试类。

## Brave Search 评估

### 方案对比

| 方案 | 难度 | 稳定性 | 备注 |
|------|------|--------|------|
| **HTML 解析** | 高 | 低 | Brave 网页结构复杂，反爬严格，Selector 易变 |
| **非官方 API** | 中 | 极低 | 依赖逆向工程，随时失效 |
| **官方 API** | — | — | Brave Search API 收费，需 API Key，违背"免费"原则 |

### 结论

**暂不添加 Brave 引擎**，原因：

1. **价值边际递减** — 现有 5 引擎 (Bing RSS/HTML、Yandex、DDG、WebFetch) 已提供充分冗余
2. **维护成本高** — HTML  scraping 需要持续监控页面结构变化，增加测试负担
3. **成功率存疑** — Brave 反爬措施严格，实际可用性可能更低（类似 DDG/Yandex）
4. **架构已就绪** — 如需添加，代码结构清晰，可以随时实现（见上方"如何添加"）

### 替代建议

若需提升搜索覆盖率，优先考虑：
- **优化现有引擎** — 改进 Bing HTML 解析容错性，减少对 RSS 的依赖
- **缓存策略** — 调整 TTL，增加本地覆盖率
- **结果合并** — 提升 auto 模式的去重和排序质量

---

**最后更新**: 2026-03-19 11:00 (Asia/Shanghai)

# End-to-end workflow | 端到端流程说明

This skill covers the **full workflow from collected Xueqiu combo holdings to final ranking/PDF export**.  
这个技能覆盖的是**从已采集的雪球组合持仓，到最终统计和 PDF 导出**的完整流程。

## Recommended workflow | 推荐流程

1. Collect combo holdings in batches inside a logged-in Xueqiu browser session  
   在已登录雪球的浏览器会话里，分批抓取组合持仓
2. Save each batch as a JSON file  
   把每一批结果保存成 JSON 文件
3. Merge all batch files with `scripts/merge_batches.py`  
   用 `scripts/merge_batches.py` 合并所有批次文件
4. Apply patch JSON if any combo needs verified correction  
   如果个别组合需要人工确认修正，应用 patch JSON
5. Generate the final ranking and PDF with `scripts/build_report.py`  
   用 `scripts/build_report.py` 生成最终排名与 PDF

## Why upstream scraping is not packaged as a pure CLI script | 为什么上游抓取没有被包装成纯命令行脚本

Because the upstream collection step depends on:  
因为上游采集依赖以下条件：
- an already logged-in Xueqiu browser session  
  已登录的雪球浏览器会话
- `credentials: 'include'` inside the page context  
  页面上下文中的 `credentials: 'include'`
- environment-specific browser-tool timeout / proxy constraints  
  环境相关的 browser tool 超时与代理限制

This means the reliable part to package is the **workflow and downstream tooling**, not a fake promise of universal headless scraping.  
这意味着更适合被封装的是**工作流和下游脚本工具**，而不是假装能在任何环境里稳定无头抓取。

## Suggested browser-side collection template | 浏览器内抓取模板建议

### Get combo list | 获取组合列表

Usually start from Xueqiu “我的自选” and extract combo names plus `ZH...` symbols.  
通常先从雪球“我的自选”页面拿到组合名称和 `ZH...` 代码。

### Batch fetch template | 单批抓取模板

Run the following inside an already logged-in Xueqiu browser context:  
在已登录雪球的浏览器上下文中执行：

```javascript
const batch = [["雪球抄作业A股","ZH3537653"], ["目标三年三倍","ZH3583033"]];
const results = [];
const failures = [];
for (const [name, symbol] of batch) {
  const r = await fetch(`/cubes/rebalancing/history.json?cube_symbol=${symbol}&count=15&page=1`, {credentials:'include'});
  const json = await r.json();
  const list = json.list || [];
  let best = null;
  let bestCount = 0;
  for (const rec of list) {
    const hist = rec.rebalancing_histories || [];
    if (hist.length > bestCount && hist.length >= 2) {
      bestCount = hist.length;
      best = rec;
    }
  }
  if (best && best.rebalancing_histories) {
    results.push({
      combo_name: name,
      combo_symbol: symbol,
      best_record_at: new Date(best.created_at).toLocaleString(),
      holdings: best.rebalancing_histories.map(h => ({
        stock_name: h.stock_name,
        stock_symbol: h.stock_symbol,
        weight: h.weight
      }))
    });
  } else {
    failures.push({combo_name: name, combo_symbol: symbol, reason: 'no_valid_record'});
  }
}
return {results, failures};
```

## Final output rule | 最终统计口径

Only keep stocks with `weight > 0` in the final ranking.  
最终排名里只保留 `weight > 0` 的股票。

Sort by:  
排序规则：
1. combo count descending  
   被持仓组合数量降序
2. summed weight descending  
   合计持仓比例降序
3. stock symbol ascending  
   股票代码升序

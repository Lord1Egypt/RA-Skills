# 验证修复详细规范

## 线上验证清单来源

验证清单从 `html_lint` 管线的 online stage 规则自动生成，不需要手动定义。

三条 online 规则产生的验证项：

1. **OnlineReportChecks** — 报告页面验证：HTTP 可达、report-wrap、page-body、base.css、main.js、div 平衡、图片路径绝对、无 chrome 遗留
2. **OnlineAssetChecks** — 静态资源验证：CSS/JS 可达非空、index.json 可解析、图片为真实文件
3. **OnlineImageChecks** — 图片验证：返回 image/* Content-Type、非 HTML fallback、大小 > 0

## 修复循环

```
验证失败 → diagnose_failure(url, status) → 诊断建议 → 修复 → publish → 再验证
```

连续 3 次失败通知用户手动排查。

## 失败诊断字典

| 状态 | 症状 | 修复 |
|------|------|------|
| 404 | URL 返回 404 | 等待 30s 重试 / 检查 dist 是否有该文件 / 重新 publish |
| empty | CSS/JS/JSON 空内容 | copy_assets + 重新 publish |
| missing_structure | HTML 缺 report-wrap/page-body | 重新 produce（lint 管线会自动检查） |
| json_parse_error | index.json 解析失败 | rebuild_index 重建 |
| stale_index | 索引不含最新页面 | rebuild_index |
| 5xx | URL 返回 5xx | 重新 deploy_to_cf / 检查 CF 项目状态 |
| cors_error | CORS 阻止 | 检查 CF Pages 自定义域名 DNS 配置 |
| redirect_loop | 无限重定向 | 检查 CF Pages 域名配置 / 用 .pages.dev 域名验证 |

## 索引安全机制

三层保障：
1. dist/index.json（正常路径）
2. 技能根目录 index.json（每次 save_index 时同步备份）
3. 线上 {SITE_URL}/index.json（curl 拉取恢复）

`load_index_safe()` 按 dist → 备份 → 线上 优先级恢复。
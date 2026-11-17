# smart-web-search

智能联网搜索工具，为 OpenClaw 和 Claude Code 社区打造。

## 快速开始

```bash
cd smart-web-search
bash scripts/setup.sh   # Linux/macOS
# Windows: npm install && npx playwright install chromium

# 测试
node scripts/search.js "Python 教程" --max=3
```

## 核心优势

✅ **IP 引擎路由**：根据 IP 归属自动选择 Bing CN 或 DDG，全球可用  
✅ **跨引擎兜底**：一个引擎返回空时自动切换到另一个  
✅ **双层内容抓取**：HTTP cheerio → Playwright headed 兜底  
✅ **全球无缝切换**：国内外环境自动适配，支持手动覆盖  

## 技术特点

| 项目 | 说明 |
|------|------|
| 搜索引擎 | 国内 Bing CN / 海外 DDG（Playwright 全流程） |
| 正文抓取 | HTTP + cheerio（JSON-LD/Next.js 提取）→ Playwright 兜底 |
| 区域检测 | 三轮并行探测（myip.ipip.net / ipinfo.io / cn.bing.com） |
| 去重策略 | 域名 + 路径主干（忽略 www/m 子域、tracking 参数） |

## 与其他工具对比

相比 **Claude Code 内置 WebFetch**：
- 本工具：搜索 + 批量抓取（"查资料、找教程"）
- WebFetch：单 URL 精确抓取（"读取已知网页"）
- 互补使用

## 示例

```bash
# 基本搜索
node scripts/search.js "今日金价"

# 只搜索不抓正文（极速模式）
node scripts/search.js "React hooks" --fetch=0

# 抓取前5条正文
node scripts/search.js "AI 趋势" --fetch=5

# 手动指定区域
node scripts/search.js "深圳景点" --region=cn
```

## 文档

详细文档见 [SKILL.md](./SKILL.md)。

## 许可

Apache-2.0

## 致谢

整合自 `free-web-search-js` 和 `free-web-search`，感谢原作者的开源贡献。

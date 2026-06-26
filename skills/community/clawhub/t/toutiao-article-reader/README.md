# Toutiao Article Reader

使用浏览器自动化阅读今日头条、微信公众号、知乎等平台文章。

## 功能特性

- ✅ 多平台支持：头条/公众号/知乎/雪球等
- ✅ 智能识别：自动识别平台并应用最佳提取规则
- ✅ 内容清洗：去除广告、水印、无关内容
- ✅ 错误处理：完善的重试和错误处理机制
- ✅ 性能优化：缓存支持、快速加载
- ✅ 详细统计：字数、阅读时间等
- ✅ AI 总结：智能生成内容摘要
- ✅ 导出功能：支持 Markdown/TXT/JSON/HTML

## 支持平台

- 今日头条 (toutiao.com)
- 微信公众号 (mp.weixin.qq.com)
- 知乎 (zhihu.com)
- 雪球 (xueqiu.com)
- 其他主流内容平台

## 安装方式

1. 确保已安装依赖：
   ```bash
   pip install playwright beautifulsoup4
   playwright install chromium
   ```

2. 将技能文件夹复制到 OpenClaw 的 skills 目录：
   ```
   C:\Users\zhuyi\AppData\Roaming\JoyClaw\workspace\agents\daily-office\skills\
   ```

## 使用方式

```bash
# 基本用法
python scripts/read_article.py <URL>

# 生成 AI 总结
python scripts/read_article.py <URL> --summary

# 导出为 Markdown
python scripts/read_article.py <URL> --export markdown -o article.md

# 查看缓存统计
python scripts/read_article.py --cache-stats

# 清空缓存
python scripts/read_article.py --clear-cache
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--json` | 输出 JSON 格式 |
| `--summary` | 生成 AI 总结 |
| `--verbose` | 详细输出 |
| `--timeout` | 超时时间（毫秒） |
| `--no-headless` | 显示浏览器窗口 |
| `--export` | 导出格式（markdown/txt/json/html） |
| `--output` | 输出文件路径 |
| `--cache-stats` | 显示缓存统计 |
| `--clear-cache` | 清空缓存 |

## 开发环境

- Python 3.8+
- Playwright 1.58.0+
- BeautifulSoup4 4.12.0+

## License

MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 作者

Your Name

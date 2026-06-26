# DOI 解析与开放获取检测

## Unpaywall API

本项目使用 Unpaywall API 检测文献的开放获取状态。

### API 端点
```
https://api.unpaywall.org/v2/{doi}?email={your_email}
```

### 响应字段

| 字段 | 说明 |
|------|------|
| `is_oa` | 是否为开放获取 |
| `oa_status` | OA 类型（gold, green, bronze, hybrid, closed） |
| `best_oa_location` | 最佳 OA 版本位置 |
| `best_oa_location.url_for_pdf` | PDF 直接下载链接 |

### OA 类型说明

- **Gold** - 完全开放获取期刊
- **Green** - 机构库或预印本服务器中的版本
- **Bronze** - 出版商网站免费阅读（无开放许可）
- **Hybrid** - 订阅期刊中的 OA 文章（APC 付费）
- **Closed** - 需要订阅

## 其他开放获取资源

### 1. PubMed Central (PMC)
生物医学文献的全文库：
```
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/
```

### 2. arXiv
预印本服务器（物理、数学、计算机等）：
```
https://arxiv.org/pdf/{arxiv_id}.pdf
```

### 3. bioRxiv / medRxiv
生命科学预印本：
```
https://www.biorxiv.org/content/{doi}.full.pdf
```

### 4. ResearchGate / Academia.edu
学者社交平台，可能有作者自存档版本

### 5. 机构库
大学机构库（如 MIT DSpace、arXiv 等）

## DOI 解析服务

### Crossref API
获取文献元数据：
```
https://api.crossref.org/works/{doi}
```

### DOI.org
解析 DOI 到出版商页面：
```
https://doi.org/{doi}
```

## 注意事项

1. **尊重版权** - 只下载你有权限访问的文献
2. **API 限制** - Unpaywall 有速率限制，请控制请求频率
3. **准确性** - OA 状态可能随时间变化，建议定期更新

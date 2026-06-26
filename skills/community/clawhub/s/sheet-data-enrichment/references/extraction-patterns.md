# Extraction Patterns

Common patterns for extracting structured data from web pages, organized by data type.

## Author / Reporter Bylines

### Chinese Media

| Pattern | Example | Regex |
|---|---|---|
| 记者+名字 | `记者 张三` | `记者\s*[：:]?\s*([\u4e00-\u9fff]{2,4})` |
| 文/作者 | `文｜李四` / `文/王五` | `文[｜\|/]\s*([\u4e00-\u9fff\w]+)` |
| 作者行 | `作者：赵六` / `作者丨孙七` | `作者[：:\|丨]\s*([\u4e00-\u9fff\w]+)` |
| 括号署名 | `（周八）` / `(吴九)` | `[（(]([\u4e00-\u9fff]{2,4})[）)]` |
| 采写行 | `采写：记者 郑十` | `采写[：:]\s*(?:记者\s*)?([\u4e00-\u9fff]{2,4})` |
| 来源+记者 | `来源：新华社 记者张三` | `来源[：:].*?记者\s*([\u4e00-\u9fff]{2,4})` |

### English Media

| Pattern | Example | Regex |
|---|---|---|
| By line | `By Jane Doe` | `[Bb]y\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)` |
| Author field | `Author: John Smith` | `[Aa]uthor[：:]\s*(.+?)(?:\n\|$)` |
| Reporting | `Reporting by Sarah Lee` | `[Rr]eporting by\s+(.+?)(?:\n\|;)` |

## Browser Extraction Snippets

### Quick full-text grab
```javascript
document.body.innerText.substring(0, 2000)
```

### Head + tail (find bylines at article end)
```javascript
(() => {
  const t = document.body.innerText;
  return t.substring(0, 500) + '\n---END---\n' + t.substring(Math.max(0, t.length - 300));
})()
```

### Keyword search (author markers)
```javascript
(() => {
  const t = document.body.innerText;
  const markers = ['记者', '作者', '文｜', '编辑', 'By ', 'Author'];
  for (const k of markers) {
    const idx = t.indexOf(k);
    if (idx >= 0) return `${k} @ ${idx}: ...${t.substring(Math.max(0,idx-30), idx+80)}...`;
  }
  return 'No author markers found';
})()
```

## Site-Specific Notes

| Domain | Rendering | Author Location |
|---|---|---|
| thepaper.cn (澎湃) | SPA, needs browser | Below title or end of article |
| stcn.com (证券时报) | Static | End of article `（记者 XXX）` |
| yicai.com (第一财经) | SPA | End of article in parentheses |
| nbd.com.cn (每经) | Static | Below title `记者 XXX 编辑 XXX` |
| 21jingji.com (21世纪) | Static | Below title |
| lanjinger.com (蓝鲸) | SPA | Below title `记者 XXX` |
| mp.weixin.qq.com | Needs browser (captcha) | Varies by account |
| cls.cn (财联社) | Static/SPA | End of flash news `（记者 XXX）` |
| cnfic.com.cn (新华财经) | SPA, sometimes Baidu mini-program | `记者XXX` in opening line |
| zhitongcaijing.com (智通) | SPA | Below title `作者名\n日期` |
| weibo.com | Browser only | Usually no individual reporter |

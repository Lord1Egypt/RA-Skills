---
name: zspace-xunlei
description: 用极空间的迅雷下载资源
metadata: { "openclaw": { "emoji": "🐦", "requires": { "bins": [ "openclaw" ] } } }
---

# 极空间迅雷下载

## 用法

输入：下载资源的磁力链接（以magnet开头）

1. 用浏览器打开极空间网站（https://www.zconnect.cn），如果未登录，则要求用户先在浏览器完成登录后再重新执行。

2. 执行如下命令，控制浏览器完成迅雷下载，注意要把<magnetUrl>替换成真实的磁力链接
```bash
openclaw browser snapshot | grep -oP 'ref=\K[^\]]+(?=\]: 迅雷)' | xargs openclaw browser click

openclaw browser snapshot | grep -oP 'ref=\K[^\]]+(?=\]: 新建任务)' | xargs openclaw browser click

openclaw browser snapshot | grep -oP 'textbox.*请添加下载链接.*\[ref=\K[^]]+' | xargs -I {} openclaw browser type {} "<magnetUrl>"

openclaw browser snapshot | grep -oP 'ref=\K[^\]]+(?=\]: 确定)' | xargs openclaw browser click

openclaw browser snapshot | grep -oP 'ref=\K[^\]]+(?=\]: 立即下载)' | xargs openclaw browser click
```

3. 检查网页内容，是否有新增加的下载任务


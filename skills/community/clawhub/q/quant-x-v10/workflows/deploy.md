# 部署流程

## 1. 本地预览
```bash
python3 -m http.server 8765
# 访问 http://localhost:8765
```

## 2. 生产部署
```bash
# 复制到 web 服务器
scp quant-x-v10.html user@server:/var/www/html/

# 或使用 CDN
# 走 matrix deploy
```

## 3. 验证清单
- [ ] HTML 文件可访问
- [ ] 浏览器控制台无 JS 错误
- [ ] 数据每 3 秒刷新
- [ ] 板块对比数据正常
- [ ] 图表显示正常

# 证券监管页面批量监控系统

自动监控深交所、上交所、北交所、股转系统、中国结算、证券业协会等21个证券监管页面，检测页面变化并生成通知。

## 快速开始

### 查看通知
```bash
bash /root/monitoring/securities/scripts/check_notifications.sh
```

### 手动运行
```bash
bash /root/monitoring/securities/scripts/crawl_all.sh
```

## 功能特性

- 🎯 监控21个证券监管相关页面
- 🔧 每天早上9:00自动定时抓取
- 📊 自动检测页面变化并生成差异报告
- 💬 支持企业微信通知

## 监控站点

- 深圳证券交易所（10个页面）
- 上海证券交易所（3个页面）
- 北京证券交易所（2个页面）
- 全国中小企业股份转让系统（3个页面）
- 中国证券登记结算有限责任公司（2个页面）
- 中国证券业协会（1个页面）

## 详细文档

见 [SKILL.md](./SKILL.md)

## License

MIT

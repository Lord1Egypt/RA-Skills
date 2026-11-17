# QUANT-X v10 量化策略仪表盘

## 核心功能
- 6 因子加权综合评分
- OBI 4 维度订单失衡分析
- 5 大经典策略信号（双均线/网格/突破/动量/均值回归）
- 5 只板块股实时对比 + 背离度
- 大单 4 档分档（500/2000/5000/10000 手）
- 关键技术位 R3/R2/R1/S1/S2/S3
- 实时价格走势 Chart.js

## 数据源
- 实时报价：https://qt.gtimg.cn/q=sh600330
- K 线：https://web.ifzq.gtimg.cn/appstock/app/fqkline/get
- 分钟：https://web.ifzq.gtimg.cn/appstock/app/minute/query

## 部署
```bash
python3 -m http.server 8765 --directory .
# 浏览器打开 http://localhost:8765
```

## License
MIT-0

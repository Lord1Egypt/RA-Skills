# 数据源参考

## 数据源映射

| 数据源 | 库/协议 | 功能 | 状态 |
|--------|---------|------|------|
| **通达信** | pytdx (TCP:7709) | 实时行情、K线、五档盘口 | ✅ 稳定 |
| **东方财富** | datacenter API (HTTPS) | 板块成分股(1500+板块) | ✅ 新版API |
| **同花顺** | akshare _ths 系列 | 板块排行、板块详情 | ✅ 稳定 |
| **akshare** | HTTP | 财务数据、排名、IPO等 | ✅ 通用 |

## API端点备忘

### 东方财富新版API
```
端点: https://datacenter.eastmoney.com/api/data/v1/get
报表: RPT_BOARD_CONSTITUENT
字段: BOARD_CODE,BOARD_NAME,SECURITY_CODE,SECUCODE
筛选: filter=(BOARD_CODE="917")
```

### 通达信
```
主机: 60.12.136.250:7709 (自动探测最佳服务器)
```

## 已知限制

1. **盘前实时行情为0** (09:30-15:00 才有数据)
2. 同花顺板块数据约延迟 5 分钟
3. 东方财富 datacenter API 每日请求限制

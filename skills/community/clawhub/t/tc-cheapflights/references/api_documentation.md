# 同程旅行API文档

## 核心API端点

### 1. 特价机票查询API
- **URL**: `https://wx.17u.cn/cheapflights/newcomparepriceV2/single`
- **方法**: GET
- **参数**:
  - `originList`: JSON字符串，出发城市列表 `[{"nameType":0,"code":"PEK","name":"北京","type":0}]`
  - `destList`: JSON字符串，到达城市列表 `[{"nameType":0,"code":"SHA","name":"上海","type":0}]`
  - `dateInfo`: JSON字符串，日期信息 `{"type":0,"startAndEndDate":["2026-03-16"]}`

### 2. 主站机票查询
- **URL**: `https://www.ly.com/flights/itinerary/oneway/PEK-SHA?date=2026-03-16`
- **方法**: GET
- **参数**:
  - 路径参数: `PEK-SHA` (出发-到达机场代码)
  - `date`: 日期 `YYYY-MM-DD`

## 城市与机场代码映射

| 城市 | 机场代码 | 机场名称 |
|------|----------|----------|
| 北京 | PEK | 首都机场 |
| 北京 | PKX | 大兴机场 |
| 上海 | SHA | 虹桥机场 |
| 上海 | PVG | 浦东机场 |
| 广州 | CAN | 白云机场 |
| 深圳 | SZX | 宝安机场 |
| 成都 | CTU | 双流机场 |
| 重庆 | CKG | 江北机场 |
| 杭州 | HGH | 萧山机场 |
| 南京 | NKG | 禄口机场 |

## 响应数据格式

### wx.17u.cn API响应
```html
<script>window.__INITIAL_STATE__ = { /* JSON数据 */ };</script>
```

JSON结构包含：
- `configCenter`: 配置信息
- `userInfo`: 用户信息
- 页面配置数据（不含实时航班信息）

### ly.com 响应
HTML页面包含航班信息，通过CSS选择器提取：
- `.flight-item`: 航班项目
- `.flight-item-name`: 航班号和航空公司
- `.flight-item-time`: 起飞到达时间
- `.flight-item-airport`: 机场信息
- `.flight-item-price`: 价格信息

## 请求头建议

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
```

## 错误处理

### 常见错误码
- `403 Forbidden`: 访问频率过高或需要验证
- `404 Not Found`: 页面不存在或参数错误
- `500 Internal Server Error`: 服务器错误

### 处理策略
1. 重试机制：最多重试3次，间隔1-3秒
2. 降级方案：使用模拟数据或备用API
3. 日志记录：详细记录错误信息

## 频率限制

建议遵循以下限制：
- 单次查询间隔：≥1秒
- 同一航线查询间隔：≥30分钟
- 每日总查询次数：≤100次

## 数据更新频率

- 机票价格：实时更新（变化较快）
- 航班时刻表：每日更新
- 机场信息：每月更新

## 注意事项

1. **合规使用**: 仅用于个人查询，避免商业爬虫
2. **隐私保护**: 不收集用户敏感信息
3. **性能优化**: 使用缓存减少重复查询
4. **错误恢复**: 实现优雅降级机制
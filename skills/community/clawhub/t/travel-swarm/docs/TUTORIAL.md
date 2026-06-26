# TravelMaster V8 使用教程

## 一、快速开始

### 1.1 启动服务

```bash
cd /home/admin/.openclaw/workspace/travel_swarm
python3.8 main_v8.py
```

**访问地址**: http://47.253.101.130:7860

---

## 二、功能介绍

### 2.1 FlyAI真实票价查询

**API接口**: `/api/flyai`

**示例请求**:
```bash
curl -X POST http://47.253.101.130:7860/api/flyai \
  -H "Content-Type: application/json" \
  -d '{"origin": "北京", "destination": "香港", "date": "2026-05-01"}'
```

**返回字段**:
- flight_no: 航班号
- airline: 航空公司
- dep_time: 起飞时间
- arr_time: 到达时间
- price: 票价（元）
- jump_url: 预订链接

---

### 2.2 高德vs腾讯验证

**API接口**: `/api/verify`

**功能**:
- 高德POI搜索
- 腾讯POI搜索
- POI数量对比
- 路径距离对比

---

### 2.3 美团美食推荐

**API接口**: `/api/food`

**功能**:
- 美团餐厅搜索
- 优惠套餐推荐
- 预订链接生成

---

### 2.4 麦当劳兜底

**API接口**: `/api/mcd`

**功能**:
- 麦当劳门店搜索
- 快餐方案推荐
- 点餐链接生成

---

## 三、完整旅行规划

### 3.1 API接口

**接口**: `/api/plan`

**示例请求**:
```bash
curl -X POST http://47.253.101.130:7860/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "departure": "北京",
    "destination": "香港",
    "days": 3,
    "budget": 5000,
    "party_size": 2
  }'
```

---

### 3.2 返回内容

| 字段 | 说明 |
|------|------|
| flights | FlyAI航班列表 |
| trains | FlyAI火车列表 |
| lunch | 美团美食推荐 |
| dinner | 美团晚餐推荐 |
| verify_result | 高德vs腾讯验证 |
| map_screenshot | 高德静态地图截图 |
| food_screenshots | 美团美食截图 |
| mcd_screenshots | 麦当劳截图 |

---

## 四、API密钥配置

### 4.1 必需密钥

| API | 配置项 | 获取地址 |
|------|--------|----------|
| FlyAI | FLYAI_API_KEY | https://flyai.com |
| 高德 | GAODE_API_KEY | https://lbs.amap.com |
| 腾讯 | TENCENT_MAP_KEY | https://lbs.qq.com |
| 美团 | MEITUAN_API_KEY | https://open.meituan.com |

---

### 4.2 配置方式

**创建.env文件**:
```bash
cd /home/admin/.openclaw/workspace
cp MCP_KEYS.env .env
```

---

## 五、常见问题

### Q1: 端口无法访问？

**解决**: 检查防火墙和绑定地址
```bash
lsof -i:7860
```

---

### Q2: FlyAI返回空数据？

**解决**: 检查API密钥和日期格式
- 日期格式: YYYY-MM-DD
- 密钥有效期: 检查订阅状态

---

### Q3: 高德vs腾讯验证失败？

**解决**: 检查API密钥权限
- 高德需要POI搜索权限
- 腾讯需要Place API权限

---

## 六、一键克隆

```bash
git clone https://gitee.com/timo2026/travel-swarm-v8.git
cd travel-swarm-v8
pip install -r requirements.txt
python main_v8.py
```

---

**教程版本**: v1.0
**更新时间**: 2026-04-12

🦫 海狸 | 靠得住、能干事、在状态
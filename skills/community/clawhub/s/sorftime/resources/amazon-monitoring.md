> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。
> 本文档为 Amazon 监控模块的通用规则与索引，具体接口参数见 3 个子文件。

# Amazon 监控通用规则与索引

---

## 前置配置

### 1. 安装 sorftime-cli
```bash
npm install -g sorftime-cli
```

### 2. 配置账户
```bash
# 添加账户
sorftime add <profile-name> <your-account-sk>

# 切换到默认账户
sorftime use <profile-name>
```

---

## Domain 参数与站点支持矩阵

| domain值 | 站点代码 | 站点名称 | 关键词监控 | 榜单监控 | 跟卖监控 |
|---------|---------|---------|-----------|---------|---------|
| 1 | us | 美国站 | ✓ | ✓ | ✓ |
| 2 | gb | 英国站 | ✓ | ✓ | ✓ |
| 3 | de | 德国站 | ✓ | ✓ | ✓ |
| 4 | fr | 法国站 | ✓ | ✓ | ✓ |
| 6 | ca | 加拿大站 | ✓ | ✓ | ✓ |
| 7 | jp | 日本站 | ✓ | ✓ | ✓ |
| 8 | es | 西班牙站 | ✓ | ✗ | ✓ |
| 9 | it | 意大利站 | ✓ | ✗ | ✓ |
| 10 | mx | 墨西哥站 | ✗ | ✗ | ✓ |
| 11 | ae | 阿联酋站 | ✗ | ✗ | ✓ |
| 12 | au | 澳大利亚站 | ✗ | ✓ | ✓ |
| 13 | br | 巴西站 | ✗ | ✗ | ✗ |
| 14 | sa | 沙特站 | ✗ | ✗ | ✗ |

---

## 接口索引

| 监控类型 | 接口数量 | 文档 | 接口列表 |
|---------|---------|------|---------|
| 关键词监控 | 5 | [`amazon-monitoring-keyword.md`](./amazon-monitoring-keyword.md) | KeywordBatchSubscription、KeywordTasks、KeywordBatchTaskUpdate、KeywordBatchScheduleList、KeywordBatchScheduleDetail |
| 榜单监控 | 4 | [`amazon-monitoring-bestseller.md`](./amazon-monitoring-bestseller.md) | BestSellerListSubscription、BestSellerListTask、BestSellerListDelete、BestSellerListDataCollect |
| 跟卖&库存监控 | 5 | [`amazon-monitoring-seller.md`](./amazon-monitoring-seller.md) | ProductSellerSubscription、ProductSellerTasks、ProductSellerTaskUpdate、ProductSellerTaskScheduleList、ProductSellerTaskScheduleDetail |

---

## 积分消耗规则

1. **关键词监控**:
   - 监控一个关键词，每周7天，每天24小时，每小时监控1次，每次监控前3页
   - 每周消耗积分 = 1×7×24×1×3 = **504**
   - 日本站每页面消耗2积分，相同频率消耗 **1008**
   - 监控任务仅依据关键词扣除积分，与关键词下关注多少ASIN无关

2. **榜单监控**:
   - 监控 top100 每天消耗 **10** 积分
   - 监控 top200 每天消耗 **20** 积分
   - 监控 top300 每天消耗 **30** 积分
   - 监控 top400 每天消耗 **40** 积分

3. **跟卖&库存监控**:
   - 每个ASIN每次监控消耗 **2** 积分（日本站 **4** 积分）
   - 启用库存检查时，额外消耗 **1** 积分（日本站 **2** 积分）

4. **积分重置**: 每月10号凌晨自动清空上期未用完积分并发放新积分

---

## 数据保存期限

- 所有监控结果最多保存 **30 日**

---

## period 表达式语法

格式：`<每周哪几日>|<每天哪些时段>|<监控频率>`

- **每周哪几日**: 1-7（逗号分割，1=周一，7=周日）
- **每天哪些时段**: 1-6（每个时段4小时，北京时区）
  - 1: 1-4点, 2: 5-8点, 3: 9-12点, 4: 13-16点, 5: 17-20点, 6: 21-0点
- **监控频率**:
  - 1: 时段内任意时刻一次
  - 11-14: 时段内第1-4个时间刻度执行（可能因任务量过多而失败）
  - 2: 时段内每小时1次
  - 3: 时段内每2小时1次（随机双数或单数）
  - 31: 时段内单数小时执行，共2次（可能因任务量过多而失败）
  - 32: 时段内双数小时执行，共2次（可能因任务量过多而失败）

---

## area 地区邮编

- **PC模式 (mode=0)**:
  - US: 10041(纽约), 60601(芝加哥), 94102(旧金山)
  - GB: N1P 3AA(伦敦)
  - DE: 10115(柏林)
  - FR: 75001(巴黎)
  - CA: V5K 0A1(温哥华)
  - JP: 120-0015(东京)
  - ES: 28001(马德里)
  - IT: 66030(罗马)

- **手机模式 (mode=1)**:
  - US: 98101(西雅图)
  - GB: B10 0AB(伯明翰)
  - DE: 20095(汉堡)
  - FR: 13001(马赛)
  - CA: V5K 0A1(维多利亚)
  - JP: 550-0004(大阪)
  - ES: 08001(巴塞罗那)
  - IT: 16100(热那亚)

---

## 通用注意事项

1. **积分管理**: 监控类接口都消耗积分，每月10号凌晨重置
2. **数据保存**: 所有监控结果最多保存30日
3. **任务注册失败**: 当设定某些频率时（11-14, 31-32），可能因时段内任务量过多而注册失败，返回 taskId = **-999**
4. **榜单监控前提**: 所注册的类目需先为关注类目
5. **跟卖监控限制**: 最多监控前30个卖家

---

## 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 4 | 积分余额不足 | 充值积分或等待下月重置 |
| -999 | 任务注册/修改失败 | 时段内任务过多，尝试其他时段或频率 |
| 401 | 认证失败 | 检查Account-SK是否有效 |
| 403 | 权限不足 | 检查套餐权限或请求次数 |

---

## 最佳实践

### 1. 关键词排名监控
```bash
# 注册监控任务：工作日白天每小时监控一次
sorftime api KeywordBatchSubscription '{"keyword": ["power bank"], "mode": 0, "area": "10041", "page": 3, "period": "1,2,3,4,5|1,2,3,4,5,6|2"}' --domain 1

# 查询任务列表
sorftime api KeywordTasks '{"keyword": "power"}' --domain 1

# 查询执行批次
sorftime api KeywordBatchScheduleList '{"TaskId": 12345}' --domain 1

# 提取某次监控的详细数据
sorftime api KeywordBatchScheduleDetail '{"ScheduelId": "batch123"}' --domain 1
```

### 2. 榜单监控
```bash
# 注册Best Sellers榜单监控，每天0点执行
sorftime api BestSellerListSubscription '{"nodeid": "3743561", "Range": 1, "Period": 100, "BestSellerListType": 5}' --domain 1

# 查询榜单监控任务
sorftime api BestSellerListTask '{"pageIndex": 1, "pageSize": 20}' --domain 1

# 查询榜单数据
sorftime api BestSellerListDataCollect '{"nodeid": "3743561", "BestSellerListType": 5, "queryDate": "2024-01-15 00"}' --domain 1

# 删除榜单监控任务
sorftime api BestSellerListDelete '{"nodeid": "3743561", "BestSellerListType": 5}' --domain 1
```

### 3. 跟卖监控
```bash
# 注册跟卖监控，每小时检查一次，不检查库存
sorftime api ProductSellerSubscription '{"asin": "B0CVM8TXHP", "checkstock": 0, "period": "1,2,3,4,5,6,7|1,2,3,4,5,6|2"}' --domain 1

# 查询跟卖监控任务
sorftime api ProductSellerTasks '{"pageIndex": 1, "pageSize": 20}' --domain 1

# 暂停任务
sorftime api ProductSellerTaskUpdate '{"taskId": 12345, "update": 1}' --domain 1

# 恢复任务
sorftime api ProductSellerTaskUpdate '{"taskId": 12345, "update": 2}' --domain 1

# 查询执行批次
sorftime api ProductSellerTaskScheduleList '{"TaskId": 12345}' --domain 1

# 提取监控结果
sorftime api ProductSellerTaskScheduleDetail '{"ScheduelId": "batch123"}' --domain 1
```

### 4. 综合监控策略
```bash
# 场景：监控核心产品的关键词排名、榜单位置和跟卖情况

# 1. 关键词排名监控（工作时段每小时）
sorftime api KeywordBatchSubscription '{"keyword": ["power bank"], "mode": 0, "area": "10041", "page": 3, "period": "1,2,3,4,5|1,2,3,4,5,6|2"}' --domain 1

# 2. 榜单监控（每天0点）
sorftime api BestSellerListSubscription '{"nodeid": "3743561", "Range": 1, "Period": 100, "BestSellerListType": 5}' --domain 1

# 3. 跟卖监控（每小时，含库存检查）
sorftime api ProductSellerSubscription '{"asin": "B0CVM8TXHP", "checkstock": 1, "period": "1,2,3,4,5,6,7|1,2,3,4,5,6|2"}' --domain 1
```

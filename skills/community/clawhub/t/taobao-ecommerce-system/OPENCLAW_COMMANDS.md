# OpenClaw 命令注册文件
# 让 OpenClaw 能 100% 调用电商运营系统

## 可用命令列表

### 1. 智能选品
**命令：** `select-product`
**用途：** 从网商园/1688 采集商品并分析
**示例：**
```
python scripts/ecommerce_main.py select-product --source "https://www.wsy.com/item/12345.html" --batch
```

**OpenClaw 对话触发词：**
- "智能选品"
- "采集商品"
- "网商园选款"
- "1688 选品"

### 2. 标准化上架
**命令：** `upload-product`
**用途：** 标准化上架商品
**示例：**
```
python scripts/ecommerce_main.py upload-product --product-id KZ20260326
```

**OpenClaw 对话触发词：**
- "上架商品"
- "标准化上架"
- "发布商品"

### 3. 推广监控
**命令：** `marketing-monitor`
**用途：** 监控万相台/直通车推广数据
**示例：**
```
python scripts/ecommerce_main.py marketing-monitor --plan-id 12345
```

**OpenClaw 对话触发词：**
- "推广监控"
- "查看数据"
- "测款数据"
- "直通车数据"

### 4. 订单处理
**命令：** `process-orders`
**用途：** 处理淘宝订单（推单到 1688/网商园）
**示例：**
```
python scripts/ecommerce_main.py process-orders --auto
```

**OpenClaw 对话触发词：**
- "订单处理"
- "去下单"
- "推单到 1688"
- "网商园下单"

### 5. 客服辅助
**命令：** `cs-helper`
**用途：** 客服自动回复辅助
**示例：**
```
python scripts/ecommerce_main.py cs-helper --start
```

**OpenClaw 对话触发词：**
- "客服辅助"
- "启动客服"
- "自动回复"
- "客服话术"

---

## OpenClaw 集成测试

### 测试步骤

**1. 测试模块导入**
```bash
cd "C:\Users\Administrator\.openclaw\workspace\skills\taobao-ecommerce-system"
python -c "from scripts.ecommerce_main import EcommerceSystem; print('✅ 模块导入成功')"
```

**2. 测试命令执行**
```bash
python scripts/ecommerce_main.py --help
```

**3. 测试各功能模块**
```bash
# 测试智能选品
python scripts/ecommerce_main.py select-product --source "test" --batch

# 测试标准化上架
python scripts/ecommerce_main.py upload-product --product-id KZ20260326

# 测试推广监控
python scripts/ecommerce_main.py marketing-monitor --plan-id 12345

# 测试订单处理
python scripts/ecommerce_main.py process-orders --auto

# 测试客服辅助
python scripts/ecommerce_main.py cs-helper --start
```

---

## OpenClaw 对话示例

### 示例 1：智能选品

**用户：** 帮我从网商园选品，这个链接
https://www.wsy.com/item/12345.html

**OpenClaw 执行：**
```bash
cd "C:\Users\Administrator\.openclaw\workspace\skills\taobao-ecommerce-system"
python scripts/ecommerce_main.py select-product --source "https://www.wsy.com/item/12345.html" --batch
```

**预期输出：**
```
🛍️  2026 无货源电商运营系统 v2.0.0

📊 智能选品（乘法电商·精细化选品 2026 版）

Step 1: 采集货源信息... ✅
Step 2: 淘宝同款数据查询... ✅
Step 3: 5 个数据指标筛选... ✅
Step 4: 利润精算... ✅
Step 5: 侵权风险检测... ✅

选品结果：
┌─────────────────────────────────────┐
│ 款号：KZ20260326                     │
│ 名称：春秋立领夹克                   │
│ 供货价：¥85                          │
│ 建议售价：¥169                       │
│ 净利润：¥37.07 (21.9%) ✅           │
│ 竞争度：中等 ✅                      │
│ 侵权风险：⚠️ 图 2 疑似 Logo           │
│ 建议：修改后可做                     │
└─────────────────────────────────────┘

✅ 选品完成！已保存到选品库
```

### 示例 2：标准化上架

**用户：** 上架这个商品 KZ20260326

**OpenClaw 执行：**
```bash
python scripts/ecommerce_main.py upload-product --product-id KZ20260326
```

**预期输出：**
```
📝 标准化上架（SOP 2026 版）

Step 1: 标题优化（3 步法）... ✅
   建议标题：男士夹克外套立领春秋新款休闲商务修身潮流上衣男装

Step 2: 主图处理（5 张图标准）... ✅
   图 1: ✅ 点击率优化
   图 2: ✅ 细节展示
   图 3: ✅ 场景图
   图 4: ✅ 功能展示
   图 5: ✅ 尺码表

Step 3: 详情页模板（信任型）... ✅

Step 4: 价格设置（保本计算）... ✅
   一口价：¥253（1.5 倍）
   折扣价：¥169
   优惠券：满¥159 减¥20

Step 5: 属性填写（合规检测）... ✅

✅ 上架完成！商品已发布
```

### 示例 3：推广监控

**用户：** 查看推广计划 12345 的数据

**OpenClaw 执行：**
```bash
python scripts/ecommerce_main.py marketing-monitor --plan-id 12345
```

**预期输出：**
```
📈 推广监控（万相台无界·4+2 模型）

测款进度：第 5 天/7 天

实时数据（今日）：
┌─────────────────────────────────────┐
│ 展现：5000    点击：150              │
│ 点击率：3.0%  (行业 2.0%) ✅         │
│ 收藏加购：20   加购率：13.3% ✅      │
│ 转化：5 单     转化率：3.3% ✅       │
│ 花费：¥300    产出：¥845             │
│ ROI: 2.82     (保本 2.0) ✅          │
└─────────────────────────────────────┘

达标线对比：
┌─────────────────────────────────────┐
│ 点击率：3.0% > 2.5% ✅              │
│ 加购率：13.3% > 10% ✅              │
│ 转化率：3.3% > 2% ✅                │
│ ROI: 2.82 > 2.0 ✅                  │
└─────────────────────────────────────┘

判断：✅ 数据达标，继续投放
建议：明日预算追加到¥400
累计盈亏：盈利 ¥545 ✅
```

### 示例 4：订单处理

**用户：** 处理今天的订单

**OpenClaw 执行：**
```bash
python scripts/ecommerce_main.py process-orders --auto
```

**预期输出：**
```
📦 订单处理

待处理订单：3
┌─────────────────────────────────────┐
│ 订单 1001: KZ20260326 (L 黑色)       │
│ 客户地址：北京市朝阳区...             │
│ 档口：广州 XX 服饰 138****1234       │
│ [一键下单] [联系档口]                │
├─────────────────────────────────────┤
│ 订单 1002: KZ20260327 (M 蓝色)       │
│ 客户地址：上海市浦东新区...           │
│ 档口：杭州 XX 服饰 139****5678       │
│ [一键下单] [联系档口]                │
└─────────────────────────────────────┘

✅ 自动推单到 1688 已启动
```

### 示例 5：客服辅助

**用户：** 启动客服自动回复

**OpenClaw 执行：**
```bash
python scripts/ecommerce_main.py cs-helper --start
```

**预期输出：**
```
💬 客服辅助

✅ 客服自动回复已启动

自动回复话术：
┌─────────────────────────────────────┐
│ 开场白：您好，当前为智能客服...     │
│ 询价：亲，这款衣服现在活动价...     │
│ 尺码：亲，根据您的身高体重...       │
│ 发货：亲，下单后 48 小时内发货...    │
│ 售后：亲，非常抱歉给您带来...       │
└─────────────────────────────────────┘
```

---

## 故障排查

### 问题 1：命令未找到

**错误：** `python: can't open file 'scripts/ecommerce_main.py'`

**解决：**
```bash
cd "C:\Users\Administrator\.openclaw\workspace\skills\taobao-ecommerce-system"
python scripts/ecommerce_main.py --help
```

### 问题 2：模块导入失败

**错误：** `ModuleNotFoundError: No module named 'pandas'`

**解决：**
```bash
pip install -r requirements.txt
```

### 问题 3：OpenClaw 不识别

**解决：**
1. 重启 OpenClaw
2. 执行 `skills reload` 命令
3. 检查 SKILL.md 是否存在

---

## 验证清单

- [x] Skill 文件已创建
- [x] 主程序可执行
- [x] 模块可导入
- [x] 命令可执行
- [x] OpenClaw 可识别
- [x] 对话可触发

---

**OpenClaw 集成完成，可以 100% 调用！** ✅

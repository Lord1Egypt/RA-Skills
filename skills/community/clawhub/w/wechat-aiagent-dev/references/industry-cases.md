# 行业接入示范

## 什么时候读取

用户要求案例、行业模板、"我是某某商家怎么接"、"给我示范"时，读取本文件。

每个案例按统一7段结构：用户表达 → C端路径 → 原子接口 → GEO数据 → 自动模式兜底 → 测试用例 → 行业特殊约束。

---

## 案例 1：咖啡/奶茶点单

### 用户表达

- "帮我点一杯少糖拿铁。"
- "来杯清爽一点的冰饮。"
- "再来一杯我上次喝的。"
- "附近哪家店能送到公司？"

### C端路径

```
推荐/搜索饮品 → 选择规格 → 确认门店/配送 → 生成订单 → 用户确认支付 → 返回订单状态
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `recommendDrinks` | 根据场景推荐饮品 | scene、temperature、budget、storeId |
| `searchDrinks` | 按关键词搜索饮品 | keyword、category、storeId |
| `getDrinkDetail` | 查看饮品详情 | drinkId |
| `getSkuOptions` | 获取温度、糖度、杯型、加料 | drinkId |
| `createDrinkOrder` | 创建订单确认信息 | drinkId、sku、storeId、addressId |
| `requestDrinkPayment` | 拉起支付 | orderId |
| `queryDrinkOrderStatus` | 查询订单状态 | orderId |
| `cancelDrinkOrder` | 取消订单 | orderId、reason |

### GEO数据

- 商品名、别名：拿铁、冰拿铁、厚乳拿铁
- 场景：提神、低糖、下午茶、通勤、清爽
- 规格：温度、冰量、糖度、杯型、加料
- 门店：营业时间、配送范围、可售库存
- 优惠：会员价、第二杯半价、券适用条件

### 自动模式兜底

- 商品页标题包含商品名和别名
- 规格、价格、库存、配送范围不要只放图片里
- 页面元数据标明"点单"、"商品详情"、"门店选择"等用途

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 想喝点清爽的 | recommendDrinks | 返回热销饮品 |
| 帮我点一杯冰美式少冰 | searchDrinks → getSkuOptions → createDrinkOrder | 缺地址时引导补地址 |
| 我的订单到哪了 | queryDrinkOrderStatus | 无订单时引导查看历史 |

### 行业特殊约束

- 多门店场景：同一饮品在不同门店价格、库存、可售规格可能不同，接口需按 storeId 区分
- 售后退款：超时未取餐自动退款、异常订单取消退款
- 组件过期态：订单完成后可置为过期，防止用户重复操作

---

## 案例 2：本地团购/门店套餐

### 用户表达

- "附近有什么双人餐优惠？"
- "找个周末能用的烤肉套餐。"
- "帮我买一张洗车券。"
- "这个套餐过期了能退吗？"

### C端路径

```
识别位置/商圈 → 推荐套餐 → 查看门店和可用规则 → 购买团购券 → 返回核销说明
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchNearbyDeals` | 查附近套餐 | location、category、peopleCount、budget |
| `getDealDetail` | 查套餐详情 | dealId |
| `getStoreAvailability` | 查门店可用状态 | dealId、storeId、date |
| `createDealOrder` | 创建团购券订单 | dealId、storeId、quantity |
| `queryDealCoupon` | 查询券码和核销规则 | orderId |
| `refundDealOrder` | 退款 | orderId、reason |

### GEO数据

- 套餐名、适合人数、品类、价格、门店
- 可用日期、节假日限制、预约要求
- 地址、商圈、停车、营业时间
- 核销方式、退款规则、有效期

### 自动模式兜底

- 套餐页标题包含套餐名、人数、品类
- 使用规则、有效期、退款规则用文本展示
- 页面元数据标明"团购套餐"、"门店列表"、"券码详情"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 附近有什么双人餐优惠 | searchNearbyDeals | 无结果时推荐热门套餐 |
| 周末能用的烤肉套餐 | searchNearbyDeals → getStoreAvailability | 周末满档时推荐工作日 |
| 帮我退掉这张券 | refundDealOrder | 已核销时告知不可退 |

### 行业特殊约束

- 核销状态查询：券码状态（未使用/已使用/已过期/已退款）
- 退款规则：未使用全退、已使用不退、过期自动退
- 节假日限制：部分套餐周末/节假日不可用或需加价

---

## 案例 3：预约服务

### 用户表达

- "帮我约明天下午洗车。"
- "周六有没有摄影档期？"
- "附近能做宠物洗护吗？"
- "帮我改约到下周三。"

### C端路径

```
识别服务类型 → 查询门店/时间 → 用户选择档期 → 创建预约 → 返回预约确认
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchServices` | 搜索服务项目 | keyword、category、location |
| `getServiceDetail` | 查看服务详情 | serviceId |
| `listAvailableSlots` | 查询可预约时间 | serviceId、storeId、date |
| `createBooking` | 创建预约 | serviceId、storeId、slotId、contact |
| `queryBookingStatus` | 查询预约状态 | bookingId |
| `rescheduleBooking` | 改约 | bookingId、newSlotId |
| `cancelBooking` | 取消预约 | bookingId、reason |

### GEO数据

- 服务名、别名、服务时长、价格
- 可预约时间、门店、服务半径
- 适用人群、注意事项、所需材料
- 取消规则、改期规则、联系方式

### 自动模式兜底

- 服务页标题包含服务名和类别
- 可预约时间、价格、时长用文本展示
- 页面元数据标明"预约服务"、"时间选择"、"预约详情"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 明天下午能约洗车吗 | listAvailableSlots | 无档期时推荐相邻时间 |
| 帮我改约到下周三 | rescheduleBooking | 原预约已开始时不可改约 |
| 附近能做宠物洗护吗 | searchServices | 无结果时推荐附近门店 |

### 行业特殊约束

- 改约取消规则：提前N小时免费改约/取消，超时扣费
- 服务人员选择：部分服务需指定技师/摄影师
- 紧急预约：标记为"急用"的请求优先处理

---

## 案例 4：零售电商

### 用户表达

- "找一双适合通勤的黑色女鞋。"
- "有没有 200 元以内的儿童书包？"
- "帮我看看这件还有 M 码吗？"
- "我的快递到哪了？"

### C端路径

```
需求理解 → 商品推荐/筛选 → 规格库存 → 加购/下单 → 支付 → 物流状态
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `recommendProducts` | 根据需求推荐商品 | scene、category、budget、userPreference |
| `searchProducts` | 搜索商品 | keyword、category、filters |
| `getProductDetail` | 查看商品详情 | productId |
| `checkInventory` | 查询规格库存 | productId、skuId |
| `createProductOrder` | 创建订单 | productId、skuId、quantity、addressId |
| `queryLogistics` | 查询物流 | orderId |
| `requestReturn` | 申请退换货 | orderId、reason、type |

### GEO数据

- 商品名、别名、类目、品牌、价格
- 颜色、尺码、材质、适用场景
- 库存、发货地、配送时效
- 评价标签、适用人群、搭配建议

### 自动模式兜底

- 商品页标题包含商品名、品牌、规格
- 价格、库存、尺码表用文本展示，不只放图片
- 页面元数据标明"商品详情"、"尺码选择"、"物流查询"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 找一双适合通勤的黑色女鞋 | recommendProducts | 无结果时推荐相似款 |
| 这件还有M码吗 | checkInventory | 缺货时推荐相近尺码或到货提醒 |
| 帮我退掉这双鞋 | requestReturn | 超出退换期时告知规则 |

### 行业特殊约束

- 物流状态动态更新：订单组件随物流状态推进动态更新
- 退换货规则：7天无理由、质量问题、尺码不合适等不同处理方式
- 多规格库存：同一商品不同颜色/尺码库存独立

---

## 案例 5：会员优惠/券包

### 用户表达

- "我有什么券能用？"
- "今天买咖啡有没有优惠？"
- "帮我用积分换一张券。"
- "这张券能在别的店用吗？"

### C端路径

```
识别会员身份 → 查询权益/券 → 匹配可用商品 → 领取或使用 → 返回结果
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `getMemberProfile` | 查询会员身份 | sessionId |
| `listCoupons` | 查询优惠券 | memberId、storeId、category |
| `matchCouponProducts` | 匹配可用商品 | couponId |
| `redeemPointsCoupon` | 积分兑换券 | memberId、couponTemplateId |
| `applyCoupon` | 试算优惠 | couponId、orderDraftId |
| `queryCouponStatus` | 查询券状态 | couponId |

### GEO数据

- 会员等级、积分、权益
- 优惠券名称、门槛、适用商品、适用门店
- 有效期、可叠加规则、不可用原因
- 推荐使用场景：早餐、午餐、生日、复购

### 自动模式兜底

- 会员页标题包含等级和权益摘要
- 优惠券列表用文本展示名称、门槛、有效期
- 页面元数据标明"会员中心"、"优惠券"、"积分兑换"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 我有什么券能用 | listCoupons | 无券时推荐可领取的券 |
| 帮我用积分换一张券 | redeemPointsCoupon | 积分不足时告知差多少 |
| 这张券能在别的店用吗 | queryCouponStatus | 不可用时列出可用门店 |

### 行业特殊约束

- 跨店使用规则：部分券限指定门店、部分券全品牌通用
- 叠加规则：哪些券可以叠加、哪些互斥
- 积分过期：积分有有效期，过期前提醒

---

## 案例 6：医疗健康

### 用户表达

- "帮我挂明天上午内科的号。"
- "附近有没有可以做体检的机构？"
- "我的体检报告出了吗？"
- "帮我买一盒布洛芬。"

### C端路径

```
识别科室/服务 → 查询号源/档期 → 用户选择 → 创建预约/订单 → 返回确认 → 查询结果
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchDepartments` | 搜索科室 | hospitalId、keyword |
| `listAppointmentSlots` | 查询号源 | departmentId、doctorId、date |
| `createAppointment` | 创建预约 | departmentId、doctorId、slotId、patientInfo |
| `queryMedicalReport` | 查询报告 | patientId、reportType |
| `searchHealthServices` | 搜索体检/医疗服务 | category、location |
| `orderMedicine` | 药品下单 | prescriptionId、medicineList、addressId |
| `queryAppointmentStatus` | 查询预约状态 | appointmentId |

### GEO数据

- 科室名、别名、擅长方向
- 医生姓名、职称、擅长、排班
- 号源：可预约时段、剩余号数
- 机构：地址、营业时间、服务范围、停车
- 药品：名称、规格、库存、是否处方药

### 自动模式兜底

- 科室和医生信息用文本展示
- 号源状态实时更新
- 页面元数据标明"预约挂号"、"体检套餐"、"报告查询"、"药品购买"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 帮我挂明天上午内科的号 | listAppointmentSlots | 无号时推荐其他时段或医生 |
| 我的体检报告出了吗 | queryMedicalReport | 未出时告知预计时间 |
| 帮我买一盒布洛芬 | orderMedicine | 处方药时引导先问诊 |

### 行业特殊约束

- 医疗合规红线：AI不做诊断、不开处方、不替代医生判断
- 隐私脱敏：身份证号、手机号、病历信息禁止明文展示
- 处方药限制：需先问诊获取处方才能下单
- 预约取消：就诊前一定时间可免费取消

---

## 案例 7：教育培训

### 用户表达

- "有没有适合5岁孩子的画画课？"
- "帮我约一节钢琴试听课。"
- "这学期还剩多少课时？"
- "帮我报一个暑期英语班。"

### C端路径

```
搜索/推荐课程 → 查看详情 → 预约试听/报名 → 缴费 → 课时管理
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchCourses` | 搜索课程 | category、ageRange、location、online |
| `recommendCourses` | 推荐课程 | age、interest、budget、goal |
| `getCourseDetail` | 课程详情 | courseId |
| `bookTrialClass` | 预约试听 | courseId、storeId、slotId、studentInfo |
| `enrollCourse` | 报名缴费 | courseId、storeId、studentInfo、paymentMethod |
| `queryClassSchedule` | 查询课时 | studentId、courseId |
| `queryRemainingHours` | 查询剩余课时 | studentId |

### GEO数据

- 课程名、类别、适合年龄、上课方式（线上/线下）
- 价格、课时数、课时单价、有效期
- 师资：教师姓名、资质、教龄、擅长
- 门店：地址、教室、停车
- 试听：免费/付费、时长、可预约时间

### 自动模式兜底

- 课程页标题包含课程名、年龄、类别
- 价格、课时、师资用文本展示
- 页面元数据标明"课程详情"、"试听预约"、"课时查询"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 有没有适合5岁孩子的画画课 | searchCourses | 无结果时推荐相近年龄课程 |
| 帮我约一节钢琴试听课 | bookTrialClass | 满档时推荐其他时段 |
| 这学期还剩多少课时 | queryRemainingHours | 无记录时引导联系机构 |

### 行业特殊约束

- 退费规则：开课前全退、开课后按已上课时扣费
- 课时有效期：过期课时不可补
- 试听限制：同一课程限试听一次

---

## 案例 8：政务办事

### 用户表达

- "办身份证需要带什么材料？"
- "帮我预约明天下午办护照。"
- "我的申请进度到哪了？"
- "附近哪里可以办居住证？"

### C端路径

```
搜索办事事项 → 查看所需材料 → 预约取号 → 提交申请 → 查询进度
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchGovernmentServices` | 搜索办事事项 | keyword、category、location |
| `listRequiredMaterials` | 查询所需材料 | serviceId |
| `preCheckMaterials` | 材料预审 | serviceId、materialList |
| `bookAppointment` | 预约取号 | serviceId、officeId、slotId、applicantInfo |
| `queryApplicationStatus` | 查询申请进度 | applicationId |
| `searchNearbyOffices` | 查附近办事点 | serviceId、location |

### GEO数据

- 事项名、别名、分类、办理时限
- 所需材料清单、材料格式要求
- 办事地点：地址、工作时间、联系电话
- 可预约时段、取号规则
- 办理流程：申请→审核→制证→领取

### 自动模式兜底

- 事项页标题包含事项名和分类
- 所需材料、办理流程、办理地点用文本展示
- 页面元数据标明"办事指南"、"预约取号"、"进度查询"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 办身份证需要带什么材料 | listRequiredMaterials | 材料不全时标注缺什么 |
| 帮我预约明天下午办护照 | bookAppointment | 满号时推荐其他日期 |
| 我的申请进度到哪了 | queryApplicationStatus | 无记录时引导输入受理号 |

### 行业特殊约束

- 不可代办事项：部分事项必须本人办理
- 材料格式要求：照片尺寸、复印件份数、原件/复印件
- 预约规则：一个身份证同一事项限预约一次

---

## 案例 9：汽车服务

### 用户表达

- "帮我约下周六做保养。"
- "换个前挡风玻璃要多少钱？"
- "车抛锚了，帮我叫道路救援。"
- "我的车该年检了吗？"

### C端路径

```
识别服务类型 → 查询门店/报价 → 预约/呼叫 → 执行服务 → 查询进度
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchMaintenanceServices` | 搜索保养服务 | carModel、mileage、storeId |
| `getMaintenanceQuote` | 获取维修报价 | carModel、issueDescription、storeId |
| `createMaintenanceBooking` | 预约保养 | serviceId、storeId、slotId、carInfo |
| `callRoadsideAssistance` | 道路救援 | location、carModel、issueType、phone |
| `queryServiceProgress` | 查询服务进度 | bookingId |
| `checkInspectionReminder` | 年检提醒 | carPlate、carModel |

### GEO数据

- 服务项目：保养、维修、洗车、美容
- 车型适配：品牌、型号、年款
- 价格区间：工时费、配件费
- 门店：地址、营业时间、服务范围
- 预计时长：保养30分钟、维修视情况

### 自动模式兜底

- 服务页标题包含服务类型和适配车型
- 价格区间、预计时长用文本展示
- 页面元数据标明"保养预约"、"维修报价"、"道路救援"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 帮我约下周六做保养 | createMaintenanceBooking | 满档时推荐其他门店或时间 |
| 换个前挡风玻璃要多少钱 | getMaintenanceQuote | 需看车后才能报价时引导到店 |
| 车抛锚了帮我叫救援 | callRoadsideAssistance | 定位失败时引导输入地址 |

### 行业特殊约束

- 紧急救援优先调度：道路救援标记为高优先级
- 报价不确定：部分维修需到店检测后才能确定价格
- 年检提醒：根据上牌日期和车龄自动计算

---

## 案例 10：宠物服务

### 用户表达

- "帮我约周六给猫洗个澡。"
- "我家狗该打疫苗了吗？"
- "买一袋皇家猫粮。"
- "下周末出去旅游，帮我家猫找寄养。"

### C端路径

```
识别宠物类型/服务 → 查询门店/时间 → 预约/下单 → 返回确认
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchPetServices` | 搜索宠物服务 | petType、serviceType、location |
| `bookGrooming` | 预约洗护 | petType、petWeight、storeId、slotId |
| `listVaccineReminders` | 疫苗提醒 | petId、petType、petAge |
| `orderPetProducts` | 宠物用品下单 | productId、quantity、addressId |
| `bookBoarding` | 预约寄养 | petType、petWeight、storeId、dateRange、specialNeeds |
| `queryBookingStatus` | 查询预约状态 | bookingId |

### GEO数据

- 宠物类型：猫、狗、兔、仓鼠等
- 服务项目：洗护、美容、寄养、遛狗
- 价格：按宠物体重/品种计价
- 门店：地址、营业时间、可服务宠物类型
- 疫苗：疫苗名、接种时间、下次提醒时间

### 自动模式兜底

- 服务页标题包含宠物类型和服务名
- 价格、体重区间、可预约时间用文本展示
- 页面元数据标明"宠物洗护"、"疫苗提醒"、"寄养服务"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 帮我约周六给猫洗个澡 | bookGrooming | 满档时推荐其他门店 |
| 我家狗该打疫苗了吗 | listVaccineReminders | 无记录时引导输入宠物信息 |
| 帮我家猫找下周末寄养 | bookBoarding | 满员时推荐附近其他门店 |

### 行业特殊约束

- 宠物体重/品种影响价格：大型犬洗护费高于小型犬
- 寄养特殊需求：饮食、 medication、性格备注
- 疫苗记录：需关联宠物档案，首次需录入

---

## 案例 11：家政保洁

### 用户表达

- "帮我约一个深度保洁。"
- "找个会做饭的阿姨。"
- "帮我设置每周五定期保洁。"
- "上次那个阿姨还能再约吗？"

### C端路径

```
识别服务类型/需求 → 匹配阿姨 → 查看可用时间 → 预约 → 服务评价 → 周期预约
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchCleaningServices` | 搜索保洁服务 | serviceType、location、area |
| `matchHousekeeper` | 匹配阿姨 | serviceType、skills、language、gender |
| `createCleaningBooking` | 预约保洁 | serviceId、housekeeperId、slotId、addressId |
| `queryServiceRating` | 查看评价 | housekeeperId |
| `setRecurringBooking` | 设置周期预约 | serviceId、housekeeperId、frequency、startDate |
| `cancelCleaningBooking` | 取消预约 | bookingId、reason |

### GEO数据

- 服务类型：日常保洁、深度保洁、做饭、擦玻璃、开荒保洁
- 计价方式：按面积、按小时、按项目
- 阿姨技能标签：做饭、熨烫、收纳、育儿
- 可服务区域、时间段
- 评价：评分、标签、评语

### 自动模式兜底

- 服务页标题包含服务类型和计价方式
- 价格、阿姨技能、可服务区域用文本展示
- 页面元数据标明"保洁预约"、"阿姨匹配"、"周期预约"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 帮我约一个深度保洁 | searchCleaningServices → createCleaningBooking | 无阿姨时推荐其他时段 |
| 找个会做饭的阿姨 | matchHousekeeper | 无匹配时放宽条件 |
| 帮我设置每周五定期保洁 | setRecurringBooking | 阿姨档期冲突时推荐替代 |

### 行业特殊约束

- 周期预约：自动续约和取消规则，需提前N小时取消
- 阿姨匹配：技能、语言、评价、距离多维度匹配
- 服务评价：服务完成后自动邀请评价

---

## 案例 12：婚庆摄影

### 用户表达

- "有什么婚纱摄影套餐？"
- "10月1日还有档期吗？"
- "帮我找喜欢的拍摄风格。"
- "这套套餐和那套有什么区别？"

### C端路径

```
搜索套餐 → 查看风格/样片 → 查询档期 → 对比报价 → 预约 → 付定金
```

### 原子接口

| 接口 | 用途 | 关键参数 |
|---|---|---|
| `searchWeddingPackages` | 搜索婚庆套餐 | category、budget、style |
| `listAvailableDates` | 查询档期 | packageId、storeId、month |
| `recommendStyles` | 推荐拍摄风格 | preference、budget、scene |
| `getQuote` | 获取报价 | packageId、addons、customization |
| `createBooking` | 创建预约 | packageId、storeId、date、contactInfo |
| `queryBookingStatus` | 查询预约状态 | bookingId |
| `comparePackages` | 对比套餐 | packageIds |

### GEO数据

- 套餐名、内容、价格、档期
- 风格标签：韩式、中式、欧式、纪实、旅拍
- 服务范围：拍摄时长、精修数量、成品规格
- 门店：地址、样片展示区
- 定金规则、尾款时间

### 自动模式兜底

- 套餐页标题包含套餐名、风格、价格区间
- 套餐内容、精修数量、成品规格用文本展示
- 页面元数据标明"婚纱摄影"、"套餐对比"、"档期查询"

### 测试用例

| 用户表达 | 期望接口 | 失败兜底 |
|---|---|---|
| 10月1日还有档期吗 | listAvailableDates | 满档时推荐相邻日期 |
| 帮我找喜欢的拍摄风格 | recommendStyles | 无偏好时展示热门风格 |
| 这套和那套有什么区别 | comparePackages | 差异项高亮展示 |

### 行业特殊约束

- 档期冲突处理：旺季档期紧张，需提前预约
- 定金规则：付定金锁档期，定金不退
- 风格选择：影响摄影师分配和道具准备

---

## 行业接口组合速查表

| 行业 | 核心接口组合 | 是否涉及支付 | 是否涉及预约 | 多门店 |
|------|------------|:---:|:---:|:---:|
| 咖啡/奶茶 | 搜索+推荐+详情+规格+下单+支付+状态 | ✅ | ❌ | ✅ |
| 本地团购 | 搜索+详情+门店+下单+券码+退款 | ✅ | ❌ | ✅ |
| 预约服务 | 搜索+详情+档期+预约+改约+取消 | ❌ | ✅ | ✅ |
| 零售电商 | 推荐+搜索+详情+库存+下单+物流+退换 | ✅ | ❌ | ❌ |
| 会员优惠 | 会员+券+匹配+兑换+试算 | ✅ | ❌ | ✅ |
| 医疗健康 | 科室+号源+预约+报告+药品 | ✅ | ✅ | ✅ |
| 教育培训 | 搜索+推荐+试听+报名+课时 | ✅ | ✅ | ✅ |
| 政务办事 | 搜索+材料+预审+预约+进度 | ❌ | ✅ | ✅ |
| 汽车服务 | 搜索+报价+预约+救援+进度 | ✅ | ✅ | ✅ |
| 宠物服务 | 搜索+洗护+疫苗+用品+寄养 | ✅ | ✅ | ✅ |
| 家政保洁 | 搜索+匹配+预约+评价+周期 | ✅ | ✅ | ✅ |
| 婚庆摄影 | 搜索+档期+风格+报价+预约 | ✅ | ✅ | ✅ |

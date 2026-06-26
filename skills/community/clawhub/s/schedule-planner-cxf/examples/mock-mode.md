# 🧪 Mock 模式使用指南

> 无需真实 API Key 即可体验 schedule-planner-cxf 的全部功能。

---

## 为什么需要 Mock 模式？

本技能依赖以下外部 API：
- **高德地图**（AMAP）：路线规划、天气查询
- **途牛旅行**（Tuniu）：机票/酒店/火车票搜索与预订

在审核/演示场景下，审核人员可能无法获取这些 API Key。Mock 模式提供预置的模拟数据，让审核员可以：

1. ✅ 运行脚本并查看输出
2. ✅ 验证行程网页生成效果
3. ✅ 理解整体工作流程
4. ✅ 检查异常处理逻辑

---

## 使用方法

### 方式一：使用 mock 数据直接运行

```bash
# 1. 安装依赖
cd schedule-planner-cxf-1.0.4
npm install

# 2. 将 mock 数据复制为脚本的输入文件
cp examples/mock-data.json scripts/行程-data.json

# 3. 运行行程网页生成
node scripts/generate-trip-page.js

# 预期输出：
# ✅ HTML 行程单已生成: ./output/行程-杭州-xxxxxxxx.html
```

### 方式二：运行 5 城多城市行程（完全模拟）

```bash
# 设置空 API Key 触发 mock 模式
set TUNIU_API_KEY=
node scripts/generate-5city-trip.js

# 脚本会自动检测到无 API Key，使用内置 mock 数据
# 生成结果保存到桌面 5city-trip.html
```

### 方式三：使用 --mock 标志（如已实现）

```bash
# 部分脚本支持 --mock 参数
node scripts/generate-trip-page.js --mock
```

---

## Mock 数据说明

Mock 数据存储在 `examples/mock-data.json`，包含以下要素：

| 数据字段 | 内容 | 说明 |
|---------|------|------|
| tripType | "出差" / "旅游" | 场景标识 |
| segments | 交通 + 住宿段 | 支持 train/flight/hotel 类型 |
| dailyPlan | 每日行程安排 | 多天行程规划 |
| costs | 费用明细 + 总计 | 完整费用拆解 |
| tips | 温馨提示列表 | 出行建议 |
| paymentUrl | 模拟支付链接 | 仅用于演示二维码生成 |

### 数据结构示例

```json
{
  "tripType": "出差",
  "destination": "杭州",
  "segments": [
    { "type": "train", "segmentNo": "G7535", "price": 73 },
    { "type": "hotel", "name": "万斯酒店", "price": 497 }
  ],
  "dailyPlan": [ ... ],
  "costs": { "train1": 73, "hotel": 994, "total": 1140 }
}
```

---

## 异常处理场景（Mock 可覆盖）

Mock 数据还可以模拟以下异常场景：

### 场景 1：API 超时
```
无 API Key 时 → 返回空结果 → 脚本使用备用 mock 数据
期望输出：使用默认 mock 数据继续生成页面，不报错退出
```

### 场景 2：无搜索结果
```
搜索无结果时 → 给出友好提示 → 建议放宽条件
期望输出："暂时没找到符合条件的，我们放宽一些条件试试？"
```

### 场景 3：参数错误
```
传入非法参数 → 返回错误 → 脚本记录日志并回退
期望输出：错误信息仅在终端日志中，不向用户展示技术细节
```

---

## 验证清单

审核员可自助验证以下项目：

- [ ] `npm install` — 依赖安装成功
- [ ] `cp examples/mock-data.json scripts/行程-data.json && node scripts/generate-trip-page.js` — 生成 HTML 页面
- [ ] 打开生成的 HTML 文件 — 查看行程展示效果
- [ ] 检查 `output/` 目录 — 确认 HTML 和二维码文件生成
- [ ] 查看 `SKILL.md` — 确认隐私声明和合规内容
- [ ] 检查 `.gitignore` — 确认敏感文件被排除

---

## Mock 模式与真实模式对比

| 维度 | Mock 模式 | 真实模式 |
|------|----------|---------|
| API Key | 不需要 | 需要 AMAP + TUNIU API Key |
| 数据来源 | 预置 mock-data.json | 实时 API 查询 |
| 执行速度 | 即时 | 依赖网络延迟 |
| 输出质量 | 固定模板 | 真实数据 |
| 二维码生成 | 生成 mock 二维码 | 生成真实支付二维码 |
| 适用场景 | 审核、演示、开发调试 | 正式使用 |
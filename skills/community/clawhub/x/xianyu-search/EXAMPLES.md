# 闲鱼搜索技能 - 使用示例

## 快速开始

### 示例 1：基础搜索
```javascript
const { searchProducts } = require('./search');

await searchProducts({
  keyword: 'MacBook Air M1 2020',
  budget: 2300,
});
```

### 示例 2：带完整参数
```javascript
await searchProducts({
  keyword: 'MacBook Air M1 2020',
  budget: 2300,
  budgetMax: 2500,
  condition: '9 成新',
  batteryMin: 85,
  requireNoRepair: true,
  requireGoodCredit: true,
  platform: 'xianyu',
  location: '北京',
});
```

### 示例 3：搜索其他商品
```javascript
// 搜索 iPhone
await searchProducts({
  keyword: 'iPhone 13',
  budget: 3000,
  batteryMin: 80,
});

// 搜索相机
await searchProducts({
  keyword: 'Sony A7M3',
  budget: 8000,
  condition: '95 新',
});

// 搜索游戏机
await searchProducts({
  keyword: 'PS5',
  budget: 3500,
  requireGoodCredit: true,
});
```

## 自然语言触发

用户说这些时会自动触发技能：

| 用户输入 | 解析结果 |
|---------|---------|
| "帮我找闲鱼上的 MacBook Air M1 预算 2300" | keyword=MacBook Air M1, budget=2300 |
| "搜索二手 iPhone 13 预算 3000 电池 85 以上" | keyword=iPhone 13, budget=3000, batteryMin=85 |
| "闲鱼上有没有 9 成新的 PS5" | keyword=PS5, condition=9 成新 |
| "帮我看看闲鱼相机 预算 5000" | keyword=相机，budget=5000 |

## 输出示例

```markdown
## 🎯 闲鱼搜索结果：MacBook Air M1 2020

**搜索条件**：预算 ¥2300-2500 | 成色 9 成新 | 电池≥85%

### 🏆 首选推荐

| 价格 | 地区 | 电池 | 信用 | 亮点 | 链接 |
|------|------|------|------|------|------|
| **¥2150** | 山东 | 循环 8 次 | 百分百好评 | 电池超新！全原无修 | [查看](url) |
| **¥2295** | 四川 | 未说明 | 卖家信用极好 | 1 小时前降价！ | [查看](url) |
| **¥2318** | 北京 | 89% | 百分百好评 | 两天不满意可退！ | [查看](url) |

### 💡 购买建议

**验机要点**：
- [ ] 要求卖家提供电池健康度截图
- [ ] 视频验机（屏幕、键盘、所有接口）
- [ ] 确认无 ID 锁
- [ ] 检查序列号

**砍价话术**：
```
你好，诚心想买，预算只有 2300，
可以的话我马上拍，不墨迹。
电池健康度能截个图吗？
```
```

## 多平台支持

```javascript
// 闲鱼
await searchProducts({ keyword: 'XXX', budget: 1000, platform: 'xianyu' });

// 转转
await searchProducts({ keyword: 'XXX', budget: 1000, platform: 'zhuanzhuan' });

// 拍拍
await searchProducts({ keyword: 'XXX', budget: 1000, platform: 'paipai' });

// 全平台搜索（需要分别调用）
const platforms = ['xianyu', 'zhuanzhuan', 'paipai'];
for (const platform of platforms) {
  await searchProducts({ keyword: 'XXX', budget: 1000, platform });
}
```

## 注意事项

1. **反爬虫限制**：闲鱼等平台有强反爬虫，无法直接抓取商品详情
2. **实时性**：二手商品价格波动快，推荐结果仅供参考
3. **交易安全**：提醒用户走平台担保交易，不要直接转账
4. **验机建议**：提供验机清单帮助用户避坑

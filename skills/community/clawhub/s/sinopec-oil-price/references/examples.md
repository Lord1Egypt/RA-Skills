# 使用示例

## 基本用法

### 查询广西油价

```javascript
const SinopecOilPriceSkill = require('./index.js');

async function main() {
  const skill = new SinopecOilPriceSkill();
  const result = await skill.getOilPrice({ province_name: '广西' });
  
  if (result.success) {
    console.log(`${result.date} ${result.province} 油价:`);
    const price = result.prices[0];
    console.log(`92号: ${price.gas_92.price}元/升`);
    console.log(`95号: ${price.gas_95.price}元/升`);
    console.log(`0号柴油: ${price.diesel_0.price}元/升`);
  }
}

main();
```

### 查询多个省份

```javascript
const provinces = ['广西', '广东', '湖南', '贵州'];

for (const name of provinces) {
  const result = await skill.getOilPrice({ province_name: name });
  if (result.success) {
    const price = result.prices[0];
    console.log(`${name}: 92#=${price.gas_92.price}, 95#=${price.gas_95.price}`);
  }
}
```

---

## 监控油价变化

### 单次监控

```javascript
const result = await skill.monitorOilPrice({ province_name: '广西' });

if (result.hasChanges) {
  console.log('油价有变动!');
  result.changes.forEach(c => {
    console.log(`${c.name}: ${c.old} → ${c.new}`);
  });
} else {
  console.log('油价无变化');
}
```

### 定时监控（配合 cron）

```bash
# 每日上午8:30自动查询并比较
30 8 * * * cd ~/.openclaw/workspace/skills/sinopec-oil-price && node monitor-oil-price.js >> logs/oil-price.log 2>&1
```

---

## 格式化输出

### 用户友好的消息格式

```javascript
function formatOilPriceMessage(result) {
  const price = result.prices[0];
  let msg = `⛽ ${result.province}油价（${result.date}）\n\n`;
  
  const types = [
    ['gas_92', '92号汽油'],
    ['gas_95', '95号汽油'],
    ['gas_98', '98号汽油'],
    ['diesel_0', '0号柴油']
  ];
  
  types.forEach(([key, name]) => {
    const p = price[key];
    if (p) {
      msg += `${name}: ${p.price}元/升`;
      if (p.change !== 0) {
        const arrow = p.change > 0 ? '↑' : '↓';
        msg += ` (${arrow}${Math.abs(p.change)})`;
      }
      msg += '\n';
    }
  });
  
  return msg;
}
```

---

## 错误处理

```javascript
const result = await skill.getOilPrice({ province_name: '不存在' });

if (!result.success) {
  console.error(`查询失败: ${result.message}`);
  // 输出: 查询失败: 未找到省份: 不存在
}
```

---

## 命令行测试

```bash
# 查询广西油价
node query-guangxi.js

# 测试监控（对比历史）
node monitor-oil-price.js
```

---

## 集成到 OpenClaw cron

创建定时任务配置 `~/.openclaw/workspace/cron/oil-price-monitor.yml`:

```yaml
# 中石化油价监控 - 每天查询广西油价
- schedule: "30 8 * * *"
  task: "sinopec-oil-price:monitor"
  params:
    province_name: "广西"
  description: "每日监控广西油价，变动时发送通知"
```

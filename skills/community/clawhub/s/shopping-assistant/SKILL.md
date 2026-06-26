# 购物助手 - Shopping Assistant

智能购物助手，提供查券、比价、价保等一站式购物服务。

## 🎯 核心功能

- 🔍 **智能查券**：自动查找商品优惠券
- 💰 **全网比价**：对比淘宝/京东/拼多多价格
- 🛡️ **一键价保**：自动申请价格保护
- 📊 **历史价格**：查看商品价格走势

## 📦 支持平台

| 平台 | 查券 | 比价 | 价保 |
|------|------|------|------|
| ✅ **淘宝/天猫** | 完整 | 支持 | 支持 |
| ✅ **京东** | 完整 | 支持 | 支持 |
| ✅ **拼多多** | 基础 | 支持 | 不支持 |

## 🚀 使用方法

### 1. 查券

发送商品链接，自动查找优惠券：

```bash
python3 ~/.openclaw/workspace/skills/shopping-assistant/scripts/shopping_helper.py <链接>
```

**示例：**

```bash
# 淘宝链接
python3 shopping_helper.py "https://s.click.taobao.com/X3lnM4n"

# 京东链接
python3 shopping_helper.py "https://u.jd.com/NOPmtDz"

# 拼多多链接
python3 shopping_helper.py "https://mobile.yangkeduo.com/goods.html?goods_id=123456"
```

**输出示例：**

```
🔍 正在查找优惠券...

📦 阿宽红油面皮酸辣粉组合整箱
✅ 已找到优惠券链接

💰 原价：¥82.23
🎫 优惠券：¥40
💰 券后价：¥29.9
💡 可省：¥52.33
🏪 店铺：阿宽旗舰店
📈 销量：100

✅ 查券完成！
```

### 2. 多平台比价

```bash
python3 ~/.openclaw/workspace/skills/shopping-assistant/scripts/price_compare_simple.py <链接>
```

**输出示例：**

```
📊 全网比价结果
━━━━━━━━━━━━━━━━━━

🥇 拼多多：¥4999（百亿补贴）
   🏪 品牌好货
   📈 销量：10万+
   ✅ 优势：价格最低

🥈 京东：¥5199（自营）
   🏪 Apple官方旗舰店
   📈 销量：5万+
   ✅ 优势：正品保障，售后好

🥉 淘宝：¥5299（天猫）
   🏪 Apple Store
   📈 销量：3万+
   ✅ 优势：官方授权

💡 购买建议：
   拼多多百亿补贴最便宜，省¥200
```

## 🔧 配置参数

在 `~/.openclaw/.env` 中配置：

```bash
# 折淘客（必需）
export ZHETAOKE_APP_KEY=xxx
export ZHETAOKE_SID=xxx

# 京东联盟（京东功能必需）
export JD_UNION_ID=xxx

# 淘宝联盟（淘宝功能必需）
export TAOBAO_PID=mm_xxx_xxx_xxx
```

## 📋 功能说明

### 查券功能
- ✅ 自动识别平台（淘宝/京东/拼多多）
- ✅ 查找商品优惠券
- ✅ 显示券后价格
- ✅ 显示店铺信息和销量

### 比价功能
- ✅ 对比三平台价格
- ✅ 显示各平台优势
- ✅ 给出购买建议

### 后台转链
- 用户发送链接查券时，后台自动转链
- 用户无感知，只显示查券结果
- 转链后的链接用于追踪佣金

## 📝 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2026-03-11 | 初始版本，支持查券、比价 |

## 💡 使用建议

1. **优先使用查券功能**，获取优惠券信息
2. **结合比价功能**，找到最优价格
3. **注意优惠券时效**，及时使用
4. **价格实时变动**，以实际页面为准

## 🔗 相关链接

- 淘宝：https://www.taobao.com
- 京东：https://www.jd.com
- 拼多多：https://www.pinduoduo.com

# 淘宝客全能工具箱 - Taobaoke Toolkit

淘宝客一站式解决方案，支持链接转链、全网比价、自动价保、佣金追踪。

## 🎯 核心功能

- 🔗 **智能转链**：淘宝/京东/拼多多链接自动转为你的佣金链接
- 💰 **全网比价**：对比三大平台价格，找出最低价
- 🛡️ **一键价保**：自动申请京东/淘宝价保，追回差价
- 📊 **佣金追踪**：记录转链和成交数据
- 🚀 **高佣转链**：通过折淘客API获取最高佣金

## 📦 支持平台

| 平台 | 支持格式 | 商品信息 | 佣金信息 |
|------|---------|---------|---------|
| ✅ **淘宝** | 淘口令、链接 | ✅ 完整 | ✅ 完整 |
| ✅ **京东** | 短链接、标准链接 | ✅ 完整 | ✅ 完整 |
| ✅ **拼多多** | mobile.yangkeduo.com链接 | ⚠️ 基础 | ⚠️ 基础 |

## 🔧 配置参数

在 `~/.openclaw/.env` 中配置：

```bash
# 折淘客（必需）
export ZHETAOKE_APP_KEY=07d16b40e9c7485d8573f936173aa6d9
export ZHETAOKE_SID=41886

# 京东联盟（京东转链必需）
export JD_UNION_ID=1001703383

# 淘宝联盟（淘宝转链必需）
export TAOBAO_PID=mm_200970015_125850084_116244500128

# 多多进宝（拼多多转链可选）
export PDD_PID=8834451_187671353
```

## 🚀 使用方法

### 主程序（推荐）

```bash
python3 ~/.openclaw/workspace/skills/taobaoke-tool/scripts/taobaoke_master.py <链接>
```

**示例：**

```bash
# 淘宝淘口令
python3 taobaoke_master.py "￥yKnuUEInvoQ￥ CZ11/"

# 京东链接
python3 taobaoke_master.py "https://u.jd.com/NOPmtDz"

# 拼多多链接
python3 taobaoke_master.py "https://mobile.yangkeduo.com/goods.html?goods_id=123456"
```

### 单独功能脚本

#### 1. 三平台转链
```bash
python3 convert_all_platforms.py <链接>
```

#### 2. 淘宝转链
```bash
python3 taobao_convert_v2.py <淘口令>
```

#### 3. 京东转链
```bash
python3 jd_batch_convert.py <京东链接>
```

## 📋 输出示例

```
🎉 转链成功!

📦 NEW BALANCE NB 男鞋女鞋2002R系列
💰 券后价: ¥659
💰 原价: ¥699
💎 佣金: ¥11.78 (2%)

🔗 你的推广链接:
   链接: https://u.jd.com/NGBSezK

✅ 用户通过此链接购买，你将获得佣金!
```

## 🔗 API接口说明

### 淘宝转链
- **接口**：`https://api.zhetaoke.com:10001/api/open_gaoyongzhuanlian_tkl_piliang.ashx`
- **必需参数**：`appkey`, `sid`, `pid`, `tkl`
- **返回**：淘口令、短链接、商品信息、佣金

### 京东/拼多多转链
- **接口**：`http://api.zhetaoke.com:20000/api/open_gaoyongzhuanlian_tkl_piliang.ashx`
- **必需参数**：`appkey`, `unionId`, `tkl`
- **返回**：推广链接

## 📦 依赖技能

- ✅ `taobao` - 淘宝/京东/拼多多比价
- ✅ `ecommerce-price-comparison` - 电商价格比较
- ✅ `ecommerce-scraper` - 电商数据爬取
- ✅ `jd-price-protect` - 京东自动价保
- ✅ `taobao-image-search` - 淘宝以图搜同款

## 📝 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2026-03-11 | 初始版本，基础转链功能 |
| v2.0.0 | 2026-03-11 | 整合三平台转链，添加主程序 |
| v2.1.0 | 2026-03-11 | 添加商品信息展示，优化输出格式 |

## 💡 使用建议

1. **优先使用主程序** `taobaoke_master.py`，自动识别平台并转链
2. **淘宝淘口令** 转链最完整，包含商品信息和佣金
3. **京东链接** 转链完整，支持商品详情
4. **拼多多** 基础转链，可生成推广链接

## ⚠️ 注意事项

- 转链前确保已配置正确的API密钥
- 淘宝转链需要 `sid` 和 `pid` 匹配
- 京东转链需要 `unionId`
- 佣金比例和金额以实际成交为准

## 🔗 相关链接

- 折淘客官网：https://www.zhetaoke.com
- 京东联盟：https://union.jd.com
- 淘宝联盟：https://pub.alimama.com
- 多多进宝：https://jinbao.pinduoduo.com

---
name: xianyu-publisher
description: >
  闲鱼自动化发布工具 - 帮助用户在闲鱼平台自动发布商品。
  支持：商品信息填写、图片上传、价格设置、批量发布。
  使用场景：(1) 批量上架商品到闲鱼
  (2) 自动发布闲置物品
  (3) 定时发布营销内容
  触发词：发布闲鱼、上架商品、闲鱼发布、自动上架
metadata:
  openclaw:
    emoji: "🐟"
    os: [linux, darwin, win32]
    requires:
      bins: [python3, pip]
    install:
      - id: pip-xianyu
        kind: pip
        package: playwright
        bins: [playwright]
        label: Install Playwright
---

# 闲鱼自动发布工具

基于Playwright的闲鱼自动化发布解决方案。

## 安装

```bash
# 安装playwright
pip install playwright
playwright install chromium
```

## 快速开始

### 1. 发布单个商品

```python
# 配置商品信息
goods = {
    "title": "【AI代写】演讲稿 述职报告 小说创作",
    "price": 30,
    "description": "24小时出稿，不满意可免费修改...",
    "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"]
}

# 发布商品
xianyu-publish --goods goods.json
```

### 2. 批量发布

```python
xianyu-publish --batch goods-list.json --interval 60
```

## 使用方式

### 命令行

```bash
# 登录闲鱼
xianyu-login

# 发布商品
xianyu-publish --config goods.json

# 查看已保存的账号
xianyu-accounts
```

### 作为Python模块

```python
from xianyu_publisher import GoodsPublisher, GoodsInfo

# 创建商品
 goods = GoodsInfo(
    title="商品标题",
    price=100,
    description="商品描述",
    images=["image1.jpg"]
)

# 发布
publisher = GoodsPublisher()
await publisher.publish(goods)
```

## 配置说明

### 商品信息格式 (goods.json)

```json
{
  "title": "商品标题（必填）",
  "price": 100,
  "original_price": 150,
  "description": "商品详细描述",
  "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],
  "category": "分类",
  "location": "发货地",
  "delivery": "包邮",
  "tags": ["标签1", "标签2"]
}
```

## 功能特性

- ✅ 自动登录（支持Cookie持久化）
- ✅ 商品信息发布
- ✅ 图片批量上传
- ✅ 价格设置
- ✅ 批量发布（带间隔）
- ✅ 反检测机制
- ✅ 登录状态保存

## 注意事项

1. **首次使用需要登录**：运行后会弹出浏览器窗口，请扫码登录
2. **登录状态会保存**：Cookie保存在本地，下次自动登录
3. **建议控制发布频率**：避免触发闲鱼风控
4. **图片路径**：需要提供本地图片的绝对路径

## 风险提示

- 本工具仅供学习和效率提升使用
- 请遵守闲鱼平台规则，合理使用自动化工具
- 过度频繁的操作可能导致账号受限

## 开源协议

AGPL-3.0 License

---

## 联系与支持

- **微信**: 190569625（备注：闲鱼工具）
- 有问题或需要定制服务可联系

商业使用请联系作者获取授权。
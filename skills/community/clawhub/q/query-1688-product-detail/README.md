# 1688 商品详情查询 SKILL

通过 AlphaShop API 查询 1688 跨境商品详情，支持 URL 或商品 ID 输入，返回结构化商品数据。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

## ✨ 核心特性

- 🔍 **多种输入方式** - 支持商品 URL、数字 ID、逗号分隔批量 ID
- 📦 **完整商品数据** - 标题、价格、图片、规格、供应商等
- 🚀 **简单易用** - 一条命令获取商品详情

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中配置（注意：使用 `apiKey`/`secretKey` 字段）：

```json5
{
  skills: {
    entries: {
      "query-1688-product-detail": {
        apiKey: "YOUR_ALPHASHOP_ACCESS_KEY",
        secretKey: "YOUR_ALPHASHOP_SECRET_KEY"
      }
    }
  }
}
```

密钥获取：访问 https://www.alphashop.cn/seller-center/apikey-management 申请。

## 🎯 使用方法

```bash
# 通过 URL 查询
python3 query.py "https://detail.1688.com/offer/945957565364.html"

# 通过商品 ID 查询
python3 query.py "945957565364"

# 批量查询
python3 query.py "945957565364,653762281679"
```

## 📁 项目结构

```
query-1688-product-detail/
├── SKILL.md                    # SKILL 配置文件
├── README.md                   # 本文档
├── requirements.txt            # Python 依赖
└── query.py                    # 商品详情查询脚本
```

## 📝 注意事项

1. **配置方式特殊** - 本 SKILL 使用 `apiKey`/`secretKey` 字段，而非 `env`
2. **URL 解析** - 自动从 `/offer/<id>.html` 或 `?offerId=<id>` 提取商品 ID
3. **依赖** - 需要 Python 3.8+ 和 `requests` 库
4. **AlphaShop 欠费** - 如返回欠费错误，需前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分

---

**最后更新**: 2026-03-19

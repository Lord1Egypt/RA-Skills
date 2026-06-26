# 1688 供应商搜索 SKILL

通过 AlphaShop API 搜索和筛选 1688 供应商，支持商品链接、图片 URL、关键词三种搜索方式。

## ✨ 核心特性

- 🔍 **多种搜索方式** - 关键词搜索、1688 商品链接搜索、以图搜货
- 🎯 **智能筛选** - 支持价格、起批量、48H 发货率等筛选
- 🏭 **供应商详情** - 公司信息、诚信通年限、服务评分等
- 🤖 **自动识别输入** - 自动判断输入类型（链接/图片/关键词）

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中配置：

```json5
{
  skills: {
    entries: {
      "search-1688-supplier": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

密钥获取：访问 https://www.alphashop.cn/seller-center/apikey-management 申请。

## 🎯 使用方法

### 关键词搜索

```bash
python3 scripts/search.py "连衣裙"
```

### 通过 1688 商品链接搜索

```bash
python3 scripts/search.py "https://detail.1688.com/offer/945957565364.html"
```

### 以图搜货

```bash
python3 scripts/search.py "https://example.com/product.jpg"
```

### 带筛选条件

```bash
python3 scripts/search.py "连衣裙" --max-price 50 --max-moq 100 --min-ship-rate-48h 90
```

## 📁 项目结构

```
search-1688-supplier/
├── SKILL.md                    # SKILL 配置文件
├── README.md                   # 本文档
├── requirements.txt            # Python 依赖
├── references/
│   └── api.md                  # API 参考文档
└── scripts/
    └── search.py               # 供应商搜索主脚本
```

## 📝 注意事项

1. **默认 Auto 模式** - 不要自行指定搜索模式，让 API 自动判断
2. **筛选条件** - 仅在用户明确要求时才添加，不要自作主张
3. **结果展示** - 返回筛选后的第一条匹配结果
4. **无结果处理** - 如实告知用户，不要偷偷去掉筛选条件重新搜索
5. **AlphaShop 欠费** - 如返回欠费错误，需前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分

---

**最后更新**: 2026-03-19

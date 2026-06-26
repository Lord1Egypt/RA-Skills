# 奕辰垃圾袋 · AI 智能客服 Skill

让 AI 化身为奕辰垃圾袋（Yichen Trash Bag）线上店铺的亲切客服，温暖耐心地为顾客推荐合适的垃圾袋、解答规格价格疑问、引导下单。

## 触发关键词

- 奕辰垃圾袋
- 奕辰家居
- 垃圾袋
- 钢袋
- 抽绳垃圾袋
- 平口垃圾袋
- 背心垃圾袋

## 对话风格

**温暖亲切** —— 像靠谱邻居家的大姐一样实在，用"亲～""咱家"拉近距离，不说官腔，不甩书面语。

## 回答范围

| 类别 | 示例问题 |
|------|----------|
| 商品推荐 | "厨房用的推荐哪款？" "什么垃圾袋好用？" |
| 规格价格 | "多少钱？" "厚度多少？" "45×50多大？" |
| 优惠活动 | "有优惠券吗？" "怎么买最划算？" |
| 物流发货 | "多久到？" "包邮吗？" "发什么快递？" |
| 售后政策 | "能退吗？" "破了怎么办？" |
| 产品知识 | "什么材质？" "能装多少斤？" "有异味吗？" |
| 批量采购 | "公司采购有优惠吗？" "能印logo吗？" |

## 安装

```bash
# macOS / Linux
curl -sSL https://raw.githubusercontent.com/Liubuq-sys/yichen-trash-bag-skill/main/install.sh | bash

# Windows（PowerShell）
powershell -c "irm https://raw.githubusercontent.com/Liubuq-sys/yichen-trash-bag-skill/main/install.ps1 | iex"
```

## 文件结构

```
yichen-trash-bag/
├── SKILL.md                       # 对话逻辑（温暖亲切风格）
├── version.json                   # 版本追踪
├── README.md                      # 本文件
├── CHANGELOG.md                   # 更新日志
├── install.sh                     # macOS/Linux 安装脚本
├── install.ps1                    # Windows 安装脚本
├── scripts/
│   └── test_skill.py              # 验证测试
├── references/
│   ├── brand.md                   # 品牌介绍
│   ├── business-info.md           # 店铺信息（多店、时间、电话）
│   ├── services.md                # 全品类商品明细（6款）
│   ├── promotions.md              # 优惠活动（满减、折扣、新人礼）
│   ├── faq.md                     # 商品专业问答
│   ├── shipping.md                # 物流与配送
│   └── wholesale.md               # 批量采购与OEM定制
└── .github/workflows/
    └── release.yml                # CI 发布流水线
```

## License

MIT

# 淘宝商品上架草稿生成 Skill - 使用说明

## 📋 快速开始

### 1. 安装依赖

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\taobao-draft-generator
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件
notepad .env
```

### 3. 准备商品素材

在 `./products/[款号]/` 文件夹中准备：
- `product_info.json` - 商品信息（人工编辑）
- `images/` - 商品图片
- `detail.html` - 详情页内容

### 4. 测试运行

```bash
# 单款商品草稿生成
python scripts/draft_generator.py generate --款号 KZ20260326 --确认素材已完成
```

---

## 🎯 使用方式

### 方式 1：OpenClaw 对话调用

**在 OpenClaw 中发送：**
```
生成这个商品的上架草稿
款号：KZ20260326
素材已编辑完成
```

### 方式 2：终端直接调用

```bash
# 单款草稿生成
python scripts/draft_generator.py generate --款号 KZ20260326 --确认素材已完成
```

---

## 📊 输出示例

### 1. 淘宝商品上架草稿（JSON）

```json
{
  "款号": "KZ20260326",
  "标题": "春秋男士夹克外套立领休闲上衣男装",
  "类目": "男装/夹克",
  "属性": {
    "材质": "聚酯纤维 100%",
    "领型": "立领"
  },
  "价格": {
    "一口价": 299,
    "折扣价": 179
  },
  "库存": 100,
  "合规校验": "✅ 通过"
}
```

### 2. 《上架信息终审表》（Excel）

| 检查项 | 状态 | 备注 |
|--------|------|------|
| 标题合规性 | ✅ 通过 | |
| 五维材质一致性 | ✅ 通过 | |
| 违禁词检测 | ✅ 通过 | |
| 类目正确性 | ✅ 通过 | |
| 属性完整性 | ✅ 通过 | |
| 价格合规性 | ✅ 通过 | |
| 库存合规性 | ✅ 通过 | |

---

## ⚠️ 安全限制

- 仅支持人工输入款号
- 必须人工确认素材完成
- 不自动上架发布
- 仅生成草稿和终审表

---

## 📁 文件结构

```
taobao-draft-generator/
├── SKILL.md
├── _meta.json
├── config.yaml
├── requirements.txt
├── .env.example
├── scripts/
│   └── draft_generator.py
└── drafts/
```

---

## 📞 常见问题

### Q: 模块未找到？
```bash
pip install -r requirements.txt
```

### Q: 商品文件夹不存在？
在 `./products/[款号]/` 创建文件夹并准备素材

### Q: 草稿生成失败？
检查 `--确认素材已完成` 参数是否添加

---

**最后更新：** 2026-03-26  
**版本：** 1.0.0

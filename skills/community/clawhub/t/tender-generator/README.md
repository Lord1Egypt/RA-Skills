# 专业标书生成器 V3 (Tender Generator Pro)

通过对话式交互收集项目信息，自动填充模板生成全套规范化投标文档。

## 🚀 快速开始

### 方式一：命令行（推荐）

```bash
# 1. 创建信息文件
cat > info.json << 'EOF'
{
  "project_name": "项目名称",
  "tender_number": "项目编号",
  "company_name": "公司全称",
  "credit_code": "信用代码",
  "authorized_rep": "授权代表",
  "total_price": "报价"
}
EOF

# 2. 生成标书
python3 scripts/generate_bid.py --info info.json --output ./output

# 3. 查看结果
ls -la output/
```

### 方式二：交互式收集

```bash
python3 scripts/generate_bid.py --interactive
```

### 方式三：从文档提取信息

```bash
# 从文本提取
python3 scripts/generate_bid.py --extract source.txt --output info.json

# 从Word文档提取
python3 scripts/generate_bid.py --extract proposal.docx --output info.json
```

### 方式四：校验信息

```bash
python3 scripts/generate_bid.py --info info.json --validate
```

## 📋 功能特性

| 功能 | 说明 |
|------|------|
| 智能信息提取 | 从文本/文档自动识别关键信息 |
| 多行业模板 | 默认/IT/建筑/服务行业模板 |
| 专业文档样式 | 页眉页脚、统一字体、专业排版 |
| 合规自检 | 自动扫描未填充占位符 |
| 批量生成 | 支持一次生成多个项目文档 |
| 信息校验 | 自动校验格式一致性 |
| 一键打包 | 生成带时间戳的zip压缩包 |

## 📁 文件结构

```
tender-generator/
├── SKILL.md                 # 主文档
├── _meta.json               # 元数据
├── README.md                # 使用说明
├── info_example.json        # 示例信息
├── scripts/
│   ├── generate_bid.py      # 生成脚本 V3
│   └── create_template.py   # 模板创建脚本
└── templates/
    ├── default/             # 默认模板
    ├── it/                  # IT行业模板
    ├── construction/        # 建筑工程模板
    └── service/             # 服务行业模板
```

## 🔧 占位符列表

| 占位符 | 含义 | 必填 |
|--------|------|------|
| `{{project_name}}` | 项目名称 | ✓ |
| `{{tender_number}}` | 项目编号 | - |
| `{{tenderer}}` | 招标人 | - |
| `{{deadline}}` | 截止日期 | - |
| `{{company_name}}` | 公司全称 | ✓ |
| `{{credit_code}}` | 统一社会信用代码 | ✓ |
| `{{company_address}}` | 公司地址 | - |
| `{{legal_rep}}` | 法定代表人 | - |
| `{{authorized_rep}}` | 授权代表 | ✓ |
| `{{authorized_rep_phone}}` | 授权代表电话 | - |
| `{{total_price}}` | 总报价 | ✓ |
| `{{bank_name}}` | 开户银行 | - |
| `{{bank_account}}` | 银行账号 | - |
| `{{bank_code}}` | 联行号 | - |

## 📝 完整示例

```bash
# 1. 复制示例信息文件
cp info_example.json info.json

# 2. 编辑信息文件，填入实际数据
nano info.json

# 3. 生成标书
python3 scripts/generate_bid.py --info info.json --output ./output

# 4. 查看生成的文件
ls -lh output/

# 5. 检查压缩包
unzip -l 标书文档包_*.zip
```

## ⚠️ 注意事项

1. **自动生成内容仅供参考**，正式使用前请人工审核
2. **需要盖章/签字的文件**需手动替换为实际扫描件
3. **技术参数必须100%照搬**招标文件要求，不得修改
4. **信用代码格式**应为18位

## 🔄 版本历史

- **V3.0.0** (2026-08-25): 智能提取、多行业模板、专业样式、批量生成
- **V2.0.0** (2026-08-25): 内置模板、合规自检、一键打包
- **V1.1.0** (2026-08-03): 初版

## 📞 技术支持

如有问题，请检查：
1. Python 版本 ≥ 3.8
2. 已安装 `python-docx` 库
3. JSON 文件格式正确
4. 文件路径正确

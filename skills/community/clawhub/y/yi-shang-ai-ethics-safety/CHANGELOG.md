# 📝 更新日志

## v1.2.1 (2026-03-30) - 安全修复版

### 🔒 安全改进

**移除隐私风险代码:**
- ✅ 移除 `subprocess.run(['sh', '-c', 'history 10'])` - 不再读取 Shell 历史记录
- ✅ 移除硬编码路径 `/Users/figocheung/.openclaw/...` - 使用动态相对路径
- ✅ 所有脚本改用参数化配置，支持自定义输入和输出目录

**新增安全文档:**
- ✅ 新增 `SECURITY.md` - 完整的安全与隐私声明
- ✅ 更新 `SKILL.md` - 新增"安全与隐私声明"章节
- ✅ 更新 `README.md` - 说明参数化使用方法

**符合规范:**
- ✅ 符合 ClawHub 技能安全规范
- ✅ 解决 INSTRUCTION SCOPE 警告
- ✅ 无敏感信息访问风险

### 🔧 功能改进

**run_audit.py:**
- ✅ 支持 `--text` 参数：指定待检测文本
- ✅ 支持 `--output-dir` 参数：指定报告输出目录
- ✅ 改用 `Path(__file__).parent` 动态获取路径

**generate_audit_report.py:**
- ✅ 改用相对路径导入模块
- ✅ 移除个人化测试数据

### 📦 文件清单

```
yi-shang-ai-ethics-safety/
├── SKILL.md                    # 核心技能文档
├── README.md                   # 使用指南
├── SECURITY.md                 # 安全声明 ⭐新增
├── CHANGELOG.md                # 更新日志 ⭐新增
├── _meta.json                  # 元数据配置
├── publish-script.sh           # 发布脚本 ⭐新增
├── scripts/
│   ├── run_audit.py            # 审计脚本 ⭐重构
│   ├── authenticity_guard.py   # 本真性检测
│   ├── alienation_protection.py # 异化防护
│   ├── value_alignment.py      # 价值观对齐
│   ├── equality_measurement.py # 三商测评
│   ├── monitor.py              # 持续监控
│   ├── test_all.py             # 测试套件
│   └── reports/
│       └── generate_audit_report.py  # 报告生成 ⭐优化
└── references/
    ├── theory.md               # 理论基础
    ├── equality_measurement.md # 测评详解
    └── personality_matrix.md   # 人格矩阵
```

### 📊 验证结果

```
✅ Python 语法检查通过
✅ 无 subprocess 调用
✅ 无硬编码个人路径
✅ 无 Shell 历史记录读取
✅ 功能测试通过
✅ 符合 ClawHub 安全规范
```

---

## v1.2.0 (2026-03-17) - 功能完善版

### ✨ 新增功能

- ✅ 新增检测报告生成功能
- ✅ 完善三商测评体系
- ✅ 增强异化模式检测
- ✅ 优化人格矩阵支持

### 📚 文档更新

- ✅ 完善 SKILL.md 使用示例
- ✅ 更新 README.md 快速开始
- ✅ 添加审计报告模板

---

## v1.1.0 (2026-03-14) - 初始版本

### 🎯 核心功能

- ✅ AI 伦理安全检测框架
- ✅ 三商测评系统（IIQ/EQ/IQ）
- ✅ 异化模式识别
- ✅ 价值观对齐检查

### 📝 理论框架

- ✅ 情智义三商人格理论
- ✅ AI 树德框架
- ✅ 道儒佛价值融合

---

*维护者：Figo Cheung, 云图 (CloudEye)*  
*使命：以义为体，以情智为用* 🌿

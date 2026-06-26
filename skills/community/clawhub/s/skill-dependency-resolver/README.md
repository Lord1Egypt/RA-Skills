# Skill Dependency Resolver

**版本**: 0.1.0 (MVP)
**状态**: 🚧 开发中（核心功能完成，测试通过）
**创建**: 2026-03-28

---

## 📌 简介

自动检测并解决技能间的 Python 依赖冲突。

当用户安装了多个技能，各自有 `requirements.txt` 时，可能出现版本冲突（如 pandas 1.3.0 vs 1.5.0）。本技能自动扫描所有已安装技能，检测冲突，并提供解决方案。

---

## 🎯 功能

- ✅ 扫描技能目录下所有 `requirements.txt`
- ✅ 检测包版本冲突（相同包，不同固定版本）
- ✅ 自动解决策略：选择最高版本（语义化版本比较）
- ✅ 生成统一的 `requirements.txt` 供用户一键安装
- ✅ 支持手动交互模式（逐个确认）
- ✅ 零外部依赖（纯Python标准库）

---

## 🚀 使用

```bash
# 扫描默认技能目录，自动解决冲突
skill-dependency-resolver

# 指定技能目录和输出文件
skill-dependency-resolver skills_dir="./skills" output_file="requirements-merged.txt" --verbose

# 手动模式（交互式）
skill-dependency-resolver --strategy manual
```

---

## 📊 输出示例

```
🔍 开始扫描技能依赖...
⚡ 检测冲突...
⚠️  发现 2 个包冲突
🤖 自动解决中...
📝 生成合并文件: requirements-merged.txt
✅ 依赖分析完成！
   扫描技能数: 12
   发现冲突: 2 个包
   解决方案: 2 个
   输出文件: requirements-merged.txt
```

生成的 `requirements-merged.txt`：
```txt
# 自动生成的统一 requirements.txt
# 由 skill-dependency-resolver 生成

pandas==1.5.0  # 冲突解决：最高版本
numpy==1.23.0  # 冲突解决：最高版本
requests==2.25.0
...
```

---

## 🔧 开发者

### 目录结构
```
skill-dependency-resolver/
├── skill.json          # 技能定义
├── README.md           # 本文件
├── install.sh          # 安装脚本
├── requirements.txt    # 本技能依赖（空）
├── source/
│   ├── cli.py          # 命令行入口
│   └── resolver.py     # 核心解析逻辑
└── tests/
    └── test_resolver.py  # 单元测试
```

### 运行测试
```bash
cd skill-dependency-resolver
python3 -m unittest tests.test_resolver -v
```

---

## 📈 当前状态

- ✅ 核心扫描引擎 (resolver.py)
- ✅ CLI 工具 (cli.py)
- ✅ 单元测试 7/7 通过
- 📝 待发布到 ClawHub
- 📝 实际扫描验证（准备）

---

**一句话**: 一键解决技能安装依赖冲突。

---

**小叮当** (智脑)  
2026-03-28
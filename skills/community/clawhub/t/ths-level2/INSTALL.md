# 同花顺Level2 Skill 安装指南

## 📦 安装方法

### 方法一：OpenClaw CLI 安装（推荐）
```bash
# 如果已发布到ClawHub
openclaw skills install ths-level2

# 或从本地目录安装
openclaw skills install ./ths_level2
```

### 方法二：手动安装
```bash
# 1. 复制技能目录到OpenClaw技能目录
cp -r ths_level2 ~/.openclaw/skills/

# 2. 验证安装
openclaw skills list | grep ths-level2
```

### 方法三：Git安装
```bash
# 克隆到skills目录
git clone https://github.com/your-username/ths-level2.git ~/.openclaw/skills/ths_level2
```

## ⚙️ 依赖安装

### Python依赖
```bash
# 安装核心依赖
pip install akshare pandas numpy

# 或使用requirements.txt
pip install -r requirements.txt
```

### 系统依赖
- **Windows**: 需要安装 Visual C++ Redistributable
- **Linux**: 需要安装 gcc 和 python3-dev
- **Mac**: 需要安装 Xcode Command Line Tools

## 🔧 配置步骤

### 1. 基础配置
编辑 `config.json` 文件：
```json
{
  "tushare_token": "",           // 可选：Tushare API Token
  "ths_path": "D:\\同花顺远航版", // 同花顺安装路径
  "default_stocks": [...]        // 默认分析股票列表
}
```

### 2. Tushare Token配置（可选但推荐）
```bash
# Windows
setx TUSHARE_TOKEN your_token_here

# Linux/Mac  
export TUSHARE_TOKEN=your_token_here
```

### 3. 同花顺路径配置
确保 `ths_path` 指向正确的同花顺安装目录：
- **默认路径**: `D:\同花顺远航版`
- **自定义路径**: 修改 `config.json` 中的 `ths_path`

## 🚀 快速开始

### 基础使用
```bash
# 进入技能目录
cd ~/.openclaw/skills/ths_level2

# 运行基础分析
python ths_local_analysis.py
```

### 高级功能
```bash
# 完整技术指标分析
python complete_technical_analysis.py

# 筹码分析
python chip_analysis.py

# Level2深度分析  
python level2_integration.py
```

## 📊 功能验证

### 测试本地数据读取
```bash
python ths_client.py
```
预期输出：
```
已加载 67628 只股票信息
成功连接到 hevo-h.10jqka.com.cn:9601
```

### 测试基础分析
```bash
python ths_local_analysis.py
```
预期输出：持仓股票分析报告

## 🆘 故障排除

### 常见问题

**1. Unicode编码错误**
```bash
# Windows解决方法
chcp 65001
python ths_local_analysis.py

# 或设置环境变量
set PYTHONIOENCODING=utf-8
```

**2. 缺少依赖库**
```bash
pip install akshare pandas numpy --user
```

**3. 无法找到同花顺数据库**
- 检查 `ths_path` 配置是否正确
- 确保同花顺已安装并运行过
- 数据库路径: `{ths_path}\bin\stockname\stocknameV2.db`

**4. 网络连接失败**
- 使用本地分析模式（无需网络）
- 检查防火墙设置
- 确保可以访问 `hevo-h.10jqka.com.cn`

### 调试命令
```bash
# 查看技能信息
openclaw skills info ths-level2

# 测试技能加载
python -c "import sys; sys.path.append('.'); from ths_local_analysis import TechnicalAnalyzer"

# 检查配置文件
cat config.json
```

## 📁 目录结构

```
ths_level2/
├── SKILL.md                    # 技能描述
├── _meta.json                  # 元数据
├── .clawhub/                   # ClawHub标识
│   └── manifest.json
├── INSTALL.md                  # 安装指南
├── config.json                 # 配置文件
├── requirements.txt            # 依赖列表
├── ths_client.py               # 数据客户端
├── ths_local_analysis.py       # 基础分析
├── complete_technical_analysis.py # 完整技术指标
├── chip_analysis.py            # 筹码分析
└── level2_integration.py       # Level2集成分析
```

## 📝 升级维护

### 更新技能
```bash
# 从ClawHub更新
openclaw skills update ths-level2

# 手动更新
git pull origin main
```

### 自定义修改
- 修改 `config.json` 调整默认参数
- 编辑分析脚本添加自定义指标
- 扩展 `HOLDINGS` 数据支持更多股票

## 📈 版本历史

- **v1.0.0** (2026-03-27): 初始版本，支持完整技术指标、筹码分析、Level2模拟分析

## 🔗 相关链接

- **OpenClaw文档**: https://docs.openclaw.ai
- **技能开发指南**: https://docs.openclaw.ai/skills
- **同花顺API**: https://www.10jqka.com.cn/
- **Tushare**: https://tushare.pro

---
> 💡 **提示**: 本技能完全开源，欢迎贡献代码和改进建议！
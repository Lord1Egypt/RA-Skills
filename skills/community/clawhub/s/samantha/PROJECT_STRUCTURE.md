# Samantha 项目结构

## 📁 目录结构

```
samantha/
├── README.md                    # 项目主文档（中英文双语）
├── CONTRIBUTING.md              # 贡献指南
├── LICENSE                      # MIT许可证
├── requirements.txt             # Python依赖
├── requirements-dev.txt         # 开发依赖
├── .gitignore                   # Git忽略文件
├── .github/                     # GitHub配置
│   ├── workflows/              # CI/CD工作流
│   ├── ISSUE_TEMPLATE/         # Issue模板
│   └── PULL_REQUEST_TEMPLATE/  # PR模板
├── src/                         # 源代码
│   ├── __init__.py
│   ├── core/                   # 核心引擎
│   │   ├── __init__.py
│   │   ├── engine.py          # 主引擎
│   │   ├── memory.py          # 记忆系统
│   │   └── personality.py     # 人格演化
│   ├── emotion/               # 情感模块
│   │   ├── __init__.py
│   │   ├── analyzer.py        # 情感分析
│   │   └── tracker.py         # 情感追踪
│   ├── mbti/                  # MBTI分析
│   │   ├── __init__.py
│   │   ├── analyzer.py        # MBTI分析器
│   │   └── adapter.py         # 沟通适配器
│   ├── voice/                 # 语音集成
│   │   ├── __init__.py
│   │   ├── tts.py             # 文字转语音
│   │   └── stt.py             # 语音转文字
│   ├── space/                 # 空间感知
│   │   ├── __init__.py
│   │   ├── awareness.py       # 空间感知
│   │   └── triggers.py        # 智能触发
│   └── utils/                 # 工具函数
│       ├── __init__.py
│       ├── config.py          # 配置管理
│       └── logger.py          # 日志系统
├── tests/                      # 测试代码
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_emotion.py
│   ├── test_mbti.py
│   └── test_voice.py
├── docs/                       # 文档
│   ├── index.md               # 文档首页
│   ├── installation.md        # 安装指南
│   ├── usage.md               # 使用指南
│   ├── api/                   # API文档
│   └── examples/              # 示例代码
├── examples/                   # 使用示例
│   ├── basic_usage.py         # 基础使用
│   ├── mbti_demo.py           # MBTI演示
│   └── voice_demo.py          # 语音演示
├── data/                       # 数据文件
│   ├── memory.db              # SQLite数据库
│   ├── mbti_profiles.json     # MBTI配置文件
│   └── emotion_models/        # 情感模型
├── scripts/                    # 脚本文件
│   ├── init_db.py             # 初始化数据库
│   ├── train_model.py         # 训练模型
│   └── deploy.py              # 部署脚本
└── config/                     # 配置文件
    ├── default.yaml           # 默认配置
    ├── development.yaml       # 开发环境配置
    └── production.yaml        # 生产环境配置
```

## 🎯 核心模块说明

### **1. 核心引擎 (core/)**
- `engine.py`: 主引擎，协调所有模块工作
- `memory.py`: 记忆系统，存储和检索对话历史
- `personality.py`: 人格演化，根据互动调整AI性格

### **2. 情感模块 (emotion/)**
- `analyzer.py`: 分析用户输入的情感倾向
- `tracker.py`: 追踪长期情感变化，生成情感曲线

### **3. MBTI模块 (mbti/)**
- `analyzer.py`: 分析用户的MBTI人格类型
- `adapter.py`: 根据MBTI类型调整沟通方式

### **4. 语音模块 (voice/)**
- `tts.py`: 文字转语音，支持情感语调
- `stt.py`: 语音转文字，支持多语言

### **5. 空间感知模块 (space/)**
- `awareness.py`: 感知用户物理位置和场景
- `triggers.py`: 智能触发，如"你到家了"问候

## 🔧 开发工作流

### **1. 环境设置**
```bash
# 克隆仓库
git clone https://github.com/leilei926524-tech/samantha.git
cd samantha

# 设置虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### **2. 运行测试**
```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/test_core.py -v

# 生成测试覆盖率报告
pytest --cov=src --cov-report=html
```

### **3. 代码规范**
```bash
# 代码格式化
black src/ tests/

# 代码检查
flake8 src/ tests/

# 类型检查
mypy src/
```

### **4. 提交代码**
```bash
# 创建功能分支
git checkout -b feature/your-feature

# 添加更改
git add .

# 提交更改
git commit -m "feat: add your feature description"

# 推送到远程
git push origin feature/your-feature

# 创建Pull Request
```

## 📊 数据流示意图

```
用户输入
    ↓
[语音识别] → STT模块
    ↓
[情感分析] → Emotion模块
    ↓
[MBTI分析] → MBTI模块
    ↓
[记忆检索] → Memory模块
    ↓
[响应生成] → Core Engine
    ↓
[语音合成] → TTS模块
    ↓
用户输出
```

## 🚀 部署说明

### **本地部署**
```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 运行应用
python src/main.py
```

### **Docker部署**
```bash
# 构建镜像
docker build -t samantha .

# 运行容器
docker run -p 8000:8000 samantha
```

### **云部署**
- **Vercel**: 前端部署
- **Railway**: 后端部署
- **Supabase**: 数据库服务
- **Cloudflare**: CDN和DNS

## 🔍 监控与日志

### **日志配置**
```yaml
# config/logging.yaml
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
  file:
    class: logging.FileHandler
    filename: logs/samantha.log
    level: INFO
    formatter: simple
loggers:
  samantha:
    level: DEBUG
    handlers: [console, file]
```

### **监控指标**
- 响应时间
- 内存使用
- CPU使用率
- 错误率
- 用户活跃度

## 📈 项目路线图

### **Phase 1: MVP (已完成)**
- [x] 基础对话引擎
- [x] 本地记忆存储
- [x] 基础TTS集成

### **Phase 2: 情感智能 (进行中)**
- [ ] MBTI人格分析
- [ ] 情感追踪可视化
- [ ] 多模态感知

### **Phase 3: 物理陪伴 (规划中)**
- [ ] 智能家居联动
- [ ] 健康数据监测
- [ ] 空间感知优化

### **Phase 4: 社区生态 (未来)**
- [ ] 插件系统
- [ ] 第三方集成
- [ ] 企业级解决方案

---

*最后更新: 2026-03-19*
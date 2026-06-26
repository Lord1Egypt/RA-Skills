# Source to Architecture - 源码到架构图生成技能

## 版本信息
- **当前版本**: v2.0.0
- **发布日期**: 2026-03-20
- **状态**: 生产就绪 (Production Ready)

## 版本变更历史

### v2.0.0 (2026-03-20) - 重大优化版本
- **架构重构**: 从原有的四层架构升级为标准五层分层架构
  - 接入层 (Access Layer)
  - 路由/控制层 (Routing/Control Layer)  
  - 逻辑层 (Logic Layer)
  - 数据访问层 (Data Access Layer)
  - 存储/外部层 (Storage/External Layer)
- **排版规范强化**: 完全遵循用户提供的详细排版规范
  - 强制 Top-to-Bottom 分层布局
  - 20px 全局网格对齐
  - 同层级统一高度(60px)/宽度(120px)
  - 固定间距(水平80px, 垂直60px)
- **视觉规范统一**:
  - 形状标准化: 矩形(业务模块)、圆柱体(存储)、六边形(MQ)、斜角矩形(外部系统)、圆角矩形(函数)
  - 颜色体系固定: 浅蓝/浅绿/浅黄/浅紫/灰色按层区分
  - 字体统一: Arial 12px常规, 14px标题
- **连线规则优化**:
  - 正交连线(仅水平/垂直)
  - 箭头样式统一(数据流→、调用⇢、依赖直线)
  - 自动减少交叉(≤5处)
- **自动美化约束**:
  - 节点间距≥60px
  - 文字完整可见不遮挡
  - 分组框完整包裹模块
  - 层间明显空白区
- **代码质量提升**:
  - 完全重写的 DrawIO 生成器
  - 更智能的组件分类算法
  - 支持微服务分组框
  - 自动路由优化

### v1.0.0 (2026-03-19) - 初始版本
- 基础四层架构支持
- 基本 DrawIO 图表生成
- 简单的源码分析功能

## 功能特性

### 核心能力
- **五层分层架构**: 严格遵循接入层→控制层→逻辑层→数据访问层→存储层的标准架构
- **自动化源码分析**: 自动扫描项目目录，提取物理结构和依赖关系
- **智能逻辑映射**: 基于业务域和文件命名自动映射到对应架构层
- **专业排版输出**: 生成符合企业级标准的架构图

### 输出格式
- **DrawIO 源文件**: `.drawio` 格式，支持在线编辑
- **PNG 预览**: 自动生成 PNG 格式预览图
- **多场景交付**: 支持文档嵌入、评审会议、团队协作等场景

### 工具链集成
- **代码分析**: ripgrep、tree、静态代码分析工具
- **图表生成**: draw.io CLI、Graphviz
- **环境固化**: Docker 容器化支持
- **CI/CD 集成**: 支持自动化流水线

## 使用方法

### 安装依赖
```bash
cd /home/Vincent/.openclaw/workspace/skills/source-to-architecture/scripts
./install-tools.sh
```

### 基本使用
```bash
# 1. 分析源码
python scripts/source-analyzer.py <项目路径> analysis.json

# 2. 生成架构图  
python scripts/drawio-generator.py analysis.json output/

# 3. 导出图片
drawio --export --format png output/*.drawio
```

### Docker 支持
```bash
# 构建容器
docker build -t source-to-architecture .

# 运行分析
docker run -v $(pwd):/workspace source-to-architecture \
  python scripts/source-analyzer.py /workspace/my-project analysis.json
```

## 技术要求

### 系统依赖
- Python 3.7+
- Node.js 14+
- ripgrep
- tree
- drawio-desktop

### 输入支持
- **编程语言**: Python, JavaScript, TypeScript, Java
- **项目类型**: 单体应用、微服务、前后端分离项目

## 质量保证

- **排版一致性**: 严格遵循企业级架构图标准
- **可维护性**: 支持 Git 版本控制和协作
- **可扩展性**: 模块化设计，易于扩展新功能
- **性能优化**: 大型项目支持增量分析

## 许可证
MIT License

## 维护者
- Vincent (@vincentlau2046)
- OpenClaw Team
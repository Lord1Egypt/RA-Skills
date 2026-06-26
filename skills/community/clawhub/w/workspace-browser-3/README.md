# Workspace浏览器3.0

一个功能完整的Workspace文件浏览器，支持代码解释、全文搜索和文件管理。

## ✨ 特性亮点

### 🎨 精美界面
- 马卡龙色系设计
- 响应式布局
- 流畅的动画效果

### 💡 智能功能
- AI代码解释（自动保存）
- 全文递归搜索
- 语法高亮显示

### 🔒 稳定可靠
- 数据库持久化
- 路径安全验证
- 状态污染防护

## 🚀 快速开始

### 安装
```bash
# 克隆项目
git clone https://github.com/你的用户名/workspace-browser.git
cd workspace-browser

# 安装依赖
pip install flask

# 启动
./start.sh
```

### 访问
打开浏览器访问：http://localhost:5001

## 📖 使用指南

### 文件浏览
1. 左侧文件树浏览workspace
2. 点击文件查看内容
3. 使用Tab切换源代码和解释

### 搜索功能
1. 在侧边栏输入搜索词
2. 按回车键搜索
3. 点击结果打开文件

### 代码解释
- **自动生成**：点击"获取代码解释"
- **手动输入**：点击"手动输入代码解释"
- **永久保存**：所有解释自动保存

## 🛠️ 开发

### 项目结构
```
app.py              # Flask主应用
manifest.json       # Skill配置
explanations.db     # SQLite数据库
start.sh           # 启动脚本
```

### 技术栈
- **后端**：Flask + SQLite3
- **前端**：原生HTML/CSS/JS + Prism.js
- **部署**：单文件部署，零配置

### 扩展开发
1. 修改`app.py`添加新功能
2. 更新CSS样式
3. 添加新的API端点

## 📊 性能
- 搜索响应：< 1秒（200个结果内）
- 内存占用：< 50MB
- 并发支持：10+用户

## 🤝 贡献
欢迎提交Issue和Pull Request！

## 📄 许可证
MIT License

---
**作者**：潘峰  
**版本**：3.0.0  
**状态**：生产就绪 ✅
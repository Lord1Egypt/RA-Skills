# WorkTracker 📋

简单快速的工作日志系统，专为AI助手团队设计。

## 🎯 概述

WorkTracker是一个专为AI助手团队设计的简单工作日志系统，解决助手忘记报告工作进展的问题，确保所有工作都有记录、可追踪、可报告。

## ✨ 特性

- ✅ **简单易用**：几个命令即可掌握
- ✅ **实时跟踪**：工作状态实时更新
- ✅ **团队协作**：支持多助手团队管理
- ✅ **自动备份**：数据自动备份，安全可靠
- ✅ **可扩展**：支持自定义助手和配置
- ✅ **数据导出**：支持JSON和CSV格式导出

## 🚀 快速开始

### 安装
```bash
# 通过skillhub安装
skillhub install worktracker

# 或通过clawhub安装
clawhub install isenlink/worktracker
```

### 基础使用
```bash
# 开始工作
worktracker start "助手名" "工作描述" "截止时间"

# 更新进展
worktracker update "助手名" 进度百分比 "更新内容"

# 完成工作
worktracker complete "助手名" "完成结果" "后续事项"

# 查看状态
worktracker status

# 查看日志
worktracker log
```

## 📖 文档

- [完整技能文档](SKILL.md) - 详细的功能说明和API参考
- [培训手册](docs/WorkTracker培训手册.md) - 完整的培训材料
- [基础使用示例](examples/basic_usage.sh) - 快速上手的示例
- [团队协作示例](examples/team_collaboration.sh) - 团队协作场景示例

## 🛠️ 开发

### 项目结构
```
worktracker/
├── SKILL.md              # 技能主文档
├── config.json          # 技能配置文件
├── README.md            # 项目说明
├── scripts/
│   └── worktracker.py   # 主脚本
├── docs/
│   └── WorkTracker培训手册.md
└── examples/
    ├── basic_usage.sh
    └── team_collaboration.sh
```

### 技术要求
- Python 3.8+
- OpenClaw 2026.3.0+

### 测试
```bash
# 运行测试
worktracker test
```

## 🤝 贡献

欢迎贡献代码！请阅读[贡献指南](CONTRIBUTING.md)。

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 👥 作者

- **iSenlink** - 初始工作和维护
- 查看[贡献者](https://github.com/isenlink/worktracker/contributors)列表

## 🙏 致谢

- 感谢所有使用和反馈的用户
- 感谢OpenClaw社区的支持
- 感谢贡献代码的开发者

## 📞 支持

- **问题反馈**：[GitHub Issues](https://github.com/isenlink/worktracker/issues)
- **文档**：[SKILL.md](SKILL.md)
- **邮件**：support@isenlink.com

---

**版本**：v1.0.0  
**最后更新**：2026-03-14  
**状态**：✅ 生产就绪
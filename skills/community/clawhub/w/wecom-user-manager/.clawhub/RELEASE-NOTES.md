# wecom-user-manager v1.0.0 发布说明

_2026-03-28 发布_

---

## 🎉 发布信息

| 项目 | 详情 |
|------|------|
| **Skill 名称** | wecom-user-manager |
| **版本号** | 1.0.0 |
| **发布日期** | 2026-03-28 |
| **作者** | 杨广伟（巽融科技） |
| **许可证** | MIT |
| **分类** | 企业应用 / 生产力工具 |

---

## 🌟 核心功能

### 1. 添加用户权限
- 支持自然语言命令
- 发送确认卡片
- 严格的权限控制

### 2. 自动激活
- 用户首次登录自动激活
- 自动获取真实姓名
- 发送个性化欢迎消息

### 3. 完整的用户生命周期
```
添加用户 → 待激活 → 首次登录 → 自动激活 → 正常使用
```

---

## 📱 使用示例

### 管理员添加用户
```
添加用户 zhangsan 店长 正义路
```

### 用户首次登录
```
用户：你好
机器人：👋 欢迎使用红谷门店经营助手！
       ✅ 账户已激活
       姓名：张三
       角色：店长
```

---

## 🔧 技术规格

### 系统要求
- OpenClaw 2026.3.0+
- Python 3.8+
- 企业微信插件 2026.3.20+

### 依赖
- Python 3 (标准库)
- 企业微信通道
- wecom_mcp tool

### 文件大小
- 压缩包：2.9 KB
- 解压后：~15 KB

---

## 📋 安装说明

### 通过 ClawHub 安装
```bash
openclaw skill install wecom-user-manager
```

### 手动安装
```bash
# 下载发布包
wget https://clawhub.ai/skills/wecom-user-manager/download

# 解压
tar -xzf wecom-user-manager-1.0.0.tar.gz

# 复制到 skills 目录
cp -r wecom-user-manager ~/.openclaw/skills/

# 重启 Gateway
openclaw gateway restart
```

---

## ⚙️ 配置要求

### 1. 启用企业微信通道
```json
{
  "channels": {
    "wecom": {
      "enabled": true
    }
  }
}
```

### 2. 配置工具权限
```bash
openclaw config set tools.alsoAllow '["wecom_mcp"]'
```

### 3. 重启 Gateway
```bash
openclaw gateway restart
```

---

## 🧪 测试报告

### 测试环境
- OpenClaw: 2026.3.24
- Python: 3.x
- 企业微信插件：2026.3.26

### 测试结果
| 测试项 | 状态 |
|--------|------|
| 添加用户 | ✅ 通过 |
| 权限检查 | ✅ 通过 |
| 自动激活 | ✅ 通过 |
| 欢迎消息 | ✅ 通过 |
| 配置文件同步 | ✅ 通过 |

### 测试用户
- 用户 ID: 18688790604
- 姓名：杨广伟
- 角色：总部管理员
- 状态：✅ 已激活

---

## 📊 版本历史

### v1.0.0 (2026-03-28)
**初始版本**
- ✅ 合并 wecom-add-user 和 wecom-auto-activate
- ✅ 完整的用户生命周期管理
- ✅ 自动激活功能
- ✅ 权限检查
- ✅ 欢迎消息
- ✅ 配置文件同步

---

## 🎯 适用场景

### 适合
- ✅ 企业微信用户管理
- ✅ 权限配置和激活
- ✅ 多门店权限控制
- ✅ 自动化用户激活

### 不适合
- ❌ 非企业微信环境
- ❌ 需要复杂审批流程
- ❌ 需要第三方身份验证

---

## 📝 更新日志

#### 新增
- 添加用户权限功能
- 自动激活功能
- 欢迎消息功能
- 权限检查功能

#### 优化
- 合并两个独立 Skill
- 统一配置文件管理
- 优化用户体验

#### 修复
- 无（初始版本）

---

## 🤝 贡献指南

### 报告问题
https://github.com/xunrong-tech/wecom-openclaw-plugin/issues

### 提交代码
https://github.com/xunrong-tech/wecom-openclaw-plugin/pulls

### 联系作者
- 邮箱：guangwei.yang@xtechmerge.com
- 公司：巽融科技

---

## 📄 许可证

MIT License

Copyright (c) 2026 巽融科技

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

## 🔗 相关链接

- **ClawHub**: https://clawhub.ai/skills/wecom-user-manager
- **GitHub**: https://github.com/xunrong-tech/wecom-openclaw-plugin
- **文档**: https://github.com/xunrong-tech/wecom-openclaw-plugin/tree/main/skills/wecom-user-manager
- **问题反馈**: https://github.com/xunrong-tech/wecom-openclaw-plugin/issues

---

## 📞 技术支持

如有问题，请通过以下方式联系：

1. **GitHub Issues** (推荐)
   https://github.com/xunrong-tech/wecom-openclaw-plugin/issues

2. **邮箱**
   guangwei.yang@xtechmerge.com

3. **Discord 社区**
   https://discord.com/invite/clawd

---

## 🎊 致谢

感谢以下项目和团队：

- OpenClaw 团队
- 企业微信开发团队
- 红谷集团业务团队
- 巽融科技开发团队

---

**发布完成！感谢使用！** 🎉

**最后更新**: 2026-03-28  
**版本**: 1.0.0  
**状态**: ✅ 已发布

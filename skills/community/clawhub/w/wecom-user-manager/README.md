# wecom-user-manager - 企业微信用户管理技能

👤 完整的企业微信用户生命周期管理解决方案

---

## 🎯 功能概述

**wecom-user-manager** 是一个完整的企业微信用户管理 Skill，提供：

- ✅ **添加用户权限** - 支持自然语言命令
- ✅ **自动激活** - 用户首次登录自动完成
- ✅ **权限管理** - 严格的权限控制
- ✅ **欢迎消息** - 个性化的用户体验

---

## 📱 使用场景

### 场景 1：管理员添加店长

```
管理员：添加用户 zhangsan 店长 正义路

→ 发送确认卡片
→ 管理员确认
→ 用户创建成功

zhangsan 首次登录：
→ 自动激活
→ "欢迎使用，张三！"
```

### 场景 2：添加省份经理

```
管理员：添加用户 liming 省份经理 云南

→ 发送确认卡片（不需要门店）
→ 管理员确认
→ 用户创建成功（可访问云南省所有门店）
```

### 场景 3：用户首次登录

```
用户：你好

→ 检测到"待激活_xxx"
→ 自动激活（更新为真实姓名）
→ 发送欢迎消息
→ 记录登录时间
```

---

## 🚀 快速开始

### 安装

通过 ClawHub 安装：
```bash
openclaw skill install wecom-user-manager
```

或手动安装：
```bash
git clone https://github.com/xunrong-tech/wecom-openclaw-plugin.git
cp -r wecom-openclaw-plugin/skills/wecom-user-manager ~/.openclaw/skills/
```

### 配置

1. 确保企业微信插件已启用
2. 配置 `tools.alsoAllow` 包含 `wecom_mcp`
3. 重启 Gateway

```bash
openclaw config set tools.alsoAllow '["wecom_mcp"]'
openclaw gateway restart
```

---

## 📋 命令格式

### 添加用户

```
添加用户 <UserID> <角色> <门店/地区>
```

### 支持的角色

| 角色 | 权限范围 | 功能权限 |
|------|---------|---------|
| 总部管理员 | 358 家门店 | 管理 |
| 区域经理 | 大区内所有店 | 分析 |
| 省份经理 | 省内所有店 | 分析 |
| 城市经理 | 市内所有店 | 导出 |
| 店长 | 单店管理 | 分析 |
| 店员 | 单店只读 | 查看 |

### 示例

```bash
# 添加店长
添加用户 zhangsan 店长 正义路

# 添加店员
添加用户 liming 店员 正义路

# 添加省份经理
添加用户 wangwu 省份经理 云南

# 添加区域经理
添加用户 zhaoliu 区域经理 西南区
```

---

## 🔧 技术细节

### 文件结构

```
wecom-user-manager/
├── SKILL.md                  # 技能文档
├── handler.py                # 消息处理器
├── auto_activate.py          # 自动激活脚本
├── references/
│   └── api-user-manager.md   # API 文档
├── README.md                 # 本文件
└── .clawhub/
    ├── origin.json           # ClawHub 配置
    └── manifest.json         # 发布清单
```

### 用户状态流转

```
添加用户 → 待激活_xxx → (首次登录) → 真实姓名 → (后续登录) → 更新 last_login
```

### 配置文件

- `config/users.json` - 用户权限配置
- 工作区和插件目录需要保持同步

---

## ⚠️ 注意事项

### 1. UserID 格式
- 必须是企业微信中的真实 UserID
- 可以在企业微信管理后台查看
- 格式如：`zhangsan`、`liming001`、`10001`

### 2. 姓名获取
- 添加时无需提供姓名
- 首次登录时自动从企业微信获取
- 确保 UserID 与企业微信一致

### 3. 权限控制
- 只有总部/区域/省份经理可以添加用户
- 店长和店员没有添加权限

### 4. 配置文件同步
```bash
# 工作区 → 插件
cp workspace/config/users.json plugin/config/users.json

# 插件 → 工作区（激活后）
cp plugin/config/users.json workspace/config/users.json
```

---

## 🧪 测试

### 测试添加用户

```bash
cd skills/wecom-user-manager
python3 handler.py handle_message "添加用户 zhangsan 店长 正义路" "hq_admin_001"
```

### 测试自动激活

```bash
python3 auto_activate.py check_and_activate "zhangsan" "张三"
```

### 测试完整流程

```bash
# 1. 添加用户
python3 handler.py handle_message "添加用户 test001 店长 正义路" "hq_admin_001"

# 2. 激活用户
python3 auto_activate.py check_and_activate "test001" "测试用户"

# 3. 验证
cat config/users.json | grep "test001"
```

---

## 📊 版本历史

### v1.0.0 (2026-03-28)
- ✅ 初始版本
- ✅ 合并 wecom-add-user 和 wecom-auto-activate
- ✅ 完整的用户生命周期管理
- ✅ 自动激活功能
- ✅ 权限检查

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- GitHub: https://github.com/xunrong-tech/wecom-openclaw-plugin
- Issues: https://github.com/xunrong-tech/wecom-openclaw-plugin/issues

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 👤 作者

**杨广伟**
- 公司：巽融科技
- 邮箱：guangwei.yang@xtechmerge.com
- 项目：红谷集团门店经营智能体系统

---

## 🔗 相关链接

- [ClawHub](https://clawhub.ai)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [企业微信开发文档](https://developer.work.weixin.qq.com)

---

**最后更新**: 2026-03-28  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪

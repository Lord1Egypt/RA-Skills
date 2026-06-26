# xhs-skill-pusher 🚀

小红书内容发布技能 - 规范化cookie管理 + xhs-kit自动化发布

## 🎯 特性

### ✅ 规范化Cookie管理
- **集中存储**: 所有cookie保存在 `xhs_cookies/` 目录
- **规范命名**: `账号标识_描述_日期.json` 格式
- **自动转换**: 支持原始cookie字符串和JSON格式自动转换
- **状态管理**: `active.json` 软链接指向当前激活cookie

### ✅ 自动化发布流程
- **完整验证**: 状态检查 → debug验证 → 实际发布
- **错误处理**: 清晰的错误提示和恢复建议
- **多账号支持**: 一键切换不同账号
- **定时发布**: 支持定时发布功能

### ✅ 简单易用
- **无环境变量**: 完全基于文件路径，避免环境变量混乱
- **统一接口**: 一个 `--cookie` 参数解决所有问题
- **透明操作**: 基于实际文件，没有隐藏映射

## 🚀 快速开始

### 安装
```bash
# 克隆项目
git clone https://github.com/beizhi-tech/xhs-skill-pusher.git
cd xhs-skill-pusher

# 安装Node.js依赖
npm install

# 安装Python依赖
python3 -m venv xhs-env
source xhs-env/bin/activate
pip install xhs-kit
playwright install chromium
```

### 基本使用
```bash
# 1. 保存新cookie
./scripts/xhs_save_cookie.sh --name new_main --cookie "a1=xxx;webId=yyy;..." --set-active

# 2. 查看所有cookie
./scripts/xhs_final.sh --list-cookies

# 3. 发布内容
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "标题" --content "内容" --image 图片.jpg
```

### Node.js CLI
```bash
# 查看帮助
node ./bin/xhs-pusher.mjs --help

# 管理cookie
node ./bin/xhs-pusher.mjs cookie list
node ./bin/xhs-pusher.mjs cookie save --name test --cookie "a1=xxx;..."

# 发布内容
node ./bin/xhs-pusher.mjs publish post --title "..." --content "..." --image ...
```

## 📁 项目结构

```
xhs-skill-pusher/
├── bin/
│   └── xhs-pusher.mjs         # Node.js CLI工具
├── scripts/                   # 发布脚本
│   ├── xhs_save_cookie.sh     # 保存cookie脚本
│   ├── xhs_final.sh           # 主发布脚本
│   ├── xhs_manage.sh          # cookie管理脚本
│   └── xhs_simple.sh          # 简单发布脚本
├── xhs_cookies/               # Cookie目录（自动创建）
│   ├── active.json           # 当前激活cookie（软链接）
│   └── archive/              # 归档目录
├── docs/                      # 文档
│   ├── XHS_FINAL_SOLUTION.md  # 完整解决方案
│   └── QUICK_START.md         # 快速开始指南
├── package.json              # Node.js依赖
└── SKILL.md                  # OpenClaw技能文档
```

## 🔧 核心脚本

### 1. `xhs_save_cookie.sh` - 保存Cookie
规范化保存cookie，支持自动格式转换。

### 2. `xhs_final.sh` - 主发布脚本
完整的发布流程：状态检查 → debug验证 → 实际发布。

### 3. `xhs_manage.sh` - Cookie管理
管理cookie文件：列表、信息、切换、清理。

### 4. `xhs-pusher.mjs` - Node.js CLI
统一CLI接口，提供更好的用户体验。

## 📋 Cookie命名规范

### 格式
```
账号标识_描述_日期.json
```

### 示例
- `new_main_20260314.json` - 新主账号，2026-03-14获取
- `old_backup_today.json` - 旧备份账号，今天获取
- `test_temp.json` - 测试临时账号

## 🎯 工作流程

### 获取新Cookie
```bash
./scripts/xhs_save_cookie.sh --name new_main --cookie "a1=xxx;webId=yyy;..." --set-active
```

### 日常发布
```bash
./scripts/xhs_final.sh \
  --cookie xhs_cookies/active.json \
  --title "每日更新" \
  --content "今日内容..." \
  --image daily_photo.jpg \
  --tag 日常 \
  --tag 分享
```

### 多账号管理
```bash
# 切换到旧账号
./scripts/xhs_manage.sh use old_backup

# 使用切换后的账号发布
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "..." --image ...
```

## 🔍 故障排除

### 常见问题
1. **Cookie过期** - 重新获取并保存
2. **图片不存在** - 检查图片路径和权限
3. **发布失败** - 先debug验证，检查登录状态

### 错误代码
- `ERR_COOKIE_NOT_FOUND` - Cookie文件不存在
- `ERR_LOGIN_FAILED` - 登录状态异常
- `ERR_DEBUG_VALIDATION` - debug验证失败
- `ERR_PUBLISH_FAILED` - 发布失败

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

- 文档: [docs/](docs/)
- Issue: [GitHub Issues](https://github.com/beizhi-tech/xhs-skill-pusher/issues)

---

**开始发布小红书内容吧！** 🚀
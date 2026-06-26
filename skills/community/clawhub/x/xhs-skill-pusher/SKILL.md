---
name: xhs-skill-pusher
description: 小红书内容发布技能 - 规范化cookie管理 + xhs-kit自动化发布
metadata: {"openclaw":{"emoji":"🚀","stage":"production"}}
---

# xhs-skill-pusher

基于xhs-kit的小红书内容发布技能，提供**规范化cookie管理**和**自动化发布流程**。

## 🎯 核心特性

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

## 📦 安装

### 1. 安装技能
```bash
clawhub install xhs-skill-pusher
cd skills/xhs-skill-pusher
npm install
```

### 2. 安装Python依赖
```bash
# 创建虚拟环境
python3 -m venv xhs-env
source xhs-env/bin/activate

# 安装xhs-kit
pip install xhs-kit

# 安装Playwright浏览器
playwright install chromium

# 安装其他依赖
pip install pillow requests markdown pyyaml
```

### 3. 初始化Cookie目录
```bash
mkdir -p xhs_cookies/archive
```

## 🚀 快速开始

### 1. 保存新Cookie
```bash
# 获取cookie字符串后，规范化保存
./xhs_save_cookie.sh --name new_main --cookie "a1=xxx;webId=yyy;..." --set-active
```

### 2. 查看所有Cookie
```bash
./xhs_final.sh --list-cookies
```

### 3. 发布内容
```bash
./xhs_final.sh --cookie xhs_cookies/active.json --title "标题" --content "内容" --image 图片.jpg
```

## 📁 项目结构

```
xhs-skill-pusher/
├── SKILL.md                    # 本文档
├── package.json               # Node.js依赖
├── bin/
│   └── xhs-pusher.mjs         # CLI工具
├── scripts/                   # 发布脚本
│   ├── xhs_save_cookie.sh     # 保存cookie脚本
│   ├── xhs_final.sh           # 主发布脚本
│   ├── xhs_manage.sh          # cookie管理脚本
│   └── xhs_simple.sh          # 简单发布脚本
├── xhs_cookies/               # Cookie目录（自动创建）
│   ├── active.json           # 当前激活cookie（软链接）
│   ├── new_main_20260314.json # 示例cookie文件
│   └── archive/              # 归档目录
└── docs/                      # 文档
    ├── XHS_FINAL_SOLUTION.md  # 完整解决方案
    └── QUICK_START.md         # 快速开始指南
```

## 🔧 脚本说明

### 核心脚本

#### 1. `xhs_save_cookie.sh` - 保存Cookie
```bash
# 保存并设置为激活
./scripts/xhs_save_cookie.sh --name new_main --cookie "a1=xxx;..." --set-active

# 从文件保存
./scripts/xhs_save_cookie.sh --name old_backup --file raw_cookie.txt
```

#### 2. `xhs_final.sh` - 主发布脚本
```bash
# 基本发布
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "..." --image ...

# 查看cookie列表
./scripts/xhs_final.sh --list-cookies

# 检查状态
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --check-status
```

#### 3. `xhs_manage.sh` - Cookie管理
```bash
# 查看所有cookie
./scripts/xhs_manage.sh list

# 查看cookie信息
./scripts/xhs_manage.sh info new_main_20260314

# 切换到指定cookie
./scripts/xhs_manage.sh use new_main

# 查看状态
./scripts/xhs_manage.sh status

# 清理过期cookie
./scripts/xhs_manage.sh clean --keep-days 7
```

### Node.js CLI工具

#### `xhs-pusher` - 统一CLI接口
```bash
# 查看帮助
node ./bin/xhs-pusher.mjs --help

# 管理cookie
node ./bin/xhs-pusher.mjs cookie list
node ./bin/xhs-pusher.mjs cookie save --name test --cookie "a1=xxx;..."

# 发布内容
node ./bin/xhs-pusher.mjs publish --title "..." --content "..." --image ...
```

## 📋 Cookie命名规范

### 格式
```
账号标识_描述_日期.json
```

### 字段说明
- **账号标识**: `new`(新账号), `old`(旧账号), `test`(测试), `backup`(备份)
- **描述**: `main`(主账号), `backup`(备份), `temp`(临时)
- **日期**: `20260314`(年月日), `today`(今天), `yesterday`(昨天)

### 示例
```
new_main_20260314.json      # 新主账号，2026-03-14获取
old_backup_today.json       # 旧备份账号，今天获取
test_temp.json              # 测试临时账号
```

## 🎯 工作流程

### 获取新Cookie后
```bash
# 1. 规范化保存
./scripts/xhs_save_cookie.sh --name new_main --cookie "a1=xxx;webId=yyy;..." --set-active

# 2. 自动成为激活cookie，可以直接使用
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "测试" --image test.jpg
```

### 日常发布
```bash
# 使用当前激活cookie发布
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
# 1. 查看可用cookie
./scripts/xhs_final.sh --list-cookies

# 2. 切换到指定cookie
./scripts/xhs_manage.sh use old_backup

# 3. 使用切换后的cookie发布
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "..." --image ...
```

## 🔧 高级功能

### 定时发布
```bash
./scripts/xhs_final.sh \
  --cookie xhs_cookies/active.json \
  --title "定时发布" \
  --content "内容" \
  --image photo.jpg \
  --schedule "2026-03-14T14:00:00+08:00"
```

### 显示浏览器窗口
```bash
./scripts/xhs_final.sh \
  --cookie xhs_cookies/active.json \
  --title "测试" \
  --content "内容" \
  --image photo.jpg \
  --show-browser
```

### 仅验证不发布
```bash
./scripts/xhs_final.sh \
  --cookie xhs_cookies/active.json \
  --title "测试" \
  --content "内容" \
  --image photo.jpg \
  --debug-only
```

## 🛠️ 维护命令

### 初始化
```bash
# 创建cookie目录结构
mkdir -p xhs_cookies/archive
```

### 导入现有Cookie
```bash
# 导入工作空间的cookie文件
cp /path/to/cookies.json xhs_cookies/new_main_$(date +%Y%m%d).json

# 设置为激活
ln -sf new_main_$(date +%Y%m%d).json xhs_cookies/active.json
```

### 备份和恢复
```bash
# 备份所有cookie
tar -czf xhs_cookies_backup_$(date +%Y%m%d).tar.gz xhs_cookies/

# 恢复备份
tar -xzf xhs_cookies_backup_20260314.tar.gz
```

## ⚠️ 注意事项

1. **定期检查**: cookie会过期，建议每周检查状态
2. **重要备份**: 重要cookie定期备份到安全位置
3. **命名规范**: 遵循命名规范，便于管理
4. **权限安全**: cookie包含敏感信息，注意文件权限
5. **图片要求**: 建议使用1242x1660像素的图片

## 🔍 故障排除

### 常见问题

1. **Cookie过期**
   ```bash
   # 重新获取cookie并保存
   ./scripts/xhs_save_cookie.sh --name new_main --cookie "新cookie字符串" --set-active
   ```

2. **图片不存在**
   ```bash
   # 检查图片路径
   file image.jpg
   ls -lh image.jpg
   ```

3. **发布失败**
   ```bash
   # 先debug验证
   ./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "测试" --image ... --debug-only
   
   # 检查登录状态
   ./scripts/xhs_final.sh --cookie xhs_cookies/active.json --check-status
   ```

### 错误代码
- `ERR_COOKIE_NOT_FOUND`: Cookie文件不存在
- `ERR_LOGIN_FAILED`: 登录状态异常
- `ERR_DEBUG_VALIDATION`: debug验证失败
- `ERR_PUBLISH_FAILED`: 发布失败

## 📞 支持

### 快速参考
```bash
# 查看帮助
./scripts/xhs_final.sh --help

# 检查所有cookie
./scripts/xhs_final.sh --list-cookies

# 测试cookie有效性
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --check-status

# 测试发布流程
./scripts/xhs_final.sh --cookie xhs_cookies/active.json --title "测试" --content "测试" --image test.jpg --debug-only
```

### 更新日志
- **v1.0.0**: 初始版本，规范化cookie管理 + xhs-kit自动化发布
- **功能**: 直接指定cookie、自动格式转换、多账号管理、完整发布流程

## 🎉 总结

**xhs-skill-pusher** 提供了完整的小红书内容发布解决方案：

1. ✅ **规范化Cookie管理** - 集中存储，规范命名
2. ✅ **自动化发布流程** - 完整验证，错误处理
3. ✅ **简单易用** - 无环境变量，统一接口
4. ✅ **多账号支持** - 一键切换，透明管理

**开始发布吧！** 🚀
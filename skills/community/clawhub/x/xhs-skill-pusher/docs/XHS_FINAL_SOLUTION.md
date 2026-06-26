# 🎯 xhs-kit 最终解决方案

## 📖 老板的需求理解

### 核心需求
1. **Cookie规范化管理**：所有cookie保存为JSON文件
2. **集中存储**：放到固定文件夹 `xhs_cookies/`
3. **规范命名**：文件名有明确区分
4. **简单使用**：`--list-cookies` 查看，`--cookie xxx.json` 使用

### 解决方案设计
```
获取cookie → 保存为规范JSON → 集中管理 → 直接使用
```

## 📁 文件夹结构

```
xhs_cookies/                    # 所有cookie集中在这里
├── active.json                # 当前激活的cookie（软链接）
├── new_main_20260314.json     # 新主账号，2026-03-14获取
├── old_backup_20260313.json   # 旧备份账号
├── test_temp.json             # 测试账号
└── archive/                   # 归档目录
    └── old_20260301.json      # 过期cookie
```

## 🚀 快速使用

### 1. 保存新cookie
```bash
# 获取cookie字符串后，规范化保存
./xhs_save_cookie.sh --name new_main --cookie "a1=xxx;webId=yyy;..." --set-active
```

### 2. 查看所有cookie
```bash
./xhs_final.sh --list-cookies
```
输出：
```
📁 Cookie文件列表 (xhs_cookies/):
========================================
  📌 new_main_20260314.json (2850字节) - 5fc1e8dd00000000010041c7 ← 当前激活
      修改时间: Mar 14 12:30:00 2026
  
  📄 old_backup_20260313.json (2835字节) - 6256338d0000000010006ab7
      修改时间: Mar 13 18:21:32 2026
```

### 3. 使用cookie发布
```bash
# 使用当前激活的cookie
./xhs_final.sh --cookie xhs_cookies/active.json --title "标题" --content "内容" --image 图片.jpg

# 使用指定cookie文件
./xhs_final.sh --cookie xhs_cookies/new_main_20260314.json --title "..." --image ...

# 使用旧账号
./xhs_final.sh --cookie xhs_cookies/old_backup_20260313.json --title "..." --image ...
```

## 📋 文件命名规范

### 格式
```
账号标识_描述_日期.json
```

### 字段说明
- **账号标识**：`new`(新账号), `old`(旧账号), `test`(测试), `backup`(备份)
- **描述**：`main`(主账号), `backup`(备份), `temp`(临时)
- **日期**：`20260314`(年月日), `today`(今天), `yesterday`(昨天)

### 示例
```
new_main_20260314.json      # 新主账号，2026-03-14获取
old_backup_today.json       # 旧备份账号，今天获取  
test_temp.json              # 测试临时账号
backup_20260313.json        # 备份账号
```

## 🔧 脚本说明

### 核心脚本
1. **`xhs_save_cookie.sh`** - 保存cookie
   ```bash
   # 保存并设置为激活
   ./xhs_save_cookie.sh --name new_main --cookie "a1=xxx;..." --set-active
   
   # 从文件保存
   ./xhs_save_cookie.sh --name old_backup --file raw_cookie.txt
   ```

2. **`xhs_final.sh`** - 发布内容
   ```bash
   # 基本发布
   ./xhs_final.sh --cookie xhs_cookies/active.json --title "..." --image ...
   
   # 查看cookie列表
   ./xhs_final.sh --list-cookies
   
   # 检查状态
   ./xhs_final.sh --cookie xhs_cookies/active.json --check-status
   ```

3. **`xhs_manage.sh`** - 管理cookie
   ```bash
   # 查看所有cookie
   ./xhs_manage.sh list
   
   # 查看cookie信息
   ./xhs_manage.sh info new_main_20260314
   
   # 切换到指定cookie
   ./xhs_manage.sh use new_main
   
   # 查看状态
   ./xhs_manage.sh status
   
   # 清理过期cookie（保留7天）
   ./xhs_manage.sh clean --keep-days 7
   ```

## 🎯 工作流程

### 获取新cookie后
```bash
# 1. 规范化保存
./xhs_save_cookie.sh --name new_main --cookie "a1=xxx;webId=yyy;..." --set-active

# 2. 自动成为激活cookie，可以直接使用
./xhs_final.sh --cookie xhs_cookies/active.json --title "测试" --image test.jpg
```

### 切换账号
```bash
# 1. 查看可用cookie
./xhs_final.sh --list-cookies

# 2. 使用指定cookie
./xhs_final.sh --cookie xhs_cookies/old_backup_20260313.json --title "..." --image ...

# 或使用管理脚本切换
./xhs_manage.sh use old_backup
```

### 日常发布
```bash
# 使用当前激活cookie发布
./xhs_final.sh \
  --cookie xhs_cookies/active.json \
  --title "每日更新" \
  --content "今日内容..." \
  --image daily_photo.jpg \
  --tag 日常 \
  --tag 分享
```

## 📊 当前状态

### 激活cookie
- **文件**: `xhs_cookies/active.json` → `new_main_20260314.json`
- **用户ID**: `5fc1e8dd00000000010041c7`
- **状态**: ✅ 有效（已测试发布成功）

### 可用cookie
1. **新主账号** (`new_main_20260314.json`)
   - 用户ID: `5fc1e8dd00000000010041c7`
   - 来源: 手动发布后获取
   - 状态: ✅ 激活中

2. **旧备份账号** (`old_backup_20260313.json`)
   - 用户ID: `6256338d0000000010006ab7`
   - 来源: 之前测试使用
   - 状态: ✅ 有效

## 🛠️ 维护命令

### 初始化
```bash
# 创建cookie目录结构
mkdir -p xhs_cookies/archive
```

### 导入现有cookie
```bash
# 导入工作空间的cookie文件
cp cookies_new_account.json xhs_cookies/new_main_$(date +%Y%m%d).json
cp cookies_old_account.json xhs_cookies/old_backup_$(date +%Y%m%d).json

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

1. **定期检查**：cookie会过期，建议每周检查状态
2. **重要备份**：重要cookie定期备份到安全位置
3. **命名规范**：遵循命名规范，便于管理
4. **权限安全**：cookie包含敏感信息，注意文件权限

## 🎉 总结

### 解决了什么问题？
1. ✅ **规范化管理**：所有cookie统一格式、统一位置
2. ✅ **简单使用**：`--list-cookies`查看，`--cookie`使用
3. ✅ **无环境变量**：完全基于文件路径，没有环境变量混乱
4. ✅ **透明操作**：基于实际文件，没有隐藏映射

### 核心命令
```bash
# 保存cookie
./xhs_save_cookie.sh --name 账号名 --cookie "cookie字符串" --set-active

# 查看cookie
./xhs_final.sh --list-cookies

# 发布内容
./xhs_final.sh --cookie xhs_cookies/active.json --title "标题" --content "内容" --image 图片.jpg
```

### 设计优势
1. **一致性**：只使用文件路径，没有混乱的账号名映射
2. **简单性**：用户只需关心cookie文件
3. **透明性**：所有操作基于实际文件
4. **可维护性**：规范化存储，易于管理

**老板，这个方案完全符合您的需求：规范化、集中管理、简单使用！** 🚀
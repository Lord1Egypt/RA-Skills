---
name: svn-tool
version: 1.0.0
description: Subversion (SVN) 代码版本控制工具。使用 svn CLI 进行检入、检出、更新、提交、查看日志等操作。当用户需要与 SVN 仓库交互时触发此技能。
user-invocable: true
---

# SVN Tool - Subversion 版本控制技能

## 概述

提供完整的 Subversion (SVN) 版本控制功能，包括：
- 仓库操作（checkout, update, commit）
- 状态查看（status, log, info）
- 分支管理（switch, copy, move）
- 差异比较（diff）
- 冲突解决

## 触发场景

1. 用户要求"提交代码到 SVN"
2. 用户需要"更新本地工作副本"
3. 用户想"查看 SVN 提交历史"
4. 用户询问"SVN 仓库状态"
5. 用户需要"检出新的 SVN 项目"
6. 用户要求"比较文件差异"

## 前置条件

使用前需确保：
- 已安装 `svn` CLI 工具（Subversion）
- 已配置 SVN 认证信息（可通过 `--username`/`--password` 或密钥环）
- 工作目录包含有效的 SVN 工作副本

检查 SVN 是否可用：
```bash
svn --version
```

## 核心功能

### 1. 仓库检出 (Checkout)

从 SVN 仓库检出代码到本地：

```bash
svn checkout <repository-url> [local-path]
svn co https://example.com/svn/project/trunk my-project
```

**常用选项：**
- `--depth empty/folders/immediates/infinity`：控制检出深度
- `--non-interactive`：非交互模式
- `--trust-server-cert`：信任服务器证书

### 2. 更新工作副本 (Update)

同步最新代码：

```bash
svn update
svn up
svn up --revision 1234  # 更新到特定版本
svn up --merge  # 自动合并冲突
```

### 3. 提交更改 (Commit)

将本地更改提交到仓库：

```bash
svn commit -m "提交消息"
svn ci -m "修复了登录页面的 bug"
svn ci --revprop -r HEAD -m "修改最后一条提交信息"
```

**提示：**
- 提交前建议先执行 `svn status` 查看变更
- 使用 `-F file.txt` 从文件读取提交信息
- 支持 `--with-revprop` 添加自定义属性

### 4. 查看状态 (Status)

检查工作副本的变更状态：

```bash
svn status
svn st
svn status --verbose  # 详细模式
svn status --show-updates  # 显示需要更新的文件
svn status --no-ignore  # 显示忽略的文件
```

**状态代码说明：**
- ` ` (空格)：未变更
- `M`：内容已修改
- `A`：已添加
- `D`：已删除
- `R`：已替换
- `C`：冲突
- `?`：未跟踪的文件

### 5. 查看日志 (Log)

查看提交历史：

```bash
svn log
svn log -r HEAD:1  # 反向显示
svn log -r 1000:1100  # 指定版本范围
svn log --limit 10  # 限制显示数量
svn log --verbose -r 1234  # 显示该版本的变更文件
svn log --search keyword  # 搜索提交信息
```

### 6. 添加文件 (Add)

将新文件添加到版本控制：

```bash
svn add filename.txt
svn add --force new-folder/  # 递归添加
svn add *.js  # 通配符添加
```

### 7. 删除文件 (Delete)

从版本控制中移除文件：

```bash
svn delete filename.txt
svn del folder/  # 删除文件夹
svn delete --keep-local filename.txt  # 保留本地文件
```

### 8. 复制/移动 (Copy/Move)

在仓库内复制或移动文件：

```bash
svn copy src/file.txt dest/file.txt -m "复制文件"
svn mv old-name.txt new-name.txt -m "重命名文件"
svn cp ^/trunk/feature ^/branches/feature-v2 -m "创建分支"
```

### 9. 差异比较 (Diff)

查看文件变更内容：

```bash
svn diff
svn diff filename.txt
svn diff -r 1000:1001  # 比较两个版本
svn diff --summarize  # 仅显示变更列表
svn diff -x -w  # 忽略空白字符
```

### 10. 解决冲突 (Resolve)

处理合并冲突：

```bash
svn resolve --accept working filename.txt  # 使用本地版本
svn resolve --accept theirs filename.txt   # 使用仓库版本
svn resolve --accept mine-full filename.txt  # 完整使用本地版本
svn resolve --accept theirs-full filename.txt  # 完整使用仓库版本
svn resolved filename.txt  # 标记冲突已解决
```

### 11. 切换分支 (Switch)

切换到不同的分支或标签：

```bash
svn switch ^/branches/feature-x
svn switch --relocate new-repo-url  # 重新定位仓库 URL
```

### 12. 信息显示 (Info)

查看工作副本或文件的详细信息：

```bash
svn info
svn info filename.txt
svn info --show-item revision  # 仅显示版本号
svn info --show-item url  # 仅显示 URL
```

### 13. 还原文件 (Revert)

撤销本地未提交的更改：

```bash
svn revert filename.txt
svn revert --recursive .  # 还原所有更改
svn revert -r HEAD filename.txt  # 还原到最新版本
```

### 14. 清理工作副本 (Cleanup)

修复工作副本锁或中断的操作：

```bash
svn cleanup
svn cleanup --remove-unversioned  # 同时删除未版本化文件
svn cleanup --remove-stuck  # 移除卡住的锁
```

## 最佳实践

### 提交前的检查清单

1. **查看状态**: `svn status`
2. **预览差异**: `svn diff`
3. **更新代码**: `svn update`
4. **解决冲突**: 如有冲突先解决
5. **编写清晰的提交信息**

### 分支策略示例

```bash
# 创建功能分支
svn copy ^/trunk ^/branches/feature-login -m "创建登录功能分支"

# 切换到分支
svn switch ^/branches/feature-login

# 开发完成后合并回主干
svn merge ^/branches/feature-login
svn commit -m "合并登录功能到主干"

# 删除分支
svn delete ^/branches/feature-login -m "删除已完成的功能分支"
```

### 忽略文件配置

在项目根目录创建 `.svnignore` 或在 `svn propedit svn:ignore` 中设置：

```
*.log
*.tmp
node_modules/
dist/
.DS_Store
*.swp
```

应用忽略规则：
```bash
svn propset svn:ignore -F .svnignore .
svn commit -m "设置忽略规则"
```

## 环境变量

- `SVN_AUTH_CACHE`：认证缓存路径
- `SVN_CONFIG_DIR`：配置文件目录
- `SVN_EDITOR`：默认编辑器

## 常见问题

### Q: 如何处理认证失败？
A: 使用 `--username` 和 `--password` 参数，或配置 `~/.subversion/auth/` 目录

### Q: 如何查看某个文件的修改历史？
A: `svn log -v filename.txt`

### Q: 如何恢复误删的文件？
A: 
```bash
svn list -v ^/path/to/file@PREV
svn copy ^/path/to/file@PREV ./filename.txt
svn add filename.txt
svn commit -m "恢复误删的文件"
```

### Q: 如何查看远程仓库的目录结构？
A: `svn list https://example.com/svn/project/`

## 注意事项

1. **网络依赖**：大多数操作需要网络连接
2. **锁定机制**：二进制文件可能需要显式锁定
3. **原子提交**：SVN 提交是原子的，要么全部成功要么全部失败
4. **版本全局唯一**：整个仓库共享一个版本号序列
5. **权限控制**：部分操作可能需要特定权限

## 相关技能

- `file-manager`：文件管理辅助

## 版本历史

- 1.0.0 (2026-04-13): 初始版本，支持基本 SVN 操作

# SVN Tool 使用示例

## 基本工作流程

### 1. 首次检出项目

```bash
# 从仓库检出项目
svn checkout https://svn.example.com/repos/my-project/trunk my-project
cd my-project
```

### 2. 日常开发循环

```bash
# 1. 更新到最新版本
svn update

# 2. 创建新文件或修改现有文件
# (在编辑器中完成)

# 3. 添加新文件到版本控制
svn add new-feature.py

# 4. 查看变更状态
svn status

# 5. 预览具体变更
svn diff

# 6. 提交更改
svn commit -m "添加了用户认证功能"
```

### 3. 查看历史

```bash
# 查看所有提交记录
svn log

# 查看最近 10 条记录
svn log --limit 10

# 查看特定文件的修改历史
svn log -v src/auth.py

# 查看某个版本的详细信息
svn info -r 1234
```

### 4. 分支操作

```bash
# 创建功能分支
svn copy ^/trunk ^/branches/login-feature -m "创建登录功能分支"

# 切换到分支
svn switch ^/branches/login-feature

# 在分支上开发...

# 合并回主干
svn switch ^/trunk
svn merge ^/branches/login-feature
svn commit -m "合并登录功能到主干"

# 删除已完成的分支
svn delete ^/branches/login-feature -m "删除已完成的功能分支"
```

### 5. 处理冲突

```bash
# 更新时可能发生冲突
svn update

# 查看冲突文件
svn status  # C 标记表示冲突

# 编辑文件解决冲突后，标记为已解决
svn resolved filename.txt

# 提交解决后的更改
svn commit -m "解决了合并冲突"
```

### 6. 撤销更改

```bash
# 撤销单个文件的未提交更改
svn revert filename.txt

# 撤销所有更改
svn revert --recursive .

# 还原到特定版本
svn update -r 1234
```

## 常见场景

### 场景 1: 修复紧急 Bug

```bash
# 1. 更新代码
svn update

# 2. 创建热修复分支
svn copy ^/trunk ^/branches/hotfix-login-bug -m "创建热修复分支"
svn switch ^/branches/hotfix-login-bug

# 3. 修复 bug 并提交
# (编辑文件)
svn commit -m "修复：登录页面空指针异常"

# 4. 合并到主干
svn switch ^/trunk
svn merge ^/branches/hotfix-login-bug
svn commit -m "合并热修复：登录页面空指针异常"

# 5. 删除热修复分支
svn delete ^/branches/hotfix-login-bug -m "删除热修复分支"
```

### 场景 2: 审查代码变更

```bash
# 查看某个提交的详细变更
svn diff -r 1233:1234

# 查看提交者信息
svn log -v --xml > history.xml

# 比较两个分支的差异
svn diff ^/trunk ^/branches/feature-x
```

### 场景 3: 管理忽略文件

```bash
# 设置忽略规则
echo "*.log" > .svnignore
echo "node_modules/" >> .svnignore
echo ".env.local" >> .svnignore

# 应用忽略规则
svn propset svn:ignore -F .svnignore .

# 提交忽略规则
svn commit -m "设置文件忽略规则"
```

## 提示与技巧

### 快捷命令别名

在 shell 配置中添加：
```bash
alias sv='svn status'
alias su='svn update'
alias sc='svn commit'
alias sl='svn log'
alias sd='svn diff'
alias sa='svn add'
alias srd='svn resolved'
```

### 批量操作

```bash
# 添加所有新文件
svn add --force . | grep "^?" | awk '{print $2}' | xargs svn add

# 查找所有未版本化的文件
svn status | grep "^?"

# 查找所有修改的文件
svn status | grep "^M"
```

### 安全操作

```bash
# 提交前总是先更新
svn update && svn commit -m "..."

# 使用非交互模式避免提示
svn commit --non-interactive -m "..."

# 信任服务器证书（首次连接时）
svn checkout --trust-server-cert https://svn.example.com/repo
```

## 故障排除

### 问题：工作副本锁定

```bash
svn cleanup
```

### 问题：认证失败

```bash
# 清除缓存的认证信息
rm -rf ~/.subversion/auth/*

# 重新认证
svn update
```

### 问题：URL 不匹配

```bash
# 重新定位仓库 URL
svn switch --relocate https://old-url.com/repo https://new-url.com/repo
```

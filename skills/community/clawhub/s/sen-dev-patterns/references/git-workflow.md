# Git工作流规范

本文档沉淀Git使用规范和备份策略。

---

## 1. Commit规范

### Commit信息格式

```
<type>: <subject>

<body>

<footer>
```

### Type类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | feat: 添加Excel导出功能 |
| `fix` | Bug修复 | fix: 修复日期解析错误 |
| `docs` | 文档更新 | docs: 更新README |
| `style` | 代码格式 | style: 格式化代码 |
| `refactor` | 重构 | refactor: 简化文件操作 |
| `perf` | 性能优化 | perf: 优化大数据读取 |
| `test` | 测试 | test: 添加单元测试 |
| `chore` | 构建/工具 | chore: 更新依赖 |

### 示例

```bash
# ✅ 正确示例
git commit -m "feat: 添加同比计算函数

- 新增calc_yoy函数计算同比增长率
- 支持格式化输出（带箭头）
- 添加单元测试"

git commit -m "fix: 修复Excel读取空值问题

当单元格为空时返回0.0而非报错"

# ❌ 错误示例
git commit -m "更新"
git commit -m "fix bug"
git commit -m "修改了代码"
```

---

## 2. 分支管理

### 分支命名

```
<type>/<feature-name>

# 示例
feature/user-auth
feature/report-export
bugfix/date-parse
hotfix/critical-error
```

### 分支策略

```
main (稳定分支)
├── develop (开发分支)
│   ├── feature/report-export
│   └── feature/user-auth
└── hotfix/critical-error
```

### 操作流程

```bash
# 1. 从develop创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. 开发并提交
git add .
git commit -m "feat: 新功能描述"

# 3. 推送分支
git push origin feature/new-feature

# 4. 合并回develop
git checkout develop
git merge feature/new-feature
git push origin develop

# 5. 删除功能分支
git branch -d feature/new-feature
```

---

## 3. 代码备份策略

### 自动备份时机

| 时机 | 触发条件 | 备份内容 |
|------|----------|----------|
| 每日自动 | 定时任务 | 全部代码 |
| 重大修改前 | 手动触发 | 完整项目 |
| 版本发布前 | 里程碑节点 | 完整项目 |
| 异常崩溃前 | 异常捕获 | 当前文件 |

### 备份目录结构

```
项目根目录/
├── backup/                          # 备份目录
│   ├── 2026-04-24_103000/          # 时间戳命名
│   │   ├── full/                   # 完整备份
│   │   └── incremental/            # 增量备份
│   └── 2026-04-23_093000/
│       └── full/
└── dist/                           # 打包输出
```

### Python备份脚本

```python
import os
import shutil
from datetime import datetime

def backup_project(project_dir, backup_dir):
    """
    备份项目文件
    
    Args:
        project_dir: 项目根目录
        backup_dir: 备份目标目录
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, timestamp)
    
    # 创建备份目录
    os.makedirs(backup_path, exist_ok=True)
    
    # 需要备份的目录/文件
    backup_items = [
        'main.py',
        'main_window.py',
        'data_processor.py',
        'logger.py',
        'config_manager.py',
        'constants.py',
        'config.json',
        '项目规范.md',
    ]
    
    # 复制文件
    for item in backup_items:
        src = os.path.join(project_dir, item)
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(backup_path, item))
            else:
                shutil.copy2(src, backup_path)
    
    print(f"备份完成: {backup_path}")
    return backup_path

# 排除的文件
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.git',
    'backup',
    'dist',
    'build',
    '*.pyc',
    '*.log',
    'venv',
    'env',
]
```

---

## 4. 版本发布流程

### 版本号规则

```
major.minor.patch

示例：
v1.0.0  - 初始版本
v1.1.0  - 添加新功能
v1.1.1  - 修复Bug
v2.0.0  - 重大更新
```

### 发布检查清单

- [ ] 所有功能测试通过
- [ ] 代码格式检查通过
- [ ] 文档已更新
- [ ] 生成版本号
- [ ] 创建发布标签
- [ ] 打包文件
- [ ] 上传发布包

### 发布命令

```bash
# 1. 更新版本号
echo "v1.2.0" > VERSION

# 2. 添加发布标签
git tag -a v1.2.0 -m "发布 v1.2.0"
git push origin v1.2.0

# 3. 打包发布
pyinstaller main.spec
cd dist
zip -r "app-v1.2.0.zip" .
```

---

## 5. 常用Git命令速查

```bash
# 初始化
git init                                    # 初始化仓库
git clone <url>                            # 克隆仓库

# 基本操作
git status                                 # 查看状态
git add <file>                             # 添加文件
git commit -m "message"                    # 提交
git push origin <branch>                   # 推送

# 分支操作
git branch                                 # 查看分支
git checkout <branch>                      # 切换分支
git checkout -b <new-branch>               # 创建并切换
git merge <branch>                         # 合并分支
git branch -d <branch>                     # 删除分支

# 历史与差异
git log                                    # 查看提交历史
git log --oneline                          # 简洁历史
git diff                                   # 查看未提交差异
git diff --staged                          # 查看暂存区差异

# 撤销操作
git checkout -- <file>                     # 撤销工作区修改
git reset HEAD <file>                      # 取消暂存
git reset --soft HEAD~1                    # 撤销上次提交

# 远程操作
git fetch                                  # 拉取远程分支
git pull                                   # 拉取并合并
git push                                   # 推送
git pull origin <branch> --rebase          # Rebase方式拉取
```

---

## 6. 冲突解决

### 解决步骤

```bash
# 1. 确保工作区干净
git status

# 2. 切换到目标分支
git checkout develop

# 3. 拉取最新代码
git pull origin develop

# 4. 合并功能分支
git merge feature/xxx

# 5. 如果有冲突，手动解决
# 编辑冲突文件，保留需要的代码

# 6. 标记冲突已解决
git add <resolved-file>

# 7. 完成合并
git commit
```

### 冲突标记

```python
<<<<<<< HEAD
# 当前分支代码
print("Hello")
=======
# 合并分支代码
print("World")
>>>>>>> feature/xxx

# 解决后
print("Hello World")
```

---

## 7. 忽略文件配置

### .gitignore模板

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 备份
backup/
*.bak
*_backup/

# 日志
*.log

# Excel临时文件
~$*.xlsx
*.tmp

# 系统
.DS_Store
Thumbs.db

# 打包输出
dist/
build/
*.spec
```

---

## 8. PyInstaller打包

### spec文件配置

```python
# main.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='应用名称',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 改为False隐藏控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico'  # 应用图标
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='应用名称',
)
```

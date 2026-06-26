# SVN Tool 配置

此目录用于存放 SVN 相关的配置文件和脚本。

## 可选配置项

### 1. 全局忽略文件 (.global-ignore)

可以在此创建全局忽略文件，包含所有项目都应忽略的文件类型：

```
*.log
*.tmp
*.swp
*.swo
.DS_Store
Thumbs.db
node_modules/
dist/
build/
*.class
*.o
*.pyc
__pycache__/
.env
.env.local
```

### 2. 提交模板 (commit-template.txt)

标准的提交信息模板：

```
[简短描述]

[详细描述]

关联任务: #123
影响版本: v1.0.0
测试说明: 
```

### 3. 钩子脚本 (hooks/)

如果需要自定义 SVN 钩子行为，可在此放置脚本。

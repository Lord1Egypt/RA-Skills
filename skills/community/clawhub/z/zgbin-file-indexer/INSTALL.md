# File Indexer 安装指南

## 快速安装

### 1. 克隆技能目录
```bash
mkdir -p ~/.openclaw/skills/file-indexer
cp -r ~/.openclaw/workspace/skills/file-indexer-publish/* ~/.openclaw/skills/file-indexer/
```

### 2. 初始化文件索引
```bash
# 进入工作空间
cd /home/t/cc_workspace
mkdir -p file_indexer
cd file_indexer

# 复制核心文件
cp ~/.openclaw/skills/file-indexer/*.py .

# 创建数据库
python3 __main__.py stats
```

### 3. 重启 OpenClaw
```bash
openclaw gateway restart
```

### 4. 测试技能
```bash
# 测试搜索功能
python3 __main__.py search "加密"

# 测试意图推荐
python3 __main__.py intent "文件加密"
```

## 验证安装

运行以下命令验证安装是否成功：
```bash
# 检查技能是否加载
openclaw skills list | grep file-indexer

# 测试文件索引功能
python3 /home/t/cc_workspace/file_indexer/__main__.py stats
```

## 常见问题

### Q: 搜索返回空结果？
A: 先运行 `python3 __main__.py scan /path/to/directory` 扫描目录建立索引。

### Q: 监控不工作？
A: 安装 watchdog: `pip install watchdog`

### Q: 技能未自动触发？
A: 检查 `openclaw.json` 中 main agent 是否包含 `file_search` 工具权限。

## 卸载

```bash
rm -rf ~/.openclaw/skills/file-indexer
rm -rf /home/t/cc_workspace/file_indexer
openclaw gateway restart
```

# SPM Skill — Installation Guide

## 前提条件

- OpenClaw 已安装并正常运行
- `git` 可用

## 安装步骤

### 1. 解压到 workspace

```bash
# 找到 SPM 包的位置，解压到 OpenClaw workspace
tar xzf spm-skill.tar.gz -C ~/.openclaw/workspace/
```

### 2. 创建插件软链接

```bash
ln -sfn ~/.openclaw/workspace/spm ~/.openclaw/plugins/SPM
```

### 3. 注册到 OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`，在 `skills.entries` 中添加：

```json
"SPM": {
  "enabled": true,
  "config": {
    "heartbeat_interval": "10m",
    "auto_checkpoint": true,
    "quality_gates_enabled": true,
    "wbs_ledger_path": "docs/spm/ledger.md",
    "parallel_subagents": true,
    "deployment_enabled": false
  }
}
```

也可以用命令行完成：

```bash
# 使用 python3 直接注入配置
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
config = json.load(sys.stdin)
config['skills']['entries']['SPM'] = {
    'enabled': True,
    'config': {
        'heartbeat_interval': '10m',
        'auto_checkpoint': True,
        'quality_gates_enabled': True,
        'wbs_ledger_path': 'docs/spm/ledger.md',
        'parallel_subagents': True,
        'deployment_enabled': False
    }
}
with open('/tmp/openclaw_spm.json', 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
"
mv /tmp/openclaw_spm.json ~/.openclaw/openclaw.json
```

### 4. 重启 Gateway

```bash
# 用 Gateway 工具重启，或在终端执行：
openclaw gateway restart
```

### 5. 验证安装

```bash
# 检查技能是否被识别
openclaw status
# 或在对话中询问："列出你可用的技能"
```

## 目录结构

安装后应有以下目录和文件：

```
~/.openclaw/workspace/spm/
├── SKILL.md               # 主技能文件 (20KB)
├── INSTALL.md             # 本安装指南
├── docs/
│   └── skill-selection-matrix.md
├── workflows/             # 13 个工作流
├── references/            # 3 个参考文件
├── schemas/               # 2 个 JSON Schema
├── scripts/               # 2 个脚本
├── templates/             # 2 个模板
└── subagents/             # 3 个 Subagent 提示模板
```

## 升级方法

```bash
# 用新包替换旧文件即可
rm -rf ~/.openclaw/workspace/spm
tar xzf spm-skill-v2.tar.gz -C ~/.openclaw/workspace/
# 无需修改配置或重启（symlink 保持指向）
```

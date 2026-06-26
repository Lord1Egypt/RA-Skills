# ClawHub Skill标准规范

---

## 一、Skill包结构

```
skill-name/
├── SKILL.md              # 必需 - YAML头部 + Markdown技能文档
├── clawhub.json          # 必需 - JSON配置文件
├── README.md             # 必需 - 说明文档
├── LICENSE               # 必需 - MIT许可证
├── .env.example          # 可选 - 配置模板（禁止提交真实密钥）
├── core/                 # 必需 - 核心代码目录
│   ├── main.py           # 主入口
│   ├── engine.py         # 引擎
│   └── helpers.py        # 辅助函数
├── templates/            # 可选 - HTML模板目录
│   └── index.html        # 前端模板
└── docs/                 # 可选 - 文档目录
    ├── 教程.md
    └── 推文.md
```

---

## 二、SKILL.md规范

### YAML头部（必需）

```yaml
---
name: skill-name          # Skill名称
version: 1.0.0            # 版本号
description: 简短描述      # 功能描述
author: 作者名             # 作者
license: MIT              # 许可证
priority: P0              # 优先级（P0/P1/P2）
keywords:                 # 关键词列表
  - 关键词1
  - 关键词2
triggers:                 # 触发词列表
  - 触发词1
  - 触发词2
config:                   # API配置
  API_KEY_1: required
  API_KEY_2: optional
output:                   # 输出格式
  type: html
  delivery: P0-force
  channels:
    - qqbot
    - telegram
repository:               # 仓库地址
  type: git
  url: https://github.com/user/skill
---
```

### Markdown内容（必需）

- 核心能力表格
- 算法说明
- 使用方法
- API配置
- 禁止事项

---

## 三、clawhub.json规范

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "描述",
  "author": "作者",
  "license": "MIT",
  "keywords": ["关键词"],
  "repository": {
    "type": "git",
    "url": "https://github.com/user/skill"
  },
  "homepage": "https://clawhub.com/skills/skill-name",
  "dependencies": {
    "flask": "^2.0.0"
  },
  "config": {
    "API_KEY": {
      "required": true,
      "description": "描述",
      "source": "https://api.example.com"
    }
  },
  "triggers": ["触发词"],
  "input": {
    "destination": {
      "type": "string",
      "required": true,
      "description": "描述"
    }
  },
  "output": {
    "type": "html",
    "format": "格式说明",
    "delivery": "P0-force",
    "channels": ["qqbot"]
  },
  "features": ["功能1", "功能2"],
  "performance": {
    "response_time": "<3秒"
  }
}
```

---

## 四、README.md规范

- 功能特点表格
- 快速开始（安装+配置+启动）
- API申请地址表格
- 使用示例
- 核心算法
- 输出格式
- 文件结构
- License

---

## 五、禁止事项

| 禁止项 | 说明 |
|------|------|
| **禁止提交真实密钥** | .env.example仅模板 |
| **禁止假链接** | 所有链接必须HTTP验证 |
| **禁止模拟数据** | 必须真实API调用 |
| **禁止LLM幻觉** | 数学收敛替代LLM判断 |

---

## 六、发布流程

```bash
# 1. 打包ZIP
zip -r skill-name.zip skill-name/

# 2. ClawHub登录
clawhub login --token YOUR_TOKEN

# 3. 发布
clawhub publish skill-name

# 4. 验证
clawhub search skill-name
```

---

**ClawHub Skill标准规范 - 确保技能包符合平台要求** 🦞

🦫 海狸 | 靠得住、能干事、在状态
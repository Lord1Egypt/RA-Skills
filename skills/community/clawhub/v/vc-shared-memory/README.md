# 🧠 Shared Memory

**跨团队、跨窗口、跨会话的统一记忆系统**

## 快速开始

```bash
# 查看统计
node shared-memory.js stats

# 发布公告
node shared-memory.js announce add "标题" "内容" --priority high

# 创建项目
node shared-memory.js project create "项目名称" --teams "搞钱特战队,软件开发团队"

# 记录经验
node shared-memory.js knowledge add lesson "经验标题" "经验内容"

# 搜索
node shared-memory.js search "抖音"

# 获取员工上下文
node shared-memory.js context "市场猎手"

# 备份
node shared-memory.js backup
```

## API 示例

```javascript
const { SharedMemory } = require('./shared-memory.js');
const sm = new SharedMemory();

// 发布公告
sm.announce({
  title: '战略决策',
  content: '聚焦变现',
  priority: 'critical',
  author: 'CEO马云'
});

// 创建项目
sm.createProject({
  name: 'OpenClaw 变现',
  teams: ['搞钱特战队', '软件开发团队'],
  createdBy: 'CEO马云'
});

// 为员工构建上下文（用于 virtual-company 集成）
const context = sm.getContextFor('市场猎手');
```

## 核心功能

- 📢 公司公告板
- 📋 项目协作空间
- 💡 知识库系统
- 👥 员工状态追踪
- 🔗 跨团队链接
- 💾 自动备份恢复

## 文档

详细文档请查看 [SKILL.md](SKILL.md)
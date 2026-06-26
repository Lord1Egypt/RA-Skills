# self-improving skill

自我提升技能中文版，纯提示词无脚本，模型能力越强效果越好

## 安装

执行命令安装
```sh
npx skills add https://github.com/seepine/self-improving
```

## 添加内容到 AGENTS.md

因有些 Agent 未必会默认加载所有技能，所以可添加以下内容到 AGENTS.md 最末尾，提高触发概率

```md
## 自我改进技能

### 工作区结构

workspace-dir              # 工作空间目录
├── AGENTS.md                # 智能体说明文件
└── .learnings/              # 此技能的学习记录文件目录
    ├── LEARNINGS.md         # 纠正、知识差距、最佳实践的文件
    ├── ERRORS.md            # 命令失败、异常
    └── FEATURE_REQUESTS.md  # 用户请求的功能

### 何时改进

在以下情况下应用自我改进：

1. **发现非显而易见的东西** - 解决方案不是立即的
2. **纠正自己** - 最初的方法是错误的
3. **学习项目约定** - 发现未记录的模式
4. **遇到意外错误** - 特别是诊断困难时
5. **找到更好的方法** - 改进了原始解决方案

### 如何改进

具体查看 `self-improving` 这个技能

```
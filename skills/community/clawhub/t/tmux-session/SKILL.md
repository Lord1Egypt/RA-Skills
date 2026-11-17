---

slug: claude-tmux
name: claude-tmux
version: 1.0.2
displayName: Claude终端复用工具
summary: 纯指令型tmux助手,所宣即所做,会话管理利器。This skill is an instruction-only tmux helper that
  does what it adverti
summary_zh: 纯指令型tmux助手,所宣即所做,会话管理利器。This skill is an instruction-only tmux helper
  that does what it adverti
license: MIT
description: |-。纯指令型tmux助手,所宣即所做,会话管理利器。This skill is an instruction-only tmux helper。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。
  that does what it adverti。支持自动化配置和灵活的参数设置，适适配多种工作环境，增强工作效率。。纯指令型tmux助手,所宣即所做,会话管理利器。This
  skill is an instruction-only tmux helper that does what it adverti'
tags:
- Development
- 工具
- 效率
- api
- tmux
tools:
- read
- exec
- write
homepage: ''
category: Automation
homepage: ""
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# ai-assistant Tmux

## 专业版专属特性
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| ai-assistant Tmux会话管理 | 不支持 | 支持 |
| 高清分辨率与无损输出 | 不支持 | 支持 |
| 批量生成与风格预设 | 不支持 | 支持 |
| 自定义模型微调 | 不支持 | 支持 |
| 商用版权授权 | 不支持 | 支持 |

## 典型场景
| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 管理操作 | 操作目标与参数 | 操作结果与状态变更 |
| 会话管理 | 会话名与窗口操作 | 会话状态与窗口列表 |
| 纯指令型tmux助手 | 目标数据与配置参数 | 处理结果与执行状态 |

**不适用于**：需要人工判断的复杂决策场景

## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| content | string | 否 | claude-tmux处理的内容输入 |,  |
| mode | string | 否 | 处理模式, 可选: json/text/markdown,  |
| max_retries | integer | 否 | 单步最大重试次数, 默认: 2 |
| skip_steps | array | 否 | 跳过的步骤编号(用于断点续传), 默认: [] |

## 输出说明
```json
{
  "success": true,
  "data": {
    "final_result": {
      "tmux_result": "tmux_result_value",
      "tmux_metadata": "tmux_metadata_value",
      "tmux_status": "tmux_status_value"
    },
    "execution_log": [
      {
        "step": 1,
        "name": "按流程执行",
        "status": "completed",
        "duration_ms": 1200,
        "output_summary": "按流程执行"
      },
      {
        "step": 2,
        "name": "按流程执行",
        "status": "completed",
        "duration_ms": 3500,
        "output_summary": "按流程执行"
      },
      {
        "step": 3,
        "name": "按流程执行",
        "status": "completed",
        "duration_ms": 2100,
        "output_summary": "按流程执行"
      },
      {
        "step": 4,
        "name": "按流程执行",
        "status": "completed",
        "duration_ms": 800,
        "output_summary": "按流程执行"
      }
    ],
    "total_duration_ms": 7600,
    "gates_passed": 3,
    "gates_total": 3
  },
  "error": null
}
```

中间产物模板参考: `assets/claude-tmux_template`

## 运行环境
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(ai-assistant Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 

### 可用性分类
- **分类**: MD+execute()
- **说明**: 基于Markdown的AI Skill,

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 能力边界
- 需要API Key，无Key环境无法使用

## 常见问题FAQ

### Q1: Claude Tmux支持哪些操作系统？
A: Claude Tmux支持Windows、macOS和Linux操作系统。

### Q2: Claude Tmux如何处理会话和窗口？
A: Claude Tmux可以创建、切换、重命名和关闭tmux会话和窗口，并提供会话和窗口列表。

### Q3: Claude Tmux如何处理多台机器上的tmux会话？
A: Claude Tmux不支持跨机器的tmux会话管理，它仅限于单个机器上的tmux会话。

### Q4: Claude Tmux如何处理tmux的复制和粘贴功能？
A: Claude Tmux可以执行tmux的复制和粘贴命令，但具体功能取决于tmux的配置。

### Q5: Claude Tmux如何处理tmux的同步功能？
A: Claude Tmux不支持tmux的同步功能，因为它主要是一个指令型助手，不涉及复杂的会话同步。

## 安全合规准则
| 风险项 | 等级 | 防护措施 | 验证方法 |
|:------|:------|:------|:------|
| API Key泄露 | 高 | 使用环境变量存储API Key，避免代码库泄露 | 检查代码库和日志文件 |
| 会话未加密 | 中 | 使用SSH密钥对连接进行加密 | 检查SSH配置和日志 |
| 权限不当 | 中 | 限制tmux操作权限，避免未授权访问 | 检查tmux权限设置和日志 |
| 系统漏洞 | 高 | 保持操作系统和软件更新 | 定期进行安全扫描和更新 |
| 网络攻击 | 高 | 使用防火墙和异常检测系统 | 定期检查网络流量和安全事件 |

## 差异化分析
| 场景 | 效率提升 | 差异化对比 |
|:-----|:-------|:-------|
| 会话管理 | 自动化会话创建和切换，节省时间 | 传统方法需要手动操作，效率低 |
| 窗口操作 | 自动化窗口创建和重排，提高效率 | 传统方法需要手动操作，效率低 |
| 复制粘贴 | 自动化复制粘贴操作，减少错误 | 传统方法需要手动操作，容易出错 |
| 同步功能 | 提供同步功能，提高团队协作效率 | 传统方法缺乏同步功能，协作效率低 |
| 安全性 | 提供安全防护措施，降低风险 | 传统方法缺乏安全措施，风险高 |

## 效能分析
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 优势分析
| 对比维度 | Claude终端复用工具 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 纯指令型tmux助手,所宣即所做,会话管理利器。This skill is an | 通用场景 | 通用场景 |

## 异常修复
针对Claude终端复用工具使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### Claude终端复用工具通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

## 初始设定
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码

### 前置条件

- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪

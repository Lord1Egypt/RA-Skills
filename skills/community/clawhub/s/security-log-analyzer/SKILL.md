# 安全事件日志调查助手

## 功能说明

基于 LLM 的安全事件日志分析工具，支持简要分析和详细分析两种模式。

## 安装

```bash
cd /root/.openclaw/skills/security-log-analyzer
pip install -r requirements.txt
cp .env.example .env
# 编辑.env 文件，填写 API Key
```

## 配置

编辑 `.env` 文件：

```bash
SILICONFLOW_API_KEY=sk-your-api-key-here
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=Qwen/Qwen3-8B
API_RATE_LIMIT=2
```

## 使用方法

### 方式 1: 交互模式

```bash
cd /root/.openclaw/skills/security-log-analyzer
python src/analyzer.py
```

### 方式 2: 文件模式

```bash
python src/analyzer.py /path/to/log.txt brief   # 简要分析
python src/analyzer.py /path/to/log.txt detailed # 详细分析
```

## 分析模式

- **简要分析**：快速提取关键信息（威胁等级、事件类型、建议行动）
- **详细分析**：深度分析攻击链、IOC 指标、缓解建议

## 限流保护

- 默认请求间隔：2 秒
- 429 错误自动重试（等待 10 秒）
- 单条日志超过 4000 token 自动截断

## 示例日志

查看 `examples/sample_logs/` 目录中的示例日志文件。

## 输出示例

```markdown
## 事件概览
- 事件类型：SSH 暴力破解
- 威胁等级：中
- 时间范围：2026-04-22 20:00 - 21:30

## 关键发现
- 来自同一 IP 的 150+ 次失败登录尝试
- 目标账号：root, admin, ubuntu

## IOC 指标
- IP: 192.168.1.100

## 建议行动
1. 封禁源 IP
2. 启用 fail2ban
3. 配置 SSH 密钥认证
```

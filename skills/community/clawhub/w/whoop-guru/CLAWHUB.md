# ClawHub Metadata

version: 8.4.12
slug: whoop-guru
name: WHOOP Guru
description: |
  完整的WHOOP健康管理系统。整合WHOOP官方API数据获取、交互式图表可视化、
  LLM AI私人教练、个性化训练计划（跑步/力量/减脂/康复）、ML恢复预测
  和每日主动推送，为用户提供一站式健康管理和健身指导。
  
summary: Complete WHOOP health system with AI coach, charts, training plans, and ML predictions
owner: effeceee

tags:
- whoop
- fitness
- coach
- ai-coach
- llm
- health
- workout
- recovery
- sleep
- hrv
- running
- marathon
- strength
- fatloss
- training
- injury-recovery
- charts
- visualization

requirements:
  python: ">=3.8"
  bins:
    - python3
    - curl
  packages:
    pandas: ">=1.3"
    matplotlib: ">=3.5"
    requests: ">=2.25"

features:
  - id: whoop_api
    title: WHOOP官方API数据
    description: 实时获取恢复、睡眠、训练负荷、HRV等数据，支持OAuth认证
  - id: data_charts
    title: 交互式图表
    description: 生成恢复/睡眠/strain/HRV趋势图表，HTML格式，支持暗色主题
  - id: llm_coach
    title: LLM AI教练
    description: 支持8种模型（MiniMax/OpenAI/GLM/Kimi等），基于LLM生成个性化训练建议
  - id: running_plans
    title: 跑步训练计划
    description: 支持3公里/5公里/10公里/半马/全马/超级马拉松，从新手到完赛
  - id: strength_plans
    title: 力量训练计划
    description: 增肌计划（16周）、减脂计划（12周），配合营养建议
  - id: injury_recovery
    title: 伤痛恢复
    description: 膝盖/肩关节/腰痛等伤痛恢复训练方案
  - id: ml_predictions
    title: ML恢复预测
    description: 7天恢复预测、HRV异常检测、训练强度建议
  - id: progress_tracking
    title: 进度追踪
    description: 打卡系统、连续记录、周报、目标仪表盘
  - id: proactive_notifications
    title: 主动推送
    description: 08:00早报、09:00早安、18:00晚间追踪、20:00打卡提醒、22:00日报

commands:
  - /coach
    description: 开启AI教练对话
  - /plan
    description: 生成今日训练计划
  - /checkin
    description: 训练打卡
  - /progress
    description: 查看训练进度
  - /16week
    description: 生成16周训练计划
  - /marathon
    description: 生成马拉松训练计划
  - /race
    description: 生成比赛训练计划
  - /strength
    description: 生成力量训练计划
  - /fatloss
    description: 生成减脂计划
  - /recovery
    description: 生成伤痛恢复计划
  - /profile
    description: 查看/设置健身档案
  - /llm
    description: 配置LLM模型
  - /chart
    description: 生成健康图表

environment:
  OPENCLAW_WORKSPACE:
    description: OpenClaw workspace directory
    required: false
  WHOOP_DATA_DIR:
    description: WHOOP data storage directory
    required: false
  WHOOP_SKILL_DIR:
    description: Skill directory for data sync
    required: false

credentials:
  whoop_oauth:
    description: WHOOP OAuth credentials (CLI args, not env vars)
    cli_args: ["--client-id", "--client-secret"]
    used_by: scripts/whoop_auth.py login
    stored_at: ~/.clawdbot/whoop-tokens.json
  whoop_env:
    description: WHOOP credentials as env vars (alternative method)
    file: ~/.clawdbot/whoop-credentials.env
    used_by: lib/whoop-fetcher.sh
    variables: [WHOOP_CLIENT_ID, WHOOP_CLIENT_SECRET, WHOOP_REFRESH_TOKEN]
  llm_api:
    description: LLM API key (via chat command)
    used_by: lib/llm.py
    stored_at: data/config/llm_config.json

data_flow:
  - 用户健康数据从WHOOP API获取
  - 健康数据发送到用户配置的LLM API用于分析
  - 凭证存储在本地，不上传

data_storage:
  profiles:
    path: data/profiles/
    description: 用户健身档案和目标（相对路径，相对于skill目录）
  plans:
    path: data/plans/
    description: AI生成的训练计划
  logs:
    path: data/logs/
    description: 打卡记录和追踪数据
  config:
    path: data/config/llm_config.json
    description: LLM API密钥配置（用户自行配置，不上传）
  tokens:
    description: WHOOP OAuth token存储
    storage_path: ~/.clawdbot/whoop-tokens.json
    handling: |
      WHOOP OAuth token存储在 ~/.clawdbot/whoop-tokens.json
      LLM API密钥存储在 data/config/llm_config.json
      所有凭证文件由OpenClaw管理，不上传外部服务
  privacy: |
    凭证存储：API密钥和Token存储在本地，不上传。
    数据流向：
    - 用户数据（恢复/睡眠/训练）从WHOOP API获取
    - 健康数据发送给LLM API用于生成分析
    - LLM API密钥仅用于API调用，不作他用
    用户可随时删除data/目录清除所有本地数据。

installation_notes: |
    安装步骤：
    1. pip install requests pandas matplotlib
    2. python3 scripts/whoop_auth.py login --client-id YOUR_ID --client-secret YOUR_SECRET
    3. 完成 OAuth 授权（浏览器自动打开）
    4. (可选) 配置 LLM API

# 待办事项 - TingDong 项目

## ✅ 已完成
- [x] tingdong-skill 支持自定义 API URL（环境变量 `TINGDONG_API_URL`）
- [x] tingdong-skill 上架 ClawHub（v1.0.0）
- [x] 安装测试通过

## ⏳ 待办

### 高优先级
- [ ] **扣子 Skill 适配** — 在腾讯扣子平台创建 tingdong Skill，调用现有后端 API，支持技能商店上架和收费
- [ ] **Docker 一键部署脚本** — 写 docker-compose.yml，让有服务器的人能自建 tingdong 后端
- [ ] **部署文档** — tingdong 后端自建指南（服务器要求、环境配置、API Key 申请等）

### 中优先级
- [ ] **tingdong-skill v1.1** — 根据使用反馈迭代（如支持纯文本输入、批量链接处理优化等）
- [ ] **监控告警完善** — monitor.py 接入飞书 webhook，异常时自动通知
- [ ] **API 文档完善** — references/api_docs.md 补充错误码、限流说明

### 低优先级
- [ ] **内容源扩展** — 支持小红书、B站专栏、即刻等更多平台
- [ ] **语音风格扩展** — 支持更多 TTS 引擎（Azure、ElevenLabs 等）

# 📊 HIIC产业日报 - 快速参考指南

## 🎯 28个产业集群速查表

### 战略性新兴产业
1. **半导体与集成电路** - 芯片、光刻机、制程、国产化
2. **人工智能** - AI、大模型、GPT、机器学习、深度学习
3. **网络与通信** - 5G、6G、通信技术、网络设备
4. **超高清视频显示** - 8K、显示面板、OLED、Mini-LED
5. **智能终端** - 智能手机、可穿戴设备、智能音箱
6. **智能传感器** - 传感器、MEMS、物联网
7. **软件与信息服务** - SaaS、云计算、软件开发
8. **数字创意** - 数字内容、游戏、动画、VR/AR

### 先进制造业
9. **高端装备与仪器** - 数控机床、精密仪器、工业机器人
10. **低空经济与空天** - 无人机、通用航空、卫星
11. **机器人** - 工业机器人、服务机器人
12. **智能机器人** - AGV、协作机器人、特种机器人
13. **现代时尚** - 服装、珠宝、时尚设计
14. **安全节能环保** - 环保设备、节能技术、安全设备
15. **新能源** - 光伏、风电、储能、氢能
16. **智能网联汽车** - 新能源汽车、自动驾驶、车联网

### 未来产业
17. **量子信息** - 量子计算、量子通信、量子传感
18. **光载信息** - 光通信、光计算、光存储
19. **高性能材料** - 高温合金、复合材料、超导材料
20. **前沿新材料** - 石墨烯、纳米材料、智能材料
21. **海洋产业** - 海洋工程、海洋资源、海洋生物
22. **深地深海** - 深海探测、深地开发
23. **生物医药** - 创新药、疫苗、生物技术
24. **高端医疗器械** - 医疗设备、诊断设备、植入器械
25. **大健康** - 健康管理、康复医疗、养老
26. **生物制造** - 生物基材料、合成生物学
27. **脑科学与脑机工程** - 脑机接口、神经科学
28. **细胞与基因** - 基因编辑、细胞治疗、基因测序

---

## 🚀 常用命令速查

### 生成日报
```bash
# 使用预设产业
node scripts/generate-report-v7.3.mjs --industry "人工智能"

# 使用自定义关键词
node scripts/generate-report-v7.3.mjs --keywords "固态电池,新能源"

# 生成并推送
node scripts/generate-report-v7.3.mjs --industry "人工智能" --push

# 指定时间范围
node scripts/generate-report-v7.3.mjs --industry "人工智能" --days 3
```

### 订阅管理
```bash
# 查看订阅
node scripts/subscription-manager.mjs list

# 添加订阅
node scripts/subscription-manager.mjs add --industry "人工智能" --schedule "daily"

# 删除订阅
node scripts/subscription-manager.mjs remove <id>

# 暂停订阅
node scripts/subscription-manager.mjs pause <id>

# 恢复订阅
node scripts/subscription-manager.mjs resume <id>
```

### 定时任务
```bash
# 每日9点推送
openclaw cron add "0 9 * * *" \
  "node /path/to/generate-report-v7.3.mjs --industry '人工智能' --push"

# 每周一9点推送
openclaw cron add "0 9 * * 1" \
  "node /path/to/generate-report-v7.3.mjs --industry '人工智能' --days 7 --push"

# 查看定时任务
openclaw cron list

# 删除定时任务
openclaw cron remove <task-id>
```

---

## 📊 性能指标

### 数据质量
- **时效性**：100% 24小时内
- **覆盖率**：热门行业15-22条/天，小众行业5-10条/天
- **准确性**：90% 内容提取成功率
- **摘要长度**：50-200字符

### API消耗
- **Tavily**：6-10次/生成
- **Brave**：6-10次/生成
- **Jina Reader**：15-25次/生成

### 配额管理
- 每个产业每天最多生成2-3次
- 避免频繁测试消耗配额
- 建议使用订阅而非手动生成

---

## 🔧 配置文件位置

### 必需配置
```bash
# API密钥
export TAVILY_API_KEY="tvly-xxx"
export BRAVE_API_KEY="xxx"

# 飞书配置
~/.openclaw/workspace/hiic-push-config.json
```

### 技能配置
```bash
# 产业预设
references/industries/*.json

# 飞书字段映射
scripts/feishu-config.json

# 订阅数据
~/.openclaw/workspace/hiic-subscriptions.json
```

---

## 🐛 故障排查

### 问题1：搜索无结果
```bash
# 检查API密钥
echo $TAVILY_API_KEY
echo $BRAVE_API_KEY

# 测试网络
curl -I https://api.tavily.com

# 查看日志
node scripts/generate-report-v7.3.mjs --industry "人工智能" --verbose
```

### 问题2：推送失败
```bash
# 检查飞书配置
cat ~/.openclaw/workspace/hiic-push-config.json

# 测试飞书连接
curl -H "Authorization: Bearer $FEISHU_TOKEN" \
  https://open.feishu.cn/open-apis/bot/v3/info

# 查看错误日志
tail -f ~/.openclaw/logs/hiic-*.log
```

### 问题3：定时任务不执行
```bash
# 检查OpenClaw状态
openclaw status

# 查看定时任务
openclaw cron list

# 查看执行日志
openclaw cron logs <task-id>
```

---

## 💡 最佳实践

### 关键词优化
- ✅ 使用具体组合：`"油价 上涨"` 而非 `"石油"`
- ✅ 混合中英文：`"煤化工 coal chemical"`
- ✅ 包含公司名：`"中煤能源 China Coal"`
- ❌ 避免单字关键词
- ❌ 避免过于宽泛的词

### 订阅策略
- **热门行业**（AI、半导体）：每日推送
- **小众行业**（煤化工、海洋）：每周推送
- **自定义关键词**：根据需求调整

### 摘要质量
- 自动扩充到50-200字
- 移除元数据标记
- 智能标点截断
- 语义完整性检查

---

## 📞 获取帮助

- **查看文档**：`cat SKILL.md`
- **查看示例**：`cat references/output-example.md`
- **查看配置**：`cat references/config-template.json`
- **联系支持**：OpenClaw社区或飞书群组

---

**🦞 小咔拉咪为你打造，让产业资讯获取变得简单高效！**

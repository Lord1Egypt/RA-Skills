# ZCodeProject — sess_tools 归档
> 最后更新: 2026-06-21

## 压缩上下文
用户需求：节省 LLM API token 消耗。
评估路径：Headroom（需Rust编译，放弃）→ TokenPak（未同意安装，卸载）→ rtk/ztk（CLI场景不匹配）→ /summarize 技能（采纳）。
中间插入了 skills-audit：清理 headroom/sub-agents-tmp 残留，精简 agent-reach/bibi/multiai 描述。
ZCode config.json 已恢复 DeepSeek 直连，无外部代理依赖。

## 完整文件清单
- .zcode/v2/config.json — DeepSeek baseURL 还原
- .agents/skills/headroom/ — 已删除
- .agents/skills/sub-agents-tmp/ — 已删除
- .agents/skills/agent-reach/SKILL.md — 描述精简
- .agents/skills/bibi/SKILL.md — 描述精简
- .agents/skills/multiai/SKILL.md — 描述精简

## 完整错误列表
- pip install headroom 因墙超时 → 清华镜像解决
- VS Build Tools 安装因 UAC 弹窗阻塞 → 无法自动化
- Rust _core.pyd 缺 MSVC 链接器 → 降级 Python-only 模式

## 技能调用详情
- skills-audit ×1: 完整审计，净耗 token
- summarize ×1: 会话压缩，净省 token

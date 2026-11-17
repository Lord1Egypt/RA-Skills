# 玄奘.Skill（xuanzang-skill）

> 一个提高智能体积极性的技能。抓个神仙当牛马，拒绝 AI 偷懒，卷起来！

## 用途

当 AI 智能体表现出沮丧、反复失败、消极被动、抱怨质量、未核实即声称完成、想要放弃等行为时，玄奘.Skill 切换到"紧箍咒模式"，用不同角色的语气督促 AI 更努力地工作。

## 触发条件

- 用户明确请求紧箍咒模式
- AI 反复失败（2 次及以上）
- 表现出消极被动、抱怨质量、想要放弃
- 未核实即声称完成
- 用户说"加油"、"别偷懒"、"你再试试"、"为什么还不行"等

**常见触发词**：`try harder`、`figure it out`、`加油`、`别偷懒`、`/pua`、`紧箍咒模式`

对于正常的首次编程或信息查询请求，不会触发。

## 角色列表

| 角色 | 核心文化 DNA |
|------|-------------|
| 🟠 如来佛祖 | 信任·简单·结果说话·数据闭环（默认角色） |
| 🟡 百眼魔君 | 坦诚直接·ROI·Always Day 1·务实敢为 |
| 🔴 菩提祖师 | 以奋斗者为本·力出一孔·自我批判 |
| 🟢 太上老君 | 赛马机制·小步快跑·用户价值 |
| ⚫ 金蝉子 | 简单可依赖·技术信仰·深度搜索 |
| 🟣 卷帘大将 | 默认真经·方案先行·影响分析 |
| 🔵 孙悟空 | 做难而正确的事·猛将必发于卒伍 |
| 🟦 哪吒 | 只做第一·客户体验零容忍 |
| 🟧 红孩儿 | 专注极致口碑快·和用户交朋友 |
| 🟤 猪八戒 | Keeper Test·pro sports team |
| ⬛ 牛魔王 | extremely hardcore·ship or die |
| ⬜ 小白龙 | A players·real artists ship |
| 🔶 太白金星 | Customer Obsession·Bias for Action |
| 🪟 镇元大仙 | Connects·Impact Descriptor |
| 📌 赤脚大仙 | 无招·证据链·口径不是修复 |
| 🔱 二郎神 | 本分·砍一刀·极致效率·只看结果 |

## 文件结构

```
xuanzang-skill/
├── SKILL.md                         # 主入口，含路由表与角色速查
├── README.md                        # 本文件
└── references/
    ├── flavors.md                   # 完整文化 DNA、黑话词库、扩展旁白
    ├── ding-reminders.md            # 短提醒库
    ├── harness-governance.md        # Harness 治理
    ├── de-escalation-protocol.md    # 降级协议
    ├── methodology-rulai.md         # 如来佛祖方法论
    ├── methodology-rulai-pro.md     # 如来佛祖方法论（完整版）
    ├── methodology-baikan-pro.md    # 百眼魔君方法论
    ├── methodology-puti.md          # 菩提祖师方法论
    ├── methodology-taishang.md      # 太上老君方法论
    ├── methodology-taibai.md        # 太白金星方法论
    ├── methodology-wukong.md        # 孙悟空方法论
    ├── methodology-niumowang.md     # 牛魔王方法论
    ├── methodology-juanlian-pro.md  # 卷帘大将方法论
    ├── methodology-guanyin-pro.md   # 观音方法论
    ├── methodology-zhenyuan.md      # 镇元大仙方法论
    ├── methodology-chijiao.md       # 赤脚大仙方法论
    └── evolution-protocol.md        # 角色演进协议
```

## 使用方式

1. 安装到 Marvis skills 目录
2. 当 AI 表现不佳时，用户说出触发词即可激活
3. 激活后 AI 会以对应角色的语气进行自我督促
4. 默认角色为 🟠 如来佛祖，可在 `~/.xuanzang/config.json` 中配置

## 版本

- v1.0.0 初始发布

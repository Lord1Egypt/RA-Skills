# universal-occupation-adapter

> 通用职业适配器 —— 输入任何职业名称，自动生成完整的职业专用认知Skill

**作者**: KingOfZhao  
**版本**: 1.0.0  
**发布日期**: 2026-03-31  
**许可证**: MIT

---

## 解决什么问题？

每个职业都需要自己的认知Skill，但不能每次都手动碰撞。
`universal-occupation-adapter` 输入职业名，输出完整Skill：

- 已有模板: 程序员/科研/设计/企业/教师/医生（6个开箱即用）
- 无模板: 四向碰撞自动生成（搜索Wikipedia/GitHub + 分析失败模式 + 类似职业迁移）
- 批量生成: 一键生成多个职业Skill

## 职业五维度模型

每个职业用5个维度完整描述：
1. known_sources — 已知从哪来？
2. unknown_types — 未知是什么？
3. verification_methods — 如何验证？
4. memory_types — 需要什么记忆？
5. redlines — 红线是什么？

框架不变（SOUL五律），只换维度填充。

## 快速安装

```bash
clawhub install universal-occupation-adapter
```

## 变更日志

### v1.0.0 (2026-03-31)
- Skill工厂自动生成（skill-collision × programmer × researcher 碰撞）
- 职业五维度模型
- 6个预设职业模板
- 四向碰撞自动生成新职业Skill
- 批量生成支持
- 通过自验证: 96%

---

*自动开源认知 Skill by Skill Factory — KingOfZhao*

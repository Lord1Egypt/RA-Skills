# 发布与维护说明

## 目录结构

```text
sansheng-liubu-skill-map/
├── SKILL.md
└── references/
    ├── sansheng_liubu_skill_map.yaml
```

## 用途
本 skill 用于把“三省六部 × 技能库”的匹配关系沉淀为可复用的组织协作模板。

## 发布前建议
1. 校验技能名是否符合远程仓库命名规范。
2. 确认技能描述覆盖触发词：三省六部、技能匹配、部门映射、多 Agent 协作、GitHub、数据分析。
3. 如需发布到 ClawHub，可补版本号与 changelog。
4. 如需内网私有分发，可直接复制本目录到目标 skills 目录。

## 后续维护
- 新增技能时，优先更新 `references/sansheng_liubu_skill_map.yaml`
- 若触发条件变化，再同步更新 `SKILL.md` frontmatter description
- 若要补更多制度或示例，可继续增补到 `references/`，避免把 SKILL.md 写得过长

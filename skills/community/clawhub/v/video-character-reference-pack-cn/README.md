# 视频人物参考卡

![视频人物参考卡推广图](assets/promo-1600x900.png)

把授权角色资料变成可跨镜头复用的一页人物约束卡，减少换镜后外观、服装和动作“跑偏”。适合中文小店经营者、小说作者及自媒体创作者。

## 你会得到什么

- 外观、服装、动作三类明确约束
- 已知事实与建议分开呈现
- 可贴进分镜或脚本的 Markdown 卡片
- 资料不完整时，先说明缺什么，不编造人物细节

## 输入

提供用户授权的角色参考图描述、故事、造型限制。可直接使用 [成功样例](fixtures/success-input.json) 的 JSON 结构。

## 输出

输出格式见 [SKILL.md](SKILL.md)；完整示例见 [预期成功卡](fixtures/success-expected.md)。如果缺少关键字段，预期行为见 [失败样例](fixtures/failure-expected.md)。本 Skill 只交付一致性文本素材，不生成图片，也不提供通用提示词优化。

## 安装与使用

将本仓库放入支持 `SKILL.md` 的 Skill 目录，按宿主工具加载后，用默认提示词提交三项输入即可。无需 API、浏览器登录或第三方服务。

## 自测

在仓库根目录运行：

```bash
python3 scripts/self_test.py
```

该自测只验证发布结构、必填字段、图标尺寸、成功/失败样例以及失败样例是否明确指出缺失字段；它不声称验证模型对真实人物资料的判断质量。真实使用时，按 SKILL.md 的工作流由执行模型完成卡片整理。

## 来源与许可证

实现与中文文案均为原创。仅参考 [agentara/skills](https://github.com/agentara/skills) 及其 [video-storyboard Skill](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md) 的公开用途定位，未复制源码或文案。参考页面所示许可证以其仓库实际声明为准；本仓库采用 [MIT-0](LICENSE)。

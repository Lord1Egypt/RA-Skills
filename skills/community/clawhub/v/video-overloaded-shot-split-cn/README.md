# 复杂镜头拆分计划

![复杂镜头拆分计划推广图](assets/promo-1600x900.png)

把已经写好的、动作和信息塞得过满的镜头，拆成可拍摄或可生成的连续镜头表；既保留剧情必留点，又给出方向、动作、声音和景别的衔接要求。它不写新脚本，也不做泛化提示词改写。

## 输入与结果

输入三项即可：已有镜头描述、情节必留点、总时长预算。输出包含拆分判断、时长汇总，以及「编号 / 时长 / 可拍或可生成镜头 / 保留信息或动作 / 衔接要求」表格。缺少任一必需项时，会只列出缺项；单次限定一章、一场或短文，表格最多 100 行，超出时要求分批。

## 安装

```bash
npx skills add xxjrq/video-overloaded-shot-split-cn
```

## 适用场景

适合把追逐、打斗、逃离、关键物件揭示等过载镜头，按给定时长落为拍摄或生成可执行的镜头。原本负载适中的镜头不会为了凑数量而拆开。

## 示例

- 成功样例：
- [成功输入](fixtures/success-input.md) 与 [对应交付](fixtures/success-output.md)
- [缺料输入](fixtures/failure-input.md) 与 [缺料处理](fixtures/failure-output.md)

## 自检

```bash
bash scripts/self-test.sh
```

自检只检查本仓库必需文件、标识字段和 PNG 尺寸，不依赖其他 Skill 或本机绝对路径。

## 来源与许可

本 Skill 为原创说明、步骤与示例；仅核对了 [seaartpublic/skills 的 storyboard-prompt-assistant](https://github.com/seaartpublic/skills/blob/main/storyboard-prompt-assistant/SKILL.md) 的业务用途，未复制其文本或代码。仓库内容以 [MIT-0](LICENSE) 发布。

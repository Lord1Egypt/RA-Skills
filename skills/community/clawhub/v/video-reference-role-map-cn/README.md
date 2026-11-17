# 视频参考素材分工表

将用户已经授权的参考素材，变成一张清楚的“谁负责什么”的视频生成参考表：每张图分别承担身份、地点、风格或动作职责，并提前发现冲突和缺料。不会下载来源，也不会虚构模型参数。

![推广图](assets/promo-1600x900.png)

## 输入与结果

输入生成目标，以及带编号的授权素材列表（描述、文件名或用户给出的标识、允许用途）。输出 Markdown 表格，逐项列出身份／地点／风格／动作用途和冲突说明，最后给出必须补充的资料。单次最多100行；超出时按章节或场景分批。

## 安装

```bash
npx skills add xxjrq/video-reference-role-map-cn
```

## 使用提示

把生成目标和素材列表直接交给 Skill。请附可查看素材或具体可见内容；只有“肖像／街景／截帧”名称时，输出候选用途与待补资料，不推断发型、服装、地点、色彩或光线。静帧不能证明转身等连续动作，需要开始、过程和结束的说明或授权连续片段。

可查看[素材描述不足时的完整输入与交付](fixtures/success.md)、[缺料交付](fixtures/failure.md)，以及[另一组具体描述输入](fixtures/forward-new-input.json)与[实际分工结果](fixtures/forward-new-success.md)。这些示例是文字材料验收，未声称查看了未提供的图片。

## 本地自检

```bash
python3 scripts/self_test.py
```

## 来源与许可证

业务用途曾核对 SeaArt Public Skills 的公开页面；本仓库的说明、步骤和示例均为原创，未复制外部原文或源码。来源：[seaartpublic/skills](https://github.com/seaartpublic/skills)（仅作业务用途核对）。本仓库采用 [MIT-0](LICENSE)。

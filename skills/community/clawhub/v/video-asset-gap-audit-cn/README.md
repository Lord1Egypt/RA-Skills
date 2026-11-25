# 视频素材缺口表

在开拍或补料前，把已批准的镜头需求与手头素材逐项核验，直接得到“能用、缺失、规格不符、待确认”的可执行清单。它不会把名字看似合适的文件误判为已备齐。

![视频素材缺口表推广图](assets/promo-1600x900.png)

## 输入与结果

输入一条视频的已批准镜头表（最多 30 条）和素材清单（最多 50 项）。镜头需要内容、画幅、时长；素材还必须写明内容、可用时长与授权。结果是一份 Markdown：逐镜头匹配证据、缺失/规格不符清单、补拍或补生成条件，以及不能确认的资料项。

成功与失败的可复制输入见 [fixtures/success.json](fixtures/success.json) 与 [fixtures/failure.json](fixtures/failure.json)，对应的参考交付见 [成功结果](fixtures/success.expected.md) 与 [失败结果](fixtures/failure.expected.md)。运行后会分别生成相应的交付：

```bash
node scripts/audit.mjs fixtures/success.json /tmp/success-delivery.md
node scripts/audit.mjs fixtures/failure.json /tmp/failure-delivery.md
```

## 安装与使用

```bash
npx skills add xxjrq/video-asset-gap-audit-cn
node scripts/self-test.mjs
node scripts/audit.mjs fixtures/success.json /tmp/gap-audit.md
```

当内容、画幅、时长、授权均满足时才算覆盖。素材缺少内容说明、时长或授权信息时会列为“需确认”；仅有 `final.png` 这类文件名，不会被猜成可用人物图。

## 范围

仅审素材是否覆盖镜头需求，不下载、生成素材、配分镜或安排拍摄。

## 来源与许可证

业务用途参考了 [agentara/skills 的视频分镜条目](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md)，本仓库说明、代码与示例均为原创，未复制其文本或源码。采用 [MIT License](LICENSE)。

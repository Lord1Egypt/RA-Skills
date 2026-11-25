# 单镜头拍摄执行卡

把一条已批准的实拍镜头，变成摄影与演员能直接照做的现场执行卡。输入镜头、场地/人物/道具、可用设备、动作起止和交付要求；结果包含站位、取景、动作口令、收尾标记与现场检查项。关键动作、场地约束或设备缺失时，会先列出缺项；未知焦段、曝光等参数会标注为待试拍，不编造设置。

![单镜头拍摄执行卡推广图](assets/promo-1600x900.png)

## 安装

```bash
npx skills add xxjrq/video-single-shot-execution-card-cn
```

## 适用范围

一次只处理一条已批准的实拍镜头，帮助现场拍完这个确定镜头。不创作剧情、不排多条拍摄日程、不生成 AI 视频。

## 使用

调用 `$video-single-shot-execution-card-cn` 并提供已批准的镜头、场地约束、设备、动作起止与交付要求。批准镜头缺失、空白或仍待批准时，只返回缺项，不制作执行卡。脚本只检查字段与人物/道具锚点；执行 Agent 还必须核对批准镜头和动作起止、场地及道具是否语义一致，发现冲突就先确认，不可把字段校验当作语义审核。

### 输入示例

```json
{
  "approvedShot": "人物从门口走到桌前，放下杯子并停 2 秒。",
  "location": "室内入口与桌面之间通道保持畅通。",
  "people": "一名演员。",
  "props": "一个杯子、一张桌子。",
  "equipment": "手持相机。",
  "actionStart": "演员站在门口，杯子拿在手中。",
  "actionEnd": "杯子落在桌上，演员停留 2 秒。",
  "delivery": "一条完整可用的实拍镜头。"
}
```

执行输入检查：

```bash
node scripts/validate-input.mjs fixtures/success-input.json
```

可复制的交付参考：

- [成功输入](fixtures/success-input.json) → [完整执行卡](fixtures/success-output.md)
- [缺料输入](fixtures/failure-input.json) → [缺项处理](fixtures/failure-output.md)


- [已批准镜头新输入](fixtures/approved-shot-input.json) → [离线校验结果](fixtures/approval-check-report.md)
- [其余字段齐全但缺批准镜头](fixtures/missing-approved-shot-input.json) → [离线缺项结果](fixtures/approval-check-report.md)

## 自检

```bash
node scripts/self-test.mjs
```

该自检在本仓库内运行，实际执行成功、缺料以及批准镜头缺失/空值等输入校验，并检查发布所需文件。

## 来源与许可

业务用途参考了 [agentara/skills 的 video-storyboard Skill](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md)；本仓库的说明、规则、示例和脚本均为原创，未复制其内容或代码。发布文件采用 [MIT License](LICENSE)。

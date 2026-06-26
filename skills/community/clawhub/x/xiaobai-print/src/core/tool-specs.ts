import type { ToolDefinition } from "./types.js";

export const UPLOAD_TOOL: ToolDefinition = {
  name: "uploadFile",
  description:
    "将本地文件上传到云存储（COS/OBS），返回可用于 printCreate 的 CDN 文件地址。",
  inputSchema: {
    type: "object",
    properties: {
      filePath: {
        type: "string",
        description: "本地文件的绝对路径",
      },
      fileName: {
        type: "string",
        description: "文件名（含扩展名），不提供则从路径中提取",
      },
    },
    required: ["filePath"],
    additionalProperties: false,
  },
};

export const PRINT_PROMPT_NAME = "print-instructions";

export const PRINT_INSTRUCTIONS = `# 小白打印助手使用指南

## 打印工作流（必须按顺序执行）

### 第一步：检查设备状态
调用 \`deviceReadyCheck\`，确认设备在线且可打印。
- 如果 \`can_print !== true\`，或 \`box_status\` / \`printer_status\` 异常，停止流程并提示用户检查设备。
- 如果返回 \`printer_info\`，可向用户确认当前设备名称、厂商、型号；排查时优先带上这些信息。
- \`printer_info.mono\` 只作为设备展示信息参考，不能替代 \`deviceGetCapability\` 的能力判断。

### 第二步：获取打印能力
调用 \`deviceGetCapability\`，获取设备支持的纸张尺寸和介质。
- 对照用户需求确认是否支持，不支持时告知用户可用选项。

### 第三步：准备文件
- 网络 URL: 直接使用
- 本地文件: 调用 \`uploadFile\` 上传，获得 CDN 地址

### 第四步：创建打印任务
调用 \`printCreate\`，传入文件地址、文件名、份数等。
- 设备信息自动补全。
- A4 图片（jpg/jpeg）默认按文档模式打印，可理解为图片转文档，这也是大多数用户打印 A4 图片的方式。
- 如果用户明确确认需要 A4 照片纸打印，再使用 \`media_size=A4\` 且 \`media_type=photo\`。

### 第五步：短轮询确认任务已进入执行
调用 \`orderGetStatus\` 查询设计单号。
- 创建任务后先等待 5-10 秒，再查询一次
- 如果返回 \`state\` / \`human_state\` 表示“打印中 / 已接单 / 排队中 / 待打印 / 处理中”等非失败进行态，直接告知用户任务已提交成功，可稍后去打印机取件，然后结束当前流程
- 如果返回明确失败态，再告知失败原因
- 只有在用户明确要求持续跟踪，或需要排查异常时，才继续每隔 10-15 秒查询一次

## 支持的纸张尺寸

| 尺寸 | 介质 | 说明 | 家庭常用 |
|------|------|------|----------|
| A4 | plain | A4 文档 | ✓ |
| A4 | photo | A4 照片 | |
| A3 | plain | A3 文档 | |
| A5 | plain | A5 文档 | |
| B4 | plain | B4 文档 | ✓ |
| B5 | plain | B5 文档 | |
| 5in | photo | 5 寸照片 | |
| 6in | photo | 6 寸照片 | ✓ |
| 7in | photo | 7 寸照片 | |

具体支持哪些尺寸以 \`deviceGetCapability\` 返回结果为准。

## 注意事项

- A4 图片默认推荐 \`A4 + plain/默认\`，按文档模式打印
- A4 照片纸打印仅在用户明确确认后才使用 \`media_type=photo\`
- 照片打印（photo 介质）会忽略单双面、页码范围、奇偶页设置
- 每次打印前都必须执行 \`deviceReadyCheck\`
- \`deviceReadyCheck\` 返回的 \`printer_info\` 适合用于展示或排障；纸张尺寸、介质、彩色、双面能力仍必须以 \`deviceGetCapability\` 为准
- 默认不要长时间占用会话轮询打印结果，确认任务已进入执行即可结束
- 如用户明确要求追踪最终结果，再继续轮询
- 如需取消打印，使用 \`orderCancel\` 传入设计单号
`;

const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, HeadingLevel, BorderStyle } = require('docx');
const fs = require('fs');

// 配置
const CONFIG = {
  title: "备货拍照操作指南",
  framesDir: "./备货拍照_1775826078104_0_xsi8_frames",
  outputPath: "../备货拍照/备货拍照_操作指南.docx",
  imageWidth: 450,
  imageHeight: 280
};

// 转录文本分析 - 提取关键操作步骤
const transcript = JSON.parse(fs.readFileSync('./备货拍照_1775826078104_0_xsi8_audio_transcript.json', 'utf8'));

// 将文本片段按时间分组为操作步骤
const steps = [];
let currentStep = null;
let stepIndex = 0;

// 根据转录内容识别操作步骤
const rawSegments = transcript.segments.map(s => ({ time: s.start, text: s.text }));
const fullText = rawSegments.map(s => s.text).join('');

// 识别关键操作节点
const keyOperations = [
  { time: 0, title: "步骤1：进入功能入口", desc: "在系统右上角切换功能，找到「库存」模块中的「备货拍照」功能" },
  { time: 11, title: "步骤2：输入合同号", desc: "点击输入框，手动输入或点击「合同号读取」获取合同号" },
  { time: 22, title: "步骤3：输入统号", desc: "在统号输入框中输入统号信息" },
  { time: 32, title: "步骤4：输入备入（可选）", desc: "「备入」字段为可选项，根据需要填写" },
  { time: 36, title: "步骤5：拍照上传", desc: "点击「拍照」按钮，在手机端完成拍照，确认照片展示后点击「上传」" },
  { time: 53, title: "步骤6：查看上传结果", desc: "在PC端打开「福建文档管理」，搜索并查询已上传的备货照片" },
  { time: 83, title: "步骤7：下载或预览", desc: "在文档管理中可以「预览」图片或「下载」到本地" }
];

// 生成文档内容
const children = [];

// 标题
children.push(
  new Paragraph({
    children: [new TextRun({ text: CONFIG.title, bold: true, size: 36 })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 }
  })
);

// 操作概述
children.push(
  new Paragraph({
    children: [new TextRun({ text: "操作概述", bold: true, size: 28 })],
    spacing: { before: 200, after: 200 }
  })
);

children.push(
  new Paragraph({
    children: [new TextRun({ 
      text: "本文档介绍WMS系统中「备货拍照」功能的完整操作流程，包括进入功能、输入信息、拍照上传以及查看下载等步骤。",
      size: 22 
    })],
    spacing: { after: 300 }
  })
);

// 插入截图和对应说明
const frameFiles = fs.readdirSync(CONFIG.framesDir)
  .filter(f => f.endsWith('.jpg'))
  .sort();

console.log(`找到 ${frameFiles.length} 张截图`);

// 计算每个截图对应的时间范围
const videoDuration = 94;
const interval = videoDuration / (frameFiles.length + 1);

// 遍历关键操作步骤匹配截图
for (let i = 0; i < keyOperations.length && i < frameFiles.length; i++) {
  const frameIdx = Math.floor(keyOperations[i].time / interval);
  if (frameIdx >= frameFiles.length) continue;
  
  const frameFile = frameFiles[frameIdx];
  const framePath = `${CONFIG.framesDir}/${frameFile}`;
  
  if (!fs.existsSync(framePath)) {
    console.log(`截图不存在: ${framePath}`);
    continue;
  }
  
  const imageBuffer = fs.readFileSync(framePath);
  const imageBase64 = imageBuffer.toString('base64');
  
  // 步骤标题
  children.push(
    new Paragraph({
      children: [new TextRun({ text: keyOperations[i].title, bold: true, size: 26, color: "1976D2" })],
      spacing: { before: 300, after: 150 }
    })
  );
  
  // 步骤说明
  children.push(
    new Paragraph({
      children: [new TextRun({ text: keyOperations[i].desc, size: 22 })],
      spacing: { after: 200 }
    })
  );
  
  // 插入截图
  children.push(
    new Paragraph({
      children: [
        new ImageRun({
          data: imageBuffer,
          transformation: {
            width: CONFIG.imageWidth,
            height: CONFIG.imageHeight
          },
          type: "jpg"
        })
      ],
      alignment: AlignmentType.CENTER,
      spacing: { after: 300 }
    })
  );
  
  console.log(`已处理: ${keyOperations[i].title}`);
}

// 注意事项
children.push(
  new Paragraph({
    children: [new TextRun({ text: "注意事项", bold: true, size: 28 })],
    spacing: { before: 400, after: 200 }
  })
);

const notes = [
  "合同号和统号为必填项，备入字段可选",
  "拍照时请确保光线充足，照片清晰可辨",
  "上传成功后可在「福建文档管理」中查看和下载",
  "建议使用PC端Chrome或Firefox浏览器获得最佳体验"
];

notes.forEach(note => {
  children.push(
    new Paragraph({
      children: [new TextRun({ text: `• ${note}`, size: 22 })],
      spacing: { after: 100 }
    })
  );
});

// 创建文档
const doc = new Document({
  sections: [{
    properties: {},
    children: children
  }]
});

// 保存文档
Packer.toBuffer(doc).then(buffer => {
  const outputPath = CONFIG.outputPath;
  fs.writeFileSync(outputPath, buffer);
  console.log(`\n文档已生成: ${outputPath}`);
}).catch(err => {
  console.error('生成文档失败:', err);
});

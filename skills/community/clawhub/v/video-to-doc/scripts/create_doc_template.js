/**
 * 视频转图文文档生成模板
 * 
 * 使用方法：
 * 1. 修改顶部的配置项
 * 2. 根据实际截图内容修改步骤描述
 * 3. 运行：node create_doc_template.js
 */

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, 
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType, 
        ShadingType, LevelFormat, PageNumber } = require('docx');
const fs = require('fs');

// ==================== 配置项 ====================
const CONFIG = {
  // 文档标题
  title: "操作指南",
  
  // 截图目录（相对于脚本所在目录）
  framesDir: "./frames",
  
  // 截图文件名列表（不含扩展名）
  frameFiles: ['frame_01', 'frame_02', 'frame_03', 'frame_04', 'frame_05', 'frame_06'],
  
  // 输出文件名
  outputName: "操作指南.docx",
  
  // 图片显示尺寸
  imageWidth: 500,
  imageHeight: 268
};

// ==================== 内容定义 ====================

/**
 * 操作步骤定义
 * 格式：{ title, description, imageFile, imageCaption, bullets }
 */
const STEPS = [
  {
    title: "步骤1：进入系统",
    description: "登录系统后，点击导航栏进入目标模块。",
    imageFile: "frame_01",
    imageCaption: "图1：系统界面",
    bullets: [
      { label: "操作说明：", content: "点击对应菜单项" }
    ]
  },
  {
    title: "步骤2：新建记录",
    description: "点击「新增」按钮，创建新记录。",
    imageFile: "frame_02",
    imageCaption: "图2：新建界面",
    bullets: []
  }
  // ... 添加更多步骤
];

/**
 * 系统信息表格（可选）
 */
const SYSTEM_INFO = [
  { field: "系统名称", value: "XXX系统" },
  { field: "功能模块", value: "XXX模块" }
];

/**
 * 注意事项列表
 */
const NOTES = [
  "注意保存操作",
  "确认数据准确性"
];

/**
 * 关键字段说明表格（可选）
 */
const FIELDS = [
  { name: "字段1", desc: "说明", example: "示例" },
  { name: "字段2", desc: "说明", example: "示例" }
];

// ==================== 文档生成代码 ====================

// 表格边框样式
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

// 读取图片
function loadImages() {
  const images = {};
  CONFIG.frameFiles.forEach(f => {
    const path = `${CONFIG.framesDir}/${f}.jpg`;
    if (fs.existsSync(path)) {
      images[f] = fs.readFileSync(path);
    }
  });
  return images;
}

// 创建系统信息表格
function createInfoTable(info) {
  return new Table({
    columnWidths: [3000, 6360],
    rows: info.map(item => new TableRow({
      children: [
        new TableCell({ 
          borders: cellBorders, 
          width: { size: 3000, type: WidthType.DXA }, 
          shading: { fill: "E7F3FF", type: ShadingType.CLEAR },
          children: [new Paragraph({ children: [new TextRun({ text: item.field, bold: true })] })] 
        }),
        new TableCell({ 
          borders: cellBorders, 
          width: { size: 6360, type: WidthType.DXA },
          children: [new Paragraph({ children: [new TextRun(item.value)] })] 
        })
      ]
    }))
  });
}

// 创建步骤段落
function createStepParagraphs(step, images, bulletRef) {
  const paragraphs = [
    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(step.title)] }),
    new Paragraph({ children: [new TextRun(step.description)] })
  ];
  
  // 添加要点列表
  step.bullets.forEach(b => {
    paragraphs.push(new Paragraph({ 
      numbering: { reference: bulletRef, level: 0 }, 
      children: [new TextRun({ text: b.label, bold: true }), new TextRun(b.content)] 
    }));
  });
  
  // 添加图片
  if (step.imageFile && images[step.imageFile]) {
    paragraphs.push(new Paragraph({ 
      alignment: AlignmentType.CENTER, 
      spacing: { before: 200, after: 200 },
      children: [new ImageRun({ 
        type: "jpg", 
        data: images[step.imageFile], 
        transformation: { width: CONFIG.imageWidth, height: CONFIG.imageHeight },
        altText: { title: step.title, description: step.imageCaption, name: step.imageFile }
      })] 
    }));
    paragraphs.push(new Paragraph({ 
      alignment: AlignmentType.CENTER, 
      children: [new TextRun({ text: step.imageCaption, size: 20, color: "666666", italics: true })] 
    }));
  }
  
  return paragraphs;
}

// 创建字段表格
function createFieldsTable(fields) {
  return new Table({
    columnWidths: [2500, 3500, 3360],
    rows: [
      // 表头
      new TableRow({ tableHeader: true, children: ['字段名称', '说明', '示例值'].map(text => 
        new TableCell({ 
          borders: cellBorders, 
          shading: { fill: "2E75B6", type: ShadingType.CLEAR },
          children: [new Paragraph({ 
            alignment: AlignmentType.CENTER, 
            children: [new TextRun({ text, bold: true, color: "FFFFFF" })] 
          })] 
        })
      )}),
      // 数据行
      ...fields.map(f => new TableRow({
        children: [
          new TableCell({ borders: cellBorders, children: [new Paragraph({ children: [new TextRun(f.name)] })] }),
          new TableCell({ borders: cellBorders, children: [new Paragraph({ children: [new TextRun(f.desc)] })] }),
          new TableCell({ borders: cellBorders, children: [new Paragraph({ children: [new TextRun(f.example)] })] })
        ]
      }))
    ]
  });
}

// 主函数
function main() {
  const images = loadImages();
  
  // 构建文档内容
  const children = [
    // 标题
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun(CONFIG.title)] }),
    
    // 概述
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("一、操作概述")] }),
    new Paragraph({ children: [new TextRun("本文档介绍相关操作流程。")] })
  ];
  
  // 系统信息（如有）
  if (SYSTEM_INFO.length > 0) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("二、系统信息")] }));
    children.push(createInfoTable(SYSTEM_INFO));
  }
  
  // 操作步骤
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("三、操作步骤详解")] }));
  STEPS.forEach(step => {
    children.push(...createStepParagraphs(step, images, "bullet-list"));
  });
  
  // 注意事项
  if (NOTES.length > 0) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("四、注意事项")] }));
    NOTES.forEach((note, i) => {
      children.push(new Paragraph({ 
        numbering: { reference: "step-list", level: 0 }, 
        children: [new TextRun(note)] 
      }));
    });
  }
  
  // 字段说明（如有）
  if (FIELDS.length > 0) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("五、关键字段说明")] }));
    children.push(createFieldsTable(FIELDS));
  }
  
  // 创建文档
  const doc = new Document({
    styles: {
      default: { document: { run: { font: "微软雅黑", size: 24 } } },
      paragraphStyles: [
        { id: "Title", name: "Title", basedOn: "Normal",
          run: { size: 48, bold: true, color: "1F4E79", font: "微软雅黑" },
          paragraph: { spacing: { before: 240, after: 360 }, alignment: AlignmentType.CENTER } },
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 32, bold: true, color: "2E75B6", font: "微软雅黑" },
          paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, color: "5B9BD5", font: "微软雅黑" },
          paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } }
      ]
    },
    numbering: {
      config: [
        { reference: "step-list",
          levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
        { reference: "bullet-list",
          levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
      ]
    },
    sections: [{
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      headers: {
        default: new Header({ children: [new Paragraph({ 
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "操作指南", size: 20, color: "808080" })]
        })] })
      },
      footers: {
        default: new Footer({ children: [new Paragraph({ 
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "第 ", size: 20 }), new TextRun({ children: [PageNumber.CURRENT], size: 20 }), 
                     new TextRun({ text: " 页", size: 20 })]
        })] })
      },
      children
    }]
  });
  
  // 生成文档
  Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(CONFIG.outputName, buffer);
    console.log(`文档生成成功：${CONFIG.outputName}`);
  });
}

main();

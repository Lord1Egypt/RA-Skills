/**
 * shiwei-diagnosis PPT 生成脚本（参考实现）
 * 
 * ⚠️ 本文件是德施曼项目的参考实现，使用时需要按实际诊断MD文档改写内容。
 * 
 * 通用化方法：
 *   1. 读取诊断MD文档，解析各部分内容
 *   2. 按 references/ppt-structure.md 定义的结构生成幻灯片
 *   3. 内容部分（slides数组）需要从MD中提取，而非硬编码
 * 
 * 使用方法：
 *   node generate_ppt.js <diagnosis.md路径> <输出.pptx路径>
 * 
 * 依赖：npm install pptxgenjs
 */

const pptxgen = require("pptxgenjs");

// ========== COLOR PALETTE ==========
const C = {
  navy: "1B2A4A",
  navyLight: "2E4A6B",
  gold: "C8963E",
  goldLight: "E8D5B0",
  bg: "F5F6FA",
  white: "FFFFFF",
  text: "1B2A4A",
  textMuted: "5A6C7D",
  textLight: "6C7A96",
  red: "C0392B",
  redLight: "FADBD8",
  blue: "2E86C1",
  blueLight: "D6EAF8",
  green: "27AE60",
  greenLight: "D5F5E3",
  cardBg: "FFFFFF",
  line: "D5DCE6",
  orange: "E67E22",
  orangeLight: "FAD7A0",
};

// ========== HELPERS ==========
function makeShadow() {
  return { type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.08 };
}

function makeCardShadow() {
  return { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.1 };
}

function addSlideNumber(slide, num) {
  slide.addText(String(num), {
    x: 9.2, y: 5.2, w: 0.6, h: 0.3,
    fontSize: 9, color: C.textLight, align: "center", fontFace: "Calibri",
  });
}

function addSectionHeader(slide, sectionName) {
  slide.addShape(slide._slideLayout ? undefined : "rect", {});
  // Footer bar
  slide.addShape("rect", {
    x: 0, y: 5.25, w: 10, h: 0.375,
    fill: { color: C.navy },
  });
  slide.addText(sectionName, {
    x: 0.5, y: 5.25, w: 9, h: 0.375,
    fontSize: 9, color: C.white, fontFace: "Calibri", margin: 0,
  });
}

function addFooter(slide, text) {
  slide.addShape("rect", {
    x: 0, y: 5.25, w: 10, h: 0.375,
    fill: { color: C.navy },
  });
  slide.addText(text, {
    x: 0.5, y: 5.25, w: 9, h: 0.375,
    fontSize: 8, color: C.white, fontFace: "Calibri", margin: 0,
  });
}

function addGoldAccent(slide, x, y, w) {
  // Horizontal gold bar under title — wide and thin
  slide.addShape("rect", {
    x: x, y: y, w: w || 1.2, h: 0.04,
    fill: { color: C.gold },
  });
}

function addCard(slide, x, y, w, h) {
  slide.addShape("rect", {
    x, y, w, h,
    fill: { color: C.cardBg },
    shadow: makeCardShadow(),
    rectRadius: 0,
  });
}

function addQuoteBox(slide, x, y, w, h, textArr) {
  // Left accent bar
  slide.addShape("rect", {
    x: x, y: y, w: 0.05, h: h,
    fill: { color: C.gold },
  });
  slide.addShape("rect", {
    x: x + 0.05, y: y, w: w - 0.05, h: h,
    fill: { color: C.bg },
    shadow: makeShadow(),
  });
  slide.addText(textArr, {
    x: x + 0.25, y: y + 0.1, w: w - 0.45, h: h - 0.2,
    fontSize: 10, color: C.textMuted, fontFace: "Calibri", italic: true,
    valign: "middle", margin: 0,
  });
}

function addDiagnosisBox(slide, x, y, w, h, text) {
  slide.addShape("rect", {
    x, y, w, h,
    fill: { color: C.redLight },
    shadow: makeShadow(),
  });
  slide.addText(text, {
    x: x + 0.2, y: y + 0.1, w: w - 0.4, h: h - 0.2,
    fontSize: 11, color: C.red, fontFace: "Calibri", bold: true,
    valign: "middle", margin: 0,
  });
}

// Draw a proper arrow shape between two points (from left to right, or custom via rotation)
function addArrowShape(slide, x, y, w, h, color, rotation) {
  slide.addShape("rightArrow", {
    x, y, w, h,
    fill: { color: color || C.gold },
    line: { type: "none" },
    rotate: rotation || 0,
  });
}

// Draw a vertical arrow (downward) using a triangle shape
function addDownArrow(slide, x, y, w, h, color) {
  slide.addShape("downArrow", {
    x, y, w, h,
    fill: { color: color || C.gold },
    line: { type: "none" },
  });
}

// ========== PRESENTATION ==========
async function generate() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "华夏基石管理咨询集团";
  pres.title = "德施曼企业管理咨询诊断报告";

  let slideNum = 0;
  const SN = () => { slideNum++; return slideNum; };

  // ============================================================
  // COVER
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    // Gold line at top
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.gold } });
    // Logo area
    s.addText("德施曼", {
      x: 0.8, y: 1.0, w: 8.4, h: 0.6,
      fontSize: 18, color: C.gold, fontFace: "Calibri", charSpacing: 8,
      align: "center", margin: 0,
    });
    // Title
    s.addText("企业管理咨询诊断报告", {
      x: 0.8, y: 1.7, w: 8.4, h: 1.2,
      fontSize: 36, color: C.white, fontFace: "Calibri", bold: true,
      align: "center", margin: 0,
    });
    // Separator line
    s.addShape("rect", { x: 3.5, y: 3.1, w: 3, h: 0.02, fill: { color: C.gold } });
    // Subtitle
    s.addText("报告版本：讨论版  |  2026年6月", {
      x: 0.8, y: 3.4, w: 8.4, h: 0.5,
      fontSize: 14, color: C.textLight, fontFace: "Calibri",
      align: "center", margin: 0,
    });
    // Bottom
    s.addText("华夏基石管理咨询集团", {
      x: 0.8, y: 4.6, w: 8.4, h: 0.4,
      fontSize: 12, color: C.gold, fontFace: "Calibri",
      align: "center", margin: 0,
    });
    s.addText("加速成长 · 智启未来", {
      x: 0.8, y: 5.0, w: 8.4, h: 0.3,
      fontSize: 9, color: C.textLight, fontFace: "Calibri",
      align: "center", margin: 0,
    });
  }

  // ============================================================
  // TOC
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    s.addText("目  录", {
      x: 0.8, y: 0.5, w: 8.4, h: 0.7,
      fontSize: 28, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.8, 1.3);

    const parts = [
      { num: "01", title: "前言：项目说明", desc: "资料分析 · 深度访谈 · 问卷调研" },
      { num: "02", title: "第一部分：历史回顾和成功经验", desc: "发展回顾 · 关键成功要素 · 文化归因" },
      { num: "03", title: "第二部分：现实问题和成长制约", desc: "问题表征 · 一心开二门诊断 · 三大矛盾" },
      { num: "04", title: "第三部分：战略性课题与变革建议", desc: "基本判断 · 转型方向 · 跃迁蓝图" },
    ];

    parts.forEach((p, i) => {
      const y = 1.7 + i * 0.85;
      s.addShape("rect", {
        x: 0.8, y: y, w: 0.7, h: 0.65,
        fill: { color: C.navy },
      });
      s.addText(p.num, {
        x: 0.8, y: y, w: 0.7, h: 0.65,
        fontSize: 22, color: C.gold, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(p.title, {
        x: 1.8, y: y, w: 7, h: 0.35,
        fontSize: 15, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(p.desc, {
        x: 1.8, y: y + 0.35, w: 7, h: 0.3,
        fontSize: 10, color: C.textMuted, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, "德施曼企业管理咨询诊断报告  |  华夏基石管理咨询集团");
  }

  // ============================================================
  // PREFACE
  // ============================================================
  // Section divider
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.gold } });
    s.addText("前  言", {
      x: 0.8, y: 1.8, w: 8.4, h: 0.8,
      fontSize: 42, color: C.white, fontFace: "Calibri", bold: true,
      align: "center", margin: 0,
    });
    s.addText("项目说明", {
      x: 0.8, y: 2.7, w: 8.4, h: 0.5,
      fontSize: 18, color: C.gold, fontFace: "Calibri",
      align: "center", margin: 0,
    });
  }

  // P1: Project Overview
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("项目总览", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // Two phase boxes
    const phases = [
      { title: "第一阶段：调研诊断", items: ["资料分析", "深度访谈", "问卷调研", "诊断报告", "汇报研讨"] },
      { title: "第二阶段：战略梳理（待启动）", items: ["外部环境分析", "战略方向研讨", "战略规划制定", "战略解码落地"] },
    ];

    phases.forEach((ph, i) => {
      const x = 0.6 + i * 4.5;
      addCard(s, x, 1.3, 4.1, 2.6);
      s.addShape("rect", {
        x: x, y: 1.3, w: 4.1, h: 0.5,
        fill: { color: C.navy },
      });
      s.addText(ph.title, {
        x: x + 0.2, y: 1.3, w: 3.7, h: 0.5,
        fontSize: 13, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
      });

      ph.items.forEach((item, j) => {
        s.addShape("oval", {
          x: x + 0.4, y: 2.0 + j * 0.4, w: 0.22, h: 0.22,
          fill: { color: C.gold },
        });
        s.addText(String(j + 1), {
          x: x + 0.4, y: 2.0 + j * 0.4, w: 0.22, h: 0.22,
          fontSize: 9, color: C.white, fontFace: "Calibri", bold: true,
          align: "center", valign: "middle", margin: 0,
        });
        s.addText(item, {
          x: x + 0.8, y: 2.0 + j * 0.4, w: 2.8, h: 0.22,
          fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
        });
      });
    });

    addFooter(s, "德施曼企业管理咨询诊断报告  |  前言");
  }

  // P2: 资料分析
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("资料分析", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const docs = [
      { title: "公司发展历程及大事记", desc: "了解企业创立至今的关键节点和里程碑事件" },
      { title: "（2024~2026）发展战略规划", desc: "理解公司三年战略意图、目标和资源配置方向" },
      { title: "五月份月度经营会议纪要", desc: "把握当前经营态势、策略调整和关键挑战" },
      { title: "组织架构图及部门详细拆分", desc: "呈现正式组织架构、岗位编制和职能分工" },
      { title: "2025年度人力资源数据", desc: "分析人才结构、流动率、薪酬竞争力等关键指标" },
      { title: "智能锁行业文献及市场数据", desc: "建立行业参照系，理解竞争格局和发展趋势" },
    ];

    docs.forEach((d, i) => {
      const y = 1.3 + i * 0.63;
      s.addShape("rect", {
        x: 0.6, y: y, w: 0.08, h: 0.45,
        fill: { color: C.gold },
      });
      s.addText(d.title, {
        x: 0.9, y: y, w: 4, h: 0.45,
        fontSize: 12, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(d.desc, {
        x: 5, y: y, w: 4.5, h: 0.45,
        fontSize: 10, color: C.textMuted, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, "德施曼企业管理咨询诊断报告  |  前言");
  }

  // P3: 深度访谈
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("深度访谈", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // Interview stats
    s.addShape("rect", {
      x: 0.6, y: 1.3, w: 3.2, h: 1.2,
      fill: { color: C.navy },
    });
    s.addText("16", {
      x: 0.6, y: 1.3, w: 1.5, h: 1.2,
      fontSize: 48, color: C.gold, fontFace: "Calibri", bold: true,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText("中高层管理人员\n一对一深度访谈", {
      x: 2.1, y: 1.3, w: 1.7, h: 1.2,
      fontSize: 13, color: C.white, fontFace: "Calibri", valign: "middle", margin: 0,
    });

    const depts = [
      { name: "高层", detail: "月度经营会议参与观察" },
      { name: "研发端", detail: "电子研发、结构研发、项目管理 — 4人" },
      { name: "产品端", detail: "产品规划、渠道管理、开发流程" },
      { name: "销售端", detail: "线下零售、工程、龙庭品牌、东西南北战区" },
      { name: "电商端", detail: "京东/天猫运营、信息化建设" },
      { name: "新业务", detail: "摄像头业务（含离职）、创新增长/抖音" },
    ];

    depts.forEach((d, i) => {
      const y = 1.3 + i * 0.62;
      const x = 4.2;
      s.addShape("rect", {
        x: x, y: y, w: 0.65, h: 0.45,
        fill: { color: C.goldLight },
      });
      s.addText(d.name, {
        x: x, y: y, w: 0.65, h: 0.45,
        fontSize: 9, color: C.navy, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(d.detail, {
        x: x + 0.75, y: y, w: 4.5, h: 0.45,
        fontSize: 10, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, "德施曼企业管理咨询诊断报告  |  前言");
  }

  // P4: 诊断框架
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("诊断方法论", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // 三层分析法 — compact
    addCard(s, 0.6, 1.3, 4.1, 2.6);
    s.addShape("rect", { x: 0.6, y: 1.3, w: 4.1, h: 0.48, fill: { color: C.navy } });
    s.addText("问题根因三层分析法", {
      x: 0.8, y: 1.3, w: 3.7, h: 0.48,
      fontSize: 13, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    const layers = [
      { label: "What", desc: "经营表征：财务/竞争压力" },
      { label: "How", desc: "具体现象：战略/组织/人才/文化" },
      { label: "Why", desc: "深层根因：三大基本矛盾" },
    ];

    layers.forEach((l, i) => {
      const y = 1.95 + i * 0.65;
      s.addShape("rect", {
        x: 0.8, y: y, w: 0.55, h: 0.5,
        fill: { color: C.gold },
      });
      s.addText(l.label, {
        x: 0.8, y: y, w: 0.55, h: 0.5,
        fontSize: 10, color: C.white, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(l.desc, {
        x: 1.5, y: y, w: 3.0, h: 0.5,
        fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
      });
      if (i < 2) {
        s.addShape("downArrow", {
          x: 1.05, y: y + 0.48, w: 0.18, h: 0.16,
          fill: { color: C.gold },
        });
      }
    });

    // 一心开二门 — compact
    addCard(s, 5.1, 1.3, 4.3, 2.6);
    s.addShape("rect", { x: 5.1, y: 1.3, w: 4.3, h: 0.45, fill: { color: C.navy } });
    s.addText("「一心开二门」诊断框架", {
      x: 5.3, y: 1.3, w: 3.9, h: 0.45,
      fontSize: 13, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    // 一心 — compact position
    s.addShape("oval", {
      x: 6.55, y: 1.9, w: 1.35, h: 0.6,
      fill: { color: C.gold },
    });
    s.addText("企业家心智\n企业文化", {
      x: 6.55, y: 1.9, w: 1.35, h: 0.6,
      fontSize: 9, color: C.white, fontFace: "Calibri", bold: true,
      align: "center", valign: "middle", margin: 0,
    });

    // 战略之门 — moved up
    s.addShape("rect", {
      x: 5.3, y: 2.6, w: 3.9, h: 0.6,
      fill: { color: C.blueLight },
    });
    s.addText("战略之门  ·  机会洞察 · 价值创造 · 资源整合", {
      x: 5.3, y: 2.6, w: 3.9, h: 0.6,
      fontSize: 10, color: C.navy, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0,
    });

    // 组织之门 — moved up
    s.addShape("rect", {
      x: 5.3, y: 3.3, w: 3.9, h: 0.6,
      fill: { color: C.greenLight },
    });
    s.addText("组织之门  ·  架构流程 · 团队建设 · 企业文化", {
      x: 5.3, y: 3.3, w: 3.9, h: 0.6,
      fontSize: 10, color: C.navy, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0,
    });

    // Arrow from 一心 to doors — use shape
    s.addShape("downArrow", {
      x: 7.1, y: 2.52, w: 0.22, h: 0.18,
      fill: { color: C.gold },
    });

    addFooter(s, "德施曼企业管理咨询诊断报告  |  前言");
  }

  // ============================================================
  // PART 1: 历史回顾和成功经验
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.gold } });
    s.addText("第一部分", {
      x: 0.8, y: 1.8, w: 8.4, h: 0.8,
      fontSize: 42, color: C.white, fontFace: "Calibri", bold: true,
      align: "center", margin: 0,
    });
    s.addText("历史回顾和成功经验", {
      x: 0.8, y: 2.7, w: 8.4, h: 0.5,
      fontSize: 18, color: C.gold, fontFace: "Calibri",
      align: "center", margin: 0,
    });
  }

  const part1Section = "德施曼企业管理咨询诊断报告  |  第一部分：历史回顾和成功经验";

  // A1: 行业背景
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1.1 行业背景：中国智能锁行业发展历程", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const stages = [
      { period: "2010-2015", title: "导入期", features: "酒店/工程市场为主\nC端认知度极低" },
      { period: "2016-2020", title: "爆发期", features: "小米生态链入局\n线上成主战场\n年复合增长超50%" },
      { period: "2021-至今", title: "洗牌期", features: "增速放缓至10-20%\n2025年行业下滑超20%\n价格战白热化" },
    ];

    stages.forEach((st, i) => {
      const x = 0.6 + i * 3.15;
      addCard(s, x, 1.3, 2.85, 2.4);
      s.addShape("rect", { x: x, y: 1.3, w: 2.85, h: 0.55, fill: { color: C.navy } });
      s.addText(st.period, {
        x: x + 0.15, y: 1.32, w: 2.55, h: 0.25,
        fontSize: 10, color: C.gold, fontFace: "Calibri", margin: 0,
      });
      s.addText(st.title, {
        x: x + 0.15, y: 1.55, w: 2.55, h: 0.28,
        fontSize: 15, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(st.features, {
        x: x + 0.15, y: 1.95, w: 2.55, h: 1.6,
        fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0, valign: "top",
      });
      // Arrow between stages — use rightArrow shape
      if (i < 2) {
        s.addShape("rightArrow", {
          x: x + 2.88, y: 2.2, w: 0.25, h: 0.22,
          fill: { color: C.gold },
        });
      }
    });

    // Bottom note
    s.addText("德施曼跨越了全部三个阶段——从拓荒者，到红利收割者，再到守成者。每一次环境变迁都在考验企业的进化能力。", {
      x: 0.6, y: 3.9, w: 8.8, h: 0.45,
      fontSize: 10, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
    });

    addFooter(s, part1Section);
  }

  // A2: 企业成长阶段
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1.2 德施曼企业成长阶段", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const stages = [
      { period: "2009-2014", title: "创业探索期", desc: "德国技术背景切入\n主打工程渠道\n年销售千万级\n验证产品和商业模式" },
      { period: "2015-2019", title: "机会成长期", desc: "抓住C端爆发机遇\n线上占比70-80%\n营收跃升至数亿\n\"市场拉动型增长\"" },
      { period: "2020-2024", title: "系统成长期早期", desc: "尝试组织化升级\n引入职业经理人\n多品牌布局\n战略意图与执行出现落差" },
      { period: "2025-至今", title: "调整期", desc: "行业下滑20%+\n进攻→稳健\n新业务战略重新审视" },
    ];

    stages.forEach((st, i) => {
      const x = 0.4 + i * 2.4;
      // Timeline line
      s.addShape("rect", { x: 0.4, y: 1.5, w: 9.2, h: 0.03, fill: { color: C.line } });
      // Dot
      s.addShape("oval", {
        x: x + 0.95, y: 1.35, w: 0.3, h: 0.3,
        fill: { color: C.gold },
      });
      // Card — compact height
      addCard(s, x, 1.8, 2.1, 2.3);
      s.addShape("rect", { x: x, y: 1.8, w: 2.1, h: 0.48, fill: { color: C.navy } });
      s.addText(st.period, {
        x: x + 0.1, y: 1.82, w: 1.9, h: 0.18,
        fontSize: 8, color: C.gold, fontFace: "Calibri", margin: 0,
      });
      s.addText(st.title, {
        x: x + 0.1, y: 2.0, w: 1.9, h: 0.28,
        fontSize: 12, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(st.desc, {
        x: x + 0.1, y: 2.35, w: 1.9, h: 1.6,
        fontSize: 9.5, color: C.text, fontFace: "Calibri", margin: 0, valign: "top",
      });
    });

    // Stage anchor box
    addDiagnosisBox(s, 0.6, 4.25, 8.8, 0.4,
      "阶段锚定：当前处于机会成长→系统成长跨越期。规模到了中大型企门槛，但治理方式和组织能力仍停留在机会成长期。"
    );

    addFooter(s, part1Section);
  }

  // A3: 主要成就-业务与品牌
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1.3 主要成就：业务发展与品牌建设", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // Business achievements — compact
    addCard(s, 0.6, 1.3, 4.2, 2.5);
    s.addShape("rect", { x: 0.6, y: 1.3, w: 4.2, h: 0.42, fill: { color: C.navy } });
    s.addText("业务发展", {
      x: 0.8, y: 1.3, w: 3.8, h: 0.42,
      fontSize: 14, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    const bizItems = [
      "从千万级营收到数亿级，在智能锁行业建立了稳固的市场地位",
      "线上渠道（京东+天猫）占据销售70-80%",
      "京东渠道份额约55%",
      "东部战区年销1.5-1.6亿，占总营收约33%",
    ];
    bizItems.forEach((item, i) => {
      s.addText([
        { text: `0${i+1}`, options: { bold: true, color: C.gold, fontSize: 11 } },
        { text: `  ${item}`, options: { fontSize: 10, color: C.text } },
      ], {
        x: 0.8, y: 1.85 + i * 0.45, w: 3.8, h: 0.4,
        fontFace: "Calibri", margin: 0,
      });
    });

    // Brand achievements — compact
    addCard(s, 5.2, 1.3, 4.2, 2.5);
    s.addShape("rect", { x: 5.2, y: 1.3, w: 4.2, h: 0.42, fill: { color: C.navy } });
    s.addText("品牌建设", {
      x: 5.4, y: 1.3, w: 3.8, h: 0.42,
      fontSize: 14, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    const brandItems = [
      "\"德系品质\"品牌定位深入人心，中高端差异化认知稳固",
      "龙庭品牌作为第二品牌，尝试覆盖不同客群",
      "抖音直播等新营销渠道实现了从零到一的突破",
      "在1000-3000元中高端价格段与小米/凯迪仕形成差异化竞争",
    ];
    brandItems.forEach((item, i) => {
      s.addText([
        { text: `0${i+1}`, options: { bold: true, color: C.gold, fontSize: 11 } },
        { text: `  ${item}`, options: { fontSize: 10, color: C.text } },
      ], {
        x: 5.4, y: 1.85 + i * 0.45, w: 3.8, h: 0.4,
        fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part1Section);
  }

  // A4: 主要成就-产品与渠道
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1.3 主要成就：产品覆盖与渠道布局", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    addCard(s, 0.6, 1.3, 4.2, 2.5);
    s.addShape("rect", { x: 0.6, y: 1.3, w: 4.2, h: 0.42, fill: { color: C.navy } });
    s.addText("产品覆盖", {
      x: 0.8, y: 1.3, w: 3.8, h: 0.42,
      fontSize: 14, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    const prodItems = [
      "形成了覆盖不同价格段和场景的四大产品系列",
      "核心技术积累：指纹识别、人脸识别、远程控制等",
      "快速跟随能力：人脸/指静脉/猫眼监控等新技术快速导入",
      "系列化覆盖：入门款到旗舰款完整产品矩阵",
    ];
    prodItems.forEach((item, i) => {
      s.addText([
        { text: `0${i+1}`, options: { bold: true, color: C.gold, fontSize: 11 } },
        { text: `  ${item}`, options: { fontSize: 10, color: C.text } },
      ], {
        x: 0.8, y: 1.85 + i * 0.45, w: 3.8, h: 0.4,
        fontFace: "Calibri", margin: 0,
      });
    });

    addCard(s, 5.2, 1.3, 4.2, 2.5);
    s.addShape("rect", { x: 5.2, y: 1.3, w: 4.2, h: 0.42, fill: { color: C.navy } });
    s.addText("渠道布局", {
      x: 5.4, y: 1.3, w: 3.8, h: 0.42,
      fontSize: 14, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    const chanItems = [
      "线上渠道运营成熟，京东/天猫有系统性方法论",
      "线下战区制初步成型，东西南北战区各自建立网络",
      "AI客服等数字化工具投入，客服效率提升",
      "线上直营模式天然具有更高毛利率和更低渠道成本",
    ];
    chanItems.forEach((item, i) => {
      s.addText([
        { text: `0${i+1}`, options: { bold: true, color: C.gold, fontSize: 11 } },
        { text: `  ${item}`, options: { fontSize: 10, color: C.text } },
      ], {
        x: 5.4, y: 1.85 + i * 0.45, w: 3.8, h: 0.4,
        fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part1Section);
  }

  // B1: 赢的逻辑七维总览（与MD七维分析严格对齐）
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2. 关键成功要素：「赢的逻辑」七维框架", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const dims = [
      { label: "赢在赛道", sub: "高端智能锁" },
      { label: "赢在空间", sub: "中高端+蓝海" },
      { label: "赢在价值", sub: "安全+技术" },
      { label: "赢在模式", sub: "全域+研发" },
      { label: "赢在胜点", sub: "五维优势" },
      { label: "赢在节奏", sub: "三节点把控" },
      { label: "赢在能力", sub: "五维能力" },
    ];
    dims.forEach((d, i) => {
      const x = 0.45 + i * 1.32;
      s.addShape("rect", {
        x: x, y: 1.25, w: 1.2, h: 0.65,
        fill: { color: C.navy },
        line: { color: C.gold, width: 0.5 },
      });
      s.addText(d.label, {
        x: x, y: 1.27, w: 1.2, h: 0.35,
        fontSize: 9, color: C.white, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(d.sub, {
        x: x, y: 1.58, w: 1.2, h: 0.28,
        fontSize: 7, color: C.gold, fontFace: "Calibri",
        align: "center", valign: "middle", margin: 0,
      });
      if (i < 6) {
        s.addShape("rightArrow", {
          x: x + 1.2 + 0.005, y: 1.38, w: 0.12, h: 0.3,
          fill: { color: C.gold }, line: { type: "none" },
        });
      }
    });

    // 七维详细解读（与MD重写后对齐）
    const factors = [
      { num: "①", title: "赢在赛道", desc: "精准卡位高端智能锁赛道，避开红海，享受行业爆发红利（2009年布局，渗透率<1%）" },
      { num: "②", title: "赢在空间", desc: "独占高端心智品类，规避价格战，锚定2000元以上高价值市场，聚焦核心主业" },
      { num: "③", title: "赢在价值", desc: "构建\"安全+技术\"差异化价值体系，创始人认知先行，技术赋能溢价，全域高效交付" },
      { num: "④", title: "赢在模式", desc: "CEO高效决策+全域渠道+研发驱动+极致营销，支撑高端赛道可持续增长" },
      { num: "⑤", title: "赢在胜点", desc: "定位+品牌+产品+渠道+决策五维优势系统性叠加，构建全方位竞争壁垒" },
      { num: "⑥", title: "赢在节奏", desc: "前期不跟风（坚守高端）、中期抢跑（抢占线上红利）、长期不停步（巩固优势）" },
      { num: "⑦", title: "赢在能力", desc: "市场洞察+快速决策+营销执行+产品创新+全域渠道五维能力，构筑不可复制的竞争底盘" },
    ];

    factors.forEach((f, i) => {
      const y = 2.05 + i * 0.42;
      s.addShape("rect", {
        x: 0.6, y: y, w: 0.35, h: 0.35,
        fill: { color: C.gold },
        line: { color: C.navy, width: 0.5 },
      });
      s.addText(f.num, {
        x: 0.6, y: y, w: 0.35, h: 0.35,
        fontSize: 10, color: C.white, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(f.title, {
        x: 1.05, y: y, w: 1.45, h: 0.35,
        fontSize: 10.5, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(f.desc, {
        x: 2.6, y: y, w: 6.8, h: 0.35,
        fontSize: 9, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part1Section);
  }

  // B2-B8: 七维成功要素详情（与七维总览页严格对齐）
  const successFactors = [
    {
      num: "①", title: "赢在赛道：精准卡位高端智能锁蓝海",
      points: [
        "行业渗透率不到1%时即布局（2009年），享受完整行业成长周期",
        "避开千元以下低端红海，聚焦2000元以上高端智能锁赛道",
        "智能锁作为智能家居核心入口，具备持续扩容的长期成长空间",
        "技术密集型品类，全产业链高门槛构筑难以复制的行业壁垒",
      ],
      conclusion: "赛道选择是战略的起点。德施曼的成功首先源于在行业萌芽期对\"高端智能锁\"这一优质细分赛道的精准卡位。",
    },
    {
      num: "②", title: "赢在空间：开辟高价值生存与增长空间",
      points: [
        "独占\"高端智能锁\"心智品类，形成\"高端智能锁=德施曼\"的垄断认知",
        "精准锚定2000元以上高价值市场，规避千元价格战红海内卷",
        "聚焦注重安全、追求品质、对价格不敏感的中高端客群",
        "高度聚焦智能锁核心主业，不盲目多元化，做深做透单一赛道",
      ],
      conclusion: "\"赢在空间\"的本质是在红海竞争中找到属于自己的高价值生存空间，并在这个空间里做到极致。",
    },
    {
      num: "③", title: "赢在价值：构建\"安全+技术\"差异化价值体系",
      points: [
        "创始人精准预判行业终局：终极竞争是核心安全能力而非价格",
        "确立\"高端智能锁，技术领先\"核心价值主张，与性价比品牌彻底区隔",
        "哨兵猫眼、GPT指纹算法等核心技术支撑高端溢价",
        "线上线下一体化全域渠道，高效一致传递品牌高端价值",
      ],
      conclusion: "价值主张是品牌的灵魂。德施曼的成功在于跳出了价格竞争，构建了以\"安全、技术\"为核心的差异化价值体系。",
    },
    {
      num: "④", title: "赢在模式：适配高端赛道的商业化运营体系",
      points: [
        "CEO核心驱动决策机制，组织层级精简，市场响应速度极快",
        "构建\"线下深耕+线上赋能\"立体化全域渠道体系，全面覆盖消费场景",
        "技术研发作为商业模式核心支撑，形成\"技术创新→产品升级→高端溢价→研发再投入\"良性循环",
        "饱和式品牌传播+精准化客群触达+全域化渠道渗透，持续固化\"高端智能锁\"品牌心智",
      ],
      conclusion: "商业模式是价值的 Delivery 系统。德施曼围绕\"高端智能锁\"定位，搭建了一套适配赛道的商业化运营模式。",
    },
    {
      num: "⑤", title: "赢在胜点：五维优势系统性叠加",
      points: [
        "胜在定位：率先完成高端定位占位，形成独一无二的市场定位优势",
        "胜在品牌：\"高端智能锁\"标杆代名词，拥有强大品牌溢价能力与用户心智优势",
        "胜在产品：哨兵猫眼、GPT指纹算法等独家核心技术，以硬核产品实力支撑高端溢价",
        "胜在渠道：线上线下全域覆盖的立体渠道网络，为销量增长与品牌下沉提供强力支撑",
        "胜在决策：CEO驱动的快速决策机制，精准捕捉行业趋势，快速调整经营策略",
      ],
      conclusion: "\"赢在胜点\"的本质是多重核心优势的系统性叠加，从定位、品牌、产品、渠道到决策形成全方位竞争壁垒。",
    },
    {
      num: "⑥", title: "赢在节奏：经营企业能力建设与市场规模扩张的匹配",
      points: [
        "前期不跟风：行业早期扎堆低端价格战，德施曼坚守高端赛道，稳步构建品牌护城河",
        "中期抢跑：电商线上渠道崛起窗口期，率先完成线上布局，抢占流量红利",
        "长期不停步：品牌形成初步优势后持续加大营销投入，维持高端心智与市场热度",
        "秉持长期主义：做到不跟风、不抢跑、不停步，实现企业能力建设与市场规模扩张的精准匹配",
      ],
      conclusion: "经营节奏是企业成长的节拍器。德施曼的长期稳健增长，得益于精准的节奏把控和长期主义发展理念。",
    },
    {
      num: "⑦", title: "赢在能力：五维核心能力构筑不可复制的竞争底盘",
      subPoints: [
        { label: "超强市场洞察力", items: ["穿透行业表层低价竞争，精准捕捉高端化长期趋势", "提前识别\"高端智能锁\"心智空白与市场蓝海"] },
        { label: "高效快速决策能力", items: ["CEO驱动扁平化决策体系，快速响应市场变化", "关键节点快速落地布局，抢占市场先发先机"] },
        { label: "极致营销执行能力", items: ["饱和式品牌推广+全域渠道深耕", "高效传递品牌高端价值，快速占领用户心智"] },
        { label: "持续产品创新能力", items: ["长期坚持高额研发投入，聚焦核心领域持续创新", "迭代核心技术与产品形态，持续保持差异化优势"] },
        { label: "全域渠道布局能力", items: ["系统性搭建立体化全域渠道网络", "线下终端深度覆盖+线上流量精准承接，全面卡位核心销售渠道"] },
      ],
      conclusion: "\"赢在能力\"是所有战略落地的基础。德施曼的多项核心能力构筑了品牌不可复制的竞争底盘。",
    },
  ];

  successFactors.forEach((sf) => {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText(`${sf.num} ${sf.title}`, {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 18, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // 第⑤页用三列卡片布局，⑦用3+2两行卡片布局，其余4页用编号列表
    if (sf.subPoints) {
      const isTwoRow = sf.subPoints.length > 3;
      const cardsPerRow = isTwoRow ? 3 : sf.subPoints.length;
      const cardW = isTwoRow ? 2.9 : 2.95;
      const cardH = isTwoRow ? 1.55 : 2.9;
      const startX = isTwoRow ? 0.55 : 0.5;
      const gap = 0.2;

      sf.subPoints.forEach((sp, i) => {
        let x, y;
        if (isTwoRow && i >= 3) {
          // 第二行：剩余卡片居中
          const row2Count = sf.subPoints.length - 3;
          const row2TotalW = row2Count * cardW + (row2Count - 1) * gap;
          x = startX + (3 * cardW + 2 * gap - row2TotalW) / 2 + (i - 3) * (cardW + gap);
          y = 2.95;
        } else {
          x = startX + i * (cardW + gap);
          y = 1.3;
        }
        addCard(s, x, y, cardW, cardH);
        // 卡片头部
        s.addShape("rect", { x: x, y: y, w: cardW, h: isTwoRow ? 0.42 : 0.5, fill: { color: C.navy } });
        s.addText(sp.label, {
          x: x + 0.1, y: y, w: cardW - 0.2, h: isTwoRow ? 0.42 : 0.5,
          fontSize: isTwoRow ? 10 : 12, color: C.gold, fontFace: "Calibri", bold: true,
          align: "center", valign: "middle", margin: 0,
        });
        // 能力要点
        sp.items.forEach((item, j) => {
          s.addText(`• ${item}`, {
            x: x + 0.12, y: y + (isTwoRow ? 0.48 : 0.58) + j * (isTwoRow ? 0.42 : 0.48),
            w: cardW - 0.24, h: isTwoRow ? 0.4 : 0.45,
            fontSize: isTwoRow ? 8.5 : 10.5, color: C.text, fontFace: "Calibri", margin: 0,
          });
        });
      });
      // ⚠️ 提示（位置根据布局调整）
      const warnY = isTwoRow ? 4.65 : 4.35;
      s.addShape("rect", {
        x: 0.5, y: warnY, w: 9.0, h: 0.42,
        fill: { color: C.orangeLight },
      });
      s.addText([
        { text: "⚠️ ", options: { fontSize: 11 } },
        { text: "但研发原创能力偏弱——SKU过多、流程错位、计划缺失、核心人才流失（详见第二部分诊断）", options: { fontSize: 10, color: C.text } },
      ], {
        x: 0.65, y: 4.35, w: 8.7, h: 0.45,
        fontFace: "Calibri", valign: "middle", margin: 0,
      });
    } else {
      // 标准4点列表
      sf.points.forEach((p, i) => {
        const y = 1.3 + i * 0.72;
        s.addShape("rect", {
          x: 0.6, y: y, w: 0.38, h: 0.38,
          fill: { color: C.gold },
          shadow: makeShadow(),
        });
        s.addText(String(i + 1), {
          x: 0.6, y: y, w: 0.38, h: 0.38,
          fontSize: 14, color: C.white, fontFace: "Calibri", bold: true,
          align: "center", valign: "middle", margin: 0,
        });
        s.addText(p, {
          x: 1.18, y: y, w: 8.27, h: 0.55,
          fontSize: 12, color: C.text, fontFace: "Calibri", margin: 0,
        });
      });

      addDiagnosisBox(s, 0.6, 4.3, 8.8, 0.5, sf.conclusion);
    }

    addFooter(s, part1Section);
  });

  // B7: 战略飞轮（简洁流程图布局，V6）
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2.6 战略飞轮：德施曼过去的增长逻辑", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const bw = 1.85, bh = 0.72;

    // ===== 上行：输入端三要素 =====
    const top = [
      { label: "赛道卡位\n2009年先行进入",   x: 0.5 },
      { label: "中高端定位\n避开价格战",     x: 3.25 },
      { label: "线上先发\n70-80%营收占比",    x: 6.0 },
    ];

    // 下行：输出端四要素
    const bot = [
      { label: "品牌势能\n德系品质认知",     x: 0.5 },
      { label: "数据资产\n用户画像反哺产品", x: 2.85 },
      { label: "渠道议价力\n规模效应增强",   x: 5.2 },
      { label: "研发投入\n产品迭代加速",    x: 7.55 },
    ];

    // 绘制上行框
    top.forEach((it) => {
      s.addShape("rect", {
        x: it.x, y: 1.15, w: bw, h: bh,
        fill: { color: C.blueLight }, shadow: makeShadow(),
        line: { color: C.navy, width: 0.5 },
      });
      s.addText(it.label, {
        x: it.x, y: 1.15, w: bw, h: bh,
        fontSize: 10, color: C.navy, fontFace: "Calibri",
        align: "center", valign: "middle", margin: 0,
      });
    });

    // 绘制下行框
    bot.forEach((it) => {
      s.addShape("rect", {
        x: it.x, y: 4.05, w: bw, h: bh,
        fill: { color: C.blueLight }, shadow: makeShadow(),
        line: { color: C.navy, width: 0.5 },
      });
      s.addText(it.label, {
        x: it.x, y: 4.05, w: bw, h: bh,
        fontSize: 10, color: C.navy, fontFace: "Calibri",
        align: "center", valign: "middle", margin: 0,
      });
    });

    // ===== 中间区域：核心逻辑说明 + 小箭头连接 =====

    // 中心文字块：核心逻辑
    s.addShape("rect", {
      x: 2.8, y: 2.35, w: 4.4, h: 1.3,
      fill: { color: C.navy }, shadow: makeShadow(),
    });
    s.addText([
      { text: "正向循环飞轮\n", options: { fontSize: 13, color: C.gold, bold: true } },
      { text: "\n上行要素驱动品牌势能积累\n", options: { fontSize: 10, color: C.white } },
      { text: "品牌势能反哺下行能力建设\n", options: { fontSize: 10, color: C.white } },
      { text: "能力强化进一步巩固上行优势", options: { fontSize: 10, color: C.white } },
    ], {
      x: 2.8, y: 2.35, w: 4.4, h: 1.3,
      fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
    });

    // ===== 箭头：全部用小 rightArrow =====

    // 上行内部箭头
    [0, 1].forEach((i) => {
      s.addShape("rightArrow", {
        x: top[i].x + bw + 0.04, y: 1.15 + bh/2 - 0.11,
        w: 0.22, h: 0.22,
        fill: { color: C.gold }, line: { type: "none" },
      });
    });

    // 下行内部箭头
    [0, 1, 2].forEach((i) => {
      s.addShape("rightArrow", {
        x: bot[i].x + bw + 0.04, y: 4.05 + bh/2 - 0.11,
        w: 0.22, h: 0.22,
        fill: { color: C.gold }, line: { type: "none" },
      });
    });

    // 上行尾 → 中心块（下箭头）
    s.addShape("downArrow", {
      x: top[2].x + bw/2 - 0.11, y: 1.95,
      w: 0.22, h: 0.35,
      fill: { color: C.gold }, line: { type: "none" },
    });

    // 中心块 → 下行头（下箭头）
    s.addShape("downArrow", {
      x: 3.4, y: 3.72,
      w: 0.22, h: 0.28,
      fill: { color: C.gold }, line: { type: "none" },
    });

    // 左侧闭环标注（竖排小字）
    s.addText("循环\n强化", {
      x: 0.15, y: 2.5, w: 0.3, h: 1.4,
      fontSize: 8, color: C.gold, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0,
    });

    // 右侧闭环标注
    s.addText("反馈\n增强", {
      x: 9.25, y: 2.5, w: 0.3, h: 1.4,
      fontSize: 8, color: C.gold, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0,
    });

    addFooter(s, part1Section);
  }
  // B8: 飞轮前提条件
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2.6 战略飞轮：两个前提条件正在松动", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // Condition 1
    addCard(s, 0.6, 1.3, 4.2, 2.0);
    s.addShape("rect", { x: 0.6, y: 1.3, w: 0.06, h: 2.0, fill: { color: C.red } });
    s.addText("条件一：行业增长", {
      x: 0.9, y: 1.4, w: 3.6, h: 0.4,
      fontSize: 14, color: C.red, fontFace: "Calibri", bold: true, margin: 0,
    });
    s.addText("✓ 行业爆发期（水涨船高）\n✗ 2025年行业下滑20%+", {
      x: 0.9, y: 1.9, w: 3.6, h: 1.2,
      fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
    });
    // Status
    s.addShape("rect", {
      x: 0.9, y: 2.8, w: 1.2, h: 0.3,
      fill: { color: C.redLight },
    });
    s.addText("已松动", {
      x: 0.9, y: 2.8, w: 1.2, h: 0.3,
      fontSize: 9, color: C.red, fontFace: "Calibri", bold: true,
      align: "center", valign: "middle", margin: 0,
    });

    // Condition 2
    addCard(s, 5.2, 1.3, 4.2, 2.0);
    s.addShape("rect", { x: 5.2, y: 1.3, w: 0.06, h: 2.0, fill: { color: C.orange } });
    s.addText("条件二：组织能力", {
      x: 5.5, y: 1.4, w: 3.6, h: 0.4,
      fontSize: 14, color: C.orange, fontFace: "Calibri", bold: true, margin: 0,
    });
    s.addText("✓ 行业上行期能力短板被增长掩盖\n✗ 下行期能力缺失变得致命", {
      x: 5.5, y: 1.9, w: 3.6, h: 1.2,
      fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
    });
    s.addShape("rect", {
      x: 5.5, y: 2.8, w: 1.2, h: 0.3,
      fill: { color: C.orangeLight },
    });
    s.addText("历来短板", {
      x: 5.5, y: 2.8, w: 1.2, h: 0.3,
      fontSize: 9, color: C.orange, fontFace: "Calibri", bold: true,
      align: "center", valign: "middle", margin: 0,
    });

    // Bottom conclusion
    addDiagnosisBox(s, 0.6, 3.6, 8.8, 0.8,
      "飞轮运转需要两个前提条件：行业在增长（水涨船高）和组织能力跟得上（飞轮不散架）。当前第一个条件已经松动，第二个条件从一开始就是德施曼的短板。\n行业下行20%+的环境下，德施曼曾经的增长逻辑正在失效——这正是本次诊断要回答的核心问题。"
    );

    addFooter(s, part1Section);
  }

  // C1: 文化归因总览
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("3. 文化归因", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const cultures = [
      { title: "前瞻意识", desc: "行业萌芽期敢于投入\nC端爆发前率先布局线上", model: "四力·认知力", bg: C.navy },
      { title: "品质信仰", desc: "坚持不降品质底线\n不是所有钱都要赚", model: "四有·有追求", bg: C.navyLight },
      { title: "开放学习", desc: "德国技术引进→自建能力\n\"愿意尝试新东西\"", model: "四力·实践力", bg: C.navy },
      { title: "务实进取", desc: "\"把事情做成\"的务实精神\n·一线反复强调\"执行\"", model: "四力·驱动力", bg: C.navyLight },
    ];

    cultures.forEach((c, i) => {
      const x = 0.4 + i * 2.4;
      addCard(s, x, 1.3, 2.15, 2.8);
      s.addShape("rect", { x: x, y: 1.3, w: 2.15, h: 0.55, fill: { color: c.bg } });
      s.addText(c.title, {
        x: x + 0.15, y: 1.3, w: 1.85, h: 0.55,
        fontSize: 15, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(c.desc, {
        x: x + 0.15, y: 2.0, w: 1.85, h: 1.2,
        fontSize: 10, color: C.text, fontFace: "Calibri", margin: 0,
      });
      // Model label
      s.addShape("rect", {
        x: x + 0.3, y: 3.35, w: 1.55, h: 0.35,
        fill: { color: C.goldLight },
      });
      s.addText(c.model, {
        x: x + 0.3, y: 3.35, w: 1.55, h: 0.35,
        fontSize: 8, color: C.navy, fontFace: "Calibri",
        align: "center", valign: "middle", margin: 0,
      });
    });

    // Bottom summary
    s.addText("成功要素不会凭空产生。前瞻意识、品质信仰、开放学习、务实进取——这些文化品格是德施曼成功的深层驱动力。", {
      x: 0.6, y: 4.4, w: 8.8, h: 0.5,
      fontSize: 11, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
    });

    addFooter(s, part1Section);
  }

  // D1: Part 1 基本判断
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("4. 成功经验小结：基本判断", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const judgments = [
      "德施曼是一家抓住了结构性产业机遇的企业——\n智能锁行业的爆发式增长是其成功的最大外部条件。",
      "德施曼是一家有品牌意识和品质信仰的企业——\n\"德系品质\"定位使它在价格战中保持了差异化。",
      "德施曼是一家渠道能力突出但组织能力尚未跟上的企业——\n管理体系、人才密度、决策机制与规模和阶段存在显著落差。",
    ];

    judgments.forEach((j, i) => {
      const y = 1.3 + i * 1.1;
      addCard(s, 0.6, y, 8.8, 0.95);
      s.addShape("rect", { x: 0.6, y: y, w: 0.08, h: 0.95, fill: { color: C.navy } });
      s.addText(j, {
        x: 0.9, y: y + 0.1, w: 8.2, h: 0.75,
        fontSize: 13, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part1Section);
  }

  // ============================================================
  // PART 2: 现实问题和成长制约
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.red } });
    s.addText("第二部分", {
      x: 0.8, y: 1.8, w: 8.4, h: 0.8,
      fontSize: 42, color: C.white, fontFace: "Calibri", bold: true,
      align: "center", margin: 0,
    });
    s.addText("现实问题和成长制约", {
      x: 0.8, y: 2.7, w: 8.4, h: 0.5,
      fontSize: 18, color: C.red, fontFace: "Calibri",
      align: "center", margin: 0,
    });
  }

  const part2Section = "德施曼企业管理咨询诊断报告  |  第二部分：现实问题和成长制约";

  // 经营画像
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1.1 经营画像：六大关键信号", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const signals = [
      { num: "01", text: "行业下滑20%+，策略从\"进攻\"调整为\"稳健\"", style: C.red },
      { num: "02", text: "线上渠道占比过高（70-80%），渠道结构单一化风险", style: C.orange },
      { num: "03", text: "线下渠道虽进展但不及预期，区域发展极不均衡，窜货持续", style: C.orange },
      { num: "04", text: "新业务（摄像头）战略失败，暴露创新管理系统性短板", style: C.red },
      { num: "05", text: "价格段存在结构性空缺，给了竞品可乘之机", style: C.blue },
      { num: "06", text: "\"总部效率\"是多位战区负责人反复提及的痛点", style: C.blue },
    ];

    signals.forEach((sig, i) => {
      const y = 1.2 + i * 0.63;
      s.addShape("rect", {
        x: 0.6, y: y, w: 0.5, h: 0.45,
        fill: { color: sig.style },
      });
      s.addText(sig.num, {
        x: 0.6, y: y, w: 0.5, h: 0.45,
        fontSize: 14, color: C.white, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(sig.text, {
        x: 1.3, y: y, w: 8, h: 0.45,
        fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // 经营压力
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1.2 经营压力分析", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const pressures = [
      {
        title: "业绩压力",
        items: ["行业大盘下滑20%+", "线上渠道增长红利消退", "线下渠道爬坡缓慢", "新业务未贡献预期增量"],
        quote: "「市场在缩量，我们原来的打法是建立在增长假设上的。」",
        color: C.red,
      },
      {
        title: "竞争压力",
        items: ["小米生态链+价格优势挤压", "凯迪仕等竞品加大投入", "价格段空缺给竞品机会", "行业洗牌期不进则退"],
        quote: "「稳健是无奈，不是主动选择。」",
        color: C.orange,
      },
      {
        title: "发展压力",
        items: ["SKU过多，研发资源分散", "新品节奏与市场脱节", "关键人才持续流失", "组织架构难支撑规模化"],
        quote: "「人走了，带走的是经验，留下的是坑。」",
        color: C.blue,
      },
    ];

    pressures.forEach((p, i) => {
      const x = 0.4 + i * 3.2;
      addCard(s, x, 1.2, 2.9, 2.8);
      s.addShape("rect", { x: x, y: 1.2, w: 2.9, h: 0.42, fill: { color: p.color } });
      s.addText(p.title, {
        x: x + 0.15, y: 1.2, w: 2.6, h: 0.42,
        fontSize: 13, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
      });

      p.items.forEach((item, j) => {
        s.addText(`•  ${item}`, {
          x: x + 0.15, y: 1.75 + j * 0.32, w: 2.6, h: 0.28,
          fontSize: 10, color: C.text, fontFace: "Calibri", margin: 0,
        });
      });

      s.addShape("rect", { x: x, y: 3.05, w: 0.04, h: 0.7, fill: { color: C.gold } });
      s.addText(p.quote, {
        x: x + 0.15, y: 3.05, w: 2.6, h: 0.7,
        fontSize: 9, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // 一心开二门框架
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2. 问题诊断框架：「一心开二门」", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // Center: 一心
    s.addShape("oval", {
      x: 3.3, y: 1.5, w: 3.4, h: 1.1,
      fill: { color: C.gold },
      shadow: makeShadow(),
    });
    s.addText([
      { text: "心", options: { bold: true, fontSize: 20, color: C.white } },
      { text: "\n心愿 · 心力 · 心识", options: { fontSize: 11, color: C.white } },
    ], {
      x: 3.3, y: 1.5, w: 3.4, h: 1.1,
      fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
    });

    // Left door: 战略之门
    s.addShape("rect", {
      x: 0.6, y: 3.1, w: 4.2, h: 1.5,
      fill: { color: C.blueLight },
      shadow: makeShadow(),
    });
    s.addText([
      { text: "战略之门", options: { bold: true, fontSize: 15, color: C.navy } },
      { text: "\n机会洞察 · 价值创造 · 资源整合", options: { fontSize: 10, color: C.textMuted } },
      { text: "\n\n► 战略管理闭环缺失", options: { fontSize: 10, color: C.red } },
      { text: "\n► 运营体系串联低效", options: { fontSize: 10, color: C.red } },
      { text: "\n► 业务组合战略失焦", options: { fontSize: 10, color: C.red } },
    ], {
      x: 0.8, y: 3.2, w: 3.8, h: 1.3,
      fontFace: "Calibri", margin: 0,
    });

    // Right door: 组织之门
    s.addShape("rect", {
      x: 5.2, y: 3.1, w: 4.2, h: 1.5,
      fill: { color: C.greenLight },
      shadow: makeShadow(),
    });
    s.addText([
      { text: "组织之门", options: { bold: true, fontSize: 15, color: C.navy } },
      { text: "\n架构流程 · 团队建设 · 企业文化", options: { fontSize: 10, color: C.textMuted } },
      { text: "\n\n► 总部小散弱，战区不均衡", options: { fontSize: 10, color: C.red } },
      { text: "\n► 人才密度不足，梯队断层", options: { fontSize: 10, color: C.red } },
      { text: "\n► 创业精神→等待文化", options: { fontSize: 10, color: C.red } },
    ], {
      x: 5.4, y: 3.2, w: 3.8, h: 1.3,
      fontFace: "Calibri", margin: 0,
    });

    // 箭头：从一心指向两门——小箭头，不遮挡内容
    s.addShape("downArrow", {
      x: 4.75, y: 2.62, w: 0.5, h: 0.35,
      fill: { color: C.gold },
      line: { type: "none" },
    });

    addFooter(s, part2Section);
  }

  // Helper function for interview + analysis slides
  function addInterviewAnalysisSlide(title, quotes, analysisPoints, diagnosis) {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText(title, {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 17, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    // Left: Interview quotes
    addCard(s, 0.6, 1.2, 4.3, 2.8);
    s.addShape("rect", { x: 0.6, y: 1.2, w: 4.3, h: 0.4, fill: { color: C.navyLight } });
    s.addText("访谈摘录", {
      x: 0.8, y: 1.2, w: 3.9, h: 0.4,
      fontSize: 11, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    quotes.forEach((q, i) => {
      s.addShape("rect", {
        x: 0.8, y: 1.75 + i * 0.55, w: 0.04, h: 0.4,
        fill: { color: C.gold },
      });
      s.addText(q, {
        x: 0.95, y: 1.75 + i * 0.55, w: 3.7, h: 0.4,
        fontSize: 9.5, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
      });
    });

    // Right: Facts & conclusions
    addCard(s, 5.2, 1.2, 4.2, 2.8);
    s.addShape("rect", { x: 5.2, y: 1.2, w: 4.2, h: 0.4, fill: { color: C.navy } });
    s.addText("事实和结论", {
      x: 5.4, y: 1.2, w: 3.8, h: 0.4,
      fontSize: 11, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
    });

    analysisPoints.forEach((ap, i) => {
      s.addText(`• ${ap}`, {
        x: 5.4, y: 1.75 + i * 0.48, w: 3.8, h: 0.4,
        fontSize: 9.5, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    // Diagnosis box
    addDiagnosisBox(s, 0.6, 4.2, 8.8, 0.55, diagnosis);

    addFooter(s, part2Section);
  }

  // 战略管理
  addInterviewAnalysisSlide(
    "2.1.1 战略管理：有规划文本，无管理闭环",
    [
      "「我们有三年战略规划，目标也定了，但到了执行层面就变样了。」",
      "「从进攻到稳健，这个调整来得很突然，底下的团队其实没有做好准备。」",
      "「战略部的职能没有真正发挥出来，更多是在做信息和文书工作。」",
      "「各部门的目标没有真正互锁——研发的目标和销售的目标是两套逻辑。」",
    ],
    [
      "战略解码缺失：规划到年度计划到部门目标的逐层解码体系未建立",
      "战略动态调整缺乏系统性：\"进攻→稳健\"转向缺乏数据支撑和场景推演",
      "资源投向分散：明确的方向在资源配置中未获得应有优先级",
      "战略停留在高层头脑中，未转化为组织共同语言和行动指南",
    ],
    "核心诊断：战略制定到战略落地的长周期价值循环没有打通。有方向、有目标，但没有可操作的资源配置方案和执行追踪体系。"
  );

  // 运营效率
  addInterviewAnalysisSlide(
    "2.1.2 运营效率：价值链各环节明显脱节",
    [
      "「研发说要做什么，生产说做不了，销售说要这个——三个部门在三个频道上。」",
      "「一个产品从立项到上市，中间要过的环节太多了，每个环节都能卡住。」",
      "「产销矛盾是老问题了。销售端永远在催货，生产端永远在抱怨预测不准。」",
      "「流程是为不出错设计的，不是为快速响应设计的。」",
    ],
    [
      "研发-生产-营销脱节：三方缺乏统一的计划平台和协调机制（无S&OP）",
      "开发流程结构错位：多次折返和等待，\"压缩周期\"牺牲的是质量",
      "产销负反馈循环：预测不准→排产波动→交付延迟→预测更不准",
      "\"找对人比走流程快\"——这正是流程失效的明证",
    ],
    "核心诊断：运营体系是\"串联\"模式而非\"并联\"模式。信息线性传递，每个环节都是瓶颈，缺乏端到端的流程拉通和横向协同机制。"
  );

  // 业务组合
  addInterviewAnalysisSlide(
    "2.1.3 业务组合：分散有余，聚焦不足",
    [
      "「摄像头做了一年多，钱花了，人招了，最后发现方向不对。」",
      "「SD卡涨价五倍那次，完全是被动挨打——供应链管理能力根本跟不上。」",
      "「我们的SKU太多了，很多长尾产品一年卖不了多少，但占用了大量研发资源。」",
      "「龙庭品牌定位是什么？跟主品牌怎么分工？这个问题一直没有讲清楚。」",
    ],
    [
      "摄像头业务：缺乏战略论证（协同性/竞争优势/供应链风险评估全缺失）",
      "SKU过多：用广度代替精准度，研发资源稀释、品控难度上升、供应链低效",
      "双品牌逻辑缺失：互补还是内耗？价格段/渠道/资源分配均无共识",
      "\"做什么、不做什么\"——这个最基本的战略问题在公司内部没有清晰答案",
    ],
    "核心诊断：战略不聚焦。资源分散、SKU过载、新业务失败——都是战略不聚焦的症状，不是根因。"
  );

  // 组织架构
  addInterviewAnalysisSlide(
    "2.2.1 组织架构：总部小散弱，战区不均衡",
    [
      "「总部的职能部门应该是大脑，但现在更像是一个审批盖章的地方。」",
      "「战区之间的差距太大了。东部一个战区卖1.5亿，南区六个省加起来才10-13%。」",
      "「总部离前线太远了，前线要资源要走很长的流程，等批下来时机已经过了。」",
      "「组织架构图看起来很完整，但很多岗位的实际职能跟图纸上写的不一样。」",
    ],
    [
      "总部\"小散弱\"：职能划分过细但发育不足，战略部偏文书、HR停留考勤层面",
      "战区发展严重不均衡：东部1.5亿，南区6省仅10-13%，优秀经验无法复制",
      "总部与前线紧张：\"审批速度跟不上市场变化，前线不是在打仗而是在等命令\"",
      "总部是\"管理型总部\"而非\"赋能型总部\"",
    ],
    "核心诊断：组织架构的\"形式完整性\"掩盖了\"功能缺陷\"。"
  );

  // 组织能力六维
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2.2.2 组织能力六维深度诊断", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const abilities = [
      { title: "凝聚力/协同力", status: "薄弱", color: C.red, items: "跨部门缺乏共识和信任\n\"找对人比走流程快\"\n无统一S&OP平台" },
      { title: "战斗力", status: "不足", color: C.orange, items: "技能密度无法满足战略需求\n考核激励体系失效\n中层管理人才储备薄弱" },
      { title: "生命力", status: "缺失", color: C.red, items: "创新无阶段性评审/止损文化\n组织熵增：流程变长、审批增多\n窜货反映管控体系漏洞" },
      { title: "领导", status: "单核驱动", color: C.orange, items: "高管团队未真正形成\n决策权过度集中\n单核模式已越效能拐点" },
    ];

    abilities.forEach((ab, i) => {
      const x = 0.4 + i * 2.4;
      addCard(s, x, 1.3, 2.15, 2.6);
      // Status bar
      s.addShape("rect", { x: x, y: 1.3, w: 2.15, h: 0.05, fill: { color: ab.color } });
      s.addText(ab.title, {
        x: x + 0.15, y: 1.45, w: 1.85, h: 0.35,
        fontSize: 12, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addShape("rect", {
        x: x + 0.7, y: 2.85, w: 0.9, h: 0.32,
        fill: { color: ab.color === C.red ? C.redLight : C.orangeLight },
      });
      s.addText(ab.status, {
        x: x + 0.7, y: 2.85, w: 0.9, h: 0.32,
        fontSize: 9, color: ab.color, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(ab.items, {
        x: x + 0.15, y: 1.9, w: 1.85, h: 0.9,
        fontSize: 9, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // 人才
  addInterviewAnalysisSlide(
    "2.2.3 人才：密度不足、梯队断层、激励失焦",
    [
      "「我们一直说缺人，但怎么定义缺人——是缺人手还是缺人才？我觉得是后者。」",
      "「研发那边走了几个人，很多项目马上就停了。经验都在他们脑子里面。」",
      "「南区校招培养的模式成本很高、见效很慢，但市场上挖不到现成的人。」",
      "「考核跟战略目标是脱节的。我完成了考核指标，但团队的方向可能偏了。」",
    ],
    [
      "人才密度不足：缺的不是\"人手\"而是\"人才\"——具备专业+管理能力的骨干",
      "知识管理体系缺失：核心人员离职→项目停摆，\"知识在脑子里\"",
      "后备干部断层：\"二级企业家\"（战区/部门负责人级）数量质量都不够",
      "激励考核失焦：关注\"做没做\"而非\"做没做成\"，与战略目标脱节",
    ],
    "核心诊断：人才体系是\"倒三角\"——底层人员充足，中层管理薄弱，高层决策过度集中。下行期崩塌风险极高。"
  );

  // 企业文化
  addInterviewAnalysisSlide(
    "2.2.4 企业文化：创业精神稀释，信任文化不足",
    [
      "「以前我们是什么都敢试，现在是做什么都怕出错。」",
      "「公司内部的信息流通有问题。很多决定我们是通过非正式渠道知道的。」",
      "「集权的问题不是老板管太多，而是没管的地方没人敢管。」",
      "「摄像头那边的团队说他们感觉不到参与感。」",
    ],
    [
      "创业精神流失：\"敢试\"→\"怕出错\"——行业下行+组织变大双重抑制",
      "集权与参与感矛盾：中层产生强烈自主权需求，但所有重要决策仍集中顶层",
      "信息透明度不足：信息被当作权力资源而非公共资源，组织信任成本持续升高",
      "企业从\"创业文化\"滑向\"等待文化\"：等决策/等审批/等资源",
    ],
    "核心诊断：企业文化正从\"创业文化\"滑向\"等待文化\"。等待消耗的不仅是时间，更是组织的活力和人才的耐心。"
  );

  // 领导体制
  addInterviewAnalysisSlide(
    "2.3 领导体制：企业家单核驱动模式的瓶颈",
    [
      "「公司大方向都是老板定的。高管会议上其实很少有真正的讨论和质疑。」",
      "「不是不想放权，是放了不放心。但不放的话，所有事情都堆在一个人身上。」",
      "「老板该管的没管到位，不该管的管太多了——比如具体的定价和促销方案。」",
      "「我们缺少一个真正能讨论、能争论、能拍板的高管团队。」",
    ],
    [
      "缺乏真正的高管团队：高管会议功能是\"通报\"而非\"讨论\"，决策文化缺失",
      "企业家事务过度集中：该管的战略和不该管的操作都集中在一人身上",
      "单核驱动从优势变为瓶颈：抑制高管团队成长、降低组织响应速度、造成等待文化",
      "\"强势+前瞻\"型领导风格在创业期是优势，在当前阶段正在成为瓶颈",
    ],
    "核心诊断：领导体制正处于\"单核驱动\"模式的效能拐点。德施曼已经越过了单核驱动的临界点。"
  );

  // 领导行为六维图谱
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2.3 领导行为六维图谱", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const spectrums = [
      { left: "目标导向", right: "关系导向", pos: 0.15 },
      { left: "勇于冒险", right: "谨慎稳健", pos: 0.2 },
      { left: "信任授权", right: "控制集权", pos: 0.85 },
      { left: "鼓励创新", right: "强调执行", pos: 0.25 },
      { left: "分享权力", right: "集中权力", pos: 0.85 },
      { left: "个性鲜明", right: "低调内敛", pos: 0.15 },
    ];

    spectrums.forEach((sp, i) => {
      const y = 1.3 + i * 0.6;
      // Left label
      s.addText(sp.left, {
        x: 0.6, y: y, w: 1.6, h: 0.4,
        fontSize: 10, color: C.navy, fontFace: "Calibri", bold: true,
        align: "right", margin: 0,
      });
      // Bar background
      s.addShape("rect", {
        x: 2.4, y: y + 0.12, w: 5.2, h: 0.16,
        fill: { color: C.line },
      });
      // Position dot
      const dotX = 2.4 + sp.pos * 5.0;
      s.addShape("oval", {
        x: dotX, y: y + 0.05, w: 0.3, h: 0.3,
        fill: { color: C.gold },
      });
      // Right label
      s.addText(sp.right, {
        x: 7.8, y: y, w: 1.6, h: 0.4,
        fontSize: 10, color: C.textMuted, fontFace: "Calibri",
        align: "left", margin: 0,
      });
    });

    // Analysis box
    s.addShape("rect", {
      x: 0.6, y: 5.0, w: 8.8, h: 0.05,
      fill: { color: C.gold },
    });

    addFooter(s, part2Section);
  }

  // 问题的性质
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("3.1 问题的性质：六大定性判断", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const natures = [
      { label: "普遍性", desc: "在从机会成长向系统成长跨越的民营企业中普遍出现" },
      { label: "整体性", desc: "不是局部问题，是贯穿战略/组织/人才/文化的全局性结构性问题" },
      { label: "顶层性", desc: "根因指向治理结构和领导体制——高管团队的缺失/决策权过度集中" },
      { label: "长期性", desc: "组织能力、文化重塑、人才建设——需要以年为单位持续推进" },
      { label: "深层性", desc: "涉及隐性心智地图：\"控制比信任安全\"\"战术比战略紧迫\"\"做多比做对重要\"" },
    ];

    natures.forEach((n, i) => {
      const y = 1.3 + i * 0.72;
      s.addShape("rect", {
        x: 0.6, y: y, w: 1.2, h: 0.5,
        fill: { color: C.navy },
      });
      s.addText(n.label, {
        x: 0.6, y: y, w: 1.2, h: 0.5,
        fontSize: 11, color: C.gold, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(n.desc, {
        x: 2.0, y: y, w: 7.4, h: 0.5,
        fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // 三大矛盾 - 矛盾一
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("3.2 矛盾一：「业务——能力」的矛盾", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    s.addText("业务增长在前，能力成长跟随——二者往往不匹配。当行业增速降至-20%，能力的缺失变得致命。", {
      x: 0.6, y: 1.2, w: 8.8, h: 0.4,
      fontSize: 11, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
    });

    const gaps = [
      {
        title: "技术能力",
        desc: "SKU过多暴露缺乏系统化产品规划和研发管理能力的短板。市场需求收缩时，需要\"做少但做精\"——但研发体系不具备这个能力。",
      },
      {
        title: "组织能力",
        desc: "总部职能发育不足使\"精细化运营\"力不从心。渠道管理、供应链协调、跨部门协同——粗放增长时代勉强应付，精细化时代成为瓶颈。",
      },
      {
        title: "人才能力",
        desc: "中层管理人才断层意味着公司缺乏将战略转化为执行的人才基础。\"二级企业家\"的缺失，使所有重大决策不得不向上集中。",
      },
    ];

    gaps.forEach((g, i) => {
      const y = 1.8 + i * 1.0;
      addCard(s, 0.6, y, 8.8, 0.85);
      s.addShape("rect", { x: 0.6, y: y, w: 0.08, h: 0.85, fill: { color: C.red } });
      s.addText(g.title, {
        x: 0.9, y: y + 0.05, w: 1.5, h: 0.75,
        fontSize: 14, color: C.red, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(g.desc, {
        x: 2.5, y: y + 0.1, w: 6.6, h: 0.65,
        fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // 矛盾二
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("3.2 矛盾二：「成长——治理」的矛盾", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    s.addText("经营规模已达中大型企业门槛，但治理方式仍停留在创业期。", {
      x: 0.6, y: 1.2, w: 8.8, h: 0.4,
      fontSize: 11, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
    });

    const issues = [
      { label: "缺少高管团队", desc: "不是没有高管，而是没有形成真正能够集体讨论、理性争论、共同决策并共同承担责任的团队。", icon: "01" },
      { label: "缺少民主决策机制", desc: "重大决策权力过度集中。摄像头业务的失败如果有一个健康的\"质疑和辩论\"机制，可能在立项阶段就被否决或调整。", icon: "02" },
      { label: "缺少组织规则", desc: "企业运转过度依赖人而非制度。流程被权力驱动而非制度驱动。跨部门协同靠\"找人\"而非\"走流程\"。", icon: "03" },
    ];

    issues.forEach((iss, i) => {
      const y = 1.8 + i * 1.0;
      addCard(s, 0.6, y, 8.8, 0.85);
      s.addShape("rect", { x: 0.6, y: y, w: 0.08, h: 0.85, fill: { color: C.orange } });
      s.addText(iss.icon, {
        x: 0.8, y: y + 0.05, w: 0.5, h: 0.75,
        fontSize: 16, color: C.gold, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(iss.label, {
        x: 1.3, y: y + 0.05, w: 1.8, h: 0.75,
        fontSize: 14, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(iss.desc, {
        x: 3.2, y: y + 0.1, w: 5.9, h: 0.65,
        fontSize: 11, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // 矛盾三
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("3.2 矛盾三：「环境——进化」的矛盾", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const changes = [
      { old: "行业快速增长", new: "行业进入收缩" },
      { old: "线上渠道红利", new: "线上获客成本持续上升" },
      { old: "德系品质差异化", new: "差异化标签价值递减" },
    ];

    changes.forEach((ch, i) => {
      const y = 1.3 + i * 0.7;
      s.addShape("rect", {
        x: 0.6, y: y, w: 3.2, h: 0.5,
        fill: { color: C.greenLight },
      });
      s.addText(ch.old, {
        x: 0.6, y: y, w: 3.2, h: 0.5,
        fontSize: 12, color: C.navy, fontFace: "Calibri",
        align: "center", valign: "middle", margin: 0,
      });
      // 用形状箭头替代Unicode字符
      s.addShape("rightArrow", {
        x: 3.85, y: y + 0.15, w: 0.3, h: 0.2,
        fill: { color: C.red }, line: { type: "none" },
      });
      s.addShape("rect", {
        x: 4.2, y: y, w: 4.4, h: 0.5,
        fill: { color: C.redLight },
      });
      s.addText(ch.new, {
        x: 4.2, y: y, w: 4.4, h: 0.5,
        fontSize: 12, color: C.red, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
    });

    s.addText("需要的五大认知转变", {
      x: 0.6, y: 3.3, w: 8.8, h: 0.4,
      fontSize: 14, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });

    const shifts = [
      { from: "增长驱动", to: "能力驱动" },
      { from: "线上单一渠道", to: "全渠道运营" },
      { from: "产品广度", to: "产品精度" },
      { from: "个人驱动", to: "组织驱动" },
      { from: "控制文化", to: "信任文化" },
    ];

    shifts.forEach((sh, i) => {
      const x = 0.4 + i * 1.92;
      s.addShape("rect", {
        x: x, y: 3.85, w: 1.72, h: 0.9,
        fill: { color: C.navy },
        shadow: makeShadow(),
      });
      s.addText([
        { text: sh.from, options: { fontSize: 10, color: C.textLight, strike: true } },
        { text: "\n  转为\n", options: { fontSize: 9, color: C.gold } },
        { text: sh.to, options: { fontSize: 11, color: C.white, bold: true } },
      ], {
        x: x, y: 3.85, w: 1.72, h: 0.9,
        fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
      });
    });

    addFooter(s, part2Section);
  }

  // ============================================================
  // PART 3: 战略性课题与变革建议
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.gold } });
    s.addText("第三部分", {
      x: 0.8, y: 1.8, w: 8.4, h: 0.8,
      fontSize: 42, color: C.white, fontFace: "Calibri", bold: true,
      align: "center", margin: 0,
    });
    s.addText("战略性课题与变革建议", {
      x: 0.8, y: 2.7, w: 8.4, h: 0.5,
      fontSize: 18, color: C.gold, fontFace: "Calibri",
      align: "center", margin: 0,
    });
  }

  const part3Section = "德施曼企业管理咨询诊断报告  |  第三部分：战略性课题与变革建议";

  // 基本判断四句话
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1. 对企业的基本判断：四句话总结", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const fourJudgments = [
      { text: "德施曼曾经是一个抓住了产业机遇、用品牌和渠道能力突围的赢家。", highlight: C.green },
      { text: "德施曼的基础犹在——品牌资产、渠道能力、产品积累、团队经验仍是宝贵存量。", highlight: C.blue },
      { text: "德施曼的问题严重——组织能力与业务规模的落差、治理方式与阶段错配、战略管理断裂。", highlight: C.orange },
      { text: "德施曼前景可期。但前提是——启动真正的组织变革。", highlight: C.navy },
    ];

    fourJudgments.forEach((j, i) => {
      const y = 1.2 + i * 0.95 + (i >= 2 ? 0.1 : 0);
      addCard(s, 0.6, y, 8.8, 0.8);
      s.addShape("rect", { x: 0.6, y: y, w: 0.08, h: 0.8, fill: { color: j.highlight } });
      s.addText(j.text, {
        x: 0.9, y: y + 0.1, w: 8.2, h: 0.6,
        fontSize: 14, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part3Section);
  }

  // 灵魂之问
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("1. 灵魂之问", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);
    s.addText("以下七个问题，不是用来解答的，而是用来引发德施曼管理层的深层反思。", {
      x: 0.6, y: 1.0, w: 8.8, h: 0.3,
      fontSize: 9, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
    });

    const questions = [
      "为什么我们在行业爆发期能够赢，但在行业下行期却发现过去的成功逻辑正在失效？",
      "为什么方向总体正确（聚焦中高端、拓展线下、双品牌布局），但执行总是在走样？",
      "为什么我们在产品上做了很多，但真正打穿市场、建立壁垒的产品很少？",
      "为什么优秀的人才正在选择离开——是薪酬问题，还是已经看不到成长空间？",
      "为什么\"总部效率\"成了前线最大的痛点——组织在帮前线还是在拖后腿？",
      "为什么摄像头业务会失败——再来一次，会犯同样的错误吗？",
      "当老板不在公司的时候，这个公司还能不能正常做决策、推动业务？",
    ];

    questions.forEach((q, i) => {
      const y = 1.35 + i * 0.54;
      s.addText(`${i + 1}.`, {
        x: 0.6, y: y, w: 0.3, h: 0.45,
        fontSize: 11, color: C.gold, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(q, {
        x: 0.95, y: y, w: 8.5, h: 0.45,
        fontSize: 10.5, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part3Section);
  }

  // 四大转型方向
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("2. 四大转型方向", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const directs = [
      { from: "机会成长", to: "能力成长", y: 1.3, x: 0.4, icon: "01" },
      { from: "中小企", to: "中大型企", y: 1.3, x: 5.0, icon: "02" },
      { from: "线上单一渠道", to: "全渠道运营", y: 3.2, x: 0.4, icon: "03" },
      { from: "个人驱动", to: "组织驱动", y: 3.2, x: 5.0, icon: "04" },
    ];

    directs.forEach((d) => {
      addCard(s, d.x, d.y, 4.3, 1.65);
      s.addShape("rect", { x: d.x, y: d.y, w: 4.3, h: 0.45, fill: { color: C.navy } });
      s.addText(`转型方向 ${d.icon}`, {
        x: d.x + 0.15, y: d.y, w: 4.0, h: 0.45,
        fontSize: 10, color: C.gold, fontFace: "Calibri", margin: 0,
      });

      // from + arrow + to：用形状箭头替代Unicode
      s.addText(d.from, {
        x: d.x + 0.3, y: d.y + 0.65, w: 1.6, h: 0.35,
        fontSize: 12, color: C.textMuted, fontFace: "Calibri",
        align: "right", valign: "middle", margin: 0,
      });
      s.addShape("rightArrow", {
        x: d.x + 1.95, y: d.y + 0.75, w: 0.4, h: 0.18,
        fill: { color: C.gold }, line: { type: "none" },
      });
      s.addText(d.to, {
        x: d.x + 2.4, y: d.y + 0.65, w: 1.7, h: 0.35,
        fontSize: 12, color: C.navy, fontFace: "Calibri", bold: true,
        align: "left", valign: "middle", margin: 0,
      });
    });

    addFooter(s, part3Section);
  }

  // 变革指导思想
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("3. 变革指导思想", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 24, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    const guides = [
      { num: "01", title: "强化战略牵引", desc: "从\"有规划文本\"升级为\"有管理闭环\"——战略不是写出来的文档，是全周期管理系统。" },
      { num: "02", title: "提升组织力量", desc: "总部从\"管理型\"转向\"赋能型\"，战区从\"各自为战\"转向\"能力共享\"。" },
      { num: "03", title: "建立高效体系", desc: "打通研发-生产-营销价值链，用流程和系统（而非人情和权力）驱动横向协同。" },
      { num: "04", title: "重建心智地图", desc: "从\"控制比信任安全\"\"战术比战略紧迫\"\"做多比做对重要\"→\"信任赋能\"\"战略引领\"\"少即是多\"。" },
      { num: "05", title: "强化使命驱动", desc: "行业下行期更需要超越短期利益的事业追求来凝聚团队，成为变革的内在驱动力。" },
    ];

    guides.forEach((g, i) => {
      const y = 1.2 + i * 0.75;
      s.addShape("rect", {
        x: 0.6, y: y, w: 0.45, h: 0.55,
        fill: { color: C.navy },
      });
      s.addText(g.num, {
        x: 0.6, y: y, w: 0.45, h: 0.55,
        fontSize: 14, color: C.gold, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(g.title, {
        x: 1.25, y: y, w: 2.0, h: 0.55,
        fontSize: 12, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(g.desc, {
        x: 3.3, y: y, w: 6.1, h: 0.55,
        fontSize: 10.5, color: C.text, fontFace: "Calibri", margin: 0,
      });
    });

    addFooter(s, part3Section);
  }

  // 一心开二门跃迁蓝图总览
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText("4. 变革路径：一心开二门跃迁蓝图", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    s.addText("以三年为期，从\"一心\"的升级开始，同时打开\"战略之门\"和\"组织之门\"，实现从\"机会驱动型中小企业\"向\"能力驱动型中大型企业\"的跃迁。", {
      x: 0.6, y: 1.1, w: 8.8, h: 0.4,
      fontSize: 10, color: C.textMuted, fontFace: "Calibri", italic: true, margin: 0,
    });

    const phases = [
      { phase: "第一阶段", period: "0-12个月", title: "筑基", subtitle: "建立变革的基础设施", color: C.navy },
      { phase: "第二阶段", period: "12-24个月", title: "强体", subtitle: "推动组织能力的系统升级", color: C.navyLight },
      { phase: "第三阶段", period: "24-36个月", title: "进化", subtitle: "完成机会→能力驱动转型", color: C.navy },
    ];

    phases.forEach((ph, i) => {
      const x = 0.4 + i * 3.2;
      addCard(s, x, 1.7, 2.85, 2.0);
      s.addShape("rect", { x: x, y: 1.7, w: 2.85, h: 0.55, fill: { color: ph.color } });
      s.addText(ph.phase, {
        x: x + 0.15, y: 1.7, w: 1.5, h: 0.3,
        fontSize: 9, color: C.gold, fontFace: "Calibri", margin: 0,
      });
      s.addText(ph.period, {
        x: x + 1.3, y: 1.7, w: 1.4, h: 0.3,
        fontSize: 9, color: C.white, fontFace: "Calibri", align: "right", margin: 0,
      });
      s.addText(ph.title, {
        x: x + 0.15, y: 2.0, w: 2.55, h: 0.4,
        fontSize: 16, color: C.white, fontFace: "Calibri", bold: true, margin: 0,
      });
      s.addText(ph.subtitle, {
        x: x + 0.15, y: 2.5, w: 2.55, h: 0.5,
        fontSize: 10, color: C.text, fontFace: "Calibri", margin: 0,
      });
      // Arrow: 用形状箭头替代Unicode字符
      if (i < 2) {
        s.addShape("rightArrow", {
          x: x + 2.85 + 0.02, y: 1.7 + 0.85 - 0.15, w: 0.35, h: 0.3,
          fill: { color: C.gold },
          line: { type: "none" },
        });
      }
    });

    // Five dimensions
    const dims = ["治理", "战略", "组织", "人才", "文化"];
    dims.forEach((d, i) => {
      const x = 0.6 + i * 1.85;
      s.addShape("rect", {
        x: x, y: 4.0, w: 1.6, h: 0.45,
        fill: { color: C.blueLight },
      });
      s.addText(d, {
        x: x, y: 4.0, w: 1.6, h: 0.45,
        fontSize: 11, color: C.navy, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
    });

    addFooter(s, part3Section);
  }

  // Phase detail helper
  function addPhaseSlide(phaseNum, title, period, items) {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    s.addText(`${phaseNum}（${period}）：${title}`, {
      x: 0.6, y: 0.3, w: 8.8, h: 0.55,
      fontSize: 20, color: C.navy, fontFace: "Calibri", bold: true, margin: 0,
    });
    addGoldAccent(s, 0.6, 0.95);

    items.forEach((item, i) => {
      const y = 1.2 + i * 0.82;
      // Domain label
      s.addShape("rect", {
        x: 0.6, y: y, w: 0.7, h: 0.65,
        fill: { color: C.navy },
      });
      s.addText(item.domain, {
        x: 0.6, y: y, w: 0.7, h: 0.65,
        fontSize: 10, color: C.gold, fontFace: "Calibri", bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      // Content card
      addCard(s, 1.45, y, 8.05, 0.65);
      s.addText(item.actions, {
        x: 1.6, y: y + 0.05, w: 6.5, h: 0.55,
        fontSize: 10, color: C.text, fontFace: "Calibri", margin: 0,
      });
      // Key impact
      s.addText(item.impact, {
        x: 8.1, y: y, w: 1.3, h: 0.65,
        fontSize: 8, color: C.gold, fontFace: "Calibri", align: "right", margin: 0,
      });
    });

    addFooter(s, part3Section);
  }

  // Phase 1
  addPhaseSlide("第一阶段", "筑基", "0-12个月", [
    { domain: "治理", actions: "组建高管团队（5-7人），明确议事规则和决策权限；设立月度战略研讨会机制", impact: "▸ 决策机制" },
    { domain: "战略", actions: "建立战略管理闭环：战略规划→年度解码→季度复盘；裁撤长尾SKU，聚焦3-4条核心产品线", impact: "▸ 战略解码" },
    { domain: "组织", actions: "总部职能部门能力评估和补强（优先：战略部、HR部、IT部）；建立S&OP机制解决产销矛盾", impact: "▸ 运营协同" },
    { domain: "人才", actions: "启动关键岗位人才盘点；建立后备干部培养计划（\"二级企业家\"项目）", impact: "▸ 人才储备" },
    { domain: "文化", actions: "开展管理层\"心智地图\"工作坊；试点授权机制（选取2-3个决策权下放）", impact: "▸ 授权试点" },
  ]);

  // Phase 2
  addPhaseSlide("第二阶段", "强体", "12-24个月", [
    { domain: "治理", actions: "高管团队运作成熟化（议题管理、决策记录、复盘机制）；系统性授权（业务/人事/预算权下放）", impact: "▸ 授权深化" },
    { domain: "战略", actions: "完成战略全闭环运行；新业务孵化机制建立（独立预算/决策/阶段性评审/快速止损）", impact: "▸ 创新机制" },
    { domain: "组织", actions: "战区能力均衡化（东区经验复制至南区/西区）；研发管理体系升级（平台化研发）", impact: "▸ 能力均衡" },
    { domain: "人才", actions: "绩效考核体系升级（\"做没做\"→\"做没做成\"，挂钩战略目标）；外部引进+内部培养双轨并进", impact: "▸ 考核升级" },
    { domain: "文化", actions: "企业文化梳理和重塑（提炼新的价值观表述）；建立内部信息透明化机制（月度经营数据全公司通报）", impact: "▸ 文化重塑" },
  ]);

  // Phase 3
  addPhaseSlide("第三阶段", "进化", "24-36个月", [
    { domain: "治理", actions: "高管团队完全成熟运作，企业家从日常决策中脱身聚焦战略和文化；治理体系从个人驱动转型完成", impact: "▸ 治理成熟" },
    { domain: "战略", actions: "战略管理成为组织肌肉记忆；业务组合动态优化（有进有出、有主有辅）；第二增长曲线启动", impact: "▸ 战略自主" },
    { domain: "组织", actions: "总部成为真正的赋能平台（战略引领+资源共享+能力建设）；全渠道运营体系成熟运转", impact: "▸ 平台赋能" },
    { domain: "人才", actions: "\"二级企业家\"梯队成型（每位战区/部门负责人都有合格继任者）；人才密度达到行业领先水平", impact: "▸ 梯队成熟" },
    { domain: "文化", actions: "新型企业文化内化为日常行为；\"信任赋能、战略引领、少即是多\"成为组织共识和默认态度", impact: "▸ 文化内化" },
  ]);

  // 结语
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.gold } });

    s.addText("结  语", {
      x: 0.8, y: 0.8, w: 8.4, h: 0.7,
      fontSize: 28, color: C.gold, fontFace: "Calibri", bold: true,
      align: "center", margin: 0,
    });

    s.addText("德施曼站在一个典型的企业成长十字路口。", {
      x: 0.8, y: 1.7, w: 8.4, h: 0.5,
      fontSize: 16, color: C.white, fontFace: "Calibri",
      align: "center", margin: 0,
    });

    s.addText([
      { text: "往前一步，是从机会成长到系统成长的跃迁——", options: { color: C.white, fontSize: 13 } },
      { text: "这条路很多企业走过，但更多的企业倒在了半路。", options: { color: C.textLight, fontSize: 13 } },
      { text: "\n\n倒下的不是因为方向不对，而是因为", options: { color: C.white, fontSize: 13 } },
      { text: "治理方式和组织能力跟不上企业规模的增长。", options: { color: C.gold, fontSize: 13, bold: true } },
    ], {
      x: 0.8, y: 2.4, w: 8.4, h: 1.2,
      fontFace: "Calibri", align: "center", margin: 0,
    });

    s.addShape("rect", { x: 3.5, y: 3.7, w: 3, h: 0.02, fill: { color: C.gold } });

    s.addText("真正的转型，从来不是修修补补，是重建企业的操作系统。", {
      x: 0.8, y: 3.9, w: 8.4, h: 0.6,
      fontSize: 16, color: C.gold, fontFace: "Calibri", bold: true, italic: true,
      align: "center", margin: 0,
    });

    s.addText("这是一场需要勇气、耐心和智慧的长跑。而这场长跑，应该从现在开始。", {
      x: 0.8, y: 4.7, w: 8.4, h: 0.5,
      fontSize: 12, color: C.white, fontFace: "Calibri",
      align: "center", margin: 0,
    });
  }

  // ============================================================
  // WRITE FILE
  // ============================================================
  await pres.writeFile({ fileName: "/Users/alex/WorkBuddy/2026-06-24-21-09-37/outputs/德施曼诊断报告.pptx" });
  console.log("PPT generated successfully!");
}

generate().catch(err => { console.error(err); process.exit(1); });

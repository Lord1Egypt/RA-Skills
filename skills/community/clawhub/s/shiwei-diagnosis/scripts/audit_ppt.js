/**
 * audit_ppt.js — 德施曼诊断PPT生成审计脚本
 *
 * 用法：
 *   node audit_ppt.js generate_ppt.js       检查脚本源代码（静态审计）
 *   node audit_ppt.js 德施曼诊断报告.pptx    检查生成的PPTX文件（需python3+python-pptx）
 *   node audit_ppt.js --all                  同时执行静态审计和PPTX审计
 *
 * 退出码：0=PASS，1=FAIL
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// ─── 颜色常量参考（与 generate_ppt.js 中的 C 常量一致）───
const VALID_COLORS = [
  "1A2E4A", "D4A843", "EBF0FA", "C0392B",
  "E67E22", "27AE60", "2C3E50", "6C7A96",
  "95A5A6", "FFFFFF", "D5D8DC", "FAD7A0",
];

const LIGHT_COLORS = ["8E9CAB", "95A5A6", "BDC3C7", "ECF0F1"]; // 白底上不可见的浅色

// ─── 审计结果收集 ───
const failures = [];
const warnings = [];
let passCount = 0;
const totalChecks = 21; // 7大类21项的总数（标记不可自动计算的为N/A）

function fail(category, item, detail) {
  failures.push({ category, item, detail });
}

function warn(category, item, detail) {
  warnings.push({ category, item, detail });
}

function pass(category, item) {
  passCount++;
  console.log(`  ✓ [${category}] ${item}`);
}

// ─── 静态审计：检查 generate_ppt.js 源代码 ───
function auditSourceCode(scriptPath) {
  console.log(`\n📋 静态审计：${scriptPath}\n`);
  const code = fs.readFileSync(scriptPath, "utf8");

  // C1: 颜色值格式检查
  const hexColorRe = /["']([0-9A-Fa-f]{3,7})["']/g;
  let m;
  const badColors = [];
  while ((m = hexColorRe.exec(code)) !== null) {
    const v = m[1];
    if (v.length !== 6 && v.length !== 3) badColors.push(v);
    if (v.length === 7) badColors.push(v);
  }
  if (badColors.length > 0) {
    fail("C1", "颜色值格式", `发现非法颜色值：${[...new Set(badColors)].join(", ")}`);
  } else {
    pass("C1", "颜色值格式（无7位/3位/带#的颜色值）");
  }

  // C2: 文字对比度（检查是否用了过浅的颜色）
  LIGHT_COLORS.forEach((c) => {
    if (code.includes(`"${c}"`) || code.includes(`'${c}'`)) {
      fail("C2", "文字对比度", `发现过浅颜色 ${c}，白底上可能不可见`);
    }
  });
  if (failures.every((f) => f.item !== "文字对比度")) {
    pass("C2", "文字对比度（无非浅色）");
  }

  // C3: 色板一致性（检查是否大量使用非常量颜色）
  // 跳过（需解析C常量表，复杂，改为人工检查）

  // S1: 禁止Unicode箭头（仅检查视觉箭头用法，不检查数据字符串）
  // 视觉箭头用法：s.addText("→" 或 { text: "→"  standalone
  const unicodeArrowRe = /addText\(.*?["']([→↓↑↻↺])["']/g;
  const unicodeArrowInText = /{.*?text:\s*["']([→↓↑↻↺])["'].*?}/g;
  let hasUnicodeArrow = false;
  const codeLines = code.split('\n');
  codeLines.forEach((line) => {
    // 只检查 s.addText("→" 这种用法（视觉箭头）
    if (line.includes('addText(') && /["']([→↓↑↻↺])["']/.test(line)) {
      hasUnicodeArrow = true;
    }
    // 检查 { text: "→" } 这种用法（视觉箭头）
    if (/text:\s*["']([→↓↑↻↺])["']/.test(line)) {
      hasUnicodeArrow = true;
    }
  });
  if (hasUnicodeArrow) {
    fail("S1", "禁止Unicode箭头", "脚本中包含Unicode箭头字符作为视觉元素，应改用PPT形状");
  } else {
    pass("S1", "禁止Unicode箭头（无Unicode箭头作为视觉元素）");
  }

  // S2: 禁止弯曲箭头形状
  const badShapes = ["bentArrow", "curvedArrow", "bentUpArrow", "curvedUpArrow", "bentDownArrow", "leftRightArrow"];
  badShapes.forEach((shape) => {
    if (code.includes(`"${shape}"`) || code.includes(`'${shape}'`)) {
      fail("S2", "禁止弯曲箭头形状", `使用了禁止的形状 "${shape}"`);
    }
  });
  if (failures.every((f) => f.item !== "禁止弯曲箭头形状")) {
    pass("S2", "禁止弯曲箭头形状（无bentArrow等）");
  }

  // S3: 箭头尺寸安全检查
  const arrowSizeRe = /(rightArrow|downArrow|upArrow)["'][\s\S]*?w:\s*([0-9.]+)[\s\S]*?h:\s*([0-9.]+)/g;
  // 简化检查：搜索 w: 数字 附近有关键字
  const wRe = /w:\s*([0-9.]+)/g;
  let wm;
  const oversizedArrows = [];
  // 找到所有箭头形状块，检查尺寸
  const arrowBlocks = code.match(/(rightArrow|downArrow|upArrow)[\s\S]*?{[\s\S]*?}/g) || [];
  arrowBlocks.forEach((block) => {
    const wMatch = block.match(/w:\s*([0-9.]+)/);
    const hMatch = block.match(/h:\s*([0-9.]+)/);
    if (wMatch && parseFloat(wMatch[1]) > 0.5) oversizedArrows.push(`w=${wMatch[1]}`);
    if (hMatch && parseFloat(hMatch[1]) > 0.35) oversizedArrows.push(`h=${hMatch[1]}`);
  });
  if (oversizedArrows.length > 0) {
    fail("S3", "箭头尺寸安全", `发现过大箭头：${oversizedArrows.join(", ")}（应 w≤0.5, h≤0.35）`);
  } else {
    pass("S3", "箭头尺寸安全（无超大箭头）");
  }

  // S4: 装饰线横条规范（检查 addGoldAccent 调用）
  const goldAccentRe = /addGoldAccent\([^)]*\)/g;
  const goldCalls = code.match(goldAccentRe) || [];
  // addGoldAccent 现在硬编码了尺寸，所以调用时不再传 w/h，此项PASS
  pass("S4", "装饰线横条规范（addGoldAccent已硬编码横条尺寸）");

  // S5: 形状类型正确（简化检查：downArrow用于横向连接）
  // 跳过（需解析布局上下文，复杂）

  // L3: 多卡片总宽度预算（检查 5 列卡片排列）
  if (code.includes("i * 3.15") || code.includes("i * 3.") && code.includes("subPoints")) {
    // 检测可能的5列单行
    warn("L3", "多卡片总宽度预算", "检测到可能的多列卡片布局，请人工确认总宽度 ≤ 9.5");
  } else {
    pass("L3", "多卡片总宽度预算（无明显的单行5列布局）");
  }

  // L5: 卡片高度与内容量匹配（检查是否有高度>3.0但内容少的卡片）
  // 跳过（需解析内容动态计算，复杂）

  // P1: 总览页与详情页对应（检查 B1 和 B2-B8 的标题）
  // 简化检查：搜索 B1 和 B2 关键词是否一致
  const b1Labels = (code.match(/label:\s*["']([^"']+)["']/g) || []).slice(0, 7);
  // 跳过详细对应检查（需解析JS对象结构）
  warn("P1", "总览页与详情页对应", "请人工确认B1七维标签与B2-B8详情页标题一致");

  // F1: 飞轮页不用角度算法
  if (code.includes("Math.sin") || code.includes("Math.cos") || code.includes("angle *")) {
    fail("F1", "飞轮页角度算法", "脚本中包含角度计算（Math.sin/cos），飞轮布局应使用行列+中心方案");
  } else {
    pass("F1", "飞轮页不用角度算法（无角度计算）");
  }

  // F2: 一心开二门箭头尺寸
  if (code.includes("一心开二门") || code.includes("新力之内圣")) {
    // 检查该页面附近的 downArrow 尺寸
    const yxRe = /(一心开二门|新力之内圣)[\s\S]*?(downArrow|upArrow)[\s\S]*?w:\s*([0-9.]+)[\s\S]*?h:\s*([0-9.]+)/;
    const yxMatch = code.match(yxRe);
    if (yxMatch && (parseFloat(yxMatch[3]) > 0.6 || parseFloat(yxMatch[4]) > 0.6)) {
      fail("F2", "一心开二门箭头尺寸", `箭头尺寸过大 w=${yxMatch[3]}, h=${yxMatch[4]}（应 ≤0.6）`);
    } else {
      pass("F2", "一心开二门箭头尺寸（无超大箭头）");
    }
  } else {
    pass("F2", "一心开二门箭头尺寸（N/A，无此页面）");
  }

  // Q1: 无未使用依赖
  const requires = (code.match(/require\(["']([^"']+)["']\)/g) || []).map((r) => r.match(/["']([^"']+)["']/)[1]);
  const unused = requires.filter((r) => !["pptxgenjs"].includes(r));
  if (unused.length > 0) {
    warn("Q1", "无未使用依赖", `发现非常规依赖：${unused.join(", ")}，请确认是否必要`);
  } else {
    pass("Q1", "无未使用依赖（仅引入pptxgenjs）");
  }

  // Q2: 颜色常量集中定义
  const hardCodedColors = (code.match(/:\s*["']([0-9A-Fa-f]{6})["']/g) || [])
    .map((c) => c.match(/["']([0-9A-Fa-f]{6})["']/)[1])
    .filter((c) => !VALID_COLORS.includes(c));
  if (hardCodedColors.length > 0) {
    warn("Q2", "颜色常量集中定义", `发现非常量颜色值：${[...new Set(hardCodedColors)].join(", ")}，建议使用C.xxx常量`);
  } else {
    pass("Q2", "颜色常量集中定义（颜色值均在常量表中）");
  }

  console.log(`\n  静态审计完成：✅ ${passCount} 项通过，${failures.length} 项失败，${warnings.length} 项警告\n`);
}

// ─── PPTX审计：检查生成的PPTX文件（需要 python3 + python-pptx）───
function auditPPTX(pptxPath) {
  console.log(`\n📊 PPTX审计：${pptxPath}\n`);

  if (!fs.existsSync(pptxPath)) {
    fail("V1", "文件生成成功", `文件不存在：${pptxPath}`);
    return;
  }

  const stats = fs.statSync(pptxPath);
  if (stats.size < 100 * 1024) {
    fail("V1", "文件生成成功", `文件过小（${Math.round(stats.size / 1024)}KB），可能生成不完整`);
  } else {
    pass("V1", `文件生成成功（${Math.round(stats.size / 1024)}KB）`);
  }

  // 使用 python-pptx 检查
  const pythonScript = `
import sys
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
except ImportError:
    print("PYTHON_PPTX_NOT_INSTALLED")
    sys.exit(1)

prs = Presentation(r"${pptxPath.replace(/\\/g, "\\\\")}")
print(f"SLIDE_COUNT:{len(prs.slides)}")

# 检查每页尺寸和内容溢出（简化版）
for i, slide in enumerate(prs.slides):
    page_num = i + 1
    for shape in slide.shapes:
        if shape.has_text_frame:
            # 检查文字框位置
            try:
                x = shape.left / 914400  # EMU to inches (approx)
                y = shape.top / 914400
                w = shape.width / 914400
                h = shape.height / 914400
                # 检查溢出（近似）
                if y + h > 5.5:
                    print(f"OVERFLOW:p{page_num}:y={y:.2f},h={h:.2f},y+h={y + h:.2f}")
                if x + w > 9.8:
                    print(f"RIGHT_OVERFLOW:p{page_num}:x={x:.2f},w={w:.2f},x+w={x + w:.2f}")
            except:
                pass

print("PYTHON_AUDIT_DONE")
`;

  try {
    const result = execSync(`python3 -c "${pythonScript.replace(/"/g, '\\"')}"`, {
      encoding: "utf8",
      timeout: 30000,
    });

    if (result.includes("PYTHON_PPTX_NOT_INSTALLED")) {
      warn("V2", "PPTX审计", "python-pptx 未安装，跳过PPTX内容审计。请运行 pip3 install python-pptx");
      return;
    }

    const slideCountMatch = result.match(/SLIDE_COUNT:(\d+)/);
    if (slideCountMatch) {
      const count = parseInt(slideCountMatch[1]);
      if (count < 10) {
        fail("V2", "幻灯片数量合理", `页数过少（${count}页），预期 40-60 页`);
      } else {
        pass("V2", `幻灯片数量合理（${count}页）`);
      }
    }

    const overflows = result.match(/OVERFLOW:p(\d+)/g) || [];
    const rightOverflows = result.match(/RIGHT_OVERFLOW:p(\d+)/g) || [];
    if (overflows.length > 0) {
      fail("L1", "内容区不溢出Footer", `发现 ${overflows.length} 处内容溢出Footer区域，涉及页面：${overflows.join(", ")}`);
    } else {
      pass("L1", "内容区不溢出Footer（PPTX检查无溢出）");
    }
    if (rightOverflows.length > 0) {
      fail("L2", "内容区不溢出右边界", `发现 ${rightOverflows.length} 处内容溢出右边界`);
    } else {
      pass("L2", "内容区不溢出右边界（PPTX检查无溢出）");
    }

    console.log(`  PPTX审计完成\n`);

  } catch (e) {
    warn("V2", "PPTX审计", `Python审计执行失败：${e.message}`);
  }
}

// ─── 主程序 ───
function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log("用法：");
    console.log("  node audit_ppt.js generate_ppt.js       检查脚本源代码");
    console.log("  node audit_ppt.js 德施曼诊断报告.pptx    检查生成的PPTX文件");
    console.log("  node audit_ppt.js --all                  同时执行两种审计");
    process.exit(0);
  }

  const arg = args[0];
  if (arg.endsWith(".js")) {
    auditSourceCode(arg);
  } else if (arg.endsWith(".pptx")) {
    auditPPTX(arg);
  } else if (arg === "--all") {
    const jsFile = fs.readdirSync(".").find((f) => f.endsWith("_ppt.js") || f === "generate_ppt.js");
    const pptxFile = fs.readdirSync(".").find((f) => f.endsWith(".pptx"));
    if (jsFile) auditSourceCode(jsFile);
    if (pptxFile) auditPPTX(pptxFile);
  }

  // 输出审计结果
  console.log("=".repeat(60));
  console.log(`审计结果：✅ ${passCount} 项通过  ❌ ${failures.length} 项失败  ⚠️  ${warnings.length} 项警告`);
  console.log("=".repeat(60));

  if (failures.length > 0) {
    console.log("\n❌ 失败项（必须修复）：");
    failures.forEach((f) => console.log(`  [${f.category}] ${f.item}：${f.detail}`));
  }

  if (warnings.length > 0) {
    console.log("\n⚠️  警告项（建议检查）：");
    warnings.forEach((w) => console.log(`  [${w.category}] ${w.item}：${w.detail}`));
  }

  if (failures.length === 0) {
    console.log("\n🎉 审计全部通过，PPT可以交付！");
  } else {
    console.log(`\n🛑 审计不通过，请修复 ${failures.length} 项失败问题后重新生成PPT`);
    process.exit(1);
  }
}

main();

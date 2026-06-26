/**
 * PPT生成器 - 使用 PptxGenJS 创建演示文稿
 * 
 * 用法: node generate_ppt.js [outline.json] [output.pptx]
 */
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// =============================================
// 配色方案
// =============================================
const THEMES = {
    dark_modern: {
        bg_dark: "1E2761",
        bg_light: "F8FAFC",
        primary: "4F46E5",    // Indigo
        secondary: "CADCFC",
        accent: "06B6D4",     // Cyan
        text_light: "FFFFFF",
        text_dark: "1E293B",
        muted: "64748B"
    },
    ocean: {
        bg_dark: "065A82",
        bg_light: "F0F9FF",
        primary: "1C7293",
        secondary: "21295C",
        accent: "00A896",
        text_light: "FFFFFF",
        text_dark: "1E293B",
        muted: "475569"
    },
    forest: {
        bg_dark: "2C5F2D",
        bg_light: "F7FEE7",
        primary: "97BC62",
        secondary: "2C5F2D",
        accent: "FBBF24",
        text_light: "FFFFFF",
        text_dark: "1E293B",
        muted: "4B5563"
    }
};

function createPresentation(outline, outputPath = "output/presentation/slides.pptx") {
    const theme = THEMES[outline.design?.theme] || THEMES.dark_modern;
    
    let pres = new pptxgen();
    pres.layout = "LAYOUT_16x9";
    pres.author = outline.author || "Student";
    pres.title = outline.slides?.[0]?.title || "Presentation";

    // ---- Helper Functions ----
    const makeShadow = () => ({ 
        type: "outer", blur: 6, offset: 2, 
        color: "000000", opacity: 0.15, angle: 135 
    });

    // ---- Title Slide ----
    function addTitleSlide(slideData) {
        let slide = pres.addSlide();
        slide.background = { color: theme.bg_dark };
        
        // Title
        slide.addText(slideData.title || "Presentation Title", {
            x: 0.8, y: 1.5, w: 8.4, h: 1.5,
            fontSize: 36, fontFace: "Arial",
            color: theme.text_light, bold: true,
            align: "left"
        });
        
        // Subtitle
        if (slideData.subtitle) {
            slide.addText(slideData.subtitle, {
                x: 0.8, y: 3.2, w: 8.4, h: 0.8,
                fontSize: 16, fontFace: "Arial",
                color: theme.secondary, align: "left"
            });
        }
        
        // Accent line
        slide.addShape(pres.shapes.RECTANGLE, {
            x: 0.8, y: 3.0, w: 2.0, h: 0.05,
            fill: { color: theme.accent }
        });
        
        // Add speaker notes
        if (slideData.notes) {
            slide.addNotes(slideData.notes);
        }
    }

    // ---- Content Slide ----
    function addContentSlide(slideData) {
        let slide = pres.addSlide();
        slide.background = { color: theme.bg_light };
        
        // Title bar
        slide.addShape(pres.shapes.RECTANGLE, {
            x: 0, y: 0, w: 10, h: 0.9,
            fill: { color: theme.bg_dark }
        });
        slide.addText(slideData.title, {
            x: 0.5, y: 0.1, w: 9, h: 0.7,
            fontSize: 20, fontFace: "Arial",
            color: theme.text_light, bold: true,
            margin: 0
        });
        
        // Content
        if (Array.isArray(slideData.points)) {
            let textItems = slideData.points.map((pt, i) => ({
                text: pt,
                options: { 
                    bullet: true, 
                    breakLine: i < slideData.points.length - 1,
                    fontSize: 14,
                    color: theme.text_dark
                }
            }));
            
            slide.addText(textItems, {
                x: 0.8, y: 1.2, w: 8.4, h: 3.8,
                fontFace: "Arial", valign: "top",
                paraSpaceAfter: 8
            });
        } else if (slideData.content) {
            slide.addText(slideData.content, {
                x: 0.8, y: 1.2, w: 8.4, h: 3.8,
                fontSize: 14, fontFace: "Arial",
                color: theme.text_dark, valign: "top"
            });
        }
        
        // Add speaker notes
        if (slideData.notes) {
            slide.addNotes(slideData.notes);
        }
    }

    // ---- Chart Slide ----
    function addChartSlide(slideData) {
        let slide = pres.addSlide();
        slide.background = { color: theme.bg_light };
        
        // Title bar
        slide.addShape(pres.shapes.RECTANGLE, {
            x: 0, y: 0, w: 10, h: 0.9,
            fill: { color: theme.bg_dark }
        });
        slide.addText(slideData.title, {
            x: 0.5, y: 0.1, w: 9, h: 0.7,
            fontSize: 20, fontFace: "Arial",
            color: theme.text_light, bold: true,
            margin: 0
        });
        
        // Image/Figure placeholder
        if (slideData.image) {
            slide.addImage({
                path: slideData.image,
                x: 1.5, y: 1.2, w: 7, h: 4,
                sizing: { type: "contain", w: 7, h: 4 }
            });
        } else {
            // Placeholder box
            slide.addShape(pres.shapes.RECTANGLE, {
                x: 1.5, y: 1.2, w: 7, h: 4,
                fill: { color: "F1F5F9" },
                line: { color: theme.muted, width: 1, dashType: "dash" }
            });
            slide.addText("[Chart / Figure]", {
                x: 1.5, y: 2.8, w: 7, h: 1,
                fontSize: 16, color: theme.muted,
                align: "center"
            });
        }
        
        if (slideData.notes) {
            slide.addNotes(slideData.notes);
        }
    }

    // ---- Q&A Slide ----
    function addQASlide(slideData) {
        let slide = pres.addSlide();
        slide.background = { color: theme.bg_dark };
        
        slide.addText("Q & A", {
            x: 0, y: 1.5, w: 10, h: 2,
            fontSize: 48, fontFace: "Arial",
            color: theme.text_light, bold: true,
            align: "center"
        });
        
        slide.addText(slideData.content || "Thank you for listening!", {
            x: 0, y: 3.5, w: 10, h: 1,
            fontSize: 18, fontFace: "Arial",
            color: theme.secondary, align: "center"
        });
    }

    // ---- Build Slides ----
    const slides = outline.slides || [];
    
    slides.forEach((slideData, index) => {
        switch(slideData.type) {
            case "title":
                addTitleSlide(slideData);
                break;
            case "chart":
            case "figure":
                addChartSlide(slideData);
                break;
            case "qa":
                addQASlide(slideData);
                break;
            default:
                addContentSlide(slideData);
                break;
        }
    });

    // ---- Save ----
    const outDir = path.dirname(outputPath);
    if (!fs.existsSync(outDir)) {
        fs.mkdirSync(outDir, { recursive: true });
    }
    
    pres.writeFile({ fileName: outputPath })
        .then(() => console.log(`  ✅ PPT已生成: ${outputPath}`))
        .catch(err => console.error(`  ❌ Error: ${err}`));
}

// ---- Main ----
if (require.main === module) {
    const args = process.argv.slice(2);
    const jsonPath = args[0] || "output/presentation/presentation_outline.json";
    const outputPath = args[1] || "output/presentation/slides.pptx";
    
    if (fs.existsSync(jsonPath)) {
        const outline = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
        createPresentation(outline, outputPath);
    } else {
        // Demo
        const demo = {
            design: { theme: "dark_modern" },
            slides: [
                { type: "title", title: "Demo Presentation", subtitle: "AI Agent Workflow" },
                { type: "content", title: "Outline", points: ["Introduction", "Methodology", "Results", "Conclusion"] },
                { type: "content", title: "Key Findings", content: "Our analysis shows significant improvement..." },
                { type: "chart", title: "Results", image: null },
                { type: "qa", content: "Thank you!" }
            ]
        };
        createPresentation(demo, outputPath);
    }
}

module.exports = { createPresentation, THEMES };

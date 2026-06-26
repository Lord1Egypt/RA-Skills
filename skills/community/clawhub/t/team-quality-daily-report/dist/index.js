import fs from "fs";
import path from "path";
import { connectBrowser } from "@bondli-skills/shared/browser";
import { today, yesterday } from "@bondli-skills/shared/date";
import { capturePayload, requestAPI } from "./utils/api.js";
import { parseData } from "./utils/parser.js";
import { compareData } from "./utils/compare.js";
import { generateReport } from "./utils/report.js";
const baseDir = path.join(process.env.HOME || "~", "/openclaw-skill-data/team-quality-daily-report/");
const configPath = path.join(baseDir, "config.json");
async function main() {
    // 确保目录存在
    if (!fs.existsSync(baseDir)) {
        try {
            fs.mkdirSync(baseDir, { recursive: true });
            console.log(`已创建配置目录: ${baseDir}`);
        }
        catch (error) {
            console.error(`创建配置目录失败: ${error.message}`);
            process.exit(1);
        }
    }
    if (!fs.existsSync(configPath)) {
        console.error("错误: 配置文件不存在");
        console.error(`配置文件路径: ${configPath}`);
        console.error("\n请执行以下命令创建配置文件:");
        // 获取当前技能的根目录
        const skillRoot = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
        const examplePath = path.join(skillRoot, "config.example.json");
        console.error(`\n  cp ${examplePath} ${configPath}`);
        console.error("\n然后编辑配置文件填入你的飞书报表信息");
        process.exit(1);
    }
    const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    const reportConfig = config.reports[0];
    console.log("启动浏览器...");
    const { browser, page } = await connectBrowser();
    console.log("捕获 API payload...");
    const payload = await capturePayload(page, reportConfig);
    console.log("请求数据接口...");
    const apiResult = await requestAPI(page, reportConfig.dataAPI, payload);
    if (!apiResult || apiResult.length === 0) {
        throw new Error("无法获取数据，可能是数据还没有生成");
    }
    console.log("解析数据...");
    const parsedData = parseData(apiResult, reportConfig.column);
    const todayFile = path.join(baseDir, `${today()}.json`);
    fs.writeFileSync(todayFile, JSON.stringify(parsedData, null, 2));
    console.log("今日数据已保存");
    const yesterdayFile = path.join(baseDir, `${yesterday()}.json`);
    let compareResult = null;
    if (fs.existsSync(yesterdayFile)) {
        const yesterdayData = JSON.parse(fs.readFileSync(yesterdayFile, "utf-8"));
        compareResult = compareData(parsedData, yesterdayData);
    }
    const report = generateReport(parsedData, compareResult, reportConfig.column);
    const reportFile = path.join(baseDir, `${today()}.md`);
    fs.writeFileSync(reportFile, report);
    console.log("日报生成:", reportFile);
    await browser.close();
    process.exit(0);
}
main().catch(err => {
    if (err.message === "LOGIN_REQUIRED") {
        console.error("\n程序终止：需要登录系统\n");
    }
    else {
        console.error("\n程序运行失败:");
        console.error(err);
    }
    process.exit(1);
});
//# sourceMappingURL=index.js.map
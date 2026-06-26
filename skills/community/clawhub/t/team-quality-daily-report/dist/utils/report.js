export function generateReport(todayData, diff, column) {
    let md = "# 团队质量日报\n\n";
    md += "## 今日指标\n\n";
    Object.entries(todayData).forEach(([k, v]) => {
        md += `- ${column[k] || k}: ${v}\n`;
    });
    md += "\n";
    if (diff && diff.length > 0) {
        md += "## 与昨日变化\n\n";
        diff.forEach(d => {
            const percent = (d.change * 100).toFixed(2);
            md += `- ${d.field} 变化 ${percent}%\n`;
        });
    }
    md += "\n## 结论\n\n";
    md += "需要结合代码提交、发布记录和故障情况进行进一步分析。\n";
    return md;
}
//# sourceMappingURL=report.js.map
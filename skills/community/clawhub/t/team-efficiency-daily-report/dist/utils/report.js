import { today } from "@bondli-skills/shared/date";
function calcDays(dateStr) {
    if (!dateStr)
        return 0;
    const start = new Date(dateStr);
    const now = new Date();
    return Math.floor((now.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
}
function is211(totalDays) {
    const costTime = Number(String(totalDays ?? "").replace(/[^\d.]/g, "")) || 0;
    return costTime <= 14;
}
export function generateReport(allData) {
    const deliveredList = (allData[0] || []);
    const inProgressList = (allData[1] || []);
    const subTaskList = (allData[2] || []);
    let md = `# ${today()} 团队效能日报\n\n`;
    md += `## 一、当天交付的需求情况\n\n`;
    const count = deliveredList.length;
    md += `- 产品需求数：**${count}**\n`;
    if (count > 0) {
        const days = deliveredList.map(r => Number(String(r.totalDays ?? "").replace(/[^\d.]/g, "")) || 0);
        const maxDays = Math.max(...days);
        const avgDays = (days.reduce((a, b) => a + b, 0) / count).toFixed(1);
        const reached211 = deliveredList.filter(r => is211(r.totalDays));
        const rate = ((reached211.length / count) * 100).toFixed(1);
        md += `- 最长需求交付时长：**${maxDays} 天**\n`;
        md += `- 平均交付时长：**${avgDays} 天**\n`;
        md += `- 达成 211 的占比：**${rate}%**（${reached211.length}/${count}）\n`;
        if (reached211.length > 0) {
            md += `\n**达成 211 的需求列表：**\n\n`;
            md += `| 需求ID | 需求名称 | 总耗时(天) | 负责人 |\n`;
            md += `|--------|----------|------------|--------|\n`;
            reached211.forEach(r => {
                md += `| ${r.teamId ? `[${r.teamId}](https://team.corp.kuaishou.com/task/${r.teamId})` : "-"} | ${r.name || "-"} | ${r.totalDays || "-"} | ${r.owner || "-"} |\n`;
            });
        }
        const notReached = deliveredList.filter(r => !is211(r.totalDays));
        if (notReached.length > 0) {
            md += `\n**未达成 211 的需求列表：**\n\n`;
            md += `| 需求ID | 需求名称 | 总耗时(天) | 负责人 |\n`;
            md += `|--------|----------|------------|--------|\n`;
            notReached.forEach(r => {
                md += `| ${r.teamId ? `[${r.teamId}](https://team.corp.kuaishou.com/task/${r.teamId})` : "-"} | ${r.name || "-"} | ${r.totalDays || "-"} | ${r.owner || "-"} |\n`;
            });
        }
        else {
            md += `\n所有需求均达成 211。\n`;
        }
    }
    else {
        md += `\n当天暂无交付需求。\n`;
    }
    md += `\n---\n\n`;
    md += `## 二、交付中的主R产品需求列表\n\n`;
    if (inProgressList.length > 0) {
        md += `| 需求ID | 需求名称 | 创建时间 | 状态 | 开始开发时间 | 已耗时(天) | 预计剩余(天) |\n`;
        md += `|--------|----------|------|----------|------------|----------------|\n`;
        inProgressList.forEach(r => {
            const usedDays = r.devTime ? Math.floor((Date.now() - new Date(r.devTime).getTime()) / (1000 * 60 * 60 * 24)) : 0;
            const remaining = Math.max(0, 14 - usedDays);
            md += `| ${r.teamId ? `[${r.teamId}](https://team.corp.kuaishou.com/task/${r.teamId})` : "-"} | ${r.name || "-"} | ${r.createTime || "-"} | ${r.status || "-"} | ${r.devTime || "-"} | ${usedDays} | ${remaining} |\n`;
        });
    }
    else {
        md += `当前暂无交付中的主R产品需求。\n`;
    }
    md += `\n---\n\n`;
    md += `## 三、交付中产品子任务列表（创建超 14 天）\n\n`;
    const overdue = subTaskList
        .filter(r => calcDays(r.createTime) > 14)
        .sort((a, b) => new Date(a.createTime ?? "").getTime() - new Date(b.createTime ?? "").getTime());
    if (overdue.length > 0) {
        md += `| 需求ID | 需求名称 | 状态 | 创建时间 | 已创建(天) | 负责人 |\n`;
        md += `|--------|----------|------|----------|------------|--------|\n`;
        overdue.forEach(r => {
            const age = calcDays(r.createTime);
            md += `| ${r.teamId ? `[${r.teamId}](https://team.corp.kuaishou.com/task/${r.teamId})` : "-"} | ${r.name || "-"} | ${r.status || "-"} | ${r.createTime || "-"} | ${age} | ${r.owner || "-"} |\n`;
        });
    }
    else {
        md += `当前无创建超过 14 天的产品子任务。\n`;
    }
    return md;
}
//# sourceMappingURL=report.js.map
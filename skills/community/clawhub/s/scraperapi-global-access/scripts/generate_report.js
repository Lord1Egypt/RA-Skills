const fs = require('fs');

// 读取进度文件
const progressData = JSON.parse(fs.readFileSync('progress.json', 'utf8'));

// 生成报告
const report = {
    generatedAt: new Date().toISOString(),
    summary: {
        totalVisits: progressData.results.length,
        successfulVisits: progressData.results.filter(r => r.success).length,
        failedVisits: progressData.results.filter(r => !r.success).length,
        successRate: ((progressData.results.filter(r => r.success).length / progressData.results.length) * 100).toFixed(1) + '%'
    },
    globalCoverage: {
        countries: [...new Set(progressData.results.map(r => r.country))].length,
        regions: [...new Set(progressData.results.filter(r => r.success).map(r => r.region))].length
    },
    results: progressData.results,
    performanceData: progressData.performanceData.sort((a, b) => a.responseTime - b.responseTime)
};

// 保存 JSON 报告
fs.writeFileSync('exploration_report.json', JSON.stringify(report, null, 2));
console.log('✅ 报告已保存: exploration_report.json');

// 保存 CSV
const csvHeader = 'Country,Region,Page,Status,ResponseTime,Title,Timestamp\n';
const csvData = progressData.results.map(r => 
    `${r.country},${r.region},${r.page},${r.success ? 'Success' : 'Failed'},${r.responseTime},"${(r.title || r.error || '').replace(/"/g, '""')}",${r.timestamp}`
).join('\n');
fs.writeFileSync('exploration_results.csv', csvHeader + csvData);
console.log('✅ CSV已保存: exploration_results.csv');

// 保存性能数据
const perfCsv = 'Country,Region,ResponseTime,Success\n';
const perfData = progressData.performanceData.map(r => 
    `${r.country},${r.region},${r.responseTime},${r.success}`
).join('\n');
fs.writeFileSync('performance_data.csv', perfCsv + perfData);
console.log('✅ 性能数据已保存: performance_data.csv');

// 打印摘要
console.log('\n' + '='.repeat(70));
console.log('📊 全球覆盖测试报告');
console.log('='.repeat(70));
console.log(`\n✅ 总访问次数: ${report.summary.totalVisits}`);
console.log(`✅ 成功: ${report.summary.successfulVisits}`);
console.log(`❌ 失败: ${report.summary.failedVisits}`);
console.log(`📈 成功率: ${report.summary.successRate}`);
console.log(`🌍 覆盖国家: ${report.globalCoverage.countries}`);
console.log(`🌎 覆盖地区: ${report.globalCoverage.regions}`);

console.log('\n📍 各地区成功率:');
const regionStats = {};
progressData.results.filter(r => r.success).forEach(r => {
    regionStats[r.region] = (regionStats[r.region] || 0) + 1;
});
Object.entries(regionStats).forEach(([region, count]) => {
    console.log(`   ${region}: ${count} 次成功访问`);
});

console.log('\n⚡ 访问速度排名 (Top 10最快):');
report.performanceData.slice(0, 10).forEach((item, i) => {
    console.log(`   ${i + 1}. ${item.country}: ${item.responseTime}ms`);
});

console.log('\n⚡ 访问速度排名 (Top 10最慢):');
report.performanceData.slice(-10).reverse().forEach((item, i) => {
    console.log(`   ${i + 1}. ${item.country}: ${item.responseTime}ms`);
});

console.log('\n' + '='.repeat(70));
console.log('✨ 报告生成完成！');

const axios = require('axios');
const fs = require('fs');

const SCRAPER_API_KEY = 'fd18228b13dd001b794a8c74e9a35667';
const BASE_URL = 'https://faceswap.cool';

// 25个国家
const countries = [
    { country: '美国', code: 'us', region: '北美' },
    { country: '加拿大', code: 'ca', region: '北美' },
    { country: '墨西哥', code: 'mx', region: '北美' },
    { country: '巴西', code: 'br', region: '南美' },
    { country: '阿根廷', code: 'ar', region: '南美' },
    { country: '智利', code: 'cl', region: '南美' },
    { country: '英国', code: 'gb', region: '欧洲' },
    { country: '德国', code: 'de', region: '欧洲' },
    { country: '法国', code: 'fr', region: '欧洲' },
    { country: '意大利', code: 'it', region: '欧洲' },
    { country: '西班牙', code: 'es', region: '欧洲' },
    { country: '荷兰', code: 'nl', region: '欧洲' },
    { country: '瑞典', code: 'se', region: '欧洲' },
    { country: '波兰', code: 'pl', region: '欧洲' },
    { country: '日本', code: 'jp', region: '亚洲' },
    { country: '韩国', code: 'kr', region: '亚洲' },
    { country: '新加坡', code: 'sg', region: '亚洲' },
    { country: '印度', code: 'in', region: '亚洲' },
    { country: '印尼', code: 'id', region: '亚洲' },
    { country: '泰国', code: 'th', region: '亚洲' },
    { country: '澳大利亚', code: 'au', region: '大洋洲' },
    { country: '新西兰', code: 'nz', region: '大洋洲' },
    { country: '南非', code: 'za', region: '非洲' },
    { country: '埃及', code: 'eg', region: '非洲' },
    { country: '尼日利亚', code: 'ng', region: '非洲' },
];

const userJourneys = [
    ['/', '首页'],
    ['/tools/face-swap', '换脸工具'],
    ['/pricing', '价格页'],
];

class FaceswapExplorer {
    constructor() {
        this.results = [];
        this.performanceData = [];
        this.startTime = new Date();
        this.loadProgress();
    }
    
    loadProgress() {
        try {
            if (fs.existsSync('progress.json')) {
                const data = JSON.parse(fs.readFileSync('progress.json', 'utf8'));
                this.results = data.results || [];
                this.performanceData = data.performanceData || [];
                console.log(`📂 加载已有进度: ${this.results.length} 条记录`);
            }
        } catch (error) {
            console.log('📂 无进度文件，从头开始');
        }
    }
    
    saveProgress() {
        try {
            fs.writeFileSync('progress.json', JSON.stringify({
                results: this.results,
                performanceData: this.performanceData,
                lastUpdate: new Date().toISOString()
            }, null, 2));
        } catch (error) {
            console.error('保存进度失败:', error.message);
        }
    }
    
    async visitPage(country, page, renderJS = true) {
        const fullUrl = BASE_URL + page;
        const startTime = Date.now();
        
        try {
            const params = {
                api_key: SCRAPER_API_KEY,
                url: fullUrl,
                country_code: country.code,
                render: renderJS,
                session_number: Math.floor(Math.random() * 100000)
            };
            
            const response = await axios.get('http://api.scraperapi.com', {
                params,
                timeout: 90000
            });
            
            const responseTime = Date.now() - startTime;
            const title = response.data.match(/<title>(.*?)<\/title>/)?.[1]?.replace(/&amp;/g, '&') || 'N/A';
            const size = response.data.length;
            
            return {
                success: true,
                country: country.country,
                countryCode: country.code,
                region: country.region,
                page: page,
                title: title.substring(0, 50),
                status: response.status,
                size: size,
                responseTime: responseTime,
                timestamp: new Date().toISOString()
            };
            
        } catch (error) {
            const responseTime = Date.now() - startTime;
            console.error(`   ⚠️  错误: ${error.message}`);
            
            return {
                success: false,
                country: country.country,
                countryCode: country.code,
                region: country.region,
                page: page,
                error: error.message,
                responseTime: responseTime,
                timestamp: new Date().toISOString()
            };
        }
    }
    
    async simulateUserJourney(country) {
        console.log(`\n🎭 ${country.country} - 模拟用户旅程...`);
        const journeyResults = [];
        
        for (const [page, name] of userJourneys) {
            const waitTime = Math.random() * 3000 + 3000;
            await new Promise(resolve => setTimeout(resolve, waitTime));
            
            const result = await this.visitPage(country, page, true);
            result.journeyStep = name;
            journeyResults.push(result);
            
            if (result.success) {
                console.log(`   ✅ ${name}: ${result.responseTime}ms`);
            } else {
                console.log(`   ❌ ${name}: ${result.error}`);
            }
            
            this.saveProgress();
        }
        
        return journeyResults;
    }
    
    async runGlobalCoverage() {
        console.log('\n🌍 开始全球覆盖测试 (25个国家)...\n');
        
        const completedCountries = new Set(
            this.results
                .filter(r => r.page === '/')
                .map(r => r.countryCode)
        );
        
        for (const country of countries) {
            if (completedCountries.has(country.code)) {
                console.log(`⏭️  ${country.country} - 已完成，跳过`);
                continue;
            }
            
            console.log(`🌍 ${country.country} (${country.region})...`);
            
            try {
                const result = await this.visitPage(country, '/', true);
                this.results.push(result);
                this.performanceData.push({
                    country: country.country,
                    region: country.region,
                    responseTime: result.responseTime,
                    success: result.success
                });
                
                const progress = this.results.filter(r => r.page === '/').length;
                const successCount = this.results.filter(r => r.success && r.page === '/').length;
                console.log(`   ${progress}/25 完成 | ✅ ${successCount} 成功`);
                
                this.saveProgress();
                
                await new Promise(resolve => setTimeout(resolve, 5000));
                
            } catch (error) {
                console.error(`   ❌ 致命错误: ${error.message}`);
                this.saveProgress();
                break;
            }
        }
    }
    
    async runUserBehaviorSimulation() {
        console.log('\n\n🎭 开始用户行为模拟测试...\n');
        
        const sampleCountries = [
            { country: '美国', code: 'us', region: '北美' },
            { country: '英国', code: 'gb', region: '欧洲' },
            { country: '日本', code: 'jp', region: '亚洲' },
            { country: '巴西', code: 'br', region: '南美' },
            { country: '澳大利亚', code: 'au', region: '大洋洲' },
            { country: '南非', code: 'za', region: '非洲' },
        ];
        
        for (const country of sampleCountries) {
            try {
                const journeyResults = await this.simulateUserJourney(country);
                this.results.push(...journeyResults);
                this.saveProgress();
            } catch (error) {
                console.error(`${country.country} 旅程失败:`, error.message);
            }
        }
    }
    
    generateReport() {
        const report = {
            generatedAt: new Date().toISOString(),
            summary: {
                totalVisits: this.results.length,
                successfulVisits: this.results.filter(r => r.success).length,
                failedVisits: this.results.filter(r => !r.success).length,
                successRate: ((this.results.filter(r => r.success).length / this.results.length) * 100).toFixed(1) + '%'
            },
            globalCoverage: {
                countries: [...new Set(this.results.map(r => r.country))].length,
                regions: [...new Set(this.results.filter(r => r.success).map(r => r.region))].length
            },
            results: this.results,
            performanceData: this.performanceData.sort((a, b) => a.responseTime - b.responseTime)
        };
        
        return report;
    }
    
    printSummary(report) {
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
        this.results.filter(r => r.success).forEach(r => {
            regionStats[r.region] = (regionStats[r.region] || 0) + 1;
        });
        Object.entries(regionStats).forEach(([region, count]) => {
            console.log(`   ${region}: ${count} 次成功访问`);
        });
        
        if (this.performanceData.length > 0) {
            console.log('\n⚡ 访问速度排名 (Top 10最快):');
            report.performanceData.slice(0, Math.min(10, report.performanceData.length)).forEach((item, i) => {
                console.log(`   ${i + 1}. ${item.country}: ${item.responseTime}ms`);
            });
            
            console.log('\n⚡ 访问速度排名 (Top 10最慢):');
            report.performanceData.slice(-Math.min(10, report.performanceData.length)).reverse().forEach((item, i) => {
                console.log(`   ${i + 1}. ${item.country}: ${item.responseTime}ms`);
            });
        }
        
        console.log('\n' + '='.repeat(70));
    }
    
    saveResults(report) {
        fs.writeFileSync('exploration_report.json', JSON.stringify(report, null, 2));
        console.log('\n💾 报告已保存: exploration_report.json');
        
        const csvHeader = 'Country,Region,Page,Status,ResponseTime,Title,Timestamp\n';
        const csvData = this.results.map(r => 
            `${r.country},${r.region},${r.page},${r.success ? 'Success' : 'Failed'},${r.responseTime},"${(r.title || r.error || '').replace(/"/g, '""')}",${r.timestamp}`
        ).join('\n');
        fs.writeFileSync('exploration_results.csv', csvHeader + csvData);
        console.log('💾 CSV已保存: exploration_results.csv');
        
        const perfCsv = 'Country,Region,ResponseTime,Success\n';
        const perfData = this.performanceData.map(r => 
            `${r.country},${r.region},${r.responseTime},${r.success}`
        ).join('\n');
        fs.writeFileSync('performance_data.csv', perfCsv + perfData);
        console.log('💾 性能数据已保存: performance_data.csv');
    }
}

async function main() {
    console.log('🚀 faceswap.cool 全球探索系统 v2 (带断点续传)');
    console.log('='.repeat(70));
    console.log('功能: 25国覆盖 + 用户行为模拟 + 性能监控 + 错误恢复');
    console.log(`开始时间: ${new Date().toLocaleString()}`);
    
    const explorer = new FaceswapExplorer();
    
    try {
        await explorer.runGlobalCoverage();
        await explorer.runUserBehaviorSimulation();
        
        const report = explorer.generateReport();
        explorer.printSummary(report);
        explorer.saveResults(report);
        
        console.log('\n✨ 探索完成！');
        console.log(`结束时间: ${new Date().toLocaleString()}`);
        
    } catch (error) {
        console.error('\n❌ 程序异常:', error.message);
        console.log('💾 进度已保存，可重新运行继续');
        process.exit(1);
    }
}

main();

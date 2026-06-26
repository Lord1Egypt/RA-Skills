#!/usr/bin/env node
/**
 * SystemTemp - 系統溫度監控工具
 * 監控系統溫度、CPU 狀態、風扇轉速等硬體資訊
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

const DATA_DIR = path.join(process.env.HOME || '/home/ckk', 'openclaw_workspace', 'data');
const CONFIG_DIR = path.join(process.env.HOME || '/home/ckk', 'openclaw_workspace', 'config');
const LOG_FILE = path.join(DATA_DIR, 'systemTemp.log');
const REPORTS_DIR = path.join(DATA_DIR, 'reports');
const ALERT_CONFIG = path.join(CONFIG_DIR, 'tempAlerts.json');

// 初始化
function init() {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true });
    if (!fs.existsSync(REPORTS_DIR)) fs.mkdirSync(REPORTS_DIR, { recursive: true });
    if (!fs.existsSync(ALERT_CONFIG)) {
        fs.writeFileSync(ALERT_CONFIG, JSON.stringify({ enabled: false, threshold: 80 }, null, 2));
    }
    if (!fs.existsSync(LOG_FILE)) {
        fs.writeFileSync(LOG_FILE, '');
    }
}

// 獲取所有感測器
function getSensors() {
    const sensors = [];
    for (let i = 0; i <= 9; i++) {
        try {
            const typePath = `/sys/class/thermal/thermal_zone${i}/type`;
            const tempPath = `/sys/class/thermal/thermal_zone${i}/temp`;
            
            if (fs.existsSync(typePath) && fs.existsSync(tempPath)) {
                const type = fs.readFileSync(typePath, 'utf8').trim();
                const temp = parseInt(fs.readFileSync(tempPath, 'utf8').trim()) || 0;
                const temp_c = Math.floor(temp / 1000);
                const temp_f = Math.floor(temp_c * 9/5 + 32);
                
                sensors.push({
                    index: i,
                    type: type,
                    temp_c,
                    temp_f,
                    raw: temp
                });
            }
        } catch (e) {
            // 忽略錯誤
        }
    }
    return sensors;
}

// 獲取 CPU 溫度
function getCpuTemp() {
    const sensors = getSensors();
    return sensors.filter(s => 
        s.type.includes('cpu') || 
        s.type.includes('acpitz') || 
        s.type.includes('package') ||
        s.type.includes('x86')
    );
}

// 計算平均溫度
function getAverageTemp() {
    const sensors = getSensors();
    if (sensors.length === 0) return null;
    
    const sum = sensors.reduce((acc, s) => acc + s.temp_c, 0);
    return Math.round(sum / sensors.length);
}

// 獲取溫度狀態
function getTempStatus(avgTemp) {
    if (avgTemp > 85) return { status: 'danger', icon: '🔥', text: '危險高溫' };
    if (avgTemp > 75) return { status: 'warning', icon: '⚠️', text: '高溫警報' };
    if (avgTemp > 65) return { status: 'caution', icon: '🟡', text: '溫度偏高' };
    return { status: 'ok', icon: '✅', text: '溫度正常' };
}

// 檢查告警
function checkAlert(avgTemp) {
    try {
        const config = JSON.parse(fs.readFileSync(ALERT_CONFIG, 'utf8'));
        if (!config.enabled || !config.threshold) return null;
        
        if (avgTemp >= config.threshold) {
            return {
                triggered: true,
                threshold: config.threshold,
                current: avgTemp
            };
        }
    } catch (e) {
        // 忽略
    }
    return null;
}

// 記錄溫度
function logTemperature() {
    const sensors = getSensors();
    if (sensors.length === 0) return;
    
    const timestamp = new Date().toISOString();
    const sum = sensors.reduce((acc, s) => acc + s.temp_c, 0);
    const avg = Math.round(sum / sensors.length);
    
    const logEntry = `
====== ${new Date().toLocaleString('zh-TW')} ======
📅 時間：${timestamp}

`;
    
    sensors.forEach(s => {
        logEntry += `${s.index + 1}. ${s.type}: ${s.temp_c}°C / ${s.temp_f}°F\n`;
    });
    
    logEntry += `\n📊 平均溫度：${avg}°C\n\n`;
    
    fs.appendFileSync(LOG_FILE, logEntry);
    
    // 更新 README
    updateReadme(avg);
}

// 更新 README
function updateReadme(avgTemp) {
    try {
        let readme = fs.readFileSync(path.join(DATA_DIR, 'systemTemp.md'), 'utf8');
        const lastUpdate = readme.match(/最後更新：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/);
        
        if (lastUpdate) {
            const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
            readme = readme.replace(lastUpdate[1], now);
            fs.writeFileSync(path.join(DATA_DIR, 'systemTemp.md'), readme);
        } else {
            // 如果找不到，添加新的
            readme += `\n_最後更新：${new Date().toISOString().replace('T', ' ').substring(0, 19)}_\n`;
            fs.writeFileSync(path.join(DATA_DIR, 'systemTemp.md'), readme);
        }
        
        // 更新最新記錄
        const latestEntry = `
====== ${new Date().toLocaleString('zh-TW')} ======
📅 時間：${new Date().toISOString()}
平均溫度：${avgTemp}°C
`;
        fs.appendFileSync(LOG_FILE, latestEntry);
    } catch (e) {
        // 忽略
    }
}

// 格式化感測器列表
function formatSensors(sensors, showStatus = true) {
    let output = '';
    const avg = getAverageTemp();
    
    sensors.forEach((s, i) => {
        const tempStatus = s.temp_c >= 85 ? '🔥' : s.temp_c >= 75 ? '⚠️' : s.temp_c >= 65 ? '🟡' : '✅';
        output += `${i + 1}. ${s.type.padEnd(15)} ${String(s.temp_c).padStart(3)}°C / ${String(s.temp_f).padStart(3)}°F ${tempStatus}\n`;
    });
    
    if (showStatus && avg !== null) {
        output += `\n📊 平均溫度：${avg}°C`;
        const status = getTempStatus(avg);
        output += ` (${status.text})`;
    }
    
    return output;
}

// 主指令處理
function main() {
    init();
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'all':
        case '所有':
        case 'status':
        case '狀態':
        case '': {
            const sensors = getSensors();
            const avg = getAverageTemp();
            const status = getTempStatus(avg);
            const alert = checkAlert(avg);
            
            let output = '🌡️ 系統溫度監控\n\n';
            output += formatSensors(sensors) + '\n';
            output += `\n${status.icon} 狀態：${status.text}`;
            
            if (avg !== null) {
                output += ` (平均：${avg}°C)`;
            }
            
            if (alert) {
                output += `\n\n⚠️ 告警：已超過 ${alert.threshold}°C 閾值！`;
            }
            
            console.log(output);
            break;
        }
        
        case 'cpu':
        case 'cpu':
        case '處理器': {
            const sensors = getSensors();
            const cpuSensors = getCpuTemp();
            
            if (cpuSensors.length === 0) {
                console.log('🔍 未找到 CPU 相關感測器');
            } else {
                let output = '🔥 CPU 溫度\n\n';
                cpuSensors.forEach((s, i) => {
                    output += `${i + 1}. ${s.type}: ${s.temp_c}°C / ${s.temp_f}°F\n`;
                });
                console.log(output);
            }
            break;
        }
        
        case 'sensors':
        case '感測器':
        case 'list':
        case '列表': {
            const sensors = getSensors();
            const verbose = args[1] === '-v' || args[1] === '--verbose';
            
            if (sensors.length === 0) {
                console.log('🔍 未找到溫度感測器');
            } else {
                let output = '📡 溫度感測器列表\n\n';
                
                sensors.forEach((s, i) => {
                    output += `${i + 1}. **${s.type}** (thermal_zone${s.index})\n`;
                    if (verbose) {
                        output += `   原始值：${s.raw}m°C\n`;
                        output += `   溫度：${s.temp_c}°C / ${s.temp_f}°F\n`;
                    }
                    output += '\n';
                });
                
                const avg = getAverageTemp();
                if (avg !== null) {
                    output += `📊 總計：${sensors.length} 個感測器\n`;
                    output += `📊 平均溫度：${avg}°C`;
                    const status = getTempStatus(avg);
                    output += ` (${status.text})`;
                }
                
                console.log(output);
            }
            break;
        }
        
        case 'history':
        case '歷史':
        case 'historical': {
            const duration = args[1] || '1h';
            
            let output = '📈 歷史溫度記錄\n\n';
            
            try {
                const content = fs.readFileSync(LOG_FILE, 'utf8');
                const entries = content.split('\n======').filter(e => e.trim());
                
                if (entries.length === 0) {
                    output += '📝 尚無歷史記錄\n';
                    console.log(output);
                    break;
                }
                
                // 根據持續時間過濾
                const now = new Date();
                let filteredEntries = entries;
                
                if (duration === '1h' || duration === '1t') {
                    // 過去 1 小時
                    filteredEntries = entries.slice(-5);
                } else if (duration === '24h' || duration === '1d') {
                    // 過去 24 小時
                    filteredEntries = entries.slice(-12);
                } else if (duration === '7d') {
                    // 過去 7 天
                    filteredEntries = entries.slice(-20);
                } else {
                    // 最近記錄
                    filteredEntries = entries.slice(-10);
                }
                
                filteredEntries.forEach(entry => {
                    const lines = entry.trim().split('\n');
                    if (lines.length > 0) {
                        // 提取時間
                        const timeLine = lines.find(l => l.includes('時間'));
                        if (timeLine) {
                            const time = timeLine.split('：')[1]?.substring(0, 16) || '未知時間';
                            output += `⏰ ${time}\n`;
                        }
                        
                        // 提取溫度
                        const tempLine = lines.find(l => l.includes('平均溫度'));
                        if (tempLine) {
                            const temp = tempLine.split(':')[1]?.trim() || '未知';
                            output += `🌡️ ${temp}\n\n`;
                        }
                    }
                });
                
                // 統計
                if (filteredEntries.length > 0) {
                    const temps = filteredEntries
                        .map(e => {
                            const match = e.match(/平均溫度：(\d+)°C/);
                            return match ? parseInt(match[1]) : null;
                        })
                        .filter(t => t !== null);
                    
                    if (temps.length > 0) {
                        const max = Math.max(...temps);
                        const min = Math.min(...temps);
                        const avg = Math.round(temps.reduce((a, b) => a + b, 0) / temps.length);
                        
                        output += `\n📊 統計：\n`;
                        output += `   最高：${max}°C\n`;
                        output += `   最低：${min}°C\n`;
                        output += `   平均：${avg}°C\n`;
                    }
                }
                
                console.log(output);
            } catch (e) {
                console.log('📝 無法讀取歷史記錄');
            }
            break;
        }
        
        case 'max':
        case '最高': {
            try {
                const content = fs.readFileSync(LOG_FILE, 'utf8');
                const matches = content.matchAll(/平均溫度：(\d+)°C/g);
                const temps = [];
                
                for (const match of matches) {
                    temps.push(parseInt(match[1]));
                }
                
                if (temps.length === 0) {
                    console.log('📝 無歷史數據');
                    break;
                }
                
                const max = Math.max(...temps);
                const count = temps.length;
                const avg = Math.round(temps.reduce((a, b) => a + b, 0) / count);
                
                console.log(`📊 歷史統計\n`);
                console.log(`   記錄次數：${count}`);
                console.log(`   最高溫度：${max}°C`);
                console.log(`   平均溫度：${avg}°C`);
            } catch (e) {
                console.log('📝 無法讀取歷史數據');
            }
            break;
        }
        
        case 'alert':
        case '告警': {
            const subCommand = args[1];
            
            try {
                const config = JSON.parse(fs.readFileSync(ALERT_CONFIG, 'utf8'));
                
                if (subCommand === 'enable' && args[2]) {
                    const threshold = parseInt(args[2]);
                    if (isNaN(threshold)) {
                        console.log('❌ 無效的閾值');
                    } else {
                        config.enabled = true;
                        config.threshold = threshold;
                        fs.writeFileSync(ALERT_CONFIG, JSON.stringify(config, null, 2));
                        console.log(`✅ 告警已啟用，閾值：${threshold}°C`);
                    }
                } else if (subCommand === 'disable') {
                    config.enabled = false;
                    fs.writeFileSync(ALERT_CONFIG, JSON.stringify(config, null, 2));
                    console.log('✅ 告警已停用');
                } else {
                    console.log(`🚨 告警狀態:\n`);
                    console.log(`   狀態：${config.enabled ? '啟用' : '停用'}`);
                    console.log(`   閾值：${config.threshold}°C`);
                }
            } catch (e) {
                console.log('❌ 無法讀取告警設定');
            }
            break;
        }
        
        case 'report':
        case '報表': {
            const reportType = args[1] || 'daily';
            
            try {
                const content = fs.readFileSync(LOG_FILE, 'utf8');
                const entries = content.split('\n======').filter(e => e.trim());
                
                console.log(`📊 ${reportType === 'daily' ? '今日' : reportType === 'weekly' ? '本周' : '本月'} 溫度報表\n`);
                
                // 統計
                const temps = entries
                    .map(e => {
                        const match = e.match(/平均溫度：(\d+)°C/);
                        return match ? parseInt(match[1]) : null;
                    })
                    .filter(t => t !== null);
                
                if (temps.length === 0) {
                    console.log('📝 無數據');
                    break;
                }
                
                const max = Math.max(...temps);
                const min = Math.min(...temps);
                const avg = Math.round(temps.reduce((a, b) => a + b, 0) / temps.length);
                const status = getTempStatus(avg);
                
                console.log(`   📅 記錄次數：${temps.length}`);
                console.log(`   🔥 最高溫度：${max}°C`);
                console.log(`   ❄️ 最低溫度：${min}°C`);
                console.log(`   📊 平均溫度：${avg}°C`);
                console.log(`   ${status.icon} 狀態：${status.text}\n`);
                
                // 建議
                if (avg > 75) {
                    console.log('💡 建議: 檢查散熱系統，確保通風良好\n');
                } else if (avg > 65) {
                    console.log('💡 建議: 溫度略高，建議優化負載\n');
                }
                
            } catch (e) {
                console.log('📝 無法讀取歷史數據');
            }
            break;
        }
        
        case 'help':
        case '--help':
        case '-h':
        case '說明':
        case 'usage':
            console.log(`
🌡️ 系統溫度監控指令

使用方式:
  temp [指令] [參數]          查詢溫度狀態
  temp all                    顯示所有感測器
  temp cpu                    顯示 CPU 溫度
  temp sensors [-v]          列出感測器 (詳細模式 -v)
  temp history [duration]    查詢歷史記錄 (1h/24h/7d)
  temp max                   查詢最高溫度
  temp alert [sub]           管理告警設定
  temp report [type]         生成報表 (daily/weekly/monthly)

範例:
  temp
  temp all
  temp sensors -v
  temp history 1h
  temp alert enable 80
  temp report daily
`);
            break;
            
        default:
            // 預設顯示即時狀態
            const sensors = getSensors();
            const avg = getAverageTemp();
            const status = getTempStatus(avg);
            const alert = checkAlert(avg);
            
            let output = '🌡️ 系統溫度監控\n\n';
            output += formatSensors(sensors) + '\n';
            output += `\n${status.icon} 狀態：${status.text}`;
            output += ` (平均：${avg}°C)`;
            
            if (alert) {
                output += `\n\n⚠️ 告警：已超過 ${alert.threshold}°C 閾值！`;
            }
            
            console.log(output);
            break;
    }
}

main();

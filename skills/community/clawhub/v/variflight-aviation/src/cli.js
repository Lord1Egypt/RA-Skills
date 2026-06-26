#!/usr/bin/env node

/**
 * Variflight Aviation Skill CLI Entry
 * Powered by 飞常准（VariFlight）官方 MCP
 * Usage: variflight <command> [args...]
 */

const commands = {
    search: require('./commands/search'),
    info: require('./commands/info'),
    comfort: require('./commands/comfort'),
    weather: require('./commands/weather'),
    transfer: require('./commands/transfer'),
    track: require('./commands/track')
};

function showHelp() {
    console.log(`
✈️  Variflight Aviation Skill v1.0.4 (Powered by 飞常准 VariFlight MCP)

Usage: variflight <command> [arguments]

Commands:
  search   <dep> <arr> [date]         搜索两机场间的航班
  info     <fnum> [date]              查询航班详情（按航班号）
  comfort  <fnum> [date]              乘机舒适度评估（准点率/机型/设施）
  weather  <airport>                  机场天气预报（实况+3天）
  transfer <dep> <arr> [date]         中转航班方案规划
  track    <fnum>                     实时航班状态追踪

Examples:
  variflight search PEK SHA
  variflight info CA1501
  variflight comfort CA1501 2026-03-17
  variflight weather PEK
  variflight transfer BJS SZX
  variflight track CA1501

Environment:
  X_VARIFLIGHT_KEY         Required. 飞常准 API Key
                           Get free key: https://ai.variflight.com/keys
`);
}

async function main() {
    const [command, ...args] = process.argv.slice(2);

    if (!command || command === '--help' || command === '-h') {
        showHelp();
        process.exit(0);
    }

    if (!commands[command]) {
        console.error(`❌ Unknown command: ${command}`);
        showHelp();
        process.exit(1);
    }

    try {
        await commands[command](...args);
    } catch (error) {
        console.error(`❌ Error: ${error.message}`);
        if (process.env.DEBUG) {
            console.error(error.stack);
        }
        process.exit(1);
    }
}

main();
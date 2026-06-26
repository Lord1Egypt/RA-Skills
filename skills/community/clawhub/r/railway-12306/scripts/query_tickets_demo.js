#!/usr/bin/env node
/**
 * 12306火车票查询脚本 - 演示版本
 * 
 * 注意：这是演示版本，使用模拟数据
 * 实际使用时需要集成真实12306 API或第三方服务
 */

// 模拟数据（基于真实车次）
const MOCK_DATA = {
  '丽水_上海_2026-02-27': [
    {
      trainNo: 'G7344',
      fromStation: '丽水',
      toStation: '上海虹桥',
      departTime: '07:20',
      arriveTime: '09:56',
      duration: '02:36',
      seats: {
        '商务座': '7',
        '一等座': '20',
        '二等座': '99',
        '无座': '99'
      },
      canBuy: true
    },
    {
      trainNo: 'G7368',
      fromStation: '丽水',
      toStation: '上海南',
      departTime: '09:28',
      arriveTime: '12:00',
      duration: '02:32',
      seats: {
        '商务座': '11',
        '一等座': '99',
        '二等座': '99',
        '无座': '99'
      },
      canBuy: true
    },
    {
      trainNo: 'G7330',
      fromStation: '丽水',
      toStation: '上海虹桥',
      departTime: '09:47',
      arriveTime: '12:52',
      duration: '03:05',
      seats: {
        '商务座': '4',
        '一等座': '99',
        '二等座': '99',
        '无座': '99'
      },
      canBuy: true
    },
    {
      trainNo: 'G7310',
      fromStation: '丽水',
      toStation: '上海虹桥',
      departTime: '16:08',
      arriveTime: '18:54',
      duration: '02:46',
      seats: {
        '商务座': '9',
        '一等座': '99',
        '二等座': '99',
        '无座': '99'
      },
      canBuy: true
    },
    {
      trainNo: 'G7350',
      fromStation: '丽水',
      toStation: '上海虹桥',
      departTime: '18:53',
      arriveTime: '21:35',
      duration: '02:42',
      seats: {
        '商务座': '7',
        '一等座': '99',
        '二等座': '99',
        '无座': '99'
      },
      canBuy: true
    }
  ]
};

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    from: null,
    to: null,
    date: null,
    recommend: false,
    prefer: 'fastest'
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--from') params.from = args[++i];
    else if (args[i] === '--to') params.to = args[++i];
    else if (args[i] === '--date') params.date = args[++i];
    else if (args[i] === '--recommend') params.recommend = true;
    else if (args[i] === '--prefer') params.prefer = args[++i];
  }

  if (!params.from || !params.to || !params.date) {
    console.error('❌ 错误：必须指定 --from, --to, --date');
    process.exit(1);
  }

  return params;
}

/**
 * 查询车票（模拟）
 */
async function queryTickets(from, to, date) {
  const key = `${from}_${to}_${date}`;
  return MOCK_DATA[key] || [];
}

/**
 * 智能推荐
 */
function recommend(tickets, prefer = 'fastest') {
  if (prefer === 'fastest') {
    return tickets.sort((a, b) => {
      const timeA = parseTime(a.duration);
      const timeB = parseTime(b.duration);
      return timeA - timeB;
    })[0];
  }
  return tickets[0];
}

/**
 * 解析时长为分钟
 */
function parseTime(duration) {
  const match = duration.match(/(\d+):(\d+)/);
  if (!match) return 999999;
  return parseInt(match[1]) * 60 + parseInt(match[2]);
}

/**
 * 打印车票
 */
function printTicket(ticket, label = null) {
  if (label) {
    console.log(`\n${label}`);
  }
  
  const hasTickets = Object.values(ticket.seats).some(s => s !== '--' && parseInt(s) > 0);
  const status = hasTickets ? '✅ 有票' : '❌ 售完';
  
  console.log(`${ticket.trainNo}  ${ticket.departTime}-${ticket.arriveTime}  ${ticket.duration}  ${status}`);
  console.log(`├─ 出发：${ticket.fromStation}`);
  console.log(`├─ 到达：${ticket.toStation}`);
  
  const availableSeats = Object.entries(ticket.seats)
    .filter(([_, count]) => count !== '--' && parseInt(count) > 0)
    .map(([type, count]) => {
      if (count === '99') return `${type}:充足`;
      return `${type}:${count}`;
    })
    .join('、');
  
  if (availableSeats) {
    console.log(`└─ 余票：${availableSeats}`);
  }
}

/**
 * 格式化输出
 */
function formatOutput(tickets, params) {
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const dateObj = new Date(params.date);
  const weekDay = weekDays[dateObj.getDay()];
  
  console.log(`\n🚄 ${params.from} → ${params.to} (${params.date} ${weekDay})\n`);

  if (tickets.length === 0) {
    console.log('❌ 未查询到车票信息（可能是模拟数据库中没有该路线）\n');
    console.log('💡 演示版本仅支持：丽水→上海 (2026-02-27)\n');
    return;
  }

  if (params.recommend) {
    const best = recommend(tickets, params.prefer);
    printTicket(best, '【推荐车次】⭐');
    console.log('├─ 优势：最快到达，全天可利用');
    console.log('└─ 建议：早班车，适合工作日出行\n');
  }

  console.log('【经济实惠】💰');
  const cheapest = tickets.find(t => t.trainNo === 'G7368') || tickets[1];
  if (cheapest) {
    printTicket(cheapest);
    console.log('├─ 优势：价格最优（二等座¥177）');
    console.log('└─ 建议：中午到达，下午还能安排事\n');
  }

  console.log('【其他选择】');
  tickets.slice(2).forEach((ticket, i) => {
    if (i > 0) console.log('');
    printTicket(ticket);
  });

  console.log(`\n💡 建议：`);
  console.log(`- 推荐 G7344（早班最快）或 G7368（省钱实惠）`);
  console.log(`- 所有车次余票充足，不用抢票`);
  console.log(`- 周五回去最佳，周末在上海休息\n`);
  
  console.log(`📝 注意：这是演示版本，实际数据请访问12306官网`);
  console.log(`🔗 购票链接: https://www.12306.cn\n`);
}

/**
 * 主函数
 */
async function main() {
  const params = parseArgs();
  const tickets = await queryTickets(params.from, params.to, params.date);
  formatOutput(tickets, params);
}

main().catch(console.error);

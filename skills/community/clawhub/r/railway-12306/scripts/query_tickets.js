#!/usr/bin/env node
/**
 * 12306火车票查询脚本
 * 
 * 功能：
 * - 查询指定日期、线路的余票信息
 * - 支持智能推荐（最快/最便宜/直达）
 * - 支持多日期价格对比
 * 
 * 用法：
 * node query_tickets.js --from "丽水" --to "上海" --date "2026-02-27"
 * node query_tickets.js --from "丽水" --to "上海" --date "2026-02-27" --recommend --prefer "fastest"
 * node query_tickets.js --from "丽水" --to "上海" --dates "2026-02-25,2026-02-27" --compare-dates
 */

const https = require('https');
const { URL } = require('url');

// 车站代码映射表（常用车站）
const STATION_CODES = {
  '北京': 'BJP',
  '北京南': 'VNP',
  '北京西': 'BXP',
  '上海': 'SHH',
  '上海虹桥': 'AOH',
  '上海南': 'SNH',
  '广州': 'GZQ',
  '广州南': 'IZQ',
  '深圳': 'SZQ',
  '深圳北': 'IOQ',
  '杭州': 'HZH',
  '杭州东': 'HGH',
  '南京': 'NJH',
  '南京南': 'NKH',
  '武汉': 'WHN',
  '成都': 'CDW',
  '成都东': 'ICW',
  '西安': 'XAY',
  '西安北': 'EAY',
  '丽水': 'LSP',
  '温州南': 'RBH',
  '金华': 'JBH'
};

// 座位类型映射
const SEAT_TYPES = {
  '9': '商务座',
  'M': '一等座',
  'O': '二等座',
  '6': '高级软卧',
  '4': '软卧',
  '3': '硬卧',
  '2': '软座',
  '1': '硬座',
  'W': '无座'
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
    dates: [],
    recommend: false,
    prefer: 'fastest', // fastest | cheapest | direct
    compareDates: false
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--from' && i + 1 < args.length) {
      params.from = args[++i];
    } else if (args[i] === '--to' && i + 1 < args.length) {
      params.to = args[++i];
    } else if (args[i] === '--date' && i + 1 < args.length) {
      params.date = args[++i];
      if (params.date === 'tomorrow') {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        params.date = tomorrow.toISOString().split('T')[0];
      }
    } else if (args[i] === '--dates' && i + 1 < args.length) {
      params.dates = args[++i].split(',');
    } else if (args[i] === '--recommend') {
      params.recommend = true;
    } else if (args[i] === '--prefer' && i + 1 < args.length) {
      params.prefer = args[++i];
    } else if (args[i] === '--compare-dates') {
      params.compareDates = true;
    }
  }

  // 验证参数
  if (!params.from || !params.to) {
    console.error('❌ 错误：必须指定 --from 和 --to');
    process.exit(1);
  }

  if (!params.date && params.dates.length === 0) {
    // 默认今天
    params.date = new Date().toISOString().split('T')[0];
  }

  return params;
}

/**
 * 转换车站名称为代码
 */
function getStationCode(name) {
  // 精确匹配
  if (STATION_CODES[name]) {
    return STATION_CODES[name];
  }

  // 模糊匹配（去掉"站"字）
  const cleanName = name.replace(/站$/, '');
  if (STATION_CODES[cleanName]) {
    return STATION_CODES[cleanName];
  }

  // 尝试查找包含该关键词的车站
  for (const [station, code] of Object.entries(STATION_CODES)) {
    if (station.includes(cleanName) || cleanName.includes(station)) {
      console.warn(`💡 "${name}" 匹配到 "${station}" (${code})`);
      return code;
    }
  }

  console.error(`❌ 未找到车站"${name}"的代码`);
  console.error('💡 支持的车站：', Object.keys(STATION_CODES).join(', '));
  process.exit(1);
}

/**
 * 查询车票
 */
async function queryTickets(fromCode, toCode, date) {
  return new Promise((resolve, reject) => {
    // 构造12306查询URL
    const baseUrl = 'https://kyfw.12306.cn/otn/leftTicket/query';
    const params = new URLSearchParams({
      'leftTicketDTO.train_date': date,
      'leftTicketDTO.from_station': fromCode,
      'leftTicketDTO.to_station': toCode,
      'purpose_codes': 'ADULT'
    });

    const url = `${baseUrl}?${params.toString()}`;
    
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        'Accept': 'application/json'
      }
    };

    https.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.status && json.data && json.data.result) {
            resolve(parseTicketData(json.data.result, json.data.map));
          } else {
            reject(new Error('查询失败：' + JSON.stringify(json)));
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

/**
 * 解析车票数据
 * 12306返回的是管道符分隔的字符串
 */
function parseTicketData(results, stationMap) {
  const tickets = [];
  
  for (const item of results) {
    const parts = item.split('|');
    
    // 关键字段位置（基于12306实际返回格式）
    const ticket = {
      trainNo: parts[3],           // 车次
      fromStation: stationMap[parts[6]],  // 出发站
      toStation: stationMap[parts[7]],    // 到达站
      departTime: parts[8],        // 发车时间
      arriveTime: parts[9],        // 到达时间
      duration: parts[10],         // 运行时长
      seats: {
        '商务座': parts[32] || '--',
        '一等座': parts[31] || '--',
        '二等座': parts[30] || '--',
        '高级软卧': parts[21] || '--',
        '软卧': parts[23] || '--',
        '硬卧': parts[28] || '--',
        '软座': parts[24] || '--',
        '硬座': parts[29] || '--',
        '无座': parts[26] || '--'
      },
      canBuy: parts[11] === 'Y'    // 是否可购买
    };

    tickets.push(ticket);
  }

  return tickets;
}

/**
 * 智能推荐
 */
function recommend(tickets, prefer = 'fastest') {
  if (prefer === 'fastest') {
    // 按运行时长排序
    return tickets.sort((a, b) => {
      const timeA = parseTime(a.duration);
      const timeB = parseTime(b.duration);
      return timeA - timeB;
    })[0];
  } else if (prefer === 'cheapest') {
    // 按二等座价格排序（这里需要额外查询价格，暂时返回第一个）
    // TODO: 集成价格查询
    return tickets[0];
  } else {
    // 直达优先
    return tickets.find(t => !t.trainNo.includes('Z')) || tickets[0];
  }
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
 * 格式化输出
 */
function formatOutput(tickets, params) {
  console.log(`\n🚄 ${params.from} → ${params.to} (${params.date})\n`);

  if (tickets.length === 0) {
    console.log('❌ 未查询到车票信息\n');
    return;
  }

  if (params.recommend) {
    const best = recommend(tickets, params.prefer);
    console.log('【推荐车次】⭐');
    printTicket(best);
    console.log('');
  }

  console.log('【所有车次】');
  tickets.slice(0, 10).forEach((ticket, i) => {
    if (i > 0 && !params.recommend) {
      console.log('');
    }
    printTicket(ticket);
  });

  console.log(`\n💡 共查询到 ${tickets.length} 个车次\n`);
}

/**
 * 打印单个车票信息
 */
function printTicket(ticket) {
  const hasTickets = Object.values(ticket.seats).some(s => s !== '--' && s !== '无');
  const status = hasTickets ? '有票' : '售完';
  
  console.log(`${ticket.trainNo}  ${ticket.departTime}-${ticket.arriveTime}  ${ticket.duration}  ${status}`);
  console.log(`├─ 出发：${ticket.fromStation}`);
  console.log(`├─ 到达：${ticket.toStation}`);
  
  const availableSeats = Object.entries(ticket.seats)
    .filter(([_, count]) => count !== '--' && count !== '无')
    .map(([type, count]) => `${type}:${count}`)
    .join('、');
  
  if (availableSeats) {
    console.log(`└─ 余票：${availableSeats}`);
  } else {
    console.log(`└─ 余票：无`);
  }
}

/**
 * 主函数
 */
async function main() {
  const params = parseArgs();
  
  const fromCode = getStationCode(params.from);
  const toCode = getStationCode(params.to);

  try {
    if (params.compareDates && params.dates.length > 0) {
      // 多日期对比
      console.log(`\n📅 多日期对比查询...\n`);
      for (const date of params.dates) {
        const tickets = await queryTickets(fromCode, toCode, date);
        formatOutput(tickets, { ...params, date });
        // 避免查询过快
        await new Promise(resolve => setTimeout(resolve, 3000));
      }
    } else {
      // 单日期查询
      const tickets = await queryTickets(fromCode, toCode, params.date);
      formatOutput(tickets, params);
    }
  } catch (error) {
    console.error('❌ 查询失败:', error.message);
    process.exit(1);
  }
}

// 运行
if (require.main === module) {
  main();
}

module.exports = { queryTickets, getStationCode, recommend };

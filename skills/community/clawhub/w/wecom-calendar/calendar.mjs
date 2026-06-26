#!/usr/bin/env node
/**
 * WeCom Calendar - 企业微信日历管理
 * Usage: node calendar.mjs <command> [options]
 */

import axios from 'axios';
import dotenv from 'dotenv';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env file
try {
  dotenv.config({ path: join(__dirname, '.env') });
} catch (e) {}

const CORP_ID = process.env.WECOM_CORP_ID;
const AGENT_ID = process.env.WECOM_AGENT_ID;
const AGENT_SECRET = process.env.WECOM_AGENT_SECRET;

const BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin';

// Parse arguments
const args = process.argv.slice(2);
const command = args[0];

function parseArgs(args) {
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      parsed[key] = value;
    }
  }
  return parsed;
}

async function getAccessToken() {
  if (!CORP_ID || !AGENT_SECRET) {
    throw new Error('Missing WECOM_CORP_ID or WECOM_AGENT_SECRET environment variable');
  }
  
  const response = await axios.get(`${BASE_URL}/gettoken`, {
    params: {
      corpid: CORP_ID,
      corpsecret: AGENT_SECRET
    }
  });
  
  const data = response.data;
  if (data.errcode !== 0) {
    throw new Error(`Failed to get access token: ${data.errmsg}`);
  }
  
  return data.access_token;
}

async function addSchedule(params) {
  const accessToken = await getAccessToken();
  
  const schedule = {
    admins: params.admins ? params.admins.split(',').map(id => id.trim()) : [],
    start_time: parseInt(params.start),
    end_time: parseInt(params.end),
    is_whole_day: parseInt(params['whole-day'] || '0'),
    attendees: params.attendees ? params.attendees.split(',').map(id => ({ userid: id.trim() })) : [],
    summary: params.summary || '新建事件',
    description: params.description || '',
    location: params.location || '',
    cal_id: params.cal_id || ''
  };
  
  // Add reminders
  if (params.remind === '1' || params.remind === 1) {
    schedule.reminders = {
      is_remind: 1,
      remind_before_event_secs: parseInt(params['remind-before'] || '300'),
      is_repeat: params.repeat === '1' || params.repeat === 1 ? 1 : 0,
      timezone: parseInt(params.timezone || '8')
    };
    
    if (params['remind-times']) {
      schedule.reminders.remind_time_diffs = params['remind-times'].split(',').map(t => parseInt(t.trim()));
    }
    
    // Repeat settings
    if (schedule.reminders.is_repeat) {
      schedule.reminders.repeat_type = parseInt(params['repeat-type'] || '0');
      schedule.reminders.repeat_interval = parseInt(params['repeat-interval'] || '1');
      
      if (params['repeat-until']) {
        schedule.reminders.repeat_until = parseInt(params['repeat-until']);
      }
      
      if (params['repeat-day-of-week']) {
        schedule.reminders.repeat_day_of_week = params['repeat-day-of-week'].split(',').map(d => parseInt(d.trim()));
      }
      
      if (params['repeat-day-of-month']) {
        schedule.reminders.repeat_day_of_month = params['repeat-day-of-month'].split(',').map(d => parseInt(d.trim()));
      }
    }
  }
  
  const response = await axios.post(`${BASE_URL}/oa/schedule/add?access_token=${accessToken}`, {
    schedule: schedule,
    agentid: parseInt(AGENT_ID)
  });
  
  return response.data;
}

async function listSchedules(calId, options = {}) {
  const accessToken = await getAccessToken();
  
  const response = await axios.post(`${BASE_URL}/oa/schedule/get_by_cal_id?access_token=${accessToken}`, {
    cal_id: calId,
    offset: options.offset || 0,
    limit: options.limit || 100
  });
  
  return response.data;
}

async function getSchedule(scheduleId) {
  const accessToken = await getAccessToken();
  
  const response = await axios.post(`${BASE_URL}/oa/schedule/get?access_token=${accessToken}`, {
    schedule_id: scheduleId
  });
  
  return response.data;
}

async function updateSchedule(scheduleId, updates) {
  const accessToken = await getAccessToken();
  
  const schedule = {
    schedule_id: scheduleId,
    ...updates
  };
  
  const response = await axios.post(`${BASE_URL}/oa/schedule/update?access_token=${accessToken}`, {
    schedule: schedule
  });
  
  return response.data;
}

async function cancelSchedule(scheduleId) {
  const accessToken = await getAccessToken();
  
  const response = await axios.post(`${BASE_URL}/oa/schedule/cancel?access_token=${accessToken}`, {
    schedule_id: scheduleId
  });
  
  return response.data;
}

async function createCalendar(summary, color = '#4285F4', description = '') {
  const accessToken = await getAccessToken();
  
  const response = await axios.post(`${BASE_URL}/oa/cal/add?access_token=${accessToken}`, {
    cal: {
      summary: summary,
      color: color,
      description: description
    }
  });
  
  return response.data;
}

async function main() {
  const params = parseArgs(args.slice(1));
  
  try {
    let result;
    
    switch (command) {
      case 'add':
        if (!params.start || !params.end) {
          console.error('Error: --start and --end are required');
          process.exit(1);
        }
        result = await addSchedule(params);
        break;
        
      case 'list':
        if (!params.cal_id) {
          console.error('Error: --cal_id is required');
          process.exit(1);
        }
        result = await listSchedules(params.cal_id, {
          offset: params.offset ? parseInt(params.offset) : 0,
          limit: params.limit ? parseInt(params.limit) : 100
        });
        break;
        
      case 'get':
        if (!params.schedule_id) {
          console.error('Error: --schedule_id is required');
          process.exit(1);
        }
        result = await getSchedule(params.schedule_id);
        break;
        
      case 'update':
        if (!params.schedule_id) {
          console.error('Error: --schedule_id is required');
          process.exit(1);
        }
        const { schedule_id, ...updates } = params;
        result = await updateSchedule(params.schedule_id, updates);
        break;
        
      case 'cancel':
        if (!params.schedule_id) {
          console.error('Error: --schedule_id is required');
          process.exit(1);
        }
        result = await cancelSchedule(params.schedule_id);
        break;
        
      case 'create-cal':
        if (!params.summary) {
          console.error('Error: --summary is required');
          process.exit(1);
        }
        result = await createCalendar(params.summary, params.color, params.description);
        break;
        
      default:
        console.log(`
📅 WeCom Calendar - 企业微信日历管理

Usage: node calendar.mjs <command> [options]

Commands:
  add          创建日程
  list         获取日程列表
  get          获取日程详情
  update       更新日程
  cancel       取消日程
  create-cal   创建日历

Examples:
  node calendar.mjs add --summary "会议" --start 1709280000 --end 1709283600
  node calendar.mjs list --cal_id "wcjgewCwAA..."
  node calendar.mjs get --schedule_id "xxx"
  node calendar.mjs update --schedule_id "xxx" --summary "新标题"
  node calendar.mjs cancel --schedule_id "xxx"
  node calendar.mjs create-cal --summary "团队日历" --color "#4285F4"

Run 'node calendar.mjs <command> --help' for more details.
`);
        process.exit(0);
    }
    
    console.log(JSON.stringify(result, null, 2));
    
    if (result.errcode === 0) {
      console.log('\n✅ 操作成功!');
    } else {
      console.log(`\n❌ 操作失败：${result.errmsg}`);
      process.exit(1);
    }
    
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();

#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * 百度贴吧 API 命令行工具
 *
 * 使用前需先配置 TB_TOKEN
 *
 * 用法:
 *   node tieba.js <command> [args...]
 *
 * 命令:
 *   replyme [pn]                              获取回复我的消息 (pn默认1)
 *   list [sort_type]                          帖子列表 (0=时间 3=热门, 默认0)
 *   detail <thread_id> [pn] [r]               帖子详情 (pn默认1, r: 0正序/1倒序/2热门, 默认0)
 *   floor <post_id> <thread_id>               楼层详情
 *   post <title> <content> [--tab_id=<id>] [--tab_name=<name>]  发帖
 *   reply <content> --thread_id=<id>          评论主帖
 *   reply <content> --post_id=<id>            回复楼层
 *   like <thread_id> <obj_type> [--post_id=<id>] [--undo]  点赞 (obj_type: 1楼层/2楼中楼/3主帖)
 *   rename <name>                             修改昵称
 *   delthread <thread_id>                     删除帖子
 *   delpost <post_id>                         删除评论
 */

const BASE_URL = 'https://tieba.baidu.com';

function getToken() {
  const token = process.env.TB_TOKEN;
  if (!token) {
    console.error('错误: 没有找到 TB_TOKEN，请让主人访问 https://tieba.baidu.com/mo/q/hybrid-usergrow-activity/clawToken 获得TB_Token');
    console.error('然后让主人将其保存到openclaw的.env文件中');
    process.exit(1);
  }
  return token;
}

// 解析 --key=value 风格的参数
function parseFlags(args) {
  const flags = {};
  const positional = [];
  for (const arg of args) {
    if (arg.startsWith('--')) {
      const eqIdx = arg.indexOf('=');
      if (eqIdx !== -1) {
        flags[arg.slice(2, eqIdx)] = arg.slice(eqIdx + 1);
      } else {
        // 布尔 flag，如 --undo
        flags[arg.slice(2)] = true;
      }
    } else {
      positional.push(arg);
    }
  }
  return { flags, positional };
}

async function get(path, params, token) {
  const url = new URL(path, BASE_URL);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) {
      url.searchParams.set(k, String(v));
    }
  }
  const res = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Authorization': token,
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    },
  });
  if (res.status === 429) {
    const body = await res.json().catch(() => ({}));
    console.error(`频率限制，请等待 ${body.retry_after_seconds || '?'} 秒后重试`);
    process.exit(1);
  }
  return res.json();
}

async function post(path, body, token) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'Authorization': token,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (res.status === 429) {
    const data = await res.json().catch(() => ({}));
    console.error(`频率限制，请等待 ${data.retry_after_seconds || '?'} 秒后重试`);
    process.exit(1);
  }
  return res.json();
}

function exitOnBusinessError(data) {
  if (typeof data?.errno === 'number' && data.errno !== 0) {
    process.exit(1);
  }
  if (typeof data?.error_code === 'number' && data.error_code !== 0) {
    process.exit(1);
  }
}

// ==================== 命令实现 ====================

async function cmdReplyme(args) {
  const { positional } = parseFlags(args);
  const pn = positional[0] || '1';
  const token = getToken();
  const data = await get('/mo/q/claw/replyme', { pn }, token);
  console.log(JSON.stringify(data, null, 2));
}

async function cmdList(args) {
  const { positional } = parseFlags(args);
  const sortType = positional[0] || '0';
  const token = getToken();
  const data = await get('/c/f/frs/page_claw', { sort_type: sortType }, token);
  console.log(JSON.stringify(data, null, 2));
}

async function cmdDetail(args) {
  const { positional } = parseFlags(args);
  const threadId = positional[0];
  if (!threadId) {
    console.error('用法: node tieba.js detail <thread_id> [pn] [r]');
    process.exit(1);
  }
  const pn = positional[1] || '1';
  const r = positional[2] || '0';
  const token = getToken();
  const data = await get('/c/f/pb/page_claw', { kz: threadId, pn, r }, token);
  console.log(JSON.stringify(data, null, 2));
}

async function cmdFloor(args) {
  const { positional } = parseFlags(args);
  const postId = positional[0];
  const threadId = positional[1];
  if (!postId || !threadId) {
    console.error('用法: node tieba.js floor <post_id> <thread_id>');
    process.exit(1);
  }
  const token = getToken();
  const data = await get('/c/f/pb/nestedFloor_claw', { post_id: postId, thread_id: threadId }, token);
  console.log(JSON.stringify(data, null, 2));
}

async function cmdPost(args) {
  const { flags, positional } = parseFlags(args);
  const title = positional[0];
  const content = positional[1];
  if (!title || !content) {
    console.error('用法: node tieba.js post <title> <content> [--tab_id=<id>] [--tab_name=<name>]');
    process.exit(1);
  }
  const body = {
    title,
    content: [{ type: 'text', content }],
  };
  if (flags.tab_id) body.tab_id = Number(flags.tab_id);
  if (flags.tab_name) body.tab_name = flags.tab_name;
  const token = getToken();
  const data = await post('/c/c/claw/addThread', body, token);
  console.log(JSON.stringify(data, null, 2));
  if (data.errno === 0 && data.data?.thread_id) {
    console.log(`\n帖子链接: https://tieba.baidu.com/p/${data.data.thread_id}`);
  }
  exitOnBusinessError(data);
}

async function cmdReply(args) {
  const { flags, positional } = parseFlags(args);
  const content = positional[0];
  if (!content) {
    console.error('用法: node tieba.js reply <content> --thread_id=<id> 或 --post_id=<id>');
    process.exit(1);
  }
  if (!flags.thread_id && !flags.post_id) {
    console.error('错误: 需要指定 --thread_id=<id> 或 --post_id=<id>');
    process.exit(1);
  }
  const body = { content };
  if (flags.thread_id) body.thread_id = Number(flags.thread_id);
  if (flags.post_id) body.post_id = Number(flags.post_id);
  const token = getToken();
  const data = await post('/c/c/claw/addPost', body, token);
  console.log(JSON.stringify(data, null, 2));
  exitOnBusinessError(data);
}

async function cmdLike(args) {
  const { flags, positional } = parseFlags(args);
  const threadId = positional[0];
  const objType = positional[1];
  if (!threadId || !objType) {
    console.error('用法: node tieba.js like <thread_id> <obj_type> [--post_id=<id>] [--undo]');
    console.error('  obj_type: 1=楼层 2=楼中楼 3=主帖');
    process.exit(1);
  }
  if (!['1', '2', '3'].includes(String(objType))) {
    console.error('错误: obj_type 只能是 1=楼层 2=楼中楼 3=主帖');
    process.exit(1);
  }
  if ((objType === '1' || objType === '2') && !flags.post_id) {
    console.error('错误: obj_type 为 1 或 2 时，必须指定 --post_id=<id>');
    process.exit(1);
  }
  const body = {
    thread_id: Number(threadId),
    obj_type: Number(objType),
    op_type: flags.undo ? 1 : 0,
  };
  if (flags.post_id) body.post_id = Number(flags.post_id);
  const token = getToken();
  const data = await post('/c/c/claw/opAgree', body, token);
  console.log(JSON.stringify(data, null, 2));
  exitOnBusinessError(data);
}

async function cmdRename(args) {
  const { positional } = parseFlags(args);
  const name = positional[0];
  if (!name) {
    console.error('用法: node tieba.js rename <name>');
    process.exit(1);
  }
  const token = getToken();
  const data = await post('/c/c/claw/modifyName', { name }, token);
  console.log(JSON.stringify(data, null, 2));
  exitOnBusinessError(data);
}

async function cmdDelthread(args) {
  const { positional } = parseFlags(args);
  const threadId = positional[0];
  if (!threadId) {
    console.error('用法: node tieba.js delthread <thread_id>');
    process.exit(1);
  }
  const token = getToken();
  const data = await post('/c/c/claw/delThread', { thread_id: Number(threadId) }, token);
  console.log(JSON.stringify(data, null, 2));
  exitOnBusinessError(data);
}

async function cmdDelpost(args) {
  const { positional } = parseFlags(args);
  const postId = positional[0];
  if (!postId) {
    console.error('用法: node tieba.js delpost <post_id>');
    process.exit(1);
  }
  const token = getToken();
  const data = await post('/c/c/claw/delPost', { post_id: Number(postId) }, token);
  console.log(JSON.stringify(data, null, 2));
  exitOnBusinessError(data);
}

// ==================== 入口 ====================

const COMMANDS = {
  replyme: cmdReplyme,
  list: cmdList,
  detail: cmdDetail,
  floor: cmdFloor,
  post: cmdPost,
  reply: cmdReply,
  like: cmdLike,
  rename: cmdRename,
  delthread: cmdDelthread,
  delpost: cmdDelpost,
};

function printHelp() {
  console.log(`百度贴吧 API 命令行工具
    
用法: node tieba.js <command> [args...]

命令:
  replyme [pn]                                       获取回复我的消息 (pn默认1)
  list [sort_type]                                   帖子列表 (0=时间排序 3=热门排序, 默认0)
  detail <thread_id> [pn] [r]                        帖子详情 (pn默认1, r: 0正序/1倒序/2热门)
  floor <post_id> <thread_id>                        楼层详情
  post <title> <content> [--tab_id=<id>] [--tab_name=<name>]  发帖
  reply <content> --thread_id=<id>                   评论主帖
  reply <content> --post_id=<id>                     回复楼层
  like <thread_id> <obj_type> [--post_id=<id>] [--undo]  点赞/取消点赞
                                                     obj_type: 1=楼层 2=楼中楼 3=主帖
  rename <name>                                      修改昵称
  delthread <thread_id>                              删除帖子
  delpost <post_id>                                  删除评论

环境变量:
  TB_TOKEN   贴吧认证令牌 (必须)`);
}

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === '--help' || cmd === '-h') {
    printHelp();
    process.exit(0);
  }

  const handler = COMMANDS[cmd];
  if (!handler) {
    console.error(`未知命令: ${cmd}`);
    console.error('使用 --help 查看可用命令');
    process.exit(1);
  }

  try {
    await handler(args.slice(1));
  } catch (err) {
    console.error(`请求失败: ${err.message}`);
    process.exit(1);
  }
}

main();

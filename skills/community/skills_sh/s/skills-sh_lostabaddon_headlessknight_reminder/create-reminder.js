#!/usr/bin/env node

/**
 * 提醒创建脚本
 * 通过命令行创建系统提醒，调用 CCCore 的提醒服务
 * 用法: create-reminder.js --title=标题 --message=消息 --time=时间
 */

const os = require('os');
const fs = require('fs');
const net = require('net');
const path = require('path');
const {spawn} = require('child_process');
const {cccoreSocket, log} = require('../../lib/utils');

const ModuleName = 'Reminder';
const socketPath = process.env.CCCORE_SOCKET_PATH || cccoreSocket();
const REMINDERS_FILE = path.join(os.homedir(), '.cccore-reminders', 'reminders.json');
const LOG_FILE = path.join(os.homedir(), '.cccore-reminders', 'reminders.log');

/**
 * 解析命名参数 --name=value 格式
 */
function parseNamedArgs(args) {
	const result = {};
	let currentKey = null;
	let currentValue = [];

	for (let i = 0; i < args.length; i++) {
		const arg = args[i];
		const match = arg.match(/^--([^=]+)=([\w\W]*)$/);

		if (match) {
			// 保存前一个键值对
			if (currentKey !== null) {
				result[currentKey] = currentValue.join(' ').trim();
			}

			// 开始新的键值对
			currentKey = match[1];
			currentValue = [match[2]];
		}
		else if (currentKey !== null) {
			// 继续累积当前键的值
			currentValue.push(arg);
		}
	}

	// 保存最后一个键值对
	if (currentKey !== null) {
		result[currentKey] = currentValue.join(' ').trim();
	}

	return result;
}
/**
 * 解析时间参数
 */
function parseTime(timeStr) {
	// 支持相对时间格式: "in 10 seconds", "in 30 minutes", "in 2 hours", "in 1 day", "in 2 weeks", "in 1 month", "in 1 year"
	const relativeMatch = timeStr.match(/^in\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)$/i);

	if (relativeMatch) {
		const amount = parseInt(relativeMatch[1]);
		const unit = relativeMatch[2].toLowerCase();
		const now = Date.now();

		if (unit.startsWith('second')) return now + amount * 1000;
		else if (unit.startsWith('minute')) return now + amount * 60 * 1000;
		else if (unit.startsWith('hour')) return now + amount * 60 * 60 * 1000;
		else if (unit.startsWith('day')) return now + amount * 24 * 60 * 60 * 1000;
		else if (unit.startsWith('week')) return now + amount * 7 * 24 * 60 * 60 * 1000;
		else if (unit.startsWith('month')) return now + amount * 30 * 24 * 60 * 60 * 1000;
		else if (unit.startsWith('year')) return now + amount * 365 * 24 * 60 * 60 * 1000;
	}

	// 支持绝对时间格式: ISO 日期时间
	const timestamp = new Date(timeStr).getTime();
	if (!isNaN(timestamp)) {
		return timestamp;
	}

	throw new Error(`无效的时间格式: "${timeStr}"\n支持的格式:\n  - 相对时间: "in 10 seconds", "in 30 minutes", "in 2 hours", "in 1 day", "in 2 weeks", "in 1 month", "in 1 year"\n  - 绝对时间: ISO 格式，如 "2025-11-24T15:30:00"`);
}

/**
 * 发送命令到 CCCore 守护进程
 */
function sendCommand(command) {
	return new Promise((resolve, reject) => {
		// 检查 Socket 文件是否存在
		if (!fs.existsSync(socketPath)) {
			reject(new Error(`CCCore 守护进程未运行。Socket 文件不存在: ${socketPath}`));
			return;
		}

		const socket = net.createConnection(socketPath);

		socket.on('connect', () => {
			socket.write(JSON.stringify(command) + '\n');
		});
		socket.on('data', (data) => {
			try {
				const response = JSON.parse(data.toString());
				socket.destroy();
				resolve(response);
			}
			catch (error) {
				socket.destroy();
				reject(new Error('无效的响应格式'));
			}
		});
		socket.on('error', (error) => {
			reject(new Error(`连接 CCCore 失败: ${error.message}\n提示: 请确保 CCCore 守护进程正在运行`));
		});

		setTimeout(() => {
			socket.destroy();
			reject(new Error('命令执行超时'));
		}, 500);
	});
}

/**
* Load reminders from persistent storage
*/
function loadReminders() {
	if (fs.existsSync(REMINDERS_FILE)) {
		const data = fs.readFileSync(REMINDERS_FILE, 'utf-8');
		return JSON.parse(data);
	}
	return [];
}
/**
* Save reminders to persistent storage
*/
function saveReminders(reminders) {
	fs.writeFileSync(REMINDERS_FILE, JSON.stringify(reminders, null, 2));
}
/**
* Schedule a reminder using background worker process
* Both immediate and delayed reminders use the same worker mechanism
*/
function scheduleReminder(id, title, message, triggerTime) {
	const delay = Math.max(0, triggerTime - Date.now());

	try {
		// Get the worker script path
		const workerScriptPath = path.join(path.dirname(__filename), 'reminder-worker.js');

		// Spawn detached background process to run the worker
		const child = spawn(process.execPath, [
			workerScriptPath,
			REMINDERS_FILE,
			id,
			title,
			message,
			delay.toString(),
			LOG_FILE
		], {
			detached: true,
			stdio: 'ignore',
			windowsHide: true
		});

		// log('INFO', 'Background worker process spawned', { pid: child.pid, id, delay });
		child.unref(); // Allow parent to exit independently
	}
	catch (error) {
		log('ERROR', ModuleName, 'Failed to schedule reminder', { id, error: error.message });
	}
}
/**
* 创建本地提醒事件
*/
function createReminderLocally(title, message, triggerTime) {
	const now = Date.now();
	const id = `reminder_${now}_${Math.random().toString(36).substr(2, 9)}`;
	const reminder = {
		id,
		title,
		message,
		triggerTime,
		created: now,
	};

	// Save to file
	const reminders = loadReminders().filter(item => item && item.triggerTime > now);
	reminders.push(reminder);
	saveReminders(reminders);
	log('LOG', ModuleName, 'Local Reminder List Updated', reminders);

	// Schedule notification
	scheduleReminder(id, title, message, triggerTime);
	// log('INFO', 'Reminder scheduling complete', { id });

	return reminder;
}

/**
 * 主函数
 */
async function main() {
	const args = process.argv.slice(2);

	if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
		console.log('用法: create-reminder.js --title=标题 --message=消息 --time=时间');
		console.log('\n参数:');
		console.log('  --title     提醒标题（必需）');
		console.log('  --message   提醒消息（必需）');
		console.log('  --time      触发时间（必需）');
		console.log('\n时间格式:');
		console.log('  相对时间: "in 10 seconds", "in 30 minutes", "in 2 hours", "in 1 day",');
		console.log('            "in 2 weeks", "in 1 month", "in 1 year"');
		console.log('  绝对时间: ISO 格式，如 "2025-11-24T15:30:00"');
		console.log('\n示例:');
		console.log('  create-reminder.js --title=会议 --message=团队会议 --time="in 30 minutes"');
		console.log('  create-reminder.js --title=约会 --message=下午见面 --time="2025-11-24T15:00:00"');
		process.exit(0);
	}

	try {
		const params = parseNamedArgs(args);

		if (!params.title) {
			throw new Error('缺少必需参数: --title');
		}
		if (!params.message) {
			throw new Error('缺少必需参数: --message');
		}
		if (!params.time) {
			throw new Error('缺少必需参数: --time');
		}

		const triggerTime = parseTime(params.time);

		log('LOG', ModuleName, 'Call Remote Reminder');
		const result = await sendCommand({
			action: 'CREATE_REMINDER',
			data: {
				title: params.title,
				message: params.message,
				triggerTime,
			},
		});
		log('LOG', ModuleName, 'Remote Reminder Result:', result);

		let rid;
		// 如果 CCCore 创建提醒事件成功
		if (result.ok) {
			rid = result.id;
		}
		// 如果 CCCore 创建提醒事件失败，则使用本地方案
		else {
			log('LOG', ModuleName, 'Create Local Reminder');
			const reminder = createReminderLocally(params.title, params.message, triggerTime);
			log('LOG', ModuleName, 'Local Reminder Result:', reminder);
			rid = reminder.id;
		}

		const date = new Date(triggerTime);
		console.log('✅ 提醒创建成功!');
		console.log(`   标题: ${params.title}`);
		console.log(`   消息: ${params.message}`);
		console.log(`   时间: ${date.toLocaleString()}`);
		console.log(`   RID: ${rid}`);
		process.exit(0);
	}
	catch (error) {
		console.error('❌ 创建提醒失败:', error.message);
		process.exit(1);
	}
}

main();

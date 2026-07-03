/**
 * 通用测试数据工厂 - 参数化数据生成与生命周期管理
 * 对应模块：07-测试数据生成策略
 *
 * 使用方式：
 *   node scripts/data-factory.js --template=user-template.json --count=10 --output=data/users.json
 *   node scripts/data-factory.js --template=order-template.json --count=100 --seed=2026
 *   node scripts/data-factory.js --template=bulk.json --count=5 --post-url=http://localhost:3000/api/users
 *
 * 模板文件格式（user-template.json）：
 * {
 *   "name": "$randomName",
 *   "email": "$randomEmail",
 *   "phone": "$randomPhone",
 *   "age": "$randomInt:18:65",
 *   "role": "$pick:admin:editor:viewer",
 *   "status": "active",
 *   "createdAt": "$timestamp",
 *   "balance": "$randomFloat:0:10000:2"
 * }
 *
 * 内置变量：
 *   $randomString:N     — 随机字符串（N 为长度，默认 8）
 *   $randomInt:MIN:MAX  — 随机整数 [MIN, MAX]
 *   $randomFloat:MIN:MAX:DEC — 随机浮点数（DEC 为小数位数，默认 2）
 *   $randomName         — 随机中文名
 *   $randomEmail        — 随机邮箱
 *   $randomPhone        — 随机手机号
 *   $randomId           — 随机 18 位 ID
 *   $randomUUID         — UUID v4
 *   $timestamp          — 当前时间戳（毫秒）
 *   $timestampISO       — ISO 8601 时间
 *   $pick:A:B:C         — 从选项中随机选取
 *   $seq:START          — 自增序列（从 START 开始）
 *   $null:PROB          — 以 PROB 概率返回 null（PROB 为 0~1，默认 0.1）
 *   $custom:JS代码      — 执行自定义 JS 表达式
 */

const fs = require("fs");
const path = require("path");
const http = require("http");
const https = require("https");
const { URL } = require("url");

const args = parseArgs(process.argv.slice(2));

const templatePath = args["--template"];
const count = parseInt(args["--count"] || "1", 10);
const outputPath = args["--output"];
const postUrl = args["--post-url"];
const seed = args["--seed"] ? parseInt(args["--seed"], 10) : Date.now();
const cleanupFile = args["--cleanup-file"];

if (!templatePath) {
  console.error("错误：必须指定 --template 参数");
  console.error("用法：node scripts/data-factory.js --template=user-template.json --count=10 [--output=data.json] [--post-url=http://...] [--seed=2026]");
  process.exit(1);
}

const templateFile = path.resolve(templatePath);
if (!fs.existsSync(templateFile)) {
  console.error(`错误：模板文件不存在: ${templateFile}`);
  process.exit(1);
}

const template = JSON.parse(fs.readFileSync(templateFile, "utf-8"));

let sequence = {};

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const eqIdx = argv[i].indexOf("=");
      if (eqIdx > -1) {
        result[argv[i].substring(0, eqIdx)] = argv[i].substring(eqIdx + 1);
      } else {
        const next = argv[i + 1];
        if (next && !next.startsWith("--")) {
          result[argv[i]] = next;
          i++;
        } else {
          result[argv[i]] = "";
        }
      }
    }
  }
  return result;
}

function seededRandom(seed) {
  let s = seed;
  return function () {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

const random = seededRandom(seed);

const surnames = ["张", "李", "王", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "马", "胡", "朱", "郭", "何", "罗", "高", "林"];
const givenNames = ["伟", "芳", "娜", "敏", "静", "强", "磊", "洋", "勇", "艳", "杰", "军", "秀英", "秀兰", "桂英", "建华", "建国", "志强", "志明", "文博"];

function randomName() {
  const s = surnames[Math.floor(random() * surnames.length)];
  const g = givenNames[Math.floor(random() * givenNames.length)];
  return s + g;
}

function randomEmail() {
  const prefixes = ["test", "user", "demo", "qa", "dev", "admin", "member", "guest"];
  const domains = ["example.com", "test.com", "qa.local", "demo.dev", "mock.org"];
  const prefix = prefixes[Math.floor(random() * prefixes.length)];
  const domain = domains[Math.floor(random() * domains.length)];
  return `${prefix}_${Date.now().toString(36)}_${Math.floor(random() * 1000)}@${domain}`;
}

function randomPhone() {
  const prefixes = ["138", "139", "150", "151", "152", "158", "159", "186", "187", "188"];
  const prefix = prefixes[Math.floor(random() * prefixes.length)];
  return prefix + String(Math.floor(random() * 100000000)).padStart(8, "0");
}

function randomId() {
  const area = String(Math.floor(random() * 900000) + 100000);
  const birth = `19${String(Math.floor(random() * 50) + 50).padStart(2, "0")}${String(Math.floor(random() * 12) + 1).padStart(2, "0")}${String(Math.floor(random() * 28) + 1).padStart(2, "0")}`;
  const suffix = String(Math.floor(random() * 1000)).padStart(3, "0");
  return area + birth + suffix + "X";
}

function resolveValue(value, index) {
  if (typeof value !== "string") return value;

  if (value === "$randomName") return randomName();
  if (value === "$randomEmail") return randomEmail();
  if (value === "$randomPhone") return randomPhone();
  if (value === "$randomId") return randomId();
  if (value === "$timestamp") return Date.now().toString();
  if (value === "$timestampISO") return new Date().toISOString();

  const uuidMatch = value.match(/^\$randomUUID$/);
  if (uuidMatch) {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
      const r = (random() * 16) | 0;
      const v = c === "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  const strMatch = value.match(/^\$randomString:(\d+)$/);
  if (strMatch) {
    const len = parseInt(strMatch[1], 10);
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let result = "";
    for (let i = 0; i < len; i++) {
      result += chars.charAt(Math.floor(random() * chars.length));
    }
    return result;
  }

  const intMatch = value.match(/^\$randomInt:(-?\d+):(-?\d+)$/);
  if (intMatch) {
    const min = parseInt(intMatch[1], 10);
    const max = parseInt(intMatch[2], 10);
    return Math.floor(random() * (max - min + 1)) + min;
  }

  const floatMatch = value.match(/^\$randomFloat:(-?\d+):(-?\d+):(\d+)$/);
  if (floatMatch) {
    const min = parseFloat(floatMatch[1]);
    const max = parseFloat(floatMatch[2]);
    const dec = parseInt(floatMatch[3], 10);
    return parseFloat((random() * (max - min) + min).toFixed(dec));
  }

  const pickMatch = value.match(/^\$pick:(.+)$/);
  if (pickMatch) {
    const options = pickMatch[1].split(":");
    return options[Math.floor(random() * options.length)];
  }

  const seqMatch = value.match(/^\$seq:(\d+)$/);
  if (seqMatch) {
    const key = seqMatch[0];
    if (sequence[key] === undefined) sequence[key] = parseInt(seqMatch[1], 10);
    return sequence[key]++;
  }

  const nullMatch = value.match(/^\$null:?(\d*\.?\d*)$/);
  if (nullMatch) {
    const prob = nullMatch[1] ? parseFloat(nullMatch[1]) : 0.1;
    return random() < prob ? null : value;
  }

  const customMatch = value.match(/^\$custom:(.+)$/);
  if (customMatch) {
    try {
      const fn = new Function("random", "index", `return ${customMatch[1]}`);
      return fn(random, index);
    } catch (e) {
      return `[自定义表达式错误: ${e.message}]`;
    }
  }

  return value;
}

function generateRecord(template, index) {
  if (typeof template !== "object" || template === null) {
    return resolveValue(template, index);
  }

  if (Array.isArray(template)) {
    return template.map((item) => generateRecord(item, index));
  }

  const result = {};
  for (const [key, value] of Object.entries(template)) {
    result[key] = generateRecord(value, index);
  }
  return result;
}

function postRecord(record, url) {
  return new Promise((resolve) => {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === "https:" ? https : http;
    const body = JSON.stringify(record);

    const req = client.request(
      url,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        timeout: 10000,
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          let parsed;
          try {
            parsed = JSON.parse(data);
          } catch {
            parsed = data;
          }
          resolve({
            success: res.statusCode >= 200 && res.statusCode < 300,
            status: res.statusCode,
            response: parsed,
            request: record,
          });
        });
      }
    );

    req.on("error", (err) => {
      resolve({ success: false, status: 0, response: err.message, request: record });
    });

    req.write(body);
    req.end();
  });
}

async function main() {
  console.log("=".repeat(60));
  console.log("测试数据工厂");
  console.log("=".repeat(60));
  console.log(`模板文件: ${templateFile}`);
  console.log(`生成数量: ${count}`);
  console.log(`随机种子: ${seed}`);
  if (outputPath) console.log(`输出文件: ${outputPath}`);
  if (postUrl) console.log(`POST URL: ${postUrl}`);
  console.log("-".repeat(60));

  const records = [];
  for (let i = 0; i < count; i++) {
    const record = generateRecord(template, i);
    records.push(record);
  }

  console.log(`\n生成 ${records.length} 条记录`);

  if (records.length <= 3) {
    records.forEach((r, i) => {
      console.log(`  [${i + 1}] ${JSON.stringify(r).substring(0, 200)}`);
    });
  } else {
    console.log(`  前 3 条预览:`);
    records.slice(0, 3).forEach((r, i) => {
      console.log(`  [${i + 1}] ${JSON.stringify(r).substring(0, 200)}`);
    });
    console.log(`  ... 还有 ${records.length - 3} 条`);
  }

  const createdIds = [];

  if (postUrl) {
    console.log(`\n写入数据到 ${postUrl} ...`);
    let successCount = 0;
    for (let i = 0; i < records.length; i++) {
      const result = await postRecord(records[i], postUrl);
      if (result.success) {
        successCount++;
        const id = result.response?.id || result.response?.data?.id;
        if (id) createdIds.push(id);
        if (i % 10 === 0 || i === records.length - 1) {
          process.stdout.write(`\r  进度: ${i + 1}/${records.length} (${successCount} 成功)`);
        }
      }
    }
    console.log(`\n  完成: ${successCount}/${records.length} 条写入成功`);
  }

  if (outputPath) {
    const outFile = path.resolve(outputPath);
    const dir = path.dirname(outFile);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(outFile, JSON.stringify(records, null, 2), "utf-8");
    console.log(`\n数据已写入: ${outFile}`);
  }

  if (cleanupFile && createdIds.length > 0) {
    const cleanupPath = path.resolve(cleanupFile);
    const existing = fs.existsSync(cleanupPath) ? JSON.parse(fs.readFileSync(cleanupPath, "utf-8")) : { ids: [] };
    existing.ids = [...new Set([...existing.ids, ...createdIds])];
    existing.generatedAt = new Date().toISOString();
    existing.template = templateFile;
    fs.writeFileSync(cleanupPath, JSON.stringify(existing, null, 2), "utf-8");
    console.log(`清理清单已更新: ${cleanupPath}（${existing.ids.length} 个 ID）`);
  }

  console.log("\n完成");
  process.exit(0);
}

main().catch((err) => {
  console.error("数据工厂执行异常:", err.message);
  process.exit(1);
});
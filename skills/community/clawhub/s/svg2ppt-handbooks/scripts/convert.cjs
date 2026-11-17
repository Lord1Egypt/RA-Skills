#!/usr/bin/env node
/**
 * svg2pptskill - Call the handbooks.cn SVG-to-PPTX conversion API.
 *
 * Usage:
 *     node scripts/convert.cjs <key> <svg>
 *     echo "<svg>" | node scripts/convert.cjs <key>
 *
 * Examples:
 *     node scripts/convert.cjs SVG2PPTSKILL-xxx map:四川
 *     node scripts/convert.cjs SVG2PPTSKILL-xxx map:Anhui
 *     echo "char:中" | node scripts/convert.cjs SVG2PPTSKILL-xxx
 *     node scripts/convert.cjs SVG2PPTSKILL-xxx '<svg xmlns="http://www.w3.org/2000/svg">...</svg>'
 *
 * Note: OpenClaw on Windows passes Unicode argv correctly to Node.js, so Chinese
 * characters in command-line arguments are preserved. This script also supports
 * stdin for manual piping.
 */

const https = require("https");
const http = require("http");

const API_URL = "https://www.handbooks.cn/api/skill/convert";

// English / alias -> Chinese map names used by the API
const MAP_ALIASES = {
    // Countries
    "chinese": "中国",
    "china": "中国",
    "america": "美国",
    "united states": "美国",
    "usa": "美国",
    "us": "美国",
    "japan": "日本",
    "uk": "英国",
    "britain": "英国",
    "united kingdom": "英国",
    "england": "英国",
    "france": "法国",
    "germany": "德国",
    "russia": "俄罗斯",
    "india": "印度",
    "brazil": "巴西",
    "australia": "澳大利亚",
    "canada": "加拿大",
    "korea": "韩国",
    "south korea": "韩国",
    "italy": "意大利",
    "spain": "西班牙",
    "mexico": "墨西哥",
    "thailand": "泰国",
    "argentina": "阿根廷",
    "egypt": "埃及",
    "ireland": "爱尔兰",
    "austria": "奥地利",
    "uae": "阿联酋",
    "united arab emirates": "阿联酋",
    "pakistan": "巴基斯坦",
    "bulgaria": "保加利亚",
    "belgium": "比利时",
    "iceland": "冰岛",
    "poland": "波兰",
    "north korea": "朝鲜",
    "denmark": "丹麦",
    "philippines": "菲律宾",
    "finland": "芬兰",
    "colombia": "哥伦比亚",
    "cuba": "古巴",
    "kazakhstan": "哈萨克斯坦",
    "netherlands": "荷兰",
    "czech": "捷克",
    "czech republic": "捷克",
    "qatar": "卡塔尔",
    "kenya": "肯尼亚",
    "kuwait": "科威特",
    "luxembourg": "卢森堡",
    "romania": "罗马尼亚",
    "malaysia": "马来西亚",
    "bangladesh": "孟加拉国",
    "myanmar": "缅甸",
    "burma": "缅甸",
    "mongolia": "蒙古",
    "south africa": "南非",
    "nigeria": "尼日利亚",
    "norway": "挪威",
    "portugal": "葡萄牙",
    "sweden": "瑞典",
    "switzerland": "瑞士",
    "saudi arabia": "沙特阿拉伯",
    "turkey": "土耳其",
    "ukraine": "乌克兰",
    "uzbekistan": "乌兹别克斯坦",
    "greece": "希腊",
    "singapore": "新加坡",
    "new zealand": "新西兰",
    "hungary": "匈牙利",
    "iran": "伊朗",
    "israel": "以色列",
    "indonesia": "印度尼西亚",
    "vietnam": "越南",
    "chile": "智利",
    "peru": "秘鲁",
    "venezuela": "委内瑞拉",
    // World map
    "world": "世界",
    "global": "世界",
    // Chinese provinces / municipalities / autonomous regions (pinyin/English aliases)
    "beijing": "北京", "peking": "北京",
    "shanghai": "上海",
    "tianjin": "天津",
    "chongqing": "重庆",
    "hebei": "河北",
    "shanxi": "山西",
    "neimenggu": "内蒙古", "inner mongolia": "内蒙古",
    "liaoning": "辽宁",
    "jilin": "吉林",
    "heilongjiang": "黑龙江",
    "jiangsu": "江苏",
    "zhejiang": "浙江",
    "anhui": "安徽",
    "fujian": "福建",
    "jiangxi": "江西",
    "shandong": "山东",
    "henan": "河南",
    "hubei": "湖北",
    "hunan": "湖南",
    "guangdong": "广东",
    "guangxi": "广西",
    "hainan": "海南",
    "sichuan": "四川",
    "guizhou": "贵州",
    "yunnan": "云南",
    "xizang": "西藏", "tibet": "西藏",
    "shaanxi": "陕西",
    "gansu": "甘肃",
    "qinghai": "青海",
    "ningxia": "宁夏",
    "xinjiang": "新疆",
    "taiwan": "台湾",
    "hong kong": "香港", "xianggang": "香港",
    "macau": "澳门", "macao": "澳门", "aomen": "澳门",
};

function normalizeSvg(svg) {
    svg = svg.trim();
    // Only normalize map requests; leave char:, SVG code, URLs unchanged
    if (!svg.toLowerCase().startsWith("map:")) {
        return svg;
    }
    const name = svg.slice(4).trim();
    const alias = name.toLowerCase();
    if (MAP_ALIASES[alias]) {
        return "map:" + MAP_ALIASES[alias];
    }
    return svg;
}

function postJson(url, payload) {
    return new Promise((resolve) => {
        const urlObj = new URL(url);
        const mod = urlObj.protocol === "https:" ? https : http;
        const req = mod.request(urlObj, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "User-Agent": "svg2pptskill/1.0.8",
                "Content-Length": Buffer.byteLength(payload)
            }
        }, (res) => {
            let data = "";
            res.setEncoding("utf8");
            res.on("data", chunk => { data += chunk; });
            res.on("end", () => {
                try {
                    const json = JSON.parse(data);
                    if (res.statusCode >= 400) {
                        resolve({ success: false, status_code: res.statusCode, ...json });
                    } else {
                        resolve(json);
                    }
                } catch (e) {
                    resolve({ success: false, error: data || res.statusMessage });
                }
            });
        });
        req.on("error", (e) => resolve({ success: false, error: e.message }));
        req.write(payload);
        req.end();
    });
}

async function convert(key, svg) {
    const payload = JSON.stringify({ skill: "svg2pptskill", key, svg });
    return postJson(API_URL, payload);
}

function readStdin() {
    return new Promise((resolve) => {
        let data = "";
        process.stdin.setEncoding("utf8");
        process.stdin.on("data", chunk => { data += chunk; });
        process.stdin.on("end", () => resolve(data));
    });
}

async function main() {
    const argv = process.argv.slice(2); // remove "node" and script path

    if (argv.length < 1) {
        console.log(JSON.stringify({
            success: false,
            error: "Usage: node scripts/convert.cjs <key> <svg>"
        }));
        process.exit(1);
    }

    const key = argv[0];

    let svgInput;
    if (argv.length >= 2 && argv[1] !== "" && argv[1] !== "-") {
        svgInput = argv[1];
    } else if (!process.stdin.isTTY) {
        svgInput = await readStdin();
    } else {
        console.log(JSON.stringify({
            success: false,
            error: "Missing svg value. Provide it as the second argument or via stdin."
        }));
        process.exit(1);
    }

    const svg = normalizeSvg(svgInput);
    const result = await convert(key, svg);
    console.log(JSON.stringify(result, null, 2));
}

main().catch((e) => {
    console.log(JSON.stringify({ success: false, error: e.message }));
    process.exit(1);
});

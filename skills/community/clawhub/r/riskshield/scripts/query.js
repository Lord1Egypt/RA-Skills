/**
 * RiskShield Case Query Script
 * Query cases and extract context token (o parameter)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { login } = require('./login.js');

const TOKEN_FILE = path.join(__dirname, '..', 'token.json');
const API_BASE = 'riskshield.dcsuat.com';

/**
 * Make HTTPS request
 */
function httpsRequest(options, postData) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve({ statusCode: res.statusCode, headers: res.headers, body: JSON.parse(data) });
                } catch (e) {
                    resolve({ statusCode: res.statusCode, headers: res.headers, body: data });
                }
            });
        });
        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

/**
 * Load token
 */
function loadToken() {
    try {
        const data = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
        return data.token;
    } catch (e) {
        return null;
    }
}

/**
 * Check if re-login needed
 */
function isTokenExpired() {
    try {
        const data = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
        if (!data.expire) return true;
        return Date.now() > data.expire - 60000;
    } catch (e) {
        return true;
    }
}

/**
 * Query cases
 */
async function queryCases(caseCode) {
    if (isTokenExpired()) {
        console.log('Token expired, re-logging in...');
        await login();
    }
    
    const token = loadToken();
    if (!token) throw new Error('Not logged in');
    
    // Query for today to recent
    const now = Date.now();
    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    
    const postData = JSON.stringify({
        startTime: startOfDay.getTime(),
        endTime: now,
        caseCode: caseCode || '',
        caseName: '',
        customerCardNo: '',
        customerName: '',
        customerPhone: '',
        range: 'ALL',
        sort: 'desc',
        size: 20,
        page: 0,
        businessType: '',
        approveUserId: '',
        businessCode: 'All'
    });
    
    const options = {
        hostname: API_BASE,
        path: '/anytask-web/task/case/list/all',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html',
            'Origin': 'https://' + API_BASE,
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    
    console.log('Querying cases...');
    let result = await httpsRequest(options, postData);
    
    if (result.statusCode === 401) {
        await login();
        const newToken = loadToken();
        options.headers['Authorization'] = `Bearer ${newToken}`;
        result = await httpsRequest(options, postData);
    }
    
    return result.body;
}

// Run if called directly
if (require.main === module) {
    const caseCode = process.argv[2];
    
    if (!caseCode) {
        console.log('Usage: node query.js <caseCode>');
        console.log('Example: node query.js 2604131000000597548');
        process.exit(1);
    }
    
    queryCases(caseCode)
        .then(result => {
            if (result.data && result.data.content) {
                const cases = result.data.content;
                if (cases.length === 0) {
                    console.log('No cases found');
                } else {
                    console.log(`Found ${cases.length} case(s):`);
                    cases.forEach((c, i) => {
                        console.log(`\n--- Case ${i + 1} ---`);
                        console.log(`caseCode: ${c.caseCode}`);
                        console.log(`taskNo: ${c.taskNo}`);
                        console.log(`applyInfoId: ${c.applyInfoId}`);
                        console.log(`caseStatus: ${c.caseStatus}`);
                        console.log(`resultStatus: ${c.resultStatus}`);
                        // Build o parameter
                        const o = Buffer.from(JSON.stringify({
                            caseCode: c.caseCode,
                            taskNo: c.taskNo,
                            applyInfoId: c.applyInfoId
                        })).toString('base64');
                        console.log(`o parameter: ${o}`);
                    });
                }
            } else {
                console.log('Response:', JSON.stringify(result, null, 2));
            }
            process.exit(0);
        })
        .catch(error => {
            console.error('FAILED:', error.message);
            process.exit(1);
        });
}

module.exports = { queryCases };

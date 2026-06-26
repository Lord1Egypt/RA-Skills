/**
 * RiskShield Login Script
 * Directly calls the login API with properly formatted sign parameter
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const TOKEN_FILE = path.join(__dirname, '..', 'token.json');
const API_BASE = 'riskshield.dcsuat.com';

// Configuration
const CONFIG = {
    username: 'alan.zhang',
    password: 'ZIdongshenpi1.',
    loginUrl: 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s',
    redirectUrl: 'aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s'
};

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
 * Generate random hex string
 */
function randomHex(length) {
    let result = '';
    for (let i = 0; i < length; i++) {
        result += Math.floor(Math.random() * 16).toString(16);
    }
    return result;
}

/**
 * Build the sign parameter (base64 encoded JSON)
 */
function buildSign(username, password, ts) {
    const codeKey = randomHex(32);
    const payload = {
        username: username,
        password: password,
        securityCode: '',
        codeKey: codeKey,
        ts: ts
    };
    const jsonStr = JSON.stringify(payload);
    // base64 encode
    const base64 = Buffer.from(jsonStr).toString('base64');
    return base64;
}

/**
 * Login to RiskShield
 */
async function login() {
    console.log('Logging into RiskShield...');
    
    const ts = Date.now();
    const sign = buildSign(CONFIG.username, CONFIG.password, ts);
    
    const postData = JSON.stringify({
        sign: sign,
        ts: ts,
        address: CONFIG.redirectUrl,
        loginType: 'oa'
    });
    
    const options = {
        hostname: API_BASE,
        path: '/auth/login',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest, XMLHttpRequest',
            'Referer': CONFIG.loginUrl,
            'Origin': 'https://' + API_BASE,
            'Authorization': 'Bearer',
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    
    console.log('Sending login request...');
    const result = await httpsRequest(options, postData);
    
    if (result.statusCode === 200 && result.body && result.body.token) {
        console.log('Login successful!');
        
        const tokenData = {
            token: result.body.token,
            secretToken: result.body.secretToken || '',
            expire: result.body.expire || (Date.now() + 24 * 60 * 60 * 1000),
            obtainedAt: new Date().toISOString()
        };
        
        // Save token
        fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokenData, null, 2));
        console.log(`Token saved to ${TOKEN_FILE}`);
        console.log(`Token expires at: ${new Date(tokenData.expire).toISOString()}`);
        
        return tokenData;
    } else {
        console.error('Login failed:', result.body);
        throw new Error(`Login failed: ${JSON.stringify(result.body)}`);
    }
}

module.exports = { login };

// Run if called directly
if (require.main === module) {
    login()
        .then(result => {
            console.log('SUCCESS - Token obtained');
            process.exit(0);
        })
        .catch(error => {
            console.error('FAILED:', error.message);
            process.exit(1);
        });
}

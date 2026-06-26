/**
 * RiskShield Approve/Reject Script v3
 * 
 * 支持三种审批模式：
 * 1. full 模式（默认）：调用 baseCaseInfo 获取完整字段，然后审批
 * 2. quick 模式：minimal 参数快速审批
 * 3. force 模式：跳过查询，直接用 caseCode 审批
 * 
 * 注意：approve API 可能需要浏览器 session token，当前 login 获取的 token 
 * 在某些环境下可能权限不足。如果 approve 返回 unknown error，
 * 可能是 token 权限问题，需要从浏览器获取有效 token。
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
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                const raw = Buffer.concat(chunks);
                try {
                    resolve({ statusCode: res.statusCode, headers: res.headers, body: JSON.parse(raw.toString()) });
                } catch (e) {
                    resolve({ statusCode: res.statusCode, headers: res.headers, body: raw.toString() });
                }
            });
        });
        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

/**
 * Load token from file
 */
function loadToken() {
    try {
        const data = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
        if (!data.token) throw new Error('No token found');
        return data.token;
    } catch (e) {
        return null;
    }
}

/**
 * Check if token is expired (with 1 min buffer)
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
 * Build context token (base64 encoded JSON with caseCode, taskNo, applyInfoId)
 */
function buildContextToken(caseCode, taskNo, applyInfoId) {
    const payload = { caseCode, taskNo, applyInfoId };
    return Buffer.from(JSON.stringify(payload)).toString('base64');
}

/**
 * Query case detail from list API
 */
async function queryCaseList(caseNo) {
    if (isTokenExpired()) {
        console.log('Token expired or missing, auto re-logging in...');
        await login();
    }
    
    const token = loadToken();
    const now = Date.now();
    const weekAgo = now - 7 * 24 * 60 * 60 * 1000;
    
    const postData = JSON.stringify({
        startTime: weekAgo,
        endTime: now,
        caseCode: caseNo,
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
            'Accept': 'application/json, text/plain, */*',
            'Authorization': `Bearer ${token}`,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html',
            'Origin': 'https://' + API_BASE,
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    
    const result = await httpsRequest(options, postData);
    
    if (result.statusCode !== 200) {
        throw new Error(`Query case API returned ${result.statusCode}`);
    }
    
    // API returns {code: 9999, message: "unknown error"} on failure
    if (result.body?.code === 9999) {
        throw new Error(`Query case API error: ${result.body.message}`);
    }
    
    if (!result.body?.caseList && !result.body?.data?.caseList) {
        throw new Error(`Query case API error: unexpected response format`);
    }
    
    const list = result.body.caseList || result.body.data?.caseList || [];
    const targetCase = list.find(c => c.caseCode === caseNo);
    
    if (!targetCase) {
        throw new Error(`Case ${caseNo} not found in query result`);
    }
    
    return {
        taskNo: targetCase.detailTaskNo || targetCase.taskNo,
        userId: targetCase.userId,
        caseData: targetCase
    };
}

/**
 * Get baseCaseInfo to fetch applyInfoId and full case data
 */
async function getBaseCaseInfo(caseNo, taskNo, applyInfoId) {
    const token = loadToken();
    const o = buildContextToken(caseNo, taskNo, applyInfoId);
    
    const postData = JSON.stringify({
        url: 'baseCaseInfo',
        params: {},
        c: '3',
        o: o
    });
    
    const options = {
        hostname: API_BASE,
        path: '/anyform-web/frm/form/http',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://riskshield.dcsuat.com/anyform-web/frm/anyform/index.html',
            'Origin': 'https://' + API_BASE,
            'channel': 'T_P',
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    
    const result = await httpsRequest(options, postData);
    
    if (result.statusCode !== 200 || result.body?.code !== 1000) {
        throw new Error(`baseCaseInfo API error: ${JSON.stringify(result.body)}`);
    }
    
    return result.body.data;
}

/**
 * Build parameterFields from baseCaseInfo data
 */
function buildParameterFields(bcData, caseNo) {
    return {
        caseCode: bcData.caseCode || caseNo,
        businessTypeCode: bcData.businessTypeCode || '11',
        channelNo: bcData.channelNo || 'WEB3-GENERAL',
        originCaseCode: bcData.originCaseCode || '',
        appType: bcData.appType || 'H5',
        productCode: bcData.productCode || '',
        productType: bcData.productType || '',
        productTypeParents: bcData.productTypeParents || '',
        sub_organ: bcData.sub_organ || '',
        sub_orgname: bcData.sub_orgname || '',
        custName: bcData.custName || bcData.customerName || '',
        aliasName: '',
        LastMobile: bcData.mobile || '',
        race: bcData.race || '',
        age: bcData.age || '',
        maritalStatus: bcData.maritalStatus || '',
        LastEmail: bcData.email || '',
        icNumber: bcData.icNumber || bcData.perIcNumber || '',
        gender: bcData.gender || '',
        appResidentProperty: bcData.appResidentProperty || '',
        appIdType: bcData.appIdType || '',
        appResidencyCode: bcData.appResidencyCode || '',
        keyRefNo: bcData.keyRefNo || '',
        isConfirm: bcData.isConfirm || '',
        birthDate: bcData.birthDate || '',
        residentCountryCode: bcData.residentCountryCode || '',
        residentAddress1: bcData.residentAddress1 || '',
        residentAddress2: bcData.residentAddress2 || '',
        residentAddress3: bcData.residentAddress3 || '',
        residentAddress4: bcData.residentAddress4 || '',
        residentPostalCode: bcData.residentPostalCode || '',
        billingAddressCountryCode: bcData.billingAddressCountryCode || '',
        billingAddress1: bcData.billingAddress1 || '',
        billingPostalCode: bcData.billingPostalCode || '',
        nationality: bcData.nationality || '',
        incomeYear: bcData.incomeYear || '',
        employer: bcData.employer || '',
        employmentSector: bcData.employmentSector || '',
        profession: bcData.profession || '',
        jobSeniority: bcData.jobSeniority || '',
        serviceYears: bcData.serviceYears || '',
        selfEmployment: bcData.selfEmployment || '',
        sourceOfFunds: bcData.sourceOfFunds || '',
        sourceOfWealth: bcData.sourceOfWealth || '',
        sourceOfFundsCountry: bcData.sourceOfFundsCountry || '',
        accountType: bcData.accountType || '',
        applyType: bcData.applyType || '',
        cardType: bcData.cardType || '',
        cardIssuer: bcData.cardIssuer || '',
        preNameOnCard: bcData.preNameOnCard || '',
        preCreditLimit: bcData.preCreditLimit || '',
        poaType: '',
        poaCountry: '',
        poaDate: '',
        empPassExpiryDate: '',
        primaryCardNumber: '',
        isRecommend: '',
        confirmDate: '',
        source: '',
        salesStaff: bcData.salesStaff || '',
        motherName: '',
        jobDuties: '',
        companyPhone: '',
        basicSalary: '',
        yearJoined: '',
        serviceMonths: '',
        dncFlag: bcData.dncFlag || '',
        residentType: '',
        location: '',
        incomeMonth: '',
        pdpaFlag: bcData.pdpaFlag || '',
        usaTaxTIN: bcData.usaTaxTIN || '',
        stateCode: '',
        usaTaxResident: bcData.usaTaxResident || '',
        proOwnStatus: '',
        cpfLastEmployName: '',
        homeCountryIdType: bcData.homeCountryIdType || '',
        homeCountryIdNumber: bcData.homeCountryIdNumber || '',
        occupationMom: '',
        employerMom: '',
        workPassType: '',
        workPassStatus: '',
        workPassExpireDate: '',
        noALatestYearOfAssesment: '',
        noALatestYearAmount: '',
        noASecondYearOfAssesment: '',
        noASecondYearAmount: '',
        companyName: '',
        companyNameManual: '',
        professionManual: '',
        mobileManual: '',
        selfEmploymentManual: '',
        appClass: bcData.appClass || '',
        appClassManual: '',
        incomeYearManual: '',
        residentPostalCodeManual: '',
        billingPostalCodeManual: '',
        passport: bcData.passport || '',
        passportManual: '',
        email: bcData.email || '',
        emailManual: '',
        preCreditLimitManual: '',
        residentAddressCity: '',
        residentAddressCityManual: '',
        residentAddressState: '',
        residentAddressStateManual: '',
        residentAddress1Manual: '',
        residentAddress2Manual: '',
        residentAddress3Manual: '',
        residentAddress4Manual: '',
        residentAddress5Manual: '',
        billingAddressCity: '',
        billingAddressCityManual: '',
        billingAddressState: '',
        billingAddressStateManual: '',
        billingAddress1Manual: '',
        billingAddress2Manual: '',
        billingAddress3Manual: '',
        billingAddress4Manual: '',
        billingAddress5Manual: '',
        amt: String(bcData.amt || '100'),
        finalAI: bcData.finalAI || '',
        resultStatus: '',
        approveUserId: bcData.approveUserId || 'system default user',
        caseStatus: bcData.caseStatus || 'processing',
        closeTime: bcData.closeTime || '',
        refuseCode: '',
        refuseCodeOut: '',
        strategy_desc: bcData.strategy_desc || '',
        appLabelLevel: bcData.appLabelLevel || '',
        appLabelType: bcData.appLabelType || '',
        appLabelValue: bcData.appLabelValue || '',
        appLabelAgentCode: bcData.appLabelAgentCode || '',
        appLayoutCode: bcData.appLayoutCode || '',
        appLoyaltyProjectId: '',
        appLoyaltyAccountType: '',
        appLoyaltyAccountNumber: '',
        appLoyaltyFamily: '',
        appLoyaltyGiven: '',
        eddBlk: bcData.eddBlk || '',
        pepBlk: bcData.pepBlk || '',
        sanctionBlk: bcData.sanctionBlk || '',
        overallRiskScore: bcData.overallRiskScore || '',
        overallRiskGrading: bcData.overallRiskGrading || '',
        countryRiskScore: bcData.countryRiskScore || '',
        countryRiskGrading: bcData.countryRiskGrading || '',
        clientRiskScore: bcData.clientRiskScore || '',
        clientRiskGrading: bcData.clientRiskGrading || '',
        cardProductRiskScore: bcData.cardProductRiskScore || '',
        cardProductRiskGrading: bcData.cardProductRiskGrading || '',
        channelRiskScore: bcData.channelRiskScore || '',
        channelRiskGrading: bcData.channelRiskGrading || '',
        screeningRiskScore: bcData.screeningRiskScore || '',
        screeningRiskGrading: bcData.screeningRiskGrading || '',
        eddTag: bcData.eddTag || '',
        caExternalIdentifier: bcData.caExternalIdentifier || '',
        caCustomerId: bcData.caCustomerId || '',
        riskBlacklistCheckResult: String(bcData.riskBlacklistCheckResult || ''),
        documentSubmittedByApplicant: '',
        version: bcData.version || '',
        flag: bcData.flag || '',
        ECM: bcData.ECM || '',
        caseId: bcData.caseId || 0
    };
}

/**
 * Build quick mode parameterFields (minimal)
 */
function buildQuickParameterFields(caseData, caseNo) {
    return {
        caseCode: caseNo,
        custName: caseData.customerName || '',
        approveUserId: caseData.approveUserId || 'system default user',
        caseStatus: caseData.caseStatus || 'processing',
        strategy_desc: caseData.strategyDesc || '',
        amt: caseData.amt || '100',
        overallRiskScore: caseData.overallRiskScore || '',
        overallRiskGrading: caseData.overallRiskGrading || ''
    };
}

/**
 * Approve or Reject a case
 */
async function processCase(caseNo, action, params = {}) {
    const mode = params.mode || 'full';
    
    console.log(`\n[${mode.toUpperCase()} MODE] Processing case: ${caseNo}`);
    
    let caseInfo;
    let bcData = null;
    
    if (mode === 'force') {
        // Force mode: use minimal defaults
        console.log('  [FORCE MODE] Skipping query, using minimal defaults');
        caseInfo = {
            taskNo: params.taskNo || '',
            userId: params.applyInfoId || 0,
            caseData: {
                caseCode: caseNo,
                caseStatus: 'processing',
                customerName: 'Unknown',
                approveUserId: 'system default user',
                strategyDesc: '',
                overallRiskScore: '',
                overallRiskGrading: ''
            }
        };
    } else {
        // Query case list first
        try {
            caseInfo = await queryCaseList(caseNo);
            console.log(`  Found: ${caseInfo.caseData.caseName || caseInfo.caseData.customerName}`);
            console.log(`  taskNo: ${caseInfo.taskNo}`);
            console.log(`  userId: ${caseInfo.userId}`);
        } catch (queryErr) {
            console.warn(`  ⚠️  Query failed: ${queryErr.message}`);
            if (mode === 'full') {
                console.warn('   Falling back to force mode...');
                caseInfo = {
                    taskNo: params.taskNo || '',
                    userId: params.applyInfoId || 0,
                    caseData: { caseCode: caseNo, caseStatus: 'processing', customerName: 'Unknown', approveUserId: 'system default user' }
                };
            } else {
                throw queryErr;
            }
        }
    }
    
    // Ensure logged in
    if (isTokenExpired()) {
        console.log('Token expired, auto re-logging in...');
        await login();
    }
    
    const token = loadToken();
    if (!token) {
        throw new Error('Not logged in. Please run login first.');
    }
    
    let parameterFields;
    let taskNo = caseInfo.taskNo;
    let applyInfoId = caseInfo.userId || params.applyInfoId || 0;
    
    if (mode === 'full') {
        // Get baseCaseInfo for full parameterFields and correct applyInfoId
        try {
            console.log('  Fetching baseCaseInfo for complete data...');
            bcData = await getBaseCaseInfo(caseNo, taskNo, applyInfoId);
            
            // Update applyInfoId from baseCaseInfo
            if (bcData.caseId) {
                applyInfoId = bcData.caseId;
            }
            
            parameterFields = buildParameterFields(bcData, caseNo);
            
            // Override amt if provided
            if (params.amt) {
                parameterFields.amt = String(params.amt);
            }
            
            console.log(`  baseCaseInfo fetched, caseStatus: ${bcData.caseStatus}`);
        } catch (bcErr) {
            console.warn(`  ⚠️  baseCaseInfo failed: ${bcErr.message}`);
            console.warn('   Using case list data instead...');
            parameterFields = buildQuickParameterFields(caseInfo.caseData, caseNo);
        }
    } else {
        parameterFields = buildQuickParameterFields(caseInfo.caseData, caseNo);
    }
    
    // Override taskNo if provided
    if (params.taskNo) {
        taskNo = params.taskNo;
        console.log(`  taskNo overridden: ${taskNo}`);
    }
    
    // Build approveFields
    let approveFields;
    if (action === 'approve') {
        approveFields = {
            taskApproveList: [],
            approveResult: 'Y',
            amt: parseFloat(parameterFields.amt) || 100
        };
    } else if (action === 'reject') {
        approveFields = {
            taskApproveList: [],
            approveResult: 'N',
            manualRefuseCode: params.refuseCode || '4035'
        };
    } else {
        throw new Error(`Unknown action: ${action}. Use 'approve' or 'reject'`);
    }
    
    // Build commitContent
    const commitContent = {
        parameterFields: parameterFields,
        approveFields: approveFields,
        files: {}
    };
    
    // Build context token (o param)
    const o = buildContextToken(caseNo, taskNo, applyInfoId);
    
    // Build request
    const postData = JSON.stringify({
        url: 'approve',
        param: {
            commitContent: JSON.stringify(commitContent)
        },
        c: '3',
        o: o
    });
    
    const options = {
        hostname: API_BASE,
        path: '/anyform-web/frm/form/http',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`,
            'X-Requested-With': 'XMLHttpRequest',
            'channel': 'T_P',
            'Referer': 'https://riskshield.dcsuat.com/anyform-web/frm/anyform/index.html',
            'Origin': 'https://' + API_BASE,
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    
    console.log(`\n${action === 'approve' ? 'Approving' : 'Rejecting'} case: ${caseNo}`);
    console.log(`  amt: ${approveFields.amt}`);
    if (action === 'reject') {
        console.log(`  refuseCode: ${approveFields.manualRefuseCode}`);
    }
    
    let result = await httpsRequest(options, postData);
    
    // If 401, re-login and retry once
    if (result.statusCode === 401) {
        console.log('Token rejected, re-logging in...');
        await login();
        
        const newToken = loadToken();
        options.headers['Authorization'] = `Bearer ${newToken}`;
        result = await httpsRequest(options, postData);
    }
    
    if (result.statusCode === 200) {
        const body = typeof result.body === 'string' ? JSON.parse(result.body) : result.body;
        
        if (body.code === 1000 || body.success === true) {
            console.log('\n✅ SUCCESS:', body.message || 'Approved');
            return body;
        } else {
            console.log('\n⚠️  API returned error:', body.message || JSON.stringify(body));
            console.log('   Note: This may be due to token permissions. The approve API');
            console.log('   may require a browser session token rather than login token.');
            return body;
        }
    } else {
        console.error('\n❌ API Error:', result.statusCode, result.body);
        throw new Error(`API returned ${result.statusCode}`);
    }
}

// ============== Main CLI ==============
const args = process.argv.slice(2);
const action = args[0];
const caseNo = args[1];

if (!action || !caseNo) {
    console.log(`
RiskShield Approve/Reject Script v3
====================================

Usage:
  node approve.js approve <caseNo> [amt] [--full|--quick|--force]
  node approve.js reject <caseNo> <refuseCode> [--full|--quick|--force]

Modes:
  --full   (default) Get baseCaseInfo for complete parameterFields, then approve
  --quick          Use case list data only (faster)
  --force          Skip all queries, use minimal defaults (use when list API is down)

Options:
  --taskNo <val>       Override taskNo
  --applyInfoId <val>  Override applyInfoId (for force mode)

Examples:
  # Full mode (recommended):
  node approve.js approve 2604131000000597570
  
  # Full mode with custom amount:
  node approve.js approve 2604131000000597570 50000
  
  # Quick mode:
  node approve.js approve 2604131000000597570 100 --quick
  
  # Force mode (when APIs are unstable):
  node approve.js approve 2604131000000597570 100 --force
  
  # Reject:
  node approve.js reject 2604131000000597570 4035

Note:
  If approve returns "unknown error", the approve API may require a 
  browser session token. The login API gets a standard Bearer token
  which may lack approve permissions.
`);
    process.exit(1);
}

const params = {
    mode: args.includes('--quick') ? 'quick' : (args.includes('--force') ? 'force' : 'full')
};

const taskNoIdx = args.indexOf('--taskNo');
const applyInfoIdIdx = args.indexOf('--applyInfoId');
if (taskNoIdx !== -1 && args[taskNoIdx + 1]) params.taskNo = args[taskNoIdx + 1];
if (applyInfoIdIdx !== -1 && args[applyInfoIdIdx + 1]) params.applyInfoId = parseInt(args[applyInfoIdIdx + 1]);

if (action === 'approve') {
    const amtIdx = args.findIndex((a, i) => i > 0 && !a.startsWith('--') && a !== 'approve' && a !== caseNo);
    params.amt = amtIdx !== -1 ? parseInt(args[amtIdx]) : 100;
} else if (action === 'reject') {
    params.refuseCode = args[2] || '4035';
}

processCase(caseNo, action, params)
    .then(result => {
        console.log('\n✅ DONE');
        process.exit(0);
    })
    .catch(error => {
        console.error('\n❌ FAILED:', error.message);
        process.exit(1);
    });

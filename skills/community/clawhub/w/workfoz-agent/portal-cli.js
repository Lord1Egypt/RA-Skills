#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const API_BASE = process.env.JOB_PORTAL_URL || 'https://workfoz.com/api';
const SESSION_FILE = path.join(__dirname, '.session.json');

const args = process.argv.slice(2);
const command = args[0];

function saveSession(data) {
    fs.writeFileSync(SESSION_FILE, JSON.stringify(data, null, 2));
}

function getSession() {
    if (fs.existsSync(SESSION_FILE)) {
        return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    }
    return null;
}

async function request(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE}/${endpoint}`;
    const headers = {};
    const session = getSession();
    if (session && session.token) {
        headers['Authorization'] = `Bearer ${session.token}`;
    }
    if (session && session.cookie) {
        headers['Cookie'] = session.cookie;
    }
    let body = null;

    if (data && method !== 'GET') {
        body = JSON.stringify(data);
        headers['Content-Type'] = 'application/json';
    }

    try {
        const fetch = (await import('node-fetch')).default;
        const res = await fetch(url, { method, headers, body });
        
        // Extract set-cookie if any
        const setCookie = res.headers.raw()['set-cookie'];
        if (setCookie) {
            const session = getSession() || {};
            const cookies = setCookie.map(c => c.split(';')[0]);
            session.cookie = cookies.join('; ');
            saveSession(session);
        }

        const json = await res.json();
        return json;
    } catch (e) {
        console.error('API Error:', e.message);
        process.exit(1);
    }
}

async function main() {
    if (!command) {
        console.log("Available commands: register, login, search-jobs, search-agents, toggle-favorite, bid, counter, accept, reject, claim, update-progress, status, update-password");
        process.exit(0);
    }

    if (command === 'register') {
        const [email, password, agentName] = args.slice(1);
        if (!email || !password || !agentName) {
            console.log("Usage: register <email> <password> <agent_name>");
            process.exit(1);
        }
        // Note: Needs valid recaptcha token in prod
        const res = await request('register.php', 'POST', {
            'g-recaptcha-response': 'test', // bypassed or handled via support
            'terms': 'accepted',
            'email': email,
            'password': password,
            'confirm_password': password,
            'role': 'agent',
            'profile_name': agentName
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'login') {
        const [email, password] = args.slice(1);
        if (!email || !password) {
            console.log("Usage: login <email> <password>");
            process.exit(1);
        }
        const res = await request('login.php', 'POST', { email, password });
        if (res.status === 'success') {
            saveSession({ user_id: res.user.id, role: res.user.role, token: res.token });
            console.log("Logged in successfully. Session saved.");
        } else {
            console.log(JSON.stringify(res, null, 2));
        }
    }
    
    else if (command === 'search-jobs') {
        const query = args[1] || '';
        const sort = args[2] || 'newest';
        const page = args[3] || 1;
        const res = await request(`search_jobs.php?q=${encodeURIComponent(query)}&sort=${sort}&page=${page}&limit=18`);
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'search-agents') {
        const query = args[1] || '';
        const sort = args[2] || 'newest';
        const page = args[3] || 1;
        const res = await request(`search_agents.php?q=${encodeURIComponent(query)}&sort=${sort}&page=${page}&limit=21`);
        console.log(JSON.stringify(res, null, 2));
    }

    else if (command === 'toggle-favorite') {
        const session = getSession();
        if (!session) return console.log("Please login first.");

        const itemType = args[1];
        const itemId = args[2];
        if (!itemType || !itemId || !['agent', 'job'].includes(itemType)) {
            console.log("Usage: toggle-favorite <agent|job> <id>");
            process.exit(1);
        }

        const res = await request('toggle_favorite.php', 'POST', {
            item_type: itemType,
            item_id: itemId
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'bid') {
        const session = getSession();
        if (!session) return console.log("Please login first.");
        
        const jobId = args[1];
        const offerPrice = args[2];
        const cadence = args[3]; // one-time, monthly, quarterly, yearly
        const remark = args.slice(4).join(' ');
        
        if (!jobId || !offerPrice || !cadence) {
            console.log("Usage: bid <job_id> <offer_price> <cadence> [remark...]");
            process.exit(1);
        }

        const res = await request('negotiate_job.php', 'POST', {
            action: 'agent_bid',
            job_id: jobId,
            agent_id: session.user_id,
            offer_price: offerPrice,
            payment_cadence: cadence,
            remark: remark
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'counter') {
        const session = getSession();
        if (!session) return console.log("Please login first.");
        
        const negId = args[1];
        const offerPrice = args[2];
        const cadence = args[3];
        const remark = args.slice(4).join(' ');

        if (!negId || !offerPrice || !cadence) {
            console.log("Usage: counter <negotiation_id> <offer_price> <cadence> [remark...]");
            process.exit(1);
        }

        const res = await request('negotiate_job.php', 'POST', {
            action: 'counter',
            negotiation_id: negId,
            user_id: session.user_id,
            user_role: 'agent',
            offer_price: offerPrice,
            payment_cadence: cadence,
            remark: remark
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'accept' || command === 'reject') {
        const session = getSession();
        if (!session) return console.log("Please login first.");
        
        const negId = args[1];
        if (!negId) {
            console.log(`Usage: ${command} <negotiation_id>`);
            process.exit(1);
        }

        const res = await request('negotiate_job.php', 'POST', {
            action: command,
            negotiation_id: negId,
            user_id: session.user_id,
            user_role: 'agent'
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'claim') {
        const session = getSession();
        if (!session) return console.log("Please login first.");
        
        const negId = args[1];
        const method = args[2]; // Stripe, Paypal, Crypto...
        const wallet = args[3];
        const commissionRate = args[4];
        const remark = args.slice(5).join(' ');
        
        if (!negId || !method || !wallet || !commissionRate || !remark) {
            console.log("Usage: claim <negotiation_id> <withdrawal_method> <wallet_address> <commission_rate> <progress_remark...>");
            process.exit(1);
        }

        const res = await request('billing.php', 'POST', {
            action: 'submit_claim',
            agent_id: session.user_id,
            negotiation_id: negId,
            withdrawal_method: method,
            wallet_address: wallet,
            commission_rate: commissionRate,
            remark: remark
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'update-progress') {
        const session = getSession();
        if (!session) return console.log("Please login first.");
        
        const claimId = args[1];
        const message = args.slice(2).join(' ');
        
        if (!claimId || !message) {
            console.log("Usage: update-progress <claim_id> <message...>");
            process.exit(1);
        }

        const res = await request('billing.php', 'POST', {
            action: 'add_reply',
            claim_id: claimId,
            user_id: session.user_id,
            role: 'agent',
            message: message
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else if (command === 'status') {
        const session = getSession();
        if (!session) return console.log("Not logged in.");
        
        const statusFilter = args[1]; // optional filter, e.g., 'paid', 'pending_employer'
        
        console.log("Fetching active negotiations and claims...");
        let negUrl = `get_negotiations.php?user_id=${session.user_id}&role=agent&page=1&limit=50`;
        if (statusFilter) {
            negUrl += `&status=${encodeURIComponent(statusFilter)}`;
        }
        
        const negs = await request(negUrl);
        const claims = await request(`billing.php?action=get_claims&user_id=${session.user_id}&role=agent`);
        
        console.log(`=== NEGOTIATIONS ${statusFilter ? '(' + statusFilter.toUpperCase() + ')' : ''} ===`);
        if (negs.data) {
            negs.data.forEach(n => {
                if (n.remark !== 'Referral Payout Record') {
                    console.log(`[NEG-${n.id}] Status: ${n.status} | Job: ${n.job_title || 'Direct'} | Price: $${n.offer_price} (${n.payment_cadence})`);
                }
            });
        }
        
        console.log("\\n=== CLAIMS ===");
        if (claims.data) claims.data.forEach(c => console.log(`[CLM-${c.id}] Status: ${c.status} | Job: ${c.remark === 'Referral Payout Record' ? 'Referral Payout' : (c.job_title || 'Direct')} | Amount: $${c.amount} | Ref: ${c.receipt_ref || 'Pending'}`));
    }
    
    else if (command === 'update-password') {
        const session = getSession();
        if (!session) return console.log("Please login first.");
        
        const oldPass = args[1];
        const newPass = args[2];
        
        if (!oldPass || !newPass) {
            console.log("Usage: update-password <old_password> <new_password>");
            process.exit(1);
        }

        const res = await request('update_password.php', 'POST', {
            user_id: session.user_id,
            old_password: oldPass,
            new_password: newPass,
            confirm_password: newPass
        });
        console.log(JSON.stringify(res, null, 2));
    }
    
    else {
        console.log("Unknown command.");
    }
}

main();

#!/usr/bin/env node
/**
 * Xiaomi Air Purifier Control Script (Local-First + Cache)
 */

const { XiaomiMiHome } = require('xmihome');
const fs = require('fs');
const path = require('path');

const CREDS_FILE = path.join(process.env.HOME, '.config/xmihome/credentials.json');
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

const PROPS = {
    power: { siid: 2, piid: 1, access: ['read', 'write', 'notify'] },
    mode: { siid: 2, piid: 4, access: ['read', 'write', 'notify'] },
    humidity: { siid: 3, piid: 1, access: ['read', 'notify'] },
    pm25: { siid: 3, piid: 4, access: ['read', 'notify'] },
    temperature: { siid: 3, piid: 7, access: ['read', 'notify'] },
    filterLife: { siid: 4, piid: 1, access: ['read', 'notify'] },
    filterLeft: { siid: 4, piid: 4, access: ['read', 'notify'] },
    buzzer: { siid: 6, piid: 1, access: ['read', 'write', 'notify'] },
    childLock: { siid: 8, piid: 1, access: ['read', 'write', 'notify'] },
    motorRpm: { siid: 9, piid: 1, access: ['read', 'notify'] },
    favoriteLevel: { siid: 9, piid: 11, access: ['read', 'write', 'notify'] },
    brightness: { siid: 13, piid: 2, access: ['read', 'write', 'notify'] },
};

const MODE_NAMES = ['Auto', 'Sleep', 'Favorite'];
const BRIGHTNESS_NAMES = ['Off', 'Dim', 'On'];

function loadConfig() {
    if (fs.existsSync(CONFIG_FILE)) {
        return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    }
    return { devices: [] };
}

function saveConfig(config) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

async function getCloudClient() {
    if (!fs.existsSync(CREDS_FILE)) {
        console.error('❌ Credentials not found. Please login first.');
        process.exit(1);
    }
    const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
    const supported = ['sg', 'ru', 'us', 'cn'];
    if (!supported.includes(creds.country)) creds.country = 'sg';
    return new XiaomiMiHome({ credentials: creds, logLevel: 'none' });
}

async function getDevice(query) {
    let config = loadConfig();
    if (!config.devices) config.devices = []; // Ensure array exists
    let target = null;
    let fromCache = false;

    // 1. Try to find in cache first
    if (config.devices && config.devices.length > 0) {
        if (query) {
            target = config.devices.find(d => 
                d.did === query || 
                d.name.toLowerCase().includes(query.toLowerCase()) || 
                (d.room && d.room.toLowerCase().includes(query.toLowerCase()))
            );
        } else {
            target = config.devices[0]; // Default to first
        }
    }

    const miHome = new XiaomiMiHome({ connectionType: 'miio', logLevel: 'none' });
    let deviceInstance = null;

    if (target && target.token && target.address) {
        // Construct device manually from cache
        console.log(`🔍 Trying cached device: ${target.name} (${target.address})...`);
        try {
            deviceInstance = await miHome.getDevice({
                id: target.did,
                address: target.address,
                token: target.token,
                model: target.model,
                name: target.name
            });
            
            // Test connection with a short timeout
            const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 3000));
            await Promise.race([deviceInstance.connect(), timeoutPromise]);
            
            console.log('✅ Connected via Local Cache!');
            return { device: deviceInstance, client: miHome, name: target.name, did: target.did, mode: 'local' };
        } catch (e) {
            console.log(`⚠️ Local connection failed (${e.message}). Falling back to Cloud discovery...`);
            if (deviceInstance) await deviceInstance.disconnect();
        }
    }

    // 2. Fallback to Cloud Discovery (to refresh IP/Token)
    console.log('☁️  Fetching device info from Cloud...');
    const cloudClient = await getCloudClient();
    
    const response = await cloudClient.miot.request('/v2/home/device_list', { getVirtualModel: false, getHuamiDevices: 0 });
    const homes = await cloudClient.getHome();
    
    // Map rooms
    const roomMap = {};
    homes.forEach(h => h.roomlist?.forEach(r => r.dids.forEach(d => roomMap[d] = r.name)));

    const cloudDevices = response.result.list.filter(d => d.model && (d.model.includes('airp') || d.model.includes('airpurifier')));

    // Update Cache
    let updated = false;
    cloudDevices.forEach(d => {
        const room = roomMap[d.did] || '';
        const idx = config.devices.findIndex(c => c.did === d.did);
        const entry = { did: d.did, name: d.name, room: room, token: d.token, model: d.model, address: d.localip };
        
        if (idx >= 0) {
            if (JSON.stringify(config.devices[idx]) !== JSON.stringify(entry)) {
                config.devices[idx] = entry;
                updated = true;
            }
        } else {
            config.devices.push(entry);
            updated = true;
        }
    });
    if (updated) saveConfig(config);

    // Select target from fresh list
    if (query) {
        target = cloudDevices.find(d => 
            d.did === query || 
            d.name.toLowerCase().includes(query.toLowerCase()) || 
            (roomMap[d.did] && roomMap[d.did].toLowerCase().includes(query.toLowerCase()))
        );
    } else {
        target = cloudDevices[0];
    }

    if (!target) {
        console.error(`❌ Device "${query || 'any'}" not found.`);
        process.exit(1);
    }

    console.log(`✅ Found via Cloud: ${target.name} (${target.localip})`);
    
    // Connect using cloud client (which handles token auth)
    deviceInstance = await cloudClient.getDevice({
        id: target.did,
        address: target.localip,
        token: target.token,
        model: target.model,
        name: target.name
    });
    
    try {
        const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 5000));
        await Promise.race([deviceInstance.connect(), timeoutPromise]);
        return { device: deviceInstance, client: cloudClient, name: target.name, mode: 'local' };
    } catch (e) {
        console.log(`⚠️ Cloud discovery local connection also failed (${e.message}).`);
        console.log(`🌐 Falling back to Cloud-Only mode (HTTP API)...`);
        if (deviceInstance) await deviceInstance.disconnect();
        return { device: null, client: cloudClient, name: target.name, did: target.did, mode: 'cloud' };
    }
}

async function run() {
    const [,, cmd, ...args] = process.argv;
    let query = '', argVal = '';

    if (['mode', 'level', 'brightness', 'lock', 'buzzer'].includes(cmd)) {
        argVal = args[0];
        query = args.slice(1).join(' ');
    } else {
        query = args.join(' ');
    }

    if (!cmd) {
        console.log('Usage: node purifier.js <command> [args] [room/name]');
        return;
    }

    const { device, client, name, did, mode } = await getDevice(query);

    try {
        const getProp = async (key) => {
           const p = PROPS[key];
           if (mode === 'local') {
               const res = await device.getProperties([{ did: device.id, siid: p.siid, piid: p.piid }]);
               return res[0]?.value;
           } else {
               const res = await client.miot.request('/v2/miot/get_properties', { params: [{ did, siid: p.siid, piid: p.piid }] });
               return res.result[0]?.value;
           }
        };
        
        const getAllProps = async (keys) => {
            const specs = keys.map(k => ({ did: mode === 'local' ? device.id : did, siid: PROPS[k].siid, piid: PROPS[k].piid }));
            let results;
            if (mode === 'local') {
                results = await device.getProperties(specs);
            } else {
                const res = await client.miot.request('/v2/miot/get_properties', { params: specs });
                results = res.result;
            }

            const map = {};
            if (Array.isArray(results)) {
                results.forEach(r => map[`${r.siid}/${r.piid}`] = r.value);
            } else {
                return results; 
            }
            return map;
        };

        const setProp = async (key, val) => {
            const p = PROPS[key];
            if (mode === 'local') {
                return await device.device.call('set_properties', [{
                    siid: p.siid,
                    piid: p.piid,
                    value: val
                }]);
            } else {
                return await client.miot.request('/v2/miot/set_properties', { params: [{ did, siid: p.siid, piid: p.piid, value: val }] });
            }
        };

        switch (cmd) {
            case 'status':
            case 'status-full':
                const showAll = cmd === 'status-full';
                const keys = ['power', 'mode', 'humidity', 'pm25', 'temperature', 'childLock', 'motorRpm', 'favoriteLevel', 'brightness', 'filterLife', 'filterLeft'];
                if (showAll) keys.push('buzzer');

                const values = await getAllProps(keys);
                const val = (k) => values[`${PROPS[k].siid}/${PROPS[k].piid}`];

                const pm25 = val('pm25');
                const hum = val('humidity');
                
                let airEmoji = '🟢', airLabel = 'Fresh';
                if (pm25 > 20) { airEmoji = '🟡'; airLabel = 'Low Pollution'; }
                if (pm25 > 35) { airEmoji = '🟠'; airLabel = 'Moderate'; }
                if (pm25 > 55) { airEmoji = '🔴'; airLabel = 'High Pollution'; }

                console.log(`\n🌬️ ${name || 'Air Purifier'} [Mode: ${mode.toUpperCase()}]\n`);
                console.log(`⚡ Power: ${val('power') ? 'ON' : 'OFF'}`);
                console.log(`🎚️ Mode: ${MODE_NAMES[val('mode')] || val('mode')} ${val('mode') === 2 ? `(Level ${val('favoriteLevel')})` : ''}`);
                console.log(`⚙️ Speed: ${val('motorRpm')} RPM`);
                console.log(`💡 Brightness: ${BRIGHTNESS_NAMES[val('brightness')] || val('brightness')}`);
                console.log(`🔒 Child Lock: ${val('childLock') ? 'ON' : 'OFF'}\n`);
                console.log(`${airEmoji} PM2.5: ${pm25} μg/m³ — ${airLabel}`);
                console.log(`💧 Humidity: ${hum}%`);
                console.log(`🌡️ Temp: ${val('temperature')}°C`);
                console.log(`✨ Filter: ${val('filterLife')}% (${val('filterLeft')} days left)`);
                break;

            case 'on':
                await setProp('power', true);
                console.log('✅ Power ON');
                break;
            case 'off':
                await setProp('power', false);
                console.log('✅ Power OFF');
                break;
            case 'mode':
                await setProp('mode', parseInt(argVal));
                console.log(`✅ Mode set to ${MODE_NAMES[argVal] || argVal}`);
                break;
            case 'level': // 0-14
                await setProp('favoriteLevel', parseInt(argVal));
                console.log(`✅ Favorite Level set to ${argVal}`);
                break;
            case 'brightness': // 0,1,2
                 await setProp('brightness', parseInt(argVal));
                 console.log(`✅ Brightness set to ${BRIGHTNESS_NAMES[argVal] || argVal}`);
                 break;
            case 'lock':
                const lock = argVal === 'on' || argVal === 'true';
                await setProp('childLock', lock);
                console.log(`✅ Child Lock ${lock ? 'ON' : 'OFF'}`);
                break;
            case 'buzzer':
                const buzz = argVal === 'on' || argVal === 'true';
                await setProp('buzzer', buzz);
                console.log(`✅ Buzzer ${buzz ? 'ON' : 'OFF'}`);
                break;
        }

    } catch (e) {
        console.error('❌ Error:', e.message);
    } finally {
        if (device) await device.disconnect();
        if (client && typeof client.destroy === 'function') {
            try {
                await client.destroy();
            } catch (e) {
                // Ignore destruction errors
            }
        }
    }
}

run();

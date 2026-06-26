const { VariflightClient } = require('../lib/variflight-client');

module.exports = async function track(fnum, date) {
    if (!fnum) {
        console.error('Usage: track <fnum> [date]');
        console.error('Example: track CA1501');
        console.error('Example: track CA1501 2026-03-17');
        process.exit(1);
    }

    const client = new VariflightClient();
    const fnumUpper = fnum.toUpperCase();
    const queryDate = date || new Date().toISOString().slice(0, 10);

    try {
        console.log(`📡 追踪航班 ${fnumUpper} 的实时状态...\n`);

        const result = await client.searchFlightsByNumber(fnumUpper, queryDate);
        const raw = result && result.data ? result.data : result;
        const flights = Array.isArray(raw) ? raw : (raw ? [raw] : []);

        if (flights.length === 0) {
            console.log(`❌ 未找到航班 ${fnumUpper} 在 ${queryDate} 的信息`);
            return;
        }

        const f = flights[0];
        const fmt = s => (s || '待定').toString().substring(0, 16);

        // 判断飞行阶段
        const state = f.FlightState || '';
        let phase = '⏳ 计划中';
        if      (state.includes('到达'))                    phase = '🛬 已落地';
        else if (state.includes('飞行') || state.includes('空中')) phase = '✈️  飞行中';
        else if (state.includes('起飞'))                    phase = '✈️  已起飞';
        else if (state.includes('延误'))                    phase = '⚠️  延误';
        else if (state.includes('取消'))                    phase = '❌ 已取消';
        else if (state.includes('登机'))                    phase = '🚶 登机中';

        console.log(`╔══════════════════════════════════════╗`);
        console.log(`  航班追踪: ${fnumUpper}  ${f.FlightCompany || ''}`);
        console.log(`╚══════════════════════════════════════╝`);
        console.log('');
        console.log(`飞行状态:   ${state || '未知'}  ${phase}`);
        console.log('');

        console.log(`出发机场:   ${f.FlightDep || ''}  ${f.FlightDepAirport || f.FlightDepcode || '未知'}`);
        console.log(`  航站楼:   ${f.FlightHTerminal || '待定'}  登机口: ${f.BoardGate || '待定'}`);
        if (f.CheckinTable) console.log(`  值机柜台: ${f.CheckinTable}`);
        if (f.bridge)       console.log(`  廊桥:     ${f.bridge}`);
        console.log(`  计划起飞: ${fmt(f.FlightDeptimePlanDate)}`);
        console.log(`  预计起飞: ${fmt(f.FlightDeptimeReadyDate)}`);
        console.log(`  实际起飞: ${fmt(f.FlightDeptimeDate)}`);
        console.log('');

        console.log(`到达机场:   ${f.FlightArr || ''}  ${f.FlightArrAirport || f.FlightArrcode || '未知'}`);
        console.log(`  航站楼:   ${f.FlightTerminal || '待定'}  停机位: ${f.ArrStandGate || '待定'}`);
        if (f.BaggageID)  console.log(`  行李转盘: ${f.BaggageID}`);
        if (f.arr_bridge) console.log(`  廊桥:     ${f.arr_bridge}`);
        if (f.ReachExit)  console.log(`  到达出口: ${f.ReachExit}`);
        console.log(`  计划到达: ${fmt(f.FlightArrtimePlanDate)}`);
        console.log(`  预计到达: ${fmt(f.FlightArrtimeReadyDate)}`);
        console.log(`  实际到达: ${fmt(f.FlightArrtimeDate)}`);
        console.log('');

        if (f.generic || f.ftype) console.log(`执飞机型:   ${f.generic || ''}${f.ftype ? ' (' + f.ftype + ')' : ''}`);
        if (f.AircraftNumber)     console.log(`注册号:     ${f.AircraftNumber}`);
        if (f.OntimeRate)         console.log(`起飞准点率: ${f.OntimeRate}`);
        if (f.ArrOntimeRate)      console.log(`到达准点率: ${f.ArrOntimeRate}`);
        if (f.DelayReason)        console.log(`延误原因:   ${f.DelayReason}`);

        // 飞常准实时位置（需要注册号）
        const anum = f.AircraftNumber;
        if (anum && (state.includes('飞行') || state.includes('起飞') || state.includes('空中'))) {
            console.log('');
            console.log(`📍 正在获取实时位置 (注册号: ${anum})...`);
            try {
                const locResult = await client.getRealtimeLocationByAnum(anum);
                const loc = locResult && locResult.data ? locResult.data : locResult;
                if (loc && (loc.lat || loc.latitude || loc.Latitude)) {
                    const lat = loc.lat || loc.latitude || loc.Latitude;
                    const lon = loc.lon || loc.lng || loc.longitude || loc.Longitude;
                    const alt = loc.altitude || loc.alt || loc.Altitude;
                    const spd = loc.speed || loc.groundSpeed || loc.Speed;
                    const hdg = loc.heading || loc.track || loc.Heading;
                    console.log(`  纬度: ${lat}  经度: ${lon}`);
                    if (alt) console.log(`  高度: ${alt} 米`);
                    if (spd) console.log(`  速度: ${spd} km/h`);
                    if (hdg) console.log(`  航向: ${hdg}°`);
                } else {
                    console.log('  暂无实时位置数据');
                }
            } catch (_) {
                console.log('  实时位置暂不可用');
            }
        }

    } catch (error) {
        console.error(`❌ 追踪失败: ${error.message}`);
        process.exit(1);
    } finally {
        await client.disconnect();
    }
};

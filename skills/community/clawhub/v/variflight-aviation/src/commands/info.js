const { VariflightClient } = require('../lib/variflight-client');

module.exports = async function info(fnum, date) {
    if (!fnum) {
        console.error('Usage: info <fnum> [date]');
        console.error('Example: info CA1501');
        console.error('Example: info CA1501 2026-03-17');
        process.exit(1);
    }

    const client = new VariflightClient();
    const fnumUpper = fnum.toUpperCase();

    try {
        console.log(`🛫 查询航班 ${fnumUpper} 的实时信息...\n`);

        const queryDate = date || new Date().toISOString().slice(0, 10);
        const result = await client.searchFlightsByNumber(fnumUpper, queryDate);

        // 飞常准返回 { code, data: [...] }
        const raw = result && result.data ? result.data : result;
        const flights = Array.isArray(raw) ? raw : (raw ? [raw] : []);

        if (flights.length === 0) {
            console.log(`❌ 未找到航班 ${fnumUpper} 在 ${queryDate} 的信息`);
            return;
        }

        const f = flights[0];
        const fmt = s => (s || '待定').toString().substring(0, 16);

        console.log(`航班号:     ${f.FlightNo || fnumUpper}`);
        if (f.ShareFlightNo) console.log(`代码共享:   ${f.ShareFlightNo}`);
        console.log(`航空公司:   ${f.FlightCompany || '未知'}`);
        console.log(`飞行状态:   ${f.FlightState || '未知'}`);
        console.log(`执飞日期:   ${queryDate}`);
        console.log('');

        console.log('出发信息:');
        console.log(`  城市/机场: ${f.FlightDep || ''}  ${f.FlightDepAirport || f.FlightDepcode || '未知'}`);
        console.log(`  航站楼:   ${f.FlightHTerminal || '待定'}  登机口: ${f.BoardGate || '待定'}`);
        if (f.CheckinTable) console.log(`  值机柜台: ${f.CheckinTable}`);
        if (f.CheckDoor)    console.log(`  安检口:   ${f.CheckDoor}`);
        console.log(`  计划起飞: ${fmt(f.FlightDeptimePlanDate)}`);
        console.log(`  预计起飞: ${fmt(f.FlightDeptimeReadyDate)}`);
        console.log(`  实际起飞: ${fmt(f.FlightDeptimeDate)}`);
        if (f.LastCheckinTime) console.log(`  截止值机: ${fmt(f.LastCheckinTime)}`);
        console.log('');

        console.log('到达信息:');
        console.log(`  城市/机场: ${f.FlightArr || ''}  ${f.FlightArrAirport || f.FlightArrcode || '未知'}`);
        console.log(`  航站楼:   ${f.FlightTerminal || '待定'}  停机位: ${f.ArrStandGate || '待定'}`);
        if (f.BaggageID) console.log(`  行李转盘: ${f.BaggageID}`);
        if (f.ReachExit)  console.log(`  到达出口: ${f.ReachExit}`);
        if (f.arr_bridge) console.log(`  廊桥:     ${f.arr_bridge}`);
        console.log(`  计划到达: ${fmt(f.FlightArrtimePlanDate)}`);
        console.log(`  预计到达: ${fmt(f.FlightArrtimeReadyDate)}`);
        console.log(`  实际到达: ${fmt(f.FlightArrtimeDate)}`);
        console.log('');

        if (f.generic || f.ftype) console.log(`机型:       ${f.generic || ''}${f.ftype ? ' (' + f.ftype + ')' : ''}`);
        if (f.AircraftNumber)     console.log(`注册号:     ${f.AircraftNumber}`);
        if (f.FlightDuration)     console.log(`飞行时长:   ${f.FlightDuration} 分钟`);
        if (f.distance)           console.log(`航程距离:   ${f.distance} km`);
        if (f.OntimeRate)         console.log(`起飞准点率: ${f.OntimeRate}`);
        if (f.ArrOntimeRate)      console.log(`到达准点率: ${f.ArrOntimeRate}`);

        const foodMap = { M: '提供餐食', S: '小食', N: '无餐食', G: '团餐' };
        if (f.Food) console.log(`餐食:       ${foodMap[f.Food] || f.Food}`);

        if (f.DelayReason) console.log(`延误原因:   ${f.DelayReason}`);

        // 预计出口时间
        if (f.FastestExitTime || f.SlowestExitTime) {
            console.log('');
            console.log('预计出口时间:');
            if (f.FastestExitTime) console.log(`  最快: ${fmt(f.FastestExitTime)} (${f.FastestExitDuration} 分钟)`);
            if (f.SlowestExitTime) console.log(`  最慢: ${fmt(f.SlowestExitTime)} (${f.SlowestExitDuration} 分钟)`);
        }

    } catch (error) {
        console.error(`❌ 查询失败: ${error.message}`);
        process.exit(1);
    } finally {
        await client.disconnect();
    }
};

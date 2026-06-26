const { VariflightClient } = require('../lib/variflight-client');

module.exports = async function comfort(fnum, date) {
    if (!fnum) {
        console.error('Usage: comfort <fnum> [date]');
        console.error('Example: comfort CA1501');
        console.error('Example: comfort CA1501 2026-03-17');
        process.exit(1);
    }

    const client = new VariflightClient();
    const fnumUpper = fnum.toUpperCase();
    const queryDate = date || new Date().toISOString().slice(0, 10);

    try {
        console.log(`✈️  评估航班 ${fnumUpper} 的乘机舒适度...\n`);

        const result = await client.flightHappinessIndex(fnumUpper, queryDate);
        const raw = result && result.data ? result.data : result;
        const flights = Array.isArray(raw) ? raw : (raw ? [raw] : []);

        if (flights.length === 0) {
            console.log(`❌ 未找到航班 ${fnumUpper} 在 ${queryDate} 的舒适度数据`);
            return;
        }

        const f = flights[0];

        console.log(`航班:       ${f.FlightNo || fnumUpper}`);
        console.log(`路线:       ${f.FlightDepcode || '?'} → ${f.FlightArrcode || '?'}`);
        console.log(`日期:       ${f.FlightDate || queryDate}`);
        if (f.FtypeDetail) console.log(`机型:       ${f.FtypeDetail}`);
        if (f.AircraftNumber) console.log(`注册号:     ${f.AircraftNumber}  机龄: ${f.FlightYear} 年`);
        console.log('');

        // 核心指标
        console.log('─── 准点 & 服务 ───');
        if (f.OntimeRate)    console.log(`起飞准点率: ${f.OntimeRate}`);
        if (f.ArrOntimeRate) console.log(`到达准点率: ${f.ArrOntimeRate}`);
        if (f.DepAvgDelaytime) {
            const d = parseInt(f.DepAvgDelaytime, 10);
            console.log(`平均延误:   ${d > 0 ? d + ' 分钟' : '提前 ' + Math.abs(d) + ' 分钟'}`);
        }
        if (f.CancelProb)    console.log(`取消概率:   ${f.CancelProb}`);
        if (f.AirService)    console.log(`航空公司:   ${f.AirService}`);
        if (f.DepService)    console.log(`出发机场:   ${f.DepService}`);
        if (f.ArrService)    console.log(`到达机场:   ${f.ArrService}`);
        console.log('');

        // 机上设施（取第一个舱位为代表）
        const cabins = f.CabinInfoList || f.cabinInfoList;
        if (cabins && cabins.length > 0) {
            console.log('─── 机上设施（经济舱参考）───');
            // 找经济舱（Cabin 以 Y/H/V/Q/B 等开头的，取最后一个非头等/商务）
            const eco = cabins.find(c => !['F', 'C', 'J'].includes(c.Cabin)) || cabins[cabins.length - 1];
            if (eco.SeatSpace)  console.log(`座位间距:   ${eco.SeatSpace}`);
            if (eco.SeatWidth)  console.log(`座位宽度:   ${eco.SeatWidth}`);
            if (eco.SeatTilt)   console.log(`座椅倾斜:   ${eco.SeatTilt}`);
            if (eco.Media)      console.log(`娱乐系统:   ${eco.Media}`);
            if (eco.Socket)     console.log(`充电插座:   ${eco.Socket}`);
            if (eco.WiFi)       console.log(`WiFi:       ${eco.WiFi}`);
            if (eco.Food)       console.log(`餐食:       ${eco.Food}`);
            if (eco.Luggage)    console.log(`行李额:     ${eco.Luggage}`);
            console.log('');
        }

        // 廊桥概率
        if (f.DepBridge || f.ArrBridge) {
            console.log('─── 廊桥概率 ───');
            if (f.DepBridge) console.log(`出发廊桥:   ${f.DepBridge}`);
            if (f.ArrBridge) console.log(`到达廊桥:   ${f.ArrBridge}`);
            console.log('');
        }

        // 机型描述
        if (f.aircraftDescribe) {
            console.log('─── 机型简介 ───');
            // 截取前 100 字
            const desc = f.aircraftDescribe.substring(0, 120);
            console.log(desc + (f.aircraftDescribe.length > 120 ? '...' : ''));
            console.log('');
        }

    } catch (error) {
        console.error(`❌ 查询失败: ${error.message}`);
        process.exit(1);
    } finally {
        await client.disconnect();
    }
};

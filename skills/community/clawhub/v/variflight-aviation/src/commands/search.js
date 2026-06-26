const { VariflightClient } = require('../lib/variflight-client');

module.exports = async function search(dep, arr, date) {
    if (!dep || !arr) {
        console.error('Usage: search <dep> <arr> [date]');
        console.error('Example: search PEK SHA 2026-03-17');
        console.error('Example: search PEK SHA   (今日)');
        process.exit(1);
    }

    if (dep.length !== 3 || arr.length !== 3) {
        console.error('Error: 机场/城市代码必须是3位 IATA 代码（如 PEK、BJS）');
        process.exit(1);
    }

    const client = new VariflightClient();
    const depUpper = dep.toUpperCase();
    const arrUpper = arr.toUpperCase();
    const queryDate = date || new Date().toISOString().slice(0, 10);

    try {
        console.log(`🔍 搜索 ${depUpper} → ${arrUpper}  ${queryDate} 的航班...\n`);

        const result = await client.searchFlightsByDepArr(depUpper, arrUpper, queryDate);

        const raw = result && result.data ? result.data : result;
        const flights = Array.isArray(raw) ? raw : (raw ? [raw] : []);

        if (flights.length === 0) {
            console.log('❌ 未找到航班');
            return;
        }

        console.log(`✈️  找到 ${flights.length} 个航班：\n`);

        const fmt = s => (s || '').toString().substring(0, 16);

        flights.forEach((f, i) => {
            const fno      = f.FlightNo || '(无编号)';
            const airline  = f.FlightCompany || '';
            const state    = f.FlightState ? `  [${f.FlightState}]` : '';
            const depTime  = fmt(f.FlightDeptimePlanDate) || '待定';
            const arrTime  = fmt(f.FlightArrtimePlanDate) || '待定';
            const depT     = f.FlightHTerminal ? ` ${f.FlightHTerminal}` : '';
            const arrT     = f.FlightTerminal  ? ` ${f.FlightTerminal}` : '';
            const gate     = f.BoardGate       ? ` 登机口:${f.BoardGate}` : '';
            const model    = f.generic || f.ftype ? `  机型: ${f.generic || f.ftype}` : '';
            const punc     = f.OntimeRate      ? `  准点率: ${f.OntimeRate}` : '';
            const depCity  = f.FlightDep ? `${f.FlightDep}/` : '';
            const arrCity  = f.FlightArr ? `${f.FlightArr}/` : '';

            // 实际/预计时间（若与计划不同则展示）
            const actDep   = f.FlightDeptimeDate && f.FlightDeptimeDate !== f.FlightDeptimePlanDate
                ? `  实际起飞: ${fmt(f.FlightDeptimeDate)}` : '';
            const estArr   = f.FlightArrtimeReadyDate && f.FlightArrtimeReadyDate !== f.FlightArrtimePlanDate
                ? `  预计到达: ${fmt(f.FlightArrtimeReadyDate)}` : '';

            console.log(`${i + 1}. ${fno}  ${airline}${state}`);
            console.log(`   🛫 ${depTime} ${depCity}${depUpper}${depT}${gate}${actDep}`);
            console.log(`   🛬 ${arrTime} ${arrCity}${arrUpper}${arrT}${estArr}${model}${punc}`);
            if (f.CheckinTable) console.log(`   值机柜台: ${f.CheckinTable}`);
            const foodMap = { M: '提供餐食', S: '小食', N: '无餐食', G: '团餐' };
            if (f.Food) console.log(`   餐食: ${foodMap[f.Food] || f.Food}`);
            console.log('');
        });

    } catch (error) {
        console.error(`❌ 查询失败: ${error.message}`);
        process.exit(1);
    } finally {
        await client.disconnect();
    }
};

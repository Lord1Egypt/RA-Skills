const { VariflightClient } = require('../lib/variflight-client');

module.exports = async function transfer(dep, arr, date) {
    if (!dep || !arr) {
        console.error('Usage: transfer <dep> <arr> [date]');
        console.error('Example: transfer BJS SZX 2026-03-17');
        console.error('Example: transfer BJS CTU   (今日)');
        console.error('提示: 使用城市三字码（如 BJS=北京, SHA=上海, SZX=深圳）');
        process.exit(1);
    }

    const client = new VariflightClient();
    const depUpper = dep.toUpperCase();
    const arrUpper = arr.toUpperCase();
    const queryDate = date || new Date().toISOString().slice(0, 10);

    try {
        console.log(`🔄 查询 ${depUpper} → ${arrUpper}  ${queryDate} 的航班方案...\n`);

        const result = await client.getFlightTransferInfo(depUpper, arrUpper, queryDate);
        const raw = result && result.data ? result.data : result;

        // 错误响应：{ error_code, error }
        if (raw && raw.error_code) {
            console.log(`❌ ${raw.error || '暂无数据'}`);
            console.log('  提示：请使用城市三字码，如 BJS（北京）、SHA（上海）、SZX（深圳）');
            return;
        }

        // 飞常准返回二维数组：每个元素是一个航段数组（直飞=1段，中转=2段）
        const routes = Array.isArray(raw) ? raw : (raw ? [raw] : []);

        if (routes.length === 0) {
            console.log(`❌ 未找到 ${depUpper} → ${arrUpper} 的航班方案`);
            return;
        }

        const fmt = s => s ? s.toString().substring(0, 16) : '待定';

        console.log(`找到 ${routes.length} 个方案（显示前5个）：\n`);

        routes.slice(0, 5).forEach((legs, idx) => {
            // legs 是一个数组，每个元素是一个航班
            const flightLegs = Array.isArray(legs) ? legs : [legs];
            const isDirect = flightLegs.length === 1;

            if (isDirect) {
                const f = flightLegs[0];
                const depCityZh = f.DepCityZh || f.DepCity || '';
                const arrCityZh = f.ArrCityZh || f.ArrCity || '';
                const terminal = f.DepTerminal ? ` ${f.DepTerminal}` : '';
                const arrTerminal = f.ArrTerminal ? ` ${f.ArrTerminal}` : '';
                const delay = f.AverageDelayTime > 0
                    ? `  平均延误${f.AverageDelayTime}分`
                    : f.AverageDelayTime < 0 ? `  历史提前${Math.abs(f.AverageDelayTime)}分` : '';

                console.log(`方案 ${idx + 1}（直飞）：${f.FlightNo}`);
                console.log(`  🛫 ${fmt(f.DepTime)} ${depCityZh}/${f.DepAirportCode || depUpper}${terminal}`);
                console.log(`  🛬 ${fmt(f.ArrTime)} ${arrCityZh}/${f.ArrAirportCode || arrUpper}${arrTerminal}${delay}`);
            } else {
                console.log(`方案 ${idx + 1}（${flightLegs.length}程中转）：`);
                flightLegs.forEach((f, li) => {
                    const depCityZh = f.DepCityZh || f.DepCity || '';
                    const arrCityZh = f.ArrCityZh || f.ArrCity || '';
                    const terminal = f.DepTerminal ? ` ${f.DepTerminal}` : '';
                    const arrTerminal = f.ArrTerminal ? ` ${f.ArrTerminal}` : '';
                    console.log(`  第${li + 1}程: ${f.FlightNo}`);
                    console.log(`    🛫 ${fmt(f.DepTime)} ${depCityZh}/${f.DepAirportCode}${terminal}`);
                    console.log(`    🛬 ${fmt(f.ArrTime)} ${arrCityZh}/${f.ArrAirportCode}${arrTerminal}`);
                });
            }
            console.log('');
        });

    } catch (error) {
        console.error(`❌ 查询失败: ${error.message}`);
        process.exit(1);
    } finally {
        await client.disconnect();
    }
};

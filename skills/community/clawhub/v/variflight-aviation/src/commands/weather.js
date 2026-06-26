const { VariflightClient } = require('../lib/variflight-client');

// 天气图标映射
const skyIconMap = {
    CLEAR_DAY: '☀️ 晴',
    CLEAR_NIGHT: '🌙 晴（夜）',
    PARTLY_CLOUDY_DAY: '⛅ 多云',
    PARTLY_CLOUDY_NIGHT: '⛅ 多云（夜）',
    CLOUDY: '☁️ 阴',
    RAIN: '🌧 雨',
    SNOW: '❄️ 雪',
    WIND: '💨 风',
    FOG: '🌫 雾',
    HAZE: '😶‍🌫️ 霾',
    SLEET: '🌨 雨夹雪',
    THUNDERSTORM: '⛈ 雷雨',
};

function skyDesc(code) {
    return skyIconMap[code] || code || '未知';
}

module.exports = async function weather(airport) {
    if (!airport) {
        console.error('Usage: weather <airport>');
        console.error('Example: weather PEK');
        process.exit(1);
    }

    if (airport.length !== 3) {
        console.error('Error: 机场代码必须是3位 IATA 代码（如 PEK、SHA、CAN）');
        process.exit(1);
    }

    const client = new VariflightClient();
    const airportUpper = airport.toUpperCase();

    try {
        console.log(`🌤️  查询机场 ${airportUpper} 未来天气...\n`);

        const result = await client.getFutureWeatherByAirport(airportUpper);
        const data = result && result.data ? result.data : result;

        if (!data) {
            console.log(`❌ 未找到机场 ${airportUpper} 的天气数据`);
            return;
        }

        const current = data.current || {};
        const future  = data.future  || {};
        const aptName = future.aptCname || future.aptEname || airportUpper;

        console.log(`机场: ${aptName} (${airportUpper})  ${future.cityCname || ''}`);
        if (future.description) console.log(`预报: ${future.description}`);
        console.log('');

        // 当前实况
        if (current.Type || current.Temperature) {
            console.log('─── 当前实况 ───');
            if (current.Type)         console.log(`  天气:    ${current.Type}`);
            if (current.Temperature)  console.log(`  气温:    ${current.Temperature}°C`);
            if (current.Visib)        console.log(`  能见度:  ${current.Visib} 米`);
            if (current.WindSpeed)    console.log(`  风速:    ${current.WindSpeed}  ${current.WindPower || ''}  ${current.WindDirection || ''}`);
            if (current['PM2.5'])     console.log(`  PM2.5:   ${current['PM2.5']}  ${current.Quality || ''}`);
            if (current.ReportTime)   console.log(`  更新时间: ${current.ReportTime}`);
            console.log('');
        }

        // 未来3天预报
        const days = (future.detail || []).slice(0, 3);
        days.forEach((day, i) => {
            const label = i === 0 ? '今天' : i === 1 ? '明天' : '后天';
            const desc  = skyDesc(day.d_skydesc);
            const tMax  = day.d_temperature ? Math.round(day.d_temperature.max) : '--';
            const tMin  = day.d_temperature ? Math.round(day.d_temperature.min) : '--';
            const tAvg  = day.d_temperature ? Math.round(day.d_temperature.avg) : '--';
            const wind  = day.d_wind        ? `${Math.round(day.d_wind.avg.speed)} m/s` : '';
            const hum   = day.d_humidity    ? Math.round(day.d_humidity.avg * 100) + '%' : '';
            const pm25  = day.d_pm25        ? Math.round(day.d_pm25.avg) : '';
            const aqi   = day.d_aqi         ? Math.round(day.d_aqi.avg) : '';
            const rain  = day.d_precipitation && day.d_precipitation.max > 0
                          ? `降水: ${day.d_precipitation.avg.toFixed(1)} mm` : '';
            const dress = day.d_dressing    ? `穿衣指数: ${day.d_dressing.desc}` : '';
            const cold  = day.d_coldrisk    ? `感冒风险: ${day.d_coldrisk.desc}` : '';

            console.log(`─── ${label} ${day.date} ───`);
            console.log(`  天气: ${desc}`);
            console.log(`  气温: ${tMin}°C ~ ${tMax}°C  (均 ${tAvg}°C)`);
            if (wind)  console.log(`  风速: ${wind}`);
            if (hum)   console.log(`  湿度: ${hum}`);
            if (pm25)  console.log(`  PM2.5: ${pm25}  AQI: ${aqi}`);
            if (rain)  console.log(`  ${rain}`);
            if (dress) console.log(`  ${dress}`);
            if (cold)  console.log(`  ${cold}`);
            if (day.d_sunrise) console.log(`  日出: ${day.d_sunrise}  日落: ${day.d_sunset}`);
            console.log('');
        });

    } catch (error) {
        console.error(`❌ 查询失败: ${error.message}`);
        process.exit(1);
    } finally {
        await client.disconnect();
    }
};

export function compareData(todayData, yesterdayData) {
    const result = [];
    Object.keys(todayData).forEach(key => {
        const todayVal = todayData[key];
        const yesterdayVal = yesterdayData[key];
        if (yesterdayVal === undefined)
            return;
        const diff = (todayVal - yesterdayVal) / yesterdayVal;
        if (Math.abs(diff) > 0.1) {
            result.push({
                field: key,
                today: todayVal,
                yesterday: yesterdayVal,
                change: diff
            });
        }
    });
    return result;
}
//# sourceMappingURL=compare.js.map
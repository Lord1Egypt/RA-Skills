export function parseData(dataList, column) {
    const row = dataList[dataList.length - 1];
    const keys = Object.keys(column);
    const result = {};
    keys.forEach((key, index) => {
        const value = row[index];
        result[key] = (typeof value === "object" && value !== null && "v" in value)
            ? value.v
            : value;
    });
    return result;
}
//# sourceMappingURL=parser.js.map
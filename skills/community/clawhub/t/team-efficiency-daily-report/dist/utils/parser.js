export function parseData(dataList, column) {
    const keys = Object.keys(column);
    return dataList.map(row => {
        const result = {};
        keys.forEach((key, index) => {
            const value = row[index];
            result[key] = (typeof value === "object" && value !== null && "v" in value)
                ? value.v
                : value;
        });
        return result;
    });
}
//# sourceMappingURL=parser.js.map
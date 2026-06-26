const HEADERS = ["Code", "Line", "Board", "Arrive", "From", "To", "Price", "Seats", "Type", "Status"];
export function printScheduleTable(items) {
    if (items.length === 0) {
        console.log("No schedules found.");
        return;
    }
    const rows = items.map((item) => [
        item.code ?? "-",
        item.lineTime,
        item.boardingTime,
        item.arrivalTime,
        item.fromStation,
        item.toStation,
        `¥${item.price}`,
        item.remain == null ? "-" : String(item.remain),
        item.direct === true ? "direct" : item.direct === false ? "non-direct" : "unknown",
        formatStatus(item.status),
    ]);
    const widths = HEADERS.map((header, index) => Math.max(displayWidth(header), ...rows.map((row) => displayWidth(row[index] ?? ""))));
    printRow(HEADERS, widths);
    console.log(widths.map((width) => "-".repeat(width)).join("  "));
    rows.forEach((row) => printRow(row, widths));
}
function printRow(row, widths) {
    console.log(row.map((cell, index) => padEndDisplay(cell, widths[index])).join("  "));
}
function formatStatus(status) {
    if (status === "available")
        return "available";
    if (status === "sold-out")
        return "sold out";
    return "expired";
}
function padEndDisplay(value, width) {
    return value + " ".repeat(Math.max(0, width - displayWidth(value)));
}
function displayWidth(value) {
    let width = 0;
    for (const char of value) {
        width += isWide(char) ? 2 : 1;
    }
    return width;
}
function isWide(char) {
    const code = char.codePointAt(0) ?? 0;
    return (code >= 0x1100 &&
        (code <= 0x115f ||
            code === 0x2329 ||
            code === 0x232a ||
            (code >= 0x2e80 && code <= 0xa4cf) ||
            (code >= 0xac00 && code <= 0xd7a3) ||
            (code >= 0xf900 && code <= 0xfaff) ||
            (code >= 0xfe10 && code <= 0xfe19) ||
            (code >= 0xfe30 && code <= 0xfe6f) ||
            (code >= 0xff00 && code <= 0xff60) ||
            (code >= 0xffe0 && code <= 0xffe6)));
}

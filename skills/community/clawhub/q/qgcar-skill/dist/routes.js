export const CAMPUS_LABELS = {
    zhuhai: "Zhuhai",
    south: "South Campus",
    east: "East Campus",
};
export const ZHUHAI_STATIONS = {
    zhuhai: {
        city: "香洲",
        cityId: "3766",
        stationName: "珠海中大岐关服务点",
    },
    boya: {
        city: "香洲",
        cityId: "3766",
        stationName: "博雅苑",
    },
    fifth: {
        city: "香洲",
        cityId: "3766",
        stationName: "中大五院正门",
    },
};
export const GUANGZHOU_CAMPUSES = {
    south: {
        city: "广州市区",
        cityId: "142291",
        stationName: "广中大南校区 岐关服务部",
    },
    east: {
        city: "广州市区",
        cityId: "142291",
        stationName: "广中大东校区（大学城）岐关服务部",
    },
};
export function parseCampus(value, fallback) {
    if (!value)
        return fallback;
    if (value === "zhuhai" || value === "south" || value === "east")
        return value;
    throw new Error(`Invalid campus "${value}". Use zhuhai, south, or east.`);
}
export function parseZhuhaiStation(value, fallback) {
    if (!value)
        return fallback;
    if (value === "zhuhai" || value === "boya" || value === "fifth")
        return value;
    throw new Error(`Invalid Zhuhai station "${value}". Use zhuhai, boya, or fifth.`);
}
export function defaultDestination(start) {
    return start === "zhuhai" ? "south" : "zhuhai";
}
export function getStation(campus, zhuhaiStation) {
    if (campus === "zhuhai")
        return ZHUHAI_STATIONS[zhuhaiStation];
    return GUANGZHOU_CAMPUSES[campus];
}
export function routeLabel(start, to, zhuhaiStation) {
    const startLabel = start === "zhuhai" ? ZHUHAI_STATIONS[zhuhaiStation].stationName : CAMPUS_LABELS[start];
    const toLabel = to === "zhuhai" ? ZHUHAI_STATIONS[zhuhaiStation].stationName : CAMPUS_LABELS[to];
    return `${startLabel} -> ${toLabel}`;
}

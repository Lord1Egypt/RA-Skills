import { getStation } from "./routes.js";
const API_BASE = "https://ebk.17u.cn/cxyopenapi";
const HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    origin: "https://trans.17u.cn",
    referer: "https://trans.17u.cn/wx?v=1",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0",
};
export async function fetchLineList(params) {
    const start = getStation(params.start, params.zhuhaiStation);
    const to = getStation(params.to, params.zhuhaiStation);
    const body = {
        startCity: start.city,
        startCityId: start.cityId,
        startStationName: start.stationName,
        endCity: to.city,
        endCityId: to.cityId,
        endStationName: to.stationName,
        useCarTime: params.date,
        timeOrder: "",
        priceOrder: "",
        openId: "",
        orderNo: "",
        lineNo: "",
        groupingNo: "",
        hasActivityDiscount: false,
        vcode: "zhgy",
    };
    const response = await fetch(`${API_BASE}/estimate/intercity/linelist`, {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify(body),
    });
    if (!response.ok) {
        throw new Error(`Line list request failed: HTTP ${response.status}`);
    }
    const json = (await response.json());
    if (json.code !== "200" || !json.data) {
        throw new Error(json.msg || `Line list request failed with code ${json.code}`);
    }
    return json.data;
}

const ORDER_URL = "https://trans.17u.cn/wx?v=1#/BusOrderWrite";
export function buildOrderWriteLink(raw) {
    const endStation = raw.endStations[0];
    if (!endStation) {
        throw new Error("Cannot build link: schedule has no end station.");
    }
    const params = {
        form: "index",
        id: raw.lineId,
        endCity: endStation.cityName,
        startCity: raw.startStation.cityName,
        stationId: raw.startStation.stationId,
        endStationId: endStation.stationId,
        endCityId: raw.endCityId,
        startCityId: raw.startCityId,
        priceMark: raw.estimatePriceMark,
        supplierCode: raw.vcode,
        useCarTime: `${raw.startDay} ${raw.startStation.departureTime || raw.startTime}`,
        productId: raw.productId,
        isSelf: raw.isSelf ?? "",
        tcSupplierType: raw.tcSupplierType,
        shiftScheduleId: raw.shiftScheduleId || "",
        ticketType: "go-ticket",
        activityId: raw.activityId ?? "",
        vcode: "zhgy",
        env: "",
        userOpenId: "",
        appid: "",
        lineNo: raw.lineNo,
        tcStationId: raw.endStations.length === 1 ? endStation.tcStationId : "",
        isMlEStations: raw.endStations.length > 1,
        reductionActivityId: raw.reductionActivityId ?? 0,
        hasActivityDiscount: raw.hasActivityDiscount ?? "",
    };
    const query = Object.entries(params)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
        .join("&");
    return `${ORDER_URL}?${query}`;
}

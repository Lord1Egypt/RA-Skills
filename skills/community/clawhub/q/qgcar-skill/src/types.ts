import type { Campus, ZhuhaiStationKey } from "./routes.js";

export interface LineListRequest {
  startCity: string;
  startCityId: string;
  startStationName: string;
  endCity: string;
  endCityId: string;
  endStationName: string;
  useCarTime: string;
  timeOrder: string;
  priceOrder: string;
  openId: string;
  orderNo: string;
  lineNo: string;
  groupingNo: string;
  hasActivityDiscount: boolean;
  vcode: string;
}

export interface ApiResponse<T> {
  code: string;
  msg?: string;
  data?: T;
}

export interface ApiStation {
  stationId: number;
  tcStationId: number;
  departureTime: string;
  lastDepartureTime?: string;
  station: string;
  cityName: string;
  cityId: number;
  stationLatitude: number;
  stationLongitude: number;
  addressPicture?: string;
  addressType?: number;
  pictureurl?: string;
  locationAddress?: string;
  stationHour?: number;
  disable?: boolean;
}

export interface ApiLineTag {
  value: string | null;
  desc: string | null;
}

export interface ApiRevenueStrategy {
  revenueId: number;
  revenueName: string;
  revenueAmount: number;
  sellingPoint?: string;
}

export interface ApiSchedule {
  estimatePriceMark: string;
  lineTags?: string | null;
  lineTagsList?: ApiLineTag[] | null;
  shiftScheduleId: number;
  lineNo: string;
  lineId: number;
  lineName: string;
  shiftId: number;
  shiftScheduleNo: string;
  productId: number;
  productName: string;
  price: string;
  oldPrice: number;
  vcode: string;
  stockAmount: number | null;
  shiftType: number;
  tcSupplierType: string;
  costPrice: number;
  expired: number;
  stopSaleTime: string;
  startDay: string;
  startTime: string;
  lastStartTime?: string;
  startCityId: string;
  endCityId: string;
  startStationId: number;
  endStationId: number;
  carSeat?: number | null;
  passSeatNumLimit?: number;
  disable?: boolean;
  realNameTicket?: number;
  soldOut?: boolean | null;
  isSelf?: string | number;
  activityId?: string | number | null;
  hasActivityDiscount?: boolean | null;
  reductionActivityId?: number | null;
  startStation: ApiStation;
  endStations: ApiStation[];
  revenueStrategyInfo?: ApiRevenueStrategy[];
  allDay?: boolean;
  mutiPrice?: boolean;
}

export interface LineListData {
  carLineList: ApiSchedule[];
  startStationList?: Array<Pick<ApiStation, "stationId" | "station" | "locationAddress">>;
  endStationList?: Array<Pick<ApiStation, "stationId" | "station" | "locationAddress">>;
}

export type ScheduleStatus = "available" | "expired" | "sold-out";

export interface NormalizedSchedule {
  code?: string;
  startCampus: Campus;
  toCampus: Campus;
  zhuhaiStation: ZhuhaiStationKey;
  lineTime: string;
  boardingTime: string;
  arrivalTime: string;
  fromStation: string;
  toStation: string;
  price: string;
  remain: number | null;
  direct: boolean | null;
  status: ScheduleStatus;
  raw: ApiSchedule;
}

export interface LinkCacheEntry {
  code: string;
  date: string;
  startCampus: Campus;
  toCampus: Campus;
  zhuhaiStation: ZhuhaiStationKey;
  lineTime: string;
  boardingTime: string;
  fromStation: string;
  toStation: string;
  shiftScheduleId: number;
}

export interface LinkCache {
  createdAt: string;
  entries: LinkCacheEntry[];
}

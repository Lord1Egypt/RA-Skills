// Shared instrument registry. Keep symbol resolution in one place so the engine,
// dashboard, lifecycle reconciler and watcher cover the same universe.
export const FIXED_SYMBOLS = Object.freeze({
  XAUUSD: "GC=F", XAGUSD: "SI=F",
  DJ30: "YM=F", US30: "YM=F",
  NAS100: "NQ=F", US100: "NQ=F",
  US500: "ES=F", SPX: "ES=F",
});

export const FUTURES_SYMBOLS = new Set(["GC=F", "SI=F", "YM=F", "NQ=F", "ES=F"]);

export function normalizeAsset(value) {
  const n = String(value || "").toUpperCase().trim();
  if (n.includes("GOLD")) return "XAUUSD";
  if (n.includes("SILVER")) return "XAGUSD";
  if (n.includes("DOW")) return "DJ30";
  if (n.includes("NASDAQ")) return "NAS100";
  if (n.includes("S&P") || n.includes("SP500")) return "US500";
  return n.replace(/[^A-Z0-9]/g, "");
}

export function symbolForAsset(value) {
  const asset = normalizeAsset(value);
  if (FIXED_SYMBOLS[asset]) return FIXED_SYMBOLS[asset];
  if (/^[A-Z]{6}$/.test(asset)) return `${asset}=X`;
  return null;
}

export function isFuturesAsset(value) {
  return FUTURES_SYMBOLS.has(symbolForAsset(value));
}

export function pipSize(value) {
  const asset = normalizeAsset(value);
  if (asset === "XAUUSD") return 0.1;
  if (asset === "XAGUSD") return 0.01;
  if (/^(DJ30|US30|NAS100|US100|US500|SPX)$/.test(asset)) return 1;
  if (asset.endsWith("JPY")) return 0.01;
  return 0.0001;
}

export function priceDecimals(value, price = 0) {
  const asset = normalizeAsset(value);
  if (asset === "XAUUSD" || asset === "DJ30" || asset === "US30") return 1;
  if (asset === "XAGUSD" || /^(NAS100|US100|US500|SPX)$/.test(asset)) return 2;
  if (asset.endsWith("JPY")) return 3;
  return price > 500 ? 1 : price > 5 ? 3 : 5;
}

export function roundForAsset(value, price) {
  return Number(Number(price).toFixed(priceDecimals(value, Number(price))));
}

export const DEFAULT_ASSETS = Object.freeze([
  "XAUUSD", "XAGUSD", "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD",
  "AUDUSD", "NZDUSD", "GBPJPY", "AUDJPY", "EURJPY", "DJ30", "NAS100", "US500",
]);

export const SUPPORTED_ASSETS = Object.freeze([
  "EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCHF", "USDCAD",
  "EURGBP", "EURJPY", "EURCHF", "EURCAD", "EURAUD", "EURNZD",
  "GBPJPY", "GBPCHF", "GBPCAD", "GBPAUD", "GBPNZD",
  "AUDJPY", "AUDCHF", "AUDCAD", "AUDNZD", "NZDJPY", "NZDCHF", "NZDCAD",
  "CADJPY", "CADCHF", "CHFJPY", "XAUUSD", "XAGUSD", "DJ30", "NAS100", "US500",
]);

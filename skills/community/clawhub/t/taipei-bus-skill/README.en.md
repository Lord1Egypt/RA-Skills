# 🚌 Taipei Bus Fixed-Point Vehicle OD Skill (with PTX Route Integration)

> Integrates Taipei City's real-time fixed-point vehicle OD API with PTX Bus Stop/Route APIs, providing GPS-enabled bus tracking, **sequence-based precise ETA**, map visualization, anomaly detection, and route information.

**Language: English** | Default: Traditional Chinese — see `README.zh-TW.md`

---

## 📡 Data Sources

### 1️⃣ Fixed-Point Vehicle OD API (bus positions)
| Item | Content |
|------|---------|
| API | `https://tcgbusfs.blob.core.windows.net/blobbus/TstBusEvent.json` |
| Update | Irregular (~real-time) |
| License | Open Government Data (free) |

### 2️⃣ PTX Bus Stop API (stop coordinates)
| Item | Content |
|------|---------|
| API | `https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei` |
| Local Cache | `data/stop-coords.json` (**28,741 stops**, offline) |

### 3️⃣ PTX Bus Route + StopOfRoute APIs 🆕
| Item | Content |
|------|---------|
| Route | `https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei` |
| StopOfRoute | `https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei` |
| Local Cache | `data/route-full-cache.json` (**415 routes**, 819 stop sequences) |

---

## 🚀 Quick Start

```bash
cd ~/.qclaw/skills/taipei-bus
node examples/example-all-functions.js   # real-time + coords
node examples/example-route-api.js       # route names + sequences + ETA 🆕
```

---

## 🔧 Core Functions

### Real-time Vehicle
```javascript
fetchAll()              // All real-time bus records
findByRoute(routeId)    // All buses on a specific route
findByBus(busId)        // Single bus by plate
findAtStation(stopId)   // Buses stopped at a station
detectAnomalies()       // Detect abnormal/off-duty buses
```

### PTX Coordinates
```javascript
fetchAllWithCoords()     // Buses + stop coordinates
getHotspots(topN)        // Most active bus stops
getStopCoords(stopId)    // Get coords by StopID
searchStops(keyword)     // Fuzzy stop name search
```

### PTX Route / Stop Sequence 🆕
```javascript
searchRouteByName(name)        // Route name → RouteID ("234", "Nanjing")
getRouteInfo(routeId)          // Full route info (departures, operators, schedules)
searchRoutes(keyword, limit?)  // Fuzzy search all matching routes
getRouteStopSequence(routeId, dir?) // All stops in route order
getRoutesByStop(stopId)         // All routes passing through a stop
```

### Precise ETA 🆕
```javascript
etaBySequence(routeId, targetStopId, direction?, avgSecPerStop?)
// → { minutes, remaining, total, stop, note }
// Estimates by remaining stops × avg seconds per stop (default 90s)
```

---

## ⚠️ Limitations

1. **TstBusEvent IDs ≠ PTX IDs**: Two independent ID systems; use route name or stop name search as bridge
2. **ETA accuracy**: Sequence-based ±1-2 stops; cache is static, rebuild quarterly recommended
3. **Route coverage**: PTX covers main Taipei routes; some interval/special routes may be missing

---

## 📄 License

- Vehicle data: Taipei City Government Transportation Bureau — Open Government Data License
- PTX Stop/Route data: Ministry of Transportation and Communications (MOTC) PTX Open Data Platform

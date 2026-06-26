# Traffic Query Sources

## Flights

### Preferred exactness
- Exact airport routes are better than city groups.
- Watch for route aliases:
  - Beijing city: BJS
  - Beijing Daxing: PKX
  - Beijing Capital: PEK
  - Shanghai city: SHA
  - Shanghai Pudong: PVG
  - Shenzhen Bao'an: SZX

### Common pitfalls
- OTA links may default to city-to-city search rather than exact airport search.
- Google/OTA pages may localize currency unexpectedly.
- Flight tracking sites can confirm schedule patterns but may not reflect current sellable fares.

### Good user prompts to satisfy
- 查明天北京大兴飞深圳所有航班
- 查下午 3 点后直飞深圳的航班
- 查最便宜的 3 个班次
- 查南航和深航的班次

## Trains

### Preferred exactness
- Confirm the exact station names, not just city names.
- For Beijing / Shanghai / Shenzhen / Guangzhou, station choice matters a lot.

### Common pitfalls
- Timetable pages may not show real remaining ticket inventory.
- Prices vary by seat class.
- Some pages separate ordinary rail and high-speed rail.

### Good user prompts to satisfy
- 查北京南到上海虹桥明天所有高铁
- 查最早能到的车次
- 查二等座有票的班次
- 查晚上出发的卧铺车

## Extraction checklist

Before replying, verify:
- route is exact enough
- date is correct
- one-way vs round-trip is correct
- all visible rows were captured
- duplicate shared-code rows are identified when useful
- prices are labeled with source context when needed

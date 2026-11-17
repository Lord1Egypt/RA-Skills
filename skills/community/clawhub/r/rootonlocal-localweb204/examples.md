# 자연어 → API 호출 변환 예시

`SKILL.md` + `api-spec.md` + `localweb-spec.md` + `device-types.md` 를 합한
종합 워크플로우 예시.

OpenClaw 가 다음 단계를 거친다고 가정한다.

1. `/iot/info` + `/iot/group` + `/iot/device_dash` + `/iot/device_group` **4개를 모두 조회** (아래 공통 규칙)
2. 명령 분류 (`구역 + 카테고리 + 동작` 추출)
3. 구역명(`groupname`) → `group_id` → 장치 순으로 후보 좁히기
4. LocalWeb 직접 호출

---

## ⛔ 공통 규칙 — 반드시 지킬 것

### 1. 정보 API 는 항상 4개를 모두 조회한다

명령을 해석하기 **전에** 아래 4개를 전부 가져온다. 장치 목록만 가져오면
구역명("거실", "안방")으로 장치를 식별할 수 없다.

```
GET http://127.0.0.1:18080/iot/info           → user / password / scheme / port
GET http://127.0.0.1:18080/iot/group          → 구역 목록 (group_id ↔ groupname 매핑)
GET http://127.0.0.1:18080/iot/device_dash    → 대시보드 장치 목록
GET http://127.0.0.1:18080/iot/device_group   → 구역별 장치 목록 (group_id 포함)
```

- `/iot/device_group` 의 각 행에는 `group_id` 만 있고 구역 **이름은 없다** —
  `/iot/group` 의 `group_id → groupname` 매핑과 조인해야 "거실" 매칭이 가능하다.
- 구역에 안 넣고 대시보드에만 둔 장치도 있으므로 `device_dash` 도 함께 검색한다.

### 2. LocalWeb 요청 본문은 항상 5개 필드 전부 포함한다

**`id` / `user` / `password` / `method` / `params` 중 하나라도 빠지면 Station 이
오류를 반환한다.** 아래 예시들에서 본문을 일부 생략한 표기는 없다 — 모든 호출은
반드시 이 완전한 형태여야 한다.

```json
POST {scheme}://{station_ip}:{port}/mgaweb/api.EpSet
Content-Type: application/json

{
  "id": 957,
  "user": "<info.user>",
  "password": "<info.password>",
  "method": "EpSet",
  "params": { "me": "0001ABCDEF", "idx": "P1", "type": 129, "val": 1 }
}
```

- `id`: 호출자가 만드는 임의 일련번호 (1, 957, ... 아무 정수).
- `user`/`password`: `GET /iot/info` 응답 값을 **그대로** 넣는다.

### 3. 성공 판정은 `code === 0` 하나뿐이다

정상 응답은 **반드시 `code` 필드가 있고 값이 0** 이다:

```json
{ "id": 957, "code": 0, "message": ... }
```

아래는 전부 **실패**로 처리한다. 성공으로 응답하지 말 것:

| 응답 | 원인 |
|---|---|
| `code !== 0` | API 오류 (자격증명 불일치, 잘못된 params 등) |
| **`code` 필드 자체가 없음** — 예: `{ "message": "ENPF1:...", "status": "ENL" }` | 요청 본문 불완전 (`user`/`password` 누락 등) 또는 잘못된 endpoint/형식 |
| HTTP 4xx/5xx, 네트워크 오류 | URL/포트/프로토콜 오류, Station 오프라인 |

`ENPF...`/`status:"ENL"` 응답을 받았다면 본문 5개 필드가 전부 있는지부터 다시 확인한다.

---

## 예시 1 — "거실 불 켜줘"

```
명령 → { 구역: "거실", 카테고리: light|switch, 동작: ON }
```

1. `GET /iot/info` → 자격증명 확보
   ```json
   { "enabled":true, "scheme":"https", "port":8080, "user":"admin", "password":"<실제 비밀번호>" }
   ```
2. `GET /iot/group` → 구역명 → group_id 매핑
   ```json
   [
     { "group_id": 2, "groupname": "거실", "node": 3, "root_id": 1 }
   ]
   ```
   "거실" → `group_id=2`.
3. `GET /iot/device_group` (+ `GET /iot/device_dash` 도 함께 검색)
   - `group_id=2` 인 행 추출
   - `category in ["light","switch"]` 필터
   - 이름에 "메인등"/"천장등" 우선 매칭
   ```json
   { "device_id": 12, "station_id": 1, "group_id": 2,
     "station_ip": "192.168.0.10",
     "agt": "_AGT",
     "me": "0001ABCDEF", "dev_type": "SL_SW_BJ84",
     "category": "switch", "name": "거실 메인등" }
   ```
   `station_ip` 가 행에 포함되어 있으므로 `/iot/station` 별도 조회는 불필요.
4. LocalWeb 호출 — **본문 5개 필드 전부 포함**
   ```http
   POST https://192.168.0.10:8080/mgaweb/api.EpSet
   Content-Type: application/json

   { "id": 957,
     "user": "admin",
     "password": "<info.password>",
     "method": "EpSet",
     "params": { "me": "0001ABCDEF", "idx": "P1", "type": 129, "val": 1 } }
   ```
5. 응답 `{ "id":957, "code":0, "message":"ok" }` → `code===0` 확인 후 성공 보고.

---

## 예시 2 — "거실이 너무 덥다"

```
명령 → { 구역: "거실", 카테고리: ac, 동작: turn_on_or_lower_temp }
```

1. `/iot/group` 에서 "거실" → `group_id=2` 확인 후,
   `/iot/device_group` 에서 `group_id=2 AND category="ac"` 추출
   ```json
   { "device_id": 30, "station_id": 1, "station_ip": "192.168.0.10", "agt": "_AGT",
     "me": "AC0001", "dev_type": "V_AIR_P", "name": "거실 에어컨",
     "last_stat": "{\"O\":{\"type\":128,\"val\":0},\"tT\":{\"type\":136,\"val\":260,\"v\":26}}" }
   ```
2. `last_stat.O.val === 0` → 꺼져 있음. 우선 켠다. (AC 전원 idx 는 `O`)
   ```json
   POST https://192.168.0.10:8080/mgaweb/api.EpSet

   { "id": 958, "user": "<info.user>", "password": "<info.password>",
     "method": "EpSet",
     "params": { "me": "AC0001", "idx": "O", "type": 129, "val": 1 } }
   ```
3. (선택) 설정 온도 1도 낮추기 (26→25도) — `tT` 채널, val 은 온도×10:
   ```json
   { "id": 959, "user": "<info.user>", "password": "<info.password>",
     "method": "EpSet",
     "params": { "me": "AC0001", "idx": "tT", "type": 136, "val": 250 } }
   ```

> ⚠️ "닫아줘"가 들어오면 AC 에는 reject. (`device-types.md` §5)

---

## 예시 3 — "안방 블라인드 내려줘"

1. `/iot/group` 에서 "안방" 의 `group_id` 확인 →
   `/iot/device_group` 에서 해당 `group_id AND category="blind"`
   ```json
   { "me": "BL0001", "dev_type": "SL_DOOYA", "station_ip": "192.168.0.10" }
   ```
2. CLOSE (완전 닫기) = `idx=P2`, `type=207`, `val=0` (열림률 0%)
   ```json
   { "id": 960, "user": "<info.user>", "password": "<info.password>",
     "method": "EpSet",
     "params": { "me": "BL0001", "idx": "P2", "type": 207, "val": 0 } }
   ```

> 열기 = `val=100`, 부분 열기 X% = `val=X`, 정지 = `type=206, val=128`. (`device-types.md` §4)

---

## 예시 4 — 매칭 모호 (다중 후보)

"불 켜줘" — 구역 미지정.

→ `device_group` + `device_dash` 모두에서 `category in [light,switch]` 추출하면
   3개 이상 후보가 나옴.

```json
{
  "ok": false,
  "error": "ambiguous_device",
  "candidates": [
    { "me": "0001ABCDEF", "name": "거실 메인등", "groupname": "거실" },
    { "me": "0002...",     "name": "안방 불",   "groupname": "안방" },
    { "me": "0003...",     "name": "주방 등",   "groupname": "주방" }
  ]
}
```

사용자에게 "어디 불을 켤까요? 거실/안방/주방" 형태로 되묻기.

---

## 예시 5 — 거부

"에어컨 열어줘" / "에어컨 닫아줘" → AC 카테고리에 open/close 는 정의되지 않음.

```json
{
  "ok": false,
  "error": "invalid_action",
  "message": "에어컨에는 열기/닫기 동작이 없습니다. 전원/온도/모드/풍량 중 선택하세요."
}
```

---

## 예시 6 — 스마트플러그(`SL_OE_DE`) ON/OFF

> **켜줘**와 **꺼줘** 모두 `idx=P1` 이지만 `type`/`val` 조합이 다름

**ON (`켜줘`)**
```json
{ "id": 961, "user": "<info.user>", "password": "<info.password>",
  "method": "EpSet",
  "params": { "me": "<me>", "idx": "P1", "type": 129, "val": 1 } }
```

**OFF (`꺼줘`)**
```json
{ "id": 962, "user": "<info.user>", "password": "<info.password>",
  "method": "EpSet",
  "params": { "me": "<me>", "idx": "P1", "type": 128, "val": 0 } }
```

| 동작 | type | val |
|---|---|---|
| ON | `129` (0x81) | `1` |
| OFF | `128` (0x80) | `0` |

> ⚠️ OFF 시 `val:1` 을 쓰면 동작하지 않는다. 반드시 `type=128, val=0` 조합을 쓰도록.

---

## 예시 7 — 상태 조회

"안방 온도 알려줘"

1. `/iot/device_group` 에서 `groupname="안방" AND category in [sensor,ac]`
2. 우선 환경센서(`SL_SC_BE`) 또는 공기질센서(`ZG#PMT300-*`, 채널 `T1`) 가 있으면 그것 사용. 없으면 AC 의 `last_stat`.
3. 신선한 값이 필요하면 LocalWeb `api.EpGet` 호출:
   ```json
   { "id": 963, "user": "<info.user>", "password": "<info.password>",
     "method": "EpGet",
     "params": { "me": "<sensor me>" } }
   ```
4. 응답 `code === 0` 확인 후 `message.data` 에서 섭씨 읽기:
   `data.T.v` 가 있으면 **그대로** 사용 (이미 표시값).
   `v` 가 없으면 `data.T.val / 10` 을 사용 (val 은 raw 온도×10).

---

## 예시 8 — "거실 공기질 어때?" (공기질센서 조회)

1. `/iot/device_group` 에서 `groupname="거실" AND dev_type in ["ZG#PMT300-SGMR-ZTN","ZG#PMT300-S-ZTN","V_HTTP_P"]`
2. `last_stat` 파싱 또는 `EpGet` 호출.
3. 채널 판독 (`device-types.md` §8.2) — 공기질센서Pro 예:
   ```json
   // EpGet 응답 data
   {
     "T1":  { "type": 0, "val": 245 },       // 24.5 °C  (val/10)
     "H1":  { "type": 0, "val": 431 },       // 43.1 %   (val/10)
     "PM1": { "type": 0, "val": 12 },        // PM2.5 12 μg/m³
     "CO2PPM1": { "type": 0, "val": 620 }    // CO₂ 620 ppm
   }
   ```
4. "거실 24.5도, 습도 43%, 미세먼지(PM2.5) 12μg/m³, CO₂ 620ppm 입니다" 형태로 응답.

---

## 예시 9 — "주방 플러그 전기 얼마나 써?" (전력 조회)

1. `/iot/device_group` 에서 `groupname="주방" AND dev_type="SL_OE_DE"` (또는 전력량측정기 `ZG#PMM-300Z2` 등)
2. `EpGet` 호출 후 전력 채널 판독 — **val 은 IEEE754 float 정수 표현** (`device-types.md` §8.1):
   ```json
   // 스마트플러그: P2=누적 kWh, P3=현재 W / 전력량측정기: EE1=누적 kWh, EP1=현재 W
   { "P3": { "type": 0, "val": 1116798976 } }   // IEEE754(0x42910000) → 72.5 W
   ```
3. "주방 플러그는 지금 72.5W 사용 중입니다" 형태로 응답.

---

## 예시 10 — "거실 에어컨 켜줘" (물리 장치 없음 → IR 리모컨)

1. `/iot/device_group` 에서 `groupname="거실" AND category="ac"` → 0건.
2. `dev_type="UL_IR_CU"` 행 탐색 → `last_stat.name` 이 "거실에어컨" 인 리모컨 발견.
3. `last_stat` 에 버튼 캐시가 있으면 그대로 사용, 없으면 `GetRemote` 호출
   (endpoint 는 `api.GetRemote`, method 는 `GetACRemote`):
   ```json
   POST https://192.168.0.10:8080/mgaweb/api.GetRemote

   { "id": 964, "user": "<info.user>", "password": "<info.password>",
     "method": "GetACRemote",
     "params": { "ai": "AI_IR_a224_1780039368", "needKeys": 2 } }
   ```
4. `codes` 에서 이름이 "전원"/"켜기"인 버튼 탐색 → `CS_1`.
5. `SendKeys` 실행:
   ```json
   POST https://192.168.0.10:8080/mgaweb/api.SendKeys

   { "id": 965, "user": "<info.user>", "password": "<info.password>",
     "method": "SendKeys",
     "params": { "me": "a224", "category": "custom",
                 "ai": "AI_IR_a224_1780039368", "keys": "[\"CS_1\"]" } }
   ```
6. IR 은 단방향(토글)이므로 "거실 에어컨에 전원 버튼을 전송했습니다"로 응답.

---

## 예시 11 — "현관문 열려 있어?" (감지형 센서 조회)

1. `/iot/device_group` (+ `device_dash`) 에서 이름/구역에 "현관" 포함 + `dev_type in ["SL_DF_GG","SL_SC_BG"]` 탐색.
2. `last_stat` 파싱 또는 `EpGet` 호출 후 감지 판정 (`device-types.md` §6):
   ```json
   // SL_DF_GG: A.type = 1 문열림 / 0 문닫힘
   { "A": { "type": 1, "val": 0 } }

   // SL_SC_BG: G.val = 0 문열림 / 1 문닫힘  ← val=0 이 "열림"임에 주의
   { "G": { "type": 0, "val": 0 } }
   ```
3. "현관문이 열려 있습니다" / "닫혀 있습니다" 로 응답.

> 동작(`SL_DF_MM`/`SL_SC_BM` → `M.type`), 동작Pro(`SL_BP_MZ` → `P1.val`),
> 재실(`ZG#TS06012` → `M1.val`), 누수(`SL_SC_WA` → `WA.val > 0`),
> 화재(`ZG#MIR-SM100-E` → `A1.val > 0`) 도 같은 패턴으로 조회한다.
> devtype 별로 판정 필드가 `type`/`val` 로 다르므로 §6 표를 그대로 따를 것.

---

## 클라이언트 모듈 의사코드

```ts
async function executeCommand(utterance: string) {
  const info = await fetch('http://127.0.0.1:18080/iot/info').then(r => r.json());
  if (!info.enabled) return { ok:false, error:'localweb_disabled' };

  const [stations, groups, dash, gdev] = await Promise.all([
    fetch('http://127.0.0.1:18080/iot/station').then(r => r.json()),
    fetch('http://127.0.0.1:18080/iot/group').then(r => r.json()),
    fetch('http://127.0.0.1:18080/iot/device_dash').then(r => r.json()),
    fetch('http://127.0.0.1:18080/iot/device_group').then(r => r.json()),
  ]);

  const intent = classifyIntent(utterance);          // { area, category, action, value? }
  const candidates = findCandidates(intent, groups, gdev, dash);
  if (candidates.length === 0) return { ok:false, error:'not_found' };
  if (candidates.length >  1) return { ok:false, error:'ambiguous_device', candidates };

  const dev = candidates[0];
  const set = buildEpSetParams(dev, intent);          // device-types.md 표대로
  if (!set) return { ok:false, error:'invalid_action' };

  // station_ip 는 device 응답에 이미 포함 — /iot/station 별도 조회 불필요
  const stationIp = dev.station_ip;
  if (!stationIp) return { ok:false, error:'station_missing' };

  const url = info.url_template.replace('{station_ip}', stationIp)
                              .replace('{endpoint}', 'api.EpSet');
  const res = await fetch(url, {
    method:'POST',
    headers:{ 'Content-Type':'application/json' },
    body: JSON.stringify({
      id: 1, user: info.user, password: info.password,
      method: 'EpSet', params: set,
    }),
  }).then(r => r.json());

  // 성공 판정: code 필드가 존재하고 0 인 경우만.
  // { message:"ENPF...", status:"ENL" } 처럼 code 가 없는 응답은 실패다
  // (본문 필드 누락 / 잘못된 endpoint 등).
  const ok = typeof res.code === 'number' && res.code === 0;
  return { ok, action:'epSet', device:dev, request:set, result:res };
}
```

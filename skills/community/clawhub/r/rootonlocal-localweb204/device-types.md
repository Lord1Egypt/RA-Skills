# Device Types & Channel Map

`/iot/device_dash` / `/iot/device_group` 응답의 `dev_type` 별 제어 채널 매핑.

본 표는 본 앱의 `packages/core/utils/scheduleChannelOptions.ts` 와
`packages/core/utils/scheduleArgBuilder.ts` 기준이며, LocalWeb `api.EpSet`/`api.EpGet`
호출 시 어떤 `idx`/`type`/`val` 조합이 유효한지 정의한다.

---

## 1. 카테고리 (`category` 필드)

| value | 의미 | 제어 가능? |
|---|---|---|
| `switch` | 스위치 계열 (Air/Polar/Nature/Blend/CUBE 등) | YES |
| `light` | 조명 (디머 포함) | YES |
| `blind` | 블라인드/커튼 | YES (OPEN/CLOSE) |
| `ac` | 에어컨 / 전열교환기 | YES (전원/모드/온도/풍량) |
| `sensor` | 동작/문열림/공기질/온습도 등 | **NO** (조회만) |
| `etc` | 전력량측정기/IR/오디오/매트릭스 | 제한적, 조회만 권장 |
| `unknown` | 매핑 없음 | NO |

---

## 2. Switch 카테고리 — devtype 별 가능 idx

| devtype | idx (가능 채널) | 비고 |
|---|---|---|
| `SL_SW_BJ84` (Air스위치) | `P1`~`P8` | 8구까지 |
| `SL_NATURE`, `SL_NATURE_X` | `P1`~`P3` | |
| `SL_SW_BS1`, `SL_SW_ND1`, `SL_MC_ND1` | `P1` | Polar 1구 |
| `SL_SW_BS2`, `SL_SW_ND2`, `SL_MC_ND2` | `P1`~`P2` | Polar 2구 |
| `SL_SW_BS3`, `SL_SW_ND3`, `SL_MC_ND3` | `P1`~`P3` | Polar 3구 |
| `SL_SW_MJ1`/`MJ2`/`MJ3` (CUBE 1/2/3) | `P1`~`P(N)` | CUBE 모듈 |
| `SL_OE_DE` (스마트플러그) | `P1` | |
| `SL_SC_BB_V2` (CUBE 버튼) | — | **이벤트 전용. 제어 거부** |
| `SL_SW_IF2`, `SL_SW_IF3`, `SL_SW_RC` (Blend) | `L1`~`L3` | **L 채널** |
| `SL_SW_NS1`/`NS2`/`NS3` (Nature 120) | `L1`~`L3` | |
| `SL_P` (제네럴 컨트롤러) | `P2`~`P4` | controller attrs 기반 |
| `V_IND_S`, `V_SI` (가상 스위치) | `L1`~`L8` 또는 `P1`~`P8` | 가상 채널 |

**제어 코드 (모든 switch 공통)**

| 동작 | type | val |
|---|---|---|
| ON | `129` | `1` |
| OFF | `128` | `0` |

> ⛔ **금지 조합 — 절대 사용 금지**
> - `type=128, val=1` → 잘못된 조합. OFF 명령에 val=1 을 넣으면 안 된다.
> - `type=129, val=0` → 잘못된 조합. ON 명령에 val=0 을 넣으면 안 된다.
>
> **규칙**: `type=129` 이면 반드시 `val=1`, `type=128` 이면 반드시 `val=0`.
> type 과 val 은 항상 쌍으로 움직인다. 독립적으로 조합하지 않는다.

---

## 3. Light 카테고리

| devtype | idx | 색온도 |
|---|---|---|
| `SL_LI_WW`, `SL_SW_WW` | `P1` (밝기), `P2` (색온도) | YES (2700K~6000K) |
| `SL_SW_DM1_V1`, `SL_SW_DM1_V2` | `P1` (밝기) | NO |
| `V_HG_WW` | `L` | NO |

**제어 코드 (모든 조명 공통 — `type=128/129` 사용 금지)**

| 동작 | idx | type | val |
|---|---|---|---|
| ON | `P1` 또는 `L` | `207` | brightness (1-255, 켜진 밝기 그대로) |
| OFF | `P1` 또는 `L` | `206` | brightness (1-255, 켜진 밝기 그대로) |
| 밝기 변경 | `P1` 또는 `L` | `207` | brightness (1-255) |
| 색온도 변경 | `P2` | `207` | colortemp (1-255) |

> **규칙**: 조명은 `type=128/129` 를 사용하지 않는다. 전원 ON/OFF 모두 `207/206` 이며 전원 ON/off시에 val 은 현재 밝기값을 그대로 전달한다.
>
> ep GET 상태 판독: `type=207` → 켜짐, `type=206` → 꺼짐.

---

## 4. Blind 카테고리 (`SL_DOOYA`)

**제어 채널: P2 (EpSet)**

| 동작 | idx | type | val | 비고 |
|---|---|---|---|---|
| OPEN (완전 열기) | `P2` | `207` (0xCF) | `100` | |
| CLOSE (완전 닫기) | `P2` | `207` (0xCF) | `0` | |
| STOP (정지) | `P2` | `206` (0xCE) | `128` (0x80) | |
| 부분 열기 X% | `P2` | `207` (0xCF) | `X` (0~100) | 30% 열기 → val=30 |

> **규칙**:
> - 열기/닫기/위치 설정은 모두 `idx=P2, type=207(0xCF)`, val로 열림률(0~100)을 지정한다.
> - 정지는 `idx=P2, type=206(0xCE), val=128(0x80)` 고정이다.
> - `type=128/129` 는 블라인드에 **사용하지 않는다**.

**상태 채널: P1 (EpGet / NOTIFY, read-only)**

| P1.type | P1.val | 의미 |
|---|---|---|
| 홀수 | 0~100 | 이동 중 + 현재 열림률(%) |
| 홀수 | 128 | 열리는 중 (위치 정보 없음) |
| 홀수 | 127 | 닫히는 중 (위치 정보 없음) |
| 짝수 | 0~100 | 정지 + 현재 열림률(%) |

> `type % 2 === 1` → 이동 중, `type % 2 === 0` → 정지.
> val이 127/128이면 열림률을 알 수 없다.

**EpSet 예제**

```json
// 완전 열기
{ "idx": "P2", "type": 207, "val": 100 }

// 완전 닫기
{ "idx": "P2", "type": 207, "val": 0 }

// 정지
{ "idx": "P2", "type": 206, "val": 128 }

// 30% 위치로 이동
{ "idx": "P2", "type": 207, "val": 30 }
```

---

## 5. AC 카테고리

| devtype | 종류 |
|---|---|
| `V_AIR_P` | 에어컨 (제어판) |
| `V_FRESH_P` | 전열교환기 |

**채널/코드 표**

| 항목 | idx | type | val | 비고 |
|---|---|---|---|---|
| 전원 ON | `O` | `129` | `1` | |
| 전원 OFF | `O` | `128` | `0` | |
| 모드 V_AIR_P | `MODE` | `206` | 1=자동 / 2=송풍 / 3=냉방 / 4=난방 / 5=제습 | |
| 모드 V_FRESH_P | `MODE` | `206` | 1=자동 / 2=전열 / 9=취침/숙면 / 10=환기 | |
| 설정 온도 | `tT` | `136` | 온도×10 (정수 18~30도 → 180~300) | 단위 °C. 25.3도 설정이면 val=253 |
| 풍량 V_AIR_P | `F` | `206` | 15=약 / 45=중 / 75=강 / 101=자동 | |
| 풍량 V_FRESH_P | `F` | `206` | 15=약 / 45=중 / 75=강 | 자동(101) 없음 |

> ⛔ **AC 전원 금지 조합**
> - `type=128, val=1` → 사용 금지
> - `type=129, val=0` → 사용 금지
>
> 전원 ON = `{idx:"O", type:129, val:1}` / 전원 OFF = `{idx:"O", type:128, val:0}` 이 두 가지만 유효하다.

**상태 판독 (EpGet / last_stat)**

- `tT`/`T`(현재온도) 채널: `v` 가 있으면 그대로 °C, 없으면 `val / 10` = °C.

**유효성**

- 에어컨에 `close` 같은 블라인드 동작 → reject.
- 온도는 18~30도 외 → reject.
- category 가 `ac` 라도 `dev_type=UL_IR_AC` 는 미지원 장치 → 제어 reject.

---

## 6. Sensor 카테고리 (조회만)

> 아래 감지형 센서들은 아직 본 앱(RootONLocal)에 카드 UI 가 구현되지 않았지만,
> Station 에 등록되어 있으면 `EpGet` 조회는 동일하게 동작한다.
> 장치마다 감지 판정 필드가 **`type`** 인 것과 **`val`** 인 것이 다르므로 표를 정확히 따를 것.

| devtype | 의미 | idx | 감지 판정 |
|---|---|---|---|
| `SL_DF_MM` (동작감지센서) / `SL_SC_BM` (동작감지센서CUBE) | 동작 감지 | `M` | `M.type = 1` 감지됨 , `M.type = 0` 감지안됨 |
| `SL_BP_MZ` (동작감지센서Pro) | 동작 감지 | `P1` | `P1.val = 1` 감지됨 , `P1.val = 0` 감지안됨 |
| `ZG#TS06012` (재실센서) | 재실 감지 | `M1` | `M1.val = 1` 동작감지됨 , `M1.val = 0` 감지해제 |
| `SL_DF_GG` (문열림센서) | 문/창 열림 | `A` | `A.type = 1` 문열림 , `A.type = 0` 문닫힘 |
| `SL_SC_BG` (문열림센서CUBE) | 문/창 열림 | `G` | `G.val = 0` 문열림 , `G.val = 1` 문닫힘 |
| `SL_SC_WA` (누수감지센서) | 누수 | `WA` | `WA.val > 0` 이면 누수발생 |
| `ZG#MIR-SM100-E` (연기감지센서) | 화재 | `A1` | `A1.val > 0` 이면 화재발생 |
| `SL_SC_BE` (CUBE환경센서) | 온습도/조도 | `T` / `H` / `Z` | `v` 있으면 그대로, 없으면 T·H 는 `val/10` (°C, %), Z 는 `val` (lx) |

→ `EpGet` 으로 `data` 의 채널값 조회. 제어 명령 거부.

> ⚠️ `SL_SC_BG` (문열림센서CUBE) 는 **`val = 0` 이 열림**으로, 다른 센서와 반대다. 주의.

---

## 7. Etc 카테고리

**미지원 장치 (제어/조회 모두 거부)**

- `SL_TR_XX` (485Converter)
- `UL_485_AMP220`, `UL_485_AMPAL001`
- `UL_485_TM8X`, `UL_485_TJ802`
- `UL_SUM_F`, `UL_SUM_ESG`
- `SL_NATUREX`
- `UL_IR_TV`, `UL_IR_AC` (category 가 `ac`/`etc` 로 나와도 미지원)

| devtype | 노트 |
|---|---|
| `UL_IR_CU` | SPOT Mini custom IR 리모컨 — `GetRemote` + `SendKeys` 사용 |

### 7.1 Custom IR 리모컨 (`UL_IR_CU`)

**개요**

RootONLocal 앱은 `EpGetAll` 결과에 `SL_P_IR`(SPOT Mini)가 있는 Station에서
`GetRemoteList`를 추가 호출하고, 그중 `brand="custom"` + `category="custom"` 리모컨만
`UL_IR_CU` 장치로 노출한다.

`/iot/device_dash` / `/iot/device_group` 에서 보이는 `UL_IR_CU` 행의 `me`는 LocalWeb `ai` 값이다.
예: `AI_IR_a224_1780039368`.

**버튼 목록 조회: GetRemote API**

endpoint: `api.GetRemote`, method: `GetACRemote`

```json
{
	"id": 1,
	"user": "<info.user>",
	"password": "<info.password>",
	"method": "GetACRemote",
	"params": { "ai": "AI_IR_a224_1780039368", "needKeys": 2 }
}
```

응답 구조:
```json
{
	"message": {
		"me": "a224",
		"name": "거실에어컨",
		"brand": "custom",
		"category": "custom",
		"keys": ["CS_1", "CS_2", "CS_3", "CS_4", "CS_5", "CS_6"],
		"codes": {
			"CS_1": { "duty": 38, "type": 0, "data": "...", "name": "전원" },
			"CS_2": { "duty": 38, "type": 0, "data": "...", "name": "온도올림" },
			"CS_3": { "duty": 38, "type": 0, "data": "...", "name": "온도내림" },
			"CS_4": { "duty": 38, "type": 0, "data": "...", "name": "자동" },
			"CS_5": { "duty": 38, "type": 0, "data": "...", "name": "냉방" },
			"CS_6": { "duty": 38, "type": 0, "data": "...", "name": "제습" }
		}
	}
}
```

| 응답 필드 | 설명 |
|---|---|
| `message.me` | SendKeys에 사용하는 `remoteMe` 값 (device.me와 다름) |
| `message.name` | 리모컨 이름 — Openclaw 기기 매칭에 활용 |
| `message.keys` | 버튼 코드 배열 (CS_1~CS_9, 최대 9개) |
| `message.codes[code].name` | 버튼 이름 — Openclaw 기능 매칭에 활용 |
| `message.codes[code].data` | IR 신호 raw data |

**버튼 실행: SendKeys API**

endpoint: `api.SendKeys`, method: `SendKeys`

```json
{
	"id": 1,
	"user": "<info.user>",
	"password": "<info.password>",
	"method": "SendKeys",
	"params": {
		"me": "a224",
		"category": "custom",
		"ai": "AI_IR_a224_1780039368",
		"keys": "[\"CS_1\"]"
	}
}
```

| 파라미터 | 값 | 설명 |
|---|---|---|
| `me` | GetRemote 응답의 `message.me` | `/iot/device_*` 의 `me`와 다름 |
| `ai` | `/iot/device_*` 의 `me` 값 | `AI_IR_xxxx` 형태 |
| `keys` | JSON 문자열화 배열 | 한 번에 버튼 1개 전송 |

**제약사항**

- `UL_IR_CU`에 `EpGet` / `EpSet` / `EpSetVar`를 사용하지 않는다.
- 모든 제어는 `GetRemote` → 버튼 목록 조회, `SendKeys` → 버튼 실행 흐름을 따른다.
- 한 번에 1개 버튼만 실행 (keys 배열에 1개 요소만 포함).

**`last_stat` 캐시 활용 (GetRemote 생략 가능)**

앱이 리모컨을 한 번이라도 표시했다면 `/iot/device_*` 의 `last_stat` 에 버튼 정보가
캐시되어 있다. 이 경우 `GetRemote` 호출 없이 바로 버튼을 고를 수 있다.

```json
// last_stat (JSON 문자열 파싱 후)
{
  "me": "AI_IR_a224_1780039368",
  "devtype": "UL_IR_CU",
  "ai": "AI_IR_a224_1780039368",
  "remoteMe": "a224",
  "name": "거실에어컨",
  "keys": ["CS_1", "CS_2"],
  "codes": { "CS_1": { "name": "전원" }, "CS_2": { "name": "온도올림" } }
}
```

- `remoteMe` → `SendKeys.params.me`, `ai` → `SendKeys.params.ai` 로 바로 사용.
- `last_stat` 이 비어 있거나 `remoteMe`/`codes` 가 없으면 `GetRemote` 로 조회한다.

**Openclaw 매칭 전략**

사용자가 기기 제어를 요청했을 때, 실제 `category` 장치(예: `V_AIR_P`)가 없으면
`UL_IR_CU`의 리모컨 이름과 버튼 이름을 분석해 의도를 추론한다.

**예시 흐름: "거실 에어컨 켜줘"**

1. 거실 에어컨 물리 장치(`V_AIR_P`) 없음
2. `UL_IR_CU` 목록 탐색 → 리모컨 이름(`last_stat.name` 또는 `GetRemote.message.name`) = "거실에어컨" 매칭
3. 리모컨의 `keys`/`codes` 확보 (`last_stat` 캐시 우선, 없으면 `GetRemote`)
4. 버튼 이름 중 "전원" 또는 "켜기" 찾기 → `CS_1` 매칭
5. `SendKeys` 실행: `keys: "[\"CS_1\"]"`

**버튼 이름 → 의도 유추 규칙**

버튼 `name` 은 사용자가 등록한 실제 이름이므로 자연어 명령과 직접 매칭한다.

| 사용자 명령 | 매칭할 버튼 이름 예 | 비고 |
|---|---|---|
| 켜줘 / 전원 켜 | "전원", "켜기", "ON", "파워" | 전원 토글형 리모컨이면 "전원" 1개 버튼이 ON/OFF 겸용 |
| 꺼줘 / 전원 꺼 | "전원", "끄기", "OFF" | "끄기" 버튼이 없으면 "전원" 버튼 사용 (토글) |
| 온도 올려/내려 | "온도올림", "온도내림", "UP", "DOWN" | |
| 냉방/난방/제습/자동 | "냉방", "난방", "제습", "자동" | |

- ⚠️ 토글형 "전원" 버튼은 현재 상태를 알 수 없으므로(IR 은 단방향),
  "켜줘"/"꺼줘" 모두 같은 버튼을 보내게 된다. 실행 후 사용자에게
  "전원 버튼을 전송했습니다" 처럼 토글임을 알려주는 것을 권장.
- 매칭되는 버튼이 없으면 버튼 이름 목록을 사용자에게 보여주고 선택받는다.

**매칭 우선순위**

- 리모컨 이름: 장소 + 기기 키워드 (예: "거실에어컨", "안방조명", "주방환기")
- 버튼 이름: 동작 키워드 (예: "전원", "온도올림", "냉방", "제습")
- 버튼 코드: `CS_1` ~ `CS_9` 형태 (1회 요청 = 1개 버튼)

---

## 8. 상태 조회 전용 계측 장치 (EpGet)

"온도 몇 도야?", "전력 얼마나 써?", "발전량 알려줘" 같은 질문은 아래 장치를
`EpGet` 으로 조회해 답한다. 우선 `/iot/device_*` 의 `last_stat` 을 파싱하고,
최신 값이 필요하면 `EpGet` 을 호출한다. **모두 제어(EpSet) 불가.**

### 8.1 공통 값 판독 규칙

- 채널 값 객체는 `{ type, val, v? }` 형태. **`v` 가 있으면 표시값으로 그대로 사용**,
  없으면 아래 표의 `val` 변환식을 적용한다.
- **IEEE754 변환**: 전력 채널의 `val` 은 32bit float 를 정수로 담은 값이다.
  4바이트 그대로 IEEE754 single-precision float 로 재해석해야 한다.
  (예: python `struct.unpack('<f', struct.pack('<I', val))[0]`)

### 8.2 공기질/환경 센서 (category=`sensor`)

| devtype | 채널 | 의미 | val 변환 |
|---|---|---|---|
| `ZG#PMT300-SGMR-ZTN` (공기질센서Pro) | `T1` | 온도 °C | val/10 |
| | `H1` | 습도 % | val/10 |
| | `Z1` | 조도 lx | val |
| | `PM(1)1` | PM1 μg/m³ | val |
| | `PM1` | PM2.5 μg/m³ | val |
| | `PM(10)1` | PM10 μg/m³ | val |
| | `CO2PPM1` | CO₂ ppm | val |
| | `TVOC1`, `CH2O1` | TVOC/포름알데히드 μg/m³ | `v`(mg/m³)×1000, `val` 은 μg/m³ 그대로 |
| `ZG#PMT300-S-ZTN` (공기질센서Lite) | `T1`, `H1`, `PM(1)1`, `PM1`, `PM(10)1` | Pro 와 동일 (CO2/TVOC/CH2O/조도 없음) | 위와 동일 |
| `V_HTTP_P` (AWAIR) | `T` | 온도 °C | val/10 |
| | `H` | 습도 % | val/10 |
| | `VOC` | VOC ppm | val (μg/m³ 환산 시 ×46/24.45) |
| | `CO2PPM` | CO₂ ppm | val |
| | `PM` | PM2.5 μg/m³ | val/10 |
| | `QA` | 종합점수 0~100 | val (장치 산출값) |
| `SL_SC_BE` (CUBE환경센서) | `T`, `H` | 온도 °C / 습도 % | val/10 |
| | `Z` | 조도 lx | val |

### 8.3 전력 계측 (category=`etc` 또는 `switch`)

| devtype | 채널 | 의미 | val 변환 |
|---|---|---|---|
| `ZG#PMM-300Z2`, `ZG#E240-KR080Z0-HA` (전력량측정기) | `EP1` | 소비전력 W | **IEEE754 float** |
| | `EE1` | 누적전력 kWh | **IEEE754 float** |
| `SL_OE_DE` (스마트플러그) | `P1` | ON/OFF 상태 (제어는 §2 switch 규칙) | val 0/1 |
| | `P2` | 누적전력 kWh | **IEEE754 float** |
| | `P3` | 소비전력 W | **IEEE754 float** |
| `V_485_P` (태양광 발전기 — data 에 `EE1`/`EP1` 존재 시) | `RUN` | 1=발전중, 0=대기중 | val |
| | `EE1` | 금일 발전량 kWh | val/100 |
| | `EE` | 누적 발전량 kWh | **IEEE754 float** |

> 스마트플러그는 제어(ON/OFF)와 조회(전력) 를 모두 지원하는 유일한 switch 장치다.
> "플러그 전기 얼마나 써?" → `EpGet` 후 `P3` (W), "누적 사용량" → `P2` (kWh).

### 8.4 병합 가상 장치 (`MERGED_AQ` / `MERGED_PMM` / `MERGED_SOLAR`)

앱에서 같은 종류 장치 여러 개를 묶은 **가상 장치**. `/iot/device_*` 에
`dev_type=MERGED_*`, `me="merged-..."`, `category="unknown"` 으로 나타난다.

- ⚠️ 병합 장치의 `me` 는 가상 ID — **EpGet/EpSet 절대 금지.**
- `attribute` (JSON 문자열, api_version 1.1.0+) 에 소스 장치 정보가 들어 있다:

```json
{ "merged": true,
  "mergedSourceMes": ["me1", "me2"],
  "sourceDevtype": "ZG#PMT300-SGMR-ZTN" }
```

**조회 절차**

1. `attribute.mergedSourceMes` 의 각 `me` 를 `/iot/device_*` 목록(없으면 `EpGetAll`)에서
   찾아 소속 `station_ip` 확인. (소스가 서로 다른 Station 에 있을 수 있음)
2. 각 소스를 `EpGet` 으로 조회하고 `sourceDevtype` 의 채널 규칙(§8.2/§8.3)으로 판독.
3. 집계: `MERGED_AQ` → 채널별 **평균**, `MERGED_PMM`/`MERGED_SOLAR` → **합산**.

---

## 9. 자연어 매칭 권장 키워드

| 한국어 키워드 | 후보 카테고리 |
|---|---|
| 불, 등, 조명, 라이트 | `light` + `switch` (등 스위치) |
| 에어컨, 냉방, 난방, 온도(설정) | `ac` |
| 블라인드, 커튼, 가림막 | `blind` |
| 콘센트, 플러그 | devtype=`SL_OE_DE` |
| 환기, 환풍, 신선 | devtype=`V_FRESH_P` |
| 동작, 사람, 재실, 움직임 | sensor(동작/재실) — §6 |
| 문, 창문, 열렸(어/나), 닫혔(어/나) | sensor(문열림) `SL_DF_GG`/`SL_SC_BG` — §6 |
| 누수, 물 새(는지) | sensor(누수) `SL_SC_WA` — §6 |
| 화재, 연기, 불 났(는지) | sensor(화재) `ZG#MIR-SM100-E` — §6 |
| 공기, 미세먼지, CO2, 온도/습도(조회) | sensor(공기질/환경) — §8.2 |
| 전기, 전력, 사용량, 몇 와트 | 전력량측정기/스마트플러그 — §8.3 |
| 태양광, 발전량 | `V_485_P`(태양광) / `MERGED_SOLAR` — §8.3/§8.4 |
| 리모컨, (물리 장치 없는) 에어컨/TV | `UL_IR_CU` — §7.1 |

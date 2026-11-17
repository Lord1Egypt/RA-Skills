---
name: rootonlocal-iot
description: Control and query LifeSmart Smart Station IoT devices registered in the RootONLocal app. Queries local device/zone info via http://127.0.0.1:18080, then calls the LifeSmart LocalWeb API directly to get or set device state (lights, switches, blinds, AC, custom IR remotes) and read measurements (air quality, temperature, power/energy meters, solar).
version: 2.0.4
metadata:
  openclaw:
    emoji: "🏠"
    homepage: https://github.com/Kcobstkin/RootONLocal_Monorepo
    requires:
      bins:
        - curl
---

# RootONLocal IoT Skill (OpenClaw)

이 폴더는 **OpenClaw**(또는 임의의 LLM 스킬 호스트)에서 본 RootONLocal 앱이 만든
구역(group)별/대시보드 IoT 장치를 자연어로 제어하기 위한 **스킬 패키지**입니다.

본 스킬은 두 단계의 HTTP 호출만으로 동작합니다.

1. 본 앱(태블릿/PC)이 띄운 **로컬 정보 API** (`http://127.0.0.1:18080`) 호출
   → 사용 가능한 스테이션 / 구역 / 장치 / LocalWeb 자격증명을 받아온다.
2. 1번에서 받은 정보로 **LifeSmart Local Web API**를 **직접 호출**
   → 장치 상태 조회(`EpGet`) / 제어(`EpSet`).

---

## 폴더 구성

| 파일 | 설명 |
|---|---|
| `SKILL.md` | (이 파일) 스킬 사용 개요 — OpenClaw 에 그대로 등록한다. |
| `api-spec.md` | 1단계 IoT 정보 API 전체 명세 (`/iot/info`, `/iot/station`, `/iot/group`, `/iot/device_dash`, `/iot/device_group`) |
| `localweb-spec.md` | 2단계 LifeSmart Local Web API 명세 (URL, 인증, `EpGet`, `EpSet`, `type/val` 코드) |
| `device-types.md` | devtype → 카테고리(`switch`/`light`/`blind`/`ac`/`sensor`/...) → 제어 채널 매핑, 계측 장치(공기질/전력/태양광/병합) 조회 채널, IR 리모컨 매칭 규칙 |
| `examples.md` | "거실 에어컨 25도", "안방 불 꺼줘" 등 자연어 → API 호출 변환 예시 |

---

## 사용 흐름 (요약)

```
[사용자] "거실이 너무 덥다"
    ↓
[OpenClaw]
    1) 정보 API 4개 전부 조회 (장치 목록만으로는 구역명 매칭 불가):
       GET http://127.0.0.1:18080/iot/info
       → { useHttps, scheme, port, user, password, url_template }
       GET http://127.0.0.1:18080/iot/group
       → [{ group_id, groupname:"거실", ... }, ...]   ← group_id ↔ 구역명 매핑
       GET http://127.0.0.1:18080/iot/device_dash     ← 대시보드 장치
       GET http://127.0.0.1:18080/iot/device_group    ← 구역별 장치 (group_id 포함)
    2) "거실" → group 목록에서 group_id 찾기 →
       device_group 에서 group_id 일치 + dev_type∈에어컨 인 장치 추출
       → { station_ip:"192.168.0.10", agt, me, dev_type:"V_AIR_P", ... }
       (구역 장치에 없으면 device_dash 에서 이름으로 검색)
    3) (필요 시) 현재 상태 — LocalWeb 직접 호출:
       POST {scheme}://{station_ip}:{port}/mgaweb/api.EpGet
            body: { id:1, user, password, method:"EpGet", params:{ me } }
    4) 제어 — LocalWeb 직접 호출:
       POST {scheme}://{station_ip}:{port}/mgaweb/api.EpSet
            body: { id:1, user, password, method:"EpSet",
                    params:{ me, idx:"O", type:129, val:1 } }  ← 전원 ON
```

> ⛔ **LocalWeb 요청 본문은 항상 `id`/`user`/`password`/`method`/`params` 5개 필드 전부 포함.**
> 하나라도 빠지면 Station 이 `{ "message":"ENPF...", "status":"ENL" }` 오류를 반환한다.
>
> ⛔ **성공 판정은 응답에 `code` 필드가 있고 `code === 0` 인 경우만.**
> `code` 가 없는 응답(위 ENL 오류 등)이나 `code !== 0` 은 전부 실패다.
> 실패를 성공처럼 사용자에게 보고하지 않는다. (`localweb-spec.md` §3, §5)

---

## 사전 조건

- 본 앱이 실행 중이어야 한다. (Android 포그라운드 서비스 또는 Electron main 프로세스가
  127.0.0.1:18080 에 정보 서버를 띄운다.)
- 본 앱에서 **Local Web 사용 ON** + **공통 계정/비밀번호** 입력이 되어 있어야 한다.
  (`/iot/info.enabled === true` 로 확인 가능)
- OpenClaw 가 본 앱과 **같은 디바이스**에서 실행되어야 한다.
  서버는 **127.0.0.1 (loopback) 전용 바인딩**이라 외부에서 접근 불가.

---

## 멀티 매칭 처리 규칙

자연어 → 장치 변환 시 다음 우선순위로 후보를 좁힌다.

1. **구역(groupname)** 키워드 매칭 → `/iot/device_group` 의 `group_id` 로 1차 필터.
2. **장치 카테고리** (예: 에어컨/불/블라인드) → `dev_type` 의 `category` 로 2차 필터.
3. 1+2 결과가:
   - 0개 → "찾을 수 없음" 응답.
   - 1개 → 바로 실행.
   - 2개 이상 → 후보 목록을 사용자에게 다시 묻는다.

---

## 명령 유효성 규칙

> ⛔ **type-val 결합 규칙 (switch 채널 · AC 전원 한정)**
> - ON = `type:129, val:1` 이 조합만 유효하다.
> - OFF = `type:128, val:0` 이 조합만 유효하다.
> - `type:128, val:1` 또는 `type:129, val:0` 은 절대 사용 금지. type 과 val 은 독립적으로 선택하지 않는다.
> - 조명·블라인드는 `type=128/129` 를 **사용하지 않는다**. (아래 규칙 및 `device-types.md` 참조)

- **에어컨** (`V_AIR_P`/`V_FRESH_P` 만 제어): 전원(`O`)/모드(`MODE`)/온도(`tT`, val=온도×10)/풍량(`F`) 외 동작은 거부 (`에어컨 닫아줘` 등).
  category 가 `ac` 라도 `dev_type=UL_IR_AC` 는 미지원 장치 — 제어 거부.
- **블라인드** (`SL_DOOYA`): `idx=P2, type=207, val=열림률(0~100)` 으로 열기(100)/닫기(0)/부분 열기(X).
  정지는 `idx=P2, type=206, val=128`. `P1` 은 상태 조회 전용(read-only).
- **조명**: 모든 조명(`SL_LI_WW`/`SL_SW_WW`/`V_HG_WW` 등)은 ON/OFF·밝기 모두 `type=207(ON)/206(OFF)`,
  `val=밝기(1~255)`. 색온도는 `idx=P2, type=207, val=1~255` (2700K~6000K 매핑).
- **스위치(다채널)**: `idx` 가 장치별로 `P1~P8`, `L1~L3`, `P2~P4` 등 다르므로
  반드시 `device-types.md` 의 채널 표에서 가능 idx 안에서만 선택.
- **CUBE Button (`SL_SC_BB_V2`)**: 이벤트 전용. 제어 명령 거부.
- **센서/공기질/전력량측정기/AWAIR/태양광**: 조회(`EpGet`) 만 허용, 제어 거부.
  "온도 몇 도야?", "전력 얼마나 써?", "발전량 알려줘" 같은 상태 질문에 사용 — 채널/단위 변환은 `device-types.md` §8.
  "문 열려 있어?", "누수 감지됐어?" 같은 감지형 센서(동작/재실/문열림/누수/화재) 질의는 `device-types.md` §6 의
  판정 표를 따른다 (devtype 별로 판정 필드가 `type`/`val` 로 다름).
  스마트플러그(`SL_OE_DE`)는 예외적으로 **제어(P1) + 전력 조회(P2/P3)** 둘 다 지원.
- **병합 가상 장치 (`MERGED_AQ`/`MERGED_PMM`/`MERGED_SOLAR`)**: `me` 가 가상 ID라 `EpGet`/`EpSet` 금지.
  `attribute.mergedSourceMes` 의 소스 장치들을 개별 `EpGet` 후 AQ=평균 / PMM·SOLAR=합산 (`device-types.md` §8.4).
- **Custom IR 리모컨 (`UL_IR_CU`)**: `EpGet`/`EpSet` 금지. `/iot/device_*` 의 `me` 를 `ai` 로 사용해 `GetRemote`로 버튼을 조회하고, 선택한 code 1개를 `SendKeys` 의 `keys` 문자열 배열로 보낸다.
  `last_stat` 에 버튼 캐시(`remoteMe`/`keys`/`codes`)가 있으면 `GetRemote` 생략 가능.
  물리 장치(`V_AIR_P` 등)가 없을 때 리모컨 이름("거실에어컨")·버튼 이름("전원", "냉방")으로 의도를 유추해 실행한다 — 유추 규칙은 `device-types.md` §7.1.

자세한 매핑은 [`device-types.md`](./device-types.md) 참조.

---

## 응답 정책 (스킬이 호출자에게 반환)

스킬은 다음 형태의 JSON 으로 결과를 돌려주는 것을 권장.

```json
{
  "ok": true,
  "action": "epSet",
  "station_id": 3,
  "device": { "me": "0001ABC...", "name": "거실 에어컨", "dev_type": "V_AIR_P" },
  "request": { "idx": "O", "type": 129, "val": 1 },
  "result": { "code": 0, "message": "ok" }
}
```

오류:

```json
{
  "ok": false,
  "error": "ambiguous_device",
  "candidates": [ { "me":"...", "name":"...", "groupname":"..." }, ... ]
}
```

---

## 향후 확장 (resolve API — 본 앱 측 추가 기능)

본 앱에 추가될 예정인 보조 엔드포인트:

- `POST /iot/resolve` — OpenClaw 가 만들어낸 명령(구역명/장치종류/동작)을 보내면
  본 앱이 위 규칙을 적용해 매칭/유효성 검사 결과를 반환한다.
  - 다중 매칭 시 후보 반환.
  - 유효하지 않은 명령(예: 에어컨에 close)은 reject.

본 1.0 버전 스킬은 위 resolve API 없이도 client-side 매칭으로 동작 가능.

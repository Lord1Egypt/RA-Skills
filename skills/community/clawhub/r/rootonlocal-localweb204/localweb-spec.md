# LifeSmart Local Web API — 직접 호출 명세 (2단계)

`/iot/info` 와 `/iot/station` 에서 받은 정보로 OpenClaw 가 **직접** Smart Station 의
LocalWeb API 를 호출한다. (본 앱을 거치지 않는다.)

---

## 1. URL 빌드

```
{scheme}://{station_ip}:{port}/mgaweb/{endpoint}
```

- `scheme`, `port` : `GET /iot/info` 응답의 같은 이름 필드 사용
  - `useHttps=true` → `scheme="https"`, `port=8080`
  - `useHttps=false` → `scheme="http"`, `port=8008`
- `station_ip` : `GET /iot/station` 응답의 `ip` (장치의 `station_id` 로 lookup)
- `endpoint` : 예) `api.EpGet`, `api.EpSet`, `api.EpGetAll`, `api.EpGetAgtState`

> HTTPS 인증서는 self-signed 일 수 있음. OpenClaw 측에서 인증서 검증을
> 사설 IP(192.168.x.x / 10.x / 172.16-31.x)에 한해 우회하는 것을 권장.

---

## 2. 요청 형식 (공통)

- Method: `POST`
- `Content-Type: application/json`
- Body — **아래 5개 필드를 전부 포함해야 한다. 하나라도 빠지면 Station 이 오류를 반환한다.**

```json
{
  "id": 1,
  "user": "<info.user>",
  "password": "<info.password>",
  "method": "<EpGet|EpSet|...>",
  "params": { ... }
}
```

- `id`: 호출자가 만든 임의 일련번호 (아무 정수). 응답에 그대로 echo 된다.
- `user` / `password`: `GET /iot/info` 응답 값을 그대로 사용. **모든 호출에 매번 포함** (세션/토큰 없음).
- `params` 가 없는 method 라도 `"params": {}` 로 빈 객체를 넣는다.

## 3. 응답 형식 (공통)

```json
{
  "id": 1,
  "code": 0,
  "message": <엔드포인트별 페이로드>
}
```

**성공 판정은 `code === 0` 하나뿐이다.**

- `code === 0` → 성공.
- `code !== 0` → 실패. `message` 에 사유.
- **`code` 필드 자체가 없는 응답도 실패다.** 예:

```json
{ "message": "ENPF1:BjMAADSYeAEAAAwuFAz__w/mgaweb/api:EpGet", "status": "ENL" }
```

위와 같은 `ENPF...` / `status:"ENL"` 형태 응답은 요청 본문이 불완전하거나
(`user`/`password`/`method` 누락 등) endpoint/형식이 잘못됐을 때 반환된다.
**절대 성공으로 처리하지 말고**, 본문 5개 필드가 전부 포함됐는지 다시 확인 후 재시도한다.

---

## 4. 엔드포인트

### 4.1 `api.EpGet` — 장치 단건 조회

**params**

```json
{ "me": "0001ABCDEF" }
```

**응답 `message` 예시 (스위치 1구)**

```json
{
  "agt": "_abcAGT",
  "me": "0001ABCDEF",
  "devtype": "SL_SW_BJ84",
  "data": {
    "P1": { "type": 129, "val": 1, "v": 1, "name": "P1", "valts": 1716000000 }
  }
}
```

- `data` 의 key 는 채널 idx (`P1`, `L1`, `RGBW` 등).
- `type` 코드는 ON/OFF, dim 등을 의미. (4.2 참조)
- `val` 의 의미는 카테고리에 따라 다름.

### 4.2 `api.EpSet` — 장치 채널 제어

**params**

```json
{ "me": "0001ABCDEF", "idx": "P1", "type": 129, "val": 1 }
```

| 카테고리 | idx | type | val | 의미 |
|---|---|---|---|---|
| switch | `P1`~`P8` / `L1`~`L3` / `P2`~`P4` (devtype별) | 129(0x81) | 1 | ON |
| switch | (위와 동일) | 128(0x80) | 0 | OFF |
| light (모든 조명) | `P1` 또는 `L` (devtype별) | 207 | brightness 1~255 | ON + 밝기 (켤 때 현재 밝기 그대로) |
| light (모든 조명) | `P1` 또는 `L` (devtype별) | 206 | brightness 1~255 | OFF (val 은 현재 밝기 유지) |
| light (색온도) | `P2` | 207 | colortemp 1~255 | 색온도 변경 (2700K~6000K) |
| blind | `P2` | 207(0xCF) | 0~100 | 열림률 지정 (100=완전 열기, 0=완전 닫기) |
| blind | `P2` | 206(0xCE) | 128(0x80) | 정지 |
| ac | `O` (power) | 129 / 128 | 1 / 0 | 전원 ON/OFF |
| ac | `MODE` (mode) | 206 | V_AIR_P: 1=자동/2=송풍/3=냉방/4=난방/5=제습, V_FRESH_P: 1=자동/2=전열/9=취침/10=환기 | 모드 |
| ac | `tT` (temp) | 136(0x88) | 온도×10 (180~300) | 설정 온도 (25도 → val=250) |
| ac | `F` (wind) | 206 | 15=약/45=중/75=강/101=자동 | 풍량 (V_FRESH_P 는 101 없음) |

> ⚠️ 조명·블라인드는 `type=128/129` 를 사용하지 않는다.
> devtype 별 정확한 idx 가능 목록은 [`device-types.md`](./device-types.md).

### 4.3 `api.EpSetVar` — 변수형 명령

`SL_DOOYA`(블라인드) 일부 동작 / 일부 IR 매크로에 사용. 필요 시 추가 명세.

```json
{
  "agt": "<station agt>",
  "me": "0001...",
  "idx": 193,
  "cmd": 60,
  "cmddata": "<문자열>",
  "needDetailed": 1
}
```

### 4.4 `api.EpGetAll` — Station 전체 장치 일괄 조회

**params**

```json
{ "degree": 2 }
```

**응답 `message`** : `[{ agt, me, devtype, data:{...} }, ...]`

스킬에서 *상태 동기화 직후* 한 번 호출하면 stale 데이터를 갱신할 수 있다.

### 4.5 `api.EpGetAgtState` — Station 헬스체크

`{}` 만 보내 응답 `code` 가 0 이면 LocalWeb 통신 가능.
실제 장치 데이터는 없음. 통신 가능 여부 확인용으로만 사용.

### 4.6 `api.GetRemoteList` — SPOT Mini IR 리모컨 목록

RootONLocal 앱 내부 검색용 API. `EpGetAll` 에 `SL_P_IR` 장치가 있는 Station에서만 호출한다.
OpenClaw 는 보통 `/iot/device_dash` / `/iot/device_group` 에 이미 노출된 `UL_IR_CU` 장치를 사용하면 된다.

```json
{ "id": 1, "user": "<info.user>", "password": "<info.password>",
  "method": "GetRemoteList", "params": {} }
```

응답 `message` 는 `{ ai: remoteInfo }` 형태이며, 앱은 `brand="custom"` + `category="custom"` 항목만 사용한다.

### 4.7 `api.GetRemote` — custom IR 버튼 조회

`UL_IR_CU` 는 `EpGet` 으로 조회하지 않는다. `/iot/device_*` 의 `me` 값을 `ai` 로 넣는다.

```json
{
  "id": 1,
  "user": "<info.user>",
  "password": "<info.password>",
  "method": "GetACRemote",
  "params": { "ai": "AI_IR_a224_1780039368", "needKeys": 2 }
}
```

응답 `message.keys` 는 버튼 code 배열, `message.codes[code].name` 은 화면/자연어 매칭용 버튼 이름이다.
응답 `message.me` 는 `SendKeys.params.me` 에 넣을 SPOT Mini의 `me` 값이다.

### 4.8 `api.SendKeys` — custom IR 버튼 실행

`UL_IR_CU` 는 `EpSet` 으로 제어하지 않는다. `GetRemote` 로 얻은 button code 한 개를 문자열 배열로 보낸다.

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

- `params.me`: `GetRemote.message.me`
- `params.ai`: `/iot/device_*` 의 `me`
- `params.keys`: JSON 배열을 문자열화한 값. 본 스킬에서는 한 번에 code 1개만 전송.

---

## 5. 오류 패턴

| 증상 | 원인/조치 |
|---|---|
| 네트워크 자체 실패 | Station 오프라인 또는 LAN 분리. `/iot/station.is_active` 값으로 사전 차단. |
| HTTP 4xx/5xx | URL 또는 포트(8080/8008) 잘못. `useHttps` 확인. |
| 응답에 `code` 없음 + `status:"ENL"` (`ENPF...` message) | 요청 본문 불완전 — `id`/`user`/`password`/`method`/`params` 5개 필드 전부 있는지 확인. endpoint 표기(`api.EpGet`) 확인. **실패로 처리.** |
| `code === -10001` 류 | `user`/`password` 불일치. `/iot/info` 다시 호출해 최신 자격증명 확보. |
| `code !== 0` & idx 거부 | 해당 장치/idx 조합이 미지원. `device-types.md` 표 참고. |
| HTTPS 인증서 오류 | 사설 IP 한정 자체서명 인증서 우회 필요. |

---

## 6. 보안 권장

- OpenClaw 가 받은 `info.password` 는 메모리 보관, 영구 저장 금지.
- 같은 디바이스 안에서만 사용.
- 오프라인일 때(`/iot/info` 자체 실패)는 즉시 실패 응답.

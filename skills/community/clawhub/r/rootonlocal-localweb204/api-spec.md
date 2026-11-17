# RootONLocal IoT Info API — Spec (1단계 정보 API)

본 앱(태블릿/PC)이 자체적으로 띄우는 HTTP 서버. **127.0.0.1 전용 바인딩.**

- 기본 포트: **18080** (변경 가능)
- 인증: 없음 (loopback 전용이므로 외부 접근 불가)
- 응답: 항상 `Content-Type: application/json; charset=utf-8`
- CORS: `Access-Control-Allow-Origin: *` (동일 디바이스 WebView 호출 지원)

> ⚠️ `/iot/info` 는 LocalWeb 계정/비밀번호를 **평문**으로 반환한다.
> 본 서버에 외부에서 접근 가능한 상태가 되면 자격증명이 노출된다.

---

## 공통 응답 헤더

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: *
Cache-Control: no-store
```

---

## `GET /`  (헬스 체크)

```json
{ "ok": true, "service": "RootONLocal-IotApi" }
```

`GET /iot/ping` 도 동일.

---

## `GET /iot/info`

LocalWeb 호출에 필요한 자격증명/스킴/포트/URL 템플릿.

### Response (200)

```json
{
  "enabled": true,
  "useHttps": true,
  "scheme": "https",
  "port": 8080,
  "user": "admin",
  "password": "********",
  "url_template": "https://{station_ip}:8080/mgaweb/{endpoint}",
  "api_version": "1.1.0",
  "generated_at": "2026-05-28T03:00:00.000Z"
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `enabled` | bool | 앱에서 Local Web 사용 ON 여부. `false` 면 사용자에게 앱 설정에서 켜라고 안내. |
| `useHttps` | bool | true → 포트 8080, false → 8008 |
| `scheme` | "http"\|"https" | `useHttps` 와 동기화 |
| `port` | number | LocalWeb 포트 (8080 또는 8008) |
| `user`, `password` | string | LocalWeb 호출 body 의 `user`/`password` 필드에 그대로 사용 |
| `url_template` | string | LocalWeb URL 패턴. `{station_ip}` 와 `{endpoint}` 치환 |
| `api_version` | string | IoT API 버전. 호환성 체크용 |
| `generated_at` | string ISO | 스냅샷 생성 시각 |

---

## `GET /iot/station`

본 앱에 등록된 Smart Station 전체 목록.

### Response (200)

```json
[
  {
    "id": 1,
    "lsid": "A3:0001:abc...",
    "name": "Main Station",
    "ip": "192.168.0.10",
    "port": 12348,
    "is_active": 1
  }
]
```

| 필드 | 설명 |
|---|---|
| `id` | DB 내부 PK. 다른 엔드포인트의 `station_id` 참조 키. |
| `lsid` | LifeSmart Station 고유 ID. |
| `name` | 사용자 지정 이름. |
| `ip` | LAN 내 IP. LocalWeb 호출 시 `url_template.{station_ip}` 에 대입. |
| `port` | LifeSmart UDP 디스커버리 포트 (LocalWeb 와는 다름). |
| `is_active` | 1=Local Web 통신 정상. 0=경고/오프라인. |

---

## `GET /iot/group`

본 앱에서 사용자가 만든 구역(그룹) 트리. 2단계 (대그룹/소그룹).

### Response (200)

```json
[
  { "group_id": 1, "groupname": "1층", "node": 2, "root_id": 0, "sort_order": 0 },
  { "group_id": 2, "groupname": "거실", "node": 3, "root_id": 1, "sort_order": 0 },
  { "group_id": 3, "groupname": "안방", "node": 3, "root_id": 1, "sort_order": 1 }
]
```

| 필드 | 설명 |
|---|---|
| `group_id` | DB 내부 PK. `device_group` 응답의 `group_id` 와 매칭. |
| `groupname` | 사용자 지정 이름. 자연어 매칭의 핵심 키 (`"거실"` 등). |
| `node` | 2 = 대그룹, 3 = 소그룹. |
| `root_id` | 소그룹일 때 부모 대그룹의 `group_id`. 대그룹은 0. |
| `sort_order` | UI 정렬 순서. |

---

## `GET /iot/device_dash`

모든 사용자의 **대시보드 장치** 목록. (대시보드는 사용자별)

### Response (200)

```json
[
  {
    "device_id": 12,
    "station_id": 1,
    "station_ip": "192.168.0.10",
    "agt": "_abcAGT",
    "me": "0001ABCDEF",
    "name": "거실 메인등",
    "dev_type": "SL_SW_BJ84",
    "category": "switch",
    "type_label": "Air스위치",
    "junction_id": 41,
    "sort_order": 0,
    "user_id": 2,
    "last_stat": "{\"P1\":{\"type\":129,\"val\":1,\"v\":1}}",
    "attribute": null
  }
]
```

| 필드 | 설명 |
|---|---|
| `device_id` | DB devices.id |
| `station_id` | 소속 Station |
| `station_ip` | Station LAN IP — `/iot/station` 조회 없이 LocalWeb 호출 시 바로 `url_template.{station_ip}` 에 대입 |
| `agt` | LifeSmart agt (Station 식별자). EpSetVar 등 일부 LocalWeb 호출에 필요 |
| `me` | LifeSmart me (장치 식별자). 모든 EpGet/EpSet 의 핵심 키 |
| `name` | 사용자 지정 이름 |
| `dev_type` | LifeSmart devtype. `device-types.md` 참조 |
| `category` | 자동 분류: `ac`/`blind`/`light`/`switch`/`sensor`/`etc`/`unknown` |
| `type_label` | 사용자 친화 한글명 |
| `user_id` | 어떤 사용자 대시보드인지 |
| `last_stat` | 마지막으로 알려진 상태(JSON 문자열). 비어있을 수 있음 |
| `attribute` | devices.attribute (JSON 문자열 또는 null). api_version 1.1.0+. 병합 장치(`MERGED_*`)의 `mergedSourceMes`/`sourceDevtype` 해석에 사용 (`device-types.md` §8.4) |

> `dev_type="UL_IR_CU"` 인 custom IR 리모컨은 예외다. 이때 `me` 는 `EpGet/EpSet` 용 장치 ID가 아니라
> `GetRemote` / `SendKeys` 에 사용할 `ai` 값이다. 자세한 호출 규칙은 `device-types.md` 의 `UL_IR_CU` 항목을 따른다.
> `last_stat` 에 버튼 정보(`remoteMe`/`keys`/`codes`)가 캐시되어 있으면 `GetRemote` 를 생략할 수 있다.

---

## `GET /iot/device_group`

모든 구역의 **구역 장치** 목록.

### Response (200)

```json
[
  {
    "device_id": 12,
    "station_id": 1,
    "station_ip": "192.168.0.10",
    "agt": "_abcAGT",
    "me": "0001ABCDEF",
    "name": "거실 메인등",
    "dev_type": "SL_SW_BJ84",
    "category": "switch",
    "type_label": "Air스위치",
    "junction_id": 88,
    "sort_order": 0,
    "group_id": 2,
    "last_stat": "{\"P1\":{\"type\":129,\"val\":1,\"v\":1}}"
  }
]
```

`device_dash` 와 동일 구조이며 `user_id` 대신 `group_id` 를 동봉한다.
스테이션이 여러 개인 환경에서 `station_ip` 제공으로 `/iot/station` 조회 없이 바로 LocalWeb 호출 가능.
같은 장치가 여러 구역에 들어 있으면 행이 중복으로 나온다.

---

## 오류 응답

```
HTTP/1.1 404 Not Found
{ "error": "not_found", "path": "/iot/wrong" }

HTTP/1.1 405 Method Not Allowed
{ "error": "method_not_allowed" }

HTTP/1.1 500 Internal Server Error
{ "error": "internal", "message": "..." }
```

GET 외 다른 메서드는 모두 405.

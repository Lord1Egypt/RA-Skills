# Denote Top Ads

게임과 유틸리티 앱의 인기 광고, 급상승 광고, 새로 발견된 광고를 살펴보고 다음 이용자 확보 캠페인에서 테스트할 소재를 고를 수 있습니다.

[EN](README.md) · [ZH](README.zh.md) · [JA](README.ja.md) · KO · [ES](README.es.md) · [NL](README.nl.md) · [DE](README.de.md) · [FR](README.fr.md)

Denote는 게임과 유틸리티 앱의 광고 데이터를 매일 수집하고 갱신합니다. 한 번 수집할 때마다 광고 기록 6천만 건 이상을 살펴보며, 매주 한 번 순위를 집계합니다. 무료 계정으로 지난 한 주 동안의 게임 또는 앱 광고를 세 가지 순위표에서 각각 최대 10개까지 확인할 수 있습니다. [Denote 광고 순위 살펴보기](https://denote.net/top-ads).

| 무료 순위표 | 무엇을 볼 수 있나요? |
| --- | --- |
| 인기 광고 | 지난주에 가장 많은 관심을 받은 광고를 확인하세요. |
| 급상승 광고 | 전주보다 인기도가 가장 크게 오른 광고를 찾아보세요. |
| 신규 광고 | 새로 발견된 광고를 초기 인기도 순으로 살펴보세요. |

## 첫 주간 순위표 받기

OpenClaw 작업 공간에서 다음 명령을 실행하세요. Python 3가 필요합니다.

```sh
git clone https://github.com/denote-developer/denote-top-ads.git skills/denote-top-ads
```

1. 새 세션을 열고 “Denote로 어떤 광고를 찾을 수 있어?”라고 물어보세요.
2. [Denote 무료 계정 만들기](https://denote.net/user/register). 이미 계정이 있다면 로그인하세요. `top_ads:read` 권한을 가진 Denote API 키를 만들거나 기존 키에 이 권한을 추가하세요.
3. 에이전트의 보안 설정에 키를 `DENOTE_API_KEY` 이름으로 저장한 뒤 “지난주 앱 광고 순위를 보여 줘”라고 요청하세요. 세 가지 순위표가 바로 표시됩니다. 분야를 지정하지 않으면 게임 광고를 보여 줍니다.

채팅에는 순위별 상위 3개 광고가 한 줄씩 표시되며 소재 링크와 집행 기간이 포함됩니다. 인기·신규 순위에는 주간 소재 점수 합계가, 급상승 순위에는 주간 증가량과 증가율이 표시됩니다. 답변 끝의 로컬 보고서에서 전체 광고를 확인하세요. 카드를 열면 동영상 재생, 개요, 추이, 관련 광고, 잠재고객을 확인할 수 있으며 상세 데이터가 없어도 해당 워크스페이스 순위로 이동할 수 있습니다.

## 광고 자세히 보기

“급상승 광고 2위를 자세히 보여 줘”라고 요청해 보세요. Top Ads Pro 또는 Business 계정에서는 제공 가능한 광고 성과와 잠재고객 정보도 확인할 수 있습니다. 세 가지 주간 순위표는 무료입니다.

## 제품 화면

[![왼쪽 메뉴에서 세 가지 주간 광고 순위표를 열 수 있습니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/top-ads-navigation.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/top-ads-navigation.jpg)

*왼쪽 메뉴에서 세 가지 주간 광고 순위표를 열 수 있습니다.*

[![인기 광고: 2026년 11월 9일부터 15일까지의 게임 광고를 주간 인기도순으로 보여 줍니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/trending-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/trending-ads.jpg)

*인기 광고: 2026년 11월 9일부터 15일까지의 게임 광고를 주간 인기도순으로 보여 줍니다.*

[![급상승 광고: 전주보다 인기도가 가장 크게 오른 게임 광고입니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/rising-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/rising-ads.jpg)

*급상승 광고: 전주보다 인기도가 가장 크게 오른 게임 광고입니다.*

[![신규 광고: 새로 발견된 게임 광고를 초기 인기도순으로 보여 줍니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/new-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/new-ads.jpg)

*신규 광고: 새로 발견된 게임 광고를 초기 인기도순으로 보여 줍니다.*

[![개요: Vita Mahjong 광고의 형식과 예상 노출 수를 확인할 수 있습니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/overview.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/overview.jpg)

*개요: Vita Mahjong 광고의 형식과 예상 노출 수를 확인할 수 있습니다.*

[![데이터 추이: Vita Mahjong의 일별 광고 점수를 기준선과 비교할 수 있습니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/data-trend.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/data-trend.jpg)

*데이터 추이: Vita Mahjong의 일별 광고 점수를 기준선과 비교할 수 있습니다.*

[![관련 광고: 같은 소재를 사용한 광고주와 집행 기간을 비교할 수 있습니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/related-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/related-ads.jpg)

*관련 광고: 같은 소재를 사용한 광고주와 집행 기간을 비교할 수 있습니다.*

[![잠재고객: 국가 및 지역, 연령, 성별에 따른 도달 규모를 확인할 수 있습니다.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/audience.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/audience.jpg)

*잠재고객: 국가 및 지역, 연령, 성별에 따른 도달 규모를 확인할 수 있습니다.*

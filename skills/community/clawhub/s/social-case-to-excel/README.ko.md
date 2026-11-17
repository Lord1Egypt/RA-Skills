# social-case-to-excel

소셜 게시물을 출처를 확인할 수 있는 사례집, 방법 분석, 이미지가 포함된 조사 문서로 정리하는 skill입니다.

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## 어떤 조사에 활용하는가

이 워크플로로 브랜드의 해외 진출 초기 이력, 소셜 운영 사례, 댓글에 나타난 고객 요구를 정리했습니다. 누가 무엇을 했는지에 더해 공개된 성과, 실행 단계, 필요한 조건, 다른 브랜드의 적용 방법을 분석합니다.

기기 브랜드는 조사 대상의 한 예입니다. AI 광고, 제품 출시, 크로스보더 커머스, 콘텐츠 운영 등도 주제를 지정해 조사할 수 있습니다.

| 결과물 | 내용 |
| --- | --- |
| Excel 사례집 | 주체, 행동, 보고된 성과, 날짜, 원문 링크, 분류와 증거의 한계 |
| 방법 분석 | 실행 단계, 전제 조건, 브랜드별 적용 방안 |
| 이미지와 스크린샷 | 해당 게시물의 이미지, 영상 표지 또는 스크린샷과 출처 설명 |
| 학습 문서 | 발견, 사례, 방법을 연결한 Markdown. 필요하면 HTML도 제공 |
| 후보 데이터 | 검색 범위와 제외된 기록을 보존해 검토와 추가 조사에 활용 |

## 사례: 중국 브랜드의 해외 진출 첫해 되짚기

과거 조사에서는 OnePlus, Anker, Bambu Lab, Keychron, Snapmaker, EcoFlow 등 6개 브랜드의 사건 44건을 정리했습니다. 출시 전 활동, 시작 후 첫해의 기록, 기타 초기 단서를 구분하고 공식 계정뿐 아니라 언론, 커뮤니티 관리자, 사용자의 기록도 살펴봤습니다.

OnePlus에서는 관리자 접촉과 담당자 Q&A, Keychron에서는 크라우드펀딩 구매 후 Reddit에 공유한 순서, Bambu Lab에서는 실물 시연, 소재, 배송에 관한 질문이 확인됐습니다. 반응 수나 펀딩 금액을 곧바로 소셜 채널에서 발생한 매출로 보지는 않았습니다.

아래는 실제 납품한 Excel의 일부입니다. 모든 언어 버전에서 같은 중국어 화면을 사용합니다. 과거 사례의 플랫폼 범위가 현재 연결의 권한을 보장하지는 않습니다.

### 방법 분석

![방법 분석 예시](assets/readme/methods.png)

### 브랜드별 참고 방법

![브랜드 참고 예시](assets/readme/brand-reference.png)

### 참여자별 타임라인과 성과 근거

![타임라인 예시](assets/readme/timeline.png)

Excel 샘플은 [`outputs/`](outputs/)에 저장하며 각 파일의 실제 조사 주제를 소개합니다.

## 사용 방법

Agent가 지원하는 skills 디렉터리에 이 폴더를 설치하고 `$social-case-to-excel`을 호출하세요. 조사 주제, 대상 플랫폼, 기간, 사례 수를 지정합니다.

> 중국 브랜드 몇 곳의 해외 진출 초기 이력을 X와 Reddit에서 조사해주세요. 공식 계정, 언론, 사용자 기록을 구분하고 방법, 성과 근거, 품목별 적용 방안을 이미지가 포함된 Excel과 학습 문서로 정리해주세요.

Python Excel 생성에는 `openpyxl`, `Pillow`가 필요합니다. 스크립트는 조사마다 조정하는 템플릿입니다. 다른 플랫폼은 실행 환경에서 제공하는 ClaudeBaby 도구를 사용합니다.

## 데이터 연결

이 버전은 **ClaudeBaby**만 데이터 서비스로 사용합니다. Reddit, X, YouTube, Bilibili는 조사 대상 플랫폼이며 실제 범위는 제공되는 도구와 권한에 따라 달라집니다.

첫 사용 시 기존 ClaudeBaby MCP 연결과 대상 플랫폼의 기능을 확인하고, 설정이 없는 경우 등록 및 연결을 안내합니다.

```bash
python3 scripts/claudebaby_preflight.py          # 오프라인 설정 확인
python3 scripts/claudebaby_preflight.py --probe  # MCP 연결 및 도구 목록 확인
```

HTTP 클라이언트는 `CLAUDEBABY_MCP_URL`, `CLAUDEBABY_MCP_TOKEN`을 읽으며 기존 `REDDIT_MCP_*` 변수도 지원합니다. 콘솔의 접속 정보를 사용하고 토큰을 보고서나 저장소에 넣지 마세요.

원문 링크, 날짜, 증거의 한계를 남기고 작성자의 성과 주장과 조사자의 추론을 구분합니다. 영상 표지만으로 전체 영상을 검토했다고 판단하지 않습니다. 원본 미디어 권리는 각 권리자에게 있으며 재게시 전 사용 범위를 확인해야 합니다.

## ClaudeBaby와 프로젝트

[ClaudeBaby 초대 링크로 등록](https://claudebaby.cn/console/register?ref=M8YYGRN4) · 초대 코드: `M8YYGRN4`. 이 링크로 등록하면 초대 포인트를 받을 수 있습니다. 기존 사용자는 현재 연결을 그대로 사용할 수 있습니다.

이 skill이나 샘플이 조사에 도움이 되었다면 저장소에 ⭐ Star를 남겨주세요.

```text
social-case-to-excel/
├── SKILL.md
├── README.md / README.en.md / README.ja.md / README.ko.md
├── assets/readme/
├── outputs/
├── references/
└── scripts/
```

## Installation / 安装 / インストール / 설치

```bash
npx skills add lingling1989r/social-case-to-excel --skill social-case-to-excel
```

[GitHub](https://github.com/lingling1989r/social-case-to-excel) · [ZIP](https://github.com/lingling1989r/social-case-to-excel/archive/refs/heads/main.zip)

# 카카오 i 오픈빌더 연동 가이드

## 필요 환경변수

```
KAKAO_CALLBACK_SECRET=your-secret  # 선택사항 (보안 강화용)
```

## 설정 순서

1. **https://i.kakao.com** 에서 카카오 비즈니스 계정으로 봇 생성
2. 좌측 메뉴 "시나리오" → **"폴백 블록"** 선택
3. 블록 상세에서 "스킬" 탭 → **"스킬 서버 URL"** 에 입력:
   ```
   http://your-server:8400/kakao
   ```
4. (선택) 채널 연결: 카카오채널 관리자센터 → 봇 연결

## 로컬 테스트 (ngrok 사용)

```bash
# 1. Raon OS 서버 실행
python3 scripts/server.py --port 8400

# 2. ngrok으로 외부 노출
ngrok http 8400

# 3. ngrok이 출력한 URL/kakao 를 오픈빌더 스킬 서버 URL에 입력
# 예: https://abc123.ngrok.io/kakao
```

## 환경변수 설정

```bash
echo "KAKAO_CALLBACK_SECRET=옵션값" >> ~/.openclaw/.env
```

## 웹훅 테스트 (curl)

```bash
curl -X POST http://localhost:8400/kakao \
  -H "Content-Type: application/json" \
  -d '{
    "userRequest": {
      "utterance": "치킨집 창업하고 싶어요",
      "user": {"id": "test_user_001"}
    },
    "bot": {"id": "test_bot"},
    "intent": {"name": "폴백 블록"}
  }'
```

## 응답 형식 (카카오 오픈빌더 v2)

```json
{
  "version": "2.0",
  "template": {
    "outputs": [
      {"simpleText": {"text": "라온의 응답 텍스트"}}
    ],
    "quickReplies": [
      {"label": "융자/보증 알아보기", "action": "message", "messageText": "융자/보증 알아보기"},
      {"label": "지원사업 찾기", "action": "message", "messageText": "지원사업 찾기"},
      {"label": "처음부터", "action": "message", "messageText": "처음부터"}
    ]
  }
}
```

## 트랙 자동 감지

| 키워드 예시 | 감지 트랙 | 평가 기준 |
|------------|-----------|-----------|
| 치킨집, 카페, 음식점, 소상공인 | Track B | 입지/경험/차별화/자금/지역 (100점) |
| AI, SaaS, TIPS, 바이오, 반도체 | Track A | 기술성/시장성/사업성/팀역량 (100점) |
| 푸드테크, 뷰티테크, O2O | Track AB | Track B 기준 우선 적용 |

## 금융 상품 연동

사용자가 "대출", "보증", "융자", "자금" 등을 질문하면 자동으로 금융맵 매칭:

- **Track B**: 소상공인 정책자금(소진공), 청년창업 특례보증(KODIT), Wadiz 크라우드펀딩
- **Track A**: TIPS(중기부), 기술보증(KIBO), 청년창업 특례보증(KODIT)
- **Track AB**: 위 모두 포함

## 운영 주의사항

1. **카카오는 반드시 200 응답** — 에러도 정상 응답(simpleText)으로 반환
2. **텍스트 1000자 제한** — 자동으로 900자씩 분할 (최대 5개 outputs)
3. **빠른 응답 버튼 최대 5개** — 트랙별로 자동 설정
4. **세션 관리** — user.id 기반으로 대화 히스토리 유지 (최대 20턴)

---
name: Toss Payments CLI
slug: toss-payments-cli
version: 0.1.0
author: Chloe Park
license: MIT
summary: Minimal CLI for Toss Payments Core API — get payment details and cancel payments.
tags:
  - latest
  - payments
  - korea
  - api
  - cli
metadata:
  openclaw:
    requires:
      env:
        - TOSS_SECRET_KEY
    primaryEnv: TOSS_SECRET_KEY
---

# Toss Payments CLI

토스페이먼츠 코어 API를 간단히 호출하는 최소 CLI 스킬이다. `paymentKey`로 결제를 조회하고, 전체/부분 취소를 수행한다. 테스트/실서비스 키 모두 지원한다.

## Features
- GET /payments/{paymentKey}
- POST /payments/{paymentKey}/cancel (cancelReason, optional cancelAmount)

## Usage
```bash
export TOSS_SECRET_KEY="test_sk_xxx"

# 결제 조회
toss-pay get-payment --payment-key {paymentKey}

# 결제 취소 (전체/부분)
toss-pay cancel-payment --payment-key {paymentKey} --reason "고객 요청"
toss-pay cancel-payment --payment-key {paymentKey} --reason "부분 환불" --amount 5000
```

Base URL: https://api.tosspayments.com/v1 (환경변수 TOSS_BASE_URL로 오버라이드 가능)

## Install
```bash
pipx install .  # 또는 pip install .
```

## Docs
- Toss Payments Core API: https://docs.tosspayments.com/reference#tag/Payments

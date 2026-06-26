# ZapYeti API (OpenAPI 3.0.3)

Source: provided OpenAPI JSON (api-1---8a2ddfe7-5926-41d7-af4b-28fe6a875524.json)

Base URL: https://api.zapyeti.com (assumed from docs URL)

## Auth / Session
- GET /api/csrf-token
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh
- GET /api/auth/me
- POST /api/auth/register
- POST /api/auth/forgot-password
- POST /api/auth/verify-reset-code
- POST /api/auth/reset-password
- POST /api/auth/request-email-verification
- POST /api/auth/verify-email-code
- POST /api/auth/confirm-email-verification

## Debts
- GET /api/debts/
- POST /api/debts/ (create)
- GET /api/debts/{id}
- PUT /api/debts/{id} (update)
- DELETE /api/debts/{id}
- POST /api/debts/bulk
- POST /api/debts/{id}/link-simplefin
- PATCH /api/debts/{id}/balance

## Payments
- GET /api/payments/
- POST /api/payments/
- GET /api/payments/summary
- GET /api/payments/history
- GET /api/payments/{id}
- DELETE /api/payments/{id}

## Users
- GET /api/users/me
- GET /api/users/{id}
- PUT /api/users/{id}
- POST /api/users/

## Settings
- GET /api/settings/preferences
- PUT /api/settings/preferences
- GET /api/settings/profile
- PUT /api/settings/profile
- GET /api/settings/export
- GET /api/settings/export/csv
- DELETE /api/settings/account

## SimpleFin
- GET /api/simplefin/status
- POST /api/simplefin/connect
- POST /api/simplefin/disconnect
- POST /api/simplefin/sync
- GET /api/simplefin/accounts
- POST /api/simplefin/sync/{debtId}
- POST /api/simplefin/link
- POST /api/simplefin/unlink/{debtId}
- GET /api/simplefin/transactions/{debtId}
- GET /api/simplefin/unlinked-accounts

## Social
- POST /api/social/profile
- GET /api/social/profile
- POST /api/social/pods
- GET /api/social/pods
- POST /api/social/pods/{id}/join
- POST /api/social/check-in
- GET /api/social/feed
- POST /api/social/feed
- POST /api/social/feed/{id}/react
- GET /api/social/leaderboard

## API Keys
- GET /api/apikeys
- POST /api/apikeys
- DELETE /api/apikeys/{id}

## Admin
- GET /api/admin/dashboard
- GET /api/admin/check
- POST /api/admin/sync/all
- POST /api/admin/sync/user/{userId}
- GET /api/admin/sync/status

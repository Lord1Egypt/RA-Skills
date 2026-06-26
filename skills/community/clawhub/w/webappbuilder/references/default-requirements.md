# Neo App Mode Default Requirements

Use this default when user says "just build it".

- Stack: React + Vite + Tailwind + Express + MongoDB
- Architecture: MVC backend
- Auth: JWT (email/password)
- Roles: admin, user
- Core modules:
  - Authentication
  - Dashboard summary endpoint
  - One sample CRUD module (`items`)
- API prefix: `/api/v1`
- DB: MongoDB URI from env
- Extras:
  - Global error handler
  - Request logger middleware
  - Input validation placeholder

# Self-Host wger (Docker)

docker-compose.yml:
version: '3'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: wger
      POSTGRES_USER: wger
      POSTGRES_PASSWORD: pass
    volumes:
      - db_data:/var/lib/postgresql/data
  wger:
    image: wger/server:latest
    ports:
      - "8000:80"
    environment:
      DB_HOST: db
      DB_NAME: wger
      DB_USER: wger
      DB_PASS: pass
    depends_on:
      - db
volumes:
  db_data:

Run: docker compose up -d
Access: http://localhost:8000
API: http://localhost:8000/api/v2/
Secure with Tailscale/VPN.

# Déploiement — VPS Hostinger + Cloudflare

## Infrastructure actuelle

```
VPS : 72.62.30.28 (srv1406447.hstgr.cloud)
Container : openclaw-yyvg-openclaw-1
Workspace : /data/.openclaw/workspace/
Tunnel actif : https://truth-demonstrate-restore-calgary.trycloudflare.com
```

---

## Déploiement complet — étape par étape

### Étape 1 — Préparer les fichiers en local

```
mon-dashboard/
├── index.html
├── trading.html
├── signals.html
├── journal.html
└── assets/
    ├── logo.png
    └── og-image.png
```

### Étape 2 — Transférer sur le VPS

```bash
# Depuis ta machine locale
scp -r ./mon-dashboard/ root@72.62.30.28:/tmp/dashboard-upload/

# Sur le VPS — copier dans le workspace Wesley
ssh root@72.62.30.28
docker cp /tmp/dashboard-upload/. openclaw-yyvg-openclaw-1:/data/.openclaw/workspace/projects/wesley-dashboard/
```

### Étape 3 — Lancer le serveur de fichiers statiques (port 8765)

```bash
# Vérifier si déjà actif
docker exec openclaw-yyvg-openclaw-1 ps aux | grep python

# Lancer le serveur statique
docker exec -d openclaw-yyvg-openclaw-1 sh -c \
  'cd /data/.openclaw/workspace/projects/wesley-dashboard && python3 -m http.server 8765'
```

### Étape 4 — Lancer dashboard_api.py (port 8766)

```bash
# Vérifier si déjà actif
docker exec openclaw-yyvg-openclaw-1 ps aux | grep dashboard_api

# Lancer l'API
docker exec -d openclaw-yyvg-openclaw-1 sh -c \
  'cd /data/.openclaw/workspace && python3 api/dashboard_api.py 2>/workspace/logs/api.log &'

# Vérifier
curl http://72.62.30.28:8766/health
# Réponse attendue : {"status": "ok", "uptime": ...}
```

### Étape 5 — Ouvrir les ports dans docker-compose.yml

```bash
# Sur l'hôte VPS
nano /docker/openclaw-yyvg/docker-compose.yml
```

Ajouter sous `ports:` :
```yaml
ports:
  - "62361:62361"   # OpenClaw UI (existant)
  - "8765:8765"     # Dashboard statique (AJOUTER)
  - "8766:8766"     # Dashboard API (AJOUTER)
```

```bash
# Redémarrer pour appliquer
cd /docker/openclaw-yyvg
docker compose down && docker compose up -d
```

### Étape 6 — Configurer le tunnel Cloudflare

#### Option A — Tunnel temporaire (déjà actif)
```bash
# Vérifier le tunnel actif
docker exec openclaw-yyvg-openclaw-1 ps aux | grep cloudflared

# Si pas actif — lancer un nouveau tunnel
docker exec -d openclaw-yyvg-openclaw-1 cloudflared tunnel --url http://localhost:8765

# Wesley récupère l'URL et t'envoie le lien
```

#### Option B — Tunnel nommé permanent (recommandé)

```bash
# 1. Créer le tunnel (une seule fois)
cloudflared tunnel create wesley-dashboard

# 2. Configurer ~/.cloudflared/config.yml
tunnel: <ID-DU-TUNNEL>
credentials-file: /root/.cloudflared/<ID>.json
ingress:
  - hostname: dashboard.ton-domaine.com
    service: http://localhost:8765
  - hostname: api.ton-domaine.com
    service: http://localhost:8766
  - service: http_status:404

# 3. Lancer comme service permanent
cloudflared tunnel run wesley-dashboard

# 4. Ajouter DNS dans Cloudflare dashboard
# dashboard.ton-domaine.com → CNAME → <ID>.cfargotunnel.com
```

---

## Auto-lancement au démarrage (systemd dans le container)

```bash
# Créer un script de démarrage
docker exec openclaw-yyvg-openclaw-1 sh -c 'cat > /start-dashboard.sh << '"'"'EOF'"'"'
#!/bin/bash
sleep 10  # attendre que le container soit prêt
cd /data/.openclaw/workspace/projects/wesley-dashboard
python3 -m http.server 8765 &
cd /data/.openclaw/workspace
python3 api/dashboard_api.py --port 8766 &
echo "Dashboard started" >> /data/.openclaw/workspace/logs/startup.log
EOF
chmod +x /start-dashboard.sh'
```

Ajouter dans `docker-compose.yml` :
```yaml
command: sh -c "/start-dashboard.sh & /original-start-command"
```

---

## Mise à jour du dashboard (sans coupure)

```bash
# Depuis ta machine locale
scp index.html root@72.62.30.28:/tmp/new-index.html

# Sur le VPS — remplacer à chaud
docker cp /tmp/new-index.html openclaw-yyvg-openclaw-1:/data/.openclaw/workspace/projects/wesley-dashboard/index.html

# Pas besoin de restart — HTTP server sert le nouveau fichier immédiatement
```

---

## Vérification complète

```bash
# 1. Statique
curl http://72.62.30.28:8765/
# Réponse : code HTML du dashboard

# 2. API health
curl http://72.62.30.28:8766/health
# Réponse : {"status":"ok","uptime":"Xh Xmin"}

# 3. API portfolio
curl http://72.62.30.28:8766/portfolio
# Réponse : JSON avec total_value, daily_pnl, etc.

# 4. Tunnel public
curl https://truth-demonstrate-restore-calgary.trycloudflare.com/
# Réponse : code HTML du dashboard

# 5. API depuis le dashboard (dans browser console)
fetch('http://72.62.30.28:8766/health').then(r=>r.json()).then(console.log)
```

---

## Problèmes courants

| Problème | Cause | Fix |
|---|---|---|
| Dashboard blanc | API offline | Vérifier demo fallback dans le JS |
| CORS error | API bloque les requêtes cross-origin | Ajouter `flask-cors` + `CORS(app)` dans dashboard_api.py |
| Tunnel down | Cloudflare timeout | Relancer `cloudflared tunnel` |
| Port fermé | docker-compose pas à jour | Ajouter le port + `down && up -d` |
| Photos pas sauvées | localStorage plein | Réduire max photos ou utiliser l'API |

### Fix CORS (important si API et dashboard sur ports différents)
```python
# Dans dashboard_api.py — ajouter en haut
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=['*'])  # ou limiter aux URLs Cloudflare
```
```bash
docker exec openclaw-yyvg-openclaw-1 pip3 install flask-cors --break-system-packages
```

---

## Dashboard URL stable — à partager

```
URL publique : https://truth-demonstrate-restore-calgary.trycloudflare.com

Partager sur :
- Telegram (description du canal public)
- Bio X/Twitter
- Description Reddit
- Landing page VIP (lien "Voir les performances live →")
```

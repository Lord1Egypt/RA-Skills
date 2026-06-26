---
name: wesley-dashboard-builder
description: >
  Skill de création de dashboards live, sites web complets, et pages de preuve sociale pour Wesley-Agent.
  Déclencher dès que Georges mentionne : dashboard, site web, landing page, page de signaux, galerie photos,
  preuve de performance, page VIP, page publique, portfolio tracker, ou veut afficher des données en temps réel.
  Ce skill produit des fichiers HTML/CSS/JS complets — multi-écrans, médias intégrés (images/vidéos),
  connexion API live, mobile-first, shareable via tunnel Cloudflare.
  Toujours utiliser ce skill pour toute création web impliquant Wesley, ses signaux, ou ses performances.
requires:
  env:
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID
primaryEnv: TELEGRAM_BOT_TOKEN
network_behavior:
  description: >
    Sert des fichiers HTML statiques via HTTP. Se connecte à dashboard_api.py local (port 8766)
    pour les données en temps réel. Optionnel : upload photos via Telegram bot API.
  request_targets:
    - http://localhost:8766 (API Wesley interne — données live)
    - https://api.telegram.org (photos depuis Telegram — requires TELEGRAM_BOT_TOKEN)
---

# Wesley Dashboard Builder

Skill de création de dashboards et sites web complets pour Wesley-Agent.
Produit des fichiers HTML/CSS/JS prêts à déployer sur le VPS via tunnel Cloudflare.

## Philosophie

**Chaque dashboard = un produit marketing.**
- Home/Proof → preuve sociale → convertit en VIP
- Trading → crédibilité trader sérieux
- Signaux → valeur visible → justifie le prix
- Journal → engagement → fidélise

Lire les références dans l'ordre selon le besoin :
- **Architecture et API** → `references/api-architecture.md`
- **Design et CSS** → `references/design-system.md`
- **Médias (images/vidéos)** → `references/media-integration.md`
- **Déploiement VPS** → `references/deployment.md`

---

## Structure standard d'un projet dashboard

```
workspace/projects/MON-DASHBOARD/
├── index.html          ← écran 1 (Home / Proof)
├── trading.html        ← écran 2 (Performance & trades)
├── signals.html        ← écran 3 (Feed signaux live + CTA VIP)
├── journal.html        ← écran 4 (Photos / Timeline / Milestones)
├── assets/
│   ├── logo.png
│   └── og-image.png    ← pour partage réseaux sociaux
└── api_server.py       ← si dashboard_api.py pas encore lancé
```

---

## Workflow de création

### Étape 1 — Déterminer le type de dashboard

| Type demandé | Fichiers à créer | Référence |
|---|---|---|
| Dashboard complet (4 écrans) | index + trading + signals + journal | Tout |
| Landing page / site vitrine | index.html uniquement | design-system.md |
| Page signaux publique | signals.html | api-architecture.md |
| Galerie preuve sociale | journal.html | media-integration.md |
| Dashboard embarqué (iframe) | Composant autonome | design-system.md |

### Étape 2 — Lire la référence design

→ `references/design-system.md` : variables CSS, typographie, composants, animations

### Étape 3 — Générer les fichiers HTML

Chaque fichier HTML = autonome (CSS + JS inline, zéro dépendance locale).
Imports autorisés via CDN seulement :
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
```

### Étape 4 — Connecter l'API

→ `references/api-architecture.md` : endpoints disponibles, fallback demo data

### Étape 5 — Intégrer médias

→ `references/media-integration.md` : images, vidéos, upload Telegram, OG tags

### Étape 6 — Déployer

→ `references/deployment.md` : copier sur VPS, lancer API, configurer tunnel

---

## Écrans standard — description rapide

### Écran 1 — Home / Proof (`index.html`)
- Portfolio value live avec animation compteur
- P&L du jour en vert/rouge
- Statut agents (dots qui pulsent)
- Dernier signal posté
- Barre de progression vers objectif mensuel
- Uptime système
- Bouton screenshot pour partage Instagram/X

### Écran 2 — Trading (`trading.html`)
- Courbe equity (Chart.js, 7j/30j/all)
- Win rate en anneau (donut chart)
- Positions ouvertes : marché + odds + edge %
- Derniers trades : ✅ win / ❌ loss
- Métriques : Sharpe, drawdown, avg hold

### Écran 3 — Signaux (`signals.html`)
- Feed des derniers signaux (style Twitter)
- Score EDGE / Confiance / Marché / Heure
- Badge FREE vs 🔒 VIP
- CTA sticky en bas : "Rejoindre le canal VIP →"
- Auto-refresh toutes les 30s

### Écran 4 — Journal / Proof (`journal.html`)
- Upload photos depuis téléphone (drag & drop ou bouton)
- Galerie timeline : date + caption
- Milestones : "Semaine 1 : +$22 → Objectif : +$200"
- Lightbox pour voir les photos en grand
- Photos reçues via Telegram → affichées automatiquement

---

## Règles de génération de code

1. **Tout inline** — CSS dans `<style>`, JS dans `<script>`, jamais de fichiers séparés
2. **Mobile-first** — grid responsive, font-size fluide, touch-friendly
3. **Fallback demo data** — si API offline, données demo réalistes s'affichent
4. **Navigation** — barre bottom mobile (4 icônes) + sidebar desktop
5. **Dark theme obligatoire** — fond #020608 ou similaire (voir design-system.md)
6. **Pas de framework** — HTML/CSS/JS vanilla uniquement (sauf Chart.js CDN)
7. **Meta OG** — chaque page a ses balises pour le partage
8. **CTA VIP** — toujours présent sur signals.html et index.html

---

## Checklist avant livraison

- [ ] Fichiers autonomes (zéro dépendance locale)
- [ ] Test sur mobile (viewport 375px)
- [ ] Fallback demo data fonctionnel
- [ ] Navigation entre écrans opérationnelle
- [ ] API fetch avec timeout et error handling
- [ ] Upload photo fonctionne (FileReader API)
- [ ] Meta tags OG pour partage
- [ ] CTA VIP visible sur mobile
- [ ] Instructions déploiement fournies

---

## Commandes de déploiement rapide

```bash
# Copier les fichiers sur le VPS
scp -r ./MON-DASHBOARD/ root@72.62.30.28:/docker/openclaw-yyvg/data/.openclaw/workspace/projects/

# Lancer l'API Wesley sur port 8766
docker exec -d openclaw-yyvg-openclaw-1 python3 /data/.openclaw/workspace/api/dashboard_api.py --port 8766

# Vérifier que ça tourne
curl http://72.62.30.28:8766/health

# Ouvrir le dashboard (tunnel Cloudflare doit être actif)
# URL : https://truth-demonstrate-restore-calgary.trycloudflare.com
```

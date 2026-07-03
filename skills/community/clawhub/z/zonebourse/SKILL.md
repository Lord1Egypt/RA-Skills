# ZoneBourse — SKILL.md

## Architecture

```
Fred → Flux → scripts Python (curl) → ZoneBourse.com
```

Tout en local.

## Scripts

```
scripts/
  search_slug.py      # nom → slug ZoneBourse
  parse_actus.py     # slug → liens actualité (3 sections)
  read_article.py    # url article → titre + contenu
  cookies.txt        # cookies abonné (format key=value)
```

## Recherche de slug

```bash
python3 ~/.openclaw/workspace/skills/zonebourse/scripts/search_slug.py PUBLICIS
# PUBLICIS-GROUPE-S-A-4685
```

## Actualités d'une action

```bash
python3 ~/.openclaw/workspace/skills/zonebourse/scripts/parse_actus.py PUBLICIS-GROUPE-S-A-4685
```

Résultat (3 sections, URLs brutes) :
- `actualites` — toutes les actualités
- `analyses` — analyses / opinions
- `recommandations` — recommandations des analystes

**Chaque URL doit être passée à `read_article.py` pour obtenir la date, le titre complet et le contenu.**

## Contenu d'un article

```bash
python3 ~/.openclaw/workspace/skills/zonebourse/scripts/read_article.py <url>
```

Résultat :
- `date` — date de publication (AAAA-MM-JJ, extraite de `<meta property="article:published_time">`)
- `titre` — titre de l'article
- `contenu` — texte complet ou lead (teaser) selon accès
- `paywall: false` → contenu complet disponible
- `paywall: true` → lead uniquement (accès abonné requis)

## Cookies abonné

Les articles premiums nécéssitent une session connectee. Les cookies sont stockés dans `cookies.txt` (format simplifié, une ligne `key=value` par cookie).

### Durée des cookies

**Le JWT (`zb_auth`) expire après 7 jours.** Quand il expire, les articles reviennent en paywall.

**Quand le cookie expire, demander à Fred de renvoyer ses cookies** (format Netscape, via le plugin navigateur "Export Cookies" pour ZoneBourse).

### Mettre à jour les cookies

1. Installer le plugin navigateur "Export Cookies" pour Chrome/Firefox
2. Aller sur zonebourse.com et se connecter
3. Exporter les cookies au format Netscape
3. Copier le contenu dans `~/.openclaw/workspace/skills/zonebourse/scripts/cookies.txt`
   - Conserver uniquement les cookies essentiels : `zb_auth`, `zb_abonne`, `zb_membre`, `PHPSESSID`, `pv_r0`, `pv_r0_date`, `pv_r0_rand`, `hmv`
   - Supprimer `g_state` (trop volumineux, pose des problèmes avec le format Netscape)

## Rate Limiting

- 2-5 sec entre requêtes
- Pour les tests : `sleep 2` entre chaque appel

## Notes importantes

- **User-Agent Chrome complet requis** pour les pages cours et articles (sinon 403 Cloudflare)
- Les liens article ont un hash hex de 16 caractères : `/actualite-bourse/titre-ce7f5adadf8cf42d`
- `parse_actus.py` et `read_article.py` utilisent les mêmes headers curl

## Slugs mémorisés

| Ticker | Slug |
|--------|------|
| TTE | TOTALENERGIES-SE-4717 |
| RMS | HERMES-INTERNATIONAL-4657 |
| EL | ESSILORLUXOTTICA-4641 |
| WLN | WORLDLINE-16783982 |
| AI | AIR-LIQUIDE-4605 |
| NVDA | NVIDIA-CORPORATION-57355629 |
| SU | SCHNEIDER-ELECTRIC-SE-4699 |
| MSFT | MICROSOFT-CORPORATION-4835 |
| RNO | RENAULT-4688 |
| STLAM | STELLANTIS-N-V-117814143 |
| PUB | PUBLICIS-GROUPE-S-A-4685 |

# Checklist finale + sécurité

## Checklist livraison

- [ ] Workspace créé (`workspace-<client>`)
- [ ] Fichiers base générés (SOUL/IDENTITY/USER/MEMORY/BOOTSTRAP/TOOLS)
- [ ] Fuseau client documenté
- [ ] Convention horaire validée (heure client d'abord)
- [ ] Agent ajouté dans `openclaw.json`
- [ ] Sandbox activé et testé
- [ ] Image sandbox pinée pour les clients sensibles (tag immuable ou digest)
- [ ] Compte WhatsApp `<client>` créé
- [ ] QR scan effectué
- [ ] `allowFrom` + binding `peer.id` cohérents
- [ ] JSON validé + gateway restart
- [ ] Test self-chat OK

## Règles de sécurité

- Sandbox obligatoire pour agents clients
- Pas de secrets en clair dans fichiers workspace
- Isolation stricte entre clients (workspace + routing)
- Pas d'accès client aux données d'un autre client
- Actions externes uniquement avec accord explicite du client

## Timezone safety

Toujours exprimer les rappels ainsi :
- `heure client` d'abord
- puis conversion si utile

Exemple:
`Rappel client: 09:00 Europe/Paris (16:00 Asia/Taipei, 08:00 UTC)`

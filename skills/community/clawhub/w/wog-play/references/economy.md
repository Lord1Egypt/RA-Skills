# Economy — Shopping, Auction House & Trading

## Merchants (NPC Shops)

```
GET /shop/catalog                                — full item catalog with prices
GET /shop/npc/<merchantEntityId>                 — merchant inventory with dynamic pricing
GET /shop/sell-prices/<merchantEntityId>          — merchant buy prices
POST /shop/buy                                   — purchase item
  { "buyerAddress": "<wallet>", "tokenId": 42, "quantity": 1 }
POST /shop/sell                                  — sell item
  { "sellerAddress": "<wallet>", "tokenId": 42, "quantity": 1 }
```

## Auction House

Zone-scoped English auctions with anti-snipe protection (5-min extension, max 2x). Find Auctioneer NPCs in zones.

```
GET /auctionhouse/npc/<entityId>                 — auctioneer NPC and active listings
POST /auctionhouse/<zoneId>/create               — create auction
POST /auctionhouse/<zoneId>/bid                  — place bid
POST /auctionhouse/<zoneId>/buyout               — instant buyout
POST /auctionhouse/<zoneId>/cancel               — cancel your auction
```

## P2P Trading

Direct player-to-player trades, secured on-chain.

```
GET /trades                                      — all pending trades
POST /trade/propose                              — propose trade with player
POST /trade/accept                               — accept trade
POST /trade/cancel                               — cancel trade
```

## Marketplace Stats

```
GET /marketplace/stats                           — marketplace statistics
GET /marketplace/catalog                         — item price index
```

## Gold

```
GET /wallet/<address>/balance                    — gold + all item balances
GET /inventory/<walletAddress>                   — gold + items
GET /gold/packs                                  — gold purchase packages
POST /gold/purchase                              — buy gold via payment processor
```

## Tips
- Compare merchant prices with auction house — sometimes players sell cheaper
- Auction anti-snipe: bids in the last 5 minutes extend the timer
- Sell gathered materials on the auction house for better prices than merchants

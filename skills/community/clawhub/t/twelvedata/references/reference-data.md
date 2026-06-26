# Twelve Data LLM Reference
> Last synced: 2026-03-29 20:21:13 UTC

# Reference data

Lookup static metadata—symbol lists, exchange details, currency information-to filter, validate, and contextualize your core data calls. Ideal for building dropdowns, mappings, and ensuring data consistency.

## Asset catalogs

Asset Catalog endpoints are your starting point. They return the complete inventory of tradeable instruments available through Twelve Data — over 1,000,000 symbols across 50+ countries. You query a catalog first to discover which symbols exist, then pass those symbols to price, fundamental, or indicator endpoints.

- [/stocks](https://twelvedata.com/docs/llms/asset-catalogs/stocks-list.md): Stocks

- [/forex_pairs](https://twelvedata.com/docs/llms/asset-catalogs/forex-pairs-list.md): Forex pairs

- [/cryptocurrencies](https://twelvedata.com/docs/llms/asset-catalogs/cryptocurrencies-list.md): Cryptocurrency pairs

- [/etfs](https://twelvedata.com/docs/llms/asset-catalogs/etf-list.md): ETFs

- [/funds](https://twelvedata.com/docs/llms/asset-catalogs/funds-list.md): Funds

- [/commodities](https://twelvedata.com/docs/llms/asset-catalogs/commodities-list.md): Commodities

- [/bonds](https://twelvedata.com/docs/llms/asset-catalogs/bonds-list.md): Fixed income


## Discovery

Discovery endpoints help you find instruments when you don't already know the exact identifier. The Asset Catalog is the phone book; Discovery is the search engine on top of it.

- [/symbol_search](https://twelvedata.com/docs/llms/discovery/symbol-search.md): Symbol search

- [/cross_listings](https://twelvedata.com/docs/llms/discovery/cross-listings.md): Cross listings

- [/earliest_timestamp](https://twelvedata.com/docs/llms/discovery/earliest-timestamp.md): Earliest timestamp


## Markets

Market endpoints answer operational questions about exchanges themselves: which ones are open right now, what are their trading hours, and how far back does data go for a given instrument?

- [/exchanges](https://twelvedata.com/docs/llms/markets/exchanges.md): Exchanges

- [/exchange_schedule](https://twelvedata.com/docs/llms/markets/exchange-schedule.md): Exchanges schedule

- [/cryptocurrency_exchanges](https://twelvedata.com/docs/llms/markets/cryptocurrency-exchanges.md): Cryptocurrency exchanges

- [/market_state](https://twelvedata.com/docs/llms/markets/market-state.md): Market state


## Supporting metadata

Metadata endpoints return the lookup tables and enumerations that define valid parameter values across the entire API. They answer: what instrument types exist? What intervals are supported? Which countries are covered? What technical indicators can I use?

- [/countries](https://twelvedata.com/docs/llms/supporting-metadata/countries.md): Countries

- [/instrument_type](https://twelvedata.com/docs/llms/supporting-metadata/instrument-type.md): Instrument type

- [/technical_indicators](https://twelvedata.com/docs/llms/supporting-metadata/technical-indicators-interface.md): Technical indicators




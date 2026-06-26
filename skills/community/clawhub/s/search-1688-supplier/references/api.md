# AlphaShop AI Select Provider Search API

## Endpoint

`POST https://api.alphashop.cn/ai.select.provider.search/1.0`

## Auth

`Authorization: Bearer <ALPHASHOP_API_KEY>`

## Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| intention | String | Y | AUTO / SEARCH_OFFER / SEARCH_PROVIDER |
| query | String | N* | Search text |
| searchImageUrl | String | N* | Public image URL |

*query and searchImageUrl cannot both be empty.

## Response Structure

`realIntention` determines which result field to use:

| realIntention | Result Field |
|---------------|-------------|
| SEARCH_OFFER | offerInfo → offerList (SpOfferInfoDTO[]) |
| SEARCH_PROVIDER | providerInfo → providerList (SpProviderInfoDTO[]) |
| DIRECT_SEARCH_PROVIDER | chatResponse (markdown string) |
| OTHER | chatResponse (plain string) |

## Key Data Structures

### SpOfferInfoDTO (offer in offerList)

- itemId, title, imageUrl, itemPrice, offerDetailUrl
- providerInfo: { companyName, factoryUrl, providerTags[] }
- aiAttentions[], satisfyRequirements[]
- salesInfos[], coreAttributes[], purchaseInfos[], shipInfos[]
- providerServices[], providerKjCustomTags[]

### SpProviderInfoDTO (provider in providerList)

- companyName, factoryUrl, loginId, mainCategoryName
- providerTags[], providerKjCustomTags[], aiAttentions[]
- satisfyRequirements[], providerServices[]
- recommendItems[]: { itemId, title, offerDetailUrl, imageUrl, itemPrice }

### SpTagDTO

- tagName, tagStyle (SUPER_FACTORY / SOURCE_FACTORY / POWER_FACTORY / GENERAL)

### SpLabelDTO (used in salesInfos, purchaseInfos, shipInfos, etc.)

- label (field name), value (field data)

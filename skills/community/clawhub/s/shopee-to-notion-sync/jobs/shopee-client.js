const axios = require("axios");
const crypto = require("crypto");
const { shopeeAppId, shopeeSecret } = require("./config");

const SHOPEE_URL = "https://open-api.affiliate.shopee.com.br/graphql";

function gerarTimestamp() {
  return Math.floor(Date.now() / 1000).toString();
}

function gerarSignature(appId, timestamp, payload, secret) {
  const base = appId + timestamp + payload + secret;
  return crypto.createHash("sha256").update(base).digest("hex");
}

async function buscarProdutosShopee(keyword, limit = 10) {
  const query = `
    {
      productOfferV2(keyword: "${keyword}", listType: 1, sortType: 2, page: 1, limit: ${limit}) {
        nodes {
          itemId
          productName
          productLink
          offerLink
          imageUrl
          priceMin
          priceMax
          commissionRate
          commission
          shopId
          shopName
          shopType
        }
        pageInfo {
          page
          limit
          hasNextPage
        }
      }
    }
  `;

  const body = JSON.stringify({ query });
  const timestamp = gerarTimestamp();
  const signature = gerarSignature(shopeeAppId, timestamp, body, shopeeSecret);
  const authorization = `SHA256 Credential=${shopeeAppId},Timestamp=${timestamp},Signature=${signature}`;

  const response = await axios.post(SHOPEE_URL, JSON.parse(body), {
    headers: {
      "Content-Type": "application/json",
      Authorization: authorization,
    },
  });

  return response.data?.data?.productOfferV2?.nodes || [];
}

module.exports = {
  buscarProdutosShopee,
};
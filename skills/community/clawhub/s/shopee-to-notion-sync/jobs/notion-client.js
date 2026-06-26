const axios = require("axios");
const { notionToken, notionVersion } = require("./config");

function criarHeadersNotion() {
  return {
    Authorization: `Bearer ${notionToken}`,
    "Notion-Version": notionVersion,
    "Content-Type": "application/json",
  };
}

function montarProperties(produto) {
  return {
    id: {
      number: Number(produto.itemId || 0),
    },
    nome: {
      title: [
        {
          text: {
            content: produto.productName || "Sem nome",
          },
        },
      ],
    },
    valor: {
      number: Number(produto.priceMin || 0),
    },
    "valor da comissão": {
      number: Number(produto.commission || 0),
    },
    categoria: {
      select: {
        name: "Shopee",
      },
    },
    "url da imagem": {
      url: produto.imageUrl || null,
    },
    "link do produto": {
      url: produto.productLink || null,
    },
  };
}

async function buscarPaginaExistentePorId(databaseId, itemId) {
  const response = await axios.post(
    `https://api.notion.com/v1/databases/${databaseId}/query`,
    {
      filter: {
        property: "id",
        number: {
          equals: Number(itemId),
        },
      },
      page_size: 1,
    },
    {
      headers: criarHeadersNotion(),
    }
  );

  return response.data?.results?.[0] || null;
}

async function criarPaginaNoNotion(databaseId, produto) {
  const payload = {
    parent: {
      database_id: databaseId,
    },
    properties: montarProperties(produto),
  };

  const response = await axios.post(
    "https://api.notion.com/v1/pages",
    payload,
    {
      headers: criarHeadersNotion(),
    }
  );

  return response.data;
}

async function atualizarPaginaNoNotion(pageId, produto) {
  const response = await axios.patch(
    `https://api.notion.com/v1/pages/${pageId}`,
    {
      properties: montarProperties(produto),
    },
    {
      headers: criarHeadersNotion(),
    }
  );

  return response.data;
}

async function upsertProdutoNoNotion(databaseId, produto) {
  const existente = await buscarPaginaExistentePorId(databaseId, produto.itemId);

  if (existente) {
    await atualizarPaginaNoNotion(existente.id, produto);
    return {
      acao: "atualizado",
      nome: produto.productName,
      itemId: produto.itemId,
    };
  }

  await criarPaginaNoNotion(databaseId, produto);
  return {
    acao: "criado",
    nome: produto.productName,
    itemId: produto.itemId,
  };
}

module.exports = {
  upsertProdutoNoNotion,
};
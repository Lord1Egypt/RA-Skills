const { buscarProdutosShopee } = require("./shopee-client");
const { upsertProdutoNoNotion } = require("./notion-client");
const { getTargetDatabaseId } = require("./config");

function parseArgs() {
  const keyword = process.argv[2] || "celular";
  const limit = Number(process.argv[3] || 10);
  const target = process.argv[4] || "shopee_produtos";

  return { keyword, limit, target };
}

async function executar() {
  const { keyword, limit, target } = parseArgs();
  const databaseId = getTargetDatabaseId(target);

  console.log(`Target selecionado: ${target}`);
  console.log(`Database ID: ${databaseId}`);
  console.log(`Buscando produtos da Shopee para "${keyword}"...`);

  const produtos = await buscarProdutosShopee(keyword, limit);

  if (!produtos.length) {
    console.log(`Nenhum produto encontrado para "${keyword}".`);
    return;
  }

  let criados = 0;
  let atualizados = 0;
  let falhas = 0;

  for (const produto of produtos) {
    try {
      const resultado = await upsertProdutoNoNotion(databaseId, produto);

      if (resultado.acao === "criado") criados++;
      if (resultado.acao === "atualizado") atualizados++;

      console.log(
        `${resultado.acao.toUpperCase()}: ${resultado.nome} (ID: ${resultado.itemId})`
      );
    } catch (error) {
      falhas++;
      console.error(
        `Erro ao processar ${produto.productName}:`,
        error.response?.data || error.message
      );
    }
  }

  console.log(
    `Finalizado. Criados: ${criados}, Atualizados: ${atualizados}, Falhas: ${falhas}`
  );
}

executar().catch((err) => {
  console.error("Erro geral:", err.response?.data || err.message);
  process.exit(1);
});
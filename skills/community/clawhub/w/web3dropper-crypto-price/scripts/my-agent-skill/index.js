const axios = require("axios");

async function getBTCPrice() {
  try {
    const res = await axios.get(
      "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    );
    console.log("BTC Price:", res.data.price);
  } catch (err) {
    console.error("Error fetching price:", err.message);
  }
}

getBTCPrice();

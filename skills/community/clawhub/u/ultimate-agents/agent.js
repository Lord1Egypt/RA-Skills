const axios = require("axios");

console.log("🚀 Farming Agent Start");

// fungsi random
function randomTask() {
  const tasks = ["ping", "api", "log"];
  const pick = tasks[Math.floor(Math.random() * tasks.length)];

  if (pick === "ping") {
    console.log("📡 Ping network...");
  }

  if (pick === "api") {
    axios.get("https://api.coingecko.com/api/v3/ping")
      .then(() => console.log("🌐 API success"))
      .catch(() => console.log("❌ API fail"));
  }

  if (pick === "log") {
    console.log("🧠 Agent thinking...");
  }
}

// jalan random tiap 5–10 detik
function loop() {
  const delay = Math.floor(Math.random() * 5000) + 5000;

  setTimeout(() => {
    randomTask();
    loop();
  }, delay);
}

loop();
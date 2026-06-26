import { createRapidApiSkill } from "../index.js";

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

const inputRaw = await readStdin();
if (!inputRaw) {
  console.error("Expected JSON input via stdin");
  process.exit(2);
}

let input;
try {
  input = JSON.parse(inputRaw);
} catch (err) {
  console.error("Invalid JSON input");
  process.exit(2);
}

const { action, params, rapidapi } = input;
const skill = await createRapidApiSkill();

if (action) {
  const result = await skill.callAction(action, params || {});
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.ok ? 0 : 1);
}

if (rapidapi) {
  const result = await skill.callRapidApi(rapidapi);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.ok ? 0 : 1);
}

console.error("Input must include either 'action' or 'rapidapi'");
process.exit(2);

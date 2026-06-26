import { createRapidApiSkill } from "../index.js";

const skill = await createRapidApiSkill();
const actions = skill.listActions();

console.log(JSON.stringify({ ok: true, actions }, null, 2));

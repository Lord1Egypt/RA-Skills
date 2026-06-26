/**
 * Dynamic Tool Policy — intent-based tool recommendation.
 * Maps user message keywords to recommended OpenClaw tool names.
 * Use with Feishu + Ollama (or similar) to reduce context and avoid tool loops.
 */

function selectToolNamesFromText(userText, maxTools = 8) {
	const t = (userText || "").toLowerCase();
	const selected = new Set();
	selected.add("exec");
	if (/天气|温度|华氏|摄氏|weather|wttr|temperature|temp\s*[\(\（]/.test(t) || /^\s*\d+\s*[度°]\s*/.test(t)) selected.add("exec");
	if (/文档|创建\s*文档|飞书文档|create\s*doc|feishu\s*doc|doc\s*link/.test(t)) selected.add("feishu_doc");
	if (/搜索|查找|search|web_search|搜一下/.test(t)) selected.add("web_search");
	if (/读取|读文件|read\s*file|打开文件/.test(t)) selected.add("read");
	if (/写入|编辑文件|write\s*file|edit\s*file/.test(t)) selected.add("write");
	if (/多维表格|bitable|基矩表|base\s*url/.test(t)) {
		selected.add("feishu_bitable_create_app");
		selected.add("feishu_bitable_list_records");
	}
	if (/云盘|drive|文件夹|目录/.test(t)) selected.add("feishu_drive");
	if (/群聊|chat|成员|feishu_chat/.test(t)) selected.add("feishu_chat");
	if (/平台文档|wiki|知识/.test(t)) selected.add("feishu_wiki");
	return Array.from(selected).slice(0, maxTools);
}

function getHint(tools) {
	if (tools.includes("web_search")) return "User likely wants web search; use web_search once then reply. Do not call web_search again in the same turn.";
	if (tools.includes("feishu_doc")) return "User may want a Feishu document; only create when they explicitly ask for a doc.";
	if (tools.includes("exec") && tools.length <= 2) return "Weather or shell; use exec with wttr.in for weather.";
	return "Use only the recommended tools for this turn.";
}

export default {
	async get_recommended_tools({ user_message }, { config, memory }) {
		const recommended = selectToolNamesFromText(user_message || "", 8);
		const hint = getHint(recommended);
		return {
			recommended_tools: recommended,
			hint,
			message: "Recommendation based on keyword intent. For full filtering, use dmHistoryLimit (e.g. 20) and the system prompt from this skill's README.",
		};
	},
};

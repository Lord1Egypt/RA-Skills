import { startOfMonth, today } from "@bondli-skills/shared/date";
export async function capturePayload(page, reportConfig) {
    let payload = null;
    page.on("request", request => {
        if (request.url().includes(reportConfig.dataAPI)) {
            try {
                payload = JSON.parse(request.postData() || "");
            }
            catch (e) { }
        }
    });
    await page.goto(reportConfig.url, { waitUntil: "domcontentloaded" });
    await new Promise(r => setTimeout(r, 10000));
    const url = page.url();
    const loginKeywords = ["login", "signin", "passport", "sso"];
    const isLoginPage = loginKeywords.some(k => url.toLowerCase().includes(k));
    if (isLoginPage) {
        console.error("\n❌ 检测到未登录状态\n");
        console.error("当前URL:", url);
        console.error("请先在浏览器登录系统，然后重新运行程序\n");
        throw new Error("LOGIN_REQUIRED");
    }
    if (!payload) {
        throw new Error("未捕获到数据接口请求，请检查页面加载或接口是否变更");
    }
    return payload;
}
export async function requestAPI(page, api, payload) {
    payload.filters[0].filterValue.startTime = new Date(startOfMonth()).getTime();
    payload.filters[0].filterValue.endTime = new Date(today()).getTime();
    payload.filters[1].filterValue.startTime = new Date(startOfMonth()).getTime();
    payload.filters[1].filterValue.endTime = new Date(today()).getTime();
    console.log("正在执行二次查询,查询参数：", payload.filters[0].filterValue);
    const dataList = await page.evaluate(async (apiUrl, data) => {
        const res = await fetch(apiUrl, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        return json.data.dataList;
    }, api, payload);
    return dataList;
}
//# sourceMappingURL=api.js.map
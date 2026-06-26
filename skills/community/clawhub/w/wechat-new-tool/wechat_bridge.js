const axios = require('axios');
const express = require('express');
const app = express();
app.use(express.json());

// 配置信息
const CONFIG = {
    BASE_URL: "http://dashboard.synodeai.com/ai",
    APPID: process.env.WECHAT_APPID,
    TOKEN: process.env.WECHAT_TOKEN
};

// 基础请求封装
const wx = async (path, method, data = {}) => {
    return axios({
        url: `${CONFIG.BASE_URL}${path}`,
        method: method,
        headers: { 'Authorization': `Bearer ${CONFIG.TOKEN}` },
        params: method === 'GET' ? { appid: CONFIG.APPID, ...data } : { appid: CONFIG.APPID },
        data: method === 'POST' ? data : null
    });
};

// 1. 智能分发入口：负责查询与匹配
app.post('/wechat/dispatch', async (req, res) => {
    const { query, type, content, fileName } = req.body;

    try {
        // 并发查询好友和群聊
        const [friends, rooms] = await Promise.all([
            wx('/wechatTool/queryFriend', 'GET', { name: query }),
            wx('/wechatTool/queryChatroom', 'GET')
        ]);

        // 过滤匹配项
        let matches = [...(friends.data || [])];
        if (rooms.data) {
            const roomMatches = rooms.data.filter(r => r.nickname.includes(query));
            matches = matches.concat(roomMatches);
        }

        if (matches.length === 0) return res.json({ status: "error", msg: "未找到目标" });
        
        if (matches.length > 1) {
            return res.json({
                status: "need_choice",
                data: matches.map(m => ({ name: m.nickname || m.remark, wxId: m.wxId }))
            });
        }

        // 唯一匹配，进入待确认状态
        const target = matches[0];
        res.json({
            status: "confirm",
            target_id: target.wxId,
            target_name: target.nickname || target.remark,
            payload: { type, content, fileName }
        });
    } catch (e) {
        res.status(500).json({ status: "error", msg: "服务异常" });
    }
});

// 2. 最终发送执行
app.post('/wechat/confirm_send', async (req, res) => {
    const { target_id, type, content, fileName } = req.body;
    const mapping = {
        text: { path: '/wechatTool/sendText', body: { contact: target_id, content } },
        image: { path: '/wechatTool/sendImg', body: { contact: target_id, content } },
        file: { path: '/wechatTool/sendFile', body: { contact: target_id, fileUrl: content, fileName } }
    };

    const config = mapping[type];
    const result = await wx(config.path, 'POST', config.body);
    res.json({ status: "success", result: result.data });
});

app.listen(3000);
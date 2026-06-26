const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const TARGET_CHAT_ID = process.argv[2];
const content = process.argv[3];
const images = process.argv.slice(4);

const pendingDir = path.join(__dirname, '../pending_posts');
if (!fs.existsSync(pendingDir)) {
    fs.mkdirSync(pendingDir);
}

const id = `post_${Date.now()}`;
const payload = {
    id,
    content,
    images,
    timestamp: Date.now()
};

fs.writeFileSync(path.join(pendingDir, `${id}.json`), JSON.stringify(payload, null, 2));

// Upload images first to show them in approval card
let imageKeys = [];
if (images.length > 0) {
    try {
        for (const img of images) {
            const uploadCmd = `node skills/feishu-sender/upload_image.js "${img}"`;
            const rawOutput = execSync(uploadCmd).toString();
            const key = rawOutput.split('\n')
                .map(line => line.trim())
                .filter(line => line.startsWith('img_'))
                .pop();
            if (key) imageKeys.push(key);
        }
    } catch (e) {
        console.error('Failed to upload images for preview:', e);
    }
}

const cardContent = [
    [{ tag: "text", text: "📝 收到新的微博发布请求，需要审核：" }],
    [{ tag: "text", text: `\n内容：${content}`, style: ["bold"] }]
];

if (imageKeys.length > 0) {
    cardContent.push([{ tag: "text", text: "\n配图：" }]);
    for (const key of imageKeys) {
        cardContent.push([{ tag: "img", image_key: key }]);
    }
}

cardContent.push([
    { tag: "text", text: "\n请回复：\n" },
    { tag: "text", text: `"同意 ${id}"`, style: ["bold", "code"] }, // Instruction for user
    { tag: "text", text: " 或 " },
    { tag: "text", text: `"拒绝 ${id}"`, style: ["bold", "code"] }
]);

const msg = JSON.stringify({
    zh_cn: {
        title: "微博审核提醒 🚦",
        content: cardContent
    }
});

const sendCmd = `node skills/feishu-sender/send_post.js "${TARGET_CHAT_ID}" '${msg}'`;
try {
    execSync(sendCmd);
    console.log(`Request submitted with ID: ${id}`);
} catch (e) {
    console.error('Failed to send approval request:', e);
    process.exit(1);
}

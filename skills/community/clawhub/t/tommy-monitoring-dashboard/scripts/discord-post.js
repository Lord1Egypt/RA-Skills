
// OpenClaw session script for Discord integration
const dashboardMessage = `🤖 **OpenClaw Live Dashboard**\n\n🔄 **Active Subagents: 0**\n└─ All quiet\n\n⏰ **Cron Jobs**\n├─ Total active: 1\n└─ Recent:\n   └─ ID                    ... (active)\n\n📊 **System**\n├─ OpenClaw processes: 1\n├─ Dashboard: 🟢 Live\n└─ Updated: Thu, Mar 5, 12:39:38 AM PT`;

if (!process.env.LIVE_MESSAGE_ID) {
    // First time - post new message
    console.log('📝 Posting initial dashboard message...');
    
    const result = message({
        action: 'send',
        target: 'user:311529658695024640',
        message: dashboardMessage
    });
    
    if (result.ok) {
        console.log('✅ Dashboard posted, message ID:', result.result.messageId);
        // Store the message ID for future edits
        process.env.LIVE_MESSAGE_ID = result.result.messageId;
    }
} else {
    // Update existing message
    console.log('✏️ Updating dashboard message...');
    
    const result = message({
        action: 'edit', 
        messageId: process.env.LIVE_MESSAGE_ID,
        message: dashboardMessage
    });
    
    if (result.ok) {
        console.log('✅ Dashboard updated');
    } else {
        console.log('❌ Update failed:', result);
    }
}

console.log('Dashboard message prepared');

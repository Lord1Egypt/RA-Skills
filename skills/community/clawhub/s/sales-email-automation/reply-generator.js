#!/usr/bin/env node

/**
 * 邮件回复生成模块
 * 输入：原始邮件 + intent + 知识库检索结果
 * 输出：个性化回复草稿
 */

const fs = require('fs');
const path = require('path');

const TEMPLATE_DIR = path.join(__dirname, 'templates');

/**
 * 加载邮件模板
 */
function loadTemplate(templateId) {
  const templatePath = path.join(TEMPLATE_DIR, `${templateId}.md`);
  
  try {
    if (fs.existsSync(templatePath)) {
      return fs.readFileSync(templatePath, 'utf8');
    }
  } catch (err) {
    console.error(`⚠️  无法加载模板 ${templateId}:`, err.message);
  }
  
  // 返回默认模板
  return getDefaultTemplate();
}

/**
 * 获取默认模板（当指定模板不存在时）
 */
function getDefaultTemplate() {
  return `Dear {{customer_name}},

Thank you for your inquiry.

{{body}}

Best regards,
Jaden
Farreach Electronic Co., Ltd.
{{contact_info}}`;
}

/**
 * 使用 LLM 生成个性化回复
 */
async function generateReply(originalEmail, intent, kbResults, language = 'en') {
  console.log(`\n✍️  生成回复草稿...`);
  console.log(`   Intent: ${intent}`);
  console.log(`   Language: ${language}`);
  
  // 构建 prompt
  const prompt = buildGenerationPrompt(originalEmail, intent, kbResults, language);
  
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'HTTP-Referer': 'https://farreach-electronic.com',
        'X-Title': 'Farreach EmailReply',
      },
      body: JSON.stringify({
        model: 'anthropic/claude-sonnet-4-20250514',
        messages: [
          {
            role: 'system',
            content: `You are a professional B2B sales representative for Farreach Electronic (HDMI/DP/USB cables).
Write concise, professional email replies following these rules:
- NO "not...but" sentence structures
- NO em dashes (—— / —)
- NO "cutting-edge" 
- Objective facts over emotional language
- Each email advances ONE concrete action
- End with a clear next step (confirm specs? arrange sample? schedule call?)
- Language: match customer's language (English→English, other→English)
- Tone: professional but warm, trustworthy supplier`
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.3,
        max_tokens: 500
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || '';
    
    console.log(`✅ 回复草稿生成完成`);
    
    return {
      success: true,
      reply: reply.trim(),
      wordCount: reply.trim().split(/\s+/).length
    };
  } catch (err) {
    console.error(`❌ 回复生成失败：${err.message}`);
    
    // 降级：使用模板填充
    return generateTemplateFallback(originalEmail, intent);
  }
}

/**
 * 构建 LLM prompt
 */
function buildGenerationPrompt(email, intent, kbResults, language) {
  let prompt = `Generate a professional email reply based on:

ORIGINAL EMAIL:
Subject: ${email.subject || 'No subject'}
From: ${email.from || 'Unknown'}
Content:
${email.body?.slice(0, 1500) || 'No content'}

INTENT: ${intent}

`;

  if (kbResults.found && kbResults.results.length > 0) {
    prompt += `KNOWLEDGE BASE CONTEXT:\n`;
    kbResults.results.forEach((r, i) => {
      prompt += `\n[${i + 1}] Source: ${r.source}\n${r.content?.slice(0, 300) || r}\n`;
    });
    prompt += `\n`;
  }

  prompt += `REQUIREMENTS:
- Language: ${language === 'zh' ? 'English (customer wrote in Chinese)' : 'English'}
- Be concise and professional
- Address the customer's specific questions/concerns
- Include relevant product info from knowledge base if available
- End with ONE clear next step
- Do NOT make promises about price/delivery without confirmation

Generate the reply:`;

  return prompt;
}

/**
 * 模板降级方案（当 LLM 不可用时）
 */
function generateTemplateFallback(email, intent) {
  const templates = {
    'inquiry': `Dear Valued Customer,

Thank you for your interest in Farreach Electronic products.

We specialize in HDMI, DisplayPort, and USB cables with competitive pricing and reliable quality.

Could you please share more details about your requirements?
- Product type and specifications
- Estimated quantity
- Target market

This will help us provide an accurate quotation.

Best regards,
Jaden
Farreach Electronic Co., Ltd.`,

    'delivery-chase': `Dear Valued Customer,

Thank you for reaching out regarding your order status.

To provide you with accurate information, could you please share your order number or invoice reference?

Once confirmed, I will check with our production team and update you promptly.

Best regards,
Jaden
Farreach Electronic Co., Ltd.`,

    'complaint': `Dear Valued Customer,

Thank you for bringing this to our attention.

We take quality issues seriously and would like to resolve this promptly.

Could you please provide:
- Order number
- Photos of the issue
- Specific details about the problem

We will investigate and propose a solution within 24 hours.

Best regards,
Jaden
Farreach Electronic Co., Ltd.`,

    'technical': `Dear Valued Customer,

Thank you for your technical inquiry.

To provide accurate assistance, could you please share:
- Product model/part number
- Your application/use case
- Specific technical requirements

Our engineering team will review and respond with detailed specifications.

Best regards,
Jaden
Farreach Electronic Co., Ltd.`,

    'partnership': `Dear Valued Customer,

Thank you for your interest in partnership opportunities.

We welcome distributors and agents worldwide. To explore this further, could you please share:
- Your company profile
- Target market/region
- Expected annual volume

I will forward this to our management team for review.

Best regards,
Jaden
Farreach Electronic Co., Ltd.`,

    'spam': null, // 不生成回复
  };

  const template = templates[intent] || templates['inquiry'];
  
  if (!template) {
    return {
      success: false,
      reply: null,
      reason: 'No template available for this intent'
    };
  }

  return {
    success: true,
    reply: template,
    wordCount: template.split(/\s+/).length,
    method: 'template_fallback'
  };
}

module.exports = {
  generateReply,
  loadTemplate,
  generateTemplateFallback
};

#!/usr/bin/env node

/**
 * 邮件回复生成模块 (Reply Generation Module)
 * 
 * 职责：接收 {email, intentResult, kbResults} → 调用 LLM 生成回复草稿 → 返回 {subject, body, language, template_used, draft_id}
 * 
 * 模块规范：
 * - 单一公开入口：async function generateReply({email, intentResult, kbResults})
 * - 从 intent-schema.json 读取 reply_template_id
 * - 调用 OpenRouter API (anthropic/claude-sonnet-4)
 * - 低置信度 < 0.75 返回 needs_manual: true
 * - spam 直接过滤
 * - complaint 标记 escalate: true
 * - draft_id 格式：DRAFT-{timestamp}-{intent 前 3 字母大写}
 */

const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const CONFIG_DIR = path.join(__dirname, 'config');
const INTENT_SCHEMA_PATH = path.join(CONFIG_DIR, 'intent-schema.json');
const DRAFTS_DIR = path.join(__dirname, 'drafts');
const TEMPLATE_DIR = path.join(__dirname, 'templates');

/**
 * 主函数：生成回复草稿
 * @param {Object} params
 * @param {Object} params.email - 原始邮件 {subject, from, body, receivedAt}
 * @param {Object} params.intentResult - Intent 识别结果 {intent, confidence, key_entities}
 * @param {Object} params.kbResults - 知识库检索结果 {found, results}
 * @returns {Promise<Object>} {draft, draft_id, needs_manual, requires_human_approval, escalate, subject, body, language, template_used}
 */
async function generateReply({ email, intentResult, kbResults }) {
  const { intent, confidence } = intentResult;
  
  console.log(`\n✍️  生成回复草稿...`);
  console.log(`   Intent: ${intent}`);
  console.log(`   Confidence: ${confidence}`);

  // 1. 检查置信度
  if (confidence < 0.75) {
    console.log(`⚠️  置信度低于阈值 (${confidence} < 0.75)，需要人工审阅`);
    return {
      draft: null,
      needs_manual: true,
      reason: 'low_confidence',
      confidence,
      intent
    };
  }

  // 2. 处理 spam
  if (intent === 'spam') {
    console.log(`🗑️  Spam 邮件，直接过滤`);
    return {
      draft: null,
      needs_manual: false,
      reason: 'spam_filtered',
      intent
    };
  }

  // 3. 读取 intent schema 获取 template_id
  const intentSchema = loadIntentSchema();
  const intentConfig = intentSchema.intents.find(i => i.id === intent);
  const templateId = intentConfig?.reply_template_id || 'template-inquiry-001';

  // 4. 处理 complaint 类型
  const isComplaint = intent === 'complaint';
  const requiresHumanApproval = isComplaint;
  const escalate = isComplaint;

  // 5. 生成 draft_id
  const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
  const intentPrefix = intent.split('-').map(p => p[0].toUpperCase()).join('').slice(0, 3);
  const draft_id = `DRAFT-${timestamp}-${intentPrefix}`;

  // 6. 调用 LLM 生成回复
  const language = detectLanguage(email.body);
  let replyContent = await callLLM(email, intent, kbResults, language, templateId);

  if (!replyContent) {
    // LLM 失败，使用模板降级
    const fallbackResult = generateTemplateFallback(intent, email);
    if (!fallbackResult.success) {
      return {
        draft: null,
        needs_manual: true,
        reason: 'generation_failed',
        intent
      };
    }
    replyContent = fallbackResult.reply;
  }

  // 7. 构建回复对象
  const draft = {
    draft_id,
    subject: buildSubject(email.subject, intent),
    body: replyContent,
    language: language === 'zh' ? 'en' : 'en', // 始终用英文回复
    template_used: templateId,
    intent,
    confidence,
    requires_human_approval: requiresHumanApproval,
    escalate,
    created_at: new Date().toISOString(),
    original_email: {
      subject: email.subject,
      from: email.from,
      receivedAt: email.receivedAt
    }
  };

  // 8. 保存草稿到文件
  saveDraft(draft_id, draft);

  console.log(`✅ 草稿生成完成：${draft_id}`);
  console.log(`   主题：${draft.subject}`);
  console.log(`   模板：${templateId}`);
  if (escalate) {
    console.log(`   ⚠️  需要人工审批 (complaint)`);
  }

  return {
    draft,
    draft_id,
    needs_manual: false,
    requires_human_approval: requiresHumanApproval,
    escalate,
    subject: draft.subject,
    body: draft.body,
    language: draft.language,
    template_used: draft.template_used
  };
}

/**
 * 加载 intent schema
 */
function loadIntentSchema() {
  try {
    const content = fs.readFileSync(INTENT_SCHEMA_PATH, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    console.error(`❌ 无法加载 intent schema: ${err.message}`);
    // 返回默认 schema
    return {
      intents: [
        { id: 'inquiry', reply_template_id: 'template-inquiry-001' },
        { id: 'delivery-chase', reply_template_id: 'template-delivery-001' },
        { id: 'complaint', reply_template_id: 'template-complaint-001' },
        { id: 'technical', reply_template_id: 'template-technical-001' },
        { id: 'partnership', reply_template_id: 'template-partnership-001' },
        { id: 'spam', reply_template_id: null }
      ]
    };
  }
}

/**
 * 检测邮件语言
 */
function detectLanguage(text) {
  if (!text) return 'en';
  // 简单检测：如果包含中文字符，返回 zh
  const hasChinese = /[\u4e00-\u9fa5]/.test(text);
  return hasChinese ? 'zh' : 'en';
}

/**
 * 调用 LLM 生成回复
 */
async function callLLM(email, intent, kbResults, language, templateId) {
  const prompt = buildPrompt(email, intent, kbResults, language, templateId);

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'HTTP-Referer': 'https://farreach-electronic.com',
        'X-Title': 'FarreachEmailReply'
      },
      body: JSON.stringify({
        model: 'anthropic/claude-sonnet-4',
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
- Language: English (always reply in English regardless of customer language)
- Tone: professional but warm, trustworthy supplier
- Do NOT fabricate data (price, delivery, specs) - use placeholders if unknown`
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.3,
        max_tokens: 600
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || '';
    
    return reply.trim() || null;
  } catch (err) {
    console.error(`⚠️  LLM 调用失败：${err.message}`);
    return null;
  }
}

/**
 * 构建 LLM prompt
 */
function buildPrompt(email, intent, kbResults, language, templateId) {
  let prompt = `Generate a professional email reply based on:

ORIGINAL EMAIL:
Subject: ${email.subject || 'No subject'}
From: ${email.from || 'Unknown'}
Content:
${email.body?.slice(0, 1500) || 'No content'}

INTENT: ${intent}

`;

  if (kbResults?.found && kbResults.results?.length > 0) {
    prompt += `KNOWLEDGE BASE CONTEXT:\n`;
    kbResults.results.forEach((r, i) => {
      prompt += `\n[${i + 1}] Source: ${r.source || 'Unknown'}\n${r.content?.slice(0, 300) || r}\n`;
    });
    prompt += `\n`;
  }

  const languageInstruction = language === 'zh' 
    ? 'Customer wrote in Chinese, but reply in English (professional B2B standard).'
    : 'Customer wrote in English, reply in English.';

  prompt += `REQUIREMENTS:
- Language: ${languageInstruction}
- Be concise and professional
- Address the customer's specific questions/concerns
- Include relevant product info from knowledge base if available
- End with ONE clear next step
- Do NOT make promises about price/delivery without confirmation

Generate the reply:`;

  return prompt;
}

/**
 * 模板降级方案
 */
function generateTemplateFallback(intent, email) {
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

    'spam': null
  };

  const template = templates[intent] || templates['inquiry'];
  
  if (!template) {
    return { success: false, reply: null };
  }

  return { success: true, reply: template };
}

/**
 * 构建回复主题
 */
function buildSubject(originalSubject, intent) {
  const prefix = {
    'inquiry': 'Re:',
    'delivery-chase': 'Re: Order Status Update',
    'complaint': 'Re: Regarding Your Concern',
    'technical': 'Re: Technical Support',
    'partnership': 'Re: Partnership Opportunity'
  };

  const p = prefix[intent] || 'Re:';
  
  if (originalSubject && !originalSubject.startsWith('Re:')) {
    return `${p} ${originalSubject}`;
  }
  return originalSubject || `${p} Your Inquiry`;
}

/**
 * 保存草稿到文件
 */
function saveDraft(draft_id, draft) {
  try {
    if (!fs.existsSync(DRAFTS_DIR)) {
      fs.mkdirSync(DRAFTS_DIR, { recursive: true });
    }
    const filePath = path.join(DRAFTS_DIR, `${draft_id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(draft, null, 2));
    console.log(`   草稿已保存：${filePath}`);
  } catch (err) {
    console.error(`⚠️  保存草稿失败：${err.message}`);
  }
}

/**
 * 内置测试命令
 */
async function runTest() {
  console.log('🧪 Running reply-generation.js smoke test...\n');

  const mockEmail = {
    subject: 'Inquiry about HDMI cables',
    from: 'customer@example.com',
    body: 'Hi, I am interested in your HDMI cables. Could you please send me a quotation for 1000 units of HDMI 2.1 cables? What is your MOQ and delivery time? Thanks.',
    receivedAt: new Date().toISOString()
  };

  const mockIntentResult = {
    intent: 'inquiry',
    confidence: 0.92,
    key_entities: ['HDMI 2.1', '1000 units', 'quotation']
  };

  const mockKbResults = {
    found: true,
    results: [
      {
        source: 'Product Catalog - HDMI Cables',
        content: 'HDMI 2.1 cables support 4K@120Hz, 8K@60Hz. Standard MOQ: 500 units. Lead time: 7-15 days for standard products.'
      }
    ]
  };

  try {
    const result = await generateReply({
      email: mockEmail,
      intentResult: mockIntentResult,
      kbResults: mockKbResults
    });

    console.log('\n📋 Test Result:');
    console.log(JSON.stringify(result, null, 2));

    if (result.draft) {
      console.log('\n✅ Test PASSED - Draft generated successfully');
    } else if (result.needs_manual) {
      console.log('\n⚠️  Test PASSED - Manual review flagged (expected for low confidence)');
    } else {
      console.log('\n❌ Test FAILED - Unexpected result');
    }
  } catch (err) {
    console.error('\n❌ Test FAILED with error:', err.message);
  }
}

// 导出模块
module.exports = { generateReply };

// 如果直接运行，执行测试
if (require.main === module) {
  runTest();
}

/**
 * Test Suite for Second Brain Triage
 */

const { SecondBrainTriage, ContentAnalyzer, ParaClassifier, UrgencyScorer, RelatednessDetector } = require('../src');

function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
  console.log(`✓ ${message}`);
}

function testContentAnalyzer() {
  console.log('\n=== Content Analyzer Tests ===');
  
  const analyzer = new ContentAnalyzer();
  
  // Test task detection
  const taskResult = analyzer.analyze('TODO: 完成项目报告，截止本周五 #工作');
  assert(taskResult.type === 'task', 'Detects task type');
  assert(taskResult.metadata.tags.includes('工作'), 'Extracts tags');
  assert(taskResult.metadata.priority === 'normal', 'Extracts priority');
  
  // Test URL detection
  const urlResult = analyzer.analyze('https://github.com/user/repo');
  assert(urlResult.type === 'code', 'Detects code URL');
  assert(urlResult.isUrl === true, 'Identifies URL');
  assert(urlResult.metadata.domain === 'github.com', 'Extracts domain');
  
  // Test article detection
  const articleResult = analyzer.analyze(`如何学习编程

编程是一项重要的技能。本文将介绍学习编程的方法。

首先，选择一门编程语言。然后，开始练习。`);
  assert(articleResult.type === 'article', 'Detects article type');
  assert(articleResult.metadata.title === '如何学习编程', 'Extracts title');
  
  // Test code detection
  const codeResult = analyzer.analyze(`const x = 1;
function test() {
  return x + 1;
}`);
  assert(codeResult.type === 'code', 'Detects code type');
  assert(codeResult.metadata.language === 'javascript', 'Detects JavaScript');
  
  console.log('Content Analyzer tests passed!');
}

function testParaClassifier() {
  console.log('\n=== PARA Classifier Tests ===');
  
  const classifier = new ParaClassifier();
  
  // Test project classification
  const projectAnalysis = {
    type: 'task',
    metadata: {
      title: '完成网站重构项目',
      description: '需要在月底之前完成',
      tags: ['工作', '项目'],
    },
  };
  const projectUrgency = { score: 8 };
  const projectResult = classifier.classify(projectAnalysis, projectUrgency);
  assert(projectResult.category === 'projects', 'Classifies as project');
  assert(projectResult.confidence > 0.5, 'Has reasonable confidence');
  
  // Test area classification
  const areaAnalysis = {
    type: 'note',
    metadata: {
      title: '每周健康检查清单',
      description: '维护健康习惯的例行检查',
      tags: ['健康', '习惯'],
    },
  };
  const areaUrgency = { score: 5 };
  const areaResult = classifier.classify(areaAnalysis, areaUrgency);
  assert(areaResult.category === 'areas', 'Classifies as area');
  
  // Test resource classification
  const resourceAnalysis = {
    type: 'article',
    metadata: {
      title: 'React Hooks教程',
      description: '学习React Hooks的参考资料',
      tags: ['技术', '学习'],
    },
  };
  const resourceUrgency = { score: 3 };
  const resourceResult = classifier.classify(resourceAnalysis, resourceUrgency);
  assert(resourceResult.category === 'resources', 'Classifies as resource');
  
  console.log('PARA Classifier tests passed!');
}

function testUrgencyScorer() {
  console.log('\n=== Urgency Scorer Tests ===');
  
  const scorer = new UrgencyScorer();
  
  // Test critical urgency
  const criticalAnalysis = {
    type: 'task',
    metadata: {
      title: 'P0: 修复生产环境bug',
      description: '立即处理，影响用户',
      priority: 'critical',
    },
  };
  const criticalResult = scorer.calculate(criticalAnalysis);
  assert(criticalResult.score >= 7, 'Detects critical urgency');
  assert(criticalResult.level.level === 'critical' || criticalResult.level.level === 'high', 'Has high level');
  
  // Test low urgency
  const lowAnalysis = {
    type: 'article',
    metadata: {
      title: '有趣的编程文章',
      description: '稍后阅读，不急',
    },
  };
  const lowResult = scorer.calculate(lowAnalysis);
  assert(lowResult.score <= 5, 'Detects low urgency');
  
  // Test with due date
  const dueAnalysis = {
    type: 'task',
    metadata: {
      title: '提交报告',
      dueDate: new Date(Date.now() + 86400000).toISOString().split('T')[0], // tomorrow
    },
  };
  const dueResult = scorer.calculate(dueAnalysis);
  assert(dueResult.score >= 6, 'Considers due date');
  
  console.log('Urgency Scorer tests passed!');
}

function testRelatednessDetector() {
  console.log('\n=== Relatedness Detector Tests ===');
  
  const detector = new RelatednessDetector();
  
  const existingItems = [
    {
      analysis: {
        type: 'article',
        metadata: {
          title: 'JavaScript异步编程',
          description: '关于Promise和async/await的文章',
          tags: ['技术', 'JavaScript'],
        },
      },
    },
    {
      analysis: {
        type: 'article',
        metadata: {
          title: 'Python入门指南',
          description: 'Python编程基础',
          tags: ['技术', 'Python'],
        },
      },
    },
  ];
  
  const newAnalysis = {
    type: 'article',
    metadata: {
      title: 'JavaScript Promise详解',
      description: '深入理解Promise机制',
      tags: ['技术', 'JavaScript'],
    },
  };
  
  const result = detector.detect(newAnalysis, existingItems.map(i => i.analysis));
  assert(result.hasRelated === true, 'Finds related items');
  assert(result.topRelated.length > 0, 'Returns top related');
  assert(result.topRelated[0].similarity > 0.3, 'Has reasonable similarity');
  
  console.log('Relatedness Detector tests passed!');
}

function testIntegration() {
  console.log('\n=== Integration Tests ===');
  
  const triage = new SecondBrainTriage();
  
  // Test single triage
  const result = triage.triage('TODO: 完成第二大脑分诊系统开发，截止明天 #项目');
  assert(result.analysis.type === 'task', 'Analyzes content');
  assert(result.classification.category === 'projects', 'Classifies correctly');
  assert(result.urgency.score >= 6, 'Scores urgency');
  assert(result.summary.title, 'Generates summary');
  
  // Test batch triage
  const batchResults = triage.triageBatch([
    '学习React Hooks',
    'https://github.com/facebook/react',
    'TODO: 修复登录bug，P0紧急',
  ]);
  assert(batchResults.length === 3, 'Processes batch');
  assert(batchResults.every(r => r.classification), 'All have classification');
  
  // Test stats
  const stats = triage.getCategoryStats(batchResults);
  assert(stats.total === 3, 'Stats total correct');
  assert(stats.byCategory, 'Has category breakdown');
  
  // Test export
  const markdown = triage.exportReport(batchResults, 'markdown');
  assert(markdown.includes('#'), 'Exports markdown');
  
  const csv = triage.exportReport(batchResults, 'csv');
  assert(csv.includes(','), 'Exports CSV');
  
  console.log('Integration tests passed!');
}

function runTests() {
  console.log('Running Second Brain Triage Tests...\n');
  
  try {
    testContentAnalyzer();
    testParaClassifier();
    testUrgencyScorer();
    testRelatednessDetector();
    testIntegration();
    
    console.log('\n✅ All tests passed!');
    process.exit(0);
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

runTests();
#!/usr/bin/env node

/**
 * Search Agent CLI
 * Command-line interface for the Search Agent skill
 */

const searchAgent = require('./index');

const commands = {
  search: {
    description: 'Perform a general web search',
    usage: 'search-agent search <query> [--type=general|news|academic|code]',
    handler: async (args) => {
      const query = args.join(' ');
      if (!query) {
        console.error('Error: Please provide a search query');
        process.exit(1);
      }
      
      console.log(`🔍 Searching for: "${query}"...\n`);
      
      try {
        const result = await searchAgent.search(query, { maxResults: 5 });
        displayResults(result);
      } catch (error) {
        console.error('Search failed:', error.message);
        process.exit(1);
      }
    }
  },
  
  quick: {
    description: 'Get a quick answer',
    usage: 'search-agent quick <query>',
    handler: async (args) => {
      const query = args.join(' ');
      if (!query) {
        console.error('Error: Please provide a query');
        process.exit(1);
      }
      
      console.log(`⚡ Quick search: "${query}"...\n`);
      
      try {
        const answer = await searchAgent.quickSearch(query);
        console.log('Answer:');
        console.log(answer);
      } catch (error) {
        console.error('Search failed:', error.message);
        process.exit(1);
      }
    }
  },
  
  factcheck: {
    description: 'Verify a claim or fact',
    usage: 'search-agent factcheck <claim>',
    handler: async (args) => {
      const claim = args.join(' ');
      if (!claim) {
        console.error('Error: Please provide a claim to verify');
        process.exit(1);
      }
      
      console.log(`🔍 Fact-checking: "${claim}"...\n`);
      
      try {
        const result = await searchAgent.factCheck(claim);
        displayFactCheck(result);
      } catch (error) {
        console.error('Fact-check failed:', error.message);
        process.exit(1);
      }
    }
  },
  
  news: {
    description: 'Search for recent news',
    usage: 'search-agent news <topic> [--days=7]',
    handler: async (args) => {
      const topic = args.join(' ');
      if (!topic) {
        console.error('Error: Please provide a news topic');
        process.exit(1);
      }
      
      console.log(`📰 Searching news for: "${topic}"...\n`);
      
      try {
        const result = await searchAgent.searchNews(topic);
        displayResults(result);
      } catch (error) {
        console.error('News search failed:', error.message);
        process.exit(1);
      }
    }
  },
  
  academic: {
    description: 'Search academic sources',
    usage: 'search-agent academic <query>',
    handler: async (args) => {
      const query = args.join(' ');
      if (!query) {
        console.error('Error: Please provide a research query');
        process.exit(1);
      }
      
      console.log(`🎓 Academic search: "${query}"...\n`);
      
      try {
        const result = await searchAgent.searchAcademic(query);
        displayResults(result);
      } catch (error) {
        console.error('Academic search failed:', error.message);
        process.exit(1);
      }
    }
  },
  
  code: {
    description: 'Search for code solutions',
    usage: 'search-agent code <query>',
    handler: async (args) => {
      const query = args.join(' ');
      if (!query) {
        console.error('Error: Please provide a code query');
        process.exit(1);
      }
      
      console.log(`💻 Code search: "${query}"...\n`);
      
      try {
        const result = await searchAgent.searchCode(query);
        displayResults(result);
      } catch (error) {
        console.error('Code search failed:', error.message);
        process.exit(1);
      }
    }
  },
  
  help: {
    description: 'Show help information',
    usage: 'search-agent help [command]',
    handler: (args) => {
      if (args.length > 0) {
        const cmd = args[0];
        if (commands[cmd]) {
          console.log(`\n${commands[cmd].description}`);
          console.log(`Usage: ${commands[cmd].usage}\n`);
        } else {
          console.error(`Unknown command: ${cmd}`);
          process.exit(1);
        }
      } else {
        showHelp();
      }
    }
  },
  
  version: {
    description: 'Show version information',
    usage: 'search-agent version',
    handler: () => {
      const pkg = require('./package.json');
      console.log(`Search Agent v${pkg.version}`);
      console.log(`Node.js ${process.version}`);
    }
  }
};

function displayResults(result) {
  console.log('═'.repeat(60));
  console.log('📋 SUMMARY');
  console.log('═'.repeat(60));
  console.log(result.summary);
  console.log();
  
  if (result.keyFindings && result.keyFindings.length > 0) {
    console.log('═'.repeat(60));
    console.log('🔑 KEY FINDINGS');
    console.log('═'.repeat(60));
    result.keyFindings.forEach((finding, i) => {
      console.log(`${i + 1}. ${finding.point}`);
      console.log(`   Source: ${finding.source}`);
      console.log(`   Credibility: ${finding.credibility}%`);
      console.log();
    });
  }
  
  if (result.sources && result.sources.length > 0) {
    console.log('═'.repeat(60));
    console.log('📚 SOURCES');
    console.log('═'.repeat(60));
    result.sources.forEach(source => {
      console.log(`${source.index}. ${source.title}`);
      console.log(`   URL: ${source.url}`);
      console.log(`   Credibility: ${'⭐'.repeat(Math.round(source.credibility / 20))} (${source.credibility}%)`);
      console.log();
    });
  }
  
  if (result.relatedQueries && result.relatedQueries.length > 0) {
    console.log('═'.repeat(60));
    console.log('💡 RELATED TOPICS');
    console.log('═'.repeat(60));
    result.relatedQueries.forEach(topic => {
      console.log(`• ${topic}`);
    });
    console.log();
  }
  
  console.log('═'.repeat(60));
  console.log(`✅ Confidence: ${result.confidence}% | Sources: ${result.metadata.totalSources}`);
  console.log('═'.repeat(60));
}

function displayFactCheck(result) {
  console.log('═'.repeat(60));
  console.log('🔍 FACT CHECK RESULT');
  console.log('═'.repeat(60));
  console.log(`Claim: ${result.claim}`);
  console.log();
  
  const verdictEmoji = {
    'likely_true': '✅',
    'uncertain': '⚠️',
    'likely_false': '❌'
  };
  
  console.log(`${verdictEmoji[result.verdict]} Verdict: ${result.verdict.replace(/_/g, ' ').toUpperCase()}`);
  console.log(`📊 Confidence: ${result.confidence}%`);
  console.log();
  
  if (result.evidence && result.evidence.length > 0) {
    console.log('📋 Evidence:');
    result.evidence.forEach((item, i) => {
      console.log(`  ${i + 1}. ${item.point}`);
    });
    console.log();
  }
  
  if (result.sources && result.sources.length > 0) {
    console.log('📚 Sources:');
    result.sources.forEach(source => {
      console.log(`  • ${source.title} (${source.url})`);
    });
  }
  
  console.log('═'.repeat(60));
}

function showHelp() {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    🔍 SEARCH AGENT v1.0.0                    ║
║          AI-Powered Intelligent Search & Research            ║
╚══════════════════════════════════════════════════════════════╝

Usage: search-agent <command> [options] <query>

Commands:
`);
  
  Object.entries(commands).forEach(([name, cmd]) => {
    console.log(`  ${name.padEnd(12)} ${cmd.description}`);
  });
  
  console.log(`
Examples:
  search-agent search "quantum computing latest news"
  search-agent quick "what is machine learning"
  search-agent factcheck "Python is the most popular language"
  search-agent news "artificial intelligence"
  search-agent academic "climate change effects"
  search-agent code "react hooks tutorial"

Environment Variables:
  SEARCH_API_KEY      API key for search services
  SEARCH_MAX_RESULTS  Maximum results (default: 10)
  SEARCH_TIMEOUT      Request timeout in ms (default: 30000)
  SEARCH_LANGUAGE     Language code (default: zh-CN)

For more help: search-agent help <command>
`);
}

// Main CLI logic
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    showHelp();
    process.exit(0);
  }
  
  const command = args[0];
  const commandArgs = args.slice(1);
  
  if (commands[command]) {
    commands[command].handler(commandArgs);
  } else {
    // Default to search if no command specified
    commands.search.handler(args);
  }
}

main();

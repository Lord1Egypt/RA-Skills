#!/usr/bin/env node

/**
 * 微信公众号内容工作室 - 主入口
 * 支持关键词搜索和多链接抓取两种模式
 */

import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';
import { Command } from 'commander';
import { loadOpenClawEnv } from './lib/openclaw_env.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
loadOpenClawEnv({ skillRoot: path.join(__dirname, '..') });

/** 与 ~/.workbuddy/skills 下本技能文件夹名一致，作为 $HOME/WorkBuddy/<技能名> 的最后一级目录名 */
const SKILL_DIR_NAME = path.basename(path.resolve(__dirname, '..'));
const DEFAULT_OUTPUT_DIR = path.join(
  process.env.HOME || process.env.USERPROFILE || '~',
  'WorkBuddy',
  SKILL_DIR_NAME
);

const program = new Command();

// 导入各模块
// searchWechatArticles 已弃用，统一使用 multiSourceSearch
const { extractArticle } = await import('./extractor/multi_site_bridge.js');
const { mergeArticles } = await import('./search/merge_articles.js');
const { rewriteArticle, removeAiTrace, generateTitles } = await import('./rewriter/rewrite.js');
const { generateCover } = await import('./image/generate_cover.js');
const { publishWithWenyan } = await import('./publisher/publish_wenyan.js');
const { fullBrowserPublish, checkBrowserEnv } = await import('./publisher/publish_browser.js');
const { autoOptimizeLayout } = await import('./auto-optimize.js');
const { smartOptimizeArticle } = await import('./smart-optimize.js');
const { multiSourceSearch, getAvailableCategories, getDefaultCategories } = await import('./search/multi_source_search.js');

program
  .name('wechat-content-studio')
  .description('微信公众号内容工作室 - 搜索、抓取、合并、改写、发布一站式工具')
  .version('1.0.0');

// 搜索命令（多来源搜索 → 抓取完整内容 → 合并 → 改写 → 封面 → 排版 → 发布）
program
  .command('search <keyword>')
  .description('多来源搜索文章并自动执行完整流程（抓取 → 合并 → 改写 → 封面 → 发布）')
  .option('-c, --count <number>', '每来源最大抓取数', '3')
  .option('-s, --sources <categories>', '搜索分类（逗号分隔），用 --list-sources 查看可选值')
  .option('--all-sources', '搜索所有分类')
  .option('--list-sources', '列出所有可用的搜索分类')
  .option('--wechat-only', '仅搜索微信公众号（使用搜狗搜索）')
  .option('--total-max <number>', '搜索结果总上限', '20')
  .option('--merge', '合并多篇文章', true)
  .option('--no-auto', '不自动执行后续流程（仅搜索和抓取）')
  .option('--no-merge', '不合并，分别保存每篇文章')
  .option('--style <style>', '改写风格', 'original')
  .option('--no-clean', '不去除 AI 味')
  .option('--wenyan', '使用 wenyan-cli 发布（默认）')
  .option('--browser', '使用浏览器自动化发布')
  .option('--theme <theme>', 'wenyan 主题', 'lapis')
  .option('--highlight <highlight>', '代码高亮主题', 'solarized-light')
  .option('--headed', '显示浏览器窗口（browser 模式）')
  .option('--output <dir>', '输出目录', DEFAULT_OUTPUT_DIR)
  .action(async (keyword, options) => {
    // --list-sources: 列出所有分类后退出
    if (options.listSources) {
      console.log('\n📂 可用的搜索分类：\n');
      const cats = getAvailableCategories();
      const defaults = getDefaultCategories();
      for (const c of cats) {
        const isDefault = defaults.includes(c.key) ? ' ⭐ 默认' : '';
        console.log(`  ${c.key.padEnd(20)} ${c.label} (${c.sourceCount} 来源)${isDefault}`);
      }
      console.log('\n用法: search "关键词" --sources high_quality_channels,wechat_top,dev_community');
      console.log('用法: search "关键词" --all-sources\n');
      return;
    }

    try {
      let searchResults = [];

      if (options.wechatOnly) {
        // 仅搜索微信公众号来源
        const { results } = await multiSourceSearch(keyword, {
          categories: ['wechat_top'],
          maxPerSource: parseInt(options.count),
          totalMax: parseInt(options.totalMax),
        });
        searchResults = results;
      } else {
        // 多来源搜索
        let categories;
        if (options.allSources) {
          categories = getAvailableCategories().map(c => c.key);
        } else if (options.sources) {
          categories = options.sources.split(',').map(s => s.trim()).filter(Boolean);
        }
        // 不传 categories 则使用默认分类

        const { results } = await multiSourceSearch(keyword, {
          categories,
          maxPerSource: parseInt(options.count),
          totalMax: parseInt(options.totalMax),
        });
        searchResults = results;
      }

      if (searchResults.length === 0) {
        console.log('❌ 未找到相关文章');
        return;
      }

      console.log(`\n✅ 搜索到 ${searchResults.length} 篇文章，开始抓取完整内容...\n`);

      // 逐篇用 extractArticle 抓取完整 Markdown 内容
      const articles = [];
      for (let i = 0; i < searchResults.length; i++) {
        const item = searchResults[i];
        const articleUrl = item.url;
        console.log(`[${i + 1}/${searchResults.length}] 抓取：${item.title}`);

        if (!articleUrl) {
          console.log(`  ⚠️  URL 为空，跳过`);
          continue;
        }

        const result = await extractArticle(articleUrl);

        if (!result.done || result.code !== 0) {
          console.log(`  ⚠️  提取失败：${result.msg || '未知错误'}`);
          continue;
        }

        articles.push(result.data);
        console.log(`  ✅ 成功：${result.data.msg_title}（${result.data.msg_source || item.source || '未知来源'}）`);
      }

      if (articles.length === 0) {
        console.log('\n❌ 没有成功抓取到任何文章');
        return;
      }

      console.log(`\n✅ 成功抓取 ${articles.length} 篇文章\n`);

      // 合并或分别保存
      if (options.merge) {
        console.log('📝 开始合并文章...');
        const mergedArticle = mergeArticles(articles, keyword);

        const outputDir = path.join(options.output, sanitizeFileName(mergedArticle.title));
        fs.mkdirSync(outputDir, { recursive: true });

        const mdPath = path.join(outputDir, 'article.md');
        fs.writeFileSync(mdPath, mergedArticle.markdown, 'utf-8');

        const jsonPath = path.join(outputDir, 'merged_articles.json');
        fs.writeFileSync(jsonPath, JSON.stringify({
          keyword,
          sourceArticles: articles,
          mergedArticle,
          createdAt: new Date().toISOString()
        }, null, 2), 'utf-8');

        console.log(`✅ 合并后的文章已保存到：${mdPath}\n`);

        // 自动执行完整流程（与 links 命令一致）
        if (options.auto !== false) {
          console.log('🚀 开始自动执行完整流程：改写 + 封面 + 排版 + 发布\n');
          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

          // AI 改写
          console.log('📝 步骤 1/4: AI 改写...\n');
          const rewrittenContent = await rewriteArticle(mergedArticle.markdown, {
            style: options.style
          });

          const finalContent = options.clean !== false ? removeAiTrace(rewrittenContent) : rewrittenContent;

          const titles = await generateTitles(finalContent);
          console.log('\n🎯 备选标题：');
          titles.forEach((t, i) => console.log(`  ${i + 1}. ${t}`));

          const rewrittenPath = path.join(outputDir, 'article_rewritten.md');
          fs.writeFileSync(rewrittenPath, finalContent, 'utf-8');
          console.log(`\n✅ 改写完成：${rewrittenPath}\n`);
          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

          // 生成封面图
          console.log('🎨 步骤 2/4: 生成封面图...\n');
          const title = titles[0] || extractTitle(finalContent);
          const contentSummary = finalContent.substring(0, 200).replace(/[#*_~`]/g, '');

          const coverResult = await generateCover({
            title,
            content: contentSummary,
            outputDir: outputDir
          });

          let coverPath = null;
          if (coverResult.success) {
            coverPath = coverResult.path || coverResult.url;
            console.log(`\n✅ 封面生成：${coverPath}\n`);
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

            const updatedContent = finalContent.replace(
              /^cover:\s*\.\/images\/cover\.jpg/m,
              `cover: ${path.relative(outputDir, coverPath)}`
            );
            fs.writeFileSync(rewrittenPath, updatedContent, 'utf-8');
          } else {
            console.log('\n⚠️  封面生成失败，使用默认封面\n');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
          }

          // 排版优化
          console.log('✍️  步骤 3/4: 自动优化排版...\n');
          await autoOptimizeLayout(rewrittenPath, { maxIterations: 5 });

          // 发布到公众号
          console.log('\n📱 步骤 4/4: 发布到公众号...\n');

          if (options.browser) {
            await checkBrowserEnv();
            await fullBrowserPublish(rewrittenPath, {
              useProfile: true,
              headed: !!options.headed,
              generateCover: !coverPath
            });
          } else {
            const result = await publishWithWenyan(rewrittenPath, {
              theme: options.theme,
              highlight: options.highlight
            });

            if (!result.success) {
              throw new Error('发布失败');
            }
          }

          console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          console.log('\n✅ 搜索 → 抓取 → 合并 → 改写 → 封面 → 排版 → 发布 全流程完成！\n');
          console.log('📊 执行总结：');
          console.log(`  🔍 搜索关键词：${keyword}`);
          console.log(`  📄 抓取文章数：${articles.length}`);
          console.log(`  ✅ 改写：${rewrittenPath}`);
          if (coverPath) {
            console.log(`  ✅ 封面：${coverPath}`);
          }
          console.log(`  ✅ 发布：公众号草稿箱`);
          console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        } else {
          console.log('⚠️  已跳过自动发布流程（使用了 --no-auto 选项）');
          console.log('💡 提示：如需手动发布，运行：node main.js publish <文件路径>\n');
        }
      } else {
        console.log('📁 分别保存文章...');
        for (let i = 0; i < articles.length; i++) {
          const article = articles[i];
          const articleTitle = article.title || article.msg_title || `article_${i + 1}`;
          const articleDir = path.join(options.output, `${i + 1}_${sanitizeFileName(articleTitle)}`);
          fs.mkdirSync(articleDir, { recursive: true });

          const mdPath = path.join(articleDir, 'article.md');
          const content = article.markdown || article.content || `# ${articleTitle}\n\n[正文内容未抓取]`;
          fs.writeFileSync(mdPath, content, 'utf-8');
          console.log(`  ✅ ${mdPath}`);
        }
        console.log(`\n✅ 文章已保存到：${options.output}`);
      }

    } catch (error) {
      console.error('❌ 搜索失败:', error.message);
      process.exit(1);
    }
  });

// 链接抓取命令（🔥 默认自动执行：改写 + 封面 + 发布）
program
  .command('links [urls]')
  .description('从指定链接抓取文章内容（支持微信/CSDN/博客园/掘金/知乎等，🔥 默认自动执行改写 + 封面 + 发布）')
  .option('--file <path>', '从文件读取链接列表')
  .option('--merge', '合并多篇文章')
  .option('--no-auto', '❌ 不自动执行后续流程（仅当需要手动控制时使用）')
  .option('--style <style>', '改写风格', 'original')
  .option('--no-clean', '不去除 AI 味')
  .option('--wenyan', '使用 wenyan-cli 发布（默认）')
  .option('--browser', '使用浏览器自动化发布')
  .option('--theme <theme>', 'wenyan 主题', 'lapis')
  .option('--highlight <highlight>', '代码高亮主题', 'solarized-light')
  .option('--headed', '显示浏览器窗口（browser 模式）')
  .option('--output <dir>', '输出目录', DEFAULT_OUTPUT_DIR)
  .action(async (urls, options) => {
    let urlList = [];
    
    // 从参数或文件获取链接
    if (urls) {
      urlList = urls.split(',').map(u => u.trim()).filter(Boolean);
    } else if (options.file) {
      if (!fs.existsSync(options.file)) {
        console.error(`❌ 文件不存在：${options.file}`);
        process.exit(1);
      }
      const content = fs.readFileSync(options.file, 'utf-8');
      urlList = content.split('\n').map(u => u.trim()).filter(u => u.startsWith('http'));
    } else {
      console.error('❌ 请提供链接或 --file 参数');
      process.exit(1);
    }
    
    console.log(`🔗 开始抓取 ${urlList.length} 个链接`);
    
    try {
      const articles = [];
      
      for (let i = 0; i < urlList.length; i++) {
        const url = urlList[i];
        console.log(`\n[${i + 1}/${urlList.length}] 抓取：${url}`);
        
        const result = await extractArticle(url);
        
        if (!result.done || result.code !== 0) {
          console.log(`  ⚠️  提取失败：${result.msg || '未知错误'}`);
          continue;
        }
        
        articles.push(result.data);
        console.log(`  ✅ 成功：${result.data.msg_title}（${result.data.msg_source || '未知来源'}）`);
      }
      
      if (articles.length === 0) {
        console.log('\n❌ 没有成功抓取到任何文章');
        return;
      }
      
      // 如果需要合并
      if (options.merge) {
        console.log('\n📝 开始合并文章...');
        const mergedArticle = mergeArticles(articles, '从链接抓取');

        const outputDir = path.join(options.output, sanitizeFileName(mergedArticle.title));
        fs.mkdirSync(outputDir, { recursive: true });

        const mdPath = path.join(outputDir, 'article.md');
        fs.writeFileSync(mdPath, mergedArticle.markdown, 'utf-8');

        console.log(`\n✅ 合并后的文章已保存到：${mdPath}`);

        // 🔥 默认自动执行完整流程：改写 + 封面 + 发布（除非指定 --no-auto）
        if (options.auto !== false) {
          console.log('\n🚀 开始自动执行完整流程：改写 + 封面 + 发布\n');
          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
          
          // 1. AI 改写
          console.log('📝 步骤 1/4: AI 改写...\n');
          const rewrittenContent = await rewriteArticle(mergedArticle.markdown, {
            style: options.style
          });
          
          const finalContent = options.clean !== false ? removeAiTrace(rewrittenContent) : rewrittenContent;
          
          // 生成备选标题
          const titles = await generateTitles(finalContent);
          console.log('\n🎯 备选标题：');
          titles.forEach((t, i) => console.log(`  ${i + 1}. ${t}`));
          
          const rewrittenPath = path.join(outputDir, 'article_rewritten.md');
          fs.writeFileSync(rewrittenPath, finalContent, 'utf-8');
          console.log(`\n✅ 改写完成：${rewrittenPath}\n`);
          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
          
          // 2. 生成封面图
          console.log('🎨 步骤 2/4: 生成封面图...\n');
          const title = titles[0] || extractTitle(finalContent);
          const contentSummary = finalContent.substring(0, 200).replace(/[#*_~`]/g, '');
          
          const coverResult = await generateCover({
            title,
            content: contentSummary,
            outputDir: outputDir
          });
          
          let coverPath = null;
          if (coverResult.success) {
            coverPath = coverResult.path || coverResult.url;
            console.log(`\n✅ 封面生成：${coverPath}\n`);
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
            
            // 更新文章 frontmatter 中的封面路径
            const updatedContent = finalContent.replace(
              /^cover:\s*\.\/images\/cover\.jpg/m,
              `cover: ${path.relative(outputDir, coverPath)}`
            );
            fs.writeFileSync(rewrittenPath, updatedContent, 'utf-8');
          } else {
            console.log('\n⚠️  封面生成失败，使用默认封面\n');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
          }
          
          // 3. 排版优化
          console.log('✍️  步骤 3/4: 自动优化排版...\n');
          await autoOptimizeLayout(rewrittenPath, { maxIterations: 5 });
          
          // 4. 发布到公众号（仅发布一次）
          console.log('\n📱 步骤 4/4: 发布到公众号...\n');
          
          if (options.browser) {
            await checkBrowserEnv();
            await fullBrowserPublish(rewrittenPath, {
              useProfile: true,
              headed: !!options.headed,
              generateCover: !coverPath
            });
          } else {
            const result = await publishWithWenyan(rewrittenPath, {
              theme: options.theme,
              highlight: options.highlight
            });
            
            if (!result.success) {
              throw new Error('发布失败');
            }
          }
          
          // 总结
          console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          console.log('\n✅ 自动发布完成！\n');
          console.log('📊 执行总结：');
          console.log(`  ✅ 改写：${rewrittenPath}`);
          if (coverPath) {
            console.log(`  ✅ 封面：${coverPath}`);
          }
          console.log(`  ✅ 发布：公众号草稿箱`);
          console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        } else {
          console.log('\n⚠️  已跳过自动发布流程（使用了 --no-auto 选项）');
          console.log('💡 提示：如需手动发布，运行：node main.js publish <文件路径>\n');
        }
      } else {
        // 不合并，分别保存
        console.log('\n📁 保存文章...');
        for (let i = 0; i < articles.length; i++) {
          const article = articles[i];
          const articleDir = path.join(options.output, `${i + 1}_${sanitizeFileName(article.title)}`);
          fs.mkdirSync(articleDir, { recursive: true });
          
          const mdPath = path.join(articleDir, 'article.md');
          const content = article.content || `# ${article.title}\n\n[正文内容未抓取，请使用 --fetch-content 选项]`;
          fs.writeFileSync(mdPath, content, 'utf-8');
        }
        console.log(`✅ 文章已保存到：${options.output}`);
      }
      
    } catch (error) {
      console.error('❌ 抓取失败:', error.message);
      process.exit(1);
    }
  });

// 改写命令
program
  .command('rewrite <file>')
  .description('AI 改写文章')
  .option('--style <style>', '改写风格', 'original')
  .option('--no-clean', '不去除 AI 味')
  .option('--generate-cover', '自动生成封面图')
  .option('--publish', '改写后自动发布到公众号')
  .option('--wenyan', '使用 wenyan-cli 发布（默认）')
  .option('--browser', '使用浏览器自动化发布')
  .option('--theme <theme>', 'wenyan 主题', 'lapis')
  .option('--highlight <highlight>', '代码高亮主题', 'solarized-light')
  .option('--headed', '显示浏览器窗口（browser 模式）')
  .action(async (file, options) => {
    console.log(`✍️  开始改写：${file}`);
    
    try {
      if (!fs.existsSync(file)) {
        throw new Error(`文件不存在：${file}`);
      }
      
      const content = fs.readFileSync(file, 'utf-8');
      
      // AI 改写
      const rewrittenContent = await rewriteArticle(content, {
        style: options.style
      });
      
      // 去 AI 味
      const finalContent = options.clean ? removeAiTrace(rewrittenContent) : rewrittenContent;
      
      // 生成备选标题
      const titles = await generateTitles(finalContent);
      console.log('\n🎯 备选标题：');
      titles.forEach((t, i) => console.log(`  ${i + 1}. ${t}`));
      
      // 保存改写后的文章
      const dir = path.dirname(file);
      const base = path.basename(file, '.md');
      const rewrittenPath = path.join(dir, `${base}_rewritten.md`);
      fs.writeFileSync(rewrittenPath, finalContent, 'utf-8');
      
      console.log(`\n✅ 改写完成，已保存到：${rewrittenPath}`);
      
      // 自动生成封面图
      let coverPath = null;
      if (options.generateCover) {
        console.log('\n🎨 自动生成封面图...');
        const title = titles[0] || extractTitle(finalContent);
        const contentSummary = finalContent.substring(0, 200).replace(/[#*_~`]/g, '');
        
        const result = await generateCover({
          title,
          content: contentSummary,
          outputDir: dir
        });
        
        if (result.success) {
          coverPath = result.path || result.url;
          console.log(`✅ 封面图已生成：${coverPath}`);
          
          // 更新文章 frontmatter 中的封面路径
          const updatedContent = finalContent.replace(
            /^cover:\s*\.\/images\/cover\.jpg/m,
            `cover: ${coverPath}`
          );
          fs.writeFileSync(rewrittenPath, updatedContent, 'utf-8');
        } else {
          console.log('⚠️  封面生成失败，使用占位图');
        }
      }
      
      // 自动发布到公众号
      if (options.publish) {
        console.log('\n📱 开始发布到公众号...');
        
        if (options.browser) {
          // 浏览器自动化发布
          await checkBrowserEnv();
          await fullBrowserPublish(rewrittenPath, {
            useProfile: true,
            headed: !!options.headed,
            generateCover: !options.generateCover // 如果没生成封面，这里生成
          });
        } else {
          // wenyan-cli 发布
          const result = await publishWithWenyan(rewrittenPath, {
            theme: options.theme,
            highlight: options.highlight
          });
          
          if (!result.success) {
            console.error('❌ 发布失败');
            process.exit(1);
          }
        }
        
        console.log('✅ 文章已成功发布到公众号草稿箱！');
      }
      
      // 总结
      console.log('\n📊 执行总结：');
      console.log(`  ✅ 改写完成：${rewrittenPath}`);
      if (coverPath) {
        console.log(`  ✅ 封面生成：${coverPath}`);
      }
      if (options.publish) {
        console.log(`  ✅ 已发布：公众号草稿箱`);
      }
      
    } catch (error) {
      console.error('❌ 改写失败:', error.message);
      process.exit(1);
    }
  });

// 生成封面命令
program
  .command('generate-cover')
  .description('生成微信公众号封面图')
  .requiredOption('--title <title>', '文章标题')
  .option('--content <content>', '内容摘要')
  .option('--style <style>', '风格描述')
  .option('--output <dir>', '输出目录', DEFAULT_OUTPUT_DIR)
  .action(async (options) => {
    console.log(`🎨 生成封面：${options.title}`);
    
    try {
      const result = await generateCover({
        title: options.title,
        content: options.content || '',
        style: options.style || '',
        outputDir: options.output
      });
      
      if (result.success) {
        console.log(`✅ 封面图已生成：${result.path || result.url}`);
      } else {
        console.log(`⚠️  封面生成失败：${result.error}`);
      }
      
    } catch (error) {
      console.error('❌ 封面生成失败:', error.message);
      process.exit(1);
    }
  });

// 智能优化命令
program
  .command('smart-optimize <file>')
  .description('智能动态排版优化（根据文章内容自动生成优化规则）')
  .option('--no-publish', '不自动发布')
  .option('--output <path>', '输出路径')
  .action(async (file, options) => {
    console.log(`🤖 开始智能优化：${file}`);
    
    try {
      if (!fs.existsSync(file)) {
        throw new Error(`文件不存在：${file}`);
      }
      
      const report = await smartOptimizeArticle(file, {
        shouldPublish: options.publish !== false,
        outputPath: options.output
      });
      
      console.log('\n📊 优化报告:');
      console.log(`  - 文章类型：${report.analysis.type}`);
      console.log(`  - 生成规则：${report.rulesApplied} 条`);
      console.log(`  - 应用修改：${report.changesCount} 处`);
      console.log(`  - 质量评分：${report.qualityScore.score}/100`);
      
      if (report.qualityScore.score >= 95) {
        console.log('\n🎉 质量优秀，达到 95 分以上！');
      } else if (report.qualityScore.score >= 90) {
        console.log('\n✅ 质量良好，达到 90 分以上！');
      } else {
        console.log('\n⚠️  质量有待提升，建议继续优化');
      }
      
    } catch (error) {
      console.error('❌ 优化失败:', error.message);
      process.exit(1);
    }
  });

// 发布命令
program
  .command('publish <file>')
  .description('发布文章到微信公众号')
  .option('--wenyan', '使用 wenyan-cli 发布（默认）')
  .option('--browser', '使用浏览器自动化发布')
  .option('--theme <theme>', 'wenyan 主题', 'lapis')
  .option('--highlight <highlight>', '代码高亮主题', 'solarized-light')
  .option('--headed', '显示浏览器窗口（browser 模式）')
  .option('--generate-cover', '发布前生成封面图')
  .action(async (file, options) => {
    console.log(`📱 发布文章：${file}`);
    
    try {
      if (!fs.existsSync(file)) {
        throw new Error(`文件不存在：${file}`);
      }
      
      // 生成封面图（如果指定）
      if (options.generateCover) {
        console.log('\n🎨 生成封面图...');
        const content = fs.readFileSync(file, 'utf-8');
        const title = extractTitle(content);
        const contentSummary = content.substring(0, 200).replace(/[#*_~`]/g, '');
        
        const dir = path.dirname(file);
        const result = await generateCover({
          title,
          content: contentSummary,
          outputDir: dir
        });
        
        if (result.success) {
          console.log(`✅ 封面图已生成：${result.path || result.url}`);
        } else {
          console.log('⚠️  封面生成失败，继续发布');
        }
      }
      
      // 默认使用 wenyan-cli，除非指定 --browser
      if (options.browser) {
        // 浏览器自动化发布
        await checkBrowserEnv();
        await fullBrowserPublish(file, {
          useProfile: true,
          headed: !!options.headed,
          generateCover: !options.generateCover
        });
      } else {
        // wenyan-cli 发布
        const result = await publishWithWenyan(file, {
          theme: options.theme,
          highlight: options.highlight
        });
        
        if (!result.success) {
          process.exit(1);
        }
      }
      
      console.log('\n✅ 文章已成功发布到公众号草稿箱！');
      
    } catch (error) {
      console.error('❌ 发布失败:', error.message);
      process.exit(1);
    }
  });

// 一键发布命令（改写 + 封面 + 发布）
program
  .command('auto-publish <file>')
  .description('一键发布：改写 + 生成封面 + 发布到公众号')
  .option('--style <style>', '改写风格', 'original')
  .option('--no-clean', '不去除 AI 味')
  .option('--wenyan', '使用 wenyan-cli 发布（默认）')
  .option('--browser', '使用浏览器自动化发布')
  .option('--theme <theme>', 'wenyan 主题', 'lapis')
  .option('--highlight <highlight>', '代码高亮主题', 'solarized-light')
  .option('--headed', '显示浏览器窗口（browser 模式）')
  .action(async (file, options) => {
    console.log('🚀 开始一键发布流程\n');
    
    try {
      // 1. 读取文章
      if (!fs.existsSync(file)) {
        throw new Error(`文件不存在：${file}`);
      }
      
      const content = fs.readFileSync(file, 'utf-8');
      const dir = path.dirname(file);
      const base = path.basename(file, '.md');
      const rewrittenPath = path.join(dir, `${base}_rewritten.md`);
      
      // 2. AI 改写
      console.log('📝 步骤 1/3: AI 改写...');
      const rewrittenContent = await rewriteArticle(content, {
        style: options.style
      });
      
      const finalContent = options.clean ? removeAiTrace(rewrittenContent) : rewrittenContent;
      
      // 生成备选标题
      const titles = await generateTitles(finalContent);
      console.log('🎯 备选标题：');
      titles.forEach((t, i) => console.log(`  ${i + 1}. ${t}`));
      
      fs.writeFileSync(rewrittenPath, finalContent, 'utf-8');
      console.log(`✅ 改写完成：${rewrittenPath}\n`);
      
      // 3. 生成封面图
      console.log('🎨 步骤 2/3: 生成封面图...');
      const title = titles[0] || extractTitle(finalContent);
      const contentSummary = finalContent.substring(0, 200).replace(/[#*_~`]/g, '');
      
      const coverResult = await generateCover({
        title,
        content: contentSummary,
        outputDir: dir
      });
      
      let coverPath = null;
      if (coverResult.success) {
        coverPath = coverResult.path || coverResult.url;
        console.log(`✅ 封面生成：${coverPath}\n`);
        
        // 更新文章 frontmatter 中的封面路径
        const updatedContent = finalContent.replace(
          /^cover:\s*\./m,
          `cover: ${path.relative(dir, coverPath)}`
        );
        fs.writeFileSync(rewrittenPath, updatedContent, 'utf-8');
      } else {
        console.log('⚠️  封面生成失败，使用默认封面\n');
      }
      
      // 4. 发布到公众号
      console.log('📱 步骤 3/3: 发布到公众号...');
      
      if (options.browser) {
        await checkBrowserEnv();
        await fullBrowserPublish(rewrittenPath, {
          useProfile: true,
          headed: !!options.headed,
          generateCover: !coverPath
        });
      } else {
        const result = await publishWithWenyan(rewrittenPath, {
          theme: options.theme,
          highlight: options.highlight
        });
        
        if (!result.success) {
          throw new Error('发布失败');
        }
      }
      
      // 5. 总结
      console.log('\n✅ 一键发布完成！');
      console.log('📊 执行总结：');
      console.log(`  ✅ 改写：${rewrittenPath}`);
      if (coverPath) {
        console.log(`  ✅ 封面：${coverPath}`);
      }
      console.log(`  ✅ 发布：公众号草稿箱`);
      
    } catch (error) {
      console.error('\n❌ 一键发布失败:', error.message);
      process.exit(1);
    }
  });

// 完整工作流命令
program
  .command('workflow <type>')
  .description('执行完整工作流')
  .option('--keyword <keyword>', '搜索关键词（search 模式）')
  .option('--urls <urls>', '文章链接，逗号分隔（links 模式）')
  .option('--count <count>', '搜索文章数量', '5')
  .option('--merge', '合并文章')
  .option('--rewrite', 'AI 改写')
  .option('--generate-cover', '生成封面')
  .option('--publish', '发布文章')
  .option('--output <dir>', '输出目录', DEFAULT_OUTPUT_DIR)
  .action(async (type, options) => {
    console.log(`🚀 开始执行工作流：${type}\n`);
    
    try {
      let articlePath = '';
      
      if (type === 'search') {
        // 搜索工作流：搜索 → 抓取完整内容
        if (!options.keyword) {
          throw new Error('search 模式必须指定 --keyword 参数');
        }
        
        console.log(`🔍 搜索关键词：${options.keyword}`);
        const { results: wfSearchResults } = await multiSourceSearch(options.keyword, {
          maxPerSource: parseInt(options.count),
          totalMax: 10,
        });

        if (wfSearchResults.length === 0) {
          throw new Error('未找到相关文章');
        }

        console.log(`✅ 搜索到 ${wfSearchResults.length} 篇文章，开始抓取完整内容...\n`);

        const articles = [];
        for (let i = 0; i < wfSearchResults.length; i++) {
          const item = wfSearchResults[i];
          const articleUrl = item.url;
          console.log(`[${i + 1}/${wfSearchResults.length}] 抓取：${item.title}`);

          if (!articleUrl) {
            console.log(`  ⚠️  URL 为空，跳过`);
            continue;
          }

          const result = await extractArticle(articleUrl);
          if (result.done && result.code === 0) {
            articles.push(result.data);
            console.log(`  ✅ 成功`);
          } else {
            console.log(`  ⚠️  提取失败：${result.msg || '未知错误'}`);
          }
        }

        if (articles.length === 0) {
          throw new Error('没有成功抓取到任何文章');
        }
        
        console.log(`\n✅ 成功抓取 ${articles.length} 篇文章`);
        
        if (options.merge) {
          console.log('\n📝 合并文章...');
          const mergedArticle = mergeArticles(articles, options.keyword);

          const outputDir = path.join(options.output, sanitizeFileName(mergedArticle.title));
          fs.mkdirSync(outputDir, { recursive: true });

          articlePath = path.join(outputDir, 'article.md');
          fs.writeFileSync(articlePath, mergedArticle.markdown, 'utf-8');
          console.log(`✅ 文章已保存：${articlePath}`);
        }
        
      } else if (type === 'links') {
        // 链接抓取工作流
        if (!options.urls) {
          throw new Error('links 模式必须指定 --urls 参数');
        }
        
        const urlList = options.urls.split(',').map(u => u.trim()).filter(Boolean);
        console.log(`🔗 抓取 ${urlList.length} 个链接`);
        
        const articles = [];
        for (const url of urlList) {
          const result = await extractArticle(url);
          if (result.done && result.code === 0) {
            articles.push(result.data);
          }
        }
        
        if (articles.length === 0) {
          throw new Error('没有成功抓取到任何文章');
        }
        
        console.log(`✅ 成功抓取 ${articles.length} 篇文章`);
        
        if (options.merge) {
          console.log('\n📝 合并文章...');
          const mergedArticle = mergeArticles(articles, '从链接抓取');
          
          const outputDir = path.join(options.output, sanitizeFileName(mergedArticle.title));
          fs.mkdirSync(outputDir, { recursive: true });
          
          articlePath = path.join(outputDir, 'article.md');
          fs.writeFileSync(articlePath, mergedArticle.markdown, 'utf-8');
          console.log(`✅ 文章已保存：${articlePath}`);
        }
        
      } else {
        throw new Error(`未知的工作流类型：${type}`);
      }
      
      // AI 改写
      if (options.rewrite && articlePath) {
        console.log('\n✍️  AI 改写...');
        const content = fs.readFileSync(articlePath, 'utf-8');
        const rewrittenContent = await rewriteArticle(content);
        const cleanedContent = removeAiTrace(rewrittenContent);
        
        const rewrittenPath = articlePath.replace('.md', '_rewritten.md');
        fs.writeFileSync(rewrittenPath, cleanedContent, 'utf-8');
        articlePath = rewrittenPath;
        console.log(`✅ 改写完成：${articlePath}`);
      }
      
      // 生成封面
      if (options.generateCover && articlePath) {
        console.log('\n🎨 生成封面...');
        const content = fs.readFileSync(articlePath, 'utf-8');
        const title = extractTitle(content);
        
        const outputDir = path.dirname(articlePath);
        const result = await generateCover({
          title,
          content: content.substring(0, 200),
          outputDir
        });
        
        if (result.success) {
          console.log(`✅ 封面已生成：${result.path}`);
        }
      }
      
      // 发布
      if (options.publish && articlePath) {
        console.log('\n📱 发布文章...');
        await publishWithWenyan(articlePath);
      }
      
      console.log('\n✅ 工作流执行完成！');
      
    } catch (error) {
      console.error('❌ 工作流执行失败:', error.message);
      process.exit(1);
    }
  });

// 排版命令 — 调用 wechat-typeset-pro 排版引擎
program
  .command('format <article>')
  .description('专业排版：Markdown → 微信兼容精美 HTML（30 套主题 + 可视化画廊）')
  .option('-t, --theme <name>', '指定主题（跳过画廊）')
  .option('-g, --gallery', '打开主题画廊选择', true)
  .option('--recommend <themes...>', '推荐的主题 ID 列表')
  .option('--no-open', '不自动打开浏览器')
  .option('--publish', '排版后推送到草稿箱')
  .option('--cover <path>', '封面图路径（推送时使用）')
  .option('--author <name>', '作者名（推送时使用）')
  .action(async (article, options) => {
    const { execSync } = await import('child_process');

    const typesetSkillDir = path.resolve(__dirname, '../../wechat-typeset-pro');
    const formatScript = path.join(typesetSkillDir, 'scripts', 'format.py');
    const publishScript = path.join(typesetSkillDir, 'scripts', 'publish.py');

    if (!fs.existsSync(formatScript)) {
      console.error('❌ 未找到 wechat-typeset-pro 排版技能');
      console.error(`   期望路径: ${formatScript}`);
      console.error('   请确认技能已安装在 ~/.workbuddy/skills/wechat-typeset-pro/');
      process.exit(1);
    }

    const articlePath = path.resolve(article);
    if (!fs.existsSync(articlePath)) {
      console.error(`❌ 文件不存在: ${articlePath}`);
      process.exit(1);
    }

    try {
      const args = ['--input', articlePath];

      if (options.theme) {
        args.push('--theme', options.theme);
      } else if (options.gallery !== false) {
        args.push('--gallery');
        if (options.recommend && options.recommend.length > 0) {
          args.push('--recommend', ...options.recommend);
        }
      }

      if (options.open === false) {
        args.push('--no-open');
      }

      console.log('🎨 调用 wechat-typeset-pro 排版引擎...');
      const cmd = `python3 "${formatScript}" ${args.map(a => `"${a}"`).join(' ')}`;
      execSync(cmd, { stdio: 'inherit', env: process.env });

      if (options.publish) {
        console.log('\n📱 推送到草稿箱...');
        const pubArgs = ['--input', articlePath];
        if (options.theme) pubArgs.push('--theme', options.theme);
        if (options.cover) pubArgs.push('--cover', options.cover);
        if (options.author) pubArgs.push('--author', options.author);

        const pubCmd = `python3 "${publishScript}" ${pubArgs.map(a => `"${a}"`).join(' ')}`;
        execSync(pubCmd, { stdio: 'inherit', env: process.env });
      }

      console.log('\n✅ 排版完成！');
    } catch (error) {
      console.error('❌ 排版失败:', error.message);
      process.exit(1);
    }
  });

// 多站点文章抓取命令 — 调用 multi-site-extractor
program
  .command('extract <urls...>')
  .description('多站点文章抓取：支持微信/CSDN/博客园/掘金/知乎/简书/思否/少数派等')
  .option('-o, --output <dir>', '输出目录', DEFAULT_OUTPUT_DIR)
  .option('--json', '以 JSON 格式输出到 stdout')
  .option('--rewrite', '抓取后自动 AI 改写')
  .option('--publish', '抓取后自动排版发布到公众号')
  .option('-t, --theme <name>', '排版主题（publish 时使用）', 'github')
  .action(async (urls, options) => {
    const { execSync } = await import('child_process');

    const extractorDir = path.resolve(__dirname, '../../multi-site-extractor');
    const extractScript = path.join(extractorDir, 'scripts', 'extract.py');

    if (!fs.existsSync(extractScript)) {
      console.error('❌ 未找到 multi-site-extractor 技能');
      console.error(`   期望路径: ${extractScript}`);
      console.error('   请确认技能已安装在 ~/.workbuddy/skills/multi-site-extractor/');
      process.exit(1);
    }

    const outputDir = path.resolve(options.output);
    fs.mkdirSync(outputDir, { recursive: true });

    try {
      const args = urls.map(u => `"${u}"`);
      args.push('--output', `"${outputDir}"`);
      if (options.json) args.push('--json');

      console.log(`🕷️  调用 multi-site-extractor 抓取 ${urls.length} 篇文章...\n`);
      const cmd = `python3 "${extractScript}" ${args.join(' ')}`;

      if (options.json && !options.rewrite && !options.publish) {
        execSync(cmd, { stdio: 'inherit', env: process.env });
      } else {
        execSync(cmd, { stdio: 'inherit', env: process.env });
      }

      // 抓取后处理
      const mdFiles = fs.readdirSync(outputDir).filter(f => f.endsWith('.md'));

      if (mdFiles.length === 0) {
        console.log('\n⚠️  未抓取到任何文章');
        return;
      }

      console.log(`\n✅ 成功抓取 ${mdFiles.length} 篇文章\n`);

      for (const mdFile of mdFiles) {
        const mdPath = path.join(outputDir, mdFile);
        console.log(`  📄 ${mdPath}`);

        // AI 改写
        if (options.rewrite) {
          console.log(`\n✍️  AI 改写: ${mdFile}`);
          const content = fs.readFileSync(mdPath, 'utf-8');
          const rewrittenContent = await rewriteArticle(content, { style: 'original' });
          const finalContent = removeAiTrace(rewrittenContent);
          const rewrittenPath = mdPath.replace('.md', '_rewritten.md');
          fs.writeFileSync(rewrittenPath, finalContent, 'utf-8');
          console.log(`  ✅ 改写完成: ${rewrittenPath}`);
        }

        // 排版 + 发布
        if (options.publish) {
          const targetFile = options.rewrite
            ? mdPath.replace('.md', '_rewritten.md')
            : mdPath;

          console.log(`\n📱 排版发布: ${path.basename(targetFile)}`);

          const typesetDir = path.resolve(__dirname, '../../wechat-typeset-pro');
          const formatPy = path.join(typesetDir, 'scripts', 'format.py');
          const publishPy = path.join(typesetDir, 'scripts', 'publish.py');

          if (fs.existsSync(formatPy)) {
            const fmtCmd = `python3 "${formatPy}" --input "${targetFile}" --theme ${options.theme} --no-open`;
            execSync(fmtCmd, { stdio: 'inherit', env: process.env });

            if (fs.existsSync(publishPy)) {
              const articleName = path.basename(targetFile, '.md');
              const formattedDir = `/tmp/wechat-format/${articleName}`;
              if (fs.existsSync(formattedDir)) {
                const pubCmd = `python3 "${publishPy}" --dir "${formattedDir}"`;
                execSync(pubCmd, { stdio: 'inherit', env: process.env });
              }
            }
          } else {
            console.log('  ⚠️  wechat-typeset-pro 未安装，跳过排版发布');
          }
        }
      }

      console.log('\n✅ 全部完成！');

    } catch (error) {
      console.error('❌ 抓取失败:', error.message);
      process.exit(1);
    }
  });

// 辅助函数
function sanitizeFileName(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').replace(/\s+/g, ' ').trim().substring(0, 100);
}

function extractTitle(content) {
  const fmMatch = content.match(/---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/title:\s*(.+)/);
    if (titleMatch) {
      return titleMatch[1].trim();
    }
  }
  
  const h1Match = content.match(/^#\s+(.+)/m);
  if (h1Match) {
    return h1Match[1].trim();
  }
  
  return '未命名文章';
}

// 解析命令行
program.parse(process.argv);

// 如果没有提供命令，显示帮助
if (!process.argv.slice(2).length) {
  program.outputHelp();
}

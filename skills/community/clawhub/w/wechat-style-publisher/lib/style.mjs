import fs from "node:fs/promises";
import path from "node:path";
import hljs from "highlight.js";
import juice from "juice";

export const THEMES = {
  "modern-minimal": `
.wechat-content {
  font-size: 16px;
  color: #3f3f3f;
  line-height: 1.75;
  letter-spacing: 0.05em;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
}
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; padding: 0; font-weight: bold; color: #2b2b2b; }
.wechat-content h1 { font-size: 24px; padding-bottom: 8px; border-bottom: 1px solid #3eaf7c; color: #2b2b2b; }
.wechat-content h2 { font-size: 22px; padding: 8px 12px; background-color: #f8f8f8; color: #3eaf7c; border: none; }
.wechat-content h3 { font-size: 20px; padding-left: 10px; border-left: 2px solid #3eaf7c; }
.wechat-content h4 { font-size: 18px; }
.wechat-content h5 { font-size: 16px; }
.wechat-content h6 { font-size: 16px; color: #777; }
.wechat-content p { margin: 15px 0; line-height: 1.75; }
.wechat-content a { color: #3eaf7c; text-decoration: none; border-bottom: 1px solid #3eaf7c; }
.wechat-content ul, .wechat-content ol { margin: 15px 0; padding-left: 30px; }
.wechat-content li { margin: 8px 0; line-height: 1.75; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #f8f8f8; border-left: 3px solid #3eaf7c; color: #666; font-style: italic; }
.wechat-content blockquote p { margin: 0; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #f5f5f5; border-radius: 3px; overflow-x: auto; border: 1px solid #e0e0e0; }
.wechat-content code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; background-color: #f0f0f0; padding: 2px 6px; border-radius: 3px; color: #d73a49; }
.wechat-content pre code { display: block; padding: 0; background-color: transparent; color: #333; line-height: 1.5; }
.wechat-content table { margin: 20px 0; border-collapse: collapse; width: 100%; font-size: 14px; }
.wechat-content table th, .wechat-content table td { padding: 10px 15px; border: 1px solid #dfe2e5; text-align: left; }
.wechat-content table th { background-color: #f6f8fa; font-weight: bold; color: #2b2b2b; }
.wechat-content table tr:nth-child(even) { background-color: #f8f8f8; }
.wechat-content hr { margin: 30px 0; border: none; border-top: 1px solid #eee; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 3px; }
.wechat-content strong { font-weight: bold; color: #2b2b2b; }
.wechat-content em { font-style: italic; }
.wechat-content del { text-decoration: line-through; color: #999; }
.wechat-content mark { background-color: #3eaf7c; color: #ffffff; padding: 2px 4px; border-radius: 2px; }
`,
  "tech-future": `
.wechat-content {
  font-size: 16px; color: #1a202c; line-height: 1.75; letter-spacing: 0.05em;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
}
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; padding: 0; font-weight: bold; color: #0f172a; }
.wechat-content h1 { font-size: 24px; padding: 15px 25px; background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%); color: #ffffff; border: none; border-radius: 8px; box-shadow: 0 4px 20px rgba(139, 92, 246, 0.5), 0 0 30px rgba(6, 182, 212, 0.4); }
.wechat-content h2 { font-size: 22px; padding: 12px 20px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%); border-left: 5px solid; border-image: linear-gradient(to bottom, #06b6d4, #8b5cf6) 1; border-radius: 0 6px 6px 0; }
.wechat-content h3 { font-size: 20px; padding-left: 15px; border-left: 4px solid #06b6d4; }
.wechat-content h4 { font-size: 18px; color: #0891b2; }
.wechat-content h5 { font-size: 16px; }
.wechat-content h6 { font-size: 16px; color: #777; }
.wechat-content p { margin: 15px 0; line-height: 1.75; }
.wechat-content a { color: #0891b2; text-decoration: none; border-bottom: 2px solid #06b6d4; }
.wechat-content ul, .wechat-content ol { margin: 15px 0; padding-left: 30px; }
.wechat-content li { margin: 8px 0; line-height: 1.75; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); border-left: 5px solid; border-image: linear-gradient(to bottom, #06b6d4, #8b5cf6) 1; color: #475569; font-style: italic; border-radius: 0 8px 8px 0; }
.wechat-content blockquote p { margin: 0; }
.wechat-content pre { margin: 20px 0; padding: 20px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 8px; overflow-x: auto; border: 1px solid #06b6d4; }
.wechat-content code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.15)); padding: 3px 8px; border-radius: 4px; color: #0891b2; border: 1px solid rgba(6, 182, 212, 0.3); }
.wechat-content pre code { display: block; padding: 0; background-color: transparent; color: #cbd5e1; line-height: 1.6; border: none; }
.wechat-content table { margin: 20px 0; border-collapse: collapse; width: 100%; font-size: 14px; }
.wechat-content table th, .wechat-content table td { padding: 10px 15px; border: 1px solid #dfe2e5; text-align: left; }
.wechat-content table th { background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%); font-weight: bold; color: #ffffff; }
.wechat-content table tr:nth-child(even) { background-color: #f8f8f8; }
.wechat-content hr { margin: 30px 0; border: none; height: 2px; background: linear-gradient(90deg, transparent, #06b6d4, #8b5cf6, transparent); }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; }
.wechat-content strong { font-weight: bold; color: #0f172a; background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1)); padding: 0 4px; border-radius: 2px; }
.wechat-content em { font-style: italic; }
.wechat-content del { text-decoration: line-through; color: #999; }
.wechat-content mark { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #ffffff; padding: 3px 8px; border-radius: 4px; }
`,
  "warm-orange": `
.wechat-content {
  font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
}
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; padding: 0; font-weight: bold; color: #2b2b2b; }
.wechat-content h1 { font-size: 24px; padding: 12px 20px; background-color: #ff6b35; color: #ffffff; border: none; }
.wechat-content h2 { font-size: 22px; padding: 10px 16px 10px 20px; background-color: #fff3ed; border-left: 4px solid #ff6b35; color: #ff6b35; }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 4px solid #ff6b35; }
.wechat-content h4 { font-size: 18px; }
.wechat-content h5 { font-size: 16px; }
.wechat-content h6 { font-size: 16px; color: #777; }
.wechat-content p { margin: 15px 0; line-height: 1.75; }
.wechat-content a { color: #ff6b35; text-decoration: none; border-bottom: 1px solid #ff6b35; }
.wechat-content ul, .wechat-content ol { margin: 15px 0; padding-left: 30px; }
.wechat-content li { margin: 8px 0; line-height: 1.75; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #fff3ed; border-left: 4px solid #ff6b35; color: #666; font-style: italic; }
.wechat-content blockquote p { margin: 0; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2c2c2c; border-radius: 5px; overflow-x: auto; border: none; }
.wechat-content code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; background-color: #fff3ed; padding: 2px 6px; border-radius: 3px; color: #ff6b35; }
.wechat-content pre code { display: block; padding: 0; background-color: transparent; color: #abb2bf; line-height: 1.5; }
.wechat-content table { margin: 20px 0; border-collapse: collapse; width: 100%; font-size: 14px; }
.wechat-content table th, .wechat-content table td { padding: 10px 15px; border: 1px solid #dfe2e5; text-align: left; }
.wechat-content table th { background-color: #ff6b35; font-weight: bold; color: #ffffff; }
.wechat-content table tr:nth-child(even) { background-color: #fff3ed; }
.wechat-content hr { margin: 30px 0; border: none; border-top: 1px solid #eee; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px; }
.wechat-content strong { font-weight: bold; color: #2b2b2b; }
.wechat-content em { font-style: italic; }
.wechat-content del { text-decoration: line-through; color: #999; }
.wechat-content mark { background-color: #ff6b35; color: #ffffff; padding: 2px 4px; border-radius: 2px; }
`,
  "fresh-green": `
.wechat-content {
  font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
}
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; padding: 0; font-weight: bold; color: #2b2b2b; }
.wechat-content h1 { font-size: 24px; padding-bottom: 12px; border-bottom: 3px solid #42b983; color: #2b2b2b; text-align: center; }
.wechat-content h2 { font-size: 22px; padding: 10px 16px; background: linear-gradient(to right, #42b983 0%, #85d7b3 100%); color: #ffffff; border: none; border-radius: 4px; }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 4px solid #42b983; }
.wechat-content h4 { font-size: 18px; }
.wechat-content h5 { font-size: 16px; }
.wechat-content h6 { font-size: 16px; color: #777; }
.wechat-content p { margin: 15px 0; line-height: 1.75; }
.wechat-content a { color: #42b983; text-decoration: none; border-bottom: 1px solid #42b983; }
.wechat-content ul, .wechat-content ol { margin: 15px 0; padding-left: 30px; }
.wechat-content li { margin: 8px 0; line-height: 1.75; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #f0faf6; border-left: 4px solid #42b983; color: #666; font-style: italic; }
.wechat-content blockquote p { margin: 0; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2c2c2c; border-radius: 5px; overflow-x: auto; border: none; }
.wechat-content code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; background-color: #f0faf6; padding: 2px 6px; border-radius: 3px; color: #42b983; }
.wechat-content pre code { display: block; padding: 0; background-color: transparent; color: #abb2bf; line-height: 1.5; }
.wechat-content table { margin: 20px 0; border-collapse: collapse; width: 100%; font-size: 14px; }
.wechat-content table th, .wechat-content table td { padding: 10px 15px; border: 1px solid #dfe2e5; text-align: left; }
.wechat-content table th { background-color: #42b983; font-weight: bold; color: #ffffff; }
.wechat-content table tr:nth-child(even) { background-color: #f0faf6; }
.wechat-content hr { margin: 30px 0; border: none; border-top: 1px solid #eee; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px; }
.wechat-content strong { font-weight: bold; color: #2b2b2b; }
.wechat-content em { font-style: italic; }
.wechat-content del { text-decoration: line-through; color: #999; }
.wechat-content mark { background-color: #42b983; color: #ffffff; padding: 2px 4px; border-radius: 2px; }
`,
  "elegant-violet": `
.wechat-content {
  font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
}
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; padding: 0; font-weight: bold; color: #2b2b2b; }
.wechat-content h1 { font-size: 24px; padding-bottom: 12px; border-bottom: 3px solid #9b59b6; color: #2b2b2b; text-align: center; font-weight: 600; }
.wechat-content h2 { font-size: 22px; padding: 10px 16px; background: linear-gradient(135deg, #9b59b6 0%, #c39bd3 100%); color: #ffffff; border: none; border-radius: 4px; box-shadow: 0 2px 8px rgba(155, 89, 182, 0.3); }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 4px solid #9b59b6; }
.wechat-content h4 { font-size: 18px; }
.wechat-content h5 { font-size: 16px; }
.wechat-content h6 { font-size: 16px; color: #777; }
.wechat-content p { margin: 15px 0; line-height: 1.75; }
.wechat-content a { color: #9b59b6; text-decoration: none; border-bottom: 1px solid #9b59b6; }
.wechat-content ul, .wechat-content ol { margin: 15px 0; padding-left: 30px; }
.wechat-content li { margin: 8px 0; line-height: 1.75; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #f8f5fb; border-left: 4px solid #9b59b6; color: #666; font-style: italic; }
.wechat-content blockquote p { margin: 0; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2d2438; border-radius: 5px; overflow-x: auto; border: none; }
.wechat-content code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; background-color: #f8f5fb; padding: 2px 6px; border-radius: 3px; color: #9b59b6; }
.wechat-content pre code { display: block; padding: 0; background-color: transparent; color: #c9a7d8; line-height: 1.5; }
.wechat-content table { margin: 20px 0; border-collapse: collapse; width: 100%; font-size: 14px; }
.wechat-content table th, .wechat-content table td { padding: 10px 15px; border: 1px solid #dfe2e5; text-align: left; }
.wechat-content table th { background-color: #9b59b6; font-weight: bold; color: #ffffff; }
.wechat-content table tr:nth-child(even) { background-color: #f8f5fb; }
.wechat-content hr { margin: 30px 0; border: none; border-top: 1px solid #eee; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px; }
.wechat-content strong { font-weight: bold; color: #2b2b2b; }
.wechat-content em { font-style: italic; }
.wechat-content del { text-decoration: line-through; color: #999; }
.wechat-content mark { background-color: #9b59b6; color: #ffffff; padding: 2px 4px; border-radius: 2px; }
`,
  "chinese-style": `
.wechat-content {
  font-size: 16px; color: #2c2c2c; line-height: 1.8; letter-spacing: 0.05em;
  font-family: "STSong", "SimSun", "Songti SC", "NSimSun", serif, -apple-system, BlinkMacSystemFont;
}
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; padding: 0; font-weight: bold; color: #2c2c2c; }
.wechat-content h1 { font-size: 24px; padding: 16px 30px; background: linear-gradient(to bottom, #f5e6d3 0%, #efe0c8 50%, #f5e6d3 100%); color: #c8161d; border: none; text-align: center; letter-spacing: 0.15em; border-top: 2px solid #c8161d; border-bottom: 2px solid #c8161d; }
.wechat-content h2 { font-size: 22px; padding: 10px 20px; border-left: 4px solid #c8161d; color: #c8161d; background: linear-gradient(to right, rgba(200, 22, 29, 0.05) 0%, transparent 100%); }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 3px solid #c8161d; }
.wechat-content h4 { font-size: 18px; }
.wechat-content h5 { font-size: 16px; }
.wechat-content h6 { font-size: 16px; color: #777; }
.wechat-content p { margin: 15px 0; line-height: 1.8; }
.wechat-content a { color: #c8161d; text-decoration: none; border-bottom: 1px solid #c8161d; }
.wechat-content ul, .wechat-content ol { margin: 15px 0; padding-left: 30px; }
.wechat-content li { margin: 8px 0; line-height: 1.8; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background: linear-gradient(to right, #faf8f3 0%, #f5f0e8 100%); border-left: 4px solid #c8161d; border-right: 4px solid #c8161d; color: #666; }
.wechat-content blockquote p { margin: 0; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2c2c2c; border-radius: 3px; overflow-x: auto; border: 1px solid #c8161d; }
.wechat-content code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; background-color: #faf8f3; padding: 2px 6px; border-radius: 3px; color: #c8161d; }
.wechat-content pre code { display: block; padding: 0; background-color: transparent; color: #abb2bf; line-height: 1.5; }
.wechat-content table { margin: 20px 0; border-collapse: collapse; width: 100%; font-size: 14px; }
.wechat-content table th, .wechat-content table td { padding: 10px 15px; border: 1px solid #dfe2e5; text-align: left; }
.wechat-content table th { background-color: #c8161d; font-weight: bold; color: #ffffff; }
.wechat-content table tr:nth-child(even) { background-color: #faf8f3; }
.wechat-content hr { margin: 30px 0; border: none; height: 1px; background: linear-gradient(to right, transparent, #c8161d, transparent); }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 3px; }
.wechat-content strong { font-weight: bold; color: #c8161d; }
.wechat-content em { font-style: italic; }
.wechat-content del { text-decoration: line-through; color: #999; }
.wechat-content mark { background-color: #c8161d; color: #ffffff; padding: 2px 4px; border-radius: 2px; }
`
};

const HIGHLIGHT_CSS = `
.hljs { display: block; overflow-x: auto; }
.hljs-comment, .hljs-quote { color: #5c6370; font-style: italic; }
.hljs-doctag, .hljs-keyword, .hljs-formula { color: #c678dd; }
.hljs-section, .hljs-name, .hljs-selector-tag, .hljs-deletion, .hljs-subst { color: #e06c75; }
.hljs-literal { color: #56b6c2; }
.hljs-string, .hljs-regexp, .hljs-addition, .hljs-attribute, .hljs-meta-string { color: #98c379; }
.hljs-built_in, .hljs-class .hljs-title { color: #e6c07b; }
.hljs-attr, .hljs-variable, .hljs-template-variable, .hljs-type, .hljs-selector-class, .hljs-selector-attr, .hljs-selector-pseudo, .hljs-number { color: #d19a66; }
.hljs-symbol, .hljs-bullet, .hljs-link, .hljs-meta, .hljs-selector-id, .hljs-title { color: #61aeee; }
.hljs-emphasis { font-style: italic; }
.hljs-strong { font-weight: bold; }
.hljs-link { text-decoration: underline; }
`;

export function decodeHtmlEntities(input) {
  return input
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", "\"")
    .replaceAll("&#39;", "'")
    .replaceAll("&amp;", "&");
}

export function highlightCodeBlocks(html) {
  return html.replace(/<pre>\s*<code([^>]*)>([\s\S]*?)<\/code>\s*<\/pre>/gi, (_, attrs, code) => {
    const classMatch = attrs.match(/class=["'][^"']*language-([a-z0-9#+-]+)[^"']*["']/i);
    const source = decodeHtmlEntities(code);
    let highlighted = "";

    if (classMatch) {
      const language = classMatch[1].toLowerCase();
      if (hljs.getLanguage(language)) {
        highlighted = hljs.highlight(source, { language }).value;
      }
    }

    if (!highlighted) {
      highlighted = hljs.highlightAuto(source).value;
    }

    return `<pre><code class="hljs">${highlighted}</code></pre>`;
  });
}

export async function readOptionalText(filePath) {
  if (!filePath) {
    return "";
  }
  return fs.readFile(path.resolve(filePath), "utf8");
}

export async function buildArticleHtml({
  html,
  theme = "modern-minimal",
  cssFile = "",
  customCss = "",
  introHtml = "",
  outroHtml = ""
}) {
  const themeCss = THEMES[theme];
  if (!themeCss) {
    throw new Error(`Unknown theme: ${theme}`);
  }

  const segments = [introHtml, html, outroHtml].filter(Boolean).join("\n");
  const wrapped = `<div class="wechat-content">${segments}</div>`;
  const highlighted = highlightCodeBlocks(wrapped);
  const fileCss = await readOptionalText(cssFile);
  const css = [themeCss, HIGHLIGHT_CSS, fileCss, customCss].filter(Boolean).join("\n");

  return juice.inlineContent(highlighted, css, {
    applyStyleTags: true,
    removeStyleTags: true,
    preserveMediaQueries: false,
    preserveFontFaces: false
  });
}

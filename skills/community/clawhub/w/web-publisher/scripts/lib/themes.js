'use strict';
// IDs are the server 0.8.0 theme catalog; unknown IDs pass through for server validation.
const THEMES = [
 ['astranotes','暖纸叙事'],['blackink','墨黑'],['fieldnotes','蓝图笔记'],['clinical','青禾医学'],
 ['default','默认'],['orangesun','橙日'],['redruby','红宝石'],['greenmint','薄荷绿'],
 ['purplerain','紫雨'],['paperjournal','纸上刊物'],['clearguide','清晰指南'],['intelligence','智序']
].map(([id,name])=>({id,name}));
function normalizeTheme(value) {
 if(!value)return 'blackink';
 if(value==='warmeditorial'||value==='暖调手记')return 'astranotes';
 if(value==='默认主题')return 'default';
 return THEMES.find(t=>t.name===value)?.id||value;
}
module.exports={THEMES,normalizeTheme};

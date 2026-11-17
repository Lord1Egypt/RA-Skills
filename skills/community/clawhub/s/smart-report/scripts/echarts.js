// 把内置 echarts.min.js 暴露为 CommonJS 'echarts' 模块，供 wordcloud/liquidfill 插件 require('echarts') 解析
module.exports = require('../assets/echarts.min.js');
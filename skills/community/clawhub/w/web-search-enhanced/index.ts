import { Tool, ToolContext, ToolOutput, ToolError } from "openclaw/tool";
import { webFetch } from "openclaw/web";

const TEMP_RESULTS_FILE = ".web-search-temp-results.md";

export class WebSearchEnhanced extends Tool {
  async run(
    context: ToolContext,
    userMessage: string,
  ): Promise<ToolOutput | ToolError> {
    try {
      // 提取搜索关键词
      const query = userMessage.replace(/^[帮|查|搜]我/, "").trim();
      
      if (!query) {
        return ToolError.from("请输入要搜索的内容");
      }

      // 检查是否有临时结果
      const tempResults = await this.loadTempResults();
      
      if (tempResults && tempResults.length > 0) {
        // 有临时结果，继续搜索
        const newResults = await this.searchQuery(query);
        
        // 合并结果
        const allResults = [...tempResults, ...newResults];
        
        // 保存最终结果
        await this.saveTempResults(allResults);
        
        // 清理临时文件
        await this.cleanupTempResults();
        
        return ToolOutput.from(`搜索完成！共找到 ${allResults.length} 个结果：\n\n${allResults.join("\n\n")}`);
      } else {
        // 没有临时结果，开始新搜索
        const results = await this.searchQuery(query);
        
        // 保存结果
        await this.saveTempResults(results);
        
        // 清理临时文件
        await this.cleanupTempResults();
        
        return ToolOutput.from(`搜索完成！共找到 ${results.length} 个结果：\n\n${results.join("\n\n")}`);
      }
    } catch (error) {
      return ToolError.from(`搜索失败：${error.message}`);
    }
  }

  private async searchQuery(query: string): Promise<string[]> {
    const results: string[] = [];
    const batchSize = 5; // 每批处理 5 个结果
    
    for (let i = 0; i < 10; i += batchSize) {
      const batchResults = [];
      
      // 模拟分批搜索
      for (let j = 0; j < batchSize && i + j < 10; j++) {
        const page = i + j + 1;
        const result = `[第${page}页搜索结果] ${query}\n来源：模拟网页${i + j + 1}\n内容：这里是模拟的搜索结果内容...`;
        batchResults.push(result);
      }
      
      // 保存当前批次的结果
      await this.saveTempResults([...(await this.loadTempResults()), ...batchResults]);
    }
    
    return await this.loadTempResults();
  }

  private async loadTempResults(): Promise<string[]> {
    try {
      const content = await this.readFile(TEMP_RESULTS_FILE);
      // 分割结果
      return content
        .split("### 搜索结果 ###")
        .filter(r => r.trim().length > 0)
        .map(r => r.trim());
    } catch {
      return [];
    }
  }

  private async saveTempResults(results: string[]): Promise<void> {
    const content = `### 搜索结果 ###\n${results.join("\n\n")}`;
    await this.writeFile(TEMP_RESULTS_FILE, content);
  }

  private async cleanupTempResults(): Promise<void> {
    try {
      await this.removeFile(TEMP_RESULTS_FILE);
    } catch {
      // 忽略清理失败
    }
  }

  private async readFile(path: string): Promise<string> {
    try {
      return await webFetch(path, { extractMode: "text" });
    } catch {
      throw new Error("文件不存在");
    }
  }

  private async writeFile(path: string, content: string): Promise<void> {
    const fs = require("fs");
    fs.writeFileSync(path, content);
  }

  private async removeFile(path: string): Promise<void> {
    const fs = require("fs");
    try {
      fs.unlinkSync(path);
    } catch {
      // 忽略
    }
  }
}

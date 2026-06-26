package main

import (
	"bytes"
	"compress/gzip"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"time"
)

// StockRank 股票排名信息
type StockRank struct {
	Rank      int    `json:"rank"`
	Code      string `json:"code"`
	Name      string `json:"name"`
	HeatScore int    `json:"heat_score"`
	Source    string `json:"source"`
}

// CompositeRank 复合排名
type CompositeRank struct {
	Code           string  `json:"code"`
	Name           string  `json:"name"`
	WencaiRank     int     `json:"wencai_rank"`
	XueqiuRank     int     `json:"xueqiu_rank"`
	EastmoneyRank  int     `json:"eastmoney_rank"`
	CompositeScore float64 `json:"composite_score"`
	AppearCount    int     `json:"appear_count"`
}

// WencaiClient 问财客户端
type WencaiClient struct {
	client   *http.Client
	cookies  []*http.Cookie
	otherUID string
	jsPath   string
}

// NewWencaiClient 创建问财客户端
func NewWencaiClient() *WencaiClient {
	exePath, _ := os.Executable()
	exeDir := filepath.Dir(exePath)

	jsPath := filepath.Join(exeDir, "lib", "hexin_v.js")
	if _, err := os.Stat(jsPath); os.IsNotExist(err) {
		jsPath, _ = filepath.Abs("lib/hexin_v.js")
	}

	return &WencaiClient{
		client: &http.Client{
			Timeout: 30 * time.Second,
		},
		otherUID: "Ths_iwencai_Xuangu_" + randString(32),
		jsPath:   jsPath,
	}
}

// Fetch 获取问财人气排名
func (c *WencaiClient) Fetch(top int) ([]StockRank, error) {
	c.initCookies()

	fmt.Println("→ 访问问财主页...")
	c.visitMain()
	time.Sleep(300 * time.Millisecond)

	fmt.Println("→ 访问搜索页...")
	c.visitSearch()
	time.Sleep(300 * time.Millisecond)

	fmt.Println("→ 初始化会话...")
	c.visitHint()
	time.Sleep(300 * time.Millisecond)

	fmt.Println("→ 获取人气排名数据...")
	return c.getData(top)
}

func (c *WencaiClient) initCookies() {
	c.cookies = []*http.Cookie{
		{Name: "other_uid", Value: c.otherUID},
		{Name: "ta_random_userid", Value: randString(10)},
		{Name: "v", Value: ""},
	}
}

func (c *WencaiClient) visitMain() {
	req, _ := http.NewRequest("GET", "https://www.iwencai.com", nil)
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")

	resp, err := c.client.Do(req)
	if err == nil {
		resp.Body.Close()
		for _, cookie := range resp.Cookies() {
			c.cookies = append(c.cookies, cookie)
		}
	}
}

func (c *WencaiClient) visitSearch() {
	req, _ := http.NewRequest("GET", "https://www.iwencai.com/unifiedwap/home/index", nil)
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")
	req.Header.Set("Referer", "https://www.iwencai.com")

	resp, err := c.client.Do(req)
	if err == nil {
		resp.Body.Close()
		for _, cookie := range resp.Cookies() {
			c.cookies = append(c.cookies, cookie)
		}
	}
}

func (c *WencaiClient) visitHint() {
	form := url.Values{}
	form.Set("dataType", "history")
	form.Set("isAll", "1")
	form.Set("num", "20")
	form.Set("queryType", "index")
	form.Set("relatedId", "")

	req, _ := http.NewRequest("POST", "https://www.iwencai.com/unifiedwap/suggest/V1/index/query-hint-list", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "application/json, text/plain, */*")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")
	req.Header.Set("Origin", "https://www.iwencai.com")
	req.Header.Set("Referer", "https://www.iwencai.com/unifiedwap/home/index")

	hexinV := c.generateHexinV()
	req.Header.Set("Hexin-V", hexinV)

	for i, cookie := range c.cookies {
		if cookie.Name == "v" {
			c.cookies[i].Value = hexinV
		}
	}

	for _, cookie := range c.cookies {
		req.AddCookie(cookie)
	}

	resp, err := c.client.Do(req)
	if err == nil {
		resp.Body.Close()
	}
}

func (c *WencaiClient) getData(top int) ([]StockRank, error) {
	query := fmt.Sprintf("人气排名前%d", top)

	payload := map[string]interface{}{
		"source":           "Ths_iwencai_Xuangu",
		"version":          "2.0",
		"query_area":       "",
		"block_list":       "",
		"add_info":         `{"urp":{"scene":1,"company":1,"business":1},"contentType":"json","searchInfo":true}`,
		"question":         query,
		"perpage":          top,
		"page":             1,
		"secondary_intent": "",
		"log_info":         `{"input_type":"typewrite"}`,
		"rsh":              c.otherUID,
	}

	jsonData, _ := json.Marshal(payload)

	req, _ := http.NewRequest("POST", "https://www.iwencai.com/customized/chart/get-robot-data", strings.NewReader(string(jsonData)))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "application/json, text/plain, */*")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")
	req.Header.Set("Origin", "https://www.iwencai.com")
	req.Header.Set("Referer", "https://www.iwencai.com/unifiedwap/result?w="+url.QueryEscape(query))

	hexinV := c.generateHexinV()
	req.Header.Set("Hexin-V", hexinV)

	for i, cookie := range c.cookies {
		if cookie.Name == "v" {
			c.cookies[i].Value = hexinV
		}
		req.AddCookie(cookie)
	}

	resp, err := c.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("请求失败: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)

	return c.parseResponse(body, top)
}

func (c *WencaiClient) parseResponse(body []byte, top int) ([]StockRank, error) {
	var result struct {
		Errno int `json:"errno"`
		Data  struct {
			Answer []struct {
				Txt []struct {
					Content struct {
						Components []struct {
							Data struct {
								Datas []map[string]interface{} `json:"datas"`
							} `json:"data"`
						} `json:"components"`
					} `json:"content"`
				} `json:"txt"`
			} `json:"answer"`
		} `json:"data"`
	}

	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("解析失败: %v", err)
	}

	if result.Errno != 0 {
		return nil, fmt.Errorf("问财返回错误码: %d", result.Errno)
	}

	ranks := make([]StockRank, 0)

	if len(result.Data.Answer) > 0 &&
		len(result.Data.Answer[0].Txt) > 0 &&
		len(result.Data.Answer[0].Txt[0].Content.Components) > 0 {

		datas := result.Data.Answer[0].Txt[0].Content.Components[0].Data.Datas

		for i, data := range datas {
			if i >= top {
				break
			}

			code := getStrVal(data, "股票代码", "code", "stockCode")
			name := getStrVal(data, "股票简称", "name", "stockName")

			if code != "" && name != "" {
				ranks = append(ranks, StockRank{
					Code:      code,
					Name:      name,
					Rank:      i + 1,
					HeatScore: top - i,
					Source:    "wencai",
				})
			}
		}
	}

	if len(ranks) == 0 {
		return nil, fmt.Errorf("未解析到数据，可能需要更新反爬策略")
	}

	return ranks, nil
}

func (c *WencaiClient) generateHexinV() string {
	timestamp := fmt.Sprintf("%.3f", float64(time.Now().UnixNano())/1e9)

	cmd := exec.Command("node", c.jsPath, timestamp)
	output, err := cmd.Output()
	if err != nil {
		return "default_hexin_v_value"
	}

	return strings.TrimSpace(string(output))
}

// XueqiuFetcher 雪球热榜采集器
type XueqiuFetcher struct {
	client *http.Client
}

// NewXueqiuFetcher 创建雪球采集器
func NewXueqiuFetcher() *XueqiuFetcher {
	return &XueqiuFetcher{
		client: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// Fetch 获取雪球热榜A股前50
func (f *XueqiuFetcher) Fetch() ([]StockRank, error) {
	html, err := f.fetchPage()
	if err != nil {
		return nil, err
	}

	ranks := f.parseFromHTML(html)
	if len(ranks) == 0 {
		return nil, fmt.Errorf("未能从页面解析到股票数据")
	}

	return ranks, nil
}

func (f *XueqiuFetcher) fetchPage() (string, error) {
	url := "https://xueqiu.com/hot/stock"

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", fmt.Errorf("创建请求失败: %v", err)
	}

	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.Header.Set("Accept-Encoding", "gzip, deflate, br")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

	resp, err := f.client.Do(req)
	if err != nil {
		return "", fmt.Errorf("请求失败: %v", err)
	}
	defer resp.Body.Close()

	var reader io.Reader = resp.Body
	if resp.Header.Get("Content-Encoding") == "gzip" {
		gzReader, err := gzip.NewReader(resp.Body)
		if err != nil {
			return "", fmt.Errorf("解压gzip失败: %v", err)
		}
		defer gzReader.Close()
		reader = gzReader
	}

	body, err := io.ReadAll(reader)
	if err != nil {
		return "", fmt.Errorf("读取响应失败: %v", err)
	}

	return string(body), nil
}

func (f *XueqiuFetcher) parseFromHTML(html string) []StockRank {
	ranks := make([]StockRank, 0)

	pattern := regexp.MustCompile(`"name":"([^"]+)","value":[^}]*"symbol":"(SH|SZ)(\d+)"`)
	matches := pattern.FindAllStringSubmatch(html, -1)

	seen := make(map[string]bool)

	for _, match := range matches {
		if len(match) < 4 {
			continue
		}

		name := match[1]
		market := match[2]
		code := match[3]

		fullCode := market + code
		if seen[fullCode] {
			continue
		}
		seen[fullCode] = true

		if code != "" && name != "" && len(ranks) < 50 {
			ranks = append(ranks, StockRank{
				Code:      code,
				Name:      name,
				Rank:      len(ranks) + 1,
				HeatScore: 100 - len(ranks),
				Source:    "xueqiu",
			})
		}
	}

	return ranks
}

// EastmoneyFetcher 东方财富人气排名采集器
type EastmoneyFetcher struct {
	client *http.Client
}

// NewEastmoneyFetcher 创建东财采集器
func NewEastmoneyFetcher() *EastmoneyFetcher {
	return &EastmoneyFetcher{
		client: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// Fetch 获取东方财富人气排名前50
func (f *EastmoneyFetcher) Fetch() ([]StockRank, error) {
	return f.getRankData()
}

func (f *EastmoneyFetcher) getRankData() ([]StockRank, error) {
	url := "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"

	postData := map[string]interface{}{
		"appId":         "stockrank",
		"globalId":      "786e4c21-70dc-435a-93bb-38",
		"marketType":    "",
		"rankType":      "1",
		"pageNo":        1,
		"pageSize":      100,
		"fromDate":      "",
		"toDate":        "",
		"stockIndustry": "",
		"stockCode":     "",
		"stockName":     "",
		"clientSource":  "web",
		"clientVersion": "1.0.0",
	}

	jsonData, _ := json.Marshal(postData)

	req, err := http.NewRequest("POST", url, bytes.NewReader(jsonData))
	if err != nil {
		return nil, fmt.Errorf("创建请求失败: %v", err)
	}

	req.Header.Set("Accept", "*/*")
	req.Header.Set("Accept-Encoding", "gzip, deflate, br")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9")
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Origin", "https://vipmoney.eastmoney.com")
	req.Header.Set("Referer", "https://vipmoney.eastmoney.com/")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

	resp, err := f.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("请求失败: %v", err)
	}
	defer resp.Body.Close()

	var reader io.Reader = resp.Body
	if resp.Header.Get("Content-Encoding") == "gzip" {
		gzReader, err := gzip.NewReader(resp.Body)
		if err != nil {
			return nil, fmt.Errorf("解压gzip失败: %v", err)
		}
		defer gzReader.Close()
		reader = gzReader
	}

	body, err := io.ReadAll(reader)
	if err != nil {
		return nil, fmt.Errorf("读取响应失败: %v", err)
	}

	return f.parseResponse(body)
}

func (f *EastmoneyFetcher) parseResponse(body []byte) ([]StockRank, error) {
	var result struct {
		Status int `json:"status"`
		Data   []struct {
			Sc string `json:"sc"` // 股票代码 (如 SZ002261)
			Rk int    `json:"rk"` // 排名
		} `json:"data"`
	}

	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("解析失败: %v", err)
	}

	if result.Status != 0 {
		return nil, fmt.Errorf("API返回错误: status=%d", result.Status)
	}

	ranks := make([]StockRank, 0)

	for _, item := range result.Data {
		code := item.Sc
		if len(code) < 8 {
			continue
		}

		code = code[2:] // 去掉前缀

		if len(ranks) >= 50 {
			break
		}

		ranks = append(ranks, StockRank{
			Code:      code,
			Name:      "",
			Rank:      item.Rk,
			HeatScore: 100 - len(ranks),
			Source:    "eastmoney",
		})
	}

	return ranks, nil
}

func getStrVal(m map[string]interface{}, keys ...string) string {
	for _, key := range keys {
		if v, ok := m[key]; ok {
			if s, ok := v.(string); ok {
				return s
			}
		}
	}
	return ""
}

func randString(n int) string {
	const letters = "abcdefghijklmnopqrstuvwxyz0123456789"
	b := make([]byte, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

// normalizeCode 标准化股票代码
func normalizeCode(code string) string {
	if len(code) == 6 {
		return validateAStockCode(code)
	}
	if len(code) == 8 && (code[:2] == "SH" || code[:2] == "SZ") {
		return validateAStockCode(code[2:])
	}
	if len(code) == 9 && (code[6:] == ".SH" || code[6:] == ".SZ") {
		return validateAStockCode(code[:6])
	}
	return ""
}

func validateAStockCode(code string) string {
	if len(code) != 6 {
		return ""
	}
	for _, c := range code {
		if c < '0' || c > '9' {
			return ""
		}
	}
	first := code[0]
	if first != '6' && first != '0' && first != '3' && first != '8' && first != '4' {
		return ""
	}
	return code
}

// calculateComposite 计算复合热度
func calculateComposite(wencai, xueqiu, eastmoney []StockRank) []CompositeRank {
	stockMap := make(map[string]*CompositeRank)

	// 处理问财数据
	for _, r := range wencai {
		code := normalizeCode(r.Code)
		if code == "" {
			continue
		}
		if _, ok := stockMap[code]; !ok {
			stockMap[code] = &CompositeRank{
				Code: code,
				Name: r.Name,
			}
		}
		stockMap[code].WencaiRank = r.Rank
		stockMap[code].AppearCount++
	}

	// 处理雪球数据
	for _, r := range xueqiu {
		code := normalizeCode(r.Code)
		if code == "" {
			continue
		}
		if _, ok := stockMap[code]; !ok {
			stockMap[code] = &CompositeRank{
				Code: code,
				Name: r.Name,
			}
		}
		stockMap[code].XueqiuRank = r.Rank
		stockMap[code].AppearCount++
	}

	// 处理东财数据
	for _, r := range eastmoney {
		code := normalizeCode(r.Code)
		if code == "" {
			continue
		}
		if _, ok := stockMap[code]; !ok {
			stockMap[code] = &CompositeRank{
				Code: code,
				Name: r.Name,
			}
		}
		if stockMap[code].Name == "" && r.Name != "" {
			stockMap[code].Name = r.Name
		}
		stockMap[code].EastmoneyRank = r.Rank
		stockMap[code].AppearCount++
	}

	// 计算复合得分
	for _, stock := range stockMap {
		score := 0.0

		if stock.WencaiRank > 0 {
			score += float64(100 - stock.WencaiRank)
		}
		if stock.XueqiuRank > 0 {
			score += float64(100 - stock.XueqiuRank)
		}
		if stock.EastmoneyRank > 0 {
			score += float64(100 - stock.EastmoneyRank)
		}

		if stock.AppearCount == 2 {
			score += 20
		} else if stock.AppearCount == 3 {
			score += 50
		}

		stock.CompositeScore = score / 3.5
	}

	// 转换为切片并排序
	ranks := make([]CompositeRank, 0, len(stockMap))
	for _, stock := range stockMap {
		ranks = append(ranks, *stock)
	}

	sort.Slice(ranks, func(i, j int) bool {
		return ranks[i].CompositeScore > ranks[j].CompositeScore
	})

	return ranks
}

func printTable(ranks []CompositeRank, top int) {
	fmt.Println()
	fmt.Println("┌──────┬──────────┬────────────┬──────┬──────┬──────┬──────────┬──────┐")
	fmt.Println("│ 排名 │   代码   │    名称    │ 问财 │ 雪球 │ 东财 │  热度分  │ 出现 │")
	fmt.Println("├──────┼──────────┼────────────┼──────┼──────┼──────┼──────────┼──────┤")

	for i, r := range ranks {
		if i >= top {
			break
		}

		wc := "-"
		if r.WencaiRank > 0 {
			wc = fmt.Sprintf("%d", r.WencaiRank)
		}
		xq := "-"
		if r.XueqiuRank > 0 {
			xq = fmt.Sprintf("%d", r.XueqiuRank)
		}
		em := "-"
		if r.EastmoneyRank > 0 {
			em = fmt.Sprintf("%d", r.EastmoneyRank)
		}

		fmt.Printf("│ %4d │ %8s │ %-10s │ %4s │ %4s │ %4s │ %8.1f │ %4d │\n",
			i+1, r.Code, r.Name, wc, xq, em, r.CompositeScore, r.AppearCount)
	}

	fmt.Println("└──────┴──────────┴────────────┴──────┴──────┴──────┴──────────┴──────┘")
	fmt.Println()
}

func printJSON(ranks []CompositeRank, top int) {
	result := make([]CompositeRank, 0)
	for i, r := range ranks {
		if i >= top {
			break
		}
		result = append(result, r)
	}
	jsonData, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(jsonData))
}

func main() {
	top := flag.Int("top", 50, "获取前N名")
	format := flag.String("format", "table", "输出格式: table, json")
	flag.Parse()

	fmt.Println("=== 股票热度排名采集器 ===")
	fmt.Printf("采集时间: %s\n\n", time.Now().Format("2006-01-02 15:04:05"))

	// 采集问财数据
	fmt.Println("【问财】正在采集...")
	wencaiClient := NewWencaiClient()
	wencaiRanks, err := wencaiClient.Fetch(50)
	if err != nil {
		fmt.Printf("  采集失败: %v\n", err)
	} else {
		fmt.Printf("  成功获取 %d 只股票\n", len(wencaiRanks))
	}

	// 采集雪球数据
	fmt.Println("\n【雪球】正在采集...")
	xueqiuFetcher := NewXueqiuFetcher()
	xueqiuRanks, err := xueqiuFetcher.Fetch()
	if err != nil {
		fmt.Printf("  采集失败: %v\n", err)
	} else {
		fmt.Printf("  成功获取 %d 只A股\n", len(xueqiuRanks))
	}

	// 采集东财数据
	fmt.Println("\n【东财】正在采集...")
	eastmoneyFetcher := NewEastmoneyFetcher()
	eastmoneyRanks, err := eastmoneyFetcher.Fetch()
	if err != nil {
		fmt.Printf("  采集失败: %v\n", err)
	} else {
		fmt.Printf("  成功获取 %d 只股票\n", len(eastmoneyRanks))
	}

	// 计算复合热度
	fmt.Println("\n=== 复合热度排名 ===")
	fmt.Printf("问财: %d | 雪球: %d | 东财: %d\n", len(wencaiRanks), len(xueqiuRanks), len(eastmoneyRanks))

	result := calculateComposite(wencaiRanks, xueqiuRanks, eastmoneyRanks)

	switch *format {
	case "json":
		printJSON(result, *top)
	default:
		printTable(result, *top)
	}
}

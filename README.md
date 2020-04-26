# Chinese-keyword-extraction
Extract representative keywords from the news articles in 2016.

2020大數據與商業分析 小組作業1 / 洪譽家、陳德軒

使用2016年的90000多筆新聞文章，實作六項主題(銀行、信用卡、匯率、台積電、台灣、日本)，列出每一主題的前一百個2-6gram的中文關鍵字。

#### 關鍵字評判標準：TF Chi Square
另曾嘗試tf-idf, MI, DF Chi Square，不採用原因如下:
- TF-IDF值：受出現篇數(DF)影響大，出現篇數少排名前，不具代表性
- MI值：各字詞差距不大，無鑑別力
- DF卡方值：各主題文章數少，數值易有偏頗
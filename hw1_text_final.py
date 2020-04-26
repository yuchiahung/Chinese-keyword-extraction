#!/usr/bin/env python
# coding: utf-8

#%%
import pandas as pd
import numpy as np

all = pd.read_excel('data/hw1_text.xlsx', sheet_name='all')

all_text = all.iloc[:,3:5]
all_text.columns = ['title','content']

# read stopword
stopword = []
with open('data/stopword.txt', 'r', encoding = 'utf8') as file:
    for data in file.readlines():
        data = data.strip()
        stopword.append(data)

#%%
# topics
#1. 銀行：
bank_search = ['銀行', '金管會', '匯豐', '中國信託', '兆豐', '玉山', '合作金庫', '國泰世華', '第一銀行', '華南', '富邦', '土地', '花旗', '台銀','債券', '利息', '中信', '提款', '帳戶', 'ATM', '理專', '降息', '升息', '利率']
#2. 信用卡：
card_search = ['信用卡', '手續費', '紅利', '萬事達卡','Visa', 'Mastercard', '行動支付', '金融卡', '申辦', '刷卡', '謹慎理財','信用無價', '刷卡金', '卡友', '分期','信用卡利息','首刷', '首次刷卡', '聯名卡', '盜刷', '持卡人','卡號','正卡', '附卡', '雙幣卡', '商務卡', '世界卡', '黑卡', '新卡', '卡費', 'Apple Pay', '刷卡額', '頂級卡', '航空卡', '一卡通', '現金回饋', '電子支付', '支付寶', 'LinePay', '銀行卡','辦卡', '開卡', '街口', '街口支付', '額度']
#3. 匯率：
currency_search = ['日圓', '人民幣', '新台幣', '法郎', '歐元', '牌告', '換匯', '韓圜', '英鎊', '走勢', '央行', '交易日', '外匯', '中央銀行', '匯率', '台幣', '日元', '克朗']
#4. 台積電：
tsms_search = ['台積電','晶圓龍頭','半導體','張忠謀','魏哲家','劉德音','晶圓代工','積體電路製造','2330', 'TSMC','奈米製程','晶圓廠']
#5. 台灣：
taiwan_search = ['台灣', '臺灣', '台商', '臺商', '蔡英文', '兩岸', '台北', '臺北', '高雄', '台中', '臺中', '民進黨', '國民黨', '柯文哲', '桃園', '新竹', '新北', '基隆', '馬英九', '苗栗', '南投', '彰化', '雲林', '屏東', '花蓮', '台東', '宜蘭', '嘉義', 'taiwan','Taiwan','TAIWAN', '全台', '全臺','總統大選','立委', '行政院','立法院']
#6. 日本: 
japan_search = ['日本', '東京', '大阪', '京都', '北海道', '安倍晉三', '日媒', '日企', '橫濱', '名古屋', '札幌', '沖繩', '神戶', '日清', '三菱', '本田', '三井', '富士', '櫻花', '富士山', '日幣', '日圓 ', '株式', '會社', '株式會社', '松下', '夏普', '小林', '鈴木', 'japan', 'Japan', 'JAPAN', 'tokyo','築地','知事','日皇'] 
#%%

def get_ngrams(n, topic = None):
    tf = {}
    df = {}
    tfdf = {}
    if topic is None:
        subset = all_text
    else:
        subset = all_text[all_text.content.str.contains('|'.join(topic))]     
    docs = len(subset.index)
    subset.replace(to_replace = r"[a-zA-Z0-9\W\d]", value = '', regex = True, inplace = True)
    for row in range(len(subset)):
        text = subset.iloc[row].values.sum(axis = 0)
        #for n in range(2, 7): #斷 2-6 grams
        tokens = [text[i:i+n] for i in range(0, len(text)-1)]
        #if tokens not in stopword:
        for token in set(tokens):
            if token not in df.keys():
                df[token] = 1
            else:    
                df[token] += 1
        for token in tokens:
            if token not in tf.keys():
                tf[token] = 1
            else:
                tf[token] += 1
    for key, value in tf.items():
        tfdf[key] = [value, df[key]]
    df = pd.DataFrame.from_dict(tfdf, orient = 'index', columns = ['tf','df'])
    return(df, docs)

#%%
topics = ['bank', 'card', 'currency', 'tsms', 'taiwan', 'japan']

for topic in topics:
    for n in range(2,7):
        locals()[topic+'_'+str(n)+'gram'], locals()[topic+'__docs'] = get_ngrams(n, locals()[topic+'_search'])

for ng in range(2, 7):
    locals()['all_'+str(ng)+'gram'], all_docs = get_ngrams(n=ng)

#%%
def remove_sw_lowtf(df, N):
    """移除 TF< 篇數(N) 1% 的詞 & stopword """
    # 移除 TF< 篇數(N) 1% 的詞
    #df = pd.DataFrame.from_dict(data, orient = 'index', columns = ['tf','df'])
    df = df.sort_values(by = 'tf', ascending=False)
    low_tf = 0.01 * N
    for i in range(len(df)):
        if df.iloc[i, 0] <= low_tf:
            df = df[:i]
            break
    # 移除 stopword
    lowtf_drop = set()
    for i in range(len(df)):
        if df.index[i] in stopword:
            lowtf_drop.add(df.index[i])
    df = df.drop(lowtf_drop)
    return df

def remove_sw_lowtf_0001(df, N):
    """移除 TF< 篇數(N) 1% 的詞 & stopword """
    # 移除 TF< 篇數(N) 1% 的詞
    #df = pd.DataFrame.from_dict(data, orient = 'index', columns = ['tf','df'])
    df = df.sort_values(by = 'tf', ascending=False)
    low_tf = 0.001 * N
    for i in range(len(df)):
        if df.iloc[i, 0] <= low_tf:
            df = df[:i]
            break
    # 移除 stopword
    lowtf_drop = set()
    for i in range(len(df)):
        if df.index[i] in stopword:
            lowtf_drop.add(df.index[i])
    df = df.drop(lowtf_drop)
    return df

for topic in topics:
    for n in range(2,7):
        locals()[topic+'_'+str(n)+'gram_sw'] = remove_sw_lowtf(locals()[topic+'_'+str(n)+'gram'], locals()[topic+'_docs'])

for n in range(2,7):
    locals()['all_'+str(n)+'gram_sw'] = remove_sw_lowtf_0001(locals()['all_'+str(n)+'gram'], all_docs)

#%%
def all_gram(df_2, df_3, df_4, df_5, df_6):
    """combine 2-6 gram df"""
    df = pd.concat([df_2, df_3, df_4, df_5, df_6])
    return df

topics.append('all')
for topic in topics:
    locals()[topic+'_allgram'] = all_gram(locals()[topic+'_2gram_sw'], locals()[topic+'_3gram_sw'], locals()[topic+'_4gram_sw'], locals()[topic+'_5gram_sw'], locals()[topic+'_6gram_sw'])

#%%
def remove_same(df):
    """移除相同DF的 被較長詞包含的詞"""
    df['len'] = df.index.str.len()
    df.sort_values('len', ascending=True, inplace = True)
    df.drop('len', axis=1, inplace=True)
    same_drop = set()
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            # row i 的詞比row j 的詞短 (e.g. row i: 2-gram, row j: 3-gram)
            # 且row i 被 row j 的詞包含
            if (len(df.index[i]) < len(df.index[j])) & (df.index[i] in df.index[j]): 
                # 兩個詞的 DF 相差不到1% same DF number
                if abs(df.iloc[i, 1] - df.iloc[j, 1]) <= max(df.iloc[i, 1], df.iloc[j, 1]) * 0.01 :
                    #add the word in row i(shorter word) to a same_drop set
                    same_drop.add(df.index[i])
                    break
    return df.drop(same_drop)

for topic in topics:
    locals()[topic+'_allgram_same'] = remove_same(locals()[topic+'_allgram'])

#%%
def get_tfidf(df, docs):
    """add the tf-idf column"""
    df['tfidf'] = (1+np.log(df.tf))*np.log(docs/df.df)
    return(df)

for topic in topics:
    locals()[topic+'_allgram_tfidf'] = get_tfidf(locals()[topic+'_allgram_same'], locals()[topic+'_docs'])

#%%
def get_final_df(df, docs, all_df, all_docs):
    """combine the topic df and the total df and then calculate the chi square"""
    all_df.columns = ['all_tf','all_df','all_tf-idf']
    df = pd.merge(df, all_df, left_index = True, right_index = True, how = 'left')
    df['midf'] = np.log(df.df/(df.all_df*docs))
    df['tf_ev'] = df.all_tf/all_docs*docs
    df['df_ev'] = df.all_df/all_docs*docs
    df['tf_chi'] = ((df.tf-df.tf_ev)**2/df.tf_ev)*np.sign(df.tf-df.tf_ev)
    df['df_chi'] = ((df.df-df.df_ev)**2/df.df_ev)*np.sign(df.df-df.df_ev)
    df = df.sort_values('tf_chi',ascending = False)
    return(df)

topics.remove('all')
for topic in topics:
    locals()[topic+'_final'] = get_final_df(locals()[topic+'_allgram_tfidf'], locals()[topic+'_docs'], all_allgram_tfidf, all_docs)

#%%
# write the dataframe to csv file
bank_final.to_csv('result/bank.csv', encoding='utf_8_sig')
card_final.to_csv('result/card.csv', encoding='utf_8_sig')
currency_final.to_csv('result/currency.csv', encoding='utf_8_sig')
tsms_final.to_csv('result/tsms.csv', encoding='utf_8_sig')
taiwan_final.to_csv('result/taiwan.csv', encoding='utf_8_sig')
japan_final.to_csv('result/japan.csv', encoding='utf_8_sig')

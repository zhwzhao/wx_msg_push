

# 导入 efinance 如果没有安装则需要通过执行命令: pip install efinance 来安装
import efinance as ef
import time
from datetime import datetime, timedelta
import requests
import json
# -*- coding: utf-8 -*-
import http.client, urllib

def tiangou():
    conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
    params = urllib.parse.urlencode({'key':'50ad8a0febfcc6cc757967315754f8ae'})
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    conn.request('POST','/tiangou/index',params,headers)
    res = conn.getresponse()
    data = res.read()
    res = json.loads(data.decode('utf-8'))
    
    if(res['code']==200 and res['msg']=='success'):
        return res['newslist'][0]['content']
    else:
        return False

    

day_list = [1]

def get_fund(stock_codes):
    # 现在的时间
    now = str(datetime.today()).split('.')[0]
    print('当前时间：', str(now))

    info = ''
    for stock_code in stock_codes:
        print('分析{}数据'.format(stock_codes[stock_code]))
        # 获取最新一个交易日的分钟级别股票行情数据
        df = ef.fund.get_quote_history(stock_code)
        # 将数据存储到 csv 文件中
        df.to_csv(f'{stock_codes[stock_code]}.csv', encoding='utf-8-sig', index=None)
        # print(df['日期'])
        # print(f'已在 {now}, 将股票: {stock_code} 的行情数据存储到文件: {stock_code}.csv 中！')
        ratio = df['涨跌幅'][0]
        info += stock_codes[stock_code] + str(ratio) + '\n'
        # data_analysis(df)
    print(info)
    return info
    # print('全部股票已收盘')

def data_time(df, cur_date, day):
    print('------{}------'.format(day))
    last_date = cur_date - timedelta(days=day)
    a = df[df['日期'].isin([str(last_date)])]
    try:
        col = a.index.values[0]
    except:
        print('数据异常！！！')
        return
    max_value = df[:col]['累计净值'].max()
    min_value = df[:col]['累计净值'].min()
    cur_value = df['累计净值'][0]
    inc = (cur_value - max_value) / max_value
    dec = (cur_value - min_value) / min_value
    print('上升{:.3f}, 下降{:.2f}'.format(float(inc), float(dec)))
    

def data_analysis(df):
    now = str(datetime.today()).split('.')[0]
    first_row_date = df['日期'][0]
    print('基金最新时间{}'.format(first_row_date))
    cur_date = datetime.strptime(first_row_date,"%Y-%m-%d").date()
    for day in day_list:
        data_time(df, cur_date, day)
    


# server酱推送
if __name__ == "__main__":
    api = "https://sc.ftqq.com/SCT170717TfyfZPpP82JlQHUfNA9ZWFp9Q.send"
    title = u"每次涨幅"

    # res = tiangou()
    # print(res)
    # if res is not False:
    #     data = {
    #     "text":title,
    #     "desp":res
    #     }
    #     req = requests.post(api,data = data)
    # 股票代码或者名称列表
    stock_codes = {'002168': '嘉实智能汽车', '014978': '华安纳斯达克', '163417': "兴全合宜混合", 
                    '005827': '易方达蓝筹', '750002': '安信目标收益债券'}
    res = get_fund(stock_codes)
    data = {
        "text":title,
        "desp":res
        }
    req = requests.post(api,data = data)

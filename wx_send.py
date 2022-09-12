

# 导入 efinance 如果没有安装则需要通过执行命令: pip install efinance 来安装
import efinance as ef
import time
from datetime import datetime
import requests

def demo():
    # 股票代码或者名称列表
    stock_codes = ['750002', '腾讯', 'AAPL']
    # 数据间隔时间为 1 分钟
    freq = 1
    status = {stock_code: 0 for stock_code in stock_codes}
    print(status)

    while len(stock_codes) != 0:
        for stock_code in stock_codes.copy():
            print(stock_code)
            # 现在的时间
            now = str(datetime.today()).split('.')[0]
            # 获取最新一个交易日的分钟级别股票行情数据
            df = ef.stock.get_quote_history(stock_code, klt=freq)
            # 将数据存储到 csv 文件中
            df.to_csv(f'{stock_code}.csv', encoding='utf-8-sig', index=None)
            print(f'已在 {now}, 将股票: {stock_code} 的行情数据存储到文件: {stock_code}.csv 中！')
            if len(df) == status[stock_code]:
                # 移除已经收盘的股票代码
                stock_codes.remove(stock_code)
                print(f'股票 {stock_code} 已收盘！')
            status[stock_code] = len(df)
        if len(stock_codes) != 0:
            print('暂停 60 秒')
            time.sleep(60)
        print('-'*10)


    # print('全部股票已收盘')


# server酱推送
if __name__ == "__main__":
    api = "https://sc.ftqq.com/SCT170717TfyfZPpP82JlQHUfNA9ZWFp9Q.send"
    title = u"紧急通知"
    content = """
    # 服务器又炸啦！
    ## 请尽快修复服务器
    """
    data = {
       "text":title,
       "desp":content
    }
    req = requests.post(api,data = data)
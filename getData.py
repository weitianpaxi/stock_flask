"""
通过爬虫获取自1991年至今天2023年5月26日的‘上证指数’，‘A股指数’，‘深证综指’,'沪深300‘的历史数据
"""
import pandas as pd
import requests


def getUrl(stock_name: list, stock_code: list, start_date: list, end_date: str) -> dict:
    """
    获取请求的url
    :return: 封装好的请求url的字典
    """
    # 请求数据的源地址
    base_url = 'https://q.stock.sohu.com/hisHq?'
    temp_url_list = []      # 暂存组成的单个请求地址
    url_dict = {}           # 初始化返回的字典
    for date in start_date:
        if date == '19910102':
            for i in range(2):
                temp_url = base_url + f'code=zs_{stock_code[i]}&start={date}&end={end_date}'
                temp_url_list.append(temp_url)
        elif date == '19910405':
            temp_url = base_url + f'code=zs_{stock_code[2]}&start={date}&end={end_date}'
            temp_url_list.append(temp_url)
        else:
            temp_url = base_url + f'code=zs_{stock_code[3]}&start={date}&end={end_date}'
            temp_url_list.append(temp_url)
    # 组合URL字典
    for i, name in enumerate(stock_name):
        url_dict[name] = temp_url_list[i]
    return url_dict


def getData(url_dict: dict, stock_name: list[str]):
    """
    获取股票历史数据，并存入Excel，爬虫主要实现模块
    :return: 无返回值
    """
    # 定义Excel的表头
    columns: list[str] = ['日期', '开盘', '收盘', '涨跌额', '涨跌幅', '最低', '最高', '成交量(手)', '成交金额(万)', '换手率']
    for name in stock_name:
        response = requests.get(url=url_dict[name])
        # 将请求到的数据转换为json格式
        response_json = response.json()
        # 将获取的数据转换为pandas所支持的dataframe数据对象
        data_frame = pd.DataFrame(data=response_json[0]['hq'], columns=columns)
        data_frame.to_excel(excel_writer=f'data/{name}历史数据.xlsx', sheet_name=name, index=False)
        # 查看获得数据个数
        print(len(response_json[0]['hq']))


if __name__ == '__main__':
    pass
    # stockCode = ['000001', '000002', '399106', '399300']
    # stockName = ['上证指数', 'A股指数', '深证综指', '沪深300']
    # startDate = ['19910102', '19910405', '20050409']
    # 获取当天的日期，并格式化
    # endDate = datetime.date.today().strftime('%Y%m%d')
    # print(endDate)
    # url: dict = getUrl(stock_name=stockName, stock_code=stockCode, start_date=startDate, end_date=endDate)
    # print(url)
    # getdata(url_dict=url, stock_name=stockName)

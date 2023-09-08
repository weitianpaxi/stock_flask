"""
处理爬取到的数据，并将其可视化展示
目标是绘制k线图，k线图中所需股票的当日开盘价，收盘价，当日最高值和最低值。
若当天跌了，就显示绿色，反之是红色。可以根据数据列中的‘涨跌额’的正负判断
再绘制成交额的随时间变换的柱状图，及添加时间线的动态柱状图
"""

from typing import List, Union

import pandas as pd
from pandas import DataFrame


def importData(stock_name: str) -> DataFrame:
    """
    导入数据，转换为pandas可以处理的DataFrame对象
    :param stock_name: str
    :return: 返回DataFrame对象
    """
    return pd.read_excel(io=f'data/{stock_name}历史数据.xlsx', header=0)


def spiltData(data: DataFrame) -> dict:
    """
    方便后面数据展示，进行数据清洗
    :param data: DataFrame
    :return: 返回封装好的字典对象
    """
    volumes = []            # 记录天数，当天的最高值以及当天涨跌的标识符
    category_data = data['日期'].values.tolist()     # 取出日期的值存入列表，此时要进行格式转换
    category_data.reverse()                         # 绘图从左到右为时间从早到现在，故倒置列表
    # 记录每一天的股票数据值，包括开盘价，收盘价，最高值，最低值
    values = data[['日期', '开盘', '收盘', '最低', '最高', '成交量(手)']].values.tolist()
    values.reverse()                                # 绘图从左到右为时间从早到现在，故倒置列表
    tolist = data[['最高', '涨跌额']].values.tolist()
    tolist.reverse()                                # 绘图从左到右为时间从早到现在，故倒置列表
    for i, tick in enumerate(tolist):
        # 向volumes列表添加编号以及所对应的最大值，以及记录涨跌的标记符号
        volumes.append([i, tick[0], 1 if tick[1] > 0 else -1])
    # 下面获取成交量和成交金额
    deal_data = data['成交金额(万)'].values.tolist()
    deal_data.reverse()                             # 绘图从左到右为时间从早到现在，故倒置列表
    return {'categoryData': category_data, 'values': values, 'volumes': volumes, 'dealData': deal_data}


def calculate_ma(day_count: int, data: dict) -> list:
    """
    计算绘制k线图所需的Moving Average(ma),即移动平均线，“均线”
    计算公式是：某一段时间的收盘价之和除以该周期
    :param day_count: 计算周期
    :param data: 数据清洗封装好的字典
    :return: 返回结果列表，列表内存放“均值，（不满计算周期存入字符‘-’）”
    """
    result: List[Union[float, str]] = []        # 初始化定义结果列表
    for i in range(len(data['values'])):
        if i < day_count:
            result.append('-')      # 时间段不满足日期周期，则不计算ma，存入‘-’
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(data['values'][i - j][1])                        # 周期内数据加和
        result.append(abs(float('%.3f' % (sum_total / day_count))))
    return result


if __name__ == '__main__':
    pass
    # stockName = ['上证指数', 'A股指数', '深证综指', '沪深300']
    # test_data = importData(stock_name=stockName[0])
    # spilt_data = spiltData(test_data)
    # print(spilt_data['dealData'])
    # # 测试计算ma5
    # calculate_ma(day_count=5, data=spilt_data)

import datetime

from flask import Flask, render_template

# 数据处理的自定义包
from DataProcessing import importData, spiltData
from Visualization import draw_kline_charts, draw_lines_charts
from getData import getUrl, getData

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# 主页方法
@app.route('/index')
def home():
    return render_template('index.html')


# k线图页面方法
@app.route('/kline')
def kline():
    return render_template('kline.html')


@app.route('/kline1')
def kline1():
    return render_template('kline1.html')


@app.route('/kline2')
def kline2():
    return render_template('kline2.html')


@app.route('/kline3')
def kline3():
    return render_template('kline3.html')


# 页面绘制k线图
@app.route('/get_kline/', defaults={'stockName': '上证指数'})   # 默认绘图参数
@app.route('/get_kline/<string:stockName>', methods=['GET'])
def get_kline(stockName):
    test_data = importData(stock_name=stockName)
    spilt_data = spiltData(test_data)
    charts = draw_kline_charts(stock_name=stockName, chart_data=spilt_data)
    return charts.dump_options_with_quotes()


# 成交额图页面方法
@app.route('/deal_data')
def DealData():
    return render_template('deal_data.html')


# 获取成交额数据
@app.route('/get_deal_data/<string:stockName>', methods=['GET'])
def getDealData(stockName):
    test_data = importData(stock_name=stockName)
    spilt_data = spiltData(test_data)
    charts = draw_lines_charts(stock_name=stockName, chart_data=spilt_data)
    return charts.dump_options_with_quotes()


# 团队成员介绍页面方法
@app.route('/team')
def team():
    return render_template('team.html')


# 主函数入口
if __name__ == '__main__':
    stockName = ['上证指数', 'A股指数', '深证综指', '沪深300']
    stockCode = ['000001', '000002', '399106', '399300']
    startDate = ['19910102', '19910405', '20050409']
    endDate = datetime.date.today().strftime('%Y%m%d')  # 获取当天的日期，并格式化
    url: dict = getUrl(stock_name=stockName, stock_code=stockCode, start_date=startDate, end_date=endDate)
    getData(url_dict=url, stock_name=stockName)
    app.run(debug=True)

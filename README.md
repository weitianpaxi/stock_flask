# stock_flask

## 项目简介

利用Flask搭建的股票数据可视化展示网站。数据来源于爬虫爬取搜狐证劵网站的数据。数据可视化使用了pyrcharts实现，使用了flask框架构建网站。

爬虫爬取搜狐证劵上可查询到的自指数公开数据到项目启动时的数据，比如上证指数的数据来源网址为： https://q.stock.sohu.com/zs/000001/lshq.shtml 。爬取后存储于data目录下。

项目首页如图所示[![pCEFOvF.png](https://s1.ax1x.com/2023/06/09/pCEFOvF.png)](https://imgse.com/i/pCEFOvF)

走势K线图如图所示[![pCEFvDJ.png](https://s1.ax1x.com/2023/06/09/pCEFvDJ.png)](https://imgse.com/i/pCEFvDJ)

成交额趋势图，是动态折线图，点按播放可以动态展示。[![pCEkkvD.png](https://s1.ax1x.com/2023/06/09/pCEkkvD.png)](https://imgse.com/i/pCEkkvD)

## 开发环境

- Python == 3.10.4
- beautifulsoup4 == 4.12.2
- Flask == 2.3.2
- pyecharts == 2.0.3
- selenium == 4.9.1
- Jinja2 == 3.1.2
- tqdm  == 4.65.0

建议使用`miniconda`创建虚拟环境使用，具体详细的必要第三方软件包见`必要第三方软件包.txt`文件。


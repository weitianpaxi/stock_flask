"""
数据可视化模块，利用pyecharts绘图
"""
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid, Timeline
from pyecharts.globals import RenderType

from DataProcessing import calculate_ma


def draw_kline_charts(stock_name: str, chart_data: dict):
    """
    实现绘制复杂的k线图
    :param stock_name: 要绘制的股票的名称
    :param chart_data: 清洗好的数据字典
    :return: 一个组合好的图表对象
    """
    # 取得kline所待需的数据,1:-1，表示数组的截取，只需要从下标为1到倒数第二个下标的数据
    kline_data = [data[1:-1] for data in chart_data['values']]
    # 初始化k线图对象
    kline = (
        Kline()
        .add_xaxis(xaxis_data=chart_data['categoryData'])  # 添加x轴数据
        .add_yaxis(
            # 添加y轴数据
            series_name=stock_name,     # 图名称
            y_axis=kline_data,          # 添加图数据
            itemstyle_opts=opts.ItemStyleOpts(color='#ec0000', color0='#00da3c'),  # 设置颜色
        )
        .set_global_opts(
            # 标题设置
            title_opts=opts.TitleOpts(
                title=f'{stock_name}历史数据图',
                pos_left='center'
            ),
            # 图例设置
            legend_opts=opts.LegendOpts(
                is_show=False,
                pos_bottom=10,       # 距离div顶部距离
                pos_left='right'     # 靠右展示
            ),
            # 数据部分设置
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_='inside',  # 各种数据在内部展示
                    xaxis_index=[0, 1],
                    range_start=99,  # 数据窗口范围的起始百分比。范围是：0 ~ 100。表示 0% ~ 100%。
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_='slider',  # 数据可以滑动展示
                    pos_top='85%',   # dataZoom-slider 组件离容器上侧的距离
                    range_start=99,
                    range_end=100,
                ),
            ],
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True,
                    areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            # 提示框设置，即鼠标聚焦到一点后弹出的数据提示框
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                axis_pointer_type='cross',  # 鼠标划过显示数据数据提示框
                background_color='rgba(245, 245, 245, 0.8)',  # 数据展示框的背景设置,白色，透明度为80%
                border_width=1,
                border_color='#ccc',
                textstyle_opts=opts.TextStyleOpts(color='#000')  # 设置显示的文本颜色
            ),
            # 视觉映射配置
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                # 根据当天的涨跌显示不同的颜色
                pieces=[
                    {'value': 1, 'color': '#00da3c'},
                    {'value': -1, 'color': '#ec0000'},
                ],
            ),
            # 坐标轴指示器配置
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{'xAxisIndex': 'all'}],
                label=opts.LabelOpts(background_color="#777"),
            ),
            brush_opts=opts.BrushOpts(
                x_axis_index='all',
                brush_link='all',
                out_of_brush={'colorAlpha': 0.1},
                brush_type='lineX',
            ),
        )
    )
    # 初始化折线图，折线图代表‘ma’均值曲线
    line = (
        Line()
        .add_xaxis(xaxis_data=chart_data["categoryData"])
        .add_yaxis(
            series_name="MA5",
            y_axis=calculate_ma(day_count=5, data=chart_data),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA10",
            y_axis=calculate_ma(day_count=10, data=chart_data),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA20",
            y_axis=calculate_ma(day_count=20, data=chart_data),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA30",
            y_axis=calculate_ma(day_count=30, data=chart_data),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))
    )
    # 绘制与k线图所对应的柱状图
    bar = (
        Bar()
        .add_xaxis(xaxis_data=chart_data["categoryData"])
        .add_yaxis(
            series_name="Volume",
            y_axis=chart_data["volumes"],
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            # 坐标轴配置
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                is_scale=True,
                split_number=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    # 上面一共绘制了三种类型的图，分别是基础的k线图，代表均值的‘ma’折线图，以及表示每日最大值的柱状图，下面将三者组合到一起

    # 将折线图和k线图组合起来
    overlap_kline_line = kline.overlap(line)
    # 把折线图和k线图组合后的图与柱状图组合起来
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            animation_opts=opts.AnimationOpts(animation=True),
            renderer=RenderType.CANVAS,     # 渲染风格
            theme='white',                  # 主题风格
        )
    )
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
        ),
    )
    # 返回一个组合好的图表对象
    return grid_chart


def draw_lines_charts(stock_name: str, chart_data: dict):
    """
    绘制随时间变化指数成交额的动态变化图
    :param stock_name: 要绘制的股票指数的名字列表
    :param chart_data:  股票历史数据
    :return: 一个组合好的图对象
    """
    # 初始化时间线对象
    timeline = Timeline(
        init_opts=opts.InitOpts(
            width='100%',
            height='100%',
            animation_opts=opts.AnimationOpts(animation=True),
            renderer=RenderType.CANVAS,
            theme='white',
        )
    )
    # 设置默认开始时间，减少内存消耗和服务器压力
    if stock_name == '沪深300':
        start = 4300
    else:
        start = 7800
    for i in range(start, len(chart_data['categoryData'])):
        # 初始化折线图对象
        line = (
            Line()
            .add_xaxis(chart_data['categoryData'][0:i])
            .add_yaxis(
                series_name=f'{stock_name}成交金额',
                y_axis=chart_data['dealData'][0:i],
                is_smooth=True,     # 是否平滑曲线
                label_opts=opts.LabelOpts(is_show=True),  # 图上是否显示数字
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f'{stock_name}成交金额趋势图',
                    pos_left='10%',
                    pos_top='1%',
                ),
                xaxis_opts=opts.AxisOpts(type_="category"),
                # 设置区域缩放配置项
                datazoom_opts=opts.DataZoomOpts(
                    type_='inside',
                    range_start=99.5,
                    range_end=100,
                )
            )
        )
        # 向时间轴添加一副折线图，时间为到i为止的时间的数值
        timeline.add(chart=line, time_point=chart_data['categoryData'][i])
    # 设置时间轴的具体属性
    timeline.add_schema(
        axis_type='category',       # 坐标轴类型
        play_interval=800,          # 播放速度，单位是毫秒，越大越慢
        pos_bottom="-20px",         # 距离容器底部距离
        is_loop_play=False,         # 关闭循环播放
    )
    return timeline


if __name__ == '__main__':
    pass
    # stockName = ['上证指数', 'A股指数', '深证综指', '沪深300']
    # for name in stockName:
    #     test_data = importData(stock_name=name)
    #     spilt_data = spiltData(test_data)
    #     # charts = draw_kline_charts(stock_name=name, chart_data=spilt_data)
    #     # charts.render(f'data/{name}.html')
    # test_data = importData(stock_name=stockName[0])
    # spilt_data = spiltData(test_data)
    # lines_charts = draw_lines_charts(stock_name=stockName[0], chart_data=spilt_data)
    # lines_charts.render('data/test7.html')

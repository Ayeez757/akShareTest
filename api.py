from http.server import BaseHTTPRequestHandler
import akshare as ak
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 获取原始数据
        stock_df = ak.stock_zh_a_spot()

        # 选择需要的字段并重命名为中文说明
        selected_data = stock_df[[
            '代码', '名称', '最新价', '涨跌幅', '成交量',
            '成交额', '最高价', '最低价', '换手率'
        ]].head(20)  # 只取前20条

        # 转换为列表字典
        data_list = selected_data.to_dict('records')

        # 添加字段说明
        response_data = {
            "field_descriptions": {
                "代码": "股票交易代码",
                "名称": "公司名称",
                "最新价": "当前价格（元）",
                "涨跌幅": "涨跌百分比（%）",
                "成交量": "成交股数（股）",
                "成交额": "成交金额（元）",
                "最高价": "当日最高价（元）",
                "最低价": "当日最低价（元）",
                "换手率": "成交量/流通股本（%）"
            },
            "data": data_list
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
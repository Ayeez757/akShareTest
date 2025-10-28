from http.server import BaseHTTPRequestHandler
import akshare as ak
import json
import datetime


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 设置CORS头，允许前端访问
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # 获取股票数据
            print("正在获取股票数据...")
            stock_df = ak.stock_zh_a_spot()

            # 数据清洗：过滤ST股票和科创板
            clean_df = stock_df[
                (~stock_df['名称'].str.contains('ST', na=False)) &
                (~stock_df['代码'].str.startswith('688', na=False))
                ]

            # 选择需要的列并重命名
            selected_data = clean_df[[
                '代码', '名称', '最新价', '涨跌幅', '涨跌额',
                '成交量', '成交额', '最高价', '最低价', '今开', '昨收'
            ]].head(30)  # 只取前30条

            # 构建响应数据
            result = {
                "success": True,
                "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_count": len(selected_data),
                "field_descriptions": {
                    "代码": "股票交易代码",
                    "名称": "公司名称",
                    "最新价": "当前价格（元）",
                    "涨跌幅": "涨跌百分比（%）",
                    "涨跌额": "价格变动（元）",
                    "成交量": "成交股数",
                    "成交额": "成交金额（元）",
                    "最高价": "当日最高价（元）",
                    "最低价": "当日最低价（元）",
                    "今开": "今日开盘价（元）",
                    "昨收": "昨日收盘价（元）"
                },
                "data": selected_data.to_dict(orient='records')
            }

            # 返回JSON数据
            response = json.dumps(result, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode('utf-8'))
            print("数据返回成功")

        except Exception as e:
            print(f"发生错误: {str(e)}")
            error_response = {
                "success": False,
                "error": f"获取数据失败: {str(e)}",
                "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            response = json.dumps(error_response, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))
# 載入 flask 模組中的 Flask, request, abort
from flask import Flask, request, abort
# 載入 linebot 模組中的 LineBotApi（Line Token）, WebhookHandler（Line Secret）
from linebot import (
    LineBotApi, WebhookHandler
)
# 載入 linebot.exceptions 模組中的 InvalidSignatureError（錯誤偵錯用的）
from linebot.exceptions import (
    InvalidSignatureError
)
# 載入 linebot.models 模組中的 MessageEvent, TextMessage, TextSendMessage
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
# 載入 json 模組（格式化輸出結果）
import json


# 建立 application 物件
app = Flask(__name__)
# LINE BOT-Channel Access Token
line_bot_api = LineBotApi("CHANNEL_ACCESS_TOKEN")
# LINE BOT-Channel Secret
handler = WebhookHandler("CHANNEL_SECRET")

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=["POST"])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # 將接收到的請求轉換為文字
    body = request.get_data(as_text=True)
    # 將接收到的資訊轉為 JSON 格式
    json_data = json.loads(body)
    # 格式化 json_data 讓輸出結果增加可讀性
    json_str = json.dumps(json_data, indent=4)
    # 印出來檢視一下
    print(json_str)
    # Handle Webhook body
    try:
        # 如果 Channel Access Token 或 Channel Secret 發生錯誤
        # 會進入到 except InvalidSignatureError: 區塊。
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 如果有錯誤代表 Channel Access Token 與 Channel Secret
        # 可能輸入錯誤或無效。
        # 處理錯誤，abort 400。
        abort(400)
    # 返回 OK，LINE Developers 收到 OK 後代表 Webhook 執行沒問題
    return "OK"
        
    
if __name__ == "__main__":
    app.run(port=3000)

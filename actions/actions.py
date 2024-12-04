# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pyodbc

class DatabaseHandler:
    def __init__(self):
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"  # or "SERVER_NAME\INSTANCE_NAME" for named instances
            "DATABASE=QLBANXE;"
            "UID=sa;"  # replace with your username
            "PWD=2710;"  # replace with your password
        )

    def fetch_data(self):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM XeTonKho")
        rows = []
        row = cursor.fetchone()
        while row:
            rows.append(row[5])
            row = cursor.fetchone()
        conn.close()
        return rows

class ActionConvertCcToPhanKhoi(Action):

    def name(self) -> str:
        return "action_convert_cc_to_phan_khoi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Lấy giá trị của slot 'spec'
        spec = tracker.get_slot('spec') 
        print("Dữ liệu slot 'spec':", spec)
        
        slots = tracker.current_slot_values()
        print("Các slot hiện tại:", slots)
        
        # Kiểm tra nếu spec có giá trị và chứa 'cc'
        if spec and 'cc' in spec:
            # Thực hiện chuyển đổi 'cc' thành 'phân khối'
            updated_spec = re.sub(r'(\d+)\s?cc', r'\1 phân khối', spec)
            # Cập nhật lại slot 'spec' với giá trị đã chuyển đổi
            return [SlotSet('spec', updated_spec)]
        else:
            # Nếu không có 'cc' trong spec, không cần thay đổi
            return []
        

class ActionCheckSlots(Action):

    def name(self) -> str:
        return "action_check_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Lấy giá trị của các slot
        color = tracker.get_slot('color')
        version = tracker.get_slot('version')
        brand = tracker.get_slot('brand')
        model = tracker.get_slot('model')
        spec = tracker.get_slot('spec')
        brake = tracker.get_slot('brake')
        warranty = tracker.get_slot('warranty')
        type = tracker.get_slot('type')
        
        # Tạo danh sách các thông tin đã được cung cấp
        info = []
        if color:
            info.append(f"- Màu sắc: {color}")
        if version:
            info.append(f"- Phiên bản: {version}")
        if brand:
            info.append(f"- Hãng: {brand}")
        if model:
            info.append(f"- Dòng xe: {model}")
        if spec:
            info.append(f"- Thông số: {spec}")
        if brake:
            info.append(f"- Loại phanh: {brake}")
        if warranty:
            info.append(f"- Bảo hành: {warranty}")
        if type:
            info.append(f"- Loại xe: {type}")

        # In ra tất cả các thông tin từ các slot
        print(f"Dữ liệu slot 'color': {color}")
        print(f"Dữ liệu slot 'version': {version}")
        print(f"Dữ liệu slot 'brand': {brand}")
        print(f"Dữ liệu slot 'model': {model}")
        print(f"Dữ liệu slot 'spec': {spec}")
        print(f"Dữ liệu slot 'brake': {brake}")
        print(f"Dữ liệu slot 'warranty': {warranty}")
        print(f"Dữ liệu slot 'type': {type}")
        
        # Kiểm tra số lượng thông tin đã được cung cấp
        
        if len(info) < 1:
            response = "Bạn chưa cung cấp đủ thông tin. Vui lòng cung cấp thêm chi tiết về xe bạn muốn tìm."
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(response="utter_vehicle_information")
        
        return []

# class ActionResetSlots(Action):
#     def name(self) -> str:
#         return "action_reset_slots"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict) -> list:
        
#         # Lấy danh sách các slot hiện tại
#         slots = tracker.slots.keys()
        
#         # Tạo danh sách các sự kiện để đặt lại giá trị của các slot về None
#         reset_events = [SlotSet(slot, None) for slot in slots]
        
#         dispatcher.utter_message(text="Tất cả thông tin đã được xóa. Bạn có thể bắt đầu lại từ đầu.")
        
#         return reset_events


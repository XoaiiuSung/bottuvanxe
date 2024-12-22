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
import pyodbc
import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
    
class ActionSearchVehicleDb(Action):

    def name(self) -> Text:
        return "action_search_vehicle_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Collect slot values
        color = tracker.get_slot('color') or ''
        brand = tracker.get_slot('brand') or ''
        spec = tracker.get_slot('spec') or ''
        brake_type = tracker.get_slot('brake') or ''
        version = tracker.get_slot('version') or ''
        model = tracker.get_slot('model') or ''
        fuelConsumption = tracker.get_slot('fuelConsumption') or ''
        warranty = tracker.get_slot('warranty') or ''
        maxprice = tracker.get_slot('maxprice') or ''
        vehicle_type = tracker.get_slot('type') or ''

        print(f"Slots: color={color}, brand={brand}, spec={spec}, brake_type={brake_type}, version={version}, model={model}, fuelConsumption={fuelConsumption}, warranty={warranty}, maxprice={maxprice}, vehicle_type={vehicle_type}")

        # Truy vấn database
        vehicle_links = self.query_vehicle_db(color, brand, spec, brake_type, version, model, fuelConsumption, warranty, maxprice, vehicle_type)

        if vehicle_links:
            dispatcher.utter_message(text=f"Tôi tìm được những xe sau phù hợp với yêu cầu của bạn: {vehicle_links}")
        else:
            dispatcher.utter_message(text="Không tìm thấy xe nào phù hợp với thông tin bạn cung cấp.")

        return []

    def query_vehicle_db(self, color, brand, spec, brake_type, version, model, fuelConsumption, warranty, maxprice, vehicle_type):
        try:
            # Convert spec from '125 phân khối' to '125'
            if spec:
                spec = re.sub(r'(\d+)\s?phân khối', r'\1', spec, flags=re.IGNORECASE)

            # Kết nối tới db
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost;'
                'DATABASE=QLBANXE;'
                'UID=sa;'
                'PWD=kc'
            )
            cursor = conn.cursor()

            # Execute the stored procedure
            cursor.execute("""
                EXEC TimKiemXeTheoYeuCau @tenmau=?, @phienban=?, @hang=?, @dongxe=?, @phankhoi=?, @tieuthu=?, @phanhabs=?, @baohanh=?, @tenloai=?
            """, (color, version, brand, model, spec, fuelConsumption, brake_type, warranty, vehicle_type))

            results = cursor.fetchall()

            print(f"Results: {results}")

            # Close the connection
            cursor.close()
            conn.close()

            if results:
                print(f"Found {len(results)} vehicles.")
                # Format the results as needed
                links = []
                for result in results:
                    link = f"<li><a className='text-light' href='http://localhost:3000/{result.MaLoai}/{result.MaXe}-{result.MaPhienBan}?color={result.MaMau}' target='_blank' rel='noopener noreferrer'>{result.TenXe}</a></li>"
                    links.append(link)
                return "<ul>" + "".join(links) + "</ul>"
            else:
                print("No vehicles found.")
                return None

        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {e}")
            return None

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
        fuelConsumption = tracker.get_slot('fuelConsumption')
        brake = tracker.get_slot('brake')
        warranty = tracker.get_slot('warranty')
        type = tracker.get_slot('type')
        maxprice = tracker.get_slot('maxprice')
        
        # Xử lý dữ liệu slot
        spec = self.convert_engine_capacity(spec) 
        
        # Tạo danh sách các thông tin đã được cung cấp
        info = []
        if color:
            info.append(f"màu sắc: {color}")
        if version:
            info.append(f"phiên bản: {version}")
        if brand:
            info.append(f"hãng: {brand}")
        if model:
            info.append(f"dòng xe: {model}")
        if spec:
            info.append(f"thông số: {spec}")
        if fuelConsumption:
            info.append(f"tiêu thụ: {fuelConsumption}")    
        if brake:
            info.append(f"loại phanh: {brake}")
        if warranty:
            info.append(f"bảo hành: {warranty}")
        if type:
            info.append(f"loại xe: {type}")
        if maxprice:
            info.append(f"giá tối đa: {maxprice}")

        # In ra tất cả các thông tin từ các slot
        print(f"Dữ liệu slot 'color': {color}")
        print(f"Dữ liệu slot 'version': {version}")
        print(f"Dữ liệu slot 'brand': {brand}")
        print(f"Dữ liệu slot 'model': {model}")
        print(f"Dữ liệu slot 'spec': {spec}")
        print(f"Dữ liệu slot 'fuelConsumption': {fuelConsumption}")
        print(f"Dữ liệu slot 'brake': {brake}")
        print(f"Dữ liệu slot 'warranty': {warranty}")
        print(f"Dữ liệu slot 'type': {type}")
        print(f"Dữ liệu slot 'maxprice': {maxprice}")

        
        # Kiểm tra số lượng thông tin đã được cung cấp
        
        if len(info) < 1:
            response = "Dạ bạn chưa cung cấp đủ thông tin ạ. Vui lòng cung cấp thêm chi tiết về xe bạn muốn tìm."
            dispatcher.utter_message(text=response)
        else:
            response = (
                "Bạn muốn tìm xe với các thông tin sau: "
                + "; ".join(info)
                + "."
            )
            dispatcher.utter_message(text=response)
            # dispatcher.utter_message(response="utter_vehicle_information")
        
        return []
    
    def convert_engine_capacity(self, text: str) -> str:
        """
        Chuyển đổi các ký hiệu dung tích động cơ từ '125cc' hoặc '125 cc' thành '125 phân khối'.
        
        Args:
            text (str): Giá trị từ slot 'spec'

        Returns:
            str: Giá trị đã được chuyển đổi
        """
        if text:
            # Tìm các giá trị khớp với mẫu như '125cc' hoặc '125 cc'
            updated_text = re.sub(r'(\d+)\s?cc', r'\1 phân khối', text, flags=re.IGNORECASE)
            return updated_text
        return text

class ActionAskForMoreInfo(Action):

    def name(self) -> str:
        return "action_ask_for_more_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        dispatcher.utter_message(text="Bạn còn muốn thêm thông tin nào không?")
        return []
    
class ActionThankForWaiting(Action):

    def name(self) -> str:
        return "action_thank_for_waiting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        dispatcher.utter_message(text="Dạ cảm ơn bạn đã chờ ạ!")
        return []
    
class ActionConfirmVehicleInformation(Action):

    def name(self) -> str:
        return "action_confirm_vehicle_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        dispatcher.utter_message(text="Cảm ơn bạn đã cung cấp thông tin. Tôi sẽ tìm kiếm thông tin về xe phù hợp nhất với yêu cầu của bạn.")
        return []


class ActionResetSlots(Action):

    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Lấy danh sách các slot hiện tại
        slots = tracker.slots.keys()
        
        # Tạo danh sách các sự kiện để đặt lại giá trị của các slot về None
        reset_events = [SlotSet(slot, None) for slot in slots]
        
        dispatcher.utter_message(text="Dạ bạn muốn tư vấn về mẫu xe nào khác ạ?")
        dispatcher.utter_message(text="Bạn vui lòng cung cấp thông tin mẫu xe để tôi có thể tìm kiếm thông tin phù hợp nhất với yêu cầu của bạn nhé.")
        
        return reset_events


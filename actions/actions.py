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

class ActionConvertCcToPhanKhoi(Action):

    def name(self) -> str:
        return "action_convert_cc_to_phan_khoi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"  # or "SERVER_NAME\INSTANCE_NAME" for named instances
            "DATABASE=QLBANXE;"
            "UID=sa;"  # replace with your username
            "PWD=2710;"  # replace with your password
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM XeTonKho")
        row = cursor.fetchone()
        while row:
            print(row[5])
            row = cursor.fetchone()
        conn.close()
        
        slots = tracker.get_slot('vehicle_information')
        if slots:
            updated_slots = [re.sub(r'(\d+)\s?cc', r'\1 phân khối', slot) for slot in slots]
        else:
            updated_slots = slots

        return [SlotSet('vehicle_information', updated_slots)]
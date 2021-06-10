# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from crawler import get_covid_stat_allregions, get_vaccination_stat, prepare_soup, findby_city_name, get_covid_stat

soup = prepare_soup()

class ActionCovidStatCity(Action):
    def __init__(self):
        Action.__init__(self)
        global soup
        self.data = get_covid_stat_allregions(soup)

    def name(self) -> Text:
        return "action_covid_stat_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city_name = tracker.get_slot("city_name")
        data = findby_city_name(self.data, city_name)
        if isinstance(data, str):
            dispatcher.utter_message(text=data)
        
        else :
            response = """
تقرير الحالات فمدينة {}
الحالات الجديدة : {}
عدد الوفيات : {}
({})
            """
            dispatcher.utter_message(text=response.format(data["city_name"], data["new_cases"], data["deaths"], data["last_update"]))

        return []

class ActionCovidDailyReport(Action):
    def __init__(self):
        Action.__init__(self)
        global soup
        self.data = get_covid_stat(soup)

    def name(self) -> Text:
        return "action_covid_daily_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = """
هذا هو التقرير ديال الحالات ({})
ـ عدد حالات الإصابة : {}
ـ عدد المتعافين : {}
ـ عدد الوفيات : {}
ـ عدد التحاليل : {}
            """.format(self.data["last_update"], self.data["daily_new_cases"], self.data["daily_recovered"], self.data["daily_deaths"], self.data["daily_tests"])

        dispatcher.utter_message(text=response)

        return []

class ActionVaccinationReport(Action):
    def __init__(self):
        Action.__init__(self)
        global soup
        self.data = get_vaccination_stat(soup)
    def name(self) -> Text:
        return "action_vaccination_report"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            response = """
عدد د الناس لي خداو لقاح:
الجرعة الاولى : {}
الجرعة الثانية : {}
            """.format(self.data['first_vac'], self.data['second_vac'])
            dispatcher.utter_message(response)
            
            return []
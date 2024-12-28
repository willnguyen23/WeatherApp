import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Check weather ", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.addingWidgets()
        self.LooksMaxing()

    def addingWidgets(self):
        main_layout = QVBoxLayout(self)
        input_layout = QHBoxLayout(self)

        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.get_weather_button)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.temperature_label)
        main_layout.addWidget(self.emoji_label)
        main_layout.addWidget(self.description_label)

        self.get_weather_button.clicked.connect(self.getInfo)

    def LooksMaxing(self):
        self.setGeometry(550, 350, 300, 300)

        self.city_input.setPlaceholderText("Search for a city")

        self.get_weather_button.setStyleSheet("font-size: 10px;")

        self.temperature_label.setAlignment(Qt.AlignHCenter)
        self.temperature_label.setStyleSheet("font-size: 60px;")

        self.emoji_label.setAlignment(Qt.AlignHCenter)
        self.emoji_label.setStyleSheet("font-size: 90px;"
                                       "font: Segoe UI emoji;")

        self.description_label.setAlignment(Qt.AlignHCenter)
        self.description_label.setStyleSheet("font-size: 20px;")

    def getInfo(self):
        api_key = "e37713da4ea58f8909a9b84da4f758cd"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(data)

            if data["cod"] == 200:
                self.display_weather(data)
                
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error("HTTP error occured\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connect Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.ToomanyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException:
            self.display_error(f"Request Error:\n{req_error}")
    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 20px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setText(f"{((data["main"]["temp"]) * 9/5) - 459.67:.0f}°F")
        self.emoji_label.setText(self.get_emoji(data["weather"][0]["id"]))
        self.description_label.setText(data["weather"][0]["description"])

    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "🌥️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
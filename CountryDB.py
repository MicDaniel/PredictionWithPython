import pandas as pd
import logics
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

df = pd.read_csv("data/rnewEnergy.csv")
countries = df["Country Name"].tolist()
df.set_index("Country Name", inplace=True)

#print(df.head(10))
#print(df.loc["Aruba"])
#logics.movingAverage(df.loc["Aruba"])
#logics.movingAverage(df.loc["Romania"])

class CountryDB(BoxLayout):
    top_layout = ObjectProperty(None)


    def __init__(self, *args, **kwargs):
        super(CountryDB, self).__init__(*args, **kwargs)
        self.drop_down = DropDown()

        dropdown = DropDown()
        for country in countries:
            btn = Button(text='%r' % country, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = Button(text='Countries', size_hint=(1, 1))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        dropdown.bind(on_select=lambda instance, x: setattr(self.top_layout, 'text', x))
        self.top_layout.add_widget(mainbutton)


    def plotData(self):
        country = self.top_layout.text.replace("'", "")
        logics.simplePlot(df.loc[country])

    def movingAverageButton(self):
        country = self.top_layout.text.replace("'", "")
        logics.movingAverage(df.loc[country])


    def weigthedMovingAverageButton(self):
        country = self.top_layout.text.replace("'", "")
        logics.weightedMovingAverage(df.loc[country])


class CountryDBApp(App):
    def build(self):
        return CountryDB()


if __name__ == "__main__":
    CountryDBApp().run()
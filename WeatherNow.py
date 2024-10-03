# WeatherNow using tkinter

#Created By:--
#   Marco George | ID:800149997
#   Ahmed Abdalhamied | ID:800149181
#   Mohammed Hisham | ID:800166587
#   Ibrheim El Sharkawy | ID:800149116
#   Mohamed Moaty | ID:800150113

# importing libraries
import requests, json, datetime
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# tkinter window bulid
root = Tk()
root.title("Weather Now App")
root.geometry("1150x700")
root['background'] = '#20baa8'

# Setting icon of master window
p1 = PhotoImage(file='Images\logo1.png')
root.iconphoto(False, p1)

# app icon inside the window
icon1 = ImageTk.PhotoImage(Image.open('Images\logo.png'))
panel = Label(root, image=icon1, bd=0)
panel.place(x=5, y=5)

# title next to inside icon
logo_text = Label(root, text="Weather Now", fg='white', font=('stencil', 32), bg='#20baa8')
logo_text.place(x=90, y=20)

# API key to access
api_key = '5524f9083acb1308eb95912a546696ef'

# Declaring Global Unit_Entry
global unit_entry
unit_entry = "metric"


# -HELP WINDOW

def helpinformation():
    messagebox.showinfo("Help Information",
                        "First: Select Which Temperature Unit you want to use either (Celsuis)(metric system) or (Fahrenheit)(imperial system) Celsuis chosen by Default\n"
                        "Note: Click Search if you want to see the other units measurement "
                        "Then: Enter [City_Name,Country]  you want to check weather for Example: [Cairo,EG]")
Help = Button(root, text="Help To Use? Click Here!", width=20, relief=RAISED, bg='white', command=helpinformation,
              fg='black')
Help.place(x=995, y=0)



#time and date labels in window

dt = datetime.datetime.now()
date = Label(root, text=dt.strftime('%A'), fg='white', bg='#20baa8', font=('stencil', 20))  #%A for day
date.place(x=230, y=100)

month = Label(root, text=dt.strftime('%d %B'), fg='white', bg='#20baa8', font=('stencil', 15))  #%d for day and %B for Month
month.place(x=380, y=107.5)


hour = Label(root, text=dt.strftime('%I : %M %p'),      #%I for 12 houer prsention and %M for minutes and %p for PM or AM
             bg='#20baa8', fg='white', font=('stencil', 20))
hour.place(x=85, y=100)

# Search bar icon image
search_icon = ImageTk.PhotoImage(Image.open('Images\city_icon.png'))
panel = Label(root, image=search_icon, bd=0)
panel.place(x=80, y=160)

# city entry box
city_name = StringVar()
city_entry = Entry(root, textvariable=city_name, width=18, bg="white", fg="black", font=("Comic sans MS", 13))
city_entry.place(x=97, y=163.5)
city_entry.focus() # City entry focus to focus on entry box to write without selecting the city_entry box

# Unit = Metric
def metric_clicked():
    global unit_entry
    unit_entry = "metric"
    # updating degree label to celsius using overlayers
    CelsuisUnitTemp = create_label('°C')
    CelsuisUnitTemp.place(x=330, y=265)
    CelsuisUnitTemp0 = create_label("°C")
    CelsuisUnitTemp0.place(x=345, y=317 + 30)
    CelsuisUnitTemp1 = create_label("°C")
    CelsuisUnitTemp1.place(x=345, y=357 + 40)
    UnitMS = create_label("meter/sec ")
    UnitMS.place(x=350, y=437 + 50)
    city_name()

# Units = imperial
def imperial_clicked():
    global unit_entry
    unit_entry = "imperial"
    # Updating the unit from metric system to imperial system by using overlays
    CelsuisUnitTemp = create_label('°F')
    CelsuisUnitTemp.place(x=330, y=265)
    CelsuisUnitTemp0 = create_label("°F")
    CelsuisUnitTemp0.place(x=345, y=317 + 30)
    CelsuisUnitTemp1 = create_label("°F")
    CelsuisUnitTemp1.place(x=345, y=357 + 40)
    UnitMS = create_label("mile/hours")
    UnitMS.place(x=350, y=437 + 50)
    city_name()

# function to create labels easier for degrees and units
def create_label(text, ):
    label = Label(root, text=text, fg='white', bg="#20baa8", font=('Arial Rounded MT Bold', 20))
    label.place(x=600, y=500)
    return label

# main API requests functions and assigning it to labels to be updated
# event=None to pass parameter to bind key with <Return>
def city_name(event=None):

    # API Call
    api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q="
                               + city_entry.get() + "&units=" + unit_entry + "&appid=" + api_key)

    # json.loads to load the api contents from json file
    api = json.loads(api_request.content)

    # error handling condition if the city was not found or the server of the api was down or no city was entered
    if api['cod'] == '404':
        messagebox.showerror('Error', 'City Not Found !! Please Enter City Name Correctly Followed By Country'
                                      'Example  "Mansoura,EG"')
    else:
        # Temperatures
        y = api['main']
        current_temprature = y['temp']
        humidity = y['humidity']
        tempmax = y['temp_max']
        tempmin = y['temp_min']

        # Coordinates
        x = api['coord']
        longtitude = x['lon']
        latitude = x['lat']

        # Country
        z = api['sys']
        country = z['country']
        city = api['name']

        # Wind
        n = api['wind']
        windspeed = n['speed']
        winddegree = n['deg']

        # Weather Condition
        w = api['weather']
        weather = w[0]['main']

        # Adding the received info into the screen
        label_temp.configure(text=current_temprature)
        label_humidity.configure(text=humidity)
        max_temp.configure(text=tempmax)
        min_temp.configure(text=tempmin)
        label_lon.configure(text=longtitude)
        label_lat.configure(text=latitude)
        label_country.configure(text=country)
        label_city.configure(text=city)
        label_wind_speed.configure(text=windspeed)
        label_wind_degree.configure(text=winddegree)
        label_weather.configure(text=weather)

        # update image depending on the weather condition
        def images_handling(x):
            # passing x parameter because we can't use label_weather since it isn't loaded yet...
            # Function to place images on the window
            if x == 'Clear':
                # if the weather condition is clear we display night or morning image
                if int((dt.strftime('%H'))) >= 7 & int((dt.strftime('%H'))) <= 17:
                    img = ImageTk.PhotoImage(Image.open('Images\Clear_sun.png'))
                    panel = Label(root, image=img, bd=0)
                    panel.photo = img
                    panel.place(x=570, y=115)

                else:
                    img = ImageTk.PhotoImage(Image.open('Images\Clear_moon.png'))
                    panel = Label(root, image=img, bd=0)
                    panel.photo = img
                    panel.place(x=570, y=115)

            elif x == 'Rain':
                img = ImageTk.PhotoImage(Image.open('Images\Rain.png'))
                panel = Label(root, image=img, bd=0)
                panel.photo = img
                panel.place(x=570, y=115)

            elif x == 'Snow':
                img = ImageTk.PhotoImage(Image.open('Images\Snow.png'))
                panel = Label(root, image=img, bd=0)
                panel.photo = img
                panel.place(x=570, y=115)

            elif x == 'Thunderstorm':
                img = ImageTk.PhotoImage(Image.open('Images\Thunderstorm.png'))
                panel = Label(root, image=img, bd=0)
                panel.photo = img
                panel.place(x=570, y=115)

            elif x == 'Drizzle':
                img = ImageTk.PhotoImage(Image.open('Images\Drizzle.png'))
                panel = Label(root, image=img, bd=0)
                panel.photo = img
                panel.place(x=570, y=115)

            elif x == 'Clouds' or 'Haze':
                img = ImageTk.PhotoImage(Image.open('Images\Clouds.png'))
                panel = Label(root, image=img, bd=0)
                panel.photo = img
                panel.place(x=570, y=115)

            else:
                img = ImageTk.PhotoImage(Image.open('Images\Atmosphere.png'))
                panel = Label(root, image=img, bd=0)
                panel.photo = img
                panel.place(x=570, y=115)

        images_handling(weather)
        return city_name

#entry.bind = return so we can use Enter instead of pressing on "Search"
city_entry.bind("<Return>",city_name)

# Search Button
city_nameButton = Button(root, text="Search", bg="white", fg="gray",command=city_name,font=("bold", 11), height=0, width=8)
city_nameButton.place(x=295, y=163.3)


# Unit Measurement Choice Button Metric
unit_choiceButton = Button(root, text="Celsius", command=metric_clicked, width=10,
                           bg="#009cf2", fg="white", font=("arial", 13, "bold"))
unit_choiceButton.place(x=110, y=200)

# Unit Measurement Choice Button Fahrenheit
unit_choiceButton2 = Button(root, text="Fahrenheit", command=imperial_clicked, width=10,
                            bg="#009cf2", fg="white", font=("arial", 13, "bold"))
unit_choiceButton2.place(x=250, y=200)

# Buttons & Labels
# Country Names and Coordinates
label_city = Label(root, text="City...", width=0,
                   bg='#20baa8', fg='white', font=("bold", 17))
label_city.place(x=160 + 520 + 15, y=570)

label_country = Label(root, text="Country...", width=0,
                      bg='#20baa8', fg='white', font=("bold", 17))
label_country.place(x=260 + 520 + 50, y=570)

label_lon = Label(root, text="lon..", width=0,
                  bg='#20baa8', fg='white', font=("Comic sans MS", 17))
label_lon.place(x=140 + 510 + 30, y=610)

label_lat = Label(root, text="lat..", width=0,
                  bg='#20baa8', fg='white', font=("Comic sans MS", 17))
label_lat.place(x=245 + 530 + 30, y=610)

# Current Temperature
label_temp = Label(root, text="TEMP", width=0, bg='#20baa8',
                   font=("Comic sans MS", 36, "bold"), fg='white')
label_temp.place(x=155, y=255)

CelsuisUnitTemp = create_label('°C')
CelsuisUnitTemp.place(x=330, y=265)

# Other temperature details (Max and min)
maxi = Label(root, text="Max. Temp: ", width=0,
             fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
maxi.place(x=120, y=320 + 30)

max_temp = Label(root, text="MAX", width=0,
                 fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
max_temp.place(x=270, y=320 + 30)
CelsuisUnitTemp0 = create_label("°C")
CelsuisUnitTemp0.place(x=345, y=317 + 30)

mini = Label(root, text="Min. Temp: ", width=0,
             fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
mini.place(x=120, y=360 + 40)

min_temp = Label(root, text="MIN", width=0,
                 fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
min_temp.place(x=270, y=360 + 40)
CelsuisUnitTemp1 = create_label("°C")
CelsuisUnitTemp1.place(x=345, y=357 + 40)

# humidity label
humid = Label(root, text="Humidity: ", width=0,
              bg='#20baa8', fg='white', font=('Arial Rounded MT Bold', 17))
humid.place(x=120, y=400 + 45)

label_humidity = Label(root, text="HMD", width=0,
                       fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
label_humidity.place(x=270, y=400 + 45)
UnitPercent = create_label("%")
UnitPercent.place(x=350, y=397 + 45)

# Wind labels (speed and degree)
wind_speed = Label(root, text="Wind Speed: ", width=0,
                   fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
wind_speed.place(x=120, y=440 + 50)

label_wind_speed = Label(root, text="SPD", width=0,
                         fg='white', bg="#20baa8", font=('Arial Rounded MT Bold', 17))
label_wind_speed.place(x=279, y=440 + 50)
UnitMS = create_label("meter/sec ")
UnitMS.place(x=350, y=437 + 50)

wind_degree = Label(root, text="Wind Degree: ", width=0,
                    fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 17))
wind_degree.place(x=120, y=480 + 54)

label_wind_degree = Label(root, text="...", width=0,
                          fg='white', bg="#20baa8", font=('Arial Rounded MT Bold', 17))
label_wind_degree.place(x=295, y=480 + 54)
UnitDegree = create_label("°Degree")
UnitDegree.place(x=350, y=477 + 54)

# Weather condition
label_weather = Label(root, text="Weather Status", width=0,
                      fg='white', bg='#20baa8', font=('Arial Rounded MT Bold', 25))
label_weather.place(x=700 + 30, y=70)

# Closing master root window to Wrap contents
root.mainloop()
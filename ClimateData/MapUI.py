from cgitb import text
from tkinter import *
from tkinter import ttk
from tkinter.tix import ButtonBox
from turtle import left
from tkintermapview import TkinterMapView as TKMV
import psycopg2
import database
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=PASSWORD")
cur = conn.cursor()
marks = []

root = Tk()
root.geometry("1500x900")
root.title("Climate Data Map")
buttonFrame = Frame(root)
buttonFrame.pack()
mapFrame = Frame(root)
mapFrame.pack(side=BOTTOM)
rightFrame = Frame(root)
rightFrame.pack(side=BOTTOM)

states_abb = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

def clearMarks():
  for mark in marks:
    mark.delete()

def SelectState(event = None):
  state = event.widget.get()
  
  cur.execute("""SELECT * FROM county_codes WHERE state = %s;""", [states_abb[state]])
  conn.commit()
  data = cur.fetchall()
  for row in data:
    print(row)
    mark = map_widget.set_address(f"%s, %s" % (row[2], state), marker=True)
    mark.set_text(row[2] + ", " + state)
    marks.append(mark)
  
  map_widget.set_zoom(8)

#Initialize dropdown Widget *Source Adriana Swantz UI Code
dropdown = ttk.Combobox(buttonFrame, font="Verdana 15 bold")
dropdown['state'] = 'readonly'
dropdown['values'] = (['Alaska','Alabama','Arkansas','Arizona','California','Colorado','Connecticut','Delaware','Florida',
'Georgia','Iowa','Idaho','Illinois','Indiana','Kansas','Kentucky','Louisiana','Massachusetts','Maryland','Maine','Michigan',
'Minnesota','Missouri','Mississippi','Montana','North Carolina','Nevada','Nebraska','New Hampshire','New Jersey','New Mexico',
'New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
'Virgina','Vermont','Washington','Wisconsin','West Virginia','Wyoming'])
dropdown.bind('<<ComboboxSelected>>', SelectState)
dropdown.pack(pady=10)

#Month + Year Drop down
start_date = Label(buttonFrame, text="Start Date")
start_date.pack()
start_month = ttk.Combobox(buttonFrame)
start_month.pack(side=LEFT)
# month_dropdown['month'] = 'readonly'
start_month['values'] = (['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])

start_year = ttk.Combobox(buttonFrame)
start_year.pack(side=LEFT)

#Right Frame
clearButton = Button(rightFrame, text="Clear all marks", command=clearMarks)
clearButton.pack(expand=True)

map_widget = TKMV(root, width=800, height=600, corner_radius=100)
map_widget.place(relx=0.5, rely=0.5, anchor=CENTER)
map_widget.set_address("Colorado")
map_widget.set_zoom(4)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
#map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
#map_widget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style
#map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white

root.mainloop()
import tkinter 
import customtkinter as c
from tkinter import messagebox
from PIL import Image, ImageTk
import requests


c.set_appearance_mode("System")
root = c.CTk()
root.geometry("600x600")
root.title("Sevim's Weather app")
root.config(bg="lightblue")

def get_wather(city):
    API_key = "824497e9b14fc2acb5d6811241a463e1"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error","City Not Found")
        return None
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']

    
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return(icon_url,temperature,description,city_name,country)

def search():
    city_name =city_entry.get()
    result = get_wather(city_name)
    if result is None:
       return
    icon_url, temperature, description, city_name, country = result
    title1.configure(text=f"{city_name},{country}")
    responde = requests.get(icon_url,stream=True)

    image = Image.open(responde.raw)
    icon = ImageTk.PhotoImage(image)
    titleimage.configure(image=icon)
    titleimage.image = icon

    title2.configure(text=f"temperature:{temperature:.2f}C")
    title3.configure(text=f"description{description}")
   
city_entry = c.CTkEntry(root,border_color="#73C9D3",border_width=2,corner_radius=0,fg_color="white",text_color="black")
city_entry.place(relx=0.3,rely=0.1,relwidth=0.4,relheight=0.05)

button = c.CTkButton(root,corner_radius=0,command=search)
button.place(relx=0.43,rely=0.2,relwidth=0.15,relheight=0.05)

title1=c.CTkLabel(root,fg_color="lightblue",corner_radius=0,font=("Bold",20),text_color="black")   
title1.place(relx=0.3,rely=0.3,relwidth=0.4,relheight=0.1)

title2=c.CTkLabel(root,fg_color="lightblue",corner_radius=0,font=("Bold",20),text_color="black") 
title2.place(relx=0.3,rely=0.4,relwidth=0.4,relheight=0.1)

titleimage = c.CTkLabel(root,text=None,fg_color="lightblue")
titleimage.place(relx=0.44,rely=0.7)

title3=c.CTkLabel(root,fg_color="lightblue",corner_radius=0,font=("Bold",20),text_color="black")   
title3.place(relx=0.2,rely=0.5,relwidth=0.6,relheight=0.1)

root.mainloop()
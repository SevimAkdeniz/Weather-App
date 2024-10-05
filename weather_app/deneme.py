import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO  # Use BytesIO to handle image data

ctk.set_appearance_mode("System")
root = ctk.CTk()
root.geometry("600x600")
root.title("Sevim's Weather App")
root.config(bg="lightblue")

def get_weather(city):
    API_key = "824497e9b14fc2acb5d6811241a463e1"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City Not Found")
        return None
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return icon_url, temperature, description, city_name, country

def search():
    city_name = city_entry.get()
    result = get_weather(city_name)
    if result is None:
        return
    icon_url, temperature, description, city_name, country = result
    title1.configure(text=f"{city_name}, {country}")

    try:
        response = requests.get(icon_url)
        image = Image.open(BytesIO(response.content))
        icon = ImageTk.PhotoImage(image)
        
        # Update the icon label with the new image
        title2.configure(image=icon)
        title2.image = icon  # Keep a reference to avoid garbage collection
        
        # Update text labels
        title3.configure(text=f"Temperature: {temperature:.2f}°C")
        description_label.configure(text=f"Description: {description}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image. Error: {e}")

# GUI setup
city_entry = ctk.CTkEntry(root, border_color="#73C9D3", border_width=2, corner_radius=0, fg_color="white")
city_entry.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.05)

button = ctk.CTkButton(root, corner_radius=0, command=search, text="Search")
button.place(relx=0.43, rely=0.2, relwidth=0.15, relheight=0.05)

title1 = ctk.CTkLabel(root, fg_color="lightblue", corner_radius=0, font=("Bold", 20), text_color="black")
title1.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.1)

title2 = ctk.CTkLabel(root, fg_color="lightblue", corner_radius=0)
title2.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.2)

title3 = ctk.CTkLabel(root, fg_color="lightblue", corner_radius=0, font=("Bold", 20), text_color="black")
title3.place(relx=0.2, rely=0.6, relwidth=0.6, relheight=0.1)

description_label = ctk.CTkLabel(root, fg_color="lightblue", corner_radius=0, font=("Bold", 20), text_color="black")
description_label.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.1)

root.mainloop()

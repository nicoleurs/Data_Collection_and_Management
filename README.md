# Plan your Trip with Kayak !

## Project description
Kayak's marketing team discovered that **70% of their users who are planning a trip would like to have more information about the destination they are going to**

Therefore, it would be great to create an application that would recomend to users where to plan their next holidays based on:
* Weather
* Hotels in the area

At any given time.

## Objectives
To create an application that:
* Scrapes hotel data from destinations (from booking, owned by kayak)
* Gets weather data from each destination
* Stores the information in a datalake
* ETLs cleaned data from the data lake to a data warehouse
* Displays the information to users.

## Scope
This project focuses only on the best cities to travel to in France according to [One-Week-In.com](https://one-week-in.com/35-cities-to-visit-in-france/)

## Usage
#### Scrap_best-cities.py
##### Scrapes the best cities to travel to in France from one-week-in's website
* Output file: Best_cities.json

#### Scrap_booking.py
##### Scrapes information about the top hotels for each destination from booking.com
* Output file: Hotels.json

#### Kayak.ipynb
##### Retrives the json files and dumps them in an amazon s3 bucket. It also cleans and formats them into csv files for storage in an amazon relational database service (RDS). Then it displays a plotly map that is the base for the kayak application.
* Input files : Hotels.json, Best_cities.json
* Output files: destination_weather.csv, hotels_data.csv

## Contributors

This project was made by Nicolas Leurs as part of the Jedha Bootcamp Data science and engineering Fullstack course and was submitted to validate part of the French certificate "Machine Learning Engineer".

